# Query 4: Security Model

**Status**: success
**Tokens Used**: 836
**Timestamp**: 2026-03-18T21:01:50.574643
**Tool Calls**: 4

---

I'll search the library for information about security measures in the librarian-MCP system.


Let me get more detailed information by reading the relevant documentation files.


Based on the library content, here's how the librarian-MCP system ensures security and protects sensitive files:

## Security Measures in Librarian-MCP

### 1. **`.librarianignore` File** [Source: .librarianignore]
The system uses a gitignore-style exclusion file that prevents indexing of sensitive content:

- **Credentials & Secrets**: `.env`, `*.env`, `credentials.*`, `*.key`, `*.pem`, `id_rsa`, `id_ed25519`
- **Version Control**: `.git/`, `.svn/`, `.hg/` (to avoid committing secrets)
- **Dependencies**: `venv/`, `node_modules/`, `__pycache__/`
- **Databases**: `*.db`, `chroma_db/` (the database itself isn't indexed)
- **Logs & Temp Files**: `*.log`, `logs/`, `tmp/`

### 2. **Directory Boundary Enforcement** [Source: search results]
- ❌ Cannot access files outside allowed directories
- All file operations are restricted to a safe working directory (configured via `LIBRARIAN_SAFE_DIR`)
- Path traversal attacks are prevented through validation that ensures resolved paths start within the base directory

### 3. **Command Restrictions** [Source: search results]
The system blocks dangerous commands including:
- File deletion/modification: `rm`, `rmdir`, `chmod`, `chown`
- Network operations: `wget`, `curl`, `ssh`, `scp`
- System utilities: `dd`, `mkfs`, `fdisk`, `mount`
- Shell interpreters: `bash`, `sh`, `python`, `perl`

### 4. **File Size Limits** [Source: search results]
- Documents larger than 100KB are excluded from indexing (configurable via `LIBRARIAN_MAX_DOCUMENT_SIZE`)
- Prevents accidental ingestion of large binary files or databases

### 5. **Timeout Protection** [Source: search results]
- Command execution has a timeout (default 15 seconds) to prevent runaway processes

### 6. **What Gets Stored vs Not Stored** [Source: search results]
**Indexed:**
- Document text content
- File metadata (name, path, size, modification time)
- Checksums for change detection

**NOT stored:**
- Passwords or credentials (unless in plain text documents that aren't ignored)
- Files matching `.librarianignore` patterns
- Original file contents in their original form (only indexed chunks)

### 7. **Layered Defense Approach** [Source: search results]
The documentation emphasizes "layered defense" - multiple security layers work together, but ultimately security is the user's responsibility to configure appropriately.

---

Would you like me to show you how to customize the `.librarianignore` file for your specific needs, or would you like to see the complete configuration options available?