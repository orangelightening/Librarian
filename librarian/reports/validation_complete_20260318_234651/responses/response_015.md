# Query 15: Troubleshooting

**Status**: success
**Tokens Used**: 441
**Timestamp**: 2026-03-18T23:47:19.326233
**Tool Calls**: 0

---

If you're experiencing issues where the librarian isn't finding documents that you know exist, here are some troubleshooting steps:

## Common Causes and Solutions

### 1. **Document Not Yet Indexed**
- The document might not be in the library yet
- **Solution**: Use `add_document(path)` to manually add the document, or use `sync_documents(path)` to sync a directory

### 2. **Document Status Issues**
- The document might exist but not be properly indexed
- **Solution**: Check document status with `get_document_status(path)` and sync if needed

### 3. **Search Query Too Vague**
- Semantic search might not match your specific query
- **Solution**: Try more specific search terms or use `search_documents()` for literal text matching

### 4. **File Type Not Supported**
- The document might be in a format the library doesn't support
- **Solution**: Check supported formats and convert if necessary

### 5. **Permission or Path Issues**
- The path might be outside the allowed directory
- **Solution**: Verify the path is within the allowed scope

## Diagnostic Steps

To diagnose the issue, I can help you:

1. **Check what's currently indexed**: `list_indexed_documents()`
2. **Verify document status**: `get_document_status(path)` for specific files
3. **Search the file system**: Use `list_documents()` or `search_documents()` to find files
4. **Check library stats**: `get_library_stats()` to understand scope

## Quick Fixes

Would you like me to:
- **Sync a specific directory** to ensure all documents are indexed?
- **Manually add a specific document** to the library?
- **Search the file system** for documents that might exist but aren't indexed?
- **Check the status** of specific documents you're having trouble finding?

Please let me know:
1. What type of documents you're looking for
2. Where they should be located (path)
3. What search terms you've tried

This will help me provide the most targeted assistance.
