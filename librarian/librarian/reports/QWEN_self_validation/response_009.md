# Response 9: How to Clear and Rebuild the Document Library Index

## Summary

There is **no single command** to directly "clear and rebuild" the library, but there are multiple approaches available depending on your needs and the desired backend.

## Option 1: Using the Rebuild Script (Recommended)

The most straightforward method is to use the provided `rebuild_library.py` script, which handles the entire process automatically.

### Basic Usage

```bash
cd /home/peter/development/librarian-mcp
source venv/bin/activate
python scripts/rebuild_library.py
```

[Source: rebuild_library.py]

### With Specific Backend

The script supports different backends via environment variables:

**Using Chonkie backend (intelligent chunking, default):**
```bash
export LIBRARIAN_BACKEND=chonkie
./venv/bin/python scripts/rebuild_library.py
```

**Using ChromaDB backend (simple chunking):**
```bash
export LIBRARIAN_BACKEND=chroma
./venv/bin/python scripts/rebuild_library.py
```

[Source: rebuild_library.py]

## What the Rebuild Script Does

1. **Clears existing data**: Removes all chunks and metadata
2. **Backs up the index**: Creates `index.json.bak` before clearing
3. **Syncs the project directory**: Processes all documents respecting `.librarianignore`
4. **Reports results**: Shows added, updated, unchanged, and removed document counts

The script uses the settings from `CONFIGURATION.md`:
- Documents directory: `./documents`
- Backend: Configurable via `LIBRARIAN_BACKEND`
- Supported extensions: `.md`, `.txt`, `.py`, `.json`, `.yaml`, `.yml`, `.toml`

[Source: rebuild_library.py]

## Option 2: Manual Document Removal

If you want more granular control, you can:

1. **List current documents** to see what's indexed:
   ```python
   list_indexed_documents()
   ```

2. **Remove documents individually** by their ID:
   ```python
   remove_document(document_id="doc_12345")
   ```

This approach allows selective removal of specific documents without affecting others.

[Source: search_library results]

## Option 3: Clear Metadata and Backend Directly

For advanced users who want direct control over the backend and metadata store:

```python
from mcp_server.core.document_manager import DocumentManager
from mcp_server.core.metadata_store import MetadataStore
from mcp_server.backend.factory import get_backend

# Clear the backend
backend.clear()

# Clear the metadata store
metadata.clear()

# Then sync again
doc_manager = DocumentManager(backend, metadata, ignore_patterns)
doc_manager.sync_directory(path="/path/to/documents")
```

## Library Status After Rebuild

After a successful rebuild, the library will show:
- **Added**: Number of documents newly indexed
- **Updated**: Documents that were modified and re-processed
- **Unchanged**: Documents with no changes
- **Removed**: Documents that no longer exist in the source directory

## Summary of Methods

| Method | Best For | Complexity |
|--------|----------|------------|
| Rebuild Script | Full library rebuild | Low (recommended) |
| Manual Removal | Selective cleanup | Medium |
| Direct Backend Clear | Advanced users, debugging | High |

## Important Notes

- The rebuild script respects the `.librarianignore` file to maintain consistency
- Backup is created automatically before clearing data
- Source tracking prevents cross-directory document removal issues
- Both Chonkie and ChromaDB backends support the rebuild process

## Summary

The recommended approach for clearing and rebuilding the library is to use the `scripts/rebuild_library.py` script. This handles the entire process safely, with automatic backups and proper error handling.

---
**Primary Sources**: 
- `/home/peter/development/librarian-mcp/scripts/rebuild_library.py`
- `/home/peter/development/librarian-mcp/ARCHITECTURE.md`
- `/home/peter/development/librarian-mcp/CONFIGURATION.md`