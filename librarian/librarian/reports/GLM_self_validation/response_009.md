# Response 009: How do I clear and rebuild the entire document library index?

## Overview

The Librarian MCP Server provides a **dedicated rebuild script** (`scripts/rebuild_library.py`) that clears the entire library index and re-syncs all documents from scratch. This script performs a complete rebuild while respecting `.librarianignore` patterns [Source: rebuild_library.py].

---

## Method 1: Using the Rebuild Script (Recommended)

### Basic Rebuild

The simplest way to clear and rebuild the entire library is to use the provided rebuild script [Source: rebuild_library.py]:

```bash
cd /home/peter/development/librarian-mcp
source venv/bin/activate
python scripts/rebuild_library.py
```

### Rebuild with Specific Backend

You can specify which backend to use for the rebuild by setting the `LIBRARIAN_BACKEND` environment variable [Source: rebuild_library.py]:

```bash
# Use Chonkie backend (intelligent chunking)
export LIBRARIAN_BACKEND=chonkie
source venv/bin/activate
python scripts/rebuild_library.py

# Use ChromaDB backend (simple chunking)
export LIBRARIAN_BACKEND=chroma
source venv/bin/activate
python scripts/rebuild_library.py
```

---

## What the Rebuild Script Does

The `rebuild_library.py` script performs the following operations [Source: rebuild_library.py]:

### 1. Initialization

```python
print("=" * 70)
print("Rebuilding Librarian Library")
print("=" * 70)
print(f"Project directory: {Settings.PROJECT_ROOT}")
print(f"Documents directory: {Settings.DOCUMENTS_DIR}")
print(f"Backend: {Settings.BACKEND}")
```

The script displays:
- Project directory path
- Documents directory path
- Backend being used
- Chunking method (if available)

---

### 2. Backend Initialization

```python
backend = get_backend(
    backend_type=Settings.BACKEND,
    collection_name=Settings.CHROMA_COLLECTION,
    db_path=Settings.CHROMA_PATH
)
```

Creates the backend instance using the backend factory, with the configured:
- Backend type (chonkie or chroma)
- ChromaDB collection name
- ChromaDB database path

---

### 3. Clear Existing Library

```python
print("Clearing existing library...")
print("-" * 70)
backend.clear()
metadata.clear()
print()
```

**This performs a complete reset**:
- **`backend.clear()`**: Removes all chunks from the ChromaDB vector store
- **`metadata.clear()`**: Clears all document metadata

---

### 4. Sync the Project Directory

```python
print("Starting sync...")
result = doc_manager.sync_directory(
    path=str(Settings.PROJECT_ROOT),
    extensions={'.md', '.txt', '.py', '.json', '.yaml', '.yml', '.toml'},
    recursive=True
)
```

Re-syncs the entire project directory with:
- Full recursive scan
- Specified file extensions
- Respect for `.librarianignore` patterns

---

### 5. Display Results

```python
print()
print("=" * 70)
print("Sync Completed!")
print("=" * 70)
print(f"  Added: {result['added']} documents")
print(f"  Updated: {result['updated']} documents")
print(f"  Unchanged: {result['unchanged']} documents")
print(f"  Removed: {result['removed']} documents")
print(f"  Ignored: {result.get('ignored', 0)} files (excluded by .librarianignore)")
```

Shows comprehensive statistics:
- Documents added (all in a fresh rebuild)
- Documents updated (0 in fresh rebuild)
- Documents unchanged (0 in fresh rebuild)
- Documents removed (0 in fresh rebuild)
- Files ignored (excluded by `.librarianignore`)

---

## Example Output

Here's what the rebuild output looks like [Source: rebuild_library.py documentation]:

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
======================================================================
  Added: 39 documents
  Updated: 0 documents
  Unchanged: 0 documents
  Removed: 0 documents
  Ignored: 127 files (excluded by .librarianignore)
```

---

## Method 2: Manual Document Removal

If you prefer to remove documents manually rather than doing a complete rebuild, you can use the MCP tools directly:

### Step 1: List All Documents

```python
list_indexed_documents()
```

This shows all documents currently in the library with their IDs and paths.

### Step 2: Remove Documents One by One

```python
remove_document(document_id="doc_12345")
```

Repeat for each document you want to remove.

**Note**: This approach is tedious for large libraries but gives you fine-grained control over which documents to remove.

---

## Method 3: File System Cleanup

If you want to start completely fresh at the file system level:

### Delete ChromaDB Database

```bash
rm -rf /path/to/chroma_db
```

### Delete Metadata

```bash
rm -rf /path/to/metadata
```

### Restart and Re-sync

The library will start empty, and you can re-add documents using:
- `add_document()` - Add individual documents
- `sync_documents()` - Sync entire directories

**Warning**: This is the most destructive approach and should be used with caution.

---

## Backend-Specific Considerations

### Rebuild with Different Backend

You can rebuild the library with a different backend to change the chunking strategy:

```bash
# Rebuild with Chonkie (intelligent semantic chunking)
export LIBRARIAN_BACKEND=chonkie
python scripts/rebuild_library.py

# Rebuild with ChromaDB (simple sentence-based chunking)
export LIBRARIAN_BACKEND=chroma
python scripts/rebuild_library.py
```

**Note**: Both backends use the same ChromaDB database, so switching backends doesn't require database migration. The rebuild script will clear and re-populate the database with the new backend's chunking strategy [Source: CHONKIE_MIGRATION.md, rebuild_library.py].

---

## Configuration Settings

The rebuild script uses settings from `mcp_server/config/settings.py` [Source: rebuild_library.py, settings.py]:

### Key Settings Used

```python
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCUMENTS_DIR = os.getenv("LIBRARIAN_DOCUMENTS_DIR", str(PROJECT_ROOT / "documents"))
CHROMA_PATH = os.getenv("LIBRARIAN_CHROMA_PATH", str(PROJECT_ROOT / "chroma_db"))
CHROMA_COLLECTION = os.getenv("LIBRARIAN_CHROMA_COLLECTION", "documents")
BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")
```

You can override these settings with environment variables before running the rebuild.

---

## Rebuild with Custom Directory

The rebuild script syncs the project root by default. If you want to rebuild a specific directory instead, you have two options:

### Option 1: Modify the Script

Edit `scripts/rebuild_library.py` and change the path in the sync call:

```python
result = doc_manager.sync_directory(
    path="/path/to/your/specific/directory",  # Custom path
    extensions={'.md', '.txt', '.py', '.json', '.yaml', '.yml', '.toml'},
    recursive=True
)
```

### Option 2: Use MCP Tools

```python
# Clear the library using backend.clear() if you have access
# Then sync the specific directory
sync_documents(
    path="/path/to/your/specific/directory",
    extensions=".md,.txt,.py",
    recursive=True
)
```

---

## When to Rebuild

### When to Use Complete Rebuild

- **Changed backends**: Switching between Chonkie and ChromaDB chunking
- **Corrupted index**: Library showing errors or unexpected behavior
- **Mass document changes**: When most documents have changed
- **Testing**: Starting fresh for testing purposes
- **New `.librarianignore` rules**: After adding significant exclusion patterns

### When Incremental Sync is Better

- **Small changes**: Only a few documents modified
- **Regular updates**: Normal development workflow
- **Large library**: Rebuilding takes time, sync is faster
- **Partial updates**: Only certain directories changed

---

## Troubleshooting

### Issue: Script Fails

**Problem**: Rebuild script fails with error

**Solutions**:
1. Ensure virtual environment is activated: `source venv/bin/activate`
2. Check Python version compatibility
3. Verify all dependencies installed: `pip install -r requirements.txt`
4. Check file permissions on database and metadata directories

### Issue: Documents Not Found

**Problem**: Rebuild shows 0 documents added

**Solutions**:
1. Check that documents directory exists and contains supported file types
2. Verify file extensions match default: `.md`, `.txt`, `.py`, `.json`, `.yaml`, `.yml`, `.toml`
3. Check `.librarianignore` patterns aren't excluding everything
4. Verify `LIBRARIAN_DOCUMENTS_DIR` environment variable if custom

### Issue: Backend Errors

**Problem**: Backend fails during rebuild

**Solutions**:
1. Verify ChromaDB is installed: `pip install chromadb`
2. For Chonkie backend, ensure Chonkie is installed: `pip install chonkie`
3. Check database path permissions
4. Try with different backend: `export LIBRARIAN_BACKEND=chroma`

---

## Safety Features

The rebuild script includes several safety features:

### 1. Clear Confirmation

The script clearly displays what it's doing before, during, and after the rebuild [Source: rebuild_library.py].

### 2. Detailed Statistics

Shows exact counts of added, removed, updated, and ignored documents for verification.

### 3. Error Handling

Errors are caught and displayed without crashing the entire process.

### 4. .librarianignore Respect

All `.librarianignore` patterns are respected during the rebuild, preventing sensitive files from being indexed.

---

## Summary

**To clear and rebuild the entire document library index**:

**Recommended Method**: Use the dedicated rebuild script [Source: rebuild_library.py]:
```bash
cd /home/peter/development/librarian-mcp
source venv/bin/activate
python scripts/rebuild_library.py
```

**With specific backend**:
```bash
export LIBRARIAN_BACKEND=chonkie  # or chroma
python scripts/rebuild_library.py
```

**What the script does**:
1. Initializes backend with current settings
2. Clears all chunks from ChromaDB (`backend.clear()`)
3. Clears all metadata (`metadata.clear()`)
4. Re-syncs the project directory from scratch
5. Displays detailed statistics of the rebuild

**Alternative methods**:
- Manual removal via `remove_document()` tool (tedious for many documents)
- File system cleanup (most destructive, use with caution)

**Best practices**:
- Use the rebuild script for clean, complete rebuilds
- Use incremental sync for regular updates
- Choose backend based on your needs (Chonkie for quality, ChromaDB for speed)
- Verify `.librarianignore` patterns before rebuilding
