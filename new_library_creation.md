# Multi-Library System Guide

**Created**: 2026-03-22
**Status**: Active

---

## Overview

The Librarian MCP Server supports **multiple independent libraries**, each with its own:
- Document collection
- Search index (ChromaDB)
- Metadata store
- Configuration
- Ignored file patterns
- Sandbox workspace

**Use Cases:**
- Separate projects (botany research, programming documentation, legal documents)
- Different content types (PDFs in one, code in another)
- Testing and experimentation
- Obsidian vault integration

---

## Important Terminology

**Understanding the Library Structure:**

| Term | Meaning | Example |
|------|---------|---------|
| **Library Root** | Your document directory | `/home/peter/botany` |
| **SAFE_DIR** | Library root (CLI tool boundary) | Same as library root |
| **CLI Sandbox** | Entire library root | All CLI tools work here |
| **Write Sandbox** | `/sandbox/` subdirectory | Only place for writes |

**Key Concepts:**

1. **Library Root (SAFE_DIR)**: Where your documents live
   - All CLI tools (`grep`, `find`, `read_document`) can operate anywhere in this directory
   - Set via `LIBRARIAN_SAFE_DIR` environment variable
   - Example: `/home/peter/botany`

2. **Write Sandbox (/librarian/)**: Where the librarian can write files
   - Automatically created at: `{library_root}/\.librarian/sandbox/`
   - ONLY place where `write_document` tool works
   - Protected by multiple security layers
   - Example: `/home/peter/botany/\.librarian/sandbox/`

**Why Two Different "Sandboxes"?**

- **CLI Sandbox** (entire library): You can search, read, and list files anywhere in your library
- **Write Sandbox** (`/librarian/` only): Librarian can only write to this specific subdirectory

**Example:**
```
SAFE_DIR = /home/peter/botany

✅ CLI tools CAN access:
   /home/peter/botany/Agronomy.pdf           (read)
   /home/peter/botany/Forestry.pdf            (read)
   /home/peter/botany/.librarian/             (read)

✅ Librarian CAN write to:
   /home/peter/botany/\.librarian/sandbox/reports/analysis.md   (write)

❌ Librarian CANNOT write to:
   /home/peter/botany/new_file.pdf                                     (blocked)
```

---

## Library Structure

Every library has a `.librarian/` directory containing all library-specific data:

```
/home/peter/botany/
├── .librarian/                    # Library configuration & data (created automatically)
│   ├── config.json                # Library settings
│   ├── .librarianignore           # What to exclude from indexing
│   ├── chroma_db/                 # ChromaDB data (isolated from other libraries)
│   ├── metadata/                  # Metadata store (isolated from other libraries)
│   ├── sandbox/                    # Sandbox for librarian writes
│   │   ├── README.md              # Sandbox documentation
│   │   └── reports/               # Analysis reports written by librarian
│   └── rebuild.sh                 # Quick rebuild script for this library
├── Agronomy.pdf                   # Your documents
├── Forestry.pdf
└── Pomology.pdf
```

**Key Points:**
- Each library is **completely isolated** from others
- No shared data between libraries
- You can delete a library by removing its `.librarian/` directory
- Your documents are never touched (only indexed)

---

## Creating a New Library

### Method 1: Using the create_library.sh Script (Recommended)

**From the librarian-mcp project directory:**

```bash
cd /home/peter/development/librarian-mcp

# Basic usage
./scripts/create_library.sh /home/peter/my-library

# With options
./scripts/create_library.sh /home/peter/botany \
  --name botany \
  --extensions .md,.pdf \
  --backend chonkie
```

**What It Does:**
1. Creates `.librarian/` directory structure
2. Generates `config.json` with your settings
3. Creates `.librarianignore` with default exclusions
4. Sets up ChromaDB and metadata directories
5. Creates librarian sandbox workspace
6. Creates library-specific rebuild script

**Interactive Prompts:**
- Shows you the configuration
- Asks for confirmation before creating
- Displays next steps when complete

### Method 2: Manual Creation

**1. Create Directory Structure:**

```bash
mkdir -p /home/peter/my-library/.librarian/{chroma_db,metadata,librarian/reports}
```

**2. Create config.json:**

```json
{
  "library_name": "my-library",
  "library_root": "/home/peter/my-library",
  "librarian_dir": "/home/peter/my-library/.librarian",
  "allowed_extensions": [".md", ".txt", ".pdf"],
  "chroma_path": "/home/peter/my-library/.librarian/chroma_db",
  "metadata_path": "/home/peter/my-library/.librarian/metadata",
  "sandbox_path": "/home/peter/my-library/.librarian/librarian",
  "backend": "chonkie",
  "chunk_size": 1000,
  "created": "2026-03-22T10:00:00+00:00"
}
```

**3. Create .librarianignore:**

See "Default Ignore Patterns" section below.

---

## Library Configuration

### config.json Settings

| Setting | Type | Description | Example |
|---------|------|-------------|---------|
| `library_name` | string | Human-readable library name | `"botany"` |
| `library_root` | string | Absolute path to library | `"/home/peter/botany"` |
| `allowed_extensions` | array | File types to index | `[".md", ".pdf"]` |
| `chroma_path` | string | ChromaDB storage location | `"/path/to/chroma_db"` |
| `metadata_path` | string | Metadata storage location | `"/path/to/metadata"` |
| `sandbox_path` | string | Librarian write sandbox | `"/path/to/librarian"` |
| `backend` | string | Chunking backend | `"chonkie"` or `"chroma"` |
| `chunk_size` | integer | Target chunk size (characters) | `1000` |

### Extension Support

**Currently Supported:**
- `.md` - Markdown
- `.txt` - Plain text
- `.py` - Python code
- `.js` - JavaScript
- `.ts` - TypeScript
- `.json` - JSON
- `.yaml`, `.yml` - YAML
- `.toml` - TOML
- `.rst` - reStructuredText
- `.html` - HTML

**Coming Soon:**
- `.pdf` - PDF documents (in development)
- `.docx` - Word documents (planned)
- Images with OCR (planned)

---

## Default Ignore Patterns

Every library gets a `.librarianignore` file with these default exclusions:

**Security (never index these):**
```
.env
*.env
credentials.*
*.key
*.pem
id_rsa
id_ed25519
```

**Development:**
```
venv/
.venv/
virtualenv/
__pycache__/
*.pyc
```

**Version Control:**
```
.git/
.svn/
.hg/
```

**Databases (don't index the database!):**
```
chroma_db/
metadata/
```

**Obsidian (if using as vault):**
```
.obsidian/
.obsidian.plugins/
```

**Add custom exclusions** to your library's `.librarianignore` file.

---

## Managing Libraries

### List All Libraries

```bash
cd /home/peter/development/librarian-mcp
./scripts/list_libraries.sh
```

**Output Example:**
```
======================================
Librarian Libraries
======================================

Library: botany
  Path:        /home/peter/botany
  Documents:   3
  Extensions:  .md, .pdf
  Backend:     chonkie

Library: librarian-mcp
  Path:        /home/peter/development/librarian-mcp
  Documents:   39
  Extensions:  .md, .txt, .py, .js, .ts, .json, .yaml, .yml, .toml, .rst, .html
  Backend:     chonkie
```

### Switch Between Libraries

**IMPORTANT:** After switching libraries, you **must restart the MCP server** for changes to take effect.

**Step 1: Get Library Configuration**

```bash
cd /home/peter/development/librarian-mcp
./scripts/use_library.sh /home/peter/botany
```

**Step 2: Update MCP Client Configuration**

Your MCP client (Jan, Claude Desktop, etc.) needs these environment variables:

```bash
# For Jan or Claude Desktop MCP configuration

# LIBRARIAN_SAFE_DIR = Library root (CLI tool boundary)
# All CLI tools (grep, find, read_document) are restricted to this directory
LIBRARIAN_SAFE_DIR=/home/peter/botany

# Library-specific data locations
LIBRARIAN_CHROMA_PATH=/home/peter/botany/.librarian/chroma_db
LIBRARIAN_METADATA_PATH=/home/peter/botany/.librarian/metadata
LIBRARIAN_BACKEND=chonkie
```

**IMPORTANT: Understanding SAFE_DIR**
- `LIBRARIAN_SAFE_DIR` = **Library root** (where your documents live)
- This is the **CLI tool boundary** - grep, find, read_document can operate anywhere in this directory
- The `/librarian/` write sandbox is automatically: `{SAFE_DIR}/\.librarian/sandbox/`
- Example: If `SAFE_DIR=/home/peter/botany`, then librarian writes to `/home/peter/botany/\.librarian/sandbox/`

**Jan Configuration:**
1. Settings → MCP Servers
2. Find Librarian MCP
3. Update environment variables
4. Toggle server OFF, wait 2 seconds
5. Toggle server ON
6. Start new chat

**Step 3: Verify Library Loaded**

Ask the librarian: "How many documents are indexed?"

Should show the document count for your active library.

---

## Indexing Documents

### Initial Index (All Documents)

**Option 1: Use Library-Specific Script**

```bash
# From the library directory
/home/peter/botany/.librarian/rebuild.sh
```

**Option 2: Use Main Script with Environment Variables**

```bash
cd /home/peter/development/librarian-mcp

# Set library-specific paths
export LIBRARIAN_CHROMA_PATH=/home/peter/botany/.librarian/chroma_db
export LIBRARIAN_METADATA_PATH=/home/peter/botany/.librarian/metadata
export LIBRARIAN_BACKEND=chonkie

# Run rebuild
./scripts/clear_and_rebuild.sh
```

**What Happens:**
1. Clears existing index (if any)
2. Scans library directory for documents
3. Respects `.librarianignore` exclusions
4. Chunks documents using Chonkie
5. Creates embeddings and stores in ChromaDB
6. Tracks metadata for change detection

**Output Example:**
```
======================================================================
Rebuilding Librarian Library
======================================================================
Using backend: chonkie
Chunking method: recursive

Clearing existing library...
Cleared 0 chunks from collection 'documents'
Backed up existing index to index.json.bak
Cleared 0 documents from metadata store

Starting sync...

Sync Completed!
  Added: 3 documents
  Updated: 0 documents
  Unchanged: 0 documents
  Removed: 0 documents
  Ignored: 0 files (excluded by .librarianignore)

📚 Library ready!
```

### Add/Update Specific Documents

**Via MCP Tool:**
```
User: Add the document /home/peter/botany/new_plant.pdf
Librarian: [Uses add_document tool]
```

**Via Script (not yet implemented):**
```bash
# Future: Add single document
./scripts/add_document.sh /home/peter/botany/new_plant.pdf
```

### Update After Document Changes

The librarian tracks file checksums. Modified files are automatically re-chunked during sync.

```bash
# Rebuild to pick up changes
/home/peter/botany/.librarian/rebuild.sh
```

---

## Using the Librarian Sandbox

Every library has a **write sandbox** at `{library_root}/\.librarian/sandbox/` where the librarian can write files.

**IMPORTANT: Two Types of File Access**

1. **Read/CLI Operations** (anywhere in library):
   - `read_document()` - Can read files anywhere in `SAFE_DIR`
   - `list_documents()` - Can list directories anywhere in `SAFE_DIR`
   - `search_documents()` - Can search anywhere in `SAFE_DIR`
   - `execute_command()` - Can run commands anywhere in `SAFE_DIR`

2. **Write Operations** (only in `/librarian/` sandbox):
   - `write_document()` - Can ONLY write to `{SAFE_DIR}/\.librarian/sandbox/`

**What the librarian writes to the sandbox:**
- Analysis reports
- Search result summaries
- Code change suggestions
- Debugging diagnostics
- Validation results

**Example Workflow:**
```
Library: /home/peter/botany
Write Sandbox: /home/peter/botany/\.librarian/sandbox/

User: "Analyze the botanical PDFs and summarize plant propagation methods"

Librarian:
1. Searches library (read access to /home/peter/botany/*.pdf)
2. Analyzes content from PDFs
3. Writes summary to /home/peter/botany/\.librarian/sandbox/reports/propagation_methods.md

User: Reads report from sandbox
```

**Sandbox Safety:**
- Librarian **cannot write outside** `\.librarian/sandbox/`
- Maximum file size: 100KB per write
- Critical file protection (can't overwrite passwords, secrets, keys)
- All operations logged
- Cannot write files with sensitive names (password, secret, key, credential)

---

## Common Workflows

### Workflow 1: Create New Botany Library

```bash
# 1. Create library structure
cd /home/peter/development/librarian-mcp
./scripts/create_library.sh /home/peter/botany \
  --name botany \
  --extensions .md,.pdf \
  --backend chonkie

# 2. Add documents to /home/peter/botany/
#    (Your PDFs and markdown files)

# 3. Index the documents
/home/peter/botany/.librarian/rebuild.sh

# 4. Update MCP configuration
./scripts/use_library.sh /home/peter/botany
# [Update MCP client with environment variables]

# 5. Restart MCP server
# [In Jan: Settings → MCP Servers → Toggle Librarian OFF/ON]

# 6. Verify
# [New chat] Ask: "How many documents are indexed?"
```

### Workflow 2: Switch Between Libraries

```bash
# 1. List available libraries
./scripts/list_libraries.sh

# 2. Get configuration for target library
./scripts/use_library.sh /home/peter/botany

# 3. Update MCP client with environment variables

# 4. Restart MCP server

# 5. Verify correct library is loaded
```

### Workflow 3: Add New Documents to Library

```bash
# 1. Copy documents to library directory
cp ~/Downloads/new_research.pdf /home/peter/botany/

# 2. Rebuild index
/home/peter/botany/.librarian/rebuild.sh

# 3. Restart MCP server (if needed)

# 4. Search new content
```

### Workflow 4: Clean Up a Library

**Remove documents from index (keeps source files):**
```bash
# Rebuild to refresh metadata
/home/peter/botany/.librarian/rebuild.sh
```

**Delete entire library (including index data):**
```bash
# WARNING: This deletes the library's search index
rm -rf /home/peter/botany/.librarian

# Your documents in /home/peter/botany/ are NOT deleted
```

---

## Troubleshooting

### Issue: Wrong library is loaded

**Symptoms:** Document count doesn't match expected library

**Cause:** MCP server not restarted after switching libraries

**Solution:**
1. Restart MCP server in Jan (Settings → MCP Servers)
2. Start new chat
3. Ask: "How many documents are indexed?"

### Issue: Documents not being indexed

**Symptoms:** Rebuild shows "Added: 0 documents"

**Check:**
```bash
# Are there supported files?
find /home/peter/botany -name "*.md" -o -name "*.pdf"

# Are they ignored?
grep "filename" /home/peter/botany/.librarian/.librarianignore

# Are they too large?
ls -lh /home/peter/botany/*.pdf  # Check against LIBRARIAN_MAX_DOCUMENT_SIZE
```

### Issue: PDFs not indexing

**Symptoms:** PDFs in directory but not indexed

**Cause:** PDF support not yet implemented (coming soon)

**Status:** PDF chunking is in development. Check updates.

### Issue: Search results seem stale

**Cause:** MCP server using cached data

**Solution:**
```bash
# 1. Rebuild index
/home/peter/botany/.librarian/rebuild.sh

# 2. Restart MCP server
# 3. Start new chat
```

### Issue: Can't find library configuration

**Symptoms:** `.librarian` directory doesn't exist

**Solution:**
```bash
# Create library structure
./scripts/create_library.sh /path/to/library
```

---

## Advanced Usage

### Multiple Libraries with Different Backends

```bash
# Botany with Chonkie (semantic chunking)
./scripts/create_library.sh /home/peter/botany \
  --backend chonkie \
  --extensions .md,.pdf

# Code documentation with Chroma (faster, simpler)
./scripts/create_library.sh /home/peter/code-docs \
  --backend chroma \
  --extensions .md,.py,.js
```

### Obsidian Vault Integration

```bash
# Create library in Obsidian vault
./scripts/create_library.sh ~/Obsidian/BotanyVault \
  --name botany-vault \
  --extensions .md

# .librarianignore automatically excludes .obsidian/
# Your vault structure is preserved
# Librarian can search across all your notes
```

### Test Library for Experimentation

```bash
# Create test library
./scripts/create_library.sh /tmp/test-library \
  --name test \
  --extensions .md,.txt

# Safe to experiment
# Delete when done: rm -rf /tmp/test-library/.librarian
```

---

## Best Practices

### DO:
✅ Create separate libraries for different topics/projects
✅ Use descriptive library names
✅ Keep `.librarian/` directory (contains your index)
✅ Backup `.librarian/` directory periodically
✅ Restart MCP server after switching libraries
✅ Test with small libraries first

### DON'T:
❌ Mix unrelated content in one library
❌ Manually edit `chroma_db/` or `metadata/` directories
❌ Delete `.librarian/` unless you mean to reset the library
❌ Forget to restart MCP server after switching
❌ Index binary files (PDFs not yet supported)

---

## Library Isolation

**Each library is completely independent:**

| Component | Isolated | Shared |
|-----------|----------|--------|
| Document files | ✅ Yes | ❌ No |
| ChromaDB data | ✅ Yes | ❌ No |
| Metadata store | ✅ Yes | ❌ No |
| Configuration | ✅ Yes | ❌ No |
| Ignore patterns | ✅ Yes | ❌ No |
| MCP server code | ❌ No | ✅ Yes |

**Benefits:**
- No cross-contamination between libraries
- Different settings per library
- Safe testing without affecting main library
- Easy deletion of unwanted libraries

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [Jan_setup.md](Jan_setup.md) - Jan configuration
- [static_analysis.md](static_analysis.md) - Static analysis approach
- [README.md](README.md) - Quick start guide

---

*Multi-library support enables powerful knowledge management while maintaining complete isolation between different domains.*
