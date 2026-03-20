# Query 11: What file reading capabilities does the librarian have and can you read specific portions of files?

The Librarian provides **targeted, secure file reading capabilities** designed for precise access rather than blind full-file reads.

## Primary Reading Tool: `read_document()`

The `read_document()` tool supports reading entire files or specific portions with multiple access patterns.

### Reading Options

The tool supports reading files in several ways:

1. **Line Ranges** - Read specific line ranges
   - `start_line=1, end_line=10` - Read lines 1 through 10
   - Line numbers are 1-based and inclusive
   - Can specify just start_line (defaults to end) or just end_line (defaults to 1)

2. **First N Lines** - Read from the beginning
   - `head=20` - Read the first 20 lines
   - Overrides start_line/end_line if specified

3. **Last N Lines** - Read from the end
   - `tail=20` - Read the last 20 lines
   - Overrides start_line/end_line if specified

4. **Full File** - Read entire document
   - Subject to character limits (default: 8000 characters)

5. **Custom Max Size** - Limit character count
   - `max_chars=20000` - Limit to 20,000 characters
   - Default is 8,000 characters for full reads

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `path` | Absolute or relative path to the document | **Required** |
| `start_line` | Starting line number (1-based, inclusive) | None |
| `end_line` | Ending line number (1-based, inclusive) | None |
| `head` | Read first N lines (overrides start_line/end_line) | None |
| `tail` | Read last N lines (overrides start_line/end_line) | None |
| `max_chars` | Maximum characters to return | 8000 |

### Examples

```python
# Read entire file (up to 8000 chars)
read_document("/path/to/file.txt")

# Read first 50 lines
read_document("/path/to/file.txt", head=50)

# Read last 50 lines
read_document("/path/to/file.txt", tail=50)

# Read lines 100-150
read_document("/path/to/file.txt", start_line=100, end_line=150)

# Read up to 20000 characters
read_document("/path/to/file.txt", max_chars=20000)
```

## Other Related File Tools

The librarian provides additional file-related capabilities:

### `document_summary(path)`
- Get a structural summary without reading full contents
- **Markdown**: Shows heading hierarchy
- **Python/JS/TS**: Shows functions and classes defined
- **Text/other**: Shows line/word count and first few lines

### `list_documents(path, extension, recursive)`
- Browse and discover files in the allowed directory
- Filter by extension (e.g., `.md`, `.py`)
- Recursive search through subdirectories
- Returns file paths with sizes

### `search_documents(query, path, extension, case_sensitive)`
- Search for literal text strings within files
- Returns matching file paths and line numbers
- Case-insensitive by default
- Can filter by file type

## Use Cases

These capabilities enable several workflows:

1. **Targeted Investigation** - Read specific sections of large files
2. **Quick Preview** - Use `head` or `tail` to see file structure
3. **Incremental Reading** - Read files in chunks using line ranges
4. **Size Management** - Use `max_chars` to handle large files
5. **Exploration** - Use `document_summary` for overviews before deep reading
6. **Discovery** - Use `list_documents` and `search_documents` to find relevant files

## Security Considerations

- Only accesses files within the allowed directory scope
- Respects `.librarianignore` file exclusions
- Prevents unauthorized access to sensitive files (credentials, keys, .env files)
- Designed for controlled, intentional reading rather than bulk data extraction
