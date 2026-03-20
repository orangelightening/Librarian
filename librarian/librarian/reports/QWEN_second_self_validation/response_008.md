# Query 8: Document Modification Detection

## How Does the Librarian Detect When Documents Have Been Modified?

### Overview

The librarian uses a **checksum-based change detection system** that operates during sync operations. This approach efficiently identifies new, modified, and unchanged documents by comparing SHA-256 file checksums against stored metadata.

### Change Detection Process

When `sync_directory()` is called, the system follows this workflow:

```
1. Discovers all documents in the specified directory
   ↓ [filters through .librarianignore patterns]
2. Calculates current SHA-256 checksums for each file
   ↓ [compares against stored metadata]
3. Detects changes:
   - New document: No existing metadata for this path
   - Modified document: Checksum differs from stored checksum
   - Unchanged document: Checksum matches stored checksum
   - Deleted document: Path exists in metadata but not on disk
```

### Technical Implementation

**Source Tracking Mechanism:**
- Each document's path and content is tracked via metadata storage
- SHA-256 checksums provide a reliable, collision-resistant fingerprint
- Checksum comparison is efficient and handles most change scenarios

**Automatic Updates:**
- During sync operations, modified documents are automatically re-indexed
- The system recalculates chunks for any document whose checksum changed
- No manual intervention required for routine updates

**Status Verification:**
- The `get_document_status()` tool can verify if a document is current or outdated
- Useful for manual checks or troubleshooting sync issues

### Edge Cases and Limitations

**Known Limitation - File Moves:**
- Files with the same checksum at different paths may not be detected as moved
- The checksum-based approach assumes document identity is tied to path, not content alone

**Best Practice:**
- For robust change detection, maintain consistent file paths
- If moving documents, consider removing the old path first to trigger re-creation

### Benefits of Checksum-Based Detection

1. **Efficiency**: Single hash comparison instead of full content comparison
2. **Reliability**: SHA-256 provides near-zero collision probability
3. **Speed**: Minimal overhead for large document libraries
4. **Automatic**: Seamless integration into sync workflow without user intervention

### Example Workflow

```bash
# User calls sync
sync_documents(path="/home/peter/docs", extensions=".md,.txt")

# System detects:
# - 3 new .md files → Added to index
# - 1 .txt file modified (checksum changed) → Re-indexed
# - 5 .md files unchanged → Skipped
# - 2 .py files removed → Removed from index
```

### Conclusion

The librarian's checksum-based detection system provides a robust, efficient mechanism for identifying document modifications. This approach balances performance with reliability, automatically handling routine updates while maintaining an accurate, up-to-date index of all tracked documents.

[Source: librarian-mcp]