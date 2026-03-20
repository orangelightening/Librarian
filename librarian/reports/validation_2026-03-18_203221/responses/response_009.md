# Query 9: Rebuild Process

**Status**: success
**Tokens Used**: 625
**Timestamp**: 2026-03-18T21:01:50.575109
**Tool Calls**: 4

---

I can help you understand how to manage your document library. Let me first check what tools are available for library management and then provide guidance on clearing and rebuilding the index.


Let me check the library stats and indexed documents to understand the current state, then I'll provide guidance on clearing and rebuilding.




Based on the library information, I can see you have **42 documents** with **439 chunks** currently indexed in ChromaDB. 

## How to Clear and Rebuild the Document Library Index

Unfortunately, there isn't a direct "clear all" command available through the Librarian tools. However, here are your options:

### Option 1: Remove Documents Individually
You can remove documents one by one using their IDs. For example:
- Use `remove_document(document_id)` with each document's ID
- This removes both the document and all its chunks from the library

### Option 2: Clear via ChromaDB Directly (if you have access)
Since the backend is **ChromaDB**, if you have direct database access, you could:
1. Connect to your ChromaDB instance
2. Delete the `documents` collection entirely
3. Re-sync all documents from scratch

### Option 3: Use the rebuild script (if available)
I noticed there's a file called **rebuild_library.py** in your scripts directory. Let me check what it contains:


Perfect! There's a **rebuild script** that does exactly what you need. Here's how to use it:

## Recommended Approach: Use the Rebuild Script

The `rebuild_library.py` script will:
1. ✅ **Clear existing data** - Calls `backend.clear()` and `metadata.clear()` to remove all documents and chunks
2. ✅ **Re-sync everything** - Scans your project directory and re-indexes all documents
3. ✅ **Respects exclusions** - Honors `.librarianignore` patterns

### To execute the rebuild:

```bash
cd /home/peter/development/librarian-mcp
python scripts/rebuild_library.py
```

Or if you have it in your PATH:
```bash
rebuild_library
```

This will give you a clean slate with all documents re-indexed from scratch.

### Alternative: Manual Clear (if script doesn't work)

If the rebuild script encounters issues, you could manually remove each document by ID using `remove_document()`, but this is tedious for 42 documents.

Would you like me to help you execute the rebuild script, or do you need assistance with anything else regarding library management?