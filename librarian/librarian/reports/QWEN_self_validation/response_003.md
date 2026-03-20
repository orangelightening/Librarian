# Response to Query 3: How many tools does the librarian have and what are they?

## Summary

The Librarian MCP Server has **14 specialized MCP tools** organized into three categories:
- **7 Library Management Tools**
- **5 File System & Document Tools**
- **2 System & Execution Tools** [Source: Tools.md]

---

## 📚 Library Management Tools (7)

These tools manage indexed documents in the library:

| Tool | Parameters | Purpose |
|------|------------|---------|
| `search_library(query, limit)` | `query`: Search text<br>`limit`: Max results (default: 5) | Semantic search across indexed docs with AI aggregation |
| `sync_documents(path, extensions, recursive)` | `path`: Directory to sync<br>`extensions`: Comma-separated (e.g., `.md,.py`)<br>`recursive`: Boolean (default: True) | Sync entire directories into library |
| `add_document(path)` | `path`: Path to file | Add a single file to library |
| `remove_document(document_id)` | `document_id`: String ID | Remove a document from library |
| `list_indexed_documents()` | (none) | List all indexed documents with metadata |
| `get_document_status(path)` | `path`: Path to file | Check if document is indexed/up-to-date |
| `get_library_stats()` | (none) | Get library statistics and information |

---

## 🔍 File System & Document Tools (5)

These tools allow reading, writing, and exploring files on disk:

| Tool | Parameters | Purpose |
|------|------------|---------|
| `read_document(path, start_line, end_line, head, tail, max_chars)` | `path`: File path<br>`start_line`, `end_line`: Line range<br>`head`: First N lines<br>`tail`: Last N lines<br>`max_chars`: Max chars (default: 8000) | Read specific portions of files |
| `write_document(path, content, create_dirs)` | `path`: File path relative to `/librarian/`<br>`content`: File content to write<br>`create_dirs`: Create parent dirs (default: True) | **Write files to librarian workspace** (two-way communication). Max 100KB per file. |
| `search_documents(query, path, extension, case_sensitive)` | `query`: Text to search<br>`path`: Subdirectory<br>`extension`: File type filter<br>`case_sensitive`: Boolean | Literal text search across files |
| `document_summary(path)` | `path`: File path | Get structural summary (headings, functions, classes) |
| `list_documents(path, extension, recursive)` | `path`: Subdirectory<br>`extension`: File filter<br>`recursive`: Boolean | List files in directory |

---

## ⚙️ System & Execution Tools (2)

These tools run commands and get system information:

| Tool | Parameters | Purpose |
|------|------------|---------|
| `execute_command(command, args, cwd)` | `command`: Binary name (e.g., `cat`, `grep`)<br>`args`: List of arguments<br>`cwd`: Optional subdirectory | Run whitelisted shell commands safely |
| `server_info()` | (none) | Get server configuration, allowed commands, and supported types |

---

## Whitelisted Commands

The `execute_command` tool can safely run these commands:

```bash
awk, cat, cd, cut, date, diff, echo, file, find, grep, head, hostname, ls, mkdir, pwd, sort, stat, tail, test, tree, uniq, wc, whoami
```

---

## Write Access Workspace

The `write_document` tool creates files in the `/librarian/` subdirectory:
```
/home/peter/development/librarian-mcp/librarian/
```

**Security features:**
- Maximum 100KB per file
- Blocks critical filenames (password, secret, key, credential, .env)
- Audit logging for all writes
- Manual review required [Source: Tools.md]

---

## Summary

The Librarian provides **14 tools** across three categories, enabling semantic search, full document lifecycle management, secure file system operations, and two-way communication for persistent analysis and collaboration [Source: Tools.md].