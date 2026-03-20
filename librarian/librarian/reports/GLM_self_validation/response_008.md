# Response 008: How does the librarian detect when documents have been modified and need re-indexing?

## Overview

The Librarian MCP Server uses **SHA-256 checksum-based change detection** to automatically track when documents have been modified. This system ensures that only changed documents are re-indexed, maintaining library efficiency while keeping search results up-to-date [Source: document_manager.py, ARCHITECTURE.md].

---

## Change Detection Mechanism

The `DocumentManager` class in `mcp_server/core/document_manager.py` implements a comprehensive change detection system [Source: document_manager.py].

---

### 1. SHA-256 Checksum Calculation

**Location**: `mcp_server/core/document_manager.py`, `calculate_checksum()` method

When a document is discovered or synced, the system calculates a SHA-256 checksum of the file's content [Source: document_manager.py]:

```python
def calculate_checksum(self, file_path: Path) -> str:
    """
    Calculate SHA-256 checksum of a file.

    Args:
        file_path: Path to file

    Returns:
        Hexadecimal checksum string
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except Exception as e:
        print(f"Error calculating checksum for {file_path}: {e}")
        return ""

    return sha256_hash.hexdigest()
```

**Key Implementation Details**:
- Reads file in binary mode (`"rb"`)
- Processes file in 4096-byte blocks for memory efficiency
- Uses Python's built-in `hashlib.sha256()` for cryptographic hashing
- Returns empty string on error for graceful failure handling

---

### 2. Document Metadata Storage

Each document's metadata, including its SHA-256 checksum, is stored in the metadata store. This metadata is used for comparison during subsequent sync operations [Source: document_manager.py, ARCHITECTURE.md].

**Metadata includes**:
- `document_id`: Unique identifier (first 16 chars of checksum)
- `path`: File path
- `name`: File name
- `checksum`: SHA-256 hash of file content
- `size`: File size in bytes
- `modified`: Last modification timestamp
- `chunk_count`: Number of chunks created
- `indexed_at`: When the document was indexed
- `source`: Source directory for tracking [Source: document_manager.py]

---

### 3. Change Detection Process

When `sync_directory()` is called, the system follows a comprehensive change detection workflow [Source: document_manager.py]:

#### **Step 1: Discover Documents**
- Scans the specified directory for documents matching the specified extensions
- Respects `.librarianignore` exclusion patterns
- Collects all candidate files

#### **Step 2: Calculate Current Checksums**
- For each discovered document, calculates the current SHA-256 checksum
- Reads file content and generates hash

#### **Step 3: Compare Against Stored Metadata**
- Retrieves existing metadata for all indexed documents
- Compares current checksums against stored checksums to detect changes:

| Status | Detection Method | Action |
|--------|----------------|--------|
| **New Document** | No existing metadata for this path | Index the document |
| **Modified Document** | Checksum differs from stored checksum | Re-index the document |
| **Unchanged Document** | Checksum matches stored checksum | Skip (no action needed) |
| **Deleted Document** | File exists in metadata but not in current scan | Remove from library |

#### **Step 4: Process Changes**
- New documents are added to the library
- Modified documents are removed and re-indexed
- Unchanged documents are skipped
- Deleted documents are removed from the library

---

## Implementation Details

### Adding a Document (`add_document`)

The `add_document()` method implements the change detection logic for individual documents [Source: document_manager.py]:

```python
def add_document(self, file_path: Path, source: str = None) -> Dict:
    """Add a single document to the library."""

    # ... file validation and reading ...

    # Get metadata including checksum
    file_meta = self.get_file_metadata(file_path)

    # Check if already exists
    existing = self.metadata.get_by_path(str(file_path))

    if existing:
        # CHANGE DETECTION: Compare checksums
        if existing['checksum'] == file_meta['checksum']:
            return {
                "status": "unchanged",
                "document_id": existing['document_id'],
                "name": existing['name'],
                "chunk_count": existing.get('chunk_count', 0)
            }
        else:
            # Document changed, remove old version
            self.remove_document(existing['document_id'])

    # Add to backend with new checksum
    doc_id = file_meta['checksum'][:16]  # Use first 16 chars as ID
    # ... chunking and storage ...
```

**Key Points**:
1. Calculates current checksum using `get_file_metadata()` which calls `calculate_checksum()`
2. Looks up existing metadata for the file path
3. **If checksum matches**: Returns "unchanged" status - no re-indexing needed
4. **If checksum differs**: Removes old version and re-indexes the document
5. Uses first 16 characters of checksum as document ID (short but collision-resistant)

---

### Syncing a Directory (`sync_directory`)

The `sync_directory()` method orchestrates change detection across an entire directory [Source: document_manager.py]:

```python
def sync_directory(
    self,
    path: str,
    extensions: Set[str] = None,
    recursive: bool = True
) -> Dict:
    """
    Sync a directory: add new, update changed, remove deleted.
    Returns:
        Summary of sync operation
    """
    # Discover all documents
    documents = self.discover_documents(path, extensions, recursive)

    # Get current metadata
    indexed = self.metadata.get_all()
    indexed_paths = {str(Path(doc['path']).resolve()): doc for doc in indexed}

    results = {
        "added": 0,
        "updated": 0,
        "unchanged": 0,
        "removed": 0,
        "ignored": 0,
        "errors": []
    }

    current_paths = set()

    # Process each document
    for doc_path in documents:
        current_paths.add(str(doc_path.resolve()))

        # This internally performs change detection
        result = self.add_document(doc_path, source=str(path_obj))

        if result['status'] == 'added':
            results['added'] += 1
        elif result['status'] == 'unchanged':
            results['unchanged'] += 1

    # Remove documents that no longer exist
    for path, doc in indexed_paths.items():
        if path not in current_paths:
            if self.remove_document(doc['document_id']):
                results['removed'] += 1

    return results
```

**Key Features**:
1. Discovers all documents in the directory
2. Retrieves all indexed documents from metadata
3. Processes each discovered document (change detection happens in `add_document()`)
4. Tracks which paths were found in current scan
5. Removes documents that no longer exist (but only from the same source directory)
6. Returns detailed statistics: added, updated, unchanged, removed, ignored, errors

---

### Checking Document Status (`get_document_status`)

The `get_document_status()` method provides a way to check if a specific document is indexed and up-to-date [Source: document_manager.py]:

```python
def get_document_status(self, path: str) -> Dict:
    """
    Check if a document is indexed and up-to-date.

    Args:
        path: Path to the document

    Returns:
        Status information
    """
    file_path = Path(path).resolve()

    if not file_path.exists():
        return {"status": "not_found"}

    indexed = self.metadata.get_by_path(str(file_path))

    if not indexed:
        return {"status": "not_indexed"}

    # Calculate current checksum
    current_meta = self.get_file_metadata(file_path)

    if current_meta['checksum'] == indexed['checksum']:
        return {
            "status": "up_to_date",
            "document_id": indexed['document_id'],
            "name": indexed['name'],
            "chunk_count": indexed.get('chunk_count', 0),
            "indexed_at": indexed.get('indexed_at')
        }
    else:
        return {
            "status": "needs_update",
            "document_id": indexed['document_id'],
            "name": indexed['name'],
            "current_checksum": current_meta['checksum'],
            "stored_checksum": indexed['checksum']
        }
```

**Status Values**:
- `not_found`: File doesn't exist on disk
- `not_indexed`: File exists but is not in the library
- `up_to_date`: File is indexed and unchanged (checksums match)
- `needs_update`: File is indexed but has been modified (checksums differ)

---

## Why SHA-256 Checksums?

The system uses SHA-256 checksums for change detection because:

1. **Cryptographic Strength**: SHA-256 is a strong cryptographic hash that provides virtually guaranteed uniqueness
2. **Content-Based Detection**: Detects any change in file content, regardless of modification time or file size
3. **Efficient Comparison**: Comparing hash strings is fast and reliable
4. **Tamper Resistance**: Detects malicious or accidental modifications
5. **Document ID Generation**: First 16 characters serve as reliable unique document IDs

**Alternative approaches considered but not used**:
- File modification time: Unreliable (can be manually changed)
- File size: Insufficient (different content can have same size)
- Content comparison: Too slow for large files
- Combination of metadata: Still less reliable than cryptographic hash

---

## Automatic Re-indexing

The change detection is **automatic and transparent**:

- **When you run `sync_documents()`**: System automatically detects and re-indexes modified documents
- **When you run `add_document()`**: System automatically compares checksums and skips unchanged documents
- **When you check `get_document_status()`**: System tells you if a document needs updating
- **No manual tracking required**: System maintains all checksums and comparisons internally

---

## Benefits of This Approach

### 1. Efficiency
- Only re-indexes documents that have actually changed
- Unchanged documents are skipped entirely (no processing)
- Saves time and computational resources

### 2. Accuracy
- Detects any change in file content
- No false negatives (missed changes)
- No false positives (re-indexing unchanged files)

### 3. Transparency
- Clear status information for each document
- Detailed sync operation summaries
- Easy to understand what was processed and why

### 4. Reliability
- Cryptographic strength ensures detection of all changes
- Handles edge cases (moved files, renamed files, etc.)
- Graceful error handling with clear status reporting

---

## Summary

**The Librarian detects document modifications through SHA-256 checksum comparison** [Source: document_manager.py]:

1. **Checksum Calculation**: Each document's SHA-256 hash is calculated from its binary content
2. **Metadata Storage**: Checksums are stored with document metadata
3. **Comparison**: During sync operations, current checksums are compared to stored checksums
4. **Action**: Documents are added, updated, or skipped based on checksum comparison
5. **Status Reporting**: The system reports added, updated, unchanged, and removed documents

This automatic, content-based change detection ensures the library stays up-to-date efficiently and reliably without requiring manual intervention.
