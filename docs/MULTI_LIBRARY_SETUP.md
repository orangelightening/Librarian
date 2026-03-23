# Multi-Library Setup Guide

**Librarian MCP Server v0.3.0 - Multi-Library Architecture**

## Overview

Librarian MCP Server supports multiple independent libraries, each with its own document collection and semantic search index. Each library is isolated in its own directory with a `.librarian/` subdirectory for data storage.

## Quick Start

### Option 1: Single Library (Simplest)

Use one MCP server at a time by toggling servers on/off in Jan.

**Dev Library MCP Config:**
```json
{
  "active": true,
  "args": [
    "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"
  ],
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "env": {
    "LIBRARIAN_BACKEND": "chonkie",
    "LIBRARIAN_CHROMA_PATH": "/home/peter/development/librarian-mcp/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/home/peter/development/librarian-mcp/.librarian/metadata",
    "LIBRARIAN_SAFE_DIR": "/home/peter/development/librarian-mcp",
    "PYTHONPATH": "/home/peter/development/librarian-mcp"
  }
}
```

**Botany Library MCP Config:**
```json
{
  "active": true,
  "args": [
    "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"
  ],
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "env": {
    "LIBRARIAN_BACKEND": "chonkie",
    "LIBRARIAN_CHROMA_PATH": "/home/peter/botany/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/home/peter/botany/.librarian/metadata",
    "LIBRARIAN_SAFE_DIR": "/home/peter/botany",
    "PYTHONPATH": "/home/peter/development/librarian-mcp"
  }
}
```

**Usage:**
1. Add the JSON config for your library in Jan's MCP settings
2. Activate only one library MCP server at a time
3. Use same system prompt and assistant for all libraries

### Option 2: Multiple Libraries (Advanced)

Run multiple MCP servers simultaneously (not recommended - AI models may confuse tools).

**Note:** Current architecture uses same tool names for all libraries. Running multiple servers simultaneously may cause AI models to use the wrong library. We recommend toggling servers on/off as needed.

## Creating a New Library

### Step 1: Create Library Directory

```bash
mkdir -p /path/to/your/library
cd /path/to/your/library
```

### Step 2: Add Documents

```bash
# Add PDFs, markdown files, code, etc.
cp ~/Documents/*.pdf /path/to/your/library/
```

### Step 3: Create MCP Config

Use one of the templates above, changing paths:
- `LIBRARIAN_CHROMA_PATH`: `/path/to/your/library/.librarian/chroma_db`
- `LIBRARIAN_METADATA_PATH`: `/path/to/your/library/.librarian/metadata`
- `LIBRARIAN_SAFE_DIR`: `/path/to/your/library`

### Step 4: Start Server and Index

```bash
# The .librarian/ directory will be created automatically
# Use the MCP tools to index documents:
sync_documents(path="/path/to/your/library")
```

## Library Structure

Each library has this structure:

```
/path/to/library/
├── .librarian/
│   ├── chroma_db/           # Vector database
│   ├── metadata/            # Document metadata
│   └── config.json          # Library configuration
├── document1.pdf
├── document2.md
└── document3.py
```

## Supported File Types

Librarian MCP Server with Chonkie backend supports:

- **PDF**: `.pdf` (uses pypdf with docling fallback)
- **Documents**: `.docx`, `.md`, `.txt`, `.rst`, `.html`
- **Code**: `.py`, `.js`, `.ts`, `.json`
- **Config**: `.yaml`, `.yml`, `.toml`

## MCP Tools

### Library Management

- **`search_library(query, limit=10)`**
  - Semantic search across all indexed documents
  - Returns ranked results with similarity scores
  - Example: `search_library("fruit tree pruning techniques")`

- **`sync_documents(path, extensions=None, recursive=True)`**
  - Index all documents in a directory
  - Automatically adds new, updates changed, removes deleted
  - Example: `sync_documents("/home/peter/botany")`

- **`add_document(path)`**
  - Add a single document to the library
  - Example: `add_document("/home/peter/botany/new_doc.pdf")`

- **`remove_document(document_id)`**
  - Remove a document from the library
  - Example: `remove_document("a1b2c3d4")`

- **`list_indexed_documents()`**
  - List all indexed documents with metadata
  - Shows document name, chunk count, file size

- **`get_document_status(path)`**
  - Check if a document is indexed, current, or outdated
  - Returns status and metadata

- **`get_library_stats()`**
  - Get library statistics
  - Total documents, chunks, storage size

### File Writing (Security Sandbox)

- **`write_document(path, content, create_dirs=True)`**
  - Write content to the librarian workspace (sandboxed)
  - **Security**: Writes are restricted to `.librarian/` subdirectory only
  - **Path Format**: Use simple relative paths
    - ✅ Good: `'report.md'`, `'sandbox/analysis.md'`, `'reports/fix.py'`
    - ❌ Bad: `'/home/peter/botany/file.md'`, `'../escape.md'`, `'/.librarian/sandbox/file.md'`
  - **Examples**:
    ```python
    write_document('report.md', '# Analysis\\n\\nFindings...')
    write_document('sandbox/contradictions.md', 'Detailed analysis...')
    write_document('reports/fix.py', 'def fix():\\n    pass')
    ```
  - **Write Location**: Files are written to `<library>/.librarian/<path>`
    - Dev library: `/home/peter/development/librarian-mcp/.librarian/sandbox/contradictions.md`
    - Botany library: `/home/peter/botany/.librarian/reports/analysis.md`
  - **Security Features**:
    - Rejects absolute paths
    - Rejects parent directory references (`..`)
    - Rejects paths starting with `.`
    - Rejects system directory patterns (`home/`, `usr/`, etc.)
    - Limits directory depth (max 3 levels)
    - Clear error messages before content generation

### CLI Tools (within safe directory)

- **`execute_command(command, args, cwd)`**
  - Execute whitelisted commands safely
  - Commands: ls, cat, grep, find, head, tail, etc.

- **`read_document(path, start_line, end_line, head, tail)`**
  - Read file contents with various options
  - Supports line ranges, first N lines, last N lines

- **`list_documents(path, extension, recursive)`**
  - List documents in directory
  - Filter by extension, recursive search

- **`search_documents(query, path, extension)`**
  - Text search across files (not semantic)
  - Find literal text matches in documents

- **`document_summary(path)`**
  - Get document structure overview
  - Shows headings for markdown, functions for code

## Performance

### Chunking Quality

- **Token-based**: 512 tokens per chunk (not character-based)
- **Semantic coherence**: Chonkie SemanticChunker preserves context
- **File-type-aware**: Different processing for PDFs, code, markdown

### Retrieval Quality

- **Vector embeddings**: Semantic similarity using sentence transformers
- **Ranked results**: Most relevant chunks first
- **Metadata**: Source tracking for each chunk

### Benchmarks

- **PDF extraction**: ~1-2 seconds per page (pypdf)
- **Chunking**: ~10-20 chunks/second (semantic)
- **Search**: <100ms for typical queries
- **Storage**: ~1KB per chunk (vector + metadata)

## Troubleshooting

### Server Won't Start

- Check Python interpreter path is correct
- Verify `PYTHONPATH` points to librarian-mcp directory
- Ensure `.librarian/` directory is writable

### No Search Results

- Verify documents are indexed: `list_indexed_documents()`
- Check document status: `get_document_status(path)`
- Re-index if needed: `sync_documents(path)`

### PDF Extraction Fails

- Ensure `pypdf` is installed: `pip install pypdf`
- Falls back to `docling` automatically
- Check PDF isn't password-protected or corrupted

### Poor Search Quality

- Try different query terms
- Increase `limit` parameter: `search_library(query, limit=20)`
- Re-index with updated Chonkie backend

## Configuration

### Environment Variables

- **`LIBRARIAN_BACKEND`**: Backend type (`chonkie` or `chroma`)
- **`LIBRARIAN_CHROMA_PATH`**: ChromaDB database directory
- **`LIBRARIAN_METADATA_PATH`**: Metadata storage directory
- **`LIBRARIAN_SAFE_DIR`**: Safe directory for CLI operations
- **`PYTHONPATH`**: Path to librarian-mcp code

### Backend Selection

- **Chonkie** (recommended): PDF support, semantic chunking
- **Chroma**: Legacy backend, character-based chunking

## Best Practices

1. **One library per topic** - Better semantic separation
2. **Use descriptive names** - Library names clarify purpose
3. **Regular syncs** - Keep index updated with changes
4. **Monitor storage** - Vector databases grow with documents
5. **Backup .librarian/** - Contains all indexed data

## Examples

### Create a Research Library

```json
{
  "active": true,
  "args": ["/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"],
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "env": {
    "LIBRARIAN_BACKEND": "chonkie",
    "LIBRARIAN_CHROMA_PATH": "/home/peter/research/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/home/peter/research/.librarian/metadata",
    "LIBRARIAN_SAFE_DIR": "/home/peter/research",
    "PYTHONPATH": "/home/peter/development/librarian-mcp"
  }
}
```

### Index and Search

```python
# In Jan, use MCP tools:
sync_documents("/home/peter/research")

# Search for specific topics:
search_library("machine learning transformers")
search_library("neural network architecture")
```

## Support

For issues or questions:
- GitHub: https://github.com/yourusername/librarian-mcp
- Documentation: `/home/peter/development/librarian-mcp/README.md`
- Architecture: `/home/peter/development/librarian-mcp/CLAUDE.md`
