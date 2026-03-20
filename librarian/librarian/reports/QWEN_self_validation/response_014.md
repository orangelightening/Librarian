# Response 14: 5 Practical Examples of Using the Librarian Tools

## Summary

The librarian tools enable powerful workflows ranging from simple document searches to complex code analysis and collaborative debugging. Here are 5 practical examples demonstrating different tool categories and use cases.

---

## Example 1: Deep Codebase Analysis with Write Access

**Scenario**: You want to understand exception handling patterns across your project and share findings with your team.

### Workflow

1. **Search for exception handling patterns:**
   ```
   "Find all instances where we catch Exception instead of specific exceptions"
   ```

2. **Librarian responds:**
   - Searches the codebase using `search_documents()`
   - Identifies files with overly broad exception catching
   - Provides file paths and line numbers
   - Suggests improvements

3. **Write analysis report:**
   ```
   "Write your findings to /librarian/exception-analysis.md"
   ```

4. **Librarian writes:**
   - Detailed report with file paths, line numbers, and recommendations
   - Cites each source file
   - Organizes by severity

5. **User reviews and approves:**
   - Reads `/librarian/exception-analysis.md`
   - Reviews findings and suggestions
   - May request clarifications or additional searches

6. **Iterate if needed:**
   ```
   "Update the analysis after I've reviewed it, add more specific examples"
   ```

### Tools Used
- `search_documents()` - Find files with specific patterns
- `write_document()` - Create analysis report
- `read_document()` - Review written report

[Source: USER_GUIDE.md]

---

## Example 2: Directory Synchronization and Bulk Import

**Scenario**: You have a new project directory and want to index all documentation at once.

### Workflow

1. **Sync entire directory:**
   ```
   "Sync the directory ~/project/docs to the library"
   ```

2. **Librarian responds:**
   - Lists discovered files (respects `.librarianignore`)
   - Shows summary: "Added: 45 documents, Ignored: 3 files"
   - Provides statistics

3. **Verify sync results:**
   ```
   "List all indexed documents"
   ```

4. **Check statistics:**
   ```
   "Get library statistics"
   ```

### Tools Used
- `sync_documents()` - Bulk import documents
- `list_indexed_documents()` - Verify what was indexed
- `get_library_stats()` - Get summary statistics

[Source: search_library]

---

## Example 3: Focused File Reading with Portion Selection

**Scenario**: You need to review a specific function in a large codebase without reading the entire file.

### Workflow

1. **Find the file:**
   ```
   "Where is the authentication function defined?"
   ```

2. **Librarian identifies file:**
   - Returns file path (e.g., `backend/auth.py`)

3. **Read specific portion:**
   ```
   "Read lines 100-150 of backend/auth.py"
   ```

   OR read last 20 lines:
   ```
   "Read the last 20 lines of backend/auth.py"
   ```

   OR read first 30 lines:
   ```
   "Read the first 30 lines of backend/auth.py"
   ```

4. **Get structural overview:**
   ```
   "Show me the structure of backend/auth.py"
   ```

### Tools Used
- `search_documents()` - Locate file containing query
- `read_document()` with `start_line`/`end_line` - Read specific lines
- `read_document()` with `tail` - Read end of file
- `read_document()` with `head` - Read beginning of file
- `document_summary()` - Get structural overview

[Source: read_document]

---

## Example 4: Document Status Check and Update

**Scenario**: You've modified documentation files and want to know if the librarian needs to re-index them.

### Workflow

1. **Check document status:**
   ```
   "Is /path/to/my-document.md up to date?"
   ```

2. **Librarian responds:**
   ```
   Status: outdated
   Reason: File has been modified
   Document ID: doc_12345
   ```

3. **Sync to update:**
   ```
   "Sync the directory ~/docs to update changes"
   ```

4. **Librarian responds:**
   ```
   Added: 0 documents
   Updated: 3 documents
   Unchanged: 47 documents
   ```

### Tools Used
- `get_document_status()` - Check if file needs re-indexing
- `sync_documents()` - Update changes

[Source: search_library]

---

## Example 5: Debugging and Command Execution

**Scenario**: You want to check server configuration or run a diagnostic command safely.

### Workflow

1. **Check server configuration:**
   ```
   "Show me the server configuration"
   ```

2. **Librarian responds:**
   - Shows allowed directories
   - Lists whitelisted commands
   - Displays supported document types

3. **Run safe command:**
   ```
   "List files in the backend directory"
   ```

   OR run another command:
   ```
   "Run git status in the allowed directory"
   ```

4. **Review results:**
   ```
   "Read the output of the command"
   ```

### Tools Used
- `server_info()` - View configuration
- `execute_command()` - Run whitelisted commands
- `read_document()` - Read command output

### Security Note
The librarian can only run whitelisted commands (like `ls`, `cat`, `grep`) and cannot execute dangerous commands (`rm`, `chmod`, `mv`, etc.).

[Source: ARCHITECTURE.md]

---

## Summary of Tool Categories

| Use Case | Primary Tools | Goal |
|----------|---------------|------|
| **Code Analysis** | `search_documents`, `write_document`, `read_document` | Find patterns, generate reports |
| **Bulk Import** | `sync_documents`, `list_indexed_documents` | Index entire directories |
| **Focused Reading** | `read_document` (line ranges), `document_summary` | Selective file access |
| **Document Management** | `get_document_status`, `sync_documents` | Keep index current |
| **System Operations** | `server_info`, `execute_command` | Configure and diagnose |

---

**Primary Sources:**
- `/home/peter/development/librarian-mcp/USER_GUIDE.md`
- `/home/peter/development/librarian-mcp/ARCHITECTURE.md`
- `/home/peter/development/librarian-mcp/README.md`