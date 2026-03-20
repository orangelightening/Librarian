# Query 9: Clearing and Rebuilding the Document Library

## How Do I Clear and Rebuild the Entire Document Library Index?

### Overview

**Important Notice**: There is **no direct "clear and rebuild" function** in the librarian-mcp system. The library does not provide a single command to wipe the entire index and start fresh. However, several approaches can achieve this goal depending on your specific needs.

### Current Library Status

Based on search results, the library currently contains:
- **61 documents**
- **742 chunks**

### Available Options for Clearing and Rebuilding

#### Option 1: Manual Document Removal (Recommended for Selective Cleanup)

**Process:**
1. List all indexed documents to see what exists
2. Remove documents individually by their document ID

```bash
# List current documents
list_indexed_documents()

# Then remove specific documents by ID
remove_document(document_id="doc_12345")
```

**Best For:**
- Removing specific old or deprecated documents
- Keeping some documents while clearing others
- Granular control over what remains

#### Option 2: Sync from Empty Directory (Complete Reset)

**Process:**
1. Run sync with an empty or non-existent directory
2. All existing documents will be removed from the index
3. New documents from the target directory will be added

```bash
# Sync from an empty directory removes everything
sync_documents(path="/empty/dir")
```

**Best For:**
- Complete library reset
- Starting fresh with a new document set
- Automated cleanup scripts

#### Option 3: Backend-Level Clear (Advanced)

**Process:**
1. Access the backend implementation directly
2. Clear the metadata store and collections
3. Re-run sync with new documents

**Implementation Details:**
```python
# Clear metadata store (internal method)
self._index = {}
self._save_index()

# Clear ChromaDB collection
collection.delete_documents()

# Re-run sync to rebuild from scratch
sync_documents(path="/path/to/docs")
```

**Best For:**
- Developers with backend access
- Complete system reset
- When sync alone doesn't achieve desired result

#### Option 4: Backup and Re-Sync (Safe Approach)

**Recommended Workflow:**
1. **Backup existing index** before clearing
2. **Clear the library** using one of the above methods
3. **Re-sync** with your desired document directory

```bash
# Backup current state
list_indexed_documents()
# Document IDs can be used to track what was removed

# Clear and rebuild
sync_documents(path="/path/to/new/docs")
```

### Step-by-Step Clear and Rebuild Guide

```bash
# Step 1: Backup current state (optional but recommended)
list_indexed_documents > backup_before_clear.txt

# Step 2: Remove all documents
# First, get all document IDs
list_indexed_documents | grep "document_id" | cut -d'"' -f2

# Then remove each one
remove_document(document_id="doc_001")
remove_document(document_id="doc_002")
# ... repeat for all documents

# OR use sync with empty directory to remove everything
sync_documents(path="/tmp")

# Step 3: Re-sync with your document directory
sync_documents(path="/home/peter/docs", extensions=".md,.txt")
```

### What Gets Cleared and What Persists

| Component | Cleared by Sync | Cleared by remove_document |
|-----------|-----------------|---------------------------|
| Document metadata | ✅ Yes | ✅ Yes |
| Chunked content | ✅ Yes | ✅ Yes |
| ChromaDB collection | ✅ Yes | ✅ Yes |
| `.librarianignore` patterns | ❌ No | ❌ No |
| Python virtual environment | ❌ No | ❌ No |

### Best Practices

1. **Always backup first**: Document current state before major operations
2. **Test in sandbox**: Try the operation on a copy of your documents first
3. **Verify after rebuild**: Use `list_indexed_documents()` to confirm expected documents remain
4. **Document IDs matter**: Keep track of document IDs if you need to preserve some documents

### Conclusion

While there's no single "clear and rebuild" command, the librarian provides flexible options for library maintenance. The most straightforward approach is to sync from an empty directory (removing all documents) and then sync with your desired source. For selective cleanup, manually removing documents by ID offers granular control. Always backup before performing major index operations.

[Source: librarian-mcp]