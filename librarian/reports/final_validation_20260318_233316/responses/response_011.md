# Query 11: File Reading Capabilities

**Status**: success
**Tokens Used**: 445
**Timestamp**: 2026-03-18T23:33:16.593496
**Tool Calls**: 0

---

Based on the librarian's capabilities, here's what I can tell you about file reading:

## File Reading Capabilities

The librarian has comprehensive file reading capabilities with several options:

### 1. **Full File Reading**
- Can read entire files (up to 8,000 characters by default)
- Supports various file types: `.md`, `.txt`, `.py`, `.js`, `.ts`, JSON, YAML, TOML, etc.

### 2. **Specific Portion Reading**
Yes, I can read specific portions of files using several methods:

**Line ranges:**
- Read lines 1-50: `read_document(path, start_line=1, end_line=50)`
- Read lines 100-150: `read_document(path, start_line=100, end_line=150)`

**First N lines:**
- First 50 lines: `read_document(path, head=50)`

**Last N lines:**
- Last 50 lines: `read_document(path, tail=50)`

**Custom character limits:**
- Up to 20,000 characters: `read_document(path, max_chars=20000)`

### 3. **Structural Analysis**
- Can get document summaries showing:
  - Heading hierarchy (for Markdown)
  - Functions and classes defined (for Python/JS/TS)
  - Line/word counts and first few lines (for text files)

### 4. **Search Capabilities**
- Can search for specific text strings across files
- Can filter by file extension
- Can search case-sensitively or case-insensitively

### Important Limitations:
- Files larger than 20,000 characters may be truncated
- For very large files, it's best to request specific sections rather than reading the entire file
- The librarian respects `.librarianignore` exclusions and only accesses files within the allowed directory

Would you like me to demonstrate reading a specific file or search for something particular?
