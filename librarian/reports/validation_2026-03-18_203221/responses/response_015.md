# Query 15: Troubleshooting

**Status**: success
**Tokens Used**: 413
**Timestamp**: 2026-03-18T21:01:50.575657
**Tool Calls**: 0

---

This is a common issue! Let me help you troubleshoot why the librarian might not be finding documents that exist in your file system.

## Common Causes and Solutions:

### 1. **Documents Not Indexed Yet**
The most likely reason is that documents haven't been added to the library yet. The librarian only searches indexed documents, not all files on disk.

**Check what's currently indexed:**
```
list_indexed_documents()
```

**Add missing documents:**
- For individual files: `add_document(path)`
- For directories: `sync_documents(path)`

### 2. **Wrong Search Terms**
Semantic search might not match your exact query terms.

**Try literal text search:**
```
search_documents(query="your specific term", extension=".md")
```

### 3. **File Extensions or Directory Issues**
Some files might be excluded by default (like `.librarianignore` exclusions).

**Check file structure:**
```
list_documents(path="/path/to/search", recursive=true)
```

### 4. **Documents Need Re-indexing**
If documents were recently modified, they may need to be re-synced.

**Check document status:**
```
get_document_status(path="/path/to/file.md")
```

## Quick Diagnostic Steps:

1. **First, let's see what's in your library:**
   - How many documents are currently indexed?

2. **Then check if your target files exist on disk:**
   - What directory should I search?
   - What file extensions are you looking for?

3. **Finally, try a direct search:**
   - What specific text or terms should I search for?

**Would you like me to:**
1. Show you what's currently in the library?
2. Help you sync a specific directory into the library?
3. Search your file system directly (not just indexed documents)?

Let me know which approach would help most!