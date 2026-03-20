# Query 15: Troubleshooting

**Status**: success
**Tokens Used**: 417
**Timestamp**: 2026-03-18T19:21:41.487656
**Tool Calls**: 2

---

If you're having trouble finding documents in the library that you believe exist, here are several troubleshooting steps:

## 1. **Check Library Status First**

Let's verify what's actually indexed:


Good! The library has **42 documents** indexed with a total of **439 chunks**. Now I can help troubleshoot common issues:

## Common Issues & Solutions

### 1. **Document Not Indexed Yet**
If you know a file exists but it's not in the list above, it may need to be synced:

- Use `sync_documents(path)` to add entire directories
- Or use `add_document(path)` for individual files
- Check if the document is being ignored (see `.librarianignore`)

### 2. **Search Terms Too Broad**
Semantic search might not find documents with different terminology. Try:
- More specific keywords from the actual content
- Different phrasing of your query
- Combining multiple related terms

### 3. **Document Exists But Outdated**
Documents can become outdated if they're modified after indexing. Use `get_document_status(path)` to check if a document needs re-indexing.

### 4. **File in Ignored Directory**
Check the `.librarianignore` file - files matching those patterns won't be indexed.

---

## What Would You Like Me To Do?

To help you specifically, could you tell me:

1. **What document(s) are you looking for?** (file names or topics)
2. **Where do you expect them to be located?** (directory paths)
3. **Have you tried searching with specific terms?** What did you search for?

I can then:
- Search the file system for those files
- Check their indexing status
- Sync them into the library if needed
- Help refine your search queries