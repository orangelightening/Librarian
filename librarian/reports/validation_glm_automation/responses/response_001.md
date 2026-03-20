# Query 1: Basic System Overview

**Status**: success
**Tokens Used**: 6257
**Timestamp**: 2026-03-19T15:01:49.663628
**Tool Calls**: 4

---

Based on the documentation, here's what the **Librarian MCP System** is and what it can do:

## What Is It?

The **Librarian MCP Server** is a production-ready Model Context Protocol (MCP) server that transforms AI models into intelligent research assistants and coding partners. It enables semantic document search with secure file system access and two-way communication through a dedicated workspace `[Source: ARCHITECTURE.md]`.

**Status**: Phase 2 Complete with 14 production tools `[Source: README.md]`

---

## Core Capabilities

### 🔍 **Semantic Search & Discovery**
- **Search documents semantically** (not just text matching) across your entire library
- **Always provides citations** - every answer references source documents
- **AI aggregation** - combines information from multiple sources into coherent answers
- Supports semantic search, literal text search, and file listing `[Source: ARCHITECTURE.md]`, `[Source: README.md]`

### 📚 **Document Management**
- **Add/remove documents** individually or in bulk via directory sync
- **Track changes** using SHA-256 checksums
- **Check document status** to see if files are indexed, modified, or missing
- **Get library statistics** including document counts and backend info `[Source: README.md]`

### 📄 **Secure File System Access**
- **Read files** with precise controls (line ranges, head, tail, character limits)
- **Write documents** to a dedicated `/librarian/` workspace for persistent analysis
- **List and search files** recursively through directories
- All access respects `.librarianignore` exclusion patterns (94+ built-in) `[Source: ARCHITECTURE.md]`, `[Source: README.md]`

### ✍️ **Two-Way Communication (NEW!)**
- **Write analysis results** to `/librarian/` workspace
- Create persistent reports instead of chat overflow
- Version tracking (v1, v2, v3) for iterative refinement
- You review before applying - maintains control `[Source: README.md]`

### 🔒 **Safe Command Execution**
- **Execute whitelisted commands** only
- Directory sandboxing prevents escaping safe directories
- Output truncation protects LLM context window `[Source: README.md]`

---

## Unique Features

### **Dual Backend Architecture**
- **Chonkie Backend** (default): Intelligent semantic chunking with context-aware boundaries
- **ChromaDB Backend** (optional): Fast sentence-based chunking
- Switch instantly via environment variable `[Source: README.md]`

### **Security First**
- 94+ built-in exclusion patterns via `.librarianignore`
- Command whitelisting
- SHA-256 change detection
- Safe workspace for writes only `[Source: README.md]`

### **Use Cases**
- 🐛 **Debugging**: Trace failures and find root causes
- 📋 **Code reviews**: Find patterns like generic exception catches
- 📚 **Documentation validation**: Compare docs against actual implementation
- 🔍 **Investigation**: Trace configuration across all files
- ✅ **Validation**: Run systematic checks `[Source: README.md]`

---

## System Design

The librarian is governed by a comprehensive system prompt (`prompt.md`) that defines:
- Behavioral principles (accuracy, citations, helpfulness)
- Security boundaries
- Tool usage guidelines
- Response format requirements `[Source: ARCHITECTURE.md]`

This ensures consistent, well-cited, and helpful responses across all interactions.

---

**In summary**: The librarian-mcp system is a complete research and code investigation platform that combines semantic search, secure file access, and two-way communication to help you understand, validate, and improve your codebase. It works with Jan, LM Studio, Claude Desktop, and any MCP-compatible client `[Source: README.md]`.

Would you like me to elaborate on any specific capability or show you how to use a particular tool?
