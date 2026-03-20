# Response 8: How the Librarian Detects Document Modifications and Handles Re-indexing

## Summary

The librarian-mcp uses a **SHA-256 checksum-based change detection system** to identify when documents have been modified and require re-indexing. This approach is efficient, reliable, and works across both backend implementations (Chonkie and ChromaDB).

## Change Detection Mechanism

### Checksum Comparison

The system calculates and stores SHA-256 checksums for all documents. On each sync operation, it compares the stored checksum against the current file's checksum to detect modifications.

**Key Code Reference:**
```python
# From document_manager.py
current_checksum = self.calculate_checksum(file_path)

if indexed['checksum'] == current_checksum:
    # Document is current - no re-indexing needed
    return {"status": "current", ...}
else:
    # Document has been modified - needs re-indexing
    return {"status": "outdated", ...}
```

[Source: document_manager.py]

### Sync Operation Flow

When `sync_directory()` is called, the system:

1. **Discovers all documents** in the target directory (respecting `.librarianignore`)
2. **Compares checksums** with stored metadata
3. **Categorizes documents** as:
   - **Added**: New documents not previously indexed
   - **Updated**: Documents with checksum mismatch (modified)
   - **Unchanged**: Documents with matching checksums
   - **Removed**: Files that no longer exist

[Source: document_manager.py]

## Automatic Re-chunking Process

When a document is detected as modified (checksum mismatch), the system performs the following steps:

1. **Removes the old document version** from the backend
2. **Re-chunks the new content** using the configured backend (Chonkie or ChromaDB)
3. **Updates metadata** with:
   - New checksum
   - New chunk count
   - Updated timestamp
4. **Re-adds the document** to the index

[Source: document_manager.py]

## Status Checking

The `get_document_status(path)` API allows users to check if a specific document needs re-indexing:

- **Status "current"**: Document is up-to-date, no action needed
- **Status "outdated"**: Document has been modified and requires re-indexing
- **Status "not_indexed"**: Document hasn't been indexed yet
- **Status "not_found"**: Document path no longer exists

[Source: document_manager.py]

## Source Tracking

For robust document lifecycle management, the system implements **source tracking**:

- Each document is tagged with the directory it was synced from
- Documents can only be removed if they were indexed from the same sync directory
- This prevents accidental removal of documents from other directories
- Legacy documents without source tracking are skipped to maintain backward compatibility

[Source: document_manager.py]

## Benefits of Checksum-Based Detection

1. **Efficiency**: Only modified files trigger re-indexing
2. **Reliability**: SHA-256 provides cryptographic verification
3. **Performance**: Fast comparison without reading full file content
4. **Cross-backend Support**: Both Chonkie and ChromaDB backends use the same detection mechanism
5. **Automatic Updates**: No manual intervention required

## Edge Cases Handled

- **File moves**: The system detects the new location and re-indexes (though there's a known limitation where files with the same checksum at different paths may not be detected as moved)
- **File deletion**: Detected via checksum comparison (file no longer exists in the scan)
- **Partial modifications**: Only the changed document is re-processed

## Summary

The librarian-mcp's change detection system uses SHA-256 checksums to efficiently identify document modifications. When changes are detected, the old document is automatically removed and re-chunked, ensuring the index always reflects the current state of the document repository.

---
**Primary Source**: `/home/peter/development/librarian-mcp/mcp_server/core/document_manager.py`
**Section**: `sync_directory()` and `get_document_status()` methods