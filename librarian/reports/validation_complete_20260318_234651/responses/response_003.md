# Query 3: Tool Count and Categorization

**Status**: success
**Tokens Used**: 294
**Timestamp**: 2026-03-18T23:47:19.325099
**Tool Calls**: 0

---

The Librarian has access to **12 tools** for searching, managing, and interacting with documents. Here they are:

### **Library Management Tools:**
1. **search_library** - Semantically search across all indexed documents
2. **sync_documents** - Sync entire directories into the library
3. **add_document** - Add individual documents to the library
4. **remove_document** - Remove documents from the library by ID
5. **list_indexed_documents** - List all currently indexed documents
6. **get_document_status** - Check if a document is indexed and up-to-date
7. **get_library_stats** - Get statistics about the library

### **File System Tools:**
8. **execute_command** - Execute whitelisted commands securely
9. **read_document** - Read document contents (with truncation safeguards)
10. **list_documents** - List documents in the allowed directory
11. **search_documents** - Search for literal text across files
12. **document_summary** - Get structural summary of documents

These tools are designed to work within secure boundaries, respecting the `.librarianignore` file and only accessing files within the allowed directory scope. The library tools focus on semantic search and document management, while the file system tools provide targeted access to specific files when needed.

Would you like me to demonstrate any of these tools or help you search for specific information?
