# Query 3: Tool Count and Categorization

**Status**: success
**Tokens Used**: 416
**Timestamp**: 2026-03-18T23:33:16.592922
**Tool Calls**: 0

---

The Librarian has access to **13 tools** that can be used to search, manage, and analyze documents. Here they are:

### **Document Management Tools**
1. **`search_library(query, limit)`** - Search the library semantically and return aggregated results with citations
2. **`sync_documents(path, extensions, recursive)`** - Sync all documents from a directory into the library
3. **`add_document(path)`** - Add a single document to the library
4. **`remove_document(document_id)`** - Remove a document and all its chunks from the library
5. **`list_indexed_documents()`** - List all documents currently indexed in the library
6. **`get_document_status(path)`** - Check if a document is indexed and up-to-date
7. **`get_library_stats()`** - Get statistics about the library (document count, chunk count, etc.)

### **File System Tools**
8. **`execute_command(command, args, cwd)`** - Execute a whitelisted command safely inside the allowed directory
9. **`read_document(path, args)`** - Read contents of a document (supports line ranges, head/tail, max chars)
10. **`list_documents(path, extension, recursive)`** - List documents in the allowed directory with optional filters
11. **`search_documents(query, path, extension)`** - Search for text strings across documents in the allowed directory
12. **`document_summary(path)`** - Get a structural summary of a document without reading full contents

These tools allow you to:
- **Search** for information semantically or by text
- **Manage** the library (add, remove, sync, check status)
- **Explore** the file system within allowed boundaries
- **Analyze** document structure and contents
- **Get statistics** about the library's current state

Would you like me to demonstrate any of these tools or help you with a specific task?
