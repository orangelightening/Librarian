# Librarian Security and Boundaries

## Overview

The Librarian MCP Server has robust security boundaries and content filtering to ensure:
- ✅ Sensitive files are never indexed or accessed
- ✅ System directories remain protected
- ✅ The librarian has clear behavioral guidelines
- ✅ Users control what content is included/excluded

---

## 1. Librarian Persona (System Prompt)

### Role Definition

The AI model receives a comprehensive system prompt that defines:

**Core Responsibilities:**
- **Research Assistant**: Helps users discover and understand information
- **Search Expert**: Uses semantic search to find relevant content
- **Citation Provider**: Always references source documents
- **Librarian**: Manages and organizes the document collection

**Behavioral Principles:**
1. **Accuracy with Citations**: Always cite sources when providing library information
2. **Transparency About Limitations**: Acknowledge when information isn't found
3. **Respect for Boundaries**: Never access off-limits files or directories
4. **Helpfulness**: Provide comprehensive, actionable responses
5. **Security Conscious**: Protect sensitive information

### Example Instructions

```
You are the Librarian, an intelligent research assistant with access to a
curated document library and secure file system tools.

## Core Principles

### Accuracy and Citations
- ALWAYS cite sources when providing information from the library
- Use the format: [Source: document_name.md]
- Distinguish between library content and general knowledge

### Secure and Respectful
- Only access files within the allowed scope
- Respect the .librarianignore file - excluded content is off-limits
- Never attempt to bypass security restrictions
- Protect sensitive information (credentials, private keys, etc.)

### What You Don't Do
❌ Don't access files outside the allowed directory
❌ Don't ignore .librarianignore exclusions
❌ Don't fabricate citations or sources
❌ Don't claim information is in the library when it's not
❌ Don't access sensitive files (.env, credentials, keys)
```

---

## 2. Off-Limits Areas

### Automatic Exclusions

The following are **automatically excluded** from indexing and access:

#### Security & Credentials
- `.env`, `.env.*`, `*.env` - Environment files
- `credentials.*`, `*.creds`, `*.secrets` - Credential files
- `*.key`, `*.pem`, `id_rsa`, `id_ed25519` - Cryptographic keys
- `.secrets`, `*.secrets` - Secret files

#### System Directories
- Version control: `.git/`, `.svn/`, `.hg/`
- Dependencies: `venv/`, `.venv/`, `virtualenv/`, `node_modules/`
- Build artifacts: `dist/`, `build/`, `target/`, `out/`
- IDE files: `.vscode/`, `.idea/`, `*.swp`
- OS files: `.DS_Store`, `Thumbs.db`

#### Database & Data
- `chroma_db/` - ChromaDB data directory
- `*.db`, `*.sqlite`, `*.sqlite3` - Database files
- `metadata/` - Librarian metadata

#### Logs & Temp
- `*.log`, `logs/` - Log files
- `*.tmp`, `*.temp`, `tmp/`, `temp/` - Temporary files
- `.cache/` - Cache directories

#### Binary & Media
- Archives: `*.zip`, `*.tar`, `*.tar.gz`, `*.rar`
- Binaries: `*.exe`, `*.dll`, `*.so`, `*.dylib`, `*.bin`
- Images: `*.png`, `*.jpg`, `*.jpeg`, `*.gif`
- Media: `*.mp4`, `*.mp3`, `*.wav`, `*.avi`
- Documents: `*.pdf` (too large for text processing)

#### Testing & Build
- `__pycache__/`, `*.pyc`, `*.pyo` - Python cache
- `.pytest_cache/`, `.tox/`, `.nox/` - Test cache
- `*.egg-info/`, `.eggs/`, `dist/` - Python build artifacts

### Custom Exclusions (`.librarianignore`)

Users can add custom exclusions via the `.librarianignore` file:

```gitignore
# Project-specific
node_modules/
.vscode/
build/
dist/

# Personal
documents/private/
work/confidential/

# Temporary
*.draft
tmp/
```

---

## 3. The `.librarianignore` File

### Location

**Root of the library directory:**
```
/home/peter/development/librarian-mcp/.librarianignore
```

### Format

Uses **gitignore-style patterns**:

```gitignore
# Comments start with #

# Exact file names
.env
credentials.json

# Wildcard patterns
*.log
*.tmp
secret_*

# Directory patterns (ending with /)
venv/
node_modules/
private/

# Patterns in any directory
**/config.ini
**/temp/
```

### Pattern Examples

| Pattern | Matches |
|---------|---------|
| `.env` | `.env` file anywhere |
| `*.log` | All `.log` files |
| `venv/` | Any `venv` directory |
| `temp/` | Any `temp` directory |
| `**/config.ini` | `config.ini` anywhere |
| `documents/private/` | That specific path |
| `*.tmp` | All `.tmp` files |

### Negation Patterns

**Override exclusions** with `!`:

```gitignore
# Ignore all logs
*.log

# But allow important.log
!important.log

# Ignore node_modules
node_modules/

# But allow this specific one
!node_modules/important-package/
```

### How It Works

1. **Discovery Phase**: When scanning directories, the ignore patterns are applied
2. **Filtering**: Matching files are excluded from indexing
3. **Reporting**: Sync operations report how many files were ignored
4. **Respect**: All tools respect the ignore patterns

### Example Output

```
Sync completed for directory: /home/peter/documents
  Added: 15 documents
  Updated: 3 documents
  Unchanged: 42 documents
  Removed: 0 documents
  Ignored: 127 (excluded by .librarianignore)
```

---

## 4. Security Boundaries

### CLI Tool Security

**File Access Boundaries:**
- All file operations restricted to `--safe-dir`
- Path traversal attacks prevented
- Symlink escape blocked
- Absolute path validation

**Command Execution Security:**
- Whitelist of allowed commands only
- Dangerous flags blocked
- Timeout protection (15 seconds)
- Output truncation (8000 chars)

**Example:**
```bash
# Allowed
list_documents(path="~/documents")
read_document(path="~/notes.md")

# Blocked (path traversal)
read_document(path="../../../etc/passwd")

# Blocked (dangerous command)
execute_command(command="rm", args=["-rf", "/"])
```

### Library Tool Security

**Document Size Limits:**
- Maximum: 10MB per document (configurable)
- Prevents memory issues
- Large files skipped with error message

**Extension Whitelist:**
- Only text-based files indexed
- Supported: `.md`, `.txt`, `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.rst`, `.html`
- Binary files automatically excluded

**Change Detection:**
- SHA-256 checksums track modifications
- Prevents re-indexing unchanged files
- Detects tampering

---

## 5. Best Practices

### For Users

**Do:**
✅ Use `.librarianignore` to exclude sensitive content
✅ Keep credentials in `.env` files (auto-excluded)
✅ Place private documents in excluded directories
✅ Review ignored count in sync reports
✅ Test with small document collections first

**Don't:**
❌ Store credentials in supported file types (`.md`, `.txt`)
❌ Put sensitive data in `documents/` without exclusions
❌ Disable ignore patterns unless you understand the risks
❌ Index entire home directory (too broad)

### For Developers

**Adding Patterns:**
```python
# In .librarianignore
# Add project-specific exclusions
internal/
confidential/
*.secret
```

**Testing Security:**
```bash
# Test that exclusions work
python scripts/ingest.py --path ~/documents
# Check "Ignored" count in output

# Test specific files
python -c "
from mcp_server.core.ignore_patterns import IgnorePatterns
ignore = IgnorePatterns('/path/to/library')
print(ignore.is_ignored(Path('/path/to/library/.env')))
"
```

---

## 6. Configuration

### Environment Variables

```bash
# Security limits
export LIBRARIAN_MAX_DOCUMENT_SIZE=10000000  # 10MB
export LIBRARIAN_MAX_OUTPUT_CHARS=8000
export LIBRARIAN_COMMAND_TIMEOUT=15

# Paths
export LIBRARIAN_SAFE_DIR=/home/peter/development
export LIBRARIAN_DOCUMENTS_DIR=/home/peter/documents
export LIBRARIAN_CHROMA_PATH=/home/peter/librarian-mcp/chroma_db
export LIBRARIAN_METADATA_PATH=/home/peter/librarian-mcp/metadata
```

### Command Line Options

```bash
python mcp_server/librarian_mcp.py \
  --safe-dir /home/peter/development \
  --documents-dir /home/peter/documents
```

---

## 7. Auditing

### Check What's Indexed

```bash
# From MCP client
list_indexed_documents()

# From command line
python -c "
from mcp_server.core.document_manager import DocumentManager
from mcp_server.backend.chroma_backend import ChromaBackend
from mcp_server.core.metadata_store import MetadataStore

dm = DocumentManager(ChromaBackend(), MetadataStore())
for doc in dm.list_indexed():
    print(f'{doc[\"path\"]}')
"
```

### Check What's Ignored

```bash
# Test specific files
python -c "
from mcp_server.core.ignore_patterns import IgnorePatterns
from pathlib import Path

ignore = IgnorePatterns('/home/peter/documents')
test_files = Path('/home/peter/documents').rglob('*')
for f in test_files:
    if ignore.is_ignored(f):
        print(f'Ignored: {f}')
"
```

---

## Summary

✅ **The Librarian has clear behavioral guidelines** - helpful, accurate, cites sources, respects boundaries

✅ **Multiple layers of security** - ignore patterns, CLI restrictions, file validation

✅ **`.librarianignore` provides control** - users decide what's excluded using familiar gitignore syntax

✅ **Sensitive content protected by default** - credentials, system directories, build artifacts auto-excluded

✅ **Transparent operation** - sync reports show how many files were ignored

The librarian is **designed to be secure by default** while giving users full control over their content boundaries.
