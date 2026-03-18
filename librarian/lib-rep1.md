# Librarian Capabilities Report

**Generated:** Current Session  
**Purpose:** Comprehensive overview of librarian tool capabilities and functionality

---

## Executive Summary

The Librarian is an intelligent research assistant with access to a curated document library and secure file system tools. It combines semantic search, document management, file system exploration, and two-way communication capabilities to help users discover, synthesize, and analyze information efficiently.

---

## Core Capabilities

### 1. Library Search & Discovery

#### Semantic Search
- **Tool:** `search_library(query, limit)`
- **Functionality:** Performs semantic search across all indexed documents using vector embeddings
- **Features:**
  - Returns aggregated results with citations
  - Configurable result limits (default: 5)
  - Understands context and meaning beyond keyword matching

#### Document Status & Management
- **Tools:**
  - `list_indexed_documents()` - View all indexed documents with metadata
  - `get_document_status(path)` - Check if document is indexed and up-to-date
  - `get_library_stats()` - Get statistics (document count, chunk count, etc.)

### 2. Document Synchronization & Ingestion

#### Directory Syncing
- **Tool:** `sync_documents(path, extensions, recursive)`
- **Functionality:** Sync entire directories into the library
- **Features:**
  - Adds new documents automatically
  - Updates changed documents via SHA-256 checksums
  - Removes deleted documents
  - Supports file extension filtering
  - Recursive subdirectory scanning (default: enabled)

#### Individual Document Operations
- **Tool:** `add_document(path)` - Add single document to library
- **Tool:** `remove_document(document_id)` - Remove document and all chunks by ID

### 3. File System Exploration & Reading

#### Directory Listing
- **Tool:** `list_documents(path, extension, recursive)`
- **Functionality:** List documents in specified directory
- **Features:**
  - Path filtering (default: root of allowed directory)
  - Extension filtering (e.g., `.md`, `.py`)
  - Recursive subdirectory scanning

#### Document Reading with Flexibility
- **Tool:** `read_document(path, start_line, end_line, head, tail, max_chars)`
- **Features:**
  - Read entire file (up to 8000 chars default)
  - Line range selection (1-based indexing)
  - First N lines (`head` parameter)
  - Last N lines (`tail` parameter)
  - Custom maximum character limits

#### Document Summaries
- **Tool:** `document_summary(path)`
- **Functionality:** Get structural overview without reading full content
- **Features:**
  - Markdown: Shows heading hierarchy
  - Python/JS/TS: Shows functions and classes defined
  - Text/other: Shows line/word count and first few lines

### 4. File Writing & Two-Way Communication

#### Write Access to Librarian Workspace
- **Tool:** `write_document(path, content, create_dirs)`
- **Functionality:** Write files to `/librarian/` subdirectory
- **Key Features:**
  - Creates parent directories automatically (default: enabled)
  - Enables two-way communication channel
  - Allows writing analysis results, code changes, documentation updates
  - User can review written output before applying changes
  - Security boundaries: Writes only allowed in `/librarian/` subdirectory
  - Version tracking support (v1, v2, v3 files for updated analysis)

### 5. Command Execution & System Interaction

- **Tool:** `execute_command(command, args, cwd)`
- **Functionality:** Execute whitelisted commands safely inside allowed directory
- **Features:**
  - Returns stdout, stderr, and return code
  - Optional working directory specification (must be inside allowed directory)
  - Security sandboxing with timeout protection (15 second default)

### 6. Tool Discovery & Configuration

#### Available Tools Listing
- **Tool:** `list_available_tools()`
- **Functionality:** List all available MCP tools and their parameters
- **Returns:** Complete list of tools with descriptions and parameter details

#### Server Information
- **Tool:** `server_info()`
- **Functionality:** Returns server configuration, allowed commands, and supported document types
- **Use Case:** Quick reference for capabilities and constraints

---

## Core Principles & Behavioral Guidelines

### Accuracy & Citations
- **Always cite sources** when providing information from the library
- Use format: `[Source: document_name.md]`
- Distinguish between library content and general knowledge
- Multiple sources cited individually for clarity

### Helpful & Thorough
- Provide comprehensive answers based on available library content
- Clearly state when library lacks relevant information
- Suggest follow-up searches or related topics
- Offer to search file system if library content is insufficient

### Secure & Respectful
- Only access files within allowed scope
- Respect `.librarianignore` exclusions (excluded content off-limits)
- Never attempt to bypass security restrictions
- Protect sensitive information (credentials, private keys, etc.)

### Transparent About Limitations
- Acknowledge when information is not found
- Explain difference between "no results" and "no good matches"
- If search seems incomplete, suggest refining queries

---

## Security Model & Boundaries

### Security Layers
1. **Directory Sandboxing** - Safe directory restrictions
2. **Output Truncation** - Protects LLM context
3. **Timeout Protection** - 15 second default timeout
4. **SHA-256 Checksums** - Change detection for documents
5. **File Size Limits** - Prevents excessive data processing
6. **`.librarianignore` Respecting** - Excluded content never accessed
7. **Backend Security** - Both backends respect security equally

### Access Restrictions
- ❌ Never access files outside allowed directory
- ❌ Ignore `.librarianignore` exclusions (they're off-limits)
- ❌ Execute commands beyond whitelist
- ❌ Fabricate citations or sources
- ❌ Claim information is in library when it's not
- ❌ Bypass safety restrictions or security measures
- ❌ Access sensitive files (.env, credentials, keys)

---

## Common Use Cases & Patterns

### 1. Code Review Assistant
- Analyze code for bugs and refactoring opportunities
- Find inconsistencies between documentation and implementation
- Validate accuracy across multiple sources

### 2. Validation with Self-Reflection
- Test configurations and query results
- Critique findings for accuracy and completeness

### 3. Tracing & Investigation
- Follow data flows across the codebase
- Understand architecture and implementation details
- Debug complex issues by tracing execution paths

### 4. Gap Analysis
- Find missing information in documentation
- Assess documentation planning and completeness
- Identify areas needing improvement

### 5. Comparative Analysis
- Compare multiple documents for contradictions
- Ensure consistency across documentation files
- Determine authoritative sources for topics

---

## Supported Document Types

The library commonly indexes:
- **Markdown** (`.md`) - Documentation, guides, reports
- **Text** (`.txt`) - Plain text files
- **Code Files:**
  - Python (`.py`)
  - JavaScript/TypeScript (`.js`, `.ts`)
- **Configuration:**
  - JSON (`.json`)
  - YAML (`.yaml`, `.yml`)
  - TOML (`.toml`)

---

## Getting Started Workflow

1. **Check Library Stats** → `get_library_stats()`
   - Understand current library scope and size

2. **List Indexed Documents** → `list_indexed_documents()`
   - Review what's currently available in the library

3. **Search for Information** → `search_library(query)`
   - Use semantic search to find relevant content

4. **Read Full Context** → `read_document(path)`
   - Get complete information when needed

5. **Write Analysis Results** → `write_document(path, content)`
   - Create reports and documentation in `/librarian/` workspace

---

## Tool Summary by Category

### Library Tools (7)
| Tool | Purpose |
|------|---------|
| `search_library(query, limit)` | Semantic search over indexed documents |
| `sync_documents(path, extensions, recursive)` | Sync directory to library |
| `add_document(path)` | Add single document |
| `remove_document(document_id)` | Remove from library |
| `list_indexed_documents()` | List all indexed documents |
| `get_document_status(path)` | Check document status |
| `get_library_stats()` | Get statistics |

### CLI Tools (6)
| Tool | Purpose |
|------|---------|
| `execute_command(command, args, cwd)` | Execute whitelisted commands |
| `read_document(path, [ranges])` | Read files with flexible ranges |
| `list_documents(path, extension, recursive)` | List directory contents |
| `search_documents(query, path, extension)` | Text search in files |
| `document_summary(path)` | Get structural overview |
| `write_document(path, content, create_dirs)` | Write to `/librarian/` workspace |

### Utility Tools (2)
| Tool | Purpose |
|------|---------|
| `list_available_tools()` | List all tools with parameters |
| `server_info()` | Get server configuration and capabilities |

---

## Conclusion

The Librarian provides a comprehensive suite of capabilities for document management, semantic search, file system exploration, and two-way communication. Its design emphasizes:

- **Accuracy** through citation discipline
- **Security** through multiple layers of protection
- **Transparency** about limitations and data availability
- **Productivity** through intelligent synthesis and organized workflows

The combination of library-based semantic understanding with direct file system access enables powerful research, analysis, and documentation tasks while maintaining strict security boundaries.

---

*Report generated based on library search results and documented capabilities.*
