# Response 11: File Reading Capabilities of the Librarian

## Summary

The librarian has **targeted, secure file reading capabilities** through the `read_document()` tool, which supports reading entire files or specific portions with fine-grained control over what content is retrieved.

## Primary Reading Tool: `read_document()`

The `read_document()` tool provides flexible file reading with multiple access patterns:

### 1. Full File Reading

Read the entire file (up to default 8000 characters):

```python
read_document("/path/to/file.txt")
```

**Limitations**:
- Default maximum: 8000 characters
- Can be increased with `max_chars` parameter (up to 20000)

[Source: read_document]

### 2. Line Range Reading

Read a specific range of lines (1-based indexing):

```python
# Lines 1-10
read_document("/path/to/file.txt", start_line=1, end_line=10)

# Lines 100-150
read_document("/path/to/file.txt", start_line=100, end_line=150)

# Lines 50 to end
read_document("/path/to/file.txt", start_line=50)
```

[Source: read_document]

### 3. First N Lines (Head)

Read the first N lines from the beginning:

```python
read_document("/path/to/file.txt", head=20)
# Equivalent to start_line=1, end_line=20
```

**Use cases**:
- Reading file headers
- Checking initial configuration
- Reviewing imports in Python files

[Source: read_document]

### 4. Last N Lines (Tail)

Read the last N lines from the end:

```python
read_document("/path/to/file.txt", tail=20)
# Equivalent to start_line=len-19, end_line=len
```

**Use cases**:
- Checking file endings
- Reviewing closing statements
- Inspecting exception handlers

[Source: read_document]

### 5. Custom Character Limit

Override the default character limit:

```python
read_document("/path/to/file.txt", max_chars=20000)
# Up to 20000 characters
```

[Source: read_document]

## File Summary: `document_summary()`

For quick structural analysis without reading full content:

```python
document_summary("/path/to/file.py")
# Returns:
# - Function/class definitions
# - Line numbers
# - File structure overview
```

**Supported file types**:
- **Markdown**: Shows heading hierarchy
- **Python/JS/TS**: Shows functions and classes defined
- **Text/other**: Shows line/word count and first few lines

[Source: document_summary]

## Security and Access Control

### Allowed Directories

File reading is restricted to the **whitelisted safe directory** (default: `/home/peter/development`). Attempting to read files outside this scope will be blocked.

### `.librarianignore` Compliance

The system respects the `.librarianignore` file, which excludes sensitive files:
- **Credentials**: `.env`, `.pem`, `.p12` files
- **Private keys**: `*.key`, `*.pem`, `id_rsa` files
- **Configuration**: System files, build artifacts

[Source: ARCHITECTURE.md]

## Practical Examples

### Example 1: Read a Python Function Definition

```python
read_document("/path/to/my_module.py", head=50)
# Shows first 50 lines including function definitions
```

### Example 2: Read Error Handling Section

```python
read_document("/path/to/my_module.py", start_line=200, end_line=250)
# Specific section for debugging
```

### Example 3: Read File Footer

```python
read_document("/path/to/config.yaml", tail=10)
# Last 10 lines, useful for checking array endings
```

### Example 4: Large File Analysis

```python
read_document("/path/to/large_log.txt", max_chars=20000)
# Read up to 20KB of log content
```

## Comparison with Other Tools

| Tool | Purpose | Granularity |
|------|---------|-------------|
| `read_document()` | Read file content | Lines, characters |
| `document_summary()` | Structural overview | Functions, classes |
| `search_documents()` | Text search | Line numbers |
| `list_documents()` | File listing | Paths, sizes |

## Limitations

1. **Character Limit**: Maximum 20000 characters per read operation
2. **Single File**: Can only read one file at a time
3. **No Binary Files**: Primarily designed for text files
4. **No Line Numbers in Output**: Line numbers are tracked but not embedded in content

## Summary

The librarian's file reading capabilities provide:
- **Flexible access**: Full file, line ranges, head, tail
- **Context control**: Specify exactly what portions to read
- **Security**: Restricted to allowed directories, respects ignore patterns
- **Efficiency**: Targeted reading rather than blind full-file reads
- **Integration**: Works seamlessly with search and analysis tools

This design balances powerful file access with security and performance considerations.

---
**Primary Source**: `/home/peter/development/librarian-mcp` (read_document tool documentation)
**Secondary Source**: `/home/peter/development/librarian-mcp/ARCHITECTURE.md`