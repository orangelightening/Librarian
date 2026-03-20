# Query 4: Security Model

**Status**: success
**Tokens Used**: 1536
**Timestamp**: 2026-03-18T23:47:19.325210
**Tool Calls**: 0

---

I'll search the library for information about how the librarian-mcp system ensures security and protects sensitive files.


Let me get more detailed information about the security features by reading the architecture and configuration documents.




Let me also check the Tools.md file for more specific security information.


Now let me check the .librarianignore file to see the current exclusion patterns:


Let me try reading the file differently:


Now I have comprehensive information. Let me provide a complete answer about the security measures:

---

Based on the library, the librarian-mcp system implements **multiple layers of security** to protect sensitive files and ensure safe access. Here's a comprehensive overview:

## 🔒 Core Security Mechanisms

### 1. **System Prompt Enforcement**
[Source: ARCHITECTURE.md]
- All librarian behavior is governed by `prompt.md` - a comprehensive system prompt
- Defines behavioral principles, citation requirements, and **security boundaries**
- Automatically loaded by the MCP server - no manual configuration needed
- Ensures consistent, accurate, and well-cited responses while respecting security rules

### 2. **Safe Directory Boundary**
[Source: CONFIGURATION.md]
- **`LIBRARIAN_SAFE_DIR`** environment variable sets the sandbox boundary (default: `$HOME`)
- CLI tools (`execute_command`, `read_document`, etc.) **cannot access files outside this directory**
- Prevents directory traversal attacks
- All operations are restricted within this boundary

### 3. **File Size Limits**
[Source: CONFIGURATION.md, Tools.md]
- **Maximum 10 MB** for document ingestion (`LIBRARIAN_MAX_DOCUMENT_SIZE`)
- **Maximum 100 KB** per file for write operations
- Prevents memory issues and context overflow
- Large documents are automatically rejected

### 4. **Sensitive File Blocking**
[Source: Tools.md, .librarianignore]
- **Critical filename blocking** for sensitive files:
  - `.env`, `*.env`, `credentials.*`, `*.key`, `*.pem`
  - `id_rsa`, `id_ed25519` (SSH keys)
  - `*.secrets`, `*.creds`
  - `password`, `secret`, `key`, `credential` patterns
  
### 5. **.librarianignore Integration**
[Source: .librarianignore, CONFIGURATION.md]
- Uses **gitignore-style patterns** to exclude files from indexing and access
- Excludes:
  - **Security files**: `.env`, SSH keys, credentials
  - **Version control**: `.git/`, `.svn/`, `.hg/`
  - **Dependencies**: `venv/`, `node_modules/`, `__pycache__/`
  - **Build artifacts**: `dist/`, `build/`, `*.pyc`
  - **IDE files**: `.vscode/`, `.idea/`
  - **Logs and temp files**: `*.log`, `*.tmp`, `logs/`
  - **Librarian workspace**: `librarian/` (transient analysis reports)
- Both backends (Chonkie and Chroma) **respect these exclusions**

### 6. **Whitelisted Commands Only**
[Source: Tools.md]
- Only a specific set of commands can be executed:
  ```
  awk, cat, cd, cut, date, diff, echo, file, find, grep, head, 
  hostname, ls, mkdir, pwd, sort, stat, tail, test, tree, uniq, wc, whoami
  ```
- Prevents execution of arbitrary or dangerous commands
- All command execution is restricted to the safe directory

### 7. **Write Access Restrictions**
[Source: Tools.md]
- **7 Layers of Protection** for write operations:
  - ✅ Writes ONLY allowed in `/librarian/` subdirectory
  - ✅ Maximum 100KB per file
  - ✅ Critical filename blocking (password, secret, key, credential, .env, config)
  - ✅ Directory traversal protection
  - ✅ Audit logging (all writes logged to console)
  - ✅ Safe directory boundary enforcement
  - ✅ Manual review required (you control what gets applied)

### 8. **Backend Abstraction**
[Source: ARCHITECTURE.md]
- All backends implement `DocumentBackend` abstract base class
- Both **ChonkieBackend** and **ChromaBackend** respect security rules
- Consistent security across different backend implementations

## 🛡️ What the System Does NOT Protect Against

[Source: ARCHITECTURE.md]
- **Malicious AI models**: Assumes the AI model follows the system prompt
- **Compromised MCP clients**: If your MCP client is compromised, all bets are off
- **Network attacks**: If running on public interfaces without proper authentication
- **User error**: Human mistakes can still lead to security issues

## 📋 Security Best Practices

[Source: ARCHITECTURE.md]
1. **Audit library**: Use `list_indexed_documents()` to check for sensitive docs
2. **Remove exclusions temporarily**: If needed, remove `.librarianignore` exclusions
3. **Report issues**: Document problems and fix them
4. **Keep .librarianignore updated**: Add project-specific exclusions as needed

## 🎯 Summary

The librarian-mcp system employs a **defense-in-depth strategy** with:
- System prompt enforcement for behavioral security
- Safe directory boundaries to limit access scope
- File size limits to prevent resource exhaustion
- Sensitive file blocking to protect credentials
- .librarianignore integration for flexible exclusions
- Whitelisted command execution
- Restricted write access with audit logging

This multi-layered approach ensures that even if one security measure fails, others provide protection. The key principle is that **security is ultimately your responsibility**, and the system provides robust defaults but requires proper configuration and maintenance.

Would you like me to search for more specific security details or help you configure any security settings?
