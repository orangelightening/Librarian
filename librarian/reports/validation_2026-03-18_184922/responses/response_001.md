# Query 1: Basic System Overview

**Status**: success
**Tokens Used**: 473
**Timestamp**: 2026-03-18T19:21:41.486515
**Tool Calls**: 0

---

The **Librarian-MCP** system is an intelligent research assistant designed to help you search, synthesize, and manage information within a curated document library and secure file system environment.

## Core Capabilities

### 1. **Search and Discovery**
- Semantic search across indexed documents using vector embeddings
- Literal text search within files for specific terms
- Explore directory structures to find relevant content

### 2. **Information Synthesis**
- Combine information from multiple sources into coherent answers
- Provide comprehensive responses based on library content
- Always cite sources in the format `[Source: document_name.md]`

### 3. **Library Management**
- Add new documents individually or sync entire directories
- Update existing documents when they change
- Remove outdated documents from the library
- Monitor library statistics and indexed content

### 4. **Secure File System Access**
- Read file contents within allowed directory boundaries
- Execute whitelisted commands safely
- Respect `.librarianignore` exclusions for security

## How It Works

The system operates on these principles:

1. **Accuracy First**: Always cite sources and distinguish between library content and general knowledge
2. **Honesty Over Completeness**: If information isn't in the library, I'll say so clearly rather than fabricating answers
3. **Security Conscious**: Never access files outside allowed scope or bypass security restrictions
4. **Transparent Limitations**: Explain when data is insufficient and suggest alternatives

## Available Tools

**Library Operations:**
- `search_library()` - Semantic search across documents
- `sync_documents()` - Add/update entire directories
- `add_document()` - Add individual files
- `list_indexed_documents()` - See what's in the library
- `get_library_stats()` - Library statistics

**File System Operations:**
- `read_document()` - Read file contents
- `search_documents()` - Literal text search
- `list_documents()` - Explore directory structure
- `execute_command()` - Run whitelisted commands

## Getting Started

Would you like me to:
1. Show you what's currently in the library?
2. Demonstrate a sample search?
3. Help you add new documents to the library?
4. Explain how to use specific tools for your needs?