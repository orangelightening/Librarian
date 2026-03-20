# Query 4: Security and Sensitive File Protection

## How the Librarian-MCP System Ensures Security and Protects Sensitive Files

The librarian-mcp system implements a comprehensive **defense-in-depth security strategy** with multiple layers of protection designed to ensure sensitive files are never indexed or accessed.

---

## 7 Layers of Protection

### Layer 1: Librarian Persona (System Prompt)
The AI model receives a comprehensive system prompt that defines behavioral boundaries and core principles:

- **Accuracy with Citations**: Always cite sources when providing library information [Source: ARCHITECTURE.md]
- **Transparency About Limitations**: Acknowledge when information isn't found [Source: ARCHITECTURE.md]
- **Respect for Boundaries**: Never access off-limits files or directories [Source: SECURITY.md]
- **Security Conscious**: Protect sensitive information [Source: SECURITY.md]
- **Critical Behavioral Rules**:
  - ❌ Don't access files outside the allowed directory [Source: SECURITY.md]
  - ❌ Don't ignore .librarianignore exclusions [Source: SECURITY.md]
  - ❌ Don't fabricate citations or sources [Source: SECURITY.md]
  - ❌ Don't access sensitive files (.env, credentials, keys) [Source: SECURITY.md]

**Source**: `mcp_server/config/librarian_prompt.py` defines `LIBRARIAN_SYSTEM_PROMPT` with these behavioral guidelines.

---

### Layer 2: .librarianignore File (94+ Built-in Patterns)
The `.librarianignore` file uses gitignore-style patterns to exclude files before they are ever processed:

**Security (Always Excluded)**:
- `.env`, `*.env`, `.env.*` - Environment files [Source: SECURITY.md]
- `credentials.*`, `*.key`, `*.pem` - Credentials and keys [Source: SECURITY.md]
- `id_rsa`, `id_ed25519` - SSH keys [Source: SECURITY.md]

**Development Artifacts**:
- `venv/`, `.venv/`, `virtualenv/` - Python virtual environments [Source: SECURITY.md]
- `node_modules/` - Node.js dependencies [Source: SECURITY.md]
- `__pycache__/`, `*.pyc` - Python cache [Source: SECURITY.md]
- `.git/`, `.svn/` - Version control [Source: SECURITY.md]

**Data & Databases**:
- `chroma_db/` - ChromaDB data (don't index the DB!) [Source: SECURITY.md]
- `metadata/` - Librarian metadata [Source: SECURITY.md]
- `*.db`, `*.sqlite`, `*.sqlite3` - Database files [Source: SECURITY.md]

**Logs & Temp Files**:
- `*.log`, `logs/` - Log files [Source: SECURITY.md]
- `*.tmp`, `tmp/`, `temp/` - Temporary files [Source: SECURITY.md]

**Binary & Media Files**:
- `*.zip`, `*.tar`, `*.tar.gz` - Archives [Source: SECURITY.md]
- `*.exe`, `*.dll`, `*.so` - Binaries [Source: SECURITY.md]
- `*.png`, `*.jpg`, `*.pdf` - Binary files [Source: SECURITY.md]

**Implementation**: `mcp_server/core/ignore_patterns.py` checks if files match any ignore pattern before processing.

---

### Layer 3: Command Whitelisting
The system maintains strict command execution controls:

**Allowed Commands** (17 binaries):
- `ls`, `cd`, `pwd`, `whoami`, `echo`, `cat`, `find`, `grep`, `head`, `tail`, `sort`, `uniq`, `cut`, `awk`, `date`, `hostname`, `file`, `mkdir`, `stat`, `tree`, `wc`, `diff`, `test` [Source: SECURITY.md]

**Dangerous Commands** (explicitly blocked):
- `rm`, `rmdir`, `chmod`, `chown`, `dd`, `mkfs`, `fdisk`, `wget`, `curl`, `nc`, `netcat`, `ssh`, `scp`, `rsync`, `tar`, `zip`, `unzip`, `mount`, `umount`, `python`, `python3`, `perl`, `bash`, `sh`, `zsh` [Source: SECURITY.md]

**Banned Flag Combinations**:
- `find -delete`, `find -exec`, `find -execdir` [Source: SECURITY.md]
- `awk system`, `awk systime` [Source: SECURITY.md]

---

### Layer 4: Directory Sandboxing
Directory traversal attacks are prevented through path validation:

```python
def is_safe_path(path: str, safe_dir: str) -> tuple[bool, str]:
    """Ensure path stays within safe directory."""
    # Critical security check - prevents directory traversal
    if not resolved.startswith(base):
        return False, f"Path traversal detected..."
```

All file operations (`read_document`, `list_documents`, `search_documents`, `execute_command`) are restricted to the safe directory boundary [Source: SECURITY.md].

---

### Layer 5: Output Truncation
Maximum output is limited to protect the LLM context window:
- Default: `LIBRARIAN_MAX_OUTPUT_CHARS=8000` [Source: SECURITY.md]
- Affects: `execute_command()`, `read_document()`, `search_documents()`, `list_documents()` [Source: SECURITY.md]

---

### Layer 6: Timeout Protection
Command execution has configurable timeouts:
- Default: `LIBRARIAN_COMMAND_TIMEOUT=15` seconds [Source: SECURITY.md]
- Prevents runaway commands that could exhaust system resources [Source: SECURITY.md]

---

### Layer 7: File Size Limits
Documents exceeding size limits are rejected:
- Default: `LIBRARIAN_MAX_DOCUMENT_SIZE=10000000` (10 MB) [Source: SECURITY.md]
- Prevents memory exhaustion from large file processing [Source: SECURITY.md]

---

## Backend Security

**Both backends (Chonkie and ChromaDB) respect all security boundaries equally**:

- ✅ Respects .librarianignore
- ✅ Applies file size limits
- ✅ Stores metadata securely
- ✅ Same security as each other [Source: SECURITY.md]

---

## Summary

The librarian-mcp system provides **multiple layers of security**:
1. System prompt enforcement for behavioral security
2. Safe directory boundaries to limit access scope
3. File size limits to prevent resource exhaustion
4. Sensitive file blocking to protect credentials
5. .librarianignore integration for flexible exclusions
6. Whitelisted command execution
7. Restricted write access to `/librarian/` workspace only [Source: SECURITY.md]

---

## References
- [Source: SECURITY.md] - Comprehensive security documentation
- [Source: ARCHITECTURE.md] - System architecture overview
- [Source: CONFIGURATION.md] - Security configuration options
- [Source: Tools.md] - Complete tool reference
- [Source: .librarianignore] - Current exclusion patterns