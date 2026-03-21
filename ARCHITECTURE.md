# Librarian MCP Server - Architecture

## Overview

The **Librarian MCP Server** is a production-ready Model Context Protocol (MCP) server that enables AI models to act as intelligent librarians with semantic document search capabilities. It combines powerful document management with secure file system access and **two-way communication** via write access to a dedicated workspace.

**Status**: Phase 2 Complete ✅ | **14 MCP Tools** (7 library + 5 file system + 2 system)

**System Prompt**: All librarian behavior is governed by `System_prompt.md` - a comprehensive system prompt that defines the librarian's role, behavioral principles, citation requirements, and security boundaries. This prompt ensures consistent, accurate, and well-cited responses.

**NEW: Two-Way Communication**: The librarian can write analysis results, code changes, and documentation updates to `/librarian/` workspace, enabling persistent task delegation and iterative refinement.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Model Chat Window                          │
│                      (MCP Client: Jan/LM Studio)                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Unified Librarian MCP Server                    │
│                      (FastMCP Framework)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    MCP Tools Layer                        │  │
│  │  ┌──────────────────┐  ┌───────────────────────────┐     │  │
│  │  │  Library Tools   │  │       CLI Tools          │     │  │
│  │  │   (7 tools)      │  │     (7 tools)            │     │  │
│  │  └────────┬─────────┘  └───────────┬───────────────┘     │  │
│  └───────────┼───────────────────────┼───────────────────────┘  │
│              │                       │                           │
│  ┌───────────┼───────────────────────┼───────────────────────┐  │
│  │           ▼                       ▼                       │  │
│  │  ┌───────────────────────────────────────────────┐       │  │
│  │  │         Core Business Logic                   │       │  │
│  │  │  ┌─────────────────────────────────────────┐  │       │  │
│  │  │  │ Document Manager                         │  │       │  │
│  │  │  │ • Discovery & lifecycle                 │  │       │  │
│  │  │  │ • SHA-256 change detection              │  │       │  │
│  │  │  │ • .librarianignore integration           │  │       │  │
│  │  │  └─────────────────────────────────────────┘  │       │  │
│  │  │  ┌─────────────────────────────────────────┐  │       │  │
│  │  │  │ Metadata Store (JSON)                   │  │       │  │
│  │  │  └─────────────────────────────────────────┘  │       │  │
│  │  │  ┌─────────────────────────────────────────┐  │       │  │
│  │  │  │ Ignore Patterns (gitignore-style)        │  │       │  │
│  │  │  └─────────────────────────────────────────┘  │       │  │
│  │  └─────────────────┬─────────────────────────────┘       │  │
│  │                    │                                     │  │
│  │                    ▼                                     │  │
│  │  ┌─────────────────────────────────────────────┐         │  │
│  │  │         Backend Abstraction Layer           │         │  │
│  │  │  ┌───────────────────────────────────────┐  │         │  │
│  │  │  │  DocumentBackend Interface (ABC)      │  │         │  │
│  │  │  └───────────────────────────────────────┘  │         │  │
│  │  │  ┌───────────────────────────────────────┐  │         │  │
│  │  │  │  Backend Factory                      │  │         │  │
│  │  │  │  get_backend(type="chonkie"|"chroma") │  │         │  │
│  │  │  └───────────────────────────────────────┘  │         │  │
│  │  └─────────────┬────────────────────────────────┘         │  │
│  │                │                                          │  │
│  │    ┌───────────┴───────────┐                             │  │
│  │    ▼                       ▼                             │  │
│  │  ┌──────────────────┐  ┌──────────────────┐             │  │
│  │  │ ChonkieBackend   │  │ ChromaBackend    │             │  │
│  │  │ (DEFAULT)        │  │ (Optional)       │             │  │
│  │  │ • Semantic chunk │  │ • Simple chunk   │             │  │
│  │  │ • Smart boundaries│  │ • Sentence split │             │  │
│  │  │ • Better search  │  │ • Faster proc    │             │  │
│  │  └────────┬─────────┘  └────────┬─────────┘             │  │
│  └───────────┼────────────────────┼─────────────────────────┘
│              │                    │
│              └────────┬───────────┘
│                       ▼
│  ┌─────────────────────────────────────────────┐
│  │         AI Layer                            │
│  │  • Result aggregation                       │
│  │  • Citation formatting                      │
│  │  • Response synthesis                       │
│  └─────────────────────────────────────────────┘
│
└───────────────────────────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  ChromaDB      │
              │  Vector Store  │
              └────────────────┘
```

---

## Backend Architecture

### Abstract Interface

All backends implement the `DocumentBackend` abstract base class:

```python
class DocumentBackend(ABC):
    @abstractmethod
    def chunk_documents(self, documents, document_ids, source) -> List[Dict]:
        """Process documents into chunks with embeddings."""
        pass

    @abstractmethod
    def query(self, query_text: str, limit: int = 5) -> List[Dict]:
        """Perform semantic search."""
        pass

    @abstractmethod
    def delete_documents(self, document_id: str):
        """Remove all chunks for a document."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict:
        """Get backend statistics."""
        pass
```

### Backend Factory

The factory pattern enables runtime backend selection:

```python
def get_backend(backend_type: str = "chonkie", **kwargs) -> 'DocumentBackend':
    if backend_type == "chonkie":
        from .chonkie_backend import ChonkieBackend
        return ChonkieBackend(**kwargs)
    elif backend_type == "chroma":
        from .chroma_backend import ChromaBackend
        return ChromaBackend(**kwargs)
    else:
        raise ValueError(f"Unsupported backend type: {backend_type}")
```

**Backend Selection**: Set via `LIBRARIAN_BACKEND` environment variable:
- **`chonkie`** (default): Intelligent semantic chunking
- **`chroma`**: Simple sentence-based chunking

---

### ChonkieBackend (Default)

**Purpose**: Intelligent semantic chunking using the Chonkie library

**Key Features**:
- ✅ **Semantic boundaries**: Respects sentence and paragraph structure
- ✅ **Context preservation**: Related concepts stay together
- ✅ **Intelligent sizing**: Adapts to document structure
- ✅ **Better search results**: Higher quality chunks = better matches

**Implementation**:
```python
class ChonkieBackend(ChromaBackend):
    def __init__(self, chunk_size: int = 1000, min_chunk_size: int = 50):
        super().__init__()
        self.chunker = RecursiveChunker(
            chunk_size=chunk_size,
            min_characters_per_chunk=min_chunk_size
        )

    def chunk_documents(self, documents, document_ids, source):
        # Use Chonkie for intelligent chunking
        chonkie_chunks = self.chunker(doc_text)
        # Store in ChromaDB with enhanced metadata
        for chunk in chonkie_chunks:
            metadata = {
                "chunk_index": chunk_idx,
                "document_id": doc_id,
                "document_name": source,
                "token_count": chunk.token_count,
                "char_count": len(chunk.text),
                "chunking_method": "chonkie_recursive"
            }
            # ... store in ChromaDB
```

**When to Use Chonkie**:
- Most document types (technical docs, articles, books)
- When search result quality is important
- When documents have complex structure
- Default choice for production use

---

### ChromaBackend (Optional)

**Purpose**: Simple sentence-based chunking (original implementation)

**Key Features**:
- ✅ **Fast processing**: Quick chunking
- ✅ **Simple approach**: Splits by sentence boundaries
- ✅ **Predictable**: Consistent chunk sizes
- ✅ **Reliable**: Well-tested implementation

**When to Use ChromaDB Backend**:
- Processing speed is more important than search quality
- Very simple documents without complex structure
- Fallback if Chonkie has issues
- Testing and development

**Implementation**:
```python
class ChromaBackend(DocumentBackend):
    def chunk_documents(self, documents, document_ids, source):
        # Simple sentence-based chunking
        chunks = self._chunk_text(doc_text)
        for chunk_idx, chunk_text in enumerate(chunks):
            metadata = {
                "chunk_index": chunk_idx,
                "document_id": doc_id,
                "document_name": source,
                "chunking_method": "chroma_sentence"
            }
            # ... store in ChromaDB
```

---

## Document Lifecycle

### 1. Discovery

**Location**: `mcp_server/core/document_manager.py`

```python
def discover_documents(self, path: Path, extensions: Set[str], recursive: bool):
    """Discover all documents in a directory."""
    documents = []
    for ext in extensions:
        documents.extend(path.rglob(f"*{ext}") if recursive else path.glob(f"*{ext}"))

    # Filter out ignored files
    if self.ignore_patterns:
        documents = self.ignore_patterns.filter_paths(documents)

    return documents
```

### 2. Filtering

**Location**: `mcp_server/core/ignore_patterns.py`

The `.librarianignore` file uses gitignore-style patterns with **94+ built-in exclusions**:

```python
class IgnorePatterns:
    def is_ignored(self, file_path: Path) -> bool:
        """Check if file matches any ignore pattern."""
        # Check negation patterns first (exceptions)
        for pattern in self.negation_patterns:
            if self._matches_pattern(rel_path, pattern):
                return False  # Explicitly NOT ignored

        # Check ignore patterns
        for pattern in self.patterns:
            if self._matches_pattern(rel_path, pattern):
                return True  # Ignored

        return False
```

### 3. Checksum Calculation

**Location**: `mcp_server/core/document_manager.py`

```python
def calculate_checksum(self, file_path: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
```

### 4. Change Detection

```python
existing = self.metadata.get_by_path(str(file_path))
if existing and existing['checksum'] == file_meta['checksum']:
    return {"status": "unchanged"}  # Skip re-processing
```

### 5. Chunking

**Default (Chonkie)**:
```python
from chonkie import RecursiveChunker
chunker = RecursiveChunker(chunk_size=1000, min_characters_per_chunk=50)
chunks = chunker(document_text)
```

**Optional (ChromaDB)**:
```python
chunks = document_text.split('. ')  # Simple sentence splitting
```

### 6. Embedding & Storage

Both backends use ChromaDB for vector storage:
```python
collection.add(
    documents=[chunk_text],
    ids=[chunk_id],
    metadatas=[metadata]
)
```

### 7. Metadata Update

```python
self.metadata.add({
    "document_id": doc_id,
    "path": str(file_path),
    "checksum": checksum,
    "chunk_count": len(chunks),
    "indexed_at": datetime.now().isoformat()
})
```

---

## Data Flow

### Document Ingestion Flow

```
User calls: sync_documents(path="/home/peter/docs", extensions=".md,.txt")
    ↓
DocumentManager.discover_documents()
    ↓ [filter through .librarianignore]
    ↓ [calculate SHA-256 checksums]
    ↓ [check metadata for changes]
    ↓
DocumentManager.add_document()
    ↓ [read file content]
    ↓ [calculate checksum]
    ↓ [check if already indexed]
    ↓
Backend.chunk_documents()
    ↓ [Chonkie: intelligent semantic chunking]
    ↓ [or ChromaDB: simple sentence chunking]
    ↓
ChromaDB collection.add()
    ↓ [generate embeddings]
    ↓ [store chunks with metadata]
    ↓
MetadataStore.add()
    ↓ [store document metadata]
    ↓
Return: {"added": X, "updated": Y, "unchanged": Z, "removed": W}
```

### Search Query Flow

```
User query: "How does the MCP server work?"
    ↓
MCP Client → FastMCP Server
    ↓
Library Tool: search_library(query="...", limit=5)
    ↓
Backend.query(query_text, limit)
    ↓ [ChromaDB semantic search]
    ↓ [vector similarity matching]
    ↓ [return top 5 chunks with scores]
    ↓
AILayer.aggregate_results(chunks, query)
    ↓ [sort by similarity score]
    ↓ [build response from chunks]
    ↓ [generate citations]
    ↓
Return formatted response:
"Found 5 relevant chunks.

[1] Chunk text excerpt... [Source: ARCHITECTURE.md]
[2] Chunk text excerpt... [Source: README.md]
...

**Sources:**
[1] ARCHITECTURE.md (Relevance: 0.95)
[2] README.md (Relevance: 0.87)
..."
```

----

## Two-Way Communication Architecture

### Overview

The librarian supports **bi-directional communication** through the `write_document` tool, enabling:

1. **Persistent Analysis**: Librarian writes detailed reports to `/librarian/` workspace
2. **Task Delegation**: Complex analysis broken into written deliverables
3. **Iterative Refinement**: v1, v2, v3 files for updated analysis
4. **User Control**: Review written output before applying changes

### Workspace Design

```
/home/peter/development/librarian-mcp/
├── librarian/                    # Write workspace (librarian-only access)
│   ├── exception-analysis.md     # Code review reports
│   ├── refactor-plan-v1.md       # Refactoring recommendations
│   ├── security-audit.md         # Security analysis results
│   └── reports/                  # Organized subdirectories
│       ├── backend-analysis.md
│       └── core-analysis.md
├── documents/                    # Source documents (read-only access)
├── chroma_db/                    # Vector index
└── metadata/                     # Document metadata
```

### Write Security Model

**7 Layers of Protection**:

1. **Subdirectory Restriction**: Writes ONLY allowed in `/librarian/`
2. **Safe Directory Boundary**: Must stay within `LIBRARIAN_SAFE_DIR`
3. **File Size Limits**: Maximum 100KB per write operation
4. **Critical File Protection**: Blocks sensitive filename patterns (password, secret, key, credential, .env, config)
5. **Directory Traversal Protection**: Same `is_safe_path()` validation as reads
6. **Audit Logging**: All writes logged to console
7. **User Control**: Files written to `/librarian/` require manual review and application

### Communication Patterns

**Pattern 1: Analysis Delivery**
```
User: "Review all exception handling in backend/"
Librarian: [Searches code, provides summary]
User: "Write detailed analysis to /librarian/backend-exceptions.md"
Librarian: [Writes comprehensive report with code snippets and recommendations]
User: [Reads file, applies approved changes]
```

**Pattern 2: Iterative Refinement**
```
User: "Create a refactoring plan for document_manager.py"
Librarian: [Writes /librarian/refactor-plan-v1.md]
User: [Reviews, applies changes]
User: "Update the plan based on my implementation"
Librarian: [Writes /librarian/refactor-plan-v2.md with verification]
```

**Pattern 3: Task Breakdown**
```
User: "Analyze the entire codebase for security issues"
Librarian: "That's a large task. I'll break it into parts:"
Librarian: [Writes /librarian/security-part1-backend.md]
Librarian: [Writes /librarian/security-part2-core.md]
Librarian: [Writes /librarian/security-part3-tools.md]
User: [Reviews each part independently]
```

### Context Window Management

**Understanding Context Usage**:

Write operations create persistent files, but content generation still consumes LLM context:

```
Task: "Analyze all exception handling in backend/"
├── Content generated: 15,000 characters
├── Chat output: 8,000 characters (truncated with warning)
├── File write: 15,000 characters (full content written)
└── Context used: 15,000 characters (full generation cost)
```

**Best Practices**:

1. **Break Large Tasks**: Analyze one module at a time
2. **Summary + Details**: Request brief summary in chat, full details to file
3. **Iterative Approach**: Start with overview, then drill down iteratively
4. **Check Limits**: Use `server_info()` to see current limits (8KB chat output, 100KB file write)

**When to Use Write Access**:
- ✅ Code reviews and refactoring plans
- ✅ Security audit results
- ✅ Multi-file analysis reports
- ✅ Documentation updates
- ✅ Debugging diagnostics

**When to Keep It Brief**:
- ❌ Simple queries ("What does this function do?")
- ❌ Quick lookups ("Find the backend configuration")
- ❌ Status checks ("How many documents indexed?")

---

## Security Model

### Multi-Layer Security

**Layer 1: .librarianignore (94+ patterns)**
- Security: `.env`, `*.key`, `*.pem`, credentials
- Development: `venv/`, `node_modules/`, `__pycache__/`
- Databases: `chroma_db/`, `metadata/`, `*.db`
- Logs: `*.log`, `logs/`, `*.tmp`

**Layer 2: Command Whitelisting**
```python
ALLOWED_BINARY_NAMES = {
    "ls", "cd", "pwd", "whoami", "echo", "cat", "find", "grep",
    "head", "tail", "sort", "uniq", "cut", "awk", "date", "hostname"
}

DANGEROUS_COMMANDS = {
    "rm", "rmdir", "chmod", "chown", "wget", "curl", "nc",
    "ssh", "python", "bash", "sh", "zsh"
}
```

**Layer 3: Directory Sandboxing**
```python
def is_safe_path(path: str, safe_dir: str):
    resolved = os.path.realpath(path)
    if not resolved.startswith(safe_dir):
        raise SecurityError("Path traversal detected")
```

**Layer 4: Output Truncation**
```python
MAX_OUTPUT_CHARS = 8000  # Protect LLM context window
```

**Layer 5: Timeout Protection**
```python
DEFAULT_TIMEOUT_SECONDS = 15  # Prevent runaway commands
```

**Layer 6: File Size Limits**
```python
MAX_DOCUMENT_SIZE = 10MB  # Prevent oversized documents
```

---

## Technology Stack

### Core Framework
- **FastMCP**: Model Context Protocol server framework
- **Python 3.13**: Core language

### Storage & Search
- **ChromaDB**: Vector database for semantic search
- **Chonkie**: Intelligent semantic chunking library

### Security & Validation
- **SHA-256**: Document checksums for change detection
- **gitignore-style patterns**: Flexible file filtering

### Deployment
- **venv**: Virtual environment (NOT Docker)
- **stdio transport**: MCP communication protocol

---

## Why venv Instead of Docker?

### Advantages of venv Approach

**1. Simplicity**
- No Docker complexity or learning curve
- Standard Python deployment
- Easier for users to understand and modify

**2. Close Coupling**
- Direct Python access to Chonkie and ChromaDB
- No container boundaries between components
- Shared memory space for efficient data passing

**3. Performance**
- **stdio transport** (no HTTP overhead)
- No container overhead (CPU, memory)
- Faster startup and shutdown

**4. Debugging**
- Direct Python debugger access
- Easy log inspection
- No container shell complexities

**5. Resource Usage**
- Lower memory footprint
- No duplicate Python installations
- Shared system libraries

**6. Integration**
- Easier to integrate with other Python tools
- Direct access to file system
- Simpler CI/CD pipelines

### When Docker Might Be Better

- Multi-user deployment requiring isolation
- Running on non-Python systems
- Complex dependency conflicts
- Enterprise deployment requirements

**For single-user local deployment, venv is superior.**

---

## MCP Tools (13 Total)

### Library Tools (7)
1. `search_library(query, limit)` - Semantic search
2. `sync_documents(path, extensions, recursive)` - Bulk sync
3. `add_document(path)` - Add single document
4. `remove_document(document_id)` - Remove document
5. `list_indexed_documents()` - List all documents
6. `get_document_status(path)` - Check document status
7. `get_library_stats()` - Get statistics

### File System Tools (5)
1. `read_document(path, start_line, end_line, head, tail, max_chars)` - Read files with ranges
2. `write_document(path, content, create_dirs)` - **Write files to `/librarian/` workspace** (two-way communication)
3. `list_documents(path, extension, recursive)` - List files
4. `search_documents(query, path, extension, case_sensitive)` - Search file contents
5. `document_summary(path)` - Get file overview

**NEW: Write Access Feature**

The `write_document` tool enables a two-way communication channel:

**Security Model**:
- ✅ Writes ONLY allowed in `/librarian/` subdirectory
- ✅ Maximum 100KB per file write
- ✅ Multiple layers of path validation
- ✅ Critical file protection (blocks passwords, secrets, keys)
- ✅ Audit logging for all write operations

**Use Cases**:
- Analysis results and code reviews
- Refactoring plans with recommendations
- Documentation updates
- Debugging diagnostics
- Task delegation outputs

**Workflow Example**:
```
User: "Analyze exception handling in backend/, write to /librarian/analysis.md"
Librarian: [Searches code, writes detailed report]
User: [Reads /librarian/analysis.md, applies approved changes]
User: "Update the analysis after my changes"
Librarian: [Writes /librarian/analysis-v2.md with verification]
```

**Context Management**: Large write operations still consume LLM context during generation. Break big tasks into chunks for optimal performance.

### System Tools (2)
1. `execute_command(command, args, cwd)` - Execute whitelisted commands
2. `server_info()` - Show configuration

---

## File Structure

```
mcp_server/
├── librarian_mcp.py           # Entry point (FastMCP server)
├── tools/
│   ├── library_tools.py       # 7 library tools
│   └── cli_tools.py           # 6 CLI tools
├── core/
│   ├── document_manager.py    # Document lifecycle
│   ├── metadata_store.py      # JSON metadata tracking
│   └── ignore_patterns.py     # Gitignore-style filtering
├── backend/
│   ├── base.py                # Abstract backend interface
│   ├── factory.py             # Backend factory
│   ├── chonkie_backend.py     # Chonkie backend (DEFAULT)
│   └── chroma_backend.py      # ChromaDB backend (optional)
├── ai_layer/
│   └── ai_layer_interface.py  # Result aggregation
└── config/
    ├── settings.py            # Configuration (Chonkie default)
    └── librarian_prompt.py    # System prompt
```

---

## Configuration

### Environment Variables

```bash
# Backend selection (chonkie = default, chroma = optional)
export LIBRARIAN_BACKEND=chonkie

# Directory configuration
export LIBRARIAN_SAFE_DIR=/home/peter/development
export LIBRARIAN_DOCUMENTS_DIR=./documents
export LIBRARIAN_CHROMA_PATH=./chroma_db
export LIBRARIAN_METADATA_PATH=./metadata

# Processing
export LIBRARIAN_MAX_DOCUMENT_SIZE=10000000  # 10MB
export LIBRARIAN_CHUNK_SIZE=1000

# Security
export LIBRARIAN_MAX_OUTPUT_CHARS=8000
export LIBRARIAN_COMMAND_TIMEOUT=15
```

### Command-Line Arguments

```bash
python mcp_server/librarian_mcp.py \
  --safe-dir /home/peter/development \
  --documents-dir ./documents \
  --chroma-path ./chroma_db \
  --metadata-path ./metadata
```

---

## See Also

- [README.md](README.md) - Quick start and overview
- [CONFIGURATION.md](CONFIGURATION.md) - Detailed configuration reference
- [SECURITY.md](SECURITY.md) - Security model and boundaries
- [Tools.md](Tools.md) - Complete tool reference
- [PHASE2/CHONKIE_MIGRATION.md](PHASE2/CHONKIE_MIGRATION.md) - Backend migration guide
