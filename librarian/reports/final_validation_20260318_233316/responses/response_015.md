# Query 15: Troubleshooting

**Status**: success
**Tokens Used**: 384
**Timestamp**: 2026-03-18T23:33:16.593784
**Tool Calls**: 0

---

If the librarian isn't finding documents you know exist, here are some troubleshooting steps:

## 1. **Check Document Index Status**
- Some documents may not be properly indexed yet
- Use `get_document_status(path)` to check if a specific document is indexed
- Use `list_indexed_documents()` to see what's currently in the library

## 2. **Verify Document Location**
- Ensure the document path is correct and accessible
- The document must be in the allowed directory
- Check if the file has a supported extension (.md, .txt, .py, etc.)

## 3. **Search the File System Directly**
- Use `search_documents()` for literal text searches
- Use `list_documents()` to explore the directory structure
- This can help identify if the file exists but isn't indexed

## 4. **Common Issues to Check**

**Document not indexed:**
- Run `sync_documents()` on the directory containing the document
- Or use `add_document()` for individual files

**Path issues:**
- Verify the path is relative or absolute as expected
- Check for typos in the path
- Ensure the directory is within the allowed scope

**Content issues:**
- Some files may be too large and get truncated during indexing
- Binary files or files with special characters may not index well
- Check `.librarianignore` to ensure the file isn't excluded

## 5. **Next Steps**

Would you like me to:
1. Check the status of a specific document you mentioned?
2. List the documents currently indexed in the library?
3. Search the file system directly for the document?
4. Help you sync a directory to ensure proper indexing?

Please provide the document path or describe what you're looking for, and I can help troubleshoot further.
