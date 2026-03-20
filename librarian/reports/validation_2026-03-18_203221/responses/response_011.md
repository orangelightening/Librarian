# Query 11: File Reading Capabilities

**Status**: success
**Tokens Used**: 482
**Timestamp**: 2026-03-18T21:01:50.575293
**Tool Calls**: 0

---

The librarian has several file reading capabilities through the `read_document` tool:

## File Reading Capabilities

**1. Read Entire Files (up to 8000 characters)**
- Simply provide the path to read a complete document
- Default limit is 8000 characters for security

**2. Read Specific Line Ranges**
- Use `start_line` and `end_line` parameters (1-based, inclusive)
- Example: Lines 100-150 of a file

**3. Read First N Lines (Head)**
- Use the `head` parameter to read the first N lines
- Useful for quickly viewing document beginnings

**4. Read Last N Lines (Tail)**
- Use the `tail` parameter to read the last N lines
- Great for checking recent changes or endings of files

**5. Custom Character Limits**
- Use `max_chars` to specify a custom maximum character count
- Default is 8000, but can be increased up to 20000 characters

## Examples:

```python
# Read entire file (up to 8000 chars)
read_document("/path/to/file.txt")

# Read first 50 lines
read_document("/path/to/file.txt", head=50)

# Read last 50 lines
read_document("/path/to/file.txt", tail=50)

# Read specific line range (lines 100-150)
read_document("/path/to/file.txt", start_line=100, end_line=150)

# Read up to 20000 characters
read_document("/path/to/file.txt", max_chars=20000)
```

## Additional Reading Tools:

- **`document_summary(path)`** - Get a structural overview without reading full content (shows heading hierarchy for Markdown, functions/classes for code files, line/word counts for text files)

- **`list_documents(path, extension, recursive)`** - Explore directory structure to find relevant files before reading them

These capabilities allow you to efficiently access specific portions of files when needed, rather than always having to read entire documents. This is particularly useful for large files or when you're looking for specific sections of code or documentation.