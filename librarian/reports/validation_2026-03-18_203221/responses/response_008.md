# Query 8: Document Lifecycle

**Status**: success
**Tokens Used**: 1339
**Timestamp**: 2026-03-18T21:01:50.575009
**Tool Calls**: 8

---

I'll search the library for information about document modification detection and re-indexing mechanisms.


Great! I found relevant information. Let me read the full documents to provide you with complete details about how document modification detection works.


Let me check what documents are indexed in the library to find the correct paths.


Perfect! Now let me read the key documents that contain information about change detection and re-indexing.


Excellent! Now let me read the USER_GUIDE.md and IMPLEMENTATION_SUMMARY.md documents to get more context about the change detection mechanism.


Now let me search for more specific information about the change detection mechanism in the USER_GUIDE.md document.


Let me search the library with a different query to find more information about the change detection mechanism.


Perfect! Now let me read the metadata_store.py to understand how checksums are used for change detection.


Excellent! Now I have a complete understanding of how the librarian detects document modifications. Let me provide you with a comprehensive answer based on the library content.

---

## How the Librarian Detects Document Modifications and Re-indexing

Based on the library documentation, here's how the librarian system works:

### **Core Mechanism: SHA-256 Checksums**

The librarian uses **SHA-256 checksums** to detect when documents have been modified. This is the primary change detection mechanism.

[Source: document_manager.py]
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

### **The Detection Process**

When documents are synced or added, the system follows this workflow:

[Source: document_manager.py]
1. **Discover Documents**: Find all files in the directory (filtered by extensions and `.librarianignore` patterns)
2. **Calculate Checksums**: Compute SHA-256 checksum for each file
3. **Check Metadata Store**: Look up if a document with that checksum already exists
4. **Compare Checksums**: 
   - If checksum matches existing → Document is unchanged (no re-indexing needed)
   - If checksum differs → Document has been modified (re-index required)

[Source: document_manager.py]
```python
# Check if already exists
existing = self.metadata.get_by_path(str(file_path))
if existing:
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
```

### **Metadata Storage**

The system stores metadata in a JSON file that tracks document information including checksums:

[Source: metadata_store.py]
- Each document has a unique `document_id` (first 16 characters of the SHA-256 checksum)
- Metadata includes: path, name, size, modified timestamp, checksum, chunk count
- The index is saved to disk for persistence across restarts

### **Re-indexing Trigger**

When a document's checksum changes:
1. Old version is removed from the library
2. New content is read and chunked
3. Chunks are re-embedded in ChromaDB (or sent to Chonkie backend)
4. Metadata is updated with new information

[Source: USER_GUIDE.md]
> "The system supports automatic change detection via SHA-256 checksums, ensuring modified documents are re-indexed automatically."

### **Important Note**

There's a known bug in the current implementation where file moves (same content at different paths) may not be detected correctly. The sync reporting can show incorrect counts for added/updated files when files are renamed or moved to different locations.

[Source: CHONKIE_MIGRATION.md]
> "The Bug: The logic doesn't detect when a file with the **same checksum** exists at a **different path**."

---

Would you like me to explain any specific part in more detail, such as:
- How the chunking strategy works after detection?
- The sync directory process flow?
- How `.librarianignore` affects document discovery?