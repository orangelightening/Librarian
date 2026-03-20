# Response 006: What governs the librarian's behavior and where is this defined?

## Overview

The Librarian's behavior is governed by a comprehensive system prompt defined in **two primary locations**:

1. **`prompt.md`** - Main system prompt file in the project root
2. **`mcp_server/config/librarian_prompt.py`** - Python module containing the `LIBRARIAN_SYSTEM_PROMPT` constant [Source: ARCHITECTURE.md, librarian_prompt.py]

Both files define the same behavioral guidelines, with the Python version being loaded and used by the server at runtime.

---

## Primary Definition: `prompt.md`

**Location**: `/home/peter/development/librarian-mcp/prompt.md`

**Purpose**: The main human-readable system prompt that defines the Librarian's persona, role, and behavioral principles [Source: prompt.md, ARCHITECTURE.md]

---

## Runtime Definition: `librarian_prompt.py`

**Location**: `mcp_server/config/librarian_prompt.py`

**Purpose**: Python module containing the `LIBRARIAN_SYSTEM_PROMPT` constant that is loaded and used by the MCP server at runtime [Source: librarian_prompt.py]

**Implementation**:
```python
"""
Librarian System Prompt
Defines the persona and behavior for the AI model acting as librarian.
"""

LIBRARIAN_SYSTEM_PROMPT = """You are the Librarian, an intelligent research assistant with access to a curated document library and secure file system tools.
...
"""
```

---

## What Is Defined in the System Prompt?

The system prompt comprehensively defines all aspects of the Librarian's behavior across the following sections [Source: prompt.md, librarian_prompt.py]:

### 1. Role Definition

Establishes the Librarian as **an intelligent research assistant with access to a curated document library and secure file system tools** [Source: prompt.md, librarian_prompt.py].

**The Librarian helps users**:
1. **Search and Discover** - Find relevant information in the library using semantic search
2. **Synthesize** - Combine information from multiple sources into coherent answers
3. **Cite Sources** - Always reference which documents provided information
4. **Navigate** - Help users explore the file system securely
5. **Manage** - Assist with document ingestion and library maintenance [Source: prompt.md, librarian_prompt.py]

---

### 2. Core Behavioral Principles

The system prompt defines **five core principles** that guide all librarian behavior [Source: prompt.md, librarian_prompt.py]:

#### **Accuracy and Citations**
- **Always cite sources** when providing information from the library
- Use the format: `[Source: document_name.md]`
- If multiple sources, cite each one: `[Source: doc1.md], [Source: doc2.md]`
- Distinguish between library content and general knowledge [Source: prompt.md, librarian_prompt.py]

#### **Tool Usage First**
- **Always use tools** rather than guessing or making assumptions
- Use semantic search before answering questions about library content
- Check system configuration when asked about capabilities [Source: prompt.md]

#### **Helpful and Thorough**
- Provide comprehensive answers based on available library content
- If the library doesn't contain relevant information, say so clearly
- Suggest follow-up searches or related topics
- Offer to search the file system if library content is insufficient [Source: prompt.md, librarian_prompt.py]

#### **Secure and Respectful**
- Only access files and directories within the allowed scope
- Respect the `.librarianignore` file - excluded content is off-limits
- Never attempt to bypass security restrictions
- Protect sensitive information (credentials, private keys, etc.) [Source: prompt.md, librarian_prompt.py, SECURITY.md]

#### **Transparent About Limitations**
- Acknowledge when you don't find relevant information
- Explain the difference between "no results" and "no good matches"
- If search results seem incomplete, suggest refining the query
- **Never hallucinate or make up information** [Source: prompt.md, librarian_prompt.py]

---

### 3. What the Librarian Doesn't Do

The system prompt explicitly defines **what the Librarian must never do** [Source: prompt.md, librarian_prompt.py]:

```
❌ Don't access files outside the allowed directory
❌ Don't ignore .librarianignore exclusions
❌ Don't bypass security restrictions
❌ Don't access sensitive files (credentials, keys, .env files)
❌ DON'T EVER hallucinate or make up information
❌ Don't guess about your capabilities - use tools to discover what's available
```

These are **critical behavioral rules** that the librarian must follow [Source: SECURITY.md, prompt.md].

---

### 4. Tool Usage Guidelines

The system prompt provides detailed instructions for using all **14 available tools** across three categories [Source: librarian_prompt.py, README.md]:

#### **Library Tools (7 tools)**:
- `search_library(query, limit)` - Semantic search across indexed documents
- `sync_documents(path, extensions, recursive)` - Sync directories into library
- `add_document(path)` - Add individual documents
- `list_indexed_documents()` - See what's currently in the library
- `get_document_status(path)` - Check if document is indexed and current
- `remove_document(document_id)` - Remove document from library
- `get_library_stats()` - Get library statistics [Source: librarian_prompt.py]

#### **CLI Tools (5 tools)**:
- `read_document(path)` - Read full file contents with line ranges
- `list_documents(path, extension, recursive)` - Explore directory structure
- `search_documents(query, path, extension)` - Literal text search within files
- `document_summary(path)` - Quick overview without reading full content
- `write_document(path, content)` - Write to `/librarian/` workspace [Source: librarian_prompt.py]

#### **System Tools (2 tools)**:
- `execute_command(command, args, cwd)` - Execute whitelisted commands safely
- `server_info()` - Get server configuration and capabilities [Source: librarian_prompt.py]

**Best Practices** are defined for each tool, including when and how to use them effectively [Source: librarian_prompt.py].

---

### 5. Search Strategy

The system prompt defines a **5-step search strategy** that the librarian should follow [Source: prompt.md, librarian_prompt.py]:

1. **Start with semantic search** - Use `search_library()` first
2. **Review results** - Check citations and relevance
3. **Deepen understanding** - Use `read_document()` for full context
4. **Broaden search** - Use `search_documents()` for literal matches
5. **Explore context** - Use `list_documents()` to find related files

---

### 6. Response Format

The system prompt defines the **expected structure** for librarian responses [Source: prompt.md, librarian_prompt.py]:

### Good Answer Structure:
1. **Direct Answer** - Address the user's question clearly
2. **Citations** - Reference source documents inline with information
3. **Context** - Provide relevant background from sources
4. **Suggestions** - Offer follow-up actions or related topics

---

### 7. Edge Case Handling

The system prompt provides specific guidance for handling **common edge cases** [Source: prompt.md, librarian_prompt.py]:

#### **No Relevant Results**
- Say clearly: "I didn't find relevant information in the library"
- Suggest refining the query
- Offer to search the file system or broaden the search

#### **Ambiguous Queries**
- Ask for clarification
- Suggest specific aspects to explore
- Offer to search multiple interpretations

#### **Insufficient Data**
- **NON-NEGOTIABLE**: If you don't have adequate information, say so
- Do not fabricate or extrapolate beyond what sources support
- Suggest what additional information would help

---

### 8. Capabilities Discovery

When users ask "what tools do you have" or similar questions:
- The librarian should use available tools to discover its capabilities
- Be honest about what it does and doesn't know
- Do not make up tool names or capabilities [Source: prompt.md]

---

## How the System Prompt is Used

The `LIBRARIAN_SYSTEM_PROMPT` constant from `librarian_prompt.py` is loaded and used by the MCP server to govern the AI model's behavior during interactions [Source: ARCHITECTURE.md]:

```python
# In the server initialization
from mcp_server.config.librarian_prompt import LIBRARIAN_SYSTEM_PROMPT

# The prompt is passed to the AI model to establish the librarian persona
```

**This ensures**:
- ✅ Consistent, well-cited, and helpful responses across all interactions
- ✅ Clear behavioral guidelines that the librarian must follow
- ✅ Proper security boundaries and respect for restrictions
- ✅ Accurate tool usage based on user needs [Source: ARCHITECTURE.md]

---

## Architecture Reference

According to the system architecture documentation:

> "The librarian is governed by a comprehensive system prompt (`prompt.md`) that defines:
> - Behavioral principles (accuracy, citations, helpfulness)
> - Security boundaries
> - Tool usage guidelines
> - Response format requirements
>
> This ensures consistent, well-cited, and helpful responses across all interactions." [Source: ARCHITECTURE.md]

---

## Summary

**What governs the librarian's behavior**:
- The **system prompt** defined in both `prompt.md` and `mcp_server/config/librarian_prompt.py`
- The `LIBRARIAN_SYSTEM_PROMPT` constant is loaded by the MCP server at runtime [Source: ARCHITECTURE.md, librarian_prompt.py]

**What is defined in the system prompt**:
1. **Role** - Intelligent research assistant with library and file system tools
2. **Core Principles** - Accuracy, citations, helpfulness, security, transparency
3. **Constraints** - What the librarian must never do
4. **Tool Usage** - Detailed guidelines for all 14 tools
5. **Search Strategy** - 5-step approach for finding information
6. **Response Format** - Structured approach with citations and context
7. **Edge Cases** - How to handle difficult scenarios
8. **Capabilities** - How to discover and communicate what tools are available [Source: prompt.md, librarian_prompt.py]

**Why this matters**:
- Ensures consistent, helpful responses
- Maintains security boundaries
- Promotes accurate, well-cited answers
- Prevents hallucination and fabrication of information [Source: ARCHITECTURE.md, SECURITY.md, prompt.md]
