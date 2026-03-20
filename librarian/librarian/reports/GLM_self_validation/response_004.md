# Response 004: How does the librarian-mcp system ensure security and protect sensitive files?

## Overview

The Librarian MCP Server implements a **defense-in-depth strategy** with **7 distinct security layers** to ensure sensitive files are never indexed or accessed, system directories remain protected, command execution is tightly controlled, and the librarian has clear behavioral guidelines [Source: SECURITY.md].

**Both backends (Chonkie and ChromaDB) respect all security boundaries equally** [Source: SECURITY.md].

---

## Security Layers

### Layer 1: Librarian Persona (System Prompt)

The AI model receives a comprehensive system prompt that defines behavioral boundaries [Source: SECURITY.md].

**Core Principles**:
1. **Accuracy with Citations** - Always cite sources when providing library information
2. **Transparency About Limitations** - Acknowledge when information isn't found
3. **Respect for Boundaries** - Never access off-limits files or directories
4. **Helpfulness** - Provide comprehensive, actionable responses
5. **Security Conscious** - Protect sensitive information [Source: SECURITY.md, prompt.md]

**Critical Behavioral Rules**:
```
❌ Don't access files outside the allowed directory
❌ Don't ignore .librarianignore exclusions
❌ Don't fabricate citations or sources
❌ Don't claim information is in the library when it's not
❌ Don't access sensitive files (.env, credentials, keys)
❌ DON'T EVER hallucinate or make up information when data is insufficient
```

**Source**: See `mcp_server/config/librarian_prompt.py` [Source: SECURITY.md]

---

### Layer 2: .librarianignore File

**Location**: `/home/peter/development/librarian-mcp/.librarianignore`

**Purpose**: Gitignore-style file exclusion with **94+ built-in security patterns** [Source: SECURITY.md]

#### Built-in Exclusion Categories

**Security (Always Excluded)**:
- `.env`, `*.env`, `.env.*` - Environment files
- `credentials.*`, `*.key`, `*.pem` - Credentials and keys
- `id_rsa`, `id_ed25519` - SSH keys [Source: SECURITY.md]

**Development**:
- `venv/`, `.venv/`, `virtualenv/` - Python virtual environments
- `node_modules/` - Node.js dependencies
- `__pycache__/`, `*.pyc` - Python cache
- `.git/`, `.svn/` - Version control [Source: SECURITY.md]

**Build Artifacts**:
- `dist/`, `build/`, `target/` - Build outputs
- `*.egg-info/`, `.eggs/` - Python packages [Source: SECURITY.md]

**Data & Databases**:
- `chroma_db/` - ChromaDB data (don't index the DB!)
- `metadata/` - Librarian metadata
- `*.db`, `*.sqlite`, `*.sqlite3` - Database files [Source: SECURITY.md]

**Logs & Temp**:
- `*.log`, `logs/` - Log files
- `*.tmp`, `tmp/`, `temp/` - Temporary files
- `.cache/` - Cache directories [Source: SECURITY.md]

**Binary & Media**:
- `*.zip`, `*.tar`, `*.tar.gz` - Archives
- `*.exe`, `*.dll`, `*.so` - Binaries
- `*.png`, `*.jpg`, `*.pdf` - Binary files [Source: SECURITY.md]

#### How It Works

**Implementation**: `mcp_server/core/ignore_patterns.py`

The `IgnorePatterns` class:
- Checks negation patterns first (exceptions)
- Checks ignore patterns
- Returns `True` if file should be ignored [Source: SECURITY.md]

**Usage**:
```bash
# Add custom exclusions
echo "*.pdf" >> .librarianignore
echo "drafts/" >> .librarianignore
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

**Implementation**: `mcp_server/tools/cli_tools.py` [Source: SECURITY.md]

**Allowed Commands** (22 binaries):
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

**Validation Process**:
1. Check if command is in `DANGEROUS_COMMANDS`
2. Check if command is in `ALLOWED_BINARY_NAMES`
3. Check for banned flag combinations
4. Only execute if all checks pass [Source: SECURITY.md]

---

### Layer 4: Directory Sandboxing

**Implementation**: `mcp_server/tools/cli_tools.py` [Source: SECURITY.md]

**Purpose**: Prevent directory traversal attacks

**Validation Function**:
```python
def is_safe_path(path: str, safe_dir: str) -> tuple[bool, str]:
    """Ensure path stays within safe directory."""
    base = os.path.realpath(os.path.expanduser(safe_dir))
    if os.path.isabs(path):
        resolved = os.path.realpath(path)
    else:
        resolved = os.path.realpath(os.path.join(base, path))

    # Critical security check
    if not resolved.startswith(base):
        return False, f"Path traversal detected: '{path}' escapes safe directory."

    return True, resolved
```

**Protected Operations**:
- `read_document(path)` - Can't read files outside safe directory
- `list_documents(path)` - Can't list directories outside safe directory
- `search_documents(query, path)` - Can't search outside safe directory
- `execute_command(command, args, cwd)` - Can't run commands outside safe directory [Source: SECURITY.md]

**Attack Prevention Examples**:
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

**Purpose**: Protect LLM context window from overflow [Source: SECURITY.md]

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
- `list_documents()` - File listings [Source: SECURITY.md]

---

### Layer 6: Timeout Protection

**Purpose**: Prevent runaway commands [Source: SECURITY.md]

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

**Purpose**: Prevent oversized documents from causing issues [Source: SECURITY.md]

**Configuration**:
```bash
export LIBRARIAN_MAX_DOCUMENT_SIZE=10000000  # 10MB default
```

Documents larger than this limit are rejected during ingestion, preventing memory issues and excessive processing time.

---

## Additional Security Features

### SHA-256 Checksums

The system uses SHA-256 checksums to track document changes automatically. This ensures that:
- Modified documents are detected and re-indexed
- Document integrity is maintained
- Tampering is identified [Source: README.md, ARCHITECTURE.md]

### Restricted Write Access

The librarian's write access is **strictly limited** to the `/librarian/` workspace subdirectory. This prevents:
- Unauthorized file modifications outside the workspace
- Accidental overwrites of user files
- Malicious code injection [Source: README.md, ARCHITECTURE.md]

---

## Security Summary Table

| Security Layer | Purpose | Implementation |
|---------------|---------|----------------|
| **System Prompt** | Behavioral boundaries | `prompt.md`, `librarian_prompt.py` |
| **.librarianignore** | File exclusion patterns | `ignore_patterns.py` (94+ patterns) |
| **Command Whitelist** | Restrict executable commands | `cli_tools.py` (22 allowed binaries) |
| **Directory Sandbox** | Prevent path traversal | `is_safe_path()` validation |
| **Output Truncation** | Protect LLM context | `truncate_output()` (8000 chars) |
| **Timeout Protection** | Prevent runaway commands | 15 second timeout |
| **File Size Limits** | Prevent oversized docs | 10MB limit |

---

## Best Practices

**Keep .librarianignore updated**: Add project-specific exclusions as needed [Source: SECURITY.md]

**Monitor sync output**: Review "Ignored" counts to ensure security patterns are working correctly.

**Use environment variables**: Configure security settings (timeout, output limits, file sizes) to match your needs.

**Review command usage**: Be aware of which commands are allowed and blocked before relying on command execution.

---

## What Is NOT Protected

The system does NOT protect against [Source: SECURITY.md]:
- Direct file system access (bypassing librarian)
- Network attacks (if exposed publicly)

**Remember**: The best security is layered defense. This system provides multiple layers, but security is ultimately your responsibility [Source: SECURITY.md].
