# Configuration Reference

Complete configuration guide for the Librarian MCP Server.

---

## System Prompt

The librarian's behavior is defined by `System_prompt.md` in the project root. This comprehensive system prompt specifies:

- **Role Definition**: AI model acts as an intelligent research assistant
- **Core Principles**: Accuracy with citations, transparency, respecting boundaries
- **Behavioral Guidelines**: How to search, cite sources, acknowledge limitations
- **Security Rules**: What not to access, how to handle sensitive data
- **Response Format**: How to structure answers with proper citations

**The system prompt is automatically loaded by the MCP server** - you don't need to manually configure it. If you want to modify the librarian's behavior, edit `System_prompt.md` and restart the server.

## Quick Configuration

**Default Setup** (Chonkie backend, standard paths):
```bash
cd /home/peter/development/librarian-mcp
source venv/bin/activate
./setup_mcp.sh
```

**Custom Backend** (ChromaDB instead of Chonkie):
```bash
export LIBRARIAN_BACKEND=chroma
./setup_mcp.sh
```

---

## Environment Variables

### Backend Selection

#### `LIBRARIAN_BACKEND`
**Purpose**: Select document processing backend

**Options**:
- `chonkie` (default) - Intelligent semantic chunking
- `chroma` - Simple sentence-based chunking

**Example**:
```bash
export LIBRARIAN_BACKEND=chonkie
```

**Recommendation**: Use `chonkie` for better search results. Only use `chroma` if you need faster processing speed.

---

### Directory Paths

#### `LIBRARIAN_SAFE_DIR`
**Purpose**: Root directory for CLI tool operations (sandbox boundary)

**Default**: `$HOME` (your home directory)

**Example**:
```bash
export LIBRARIAN_SAFE_DIR=/home/peter/development/librarian-mcp
```

**Notes**:
- CLI tools cannot access files outside this directory
- All `execute_command`, `read_document`, etc. operations are restricted
- Prevents directory traversal attacks

---

#### `LIBRARIAN_DOCUMENTS_DIR`
**Purpose**: Default location for document storage

**Default**: `./documents` (relative to project root)

**Example**:
```bash
export LIBRARIAN_DOCUMENTS_DIR=/home/peter/documents
```

**Notes**:
- Used by ingestion scripts
- Can be overridden in tool calls

---

#### `LIBRARIAN_CHROMA_PATH`
**Purpose**: ChromaDB database storage location

**Default**: `./chroma_db`

**Example**:
```bash
export LIBRARIAN_CHROMA_PATH=/home/peter/librarian-data/chroma
```

**Notes**:
- Stores vector embeddings and metadata
- Can be large (grows with document collection)
- Safe to backup/move

---

#### `LIBRARIAN_METADATA_PATH`
**Purpose**: Document metadata storage location

**Default**: `./metadata`

**Example**:
```bash
export LIBRARIAN_METADATA_PATH=/home/peter/librarian-data/metadata
```

**Notes**:
- Stores `index.json` with document checksums
- Tracks which documents have been indexed
- Safe to backup/move

---

### Document Processing

#### `LIBRARIAN_MAX_DOCUMENT_SIZE`
**Purpose**: Maximum file size for document ingestion

**Default**: `10000000` (10 MB)

**Example**:
```bash
export LIBRARIAN_MAX_DOCUMENT_SIZE=50000000  # 50 MB
```

**Notes**:
- Larger documents are rejected
- Prevents memory issues
- Adjust if you regularly process large files

---

#### `LIBRARIAN_CHUNK_SIZE`
**Purpose**: Target chunk size for document splitting

**Default**: `1000` (characters)

**Example**:
```bash
export LIBRARIAN_CHUNK_SIZE=2000
```

**Notes**:
- Chonkie uses this as a guideline (respects semantic boundaries)
- ChromaDB backend tries to match this exactly
- Larger chunks = more context per chunk
- Smaller chunks = more precise search results

---

### Security Limits

#### `LIBRARIAN_MAX_OUTPUT_CHARS`
**Purpose**: Maximum output size for CLI tools

**Default**: `8000` (characters)

**Example**:
```bash
export LIBRARIAN_MAX_OUTPUT_CHARS=16000  # 16 KB
```

**Notes**:
- Protects LLM context window
- Larger values may cause context overflow
- Affects `execute_command`, `read_document`, `search_documents`

---

#### `LIBRARIAN_COMMAND_TIMEOUT`
**Purpose**: Maximum execution time for CLI commands

**Default**: `15` (seconds)

**Example**:
```bash
export LIBRARIAN_COMMAND_TIMEOUT=30  # 30 seconds
```

**Notes**:
- Prevents runaway commands
- Affects `execute_command` only
- Increase for long-running operations

---

### Chonkie Settings (Phase 2)

#### `LIBRARIAN_CHONKIE_URL`
**Purpose**: Chonkie service URL (for future remote Chonkie deployment)

**Default**: `http://localhost:8000`

**Example**:
```bash
export LIBRARIAN_CHONKIE_URL=http://chonkie-server:8000
```

**Notes**:
- Currently not used (Chonkie runs in-process)
- Reserved for future distributed deployments
- Can be ignored for now

---

## Command-Line Arguments

The `librarian_mcp.py` server accepts these arguments:

### `--safe-dir`
**Purpose**: Override safe directory for CLI operations

**Example**:
```bash
python mcp_server/librarian_mcp.py --safe-dir /home/peter/projects
```

**Overrides**: `LIBRARIAN_SAFE_DIR` environment variable

---

### `--documents-dir`
**Purpose**: Override default documents directory

**Example**:
```bash
python mcp_server/librarian_mcp.py --documents-dir ~/my-docs
```

**Overrides**: `LIBRARIAN_DOCUMENTS_DIR` environment variable

---

### `--chroma-path`
**Purpose**: Override ChromaDB storage location

**Example**:
```bash
python mcp_server/librarian_mcp.py --chroma-path /data/chroma
```

**Overrides**: `LIBRARIAN_CHROMA_PATH` environment variable

---

### `--metadata-path`
**Purpose**: Override metadata storage location

**Example**:
```bash
python mcp_server/librarian_mcp.py --metadata-path /data/metadata
```

**Overrides**: `LIBRARIAN_METADATA_PATH` environment variable

---

## Precedence Order

Configuration is applied in this order (later overrides earlier):

1. **Code defaults** (in `settings.py`)
2. **Environment variables** (`LIBRARIAN_*`)
3. **Command-line arguments** (`--*`)

**Example**:
```bash
# Code default: SAFE_DIR = $HOME
# Environment: LIBRARIAN_SAFE_DIR=/home/peter/development/librarian-mcp
# Command-line: --safe-dir /home/peter/development/librarian-mcp
# Final value: /home/peter/development/librarian-mcp (command-line wins)
```

---

## Backend Selection Guide

### Chonkie Backend (Default)

**Use When**:
- Search result quality is important
- Documents have complex structure
- You want semantic understanding
- Production use

**Advantages**:
- ✅ Intelligent semantic boundaries
- ✅ Better search relevance
- ✅ Context preservation
- ✅ Adapts to document structure

**Disadvantages**:
- ⚠️ Slightly slower processing
- ⚠️ More complex chunking logic

**Configuration**:
```bash
export LIBRARIAN_BACKEND=chonkie  # This is the default
```

---

### ChromaDB Backend

**Use When**:
- Processing speed is critical
- Documents are very simple
- Testing and development
- Fallback option

**Advantages**:
- ✅ Fast processing
- ✅ Simple predictable chunks
- ✅ Well-tested implementation

**Disadvantages**:
- ⚠️ Poorer search relevance
- ⚠️ May break semantic boundaries
- ⚠️ Less context preservation

**Configuration**:
```bash
export LIBRARIAN_BACKEND=chroma
```

---

### Switching Backends

**Temporary Switch** (current session only):
```bash
export LIBRARIAN_BACKEND=chroma
./setup_mcp.sh
```

**Permanent Switch** (all sessions):
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export LIBRARIAN_BACKEND=chroma' >> ~/.bashrc
source ~/.bashrc
```

**Verify Current Backend**:
```python
from mcp_server.config.settings import settings
print(f"Current backend: {settings.BACKEND}")
```

---

## The .librarianignore File

### Location
```
/home/peter/development/librarian-mcp/.librarianignore
```

### Purpose
Specifies which files and directories should be excluded from indexing and access.

### Pattern Syntax
Uses gitignore-style patterns:

```
# Comments start with #
# Negation patterns start with !

# Exclude all .env files
.env
*.env

# Except .env.example
!.env.example

# Exclude directories
venv/
node_modules/
__pycache__/

# Exclude files by type
*.log
*.tmp
*.key
*.pem
```

### Built-in Patterns

The system includes **94+ built-in exclusion patterns** automatically:

**Security** (always excluded):
- `.env`, `*.env`, credentials
- `*.key`, `*.pem`
- `id_rsa`, `id_ed25519`

**Development**:
- `venv/`, `.venv/`, `virtualenv/`
- `node_modules/`
- `__pycache__/`, `*.pyc`

**Databases**:
- `chroma_db/`
- `metadata/`
- `*.db`, `*.sqlite`

**Build Artifacts**:
- `dist/`, `build/`
- `*.egg-info/`

**Logs & Temp**:
- `*.log`, `logs/`
- `*.tmp`, `tmp/`

### Custom Patterns

Add your own patterns to `.librarianignore`:

```bash
# Add custom exclusions
echo "*.pdf" >> .librarianignore
echo "drafts/" >> .librarianignore
echo "*.secret" >> .librarianignore
```

### Testing Patterns

Check if a file would be ignored:

```python
from mcp_server.core.ignore_patterns import IgnorePatterns

patterns = IgnorePatterns("/home/peter/development/librarian-mcp")
print(patterns.is_ignored(Path("/home/peter/development/librarian-mcp/venv/file.py")))
# Output: True
```

---

## Deployment Configuration

### venv Deployment (Recommended)

**Advantages**:
- ✅ Simpler setup
- ✅ Close Chonkie-ChromaDB coupling
- ✅ Better performance (stdio transport)
- ✅ Easier debugging
- ✅ Lower resource usage

**Setup**:
```bash
cd /home/peter/development/librarian-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Why Not Docker**:
- Docker adds complexity for single-user deployments
- Container boundaries prevent efficient data sharing
- Additional resource overhead
- Harder to debug
- stdio transport is faster than HTTP

---

## Common Configuration Scenarios

### Scenario 1: Development Setup

```bash
# Use Chonkie backend (default)
export LIBRARIAN_BACKEND=chonkie

# Safe directory is current project (overrides default: $HOME)
export LIBRARIAN_SAFE_DIR=/home/peter/development/librarian-mcp

# Smaller chunks for testing
export LIBRARIAN_CHUNK_SIZE=500

# Start server
./setup_mcp.sh
```

---

### Scenario 2: Production with Large Document Collection

```bash
# Use Chonkie for best search quality
export LIBRARIAN_BACKEND=chonkie

# Large document storage
export LIBRARIAN_DOCUMENTS_DIR=/data/documents

# External database storage
export LIBRARIAN_CHROMA_PATH=/data/chroma_db
export LIBRARIAN_METADATA_PATH=/data/metadata

# Larger document support
export LIBRARIAN_MAX_DOCUMENT_SIZE=50000000  # 50 MB

# Start server
./setup_mcp.sh
```

---

### Scenario 3: Fast Testing with Simple Backend

```bash
# Use ChromaDB backend for speed
export LIBRARIAN_BACKEND=chroma

# Small test dataset
export LIBRARIAN_DOCUMENTS_DIR=./test-docs

# Smaller chunks
export LIBRARIAN_CHUNK_SIZE=250

# Start server
./setup_mcp.sh
```

---

### Scenario 4: Secure Multi-Project Setup

```bash
# Restrict to specific project
export LIBRARIAN_SAFE_DIR=/home/peter/projects/current

# Separate database per project
export LIBRARIAN_CHROMA_PATH=/home/peter/projects/current/.librarian/chroma
export LIBRARIAN_METADATA_PATH=/home/peter/projects/current/.librarian/metadata

# Strict security
export LIBRARIAN_MAX_OUTPUT_CHARS=4000  # Smaller output
export LIBRARIAN_COMMAND_TIMEOUT=10    # Shorter timeout

# Start server
./setup_mcp.sh
```

---

## Troubleshooting

### Issue: Backend Not Changing

**Problem**: Changed `LIBRARIAN_BACKEND` but still using old backend

**Solution**:
```bash
# Stop the server
# Clear environment
unset LIBRARIAN_BACKEND

# Set new value
export LIBRARIAN_BACKEND=chonkie

# Restart server
./setup_mcp.sh
```

---

### Issue: Documents Not Being Indexed

**Problem**: Files in directory but not appearing in library

**Check**:
```bash
# Is file in .librarianignore?
grep -r "filename" .librarianignore

# Is file extension supported?
echo ".md" | grep -E "\.(md|txt|py|js|ts|json|yaml|yml|toml|rst|html)$"

# Is file too large?
ls -lh yourfile.txt  # Check against LIBRARIAN_MAX_DOCUMENT_SIZE
```

---

### Issue: "Command Not Found" Error

**Problem**: Server can't find Python interpreter

**Solution**:
```bash
# Use absolute path to venv python
/home/peter/development/librarian-mcp/venv/bin/python \
  mcp_server/librarian_mcp.py
```

---

## Library Management

### Clearing and Rebuilding the Document Index

When you need to completely rebuild the library (e.g., after major documentation changes), use the rebuild script:

**Basic Rebuild** (uses default backend - Chonkie):
```bash
cd /home/peter/development/librarian-mcp
source venv/bin/activate
python scripts/rebuild_library.py
```

**Rebuild with Specific Backend**:
```bash
# Use Chonkie backend (intelligent chunking)
export LIBRARIAN_BACKEND=chonkie
./venv/bin/python scripts/rebuild_library.py

# Use ChromaDB backend (simple chunking)
export LIBRARIAN_BACKEND=chroma
./venv/bin/python scripts/rebuild_library.py
```

**What the Rebuild Script Does**:
1. **Clears existing data** - Removes all chunks from ChromaDB
2. **Backs up metadata** - Saves current index as `index.json.bak`
3. **Scans project directory** - Finds all supported document types
4. **Applies .librarianignore** - Filters out excluded files
5. **Re-ingests documents** - Chunks and indexes all valid documents
6. **Reports results** - Shows added/updated/unchanged/removed/ignored counts

**Example Output**:
```
======================================================================
Rebuilding Librarian Library
======================================================================
Using backend: chonkie
Chunking method: recursive

Clearing existing library...
Cleared 353 chunks from collection 'documents'
Backed up existing index to index.json.bak
Cleared 40 documents from metadata store

Starting sync...

Sync Completed!
  Added: 39 documents
  Updated: 0 documents
  Unchanged: 0 documents
  Removed: 0 documents
  Ignored: 24746 files (excluded by .librarianignore)

📚 Library ready!
```

**When to Rebuild**:
- ✅ After major documentation updates
- ✅ After changing backend (ChromaDB ↔ Chonkie)
- ✅ After modifying .librarianignore patterns
- ✅ When search results seem stale
- ⚠️ **Note**: Rebuild clears the search index (ChromaDB + metadata), then rebuilds it from source documents. Source files are never deleted.

**Alternative: Partial Updates** (without clearing):
- Use `sync_documents()` tool to add/update specific directories
- Use `add_document()` to add individual files
- Preserves existing library contents

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
- [README.md](README.md) - Quick start guide
- [SECURITY.md](SECURITY.md) - Security model
- [Tools.md](Tools.md) - Tool reference
