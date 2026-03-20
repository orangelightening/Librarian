# Query 11: File Reading Capabilities

**Status**: success
**Tokens Used**: 399
**Timestamp**: 2026-03-18T19:21:41.487332
**Tool Calls**: 0

---

Based on the available tools, here's what I can do regarding file reading:

## File Reading Capabilities

### 1. **Read Full Documents**
I can read entire files within the allowed directory using `read_document(path)`. This returns up to 8000 characters by default.

[Source: Tool documentation]

### 2. **Read Specific Portions of Files**
Yes, I can read specific portions of files in several ways:

- **Line ranges**: Read lines 100-150 using `start_line=100, end_line=150`
- **First N lines**: Read the first 20 lines using `head=20`
- **Last N lines**: Read the last 20 lines using `tail=20`
- **Custom character limit**: Limit to specific number of characters using `max_chars=20000`

[Source: Tool documentation]

### 3. **Document Summaries**
I can get structural summaries without reading full content using `document_summary(path)`. This shows:
- Markdown heading hierarchy with line numbers
- Functions and classes for Python/JS/TS files
- Line/word count and first few lines for text files

[Source: Tool documentation]

### 4. **Search Within Files**
I can search for specific text strings across documents using `search_documents(query, path, extension)`, which returns matching file paths with line numbers.

[Source: Tool documentation]

## Important Limitations

- I can only read files within the **allowed directory scope**
- I must respect the `.librarianignore` exclusions
- I cannot access sensitive files (credentials, private keys, .env files)
- File reading is limited to whitelisted operations for security

Would you like me to demonstrate any of these capabilities on a specific file in your workspace?