# Query 3: Tool Count and Categorization

**Status**: success
**Tokens Used**: 446
**Timestamp**: 2026-03-18T19:21:41.486773
**Tool Calls**: 2

---

I can provide you with a complete list of all available tools for the librarian system. Let me retrieve that information for you.


I apologize, but there appears to be an issue with retrieving the tool list. Let me try a different approach by checking the server information which should include details about available tools and their parameters.


Based on the server information and my role as the Librarian, here are all the tools available to me:

## Library Tools (for document management and search)

1. **search_library(query, limit)** - Semantic search across indexed documents
2. **sync_documents(path, extensions, recursive)** - Sync directories into the library
3. **add_document(path)** - Add individual documents to the library
4. **remove_document(document_id)** - Remove documents from the library
5. **list_indexed_documents()** - List all indexed documents
6. **get_document_status(path)** - Check document indexing status
7. **get_library_stats()** - Get library statistics

## CLI Tools (for file system access)

1. **execute_command(command, args, cwd)** - Execute whitelisted commands
2. **read_document(path, args)** - Read file contents with various options
3. **list_documents(path, extension, recursive)** - List files in directories
4. **search_documents(query, path, extension)** - Literal text search in files
5. **document_summary(path)** - Get structural overview of documents

## System Tools (for configuration)

1. **server_info()** - Get server configuration details
2. **list_available_tools()** - List all available tools and parameters

---

The librarian has access to these 12 core tools organized into three categories: library management, file system operations, and system utilities. All tools operate within the allowed directory `/home/peter/development/librarian-mcp` with write permissions in the `librarian` subdirectory.

Would you like me to demonstrate any specific tool or help you explore the library's current contents?