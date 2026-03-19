# Validation Query 8: Document Lifecycle

**Query:**
"How does the librarian detect when documents have been modified and need re-indexing?"

---

## Instructions

1. Use **search_library** tool to find information about change detection
2. Use **read_document** if needed to understand the implementation
3. Formulate a comprehensive answer based on search results
4. Include proper citations using `[Source: document.md]` format
5. Write your complete response to:
   - `librarian/reports/self_validation/response_008.md`

---

## Expected Criteria

The response should:
- ✅ Explain SHA-256 checksum usage for change detection
- ✅ Describe metadata storage tracking
- ✅ Cover the sync process (add/update/remove detection)
- ✅ Explain automatic re-chunking of modified documents
- ✅ Mention both backends use the same change detection
- ✅ Include citations to documentation

---

## Completion

When done, tell me **"Query 8 complete"** and provide a brief summary of your findings.
