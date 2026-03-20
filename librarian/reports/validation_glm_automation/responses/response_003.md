# Query 3: Tool Count and Categorization

**Status**: success
**Tokens Used**: 1868
**Timestamp**: 2026-03-19T15:01:49.663787
**Tool Calls**: 0

---

I have **14 tools** available to me, organized into three categories:

## Library Management Tools (7)
1. **search_library(query, limit)** - Semantic search with AI aggregation
2. **sync_documents(path, extensions, recursive)** - Bulk directory sync
3. **add_document(path)** - Add single document
4. **remove_document(document_id)** - Remove by document ID
5. **list_indexed_documents()** - List all documents
6. **get_document_status(path)** - Check document status
7. **get_library_stats()** - Get library statistics

## File System Tools (5)
8. **read_document(path, start_line, end_line, head, tail, max_chars)** - Read files
9. **write_document(path, content, create_dirs)** - Write to /librarian/ workspace
10. **list_documents(path, extension, recursive)** - List files
11. **search_documents(query, path, extension, case_sensitive)** - Literal text search
12. **document_summary(path)** - Get file overview

## System Tools (2)
13. **execute_command(command, args, cwd)** - Execute whitelisted commands
14. **server_info()** - Get server configuration

These tools allow me to search and manage a document library, read and write files within a secure workspace, execute certain system commands, and retrieve server information. Is there a specific tool you'd like to know more about?
