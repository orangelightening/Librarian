# Query 8: Document Lifecycle

**Status**: success
**Tokens Used**: 584
**Timestamp**: 2026-03-18T23:33:16.593281
**Tool Calls**: 0

---

Based on the library content, the librarian system detects document modifications using **SHA-256 checksums** as the primary mechanism:

## Change Detection Mechanism

**[Source: features.md]**
> Change detection uses SHA-256 checksums...

## How It Works

1. **During Sync Operations**:
   - When `sync_documents()` is called, the system calculates SHA-256 checksums for all discovered files
   - These checksums are compared against stored metadata to detect changes
   - Both backends (Chonkie and ChromaDB) use the same change detection mechanism

2. **During Document Processing**:
   - The `calculate_checksum()` function computes the SHA-256 hash of each file
   - This checksum is stored in the document metadata
   - When a new file is discovered, its checksum is compared against existing indexed documents

3. **Status Checking**:
   - The `get_document_status()` function checks if a document is indexed and up-to-date
   - It compares the current file checksum against the stored metadata checksum
   - Returns one of three statuses:
     - `unchanged`: Document hasn't been modified
     - `current`: Document is indexed and current
     - `not_found`/`not_indexed`: Document doesn't exist or isn't indexed

## What Gets Re-indexed

**[Source: librarian-mcp]**
> ✅ Changed documents are re-chunked automatically

When a document's checksum changes (indicating modification):
- The old document version is removed from the index
- The new content is re-chunked (typically into 1000-character segments)
- New chunks are added to the backend (ChromaDB or Chonkie)

## Important Limitation

**[Source: librarian-mcp]**
> The logic doesn't detect when a file with the same checksum exists at a different path.

There's a known bug where files moved to different paths with unchanged content may be incorrectly reported as "added" rather than "updated."

Would you like me to show you how to check the status of a specific document, or explore the implementation details further?
