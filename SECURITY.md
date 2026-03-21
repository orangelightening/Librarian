# Security Model and Boundaries

Comprehensive security documentation for the Librarian MCP Server.

---

## Overview

The Librarian MCP Server implements **multiple layers of security** to ensure:
- ✅ Sensitive files are never indexed or accessed
- ✅ System directories remain protected
- ✅ Command execution is tightly controlled
- ✅ The librarian has clear behavioral guidelines
- ✅ Users control what content is included/excluded

**Both backends (Chonkie and ChromaDB) respect all security boundaries equally.**

---

## Security Layers

### Layer 1: Librarian Persona (System Prompt)

The AI model receives a comprehensive system prompt that defines behavioral boundaries:

**Core Principles**:
1. **Accuracy with Citations**: Always cite sources when providing library information
2. **Transparency About Limitations**: Acknowledge when information isn't found
3. **Respect for Boundaries**: Never access off-limits files or directories
4. **Helpfulness**: Provide comprehensive, actionable responses
5. **Security Conscious**: Protect sensitive information

**Critical Behavioral Rules**:
```
❌ Don't access files outside the allowed directory
❌ Don't ignore .librarianignore exclusions
❌ Don't fabricate citations or sources
❌ Don't claim information is in the library when it's not
❌ Don't access sensitive files (.env, credentials, keys)
❌ DON'T EVER hallucinate or make up information when data is insufficient
```

**Source**: See `System_prompt.md` in the project root

---

### Layer 2: .librarianignore File

**Location**: `/home/peter/development/librarian-mcp/.librarianignore`

**Purpose**: Gitignore-style file exclusion with **94+ built-in security patterns**

#### Built-in Exclusion Categories

**Security (Always Excluded)**:
- `.env`, `*.env`, `.env.*` - Environment files
- `credentials.*`, `*.key`, `*.pem` - Credentials and keys
- `id_rsa`, `id_ed25519` - SSH keys

**Development**:
- `venv/`, `.venv/`, `virtualenv/` - Python virtual environments
- `node_modules/` - Node.js dependencies
- `__pycache__/`, `*.pyc` - Python cache
- `.git/`, `.svn/` - Version control

**Build Artifacts**:
- `dist/`, `build/`, `target/` - Build outputs
- `*.egg-info/`, `.eggs/` - Python packages

**Data & Databases**:
- `chroma_db/` - ChromaDB data (don't index the DB!)
- `metadata/` - Librarian metadata
- `*.db`, `*.sqlite`, `*.sqlite3` - Database files

**Logs & Temp**:
- `*.log`, `logs/` - Log files
- `*.tmp`, `tmp/`, `temp/` - Temporary files
- `.cache/` - Cache directories

**Binary & Media**:
- `*.zip`, `*.tar`, `*.tar.gz` - Archives
- `*.exe`, `*.dll`, `*.so` - Binaries
- `*.png`, `*.jpg`, `*.pdf` - Binary files

#### How It Works

**Implementation**: `mcp_server/core/ignore_patterns.py`

```python
class IgnorePatterns:
    def is_ignored(self, file_path: Path) -> bool:
        """Check if file matches any ignore pattern."""
        # Check negation patterns first (exceptions)
        for pattern in self.negation_patterns:
            if self._matches_pattern(rel_path, pattern):
                return False  # Explicitly NOT ignored

        # Check ignore patterns
        for pattern in self.patterns:
            if self._matches_pattern(rel_path, pattern):
                return True  # Ignored

        return False
```

**Usage**:
```bash
# Add custom exclusions
echo "*.pdf" >> .librarianignore
echo "drafts/" >> .librarianignore

# Test patterns
python -c "
from mcp_server.core.ignore_patterns import IgnorePatterns
patterns = IgnorePatterns('.')
print(patterns.is_ignored(Path('venv/file.py')))  # True
"
```

**Reporting**: When you sync documents, the system shows:
```
Sync completed for directory: /home/peter/documents
  Added: 15 documents
  Updated: 3 documents
  Unchanged: 42 documents
  Ignored: 127 (excluded by .librarianignore)  ← Security in action!
```

---

### Layer 3: Command Whitelisting

**Implementation**: `mcp_server/tools/cli_tools.py`

**Allowed Commands** (17 binaries):
```python
ALLOWED_BINARY_NAMES = {
    "ls", "cd", "pwd", "whoami", "echo", "cat", "find", "grep",
    "head", "tail", "sort", "uniq", "cut", "awk", "date", "hostname",
    "file", "mkdir", "stat", "tree", "wc", "diff", "test"
}
```

**Dangerous Commands** (explicitly blocked):
```python
DANGEROUS_COMMANDS = {
    "rm", "rmdir", "chmod", "chown", "dd", "mkfs", "fdisk",
    "wget", "curl", "nc", "netcat", "ssh", "scp", "rsync",
    "tar", "zip", "unzip", "mount", "umount", "python",
    "python3", "perl", "bash", "sh", "zsh"
}
```

**Banned Flag Combinations**:
```python
BANNED_FLAG_COMBOS = {
    ("find", "-delete"),      # Can't delete via find
    ("find", "-exec"),        # Can't execute via find
    ("find", "-execdir"),     # Can't execute via find
    ("awk", "system"),        # Can't run system commands via awk
    ("awk", "systime"),       # Can't access time functions via awk
}
```

**Validation Function**:
```python
def is_safe_command(cmd: str, args: list) -> tuple[bool, str]:
    """Validate command against whitelist and banned flags."""
    cmd_name = os.path.basename(cmd)

    # Check dangerous commands
    if cmd_name in DANGEROUS_COMMANDS:
        return False, f"Command '{cmd_name}' is explicitly blocked."

    # Check whitelist
    if cmd_name not in ALLOWED_BINARY_NAMES:
        return False, f"Command '{cmd_name}' is not in the allowed list."

    # Check banned flag combinations
    args_str = ' '.join(args)
    for banned_cmd, banned_flag in BANNED_FLAG_COMBOS:
        if cmd_name == banned_cmd and banned_flag in args_str:
            return False, f"Flag '{banned_flag}' is not permitted with '{banned_cmd}'"

    return True, "OK"
```

---

### Layer 4: Directory Sandboxing

**Implementation**: `mcp_server/tools/cli_tools.py`

**Purpose**: Prevent directory traversal attacks

**Validation Function**:
```python
def is_safe_path(path: str, safe_dir: str) -> tuple[bool, str]:
    """Ensure path stays within safe directory."""
    try:
        base = os.path.realpath(os.path.expanduser(safe_dir))
        if os.path.isabs(path):
            resolved = os.path.realpath(path)
        else:
            resolved = os.path.realpath(os.path.join(base, path))

        # Critical security check
        if not resolved.startswith(base):
            return False, f"Path traversal detected: '{path}' escapes safe directory."

        return True, resolved
    except Exception as e:
        return False, f"Invalid path: {e}"
```

**Protected Operations**:
- `read_document(path)` - Can't read files outside safe directory
- `list_documents(path)` - Can't list directories outside safe directory
- `search_documents(query, path)` - Can't search outside safe directory
- `execute_command(command, args, cwd)` - Can't run commands outside safe directory

**Attack Prevention**:
```bash
# Blocked: Path traversal attempts
read_document("../../../etc/passwd")
# Result: [security error] Path traversal detected: '../../../etc/passwd' escapes safe directory.

# Blocked: Absolute paths outside safe directory
read_document("/etc/shadow")
# Result: [security error] Path traversal detected: '/etc/shadow' escapes safe directory.
```

---

### Layer 5: Output Truncation

**Purpose**: Protect LLM context window from overflow

**Implementation**: `mcp_server/tools/cli_tools.py`

```python
MAX_OUTPUT_CHARS = 8000  # Default limit

def truncate_output(text: str, limit: int = None) -> str:
    """Truncate output to protect LLM context window."""
    max_chars = limit if limit is not None else MAX_OUTPUT_CHARS
    if len(text) > max_chars:
        return text[:max_chars] + f"\n[output truncated — exceeded {max_chars} chars]"
    return text
```

**Configuration**:
```bash
export LIBRARIAN_MAX_OUTPUT_CHARS=16000  # Increase limit
```

**Affected Tools**:
- `execute_command()` - Command output
- `read_document()` - File contents (can override per-read)
- `search_documents()` - Search results
- `list_documents()` - File listings

---

### Layer 6: Timeout Protection

**Purpose**: Prevent runaway commands

**Implementation**: `mcp_server/tools/cli_tools.py`

```python
DEFAULT_TIMEOUT_SECONDS = 15

result = subprocess.run(
    full_cmd,
    capture_output=True,
    text=True,
    cwd=final_cwd,
    timeout=DEFAULT_TIMEOUT_SECONDS,
    shell=False
)
```

**Configuration**:
```bash
export LIBRARIAN_COMMAND_TIMEOUT=30  # 30 seconds
```

**Timeout Behavior**:
```python
except subprocess.TimeoutExpired:
    return f"[timeout]\nCommand timed out after {DEFAULT_TIMEOUT_SECONDS} seconds."
```

---

### Layer 7: File Size Limits

**Purpose**: Prevent oversized documents from causing issues

**Implementation**: `mcp_server/core/document_manager.py`

```python
MAX_DOCUMENT_SIZE = int(os.getenv("LIBRARIAN_MAX_DOCUMENT_SIZE", "10000000"))  # 10MB

def add_document(self, file_path: Path):
    if file_path.stat().st_size > MAX_DOCUMENT_SIZE:
        return {
            "status": "error",
            "error": f"Document exceeds maximum size of {MAX_DOCUMENT_SIZE} bytes"
        }
```

**Configuration**:
```bash
export LIBRARIAN_MAX_DOCUMENT_SIZE=50000000  # 50 MB
```

---

## MCP Tools Security

### Tool Count: 14 Total

**Library Tools** (7):
1. `search_library(query, limit)` - Semantic search (respects .librarianignore)
2. `sync_documents(path, extensions, recursive)` - Sync (respects .librarianignore)
3. `add_document(path)` - Add document (respects .librarianignore)
4. `remove_document(document_id)` - Remove by ID
5. `list_indexed_documents()` - List indexed docs
6. `get_document_status(path)` - Check status
7. `get_library_stats()` - Get statistics

**CLI Tools** (7):
1. `execute_command(command, args, cwd)` - Whitelisted commands only
2. `read_document(path, start_line, end_line, head, tail, max_chars)` - Sandboxed reads
3. `write_document(path, content, create_dirs)` - **Writes to `/librarian/` subdirectory only**
4. `list_documents(path, extension, recursive)` - Sandboxed listings
5. `search_documents(query, path, extension, case_sensitive)` - Sandboxed searches
6. `document_summary(path)` - Sandboxed summaries
7. `server_info()` - Show configuration

**All 14 tools respect security boundaries equally, regardless of backend.**

---

## Write Access Security

### Safe Write Operations

The `write_document` tool provides a **two-way communication channel** while maintaining strict security:

**Multiple Layers of Protection**:

1. **Subdirectory Restriction**: Writes only allowed in `/librarian/` subdirectory
   ```python
   # Path validation enforces librarian/ subdirectory
   librarian_dir = os.path.join(safe_dir, "librarian")
   if not resolved_path.startswith(librarian_dir):
       return "[security error] Write operations only allowed in /librarian/"
   ```

2. **File Size Limits**: Maximum 100KB per write operation
   ```python
   MAX_WRITE_FILE_SIZE = 100000  # 100KB
   if len(content) > MAX_WRITE_FILE_SIZE:
       return "[error] Content too large"
   ```

3. **Critical File Protection**: Cannot overwrite files with sensitive names
   ```python
   critical_patterns = ['password', 'secret', 'key', 'credential', '.env', 'config']
   for pattern in critical_patterns:
       if pattern in path_lower:
           return "[security error] Cannot write to files containing sensitive pattern"
   ```

4. **Audit Logging**: All write operations logged to console
   ```python
   print(f"[librarian-mcp] [write] {resolved_path} ({len(content)} bytes)")
   ```

5. **Directory Traversal Protection**: Same `is_safe_path()` validation as read operations
6. **Safe Directory Enforcement**: Must stay within `LIBRARIAN_SAFE_DIR` boundary

**Use Cases for Write Access**:
- ✅ Analysis results and reports
- ✅ Code change suggestions
- ✅ Documentation updates
- ✅ Debugging diagnostics
- ✅ Task delegation outputs

**User Review Process**:
1. Librarian writes analysis to `/librarian/analysis.md`
2. User reviews the file with `read_document('/librarian/analysis.md')`
3. User applies changes manually if approved
4. User can delete `/librarian/` files at any time

**Cannot Write To**:
- ❌ Files outside `/librarian/` subdirectory
- ❌ System configuration files
- ❌ Files with sensitive names (password, secret, key, etc.)
- ❌ Files larger than 100KB
- ❌ Files outside safe directory boundary

---

## Backend Security

### Both Backends Respect Security

**ChonkieBackend** (default):
- ✅ Respects .librarianignore
- ✅ Applies file size limits
- ✅ Stores metadata securely
- ✅ Same security as ChromaDB backend

**ChromaBackend** (optional):
- ✅ Respects .librarianignore
- ✅ Applies file size limits
- ✅ Stores metadata securely
- ✅ Same security as Chonkie backend

**Security is independent of backend choice.**

---

## Security Best Practices

### For Users

1. **Review .librarianignore**: Ensure sensitive files are excluded
2. **Set appropriate safe directory**: Restrict to necessary directories
3. **Use whitelist**: Only whitelist commands you actually need
4. **Monitor logs**: Check for security violations
5. **Keep updated**: Security improvements in future releases

### For Deployment

1. **Separate databases**: Don't store ChromaDB data in web-accessible directories
2. **Restrict safe directory**: Use minimal necessary directory
3. **File permissions**: Ensure proper file permissions on metadata
4. **Network isolation**: Run on localhost, not public interfaces
5. **Regular audits**: Periodically review indexed documents

---

## Security Audit Checklist

- [ ] .librarianignore excludes sensitive files
- [ ] Safe directory is minimal
- [ ] File permissions are correct (metadata, chroma_db)
- [ ] Command whitelist is minimal
- [ ] Timeout limits are appropriate
- [ ] Output truncation is enabled
- [ ] File size limits are set
- [ ] No documents contain credentials
- [ ] Server runs on localhost only
- [ ] Logs are monitored for violations

---

## Incident Response

If you discover a security issue:

1. **Stop the server**: `pkill -f librarian_mcp.py`
2. **Review logs**: Check for unauthorized access attempts
3. **Audit library**: `list_indexed_documents()` - check for sensitive docs
4. **Clear if needed**: Remove `.librarianignore` exclusions temporarily
5. **Report**: Document the issue and fix

---

## Security Limitations

### What This System Does NOT Protect Against

- **Malicious AI models**: The system assumes the AI model follows the system prompt
- **Compromised MCP clients**: If your MCP client is compromised, all bets are off
- **Network attacks**: If running on public interfaces (not recommended)
- **Physical access**: Someone with physical access can bypass all security

### Threat Model

**Protects against**:
- ✅ Accidental access to sensitive files
- ✅ AI model hallucinations about file contents
- ✅ Command execution mistakes
- ✅ Directory traversal attempts
- ✅ Oversized documents causing issues

**Does NOT protect against**:
- ❌ Malicious AI models
- ❌ Compromised MCP clients
- ❌ Direct file system access (bypassing librarian)
- ❌ Network attacks (if exposed publicly)

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [CONFIGURATION.md](CONFIGURATION.md) - Security configuration options
- [Tools.md](Tools.md) - Complete tool reference
- [.librarianignore](.librarianignore) - Current exclusion patterns

---

**Remember**: The best security is layered defense. This system provides multiple layers, but security is ultimately your responsibility as the operator.

*Last updated: Phase 2 Complete (Chonkie + ChromaDB dual backend)*
