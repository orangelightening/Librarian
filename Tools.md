
Here is the complete list of available **Librarian MCP tools** that you can use to modify, read, or manage your `librarian-mcp` files:

---

### 📚 **Library Management Tools** (Manage the indexed documents)

| Tool | Parameters | Purpose |
|------|------------|---------|
| `search_library(query, limit)` | `query`: Search text<br>`limit`: Max results (default: 5) | Semantic search across indexed docs |
| `sync_documents(path, extensions, recursive)` | `path`: Directory to sync<br>`extensions`: Comma-separated (e.g., `.md,.py`)<br>`recursive`: Boolean (default: True) | Sync entire directories into library |
| `add_document(path)` | `path`: Path to file | Add a single file to library |
| `remove_document(document_id)` | `document_id`: String ID | Remove a document from library |
| `list_indexed_documents()` | (none) | List all indexed documents |
| `get_document_status(path)` | `path`: Path to file | Check if document is indexed/up-to-date |
| `get_library_stats()` | (none) | Get library statistics |

---

### 🔍 **File System & Document Tools** (Read/write files on disk)

| Tool | Parameters | Purpose |
|------|------------|---------|
| `read_document(path, start_line, end_line, head, tail, max_chars)` | `path`: File path<br>`start_line`, `end_line`: Line range<br>`head`: First N lines<br>`tail`: Last N lines<br>`max_chars`: Max chars (default: 8000) | Read specific portions of files |
| `write_document(path, content, create_dirs)` | `path`: File path relative to `/librarian/`<br>`content`: File content to write<br>`create_dirs`: Create parent dirs (default: True) | **Write files to librarian workspace** (two-way communication). Enables persistent analysis, code reviews, refactoring plans. Max 100KB per file. **⚠️ Context: Large writes still consume LLM context during generation. Break big tasks into chunks for best performance.** |
| `search_documents(query, path, extension, case_sensitive)` | `query`: Text to search<br>`path`: Subdirectory<br>`extension`: File type filter<br>`case_sensitive`: Boolean | Literal text search across files |
| `document_summary(path)` | `path`: File path | Get structural summary (headings/functions) |
| `list_documents(path, extension, recursive)` | `path`: Subdirectory<br>`extension`: File filter<br>`recursive`: Boolean | List files in directory |

---

### ⚙️ **System & Execution Tools** (Run commands on your system)

| Tool | Parameters | Purpose |
|------|------------|---------|
| `execute_command(command, args, cwd)` | `command`: Binary name (e.g., `cat`, `grep`)<br>`args`: List of arguments<br>`cwd`: Optional subdirectory | Run whitelisted shell commands |
| `server_info()` | (none) | Get server config, allowed commands, and supported types |

---

### 📝 **Whitelisted Commands** (Safe to execute directly)
These commands can be run via `execute_command`:

```bash
awk, cat, cd, cut, date, diff, echo, file, find, grep, head, hostname, ls, mkdir, pwd, sort, stat, tail, test, tree, uniq, wc, whoami
```

---

### ✅ **Your Current Context**
- **Allowed Directory**: `/home/peter/development/librarian-mcp`
- **Write Workspace**: `/home/peter/development/librarian-mcp/librarian/` (librarian-only write access)
- **Supported Extensions**: `.html`, `.js`, `.json`, `.md`, `.py`, `.rst`, `.toml`, `.ts`, `.txt`, `.yaml`, `.yml`
- **Max Output Size**: 8000 characters per read. See parameters  in a previous section.
- **Max Write Size**: 100,000 bytes (100KB) per write operation

---

## ✍️ **Write Access Guide**

### What is Write Access?

The `write_document` tool enables the librarian to create persistent files in the `/librarian/` workspace. This creates a **two-way communication channel** where the librarian can deliver analysis results, code changes, and documentation updates that you can review and apply.

### Security & Safety

**7 Layers of Protection**:
- ✅ Writes ONLY allowed in `/librarian/` subdirectory
- ✅ Maximum 100KB per file
- ✅ Critical filename blocking (password, secret, key, credential, .env, config)
- ✅ Directory traversal protection
- ✅ Audit logging (all writes logged to console)
- ✅ Safe directory boundary enforcement
- ✅ Manual review required (you control what gets applied)

### Usage Examples

**Example 1: Code Review**
```
You: "Review all exception handling in backend/, write analysis to /librarian/backend-exceptions.md"
Librarian: [Writes comprehensive report with file paths, line numbers, and recommendations]
You: [Reads /librarian/backend-exceptions.md to review findings]
You: [Applies approved code changes]
```

**Example 2: Refactoring Plan**
```
You: "Create a refactoring plan for document_manager.py, write to /librarian/refactor-plan.md"
Librarian: [Writes detailed plan with code examples and step-by-step instructions]
You: [Reviews plan, implements changes]
You: "Update the plan after my implementation"
Librarian: [Writes /librarian/refactor-plan-v2.md with verification]
```

**Example 3: Security Audit**
```
You: "Perform security audit of execute_command tool, write results to /librarian/security-audit.md"
Librarian: [Writes detailed security analysis with findings and recommendations]
You: [Reviews audit, addresses security issues]
```

### Context Window Management

**⚠️ Important**: Write operations create persistent files, but **large responses still consume LLM context during generation**.

**What happens**:
```
Task: "Analyze entire backend/ directory"
├── Librarian generates: 25,000 characters of analysis
├── Chat output shows: 8,000 characters (truncated with warning)
├── File write succeeds: 25,000 characters written to disk
└── Context used: 25,000 characters (full generation cost)
```

**Best Practices for Optimal Performance**:

1. **Break large tasks into chunks**:
   ```
   "Analyze backend/chroma_backend.py only, write to /librarian/chroma-analysis.md"
   "Now analyze backend/chonkie_backend.py, write to /librarian/chonkie-analysis.md"
   ```

2. **Request summary in chat, full details to file**:
   ```
   "Give me a brief summary in chat, but write the complete detailed analysis to /librarian/full-analysis.md"
   ```

3. **Use iterative refinement**:
   ```
   "List the files you'll analyze"
   "OK, analyze first 3 files, write to /librarian/analysis-part1.md"
   "Now analyze next 3 files, write to /librarian/analysis-part2.md"
   ```

**When to use write access**:
- ✅ Code reviews and refactoring plans (multi-file analysis)
- ✅ Security audit results
- ✅ Documentation updates
- ✅ Debugging diagnostics
- ✅ Task delegation outputs

**When to keep it brief**:
- ❌ Simple queries ("What does this function do?")
- ❌ Quick lookups ("Find the backend configuration")
- ❌ Status checks ("How many documents are indexed?")

### File Organization

```
/home/peter/development/librarian-mcp/librarian/
├── analyses/              # Analysis results
│   ├── backend-review.md
│   └── core-review.md
├── plans/                 # Refactoring plans
│   ├── refactor-plan-v1.md
│   └── refactor-plan-v2.md
├── security/              # Security audits
│   └── security-audit.md
└── reports/               # General reports
    ├── exception-analysis.md
    └── performance-analysis.md
```

**Tip**: Use subdirectories to organize related files. The librarian will create them automatically when `create_dirs=True` (default).



