# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Librarian MCP Server** - A unified MCP server that provides AI models with:
- Semantic document search via ChromaDB
- Secure CLI and file access
- Complete document lifecycle management
- Change detection and sync capabilities

## Architecture

### Core Components

```
mcp_server/
├── librarian_mcp.py       # Main MCP server entry point
├── tools/                 # MCP tool implementations
│   ├── library_tools.py   # Library/document management tools
│   └── cli_tools.py       # CLI tools (from CLI-MCP)
├── core/                  # Core business logic
│   ├── document_manager.py    # Document lifecycle management
│   └── metadata_store.py      # Track processed documents
├── backend/               # Storage backends
│   ├── base.py                # Abstract interface
│   └── chroma_backend.py      # ChromaDB implementation
├── ai_layer/              # AI response synthesis
│   └── ai_layer_interface.py
└── config/                # Configuration
    └── settings.py            # Centralized settings
```

### Key Design Patterns

1. **Lazy Initialization**: Backend, metadata, and document manager are created on first use
2. **Backend Abstraction**: `DocumentBackend` interface allows swapping ChromaDB ↔ Chonkie
3. **Metadata Tracking**: JSON-based store tracks document checksums for change detection
4. **Security Inheritance**: CLI tools preserve security model from CLI-MCP-Duplicate

## Development Commands

### Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Start MCP server (with defaults)
./setup_mcp.sh

# Start with custom paths
python mcp_server/librarian_mcp.py \
  --safe-dir /home/peter/development \
  --documents-dir ./documents \
  --chroma-path ./chroma_db \
  --metadata-path ./metadata
```

### Document Ingestion

```bash
# Bulk ingest from directory
python scripts/ingest.py --path /path/to/docs --extensions .md,.txt,.py

# Ingest single file
python scripts/ingest.py --path /path/to/file.md

# Non-recursive scan
python scripts/ingest.py --path /path/to/docs --no-recursive
```

### Testing

```bash
# Test with Python (basic import test)
python -c "from mcp_server.core.document_manager import DocumentManager; print('OK')"

# Test ChromaDB connection
python -c "from mcp_server.backend.chroma_backend import ChromaBackend; b=ChromaBackend(); print(b.get_stats())"
```

## Code Conventions

### Configuration

All configuration is centralized in `mcp_server/config/settings.py`:
- Use `settings.Settings` class for access
- Environment variables override defaults
- Directory paths are created automatically

### Backend Interface

When adding new backends (e.g., Chonkie):
1. Inherit from `DocumentBackend` in `backend/base.py`
2. Implement all abstract methods
3. Select via `LIBRARIAN_BACKEND` environment variable

### Tool Registration

MCP tools are registered via functions:
- `register_library_tools(mcp)` - Library-related tools
- `register_cli_tools(mcp, safe_dir)` - CLI-related tools

### Error Handling

- All tools return human-readable error messages
- Document operations return status dictionaries: `{'status': 'added|unchanged|error', ...}`
- CLI tools prefix errors with `[error]`, security issues with `[security error]`

## Key Files

### `mcp_server/core/document_manager.py`

**Purpose**: Heart of the system - manages complete document lifecycle

**Key Methods**:
- `discover_documents(path, extensions, recursive)` - Find documents
- `add_document(file_path)` - Add single document
- `sync_directory(path, extensions, recursive)` - Full sync (add/update/remove)
- `get_document_status(path)` - Check if document is current/outdated/not indexed

**Important**: Uses checksums for change detection - modified files are re-chunked automatically

### `mcp_server/core/metadata_store.py`

**Purpose**: Tracks which documents have been processed

**Storage**: `metadata/index.json` (JSON file)

**Key Methods**:
- `add(metadata)` - Add document metadata
- `get_by_path(path)` - Find document by file path
- `get_all()` - List all indexed documents

### `mcp_server/backend/chroma_backend.py`

**Purpose**: ChromaDB implementation of storage backend

**Key Methods**:
- `chunk_documents(documents, document_ids, source)` - Chunk and embed documents
- `query(query_text, limit)` - Semantic search
- `delete_documents(document_id)` - Remove all chunks for a document

**Chunking**: Simple sentence-based chunking (will be replaced by Chonkie in Phase 2)

### `mcp_server/tools/library_tools.py`

**Purpose**: MCP tools for library operations

**Tools**:
- `search_library(query, limit)` - Semantic search with AI aggregation
- `sync_documents(path, extensions, recursive)` - Sync directory
- `add_document(path)` - Add single document
- `remove_document(document_id)` - Remove document
- `list_indexed_documents()` - List all documents
- `get_document_status(path)` - Check document status
- `get_library_stats()` - Get statistics

### `mcp_server/tools/cli_tools.py`

**Purpose**: MCP tools for CLI operations (from CLI-MCP-Duplicate)

**Security Features**:
- Command whitelisting (`ALLOWED_BINARY_NAMES`)
- Directory sandboxing (all operations in `SAFE_WORKING_DIR`)
- Timeout protection (15s default)
- Output truncation (8000 chars)
- Dangerous flag blocking

**Tools**:
- `execute_command(command, args, cwd)` - Execute whitelisted commands
- `read_document(path)` - Read file contents
- `list_documents(path, extension, recursive)` - List files
- `search_documents(query, path, extension)` - Search file contents
- `document_summary(path)` - Get file structure

## Common Tasks

### Adding a New MCP Tool

1. Define tool function in appropriate `tools/*.py` file
2. Register in `register_*_tools()` function
3. Update README.md with tool documentation
4. Test via MCP client

### Adding a New Document Extension

1. Add to `DEFAULT_EXTENSIONS` in `config/settings.py`
2. Add to `DOCUMENT_EXTENSIONS` in `tools/cli_tools.py` (if needed for CLI tools)
3. Update README.md

### Debugging Document Issues

```python
# Check document status
from mcp_server.core.document_manager import DocumentManager
from mcp_server.backend.chroma_backend import ChromaBackend
from mcp_server.core.metadata_store import MetadataStore

dm = DocumentManager(ChromaBackend(), MetadataStore())
status = dm.get_document_status("/path/to/file.md")
print(status)

# List all indexed documents
docs = dm.list_indexed()
for doc in docs:
    print(f"{doc['name']}: {doc['document_id']}")
```

### Viewing ChromaDB Contents

```python
from mcp_server.backend.chroma_backend import ChromaBackend

backend = ChromaBackend()
stats = backend.get_stats()
print(stats)

# Query test
results = backend.query("test query", limit=5)
for result in results:
    print(f"{result['text'][:100]}... (score: {result['similarity_score']:.2f})")
```

## Testing Strategy

### Unit Tests (Not Yet Implemented)

When adding tests:
1. Test `DocumentManager` with mock backend
2. Test `MetadataStore` file operations
3. Test tool functions independently
4. Test security validation functions

### Integration Testing

Use MCP clients:
- **Jan**: Primary testing (excellent MCP support)
- **LM Studio**: Single MCP server testing
- **Claude Desktop**: Multi-MCP testing

### Manual Testing Checklist

- [ ] Ingest documents from test directory
- [ ] Search for known content
- [ ] Add new document
- [ ] Modify existing document (detect change)
- [ ] Delete document
- [ ] List indexed documents
- [ ] Get document status
- [ ] CLI tools work correctly
- [ ] Security restrictions enforced

## Phase 2 Preparation

### Chonkie Integration

When implementing Chonkie backend:

1. Create `mcp_server/backend/chonkie_backend.py`
2. Inherit from `DocumentBackend`
3. Implement all abstract methods
4. Select via environment: `export LIBRARIAN_BACKEND=chonkie`
5. No changes needed to:
   - Document Manager
   - MCP Tools
   - Metadata Store

### Files That Won't Change in Phase 2

- `mcp_server/core/document_manager.py` - Works with any backend
- `mcp_server/core/metadata_store.py` - Backend-agnostic
- `mcp_server/tools/library_tools.py` - Backend-agnostic
- `mcp_server/tools/cli_tools.py` - Independent

### Files That Will Change

- `mcp_server/backend/chonkie_backend.py` - NEW
- `requirements.txt` - Add Chonkie SDK
- `README.md` - Update documentation

## Important Notes

### Do Not Modify

- `/home/peter/development/librarian/` - Original project (reference only)
- Any existing ChromaDB data we're starting fresh

### Security Considerations

- Never bypass command whitelist
- Never allow operations outside safe directory
- Always validate file paths
- Always truncate long outputs

### Performance Considerations

- Large documents are chunked automatically (default: 1000 chars)
- ChromaDB handles embedding automatically
- For very large libraries, consider batch ingestion via `scripts/ingest.py`

## Troubleshooting

### Import Errors

```bash
# Ensure you're in the project directory
cd /home/peter/development/librarian-mcp

# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### ChromaDB Issues

```bash
# Clear and restart
rm -rf chroma_db metadata
mkdir chroma_db metadata
```

### MCP Connection Issues

```bash
# Check server is running
./setup_mcp.sh

# Check paths are absolute
# In MCP client config, use full paths:
# /home/peter/development/librarian-mcp/venv/bin/python
```

## Future Enhancements

- [ ] Unit tests for all components
- [ ] Performance benchmarking
- [ ] Chonkie backend implementation
- [ ] Document versioning
- [ ] Incremental sync optimization
- [ ] REST API for administration (optional)
