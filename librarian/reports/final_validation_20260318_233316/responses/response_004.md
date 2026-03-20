# Query 4: Security Model

**Status**: success
**Tokens Used**: 1055
**Timestamp**: 2026-03-18T23:33:16.592997
**Tool Calls**: 0

---

Based on my search of the library, the librarian-mcp system implements **multiple layers of security** to protect sensitive files and ensure safe operation:

## Security Layers

### **Layer 1: Librarian Persona (System Prompt)**
The AI model operates under strict behavioral guidelines that explicitly prohibit:
- Accessing files outside the allowed directory
- Ignoring `.librarianignore` exclusions
- Fabricating citations or sources
- Accessing sensitive files (`.env`, credentials, keys)
- Hallucinating information when data is insufficient

### **Layer 2: `.librarianignore` File**
A Gitignore-style exclusion file with **94+ built-in security patterns** that automatically blocks:

**Security-critical exclusions:**
- `.env`, `*.env`, `.env.*` - Environment files
- `credentials.*`, `*.key`, `*.pem` - Credentials and keys  
- `id_rsa`, `id_ed25519` - SSH keys
- `*.db`, `*.sqlite`, `*.sqlite3` - Database files

**Development artifacts:**
- `venv/`, `node_modules/`, `__pycache__/`, `.git/`
- `*.log`, `*.tmp`, `*.cache/`

**Binary & media files:**
- `*.zip`, `*.tar`, `*.exe`, `*.dll`, `*.png`, `*.pdf`

### **Layer 3: Command Whitelisting**
Only **17 safe commands** are allowed:
- `ls`, `cd`, `pwd`, `whoami`, `echo`, `cat`, `find`, `grep`, `head`, `tail`, `sort`, `uniq`, `cut`, `awk`, `date`, `hostname`, `file`

**Dangerous commands are explicitly blocked:**
- `rm`, `rmdir`, `chmod`, `chown`, `wget`, `curl`, `nc`, `netcat`, `ssh`, `scp`, `tar`, `zip`, `python`, `bash`, `sh`

**Banned flag combinations** prevent dangerous combinations like `find -delete` or `awk system()`.

### **Layer 4: Directory Sandboxing**
All file operations are validated to prevent directory traversal attacks:
- Paths are resolved to real paths
- Absolute paths are checked against the safe directory boundary
- Any attempt to escape the allowed directory is blocked with a security error

### **Layer 5: Output Truncation**
Limits output to **8,000 characters** (configurable up to 16,000) to protect the LLM context window from overflow.

### **Layer 6: Timeout Protection**
Commands have execution timeouts to prevent runaway processes.

### **Layer 7: File Size Limits**
- **Document size**: Maximum 10MB for indexed documents (configurable up to 50MB)
- **Write operations**: Maximum 100KB per write
- Prevents memory exhaustion from large files

## Write Access Security

The `write_document` tool provides limited write access with additional protections:
- Writes only to `/librarian/` subdirectory
- Cannot overwrite files with sensitive names (password, secret, key, .env, config)
- All write operations are logged
- User must manually review and approve any written content

## Security Audit Checklist

The system provides a comprehensive checklist for users to verify their security configuration:
- ✅ `.librarianignore` excludes sensitive files
- ✅ Safe directory is minimal
- ✅ File permissions are correct
- ✅ Command whitelist is minimal
- ✅ Server runs on localhost only
- ✅ Logs are monitored for violations

## Security Limitations

The system explicitly acknowledges what it **does NOT protect against**:
- Malicious AI models (assumes the model follows the system prompt)
- Compromised MCP clients
- Direct file system access bypassing the librarian
- Network attacks if exposed publicly
- Physical access to the system

The system's security philosophy is **layered defense**, where each layer adds protection, but ultimately security is the operator's responsibility.
