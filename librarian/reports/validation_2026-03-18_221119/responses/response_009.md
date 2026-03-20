# Query 9: Rebuild Process

**Status**: success
**Tokens Used**: 279
**Timestamp**: 2026-03-18T22:13:06.525247
**Tool Calls**: 0

---

I searched the library for information on how to clear and rebuild the entire document index.

[Source: manage.md]
The documentation indicates that to clear the index, you should use the `remove_document` tool with the document ID, or potentially clear the entire index if a bulk operation exists (though specific syntax isn't detailed in the current snippets).

However, upon reviewing the available tools and documentation, **there is no specific command or documented procedure listed for "clearing and rebuilding the entire index" as a single atomic operation.**

The available management tools are:
*   `remove_document(document_id)`: Removes a single document by ID.
*   `sync_documents(path, extensions, recursive)`: Syncs directories into the library (which would re-index existing files, but not necessarily clear the current index structure first).
*   `add_document(path)`: Adds individual documents.

**There is insufficient data in the library to answer this question with a specific command.**

Would you like me to:
1.  Search the file system for configuration files (like `config.json` or `setup.py`) that might contain the rebuild logic?
2.  Help you manually remove documents one by one if you have a list of IDs?
3.  Assist you in syncing a fresh set of documents to ensure the index reflects the latest state?