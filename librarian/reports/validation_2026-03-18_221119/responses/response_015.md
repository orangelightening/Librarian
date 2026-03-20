# Query 15: Troubleshooting

**Status**: success
**Tokens Used**: 522
**Timestamp**: 2026-03-18T22:13:06.525627
**Tool Calls**: 0

---

If the Librarian isn't finding documents that you know exist, we need to troubleshoot the search mechanism and the library's current state. Here is a step-by-step guide to resolving this:

### 1. Check Library Statistics and Scope
First, let's verify what is actually in the library. Sometimes documents exist in the file system but haven't been indexed yet.
*   Run `get_library_stats()` to see the total document count and chunk count.
*   Run `list_indexed_documents()` to see a sample of what is currently indexed.

### 2. Verify Document Inclusion (`.librarianignore`)
The Librarian respects the `.librarianignore` file. If your document is listed there, it will be excluded from the library entirely.
*   **Action:** Check if your document path appears in `.librarianignore`.
*   **Fix:** Remove the path from the ignore list if it was accidentally added.

### 3. Check Document Status
A document might be in the library but marked as "stale" or needing re-indexing.
*   **Action:** Run `get_document_status(path)` for the specific file to see if it is current.
*   **Fix:** If it's outdated, run `sync_documents(path)` or `add_document(path)` to refresh the index.

### 4. Refine the Search Query
Semantic search requires specific terminology. If you search for "hello" but the document only says "Greetings," the match might fail.
*   **Action:** Try searching for specific keywords found *inside* the document (e.g., exact phrases, technical terms) rather than broad concepts.
*   **Action:** Try a literal text search using `search_documents(query, path, extension)` if semantic search fails.

### 5. Manual Verification
If the Librarian still cannot find it, we can manually verify the file is present and readable.
*   **Action:** Use `list_documents(path, extension, recursive)` to confirm the file exists in the directory structure.
*   **Action:** Use `document_summary(path)` to get a quick overview of the file's content.

### 6. Add Documents Manually
If the file exists but isn't in the library, you can add it directly.
*   **Action:** Run `add_document(path)` to ingest the file immediately.

---

**Would you like me to start by checking the library stats and listing the indexed documents to see what is currently available?**