# Query 4: Security Model

**Status**: success
**Tokens Used**: 1367
**Timestamp**: 2026-03-18T19:21:41.486845
**Tool Calls**: 5

---

I'll search the library for information about security measures and how the librarian-MCP system protects sensitive files.


Let me read the full content of these security-related documents to provide you with comprehensive information.


I found the SECURITY.md file. Let me read it to get comprehensive information about security measures.


Now let me also check the ignore patterns implementation to provide complete information.


Perfect! Now I have comprehensive information about the security measures. Let me provide a detailed answer with proper citations.

---

The librarian-MCP system implements **multiple layers of security** to protect sensitive files and ensure safe operation:

## Security Layers

### 1. **Librarian Persona (System Prompt)** [Source: SECURITY.md]
The AI model receives behavioral guidelines that explicitly prohibit accessing off-limits content:
- ❌ Don't access files outside the allowed directory
- ❌ Don't ignore `.librarianignore` exclusions
- ❌ Don't access sensitive files (.env, credentials, keys)
- ❌ DON'T EVER hallucinate or make up information when data is insufficient

### 2. **.librarianignore File** [Source: SECURITY.md], [Source: ignore_patterns.py]
A Gitignore-style exclusion file with **94+ built-in security patterns**:

**Security-Critical Files (Always Excluded):**
- `.env`, `*.env` - Environment files
- `credentials.*`, `*.key`, `*.pem` - Credentials and keys
- `id_rsa`, `id_ed25519` - SSH keys

**Development & Build:**
- `venv/`, `.venv/`, `virtualenv/` - Python virtual environments
- `node_modules/` - Node.js dependencies
- `__pycache__/`, `*.pyc` - Python cache
- `.git/`, `.svn/` - Version control

**Data & Databases:**
- `chroma_db/` - ChromaDB data (don't index the DB!)
- `metadata/` - Librarian metadata
- `*.db`, `*.sqlite`, `*.sqlite3` - Database files

### 3. **Command Whitelisting** [Source: SECURITY.md]
Only 17 safe commands are allowed; dangerous ones are explicitly blocked:

**Allowed Commands:** `ls`, `cd`, `pwd`, `whoami`, `echo`, `cat`, `find`, `grep`, `head`, `tail`, `sort`, `uniq`, `cut`, `awk`, `date`, `hostname`, `file`, `mkdir`, `stat`, `tree`, `wc`, `diff`, `test`

**Blocked Commands:** `rm`, `rmdir`, `chmod`, `chown`, `dd`, `mkfs`, `wget`, `curl`, `nc`, `netcat`, `ssh`, `scp`, `rsync`, `tar`, `zip`, `unzip`, `mount`, `umount`, and scripting languages

### 4. **Directory Sandboxing** [Source: SECURITY.md]
Prevents directory traversal attacks with path validation:
```python
# Critical security check ensures paths stay within safe directory
if not resolved.startswith(base):
    return False, "Path traversal detected"
```

Blocks attempts like:
- `read_document("../../../etc/passwd")` - Path traversal
- `read_document("/etc/shadow")` - Absolute path outside safe directory

### 5. **Output Truncation** [Source: SECURITY.md]
Limits output to protect LLM context window (default: 8000 chars, configurable via `LIBRARIAN_MAX_OUTPUT_CHARS`)

### 6. **Timeout Protection** [Source: SECURITY.md]
Prevents runaway commands with a default 15-second timeout (configurable via `LIBRARIAN_COMMAND_TIMEOUT`)

### 7. **File Size Limits** [Source: SECURITY.md]
Maximum document size of 10MB by default (`LIBRARIAN_MAX_DOCUMENT_SIZE`), preventing oversized documents from causing issues

## Write Access Security [Source: SECURITY.md]

The `write_document` tool provides a two-way communication channel with strict protections:

- **Subdirectory Restriction**: Writes only allowed in `/librarian/` subdirectory
- **File Size Limits**: Maximum 100KB per write operation
- **Critical File Protection**: Cannot overwrite files containing sensitive patterns (password, secret, key, credential, .env)
- **Directory Traversal Protection**: Same validation as read operations

## Backend Security [Source: SECURITY.md]

Both backends (**ChonkieBackend** and **ChromaBackend**) respect all security boundaries equally:
- ✅ Respects `.librarianignore`
- ✅ Applies file size limits
- ✅ Stores metadata securely

---

Would you like me to show you the current `.librarianignore` patterns in detail, or would you like to explore how any specific security layer works?