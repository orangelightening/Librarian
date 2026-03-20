# Response to Query 1: What is the librarian-mcp system and what can it do?

## Overview

The **Librarian MCP Server** is a production-ready Model Context Protocol (MCP) server that enables AI models to act as intelligent librarians with semantic document search capabilities. It combines powerful document management with secure file system access and **two-way communication** via write access to a dedicated workspace [Source: ARCHITECTURE.md].

## Core Capabilities

### 1. Semantic Document Search
- `search_library(query, limit)` - Semantic search with AI aggregation across indexed documents
- Supports intelligent retrieval based on document content, not just file names
- Returns aggregated results with citations

### 2. Document Lifecycle Management
- `sync_documents(path, extensions, recursive)` - Sync entire directories into the library
- `add_document(path)` - Add a single file to the library
- `remove_document(document_id)` - Remove a document from the library by ID
- `list_indexed_documents()` - List all currently indexed documents with metadata
- `get_document_status(path)` - Check if a document is indexed and up-to-date
- `get_library_stats()` - Get library statistics and information

### 3. File System Operations
- `read_document(path, ...)` - Read files with line ranges, head, tail, or max character limits
- `write_document(path, content, ...)` - Write files to the `/librarian/` workspace (two-way communication channel)
- `search_documents(query, ...)` - Literal text search across files
- `document_summary(path)` - Get structural summary (headings, functions, classes)
- `list_documents(path, ...)` - List files in directories with optional filtering

### 4. System & Execution
- `execute_command(command, args, cwd)` - Execute whitelisted shell commands safely
- `server_info()` - Get server configuration, allowed commands, and supported types

## Key Differentiators

### Two-Way Communication via Write Access
Most MCP servers are read-only, but the Librarian provides **two-way communication** through write access to a dedicated workspace. This enables:
- Persistent analysis results and reports
- Code reviews with detailed recommendations
- Refactoring plans with step-by-step instructions
- Debugging diagnostics
- Task delegation outputs [Source: Tools.md]

### Intelligent Chunking
Uses **Chonkie** for intelligent semantic chunking, providing better search results through context-aware boundaries compared to simple sentence splitting or fixed-size chunks [Source: CHONKIE_INTEGRATION.md].

### Automatic Change Detection
Supports SHA-256 checksum-based change detection to ensure modified documents are re-indexed automatically [Source: ARCHITECTURE.md].

## Security Boundaries

- Writes ONLY allowed in the `/librarian/` subdirectory
- Maximum 100KB per file write
- Multiple layers of path validation
- Critical file protection (blocks passwords, secrets, keys, .env files)
- Audit logging for all write operations [Source: Tools.md]

## Summary

The Librarian MCP Server transforms AI models into intelligent research assistants and coding partners by combining semantic search, document management, secure file system access, and persistent two-way communication [Source: ARCHITECTURE.md].