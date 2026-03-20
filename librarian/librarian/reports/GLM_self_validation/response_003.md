# Response 003: How many tools does the librarian have and what are they?

## Tool Count Summary

The Librarian MCP Server has **14 production tools** organized into three categories:

- **7 Library Tools** - For searching and managing the document library
- **5 File System Tools** - For reading and analyzing files securely
- **2 System Tools** - For executing commands and getting server information [Source: README.md, ARCHITECTURE.md]

---

## Library Tools (7 Tools)

These tools focus on semantic search and document management within the library.

### 1. `search_library`

**Purpose**: Semantically search across all indexed documents in the library [Source: library_tools.py]

**Parameters**:
- `query` (string, required): The search query text
- `limit` (integer, default: 5): Maximum number of results to return

**Returns**: Aggregated search results with citations

**Description**: Performs semantic search across the vector store and returns the most relevant chunks from the document library with proper citations.

---

### 2. `sync_documents`

**Purpose**: Sync entire directories into the library - adds new documents, updates changed ones, removes deleted ones [Source: library_tools.py]

**Parameters**:
- `path` (string, required): Directory path to sync
- `extensions` (string, optional): Comma-separated list of extensions (e.g., '.md,.txt,.py')
- `recursive` (boolean, default: True): Whether to scan subdirectories

**Returns**: Summary of sync operation

**Description**: Synchronizes a directory with the library, handling additions, updates, and deletions automatically. Respects `.librarianignore` exclusion patterns.

---

### 3. `add_document`

**Purpose**: Add a single document to the library [Source: library_tools.py]

**Parameters**:
- `path` (string, required): Path to the document file

**Returns**: Result of the add operation

**Description**: Ingests a single document into the library, chunking it and storing it in the vector store for semantic search.

---

### 4. `remove_document`

**Purpose**: Remove a document and all its chunks from the library [Source: library_tools.py]

**Parameters**:
- `document_id` (string, required): ID of the document to remove

**Returns**: Result of the remove operation

**Description**: Completely removes a document and all associated chunks from the vector store, cleaning up both embeddings and metadata.

---

### 5. `list_indexed_documents`

**Purpose**: List all documents currently indexed in the library [Source: library_tools.py]

**Parameters**: None

**Returns**: List of indexed documents with metadata

**Description**: Returns a comprehensive list of all documents currently in the library, including document IDs, names, and metadata.

---

### 6. `get_document_status`

**Purpose**: Check if a document is indexed and up-to-date [Source: library_tools.py]

**Parameters**:
- `path` (string, required): Path to the document

**Returns**: Document status information

**Description**: Checks whether a document is in the library and whether its indexed version matches the current file (using SHA-256 checksums).

---

### 7. `get_library_stats`

**Purpose**: Get statistics about the library [Source: library_tools.py]

**Parameters**: None

**Returns**: Library statistics

**Description**: Returns comprehensive statistics including document count, total chunks, backend type, and other metrics about the library state.

---

## File System Tools (5 Tools)

These tools provide targeted access to specific files when needed, working within secure boundaries and respecting the `.librarianignore` file.

### 8. `read_document`

**Purpose**: Read contents of a document inside the allowed directory [Source: cli_tools.py]

**Parameters**:
- `path` (string, required): Absolute or relative path to the document
- `start_line` (integer, optional): Starting line number (1-based, inclusive)
- `end_line` (integer, optional): Ending line number (1-based, inclusive)
- `head` (integer, optional): Read first N lines
- `tail` (integer, optional): Read last N lines
- `max_chars` (integer, default: 8000): Maximum characters to return

**Returns**: Document contents or error message

**Description**: Supports reading entire file or specific portions with line ranges, first/last N lines, or custom max size.

**Examples**:
- Read entire file: `read_document("/path/to/file.txt")`
- Read first 50 lines: `read_document("/path/to/file.txt", head=50)`
- Read lines 100-150: `read_document("/path/to/file.txt", start_line=100, end_line=150)`

---

### 9. `list_documents`

**Purpose**: List documents in the allowed directory [Source: cli_tools.py]

**Parameters**:
- `path` (string, optional): Subdirectory to list (default: root)
- `extension` (string, optional): Filter by extension e.g., '.md', '.py'
- `recursive` (boolean, default: True): Whether to recurse into subdirectories

**Returns**: List of document paths with sizes

**Description**: Lists all supported documents in a directory, with optional filtering by extension and recursion control.

---

### 10. `search_documents`

**Purpose**: Search for a text string across documents in the allowed directory [Source: cli_tools.py]

**Parameters**:
- `query` (string, required): Text string to search for
- `path` (string, optional): Subdirectory to search (default: root)
- `extension` (string, optional): Limit search to file type e.g., '.md'
- `case_sensitive` (boolean, default: False): Whether search is case sensitive

**Returns**: Matching files and lines with line numbers

**Description**: Performs literal text search (grep-like) across files, returning matching file paths and the specific lines containing the match with line numbers.

---

### 11. `document_summary`

**Purpose**: Get a structural summary of a document without reading full contents [Source: cli_tools.py]

**Parameters**:
- `path` (string, required): Path to the document

**Returns**: Structural summary with line numbers

**Description**: Provides different types of summaries based on document type:
- **Markdown**: Shows heading hierarchy
- **Python/JS/TS**: Shows functions and classes defined
- **Text/other**: Shows line/word count and first few lines

---

### 12. `write_document`

**Purpose**: Write content to a file in the librarian workspace subdirectory [Source: cli_tools.py]

**Parameters**:
- `path` (string, required): File path relative to `/librarian/` subdirectory
- `content` (string, required): File content to write
- `create_dirs` (boolean, default: True): Create parent directories if they don't exist

**Returns**: Success confirmation with file path and size

**Description**: Creates a two-way communication channel where the librarian can write files (analysis results, code changes, documentation updates) that the user can review and apply. Only writes to the safe `/librarian/` subdirectory.

---

## System Tools (2 Tools)

These tools provide system-level capabilities for command execution and server information.

### 13. `execute_command`

**Purpose**: Execute a whitelisted command safely inside the allowed directory [Source: cli_tools.py]

**Parameters**:
- `command` (string, required): The binary to execute (e.g., 'ls', 'cat', 'grep')
- `args` (array of strings, default: []): List of arguments to pass to the command
- `cwd` (string, optional): Optional subdirectory to run in (must be inside allowed directory)

**Returns**: stdout, stderr, return code

**Description**: Safely executes whitelisted commands with proper security controls:
- Only approved binaries can execute
- Cannot escape the allowed directory
- Output is truncated to protect LLM context window

---

### 14. `server_info`

**Purpose**: Return server configuration, allowed commands, and supported document types [Source: cli_tools.py]

**Parameters**: None

**Returns**: Server information including configuration and capabilities

**Description**: Provides information about the server state, including which tools are available, what commands are whitelisted, and what document types are supported.

---

## Tool Categories Summary

| Category | Count | Purpose |
|----------|-------|---------|
| **Library Tools** | 7 | Semantic search and document management |
| **File System Tools** | 5 | Secure file access and analysis |
| **System Tools** | 2 | Command execution and server info |
| **Total** | **14** | Complete research and code investigation platform |

---

## Key Design Principles

All tools are designed to:

1. **Work within secure boundaries** - Respect the `.librarianignore` file and only access files within the allowed directory scope
2. **Provide proper error handling** - Return clear error messages when operations fail
3. **Support citations** - Library tools return results with source citations
4. **Enable two-way communication** - Write tool allows persistent task delegation
5. **Protect the LLM context** - Output truncation prevents context window overflow [Source: cli_tools.py, library_tools.py]

---

## Tool Interaction Example

A typical workflow might use multiple tools:

1. `search_library` - Find relevant documents semantically
2. `read_document` - Read specific sections of interest
3. `search_documents` - Find literal text matches across files
4. `document_summary` - Get structure without full content
5. `write_document` - Write analysis results for review
6. `execute_command` - Run safe commands as needed

This comprehensive toolkit enables the Librarian to act as a full research assistant and code investigation partner, not just a search engine [Source: README.md].
