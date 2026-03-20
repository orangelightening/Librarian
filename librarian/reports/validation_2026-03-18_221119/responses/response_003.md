# Query 3: Tool Count and Categorization

**Status**: success
**Tokens Used**: 668
**Timestamp**: 2026-03-18T22:13:06.524865
**Tool Calls**: 0

---

Based on the library tools defined in my system instructions, I have access to the following **10 tools**:

### Library Tools
1.  **`search_library(query, limit)`**
    *   Performs semantic search across all indexed documents.
    *   *Usage:* Default limit is 5 results; adjust based on query complexity.

2.  **`sync_documents(path, extensions, recursive)`**
    *   Syncs entire directories into the library.
    *   *Usage:* Specify file extensions to filter types; useful for adding new documents.

3.  **`add_document(path)`**
    *   Adds individual documents to the library.
    *   *Usage:* Good for quick additions without a full directory sync.

4.  **`remove_document(document_id)`**
    *   Removes a specific document from the library.
    *   *Usage:* Clean up outdated or erroneous entries by ID.

5.  **`list_indexed_documents()`**
    *   Lists all documents currently in the library.
    *   *Usage:* Understand the scope of available content.

6.  **`get_document_status(path)`**
    *   Checks if a document is indexed and current.
    *   *Usage:* Identifies documents that need updating or re-indexing.

7.  **`get_library_stats()`**
    *   Retrieves statistics about the library.
    *   *Usage:* Get counts for document chunks, total documents, etc.

### CLI Tools
8.  **`execute_command(command, args, cwd)`**
    *   Executes whitelisted commands within the system.
    *   *Usage:* Restricted for security; only whitelisted commands allowed.

9.  **`read_document(path, args)`**
    *   Reads full file contents.
    *   *Usage:* Used after a search to get complete context for a specific file.

10. **`list_documents(path, extension, recursive)`**
    *   Explores the directory structure.
    *   *Usage:* Find relevant files before reading them.

11. **`search_documents(query, path, extension)`**
    *   Performs literal text search within files.
    *   *Usage:* Complements semantic search when specific keywords are needed.

12. **`document_summary(path)`**
    *   Provides a quick overview of a document.
    *   *Usage:* Good for understanding structure without reading the entire file.

*(Note: While the instructions list 12 tools, `remove_document` is typically a management action rather than a direct "tool" in the same sense as the others, but it is listed as a distinct capability. If strictly counting the functional tool classes: 7 Library Tools + 5 CLI Tools = 12 total capabilities.)*

**Summary:**
*   **Library Management Tools:** 7
*   **File System/CLI Tools:** 5
*   **Total Capabilities:** 12

Would you like me to check the current status of the library or list the actual documents available? `[Source: system_instructions]`