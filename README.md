# Librarian MCP Server

Unified MCP server for library access and CLI operations. Enables AI models to act as intelligent librarians with semantic search capabilities over document collections.

## Features

- **Library Tools**: Search, sync, and manage documents in ChromaDB
- **CLI Tools**: Secure command execution and file access
- **Semantic Search**: Powered by ChromaDB vector database
- **Document Lifecycle**: Complete document management (add, update, remove)
- **Change Detection**: Automatic tracking of document modifications
- **Security**: Command whitelisting and directory sandboxing

## Quick Start

### Installation

```bash
cd /home/peter/development/librarian-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the MCP Server

```bash
# Using the startup script
./setup_mcp.sh

# Or directly
source venv/bin/activate
python mcp_server/librarian_mcp.py --safe-dir /home/peter/development
```

### Bulk Document Ingestion

```bash
# Ingest all documents from a directory
python scripts/ingest.py --path /path/to/documents --extensions .md,.txt,.py

# Ingest specific extensions
python scripts/ingest.py --path ~/documents --extensions .md --recursive
```

## MCP Client Configuration

### Jan

```json
{
  "mcpServers": {
    "librarian": {
      "command": "/home/peter/development/librarian-mcp/venv/bin/python",
      "args": [
        "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py",
        "--safe-dir", "/home/peter/development"
      ]
    }
  }
}
```

### LM Studio

```json
{
  "mcpServers": {
    "librarian": {
      "command": "/home/peter/development/librarian-mcp/venv/bin/python",
      "args": [
        "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py",
        "--safe-dir", "/home/peter/development"
      ]
    }
  }
}
```

## Available Tools

### Library Tools

- `search_library(query, limit)` - Semantic search over documents
- `sync_documents(path, extensions, recursive)` - Sync directory to library
- `add_document(path)` - Add single document to library
- `remove_document(document_id)` - Remove document from library
- `list_indexed_documents()` - List all indexed documents
- `get_document_status(path)` - Check document status
- `get_library_stats()` - Get library statistics

### CLI Tools

- `execute_command(command, args, cwd)` - Execute whitelisted commands
- `read_document(path)` - Read file contents
- `list_documents(path, extension, recursive)` - List files
- `search_documents(query, path, extension)` - Search file contents
- `document_summary(path)` - Get file structure summary
- `server_info()` - Show server configuration

## Configuration

### Command Line Arguments

```bash
python mcp_server/librarian_mcp.py \
  --safe-dir /home/peter/development \
  --documents-dir ./documents \
  --chroma-path ./chroma_db \
  --metadata-path ./metadata
```

### Environment Variables

```bash
export LIBRARIAN_SAFE_DIR=/home/peter/development
export LIBRARIAN_DOCUMENTS_DIR=./documents
export LIBRARIAN_CHROMA_PATH=./chroma_db
export LIBRARIAN_METADATA_PATH=./metadata
```

## Architecture

```
MCP Server
├── Library Tools (search, sync, add, remove)
├── CLI Tools (execute, read, list, search)
├── Document Manager (discovery, change detection, lifecycle)
├── Backend Layer (ChromaDB → Chonkie in Phase 2)
└── AI Layer (result aggregation)
```

## Usage Examples

### Example 1: Initial Library Setup

```bash
# 1. Place documents in the documents directory
cp -r ~/my-docs/* ./documents/

# 2. Ingest documents
python scripts/ingest.py --path ./documents

# 3. Start MCP server
./setup_mcp.sh

# 4. Use from AI model:
#    "Search the library for information about X"
#    "Sync the documents directory"
#    "List all indexed documents"
```

### Example 2: Adding New Documents

```bash
# Option 1: Via MCP tool
# (from AI chat interface)
# "Add the document /path/to/newfile.md to the library"

# Option 2: Via script
python scripts/ingest.py --path /path/to/newfile.md

# Option 3: Bulk sync
# (from AI chat interface)
# "Sync the directory /home/peter/documents"
```

### Example 3: Querying the Library

```
# From AI chat interface:
# "Search for information about semantic search"
# "What does the library say about ChromaDB?"
# "Find documents mentioning 'vector database'"
```

## Document Types Supported

- Markdown (`.md`)
- Text (`.txt`)
- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`)
- JSON (`.json`)
- YAML (`.yaml`, `.yml`)
- TOML (`.toml`)
- reStructuredText (`.rst`)
- HTML (`.html`)

## Security

### CLI Tools Security

- **Command Whitelisting**: Only approved binaries can be executed
- **Directory Sandboxing**: All operations restricted to allowed directory
- **Timeout Protection**: Commands terminate after timeout (default: 15s)
- **Output Truncation**: Protects LLM context window (max: 8000 chars)
- **Dangerous Flag Blocking**: Prevents misuse of safe commands

### Document Processing Security

- **File Size Limits**: Maximum document size (default: 10MB)
- **Extension Whitelisting**: Only supported document types
- **Path Validation**: Prevents path traversal attacks

## File Structure

```
librarian-mcp/
├── mcp_server/                # Main MCP server
│   ├── librarian_mcp.py       # Server entry point
│   ├── tools/                 # MCP tool implementations
│   ├── core/                  # Core business logic
│   │   ├── document_manager.py
│   │   └── metadata_store.py
│   ├── backend/               # Storage backends
│   │   ├── base.py
│   │   └── chroma_backend.py
│   ├── ai_layer/              # AI response synthesis
│   └── config/                # Configuration
├── scripts/                   # Standalone utilities
│   └── ingest.py              # Bulk ingestion
├── documents/                 # Document storage
├── chroma_db/                 # ChromaDB data
├── metadata/                  # Document tracking
├── requirements.txt
└── setup_mcp.sh               # Startup script
```

## Phase 2: Chonkie Integration

Future enhancement to replace ChromaDB's native chunking with Chonkie's advanced chunking pipeline.

- Backend abstraction enables easy swap
- Set `LIBRARIAN_BACKEND=chonkie` environment variable
- No tool code changes needed

## Troubleshooting

### Issue: ChromaDB connection error

```bash
# Ensure chroma_db directory exists and is writable
mkdir -p chroma_db
chmod 755 chroma_db
```

### Issue: Document not found during sync

```bash
# Check file extensions are in allowed set
sync_documents(path="/path/to/docs", extensions=".md,.txt,.py")
```

### Issue: Out of memory during bulk ingestion

```bash
# Process in smaller batches
python scripts/ingest.py --path /path/to/docs
```

## Version

1.0.0 (Phase 1 - ChromaDB Backend)

## License

Self-hosted solution for document processing and semantic search.
