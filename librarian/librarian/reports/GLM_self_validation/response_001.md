# Response 001: What is the librarian-mcp system and what can it do?

## What is the Librarian MCP System?

The **Librarian MCP Server** is a production-ready Model Context Protocol (MCP) server that transforms AI models into intelligent research assistants and coding partners. It enables AI models to act as intelligent librarians with semantic document search capabilities [Source: ARCHITECTURE.md].

### Core Architecture

The system combines three main components:

1. **Document Management** - Powerful tools for managing a curated document library
2. **Secure File System Access** - Tools for reading and analyzing files safely
3. **Two-Way Communication** - Write access to a dedicated `/librarian/` workspace for persistent task delegation and iterative refinement [Source: ARCHITECTURE.md]

The librarian is governed by a comprehensive system prompt (`prompt.md`) that defines:
- Behavioral principles (accuracy, citations, helpfulness)
- Security boundaries
- Tool usage guidelines
- Response format requirements [Source: ARCHITECTURE.md]

This ensures consistent, well-cited, and helpful responses across all interactions.

### Current Status

- **Phase**: Phase 2 Complete ✅
- **Backend**: Chonkie (intelligent chunking) - default backend
- **Tools**: 14 Production MCP Tools [Source: README.md]

---

## What Can It Do?

### Primary Functions

The Librarian MCP Server enables AI models to:

1. **Search and Discover** - Find relevant information in the library using semantic search
2. **Synthesize** - Combine information from multiple sources into coherent answers
3. **Cite Sources** - Always reference which documents provided information
4. **Navigate** - Help users explore the file system securely
5. **Manage** - Assist with document ingestion and library maintenance [Source: prompt.md]

### Beyond Simple Search

The Librarian is more than just a search engine - it's an **active development assistant** [Source: README.md]:

#### **Debugging Assistant**
- Traces code flow across multiple files
- Identifies root causes of issues
- Analyzes patterns and problems systematically
- Writes detailed analysis reports

#### **Documentation Validator**
- Validates documentation against actual implementation
- Finds discrepancies between docs and code
- Identifies outdated or inaccurate documentation
- Suggests documentation improvements

#### **Code Investigator**
- Investigates code across the entire codebase
- Traces configuration and dependencies
- Finds implementation patterns
- Provides systematic code analysis [Source: README.md]

### Two-Way Communication (Unique Feature)

Unlike most MCP servers that are read-only, the Librarian provides **two-way communication** via write access to a dedicated workspace:

- **Write analysis results** - Can write reports and findings to `/librarian/` workspace
- **Write code changes** - Can generate fixes and improvements
- **Write documentation updates** - Can update or create documentation
- **Persistent analysis** - No more copying/pasting long chat responses
- **Version tracking** - Can create v1, v2, v3 files for iterative analysis
- **User control** - You review librarian's written output before applying changes [Source: README.md, ARCHITECTURE.md]

### Practical Use Cases

The Librarian can be used for:

- **🐛 Debugging**: "Trace why document sync is failing" → Gets root cause with code paths
- **📋 Code Reviews**: "Find all generic Exception catches" → Writes analysis report
- **📚 Documentation**: "Validate README matches implementation" → Finds discrepancies
- **🔍 Investigation**: "Where is timeout configuration set?" → Traces across all files
- **✅ Validation**: Run systematic validation queries to self-check documentation accuracy [Source: README.md]

---

## Key Capabilities Summary

| Capability | Description |
|-----------|-------------|
| **Semantic Search** | Finds relevant information across the library, not just text matching |
| **Document Management** | Add, update, remove, and sync documents into the library |
| **Secure File Access** | Read files with line ranges, head, tail - respects `.librarianignore` |
| **Safe Command Execution** | Whitelisted binaries only, directory sandboxed |
| **Write Workspace** | Write analysis reports, code changes, documentation updates |
| **Citations** | Always cites sources for every answer |
| **SHA-256 Tracking** | Automatically detects document changes |
| **94+ Exclusion Patterns** | Built-in security via `.librarianignore` |

---

## System Design Principles

The librarian operates under core principles:

1. **Accuracy and Citations** - Always cite sources when providing information from the library
2. **Tool Usage First** - Always use tools rather than guessing or making assumptions
3. **Helpful and Thorough** - Provide comprehensive answers based on available library content
4. **Secure and Respectful** - Only access files within allowed scope, respect exclusions
5. **Transparent About Limitations** - Acknowledge when information is not available [Source: prompt.md]

---

**In summary**: The librarian-mcp system is a complete research and code investigation platform that combines semantic search with two-way communication, intelligent chunking, and automatic change detection - features that most standard MCP servers don't provide [Source: quick-start.md].
