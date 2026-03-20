# Validation Query 9: Rebuild Process

**Query:**
"How do I clear and rebuild the entire document library index?"

---

## Response

To clear and rebuild the entire document library index, the librarian-mcp provides a dedicated **rebuild script** that automates the process completely. There is no need for manual document removal or complex procedures.

### The Rebuild Script

The system includes a dedicated script at **`scripts/rebuild_library.py`** that performs a complete library rebuild from scratch [Source: scripts/rebuild_library.py].

### Basic Rebuild Process

The simplest way to rebuild your library is:

```bash
cd /home/peter/development/librarian-mcp
source venv/bin/activate
python scripts/rebuild_library.py
```

This command will:
1. Use the **default backend** (Chonkie) [Source: librarian-mcp]
2. Clear all existing data
3. Re-sync the entire project directory
4. Display detailed results

### Rebuilding with a Specific Backend

You can specify which backend to use for the rebuild by setting the `LIBRARIAN_BACKEND` environment variable:

#### Using Chonkie Backend (Intelligent Chunking)
```bash
export LIBRARIAN_BACKEND=chonkie
./venv/bin/python scripts/rebuild_library.py
```

#### Using ChromaDB Backend (Simple Chunking)
```bash
export LIBRARIAN_BACKEND=chroma
./venv/bin/python scripts/rebuild_library.py
```

[Source: librarian-mcp]

### What the Rebuild Script Does

The rebuild process performs the following operations in order [Source: scripts/rebuild_library.py]:

#### 1. Display Configuration Information
```
======================================================================
Rebuilding Librarian Library
======================================================================
Project directory: [path to project root]
Documents directory: [path to documents]
Backend: [chonkie or chroma]
Using backend: [backend type]
Chunking method: [recursive or other]
```

#### 2. Clear Existing Data
The script completely clears the library:
- **Clears all chunks** from the vector database collection [Source: scripts/rebuild_library.py]
- **Clears all metadata** from the metadata store [Source: scripts/rebuild_library.py]
- Example output:
```
Clearing existing library----------------------------------------------------------------------
Cleared 353 chunks from collection 'documents'
Cleared 40 documents from metadata store
```

#### 3. Sync Project Directory
The script then re-syncs the entire project directory:
- Scans all documents respecting **`.librarianignore`** patterns [Source: scripts/rebuild_library.py]
- Processes supported file extensions: `.md`, `.txt`, `.py`, `.json`, `.yaml`, `.yml`, `.toml` [Source: scripts/rebuild_library.py]
- Recursively processes all subdirectories [Source: scripts/rebuild_library.py]

#### 4. Display Results
After completion, the script shows detailed statistics:
```
======================================================================
Sync Completed!
======================================================================
  Added: 39 documents
  Updated: 0 documents
  Unchanged: 0 documents
  Removed: 0 documents
  Ignored: 12 files (excluded by .librarianignore)
```

If any errors occurred during processing, they are displayed:
```
⚠️  Errors: 2
    - [error details]
```

Finally, the script confirms completion:
```
📚 Library ready!
```

[Source: scripts/rebuild_library.py]

### Key Features of the Rebuild Process

#### Complete Reset
- **True rebuild from scratch** - the script uses `backend.clear()` and `metadata.clear()` to ensure no old data remains [Source: scripts/rebuild_library.py]
- All existing chunks and metadata are removed before re-syncing

#### Respect for Ignore Patterns
- The rebuild process **fully respects `.librarianignore`** patterns [Source: scripts/rebuild_library.py]
- Files excluded by these patterns are not indexed

#### Backend Flexibility
- Works with **both Chonkie and ChromaDB backends** [Source: scripts/rebuild_library.py]
- Uses the backend factory pattern to initialize the correct backend based on settings

#### Detailed Reporting
- Provides **comprehensive statistics** about the sync operation [Source: scripts/rebuild_library.py]
- Shows added, updated, unchanged, removed, and ignored counts
- Displays any processing errors

### When to Rebuild

You might want to rebuild the entire library when:
- Switching between backends (Chonkie ↔ ChromaDB)
- The index appears corrupted or inconsistent
- You've made significant changes to `.librarianignore` patterns
- You want to apply new chunking strategies to all documents
- Troubleshooting indexing or search issues

### Summary

The librarian-mcp provides a **single, simple command** to completely clear and rebuild the document library index. The `scripts/rebuild_library.py` script handles the entire process automatically: clearing existing data, re-syncing documents with proper extension filtering, respecting ignore patterns, and providing detailed results reporting. This eliminates the need for manual document-by-document removal and ensures a clean, consistent library state after rebuild operations.
