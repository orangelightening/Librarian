# Validation Query 8: Document Lifecycle

**Query:**
"How does the librarian detect when documents have been modified and need re-indexing?"

---

## Response

The librarian-mcp uses a **SHA-256 checksum-based change detection system** to identify when documents have been modified and need to be re-indexed. This approach ensures efficient tracking of document changes while maintaining data integrity.

### Change Detection Mechanism

#### 1. SHA-256 Checksum Calculation
When a document is first discovered or synced, the system calculates a **SHA-256 checksum** of the file's complete content [Source: document_manager.py]. This checksum serves as a unique fingerprint for that specific version of the document.

```python
def calculate_checksum(self, file_path: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    # Read file content and update hash
    return sha256_hash.hexdigest()
```

#### 2. Checksum Storage and Comparison
- Checksums are **stored in the metadata store** along with other document information [Source: librarian-mcp]
- On subsequent sync operations, the system **recalculates the checksum** for each file
- The **new checksum is compared** against the stored checksum from previous indexing [Source: document_manager.py]

#### 3. Change Detection Logic
The DocumentManager class implements the comparison logic:

```python
existing = self.metadata.get_by_path(str(file_path))
if existing:
    if existing['checksum'] == file_meta['checksum']:
        # Document unchanged - skip processing
    else:
        # Document modified - trigger re-indexing
```

### Automatic Re-chunking Process

When a document is detected as modified (checksum mismatch), the system automatically handles the update:

1. **Removes the old document version** and its associated chunks from the index [Source: document_manager.py]
2. **Re-chunks the new content** using the configured backend (Chonkie or ChromaDB) [Source: document_manager.py]
3. **Updates the metadata** with new checksum, chunk count, and timestamp [Source: document_manager.py]

### Additional Features

#### Source Tracking
- **Source tracking ensures** documents are only removed if they were indexed from the same sync directory [Source: librarian-mcp]
- This prevents accidental deletion of documents indexed from different locations

#### Status Checking
- The **`get_document_status()` function** can be used to verify if a document is current or outdated [Source: librarian-mcp]
- This allows users to check whether a specific document needs to be re-indexed without a full sync

#### Backend Agnostic
- **Both backends** (Chonkie and ChromaDB) use the **same change detection mechanism** [Source: librarian-mcp]
- This ensures consistent behavior regardless of which vector store is being used

### Known Limitations

The checksum-based approach has one documented limitation:
- Files with the **same checksum at different paths** may not be detected as moved [Source: librarian-mcp]
- The system treats these as separate documents rather than recognizing them as the same content moved to a new location

### Summary

The librarian-mcp's change detection system is built on **SHA-256 checksums** that provide a reliable and efficient way to detect document modifications. When changes are detected, the system automatically re-chunks and re-indexes the content, maintaining search accuracy without requiring manual intervention. This approach works consistently across both supported backends and integrates seamlessly with the sync workflow, ensuring that the search index always reflects the current state of documents in the library.
