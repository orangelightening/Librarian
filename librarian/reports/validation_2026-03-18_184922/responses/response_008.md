# Query 8: Document Lifecycle

**Status**: success
**Tokens Used**: 1484
**Timestamp**: 2026-03-18T19:21:41.487132
**Tool Calls**: 12

---

I'll help you understand how document modification detection works in this library system. Let me search for relevant information about change detection and indexing mechanisms.


Great! I found relevant information about the change detection mechanism. Let me get more details from the key source documents to provide a comprehensive answer.


Let me check what documents are currently indexed in the library and find the relevant source files.


Perfect! I can see the relevant source documents. Let me read the key files that contain information about change detection - specifically `document_manager.py` and `USER_GUIDE.md`.


Now let me read the USER_GUIDE.md to get more context about the change detection mechanism:


Let me continue reading the USER_GUIDE.md to find information about change detection:


Let me search more broadly:


Let me read the ARCHITECTURE.md file which was mentioned in the search results:


Perfect! I found the key information. Let me also check if there's a FEATURES.md or similar document that might have more details:


Excellent! Now I have enough information to provide a comprehensive answer. Let me compile the findings from the source documents.

---

Based on the library documentation, here's how the Librarian detects when documents have been modified and need re-indexing:

## Change Detection Mechanism

The Librarian uses **SHA-256 checksums** for automatic change detection, ensuring that modified documents are automatically re-indexed. [Source: ARCHITECTURE.md]

### How It Works

1. **Checksum Calculation**: When a document is processed, the system calculates its SHA-256 hash by reading the entire file content in 4096-byte blocks. [Source: mcp_server/core/document_manager.py]

```python
def calculate_checksum(self, file_path: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
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

[Source: mcp_server/core/document_manager.py]

2. **Metadata Storage**: Each document's metadata includes its checksum, allowing the system to track changes over time. [Source: mcp_server/core/document_manager.py]

3. **Change Detection Logic**: During sync operations, the system compares current file checksums against stored metadata:
   - If checksums match → Document is unchanged (no re-indexing needed)
   - If checksums differ → Document has been modified (re-indexed automatically) [Source: mcp_server/core/document_manager.py]

```python
# Check if already exists
existing = self.metadata.get_by_path(str(file_path))
if existing:
    if existing['checksum'] == file_meta['checksum']:
        return {"status": "unchanged", ...}  # No re-indexing needed
    else:
        # Document changed, remove old version and re-add
        self.remove_document(existing['document_id'])
```

[Source: mcp_server/core/document_manager.py]

### Sync Behavior

When running `sync_documents()`, the system reports changes accurately:
- **Added**: New files not previously indexed
- **Updated**: Files with changed checksums (re-indexed)
- **Unchanged**: Files with matching checksums (skipped) [Source: mcp_server/core/document_manager.py]

### Important Note

There is a known bug where file moves (same content, different path) may be incorrectly reported as "added" instead of "updated," though this doesn't affect the actual search functionality. [Source: ARCHITECTURE.md]

---

**Would you like me to:**
1. Explain how the chunking strategy works for re-indexed documents?
2. Show you how to manually check if a specific document is up-to-date?
3. Discuss the sync operation workflow in more detail?