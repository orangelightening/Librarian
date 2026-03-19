## Query: Explain the librarian-mcp architecture with source citations

## Response from qwen3.5 9b 4 bit  quant running  locally in Lmstudio chat window


I'll search the library for information about the librarian-mcp architecture.

Let me read the key architectural documents to provide you with comprehensive details and proper citations.

Based on the comprehensive documentation in the library, here's a detailed explanation of the **Librarian MCP architecture**:

---

## 🏗️ Librarian MCP Architecture Overview

The Librarian MCP Server is a unified Model Context Protocol (MCP) server that enables AI models to act as intelligent librarians with document querying capabilities. It merges two existing projects: **Librarian AI** (semantic search system) and **CLI-MCP** (secure CLI access).

[Source: reco.md], [Source: IMPLEMENTATION_SUMMARY.md]

---

## 📐 Core Architecture Components

### 1. **MCP Server Layer** (FastMCP-based)
The server uses **FastMCP** as its base framework, providing a unified interface for AI models to interact with the system.

[Source: reco.md]

```
AI Model → MCP Client → FastMCP Server → Tools & Backend
```

### 2. **Tool Categories**

#### Library Tools (7 tools)
- `search_library(query, limit)` - Semantic search over documents using ChromaDB vector embeddings
- `sync_documents(path, extensions, recursive)` - Sync entire directories into the library
- `add_document(path)` - Add single document to library
- `remove_document(document_id)` - Remove document from library
- `list_indexed_documents()` - List all indexed documents with metadata
- `get_document_status(path)` - Check if document is indexed and up-to-date
- `get_library_stats()` - Get library statistics (document count, chunk count, etc.)

[Source: IMPLEMENTATION_SUMMARY.md], [Source: README.md]

#### CLI Tools (6 tools)
- `execute_command(command, args, cwd)` - Execute whitelisted commands securely
- `read_document(path)` - Read file contents with optional line ranges
- `list_documents(path, extension, recursive)` - List files in directory
- `search_documents(query, path, extension)` - Literal text search within files
- `document_summary(path)` - Get structural overview without reading full content
- `server_info()` - Show server configuration and allowed commands

[Source: IMPLEMENTATION_SUMMARY.md]

### 3. **Backend Layer** (ChromaDB → Chonkie)
The backend provides storage and retrieval capabilities with abstraction for future upgrades.

```
├── chroma_backend.py     # Current ChromaDB implementation (Phase 1)
└── chonkie_backend.py    # Future advanced chunking (Phase 2)
```

[Source: reco.md], [Source: IMPLEMENTATION_SUMMARY.md]

### 4. **AI Layer** (Response Synthesis)
The AI layer handles result aggregation and citation formatting, ensuring proper attribution of sources.

[Source: IMPLEMENTATION_SUMMARY.md]

---

## 🔒 Security Architecture

### The `.librarianignore` File
A gitignore-style exclusion file with **94 built-in security patterns** that automatically exclude sensitive files from indexing.

[Source: IMPLEMENTATION_SUMMARY.md], [Source: SECURITY_AND_BOUNDARIES.md]

#### Key Exclusions Include:
- **Security**: `.env`, `*.key`, `*.pem`, SSH keys (`id_rsa`)
- **Development**: `venv/`, `node_modules/`, `__pycache__/`
- **Databases**: `chroma_db/`, `metadata/`, `*.db` (don't index the DB!)
- **Logs & Temp**: `*.log`, `tmp/`, `temp/`

[Source: IMPLEMENTATION_SUMMARY.md]

### CLI Tool Security Features
1. **Command Whitelisting** - Only approved binaries can execute
2. **Directory Sandboxing** - All operations restricted to allowed directory (`--safe-dir`)
3. **Timeout Protection** - Commands terminate after timeout (default: 15s)
4. **Output Truncation** - Protects LLM context window (max: 8000 chars)
5. **Dangerous Flag Blocking** - Prevents misuse of safe commands

[Source: README.md], [Source: reco.md]

---

## 🔄 Data Flow Architecture

### Proposed Integrated Architecture:
```
AI Model Chat Window
    ↓
MCP Client
    ↓
Unified Librarian MCP Server (FastMCP)
    ├─→ Librarian Tools → ChromaDB Backend → ChromaDB Storage
    └─→ CLI Tools → File System Access
```

[Source: reco.md]

---

## 🛠️ Implementation Structure

### Project Directory Layout:
```
librarian-mcp/
├── mcp_server/                    # Main MCP server
│   ├── librarian_mcp.py           # Entry point with librarian prompt
│   │
│   ├── tools/                     # MCP tool implementations
│   │   ├── library_tools.py       # 7 library management tools
│   │   └── cli_tools.py           # 6 CLI/file access tools
│   │
│   ├── core/                      # Core business logic
│   │   ├── document_manager.py    # Document lifecycle (with ignore support)
│   │   ├── metadata_store.py      # JSON-based metadata tracking
│   │   └── ignore_patterns.py     # Gitignore-style pattern matching
│   │
│   ├── backend/                   # Storage backends
│   │   ├── base.py                # Abstract interface
│   │   └── chroma_backend.py      # ChromaDB implementation
│   │
│   ├── ai_layer/                  # AI response synthesis
│   │   └── ai_layer_interface.py  # Result aggregation with citations
│   │
│   └── config/                    # Configuration
│       ├── settings.py            # Centralized settings
│       └── librarian_prompt.py    # System prompt definitions
│
├── scripts/                       # Utility scripts
│   └── ingest.py                  # Bulk document ingestion
│
├── documents/                     # Document storage
├── chroma_db/                     # ChromaDB data
├── metadata/                      # Document tracking
├── .librarianignore               # Security exclusions (94 patterns)
└── requirements.txt               # Dependencies

```

[Source: IMPLEMENTATION_SUMMARY.md], [Source: README.md]

---

## 🤖 The Librarian Persona & Behavioral Guidelines

The system includes a comprehensive **Librarian Persona** with strict behavioral guidelines:

### Core Principles:
1. ✅ **Always cite sources** - Format: `[Source: document_name.md]`
2. ✅ **Acknowledge limitations** - Clearly state when information isn't found
3. ✅ **Respect boundaries** - Never access excluded files (`.librarianignore`)
4. ✅ **Protect sensitive data** - Credentials, keys, private files are off-limits
5. ✅ **Provide comprehensive answers** - Include citations and context

### Response Format:
```
Based on the library, semantic search is implemented using ChromaDB vector embeddings.

[Source: architecture.md]
Documents are chunked into 1000-character segments and embedded using
ChromaDB's default embedding function.

[Source: features.md]
The system supports automatic change detection via SHA-256 checksums,
ensuring modified documents are re-indexed automatically.

Would you like me to explain the chunking strategy in more detail?
```

[Source: IMPLEMENTATION_SUMMARY.md], [Source: USER_GUIDE.md]

---

## 🚀 Deployment Architecture

### Phase 1 (Current): Separate Processes Recommended
To avoid async/sync conflicts between FastAPI and FastMCP, the architecture recommends running components separately:

```bash
# Terminal 1: MCP Server Process (sync)
python mcp_server/librarian_mcp.py

# Optional Terminal 2: API Server Process (async - for testing only)
python api-layer/main.py
```

[Source: reco.md]

### Environment Variables:
```bash
export LIBRARIAN_SAFE_DIR=/home/peter/development
export LIBRARIAN_DOCUMENTS_DIR=./documents
export LIBRARIAN_CHROMA_PATH=./chroma_db
export LIBRARIAN_METADATA_PATH=./metadata
```

[Source: README.md]

---

## 📊 Current Status

- ✅ **Production Ready** - Version 1.0.0 (Phase 1)
- ✅ **All components tested and verified**
- ✅ **Comprehensive documentation** for users and developers
- ⏳ **Phase 2**: Chonkie integration planned (advanced chunking)

[Source: IMPLEMENTATION_SUMMARY.md], [Source: reco.md]

---

## 🔮 Future Enhancements (Phase 2)

1. **Chonkie Integration** - Replace ChromaDB's native chunking with advanced chunking pipeline
2. **Backend Abstraction** - Configurable backend selection via environment variables
3. **Performance Optimization** - Caching and batching improvements
4. **Enhanced AI Layer** - Better result synthesis algorithms

[Source: reco.md], [Source: PHASE2.md]

---

Would you like me to elaborate on any specific aspect of the architecture, such as the security model, the ChromaDB integration details, or the planned Chonkie migration?