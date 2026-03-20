# Query 3: Tool Count and Categorization

**Status**: success
**Tokens Used**: 395
**Timestamp**: 2026-03-18T21:01:50.574537
**Tool Calls**: 2

---

I can help you find out about the available tools for the librarian system. Let me check what tools are currently available.


Let me try using the server_info function to get information about available tools and configuration.


Based on the server info and my available functions, here are the tools the librarian has access to:

## Library Tools (for document management):

1. **search_library** - Semantic search across indexed documents
2. **sync_documents** - Sync directories into the library
3. **add_document** - Add individual documents
4. **remove_document** - Remove documents from the library
5. **list_indexed_documents** - List all indexed documents
6. **get_document_status** - Check document indexing status
7. **get_library_stats** - Get library statistics
8. **document_summary** - Get structural summaries of documents

## File System Tools (for CLI operations):

1. **execute_command** - Run whitelisted commands (awk, cat, cd, cut, date, diff, echo, file, find, grep, head, hostname, ls, mkdir, pwd, sort, stat, tail, test, tree, uniq, wc, whoami)
2. **read_document** - Read document contents with various options (line ranges, head/tail, max chars)
3. **list_documents** - List files in directories with filtering options

## Additional Tools:

4. **search_documents** - Literal text search within files
5. **write_document** - Write content to files in the librarian workspace
6. **server_info** - Get server configuration and allowed commands

In total, there are **12 distinct tools** available for the librarian system, covering document management, file system operations, and library administration tasks.