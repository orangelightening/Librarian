
## Query

HOW DOES THE MCP SERVER WORK? EXPLAIN USING REFERENCES TO THE python programs which are in the system. I want citations for the items referenced. Dig deep and be thorough.


# Responses

 ## GLM-4.7 frontier model

Failed the first time trying to use sequentialthinking
The second time crashed as well. I don't know why. It Just stopped. 


---
## Qwen3.5 9b 4 bit


# How the MCP Server Works: Complete Architecture Explanation

## 🏗️ High-Level Architecture

The Librarian MCP Server is built on **FastMCP** framework and follows a layered architecture with four main components:

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Server Entry Point                 │
│              librarian_mcp.py (FastMCP)                   │
├──────────────────────────────────────────────────────────┤
│  Library Tools │ CLI Tools │ Document Manager │ Backend  │
│   Layer       │   Layer    │   Core Logic     │  Layer   │
├──────────────────────────────────────────────────────────┤
│              AI Layer (Result Aggregation)                │
└──────────────────────────────────────────────────────────┘
```

[Source: librarian_mcp.py]

---

## 🚪 1. Entry Point: `librarian_mcp.py`

The main entry point initializes the FastMCP server with a librarian persona and registers all tools.

**Key Components:**
- **FastMCP Server**: Created with instructions from `librarian_prompt.py`
- **Tool Registration**: Calls `register_library_tools()` and `register_cli_tools()`
- **Configuration**: Loads settings from environment variables or CLI arguments

```python
# From librarian_mcp.py (lines 47-95)
mcp = FastMCP(
    "librarian-mcp",
    instructions=instructions  # Librarian persona from librarian_prompt.py
)

register_library_tools(mcp)   # Registers 7 library tools
register_cli_tools(mcp, args.safe_dir)  # Registers 6 CLI tools
```

[Source: librarian_mcp.py]

---

## 📚 2. Library Tools Layer (`library_tools.py`)

This module implements **7 MCP tools** for document management using a **lazy initialization pattern** with singleton instances.

### Tool Registration Pattern

```python
# From library_tools.py (lines 15-30)
_backend = None
_metadata = None
_doc_manager = None
_ai_layer = None

def get_backend():
    """Get or create backend instance based on settings."""
    global _backend
    if _backend is None:
        _backend = create_backend(
            backend_type=settings.BACKEND,  # 'chroma' or 'chonkie'
            collection_name=settings.CHROMA_COLLECTION,
            db_path=settings.CHROMA_PATH
        )
    return _backend
```

[Source: library_tools.py]

### The 7 Library Tools:

| Tool | Implementation Location | Purpose |
|------|------------------------|---------|
| `search_library(query, limit)` | Lines 49-80 | Semantic search via ChromaDB + AI aggregation |
| `sync_documents(path, extensions, recursive)` | Lines 82-137 | Add/update/remove documents from directory |
| `add_document(path)` | Lines 139-165 | Add single document to library |
| `remove_document(document_id)` | Lines 167-185 | Remove document and all chunks |
| `list_indexed_documents()` | Lines 187-220 | List all indexed documents with metadata |
| `get_document_status(path)` | Lines 222-260 | Check if document is indexed/current/outdated |
| `get_library_stats()` | (Not shown in excerpt) | Get library statistics |

[Source: library_tools.py]

---

## 🛠️ 3. CLI Tools Layer (`cli_tools.py`)

This module implements **6 MCP tools** for secure file system access with **multiple security layers**.

### Security Architecture

```python
# From cli_tools.py (lines 16-40)
ALLOWED_BINARY_NAMES = {
    "ls", "cd", "pwd", "whoami", "echo", "cat", "find", "grep", 
    "head", "tail", "sort", "uniq", "cut", "awk", "date", "hostname"
}

DANGEROUS_COMMANDS = {
    "rm", "rmdir", "chmod", "chown", "dd", "mkfs", "fdisk",
    "wget", "curl", "nc", "netcat", "ssh", "scp", "rsync",
    "tar", "zip", "unzip", "mount", "umount", "python", 
    "python3", "perl", "bash", "sh", "zsh"
}

BANNED_FLAG_COMBOS = {
    ("find", "-delete"),
    ("find", "-exec"),
    ("awk", "system"),
    ("awk", "systime"),
}
```

[Source: cli_tools.py]

### The 6 CLI Tools:

| Tool | Implementation Location | Purpose |
|------|------------------------|---------|
| `execute_command(command, args, cwd)` | Lines 82-137 | Execute whitelisted commands with timeout (15s) |
| `read_document(path, start_line, end_line, head, tail, max_chars)` | Lines 139-206 | Read file contents with optional line ranges |
| `list_documents(path, extension, recursive)` | (Not shown in excerpt) | List files in directory |
| `search_documents(query, path, extension, case_sensitive)` | (Not shown in excerpt) | Literal text search in files |
| `document_summary(path)` | (Not shown in excerpt) | Get file structure/overview |
| `server_info()` | (Not shown in excerpt) | Show server configuration |

**Security Features:**
- **Command Whitelisting**: Only approved binaries can execute
- **Path Validation**: Uses `is_safe_path()` to prevent directory traversal
- **Output Truncation**: Limits output to 8000 chars (configurable via `MAX_OUTPUT_CHARS`)
- **Timeout Protection**: Commands terminate after 15 seconds

[Source: cli_tools.py]

---

## 📦 4. Core Business Logic Layer (`mcp_server/core/`)

### Document Manager (`document_manager.py`)

The document manager handles the complete document lifecycle with **SHA-256 checksum-based change detection**.

**Key Features:**
- **Discovery**: Scans directories using `discover_documents()` (lines 38-70)
- **Checksum Calculation**: SHA-256 for detecting modifications (lines 72-86)
- **Change Detection**: Compares checksums to determine add/update/delete
- **Size Limits**: Enforces maximum document size (default: 10MB)

```python
# From document_manager.py (lines 88-135)
def add_document(self, file_path: Path, source: str = None) -> Dict:
    """Add a single document to the library."""
    # Check file size
    if file_path.stat().st_size > settings.MAX_DOCUMENT_SIZE:
        return {"status": "error", "error": "Exceeds max size"}
    
    # Read and chunk document
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Calculate checksum for change detection
    file_meta = self.get_file_metadata(file_path)
    
    # Check if already exists (change detection via checksum)
    existing = self.metadata.get_by_path(str(file_path))
    if existing and existing['checksum'] == file_meta['checksum']:
        return {"status": "unchanged", ...}
```

[Source: document_manager.py]

**Document Lifecycle Operations:**
1. **Add**: New documents are chunked and indexed
2. **Update**: Modified documents (detected via checksum change) replace old versions
3. **Remove**: Documents deleted from source are removed from library
4. **Sync**: Bulk operation that handles all three cases

[Source: document_manager.py]

### Metadata Store (`metadata_store.py`)

JSON-based metadata tracking stored in `metadata/index.json`.

**Key Operations:**
- **Add**: Stores document metadata with checksum, size, modification time
- **Get by Path**: Finds document by file path for change detection
- **Delete**: Removes document metadata when deleted from library
- **Update**: Updates document metadata (e.g., chunk count)

```python
# From metadata_store.py (lines 45-70)
def add(self, metadata: Dict):
    """Add document metadata."""
    if 'document_id' not in metadata:
        raise ValueError("Metadata must contain 'document_id'")
    
    self._index[metadata['document_id']] = metadata
    self._save_index()  # Persist to disk

def get_by_path(self, path: str) -> Optional[Dict]:
    """Get metadata by file path for change detection."""
    normalized_path = str(Path(path).resolve())
    for doc in self._index.values():
        if Path(doc.get('path', '')).resolve() == Path(normalized_path).resolve():
            return doc
    return None
```

[Source: metadata_store.py]

### Ignore Patterns (`ignore_patterns.py`)

Gitignore-style pattern matching with **94 built-in exclusion patterns** for security.

**Security Categories:**
- **Always Excluded**: `.env`, `*.key`, `*.pem`, credentials files
- **Development**: `venv/`, `node_modules/`, `__pycache__/`
- **Build Artifacts**: `dist/`, `build/`, `*.egg-info/`
- **Data & Databases**: `chroma_db/`, `metadata/`, `*.sqlite`
- **Logs & Temp**: `*.log`, `logs/`, `*.tmp`

```python
# From ignore_patterns.py (lines 39-75)
def is_ignored(self, file_path: Path) -> bool:
    """Check if a file path matches any ignore pattern."""
    file_path = file_path.resolve()
    rel_path = str(file_path.relative_to(self.root_path))
    
    # Check negation patterns first (exceptions)
    for pattern in self.negation_patterns:
        if self._matches_pattern(rel_path, pattern):
            return False  # Explicitly NOT ignored
    
    # Check ignore patterns
    for pattern in self.patterns:
        if self._matches_pattern(rel_path, pattern):
            return True  # Ignored
    
    return False  # Not ignored

def filter_paths(self, paths: List[Path]) -> List[Path]:
    """Filter a list of paths, removing ignored ones."""
    return [p for p in paths if not self.is_ignored(p)]
```

[Source: ignore_patterns.py]

**Usage Example:**
```
Sync completed for directory: /home/peter/documents
  Added: 15 documents
  Updated: 3 documents
  Unchanged: 42 documents
  Removed: 0 documents
  Ignored: 127 (excluded by .librarianignore)  ← Security in action!
```

[Source: IMPLEMENTATION_SUMMARY.md]

---

## 💾 5. Backend Layer (`mcp_server/backend/`)

### Abstract Interface (`base.py`)

Defines the contract for all document backends using Python's abstract base classes.

```python
# From base.py (lines 10-48)
class DocumentBackend(ABC):
    """Abstract base class for document storage and retrieval."""
    
    @abstractmethod
    def chunk_documents(self, documents: List[str], 
                       document_ids: Optional[List[str]] = None,
                       source: str = "upload") -> List[Dict]:
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

[Source: base.py]

### ChromaDB Backend (`chroma_backend.py`)

Implements the document storage and retrieval using ChromaDB vector database.

**Key Operations:**

1. **Initialization**: Creates persistent ChromaDB client with HNSW index (cosine similarity)
2. **Chunking**: Splits documents into sentence-based chunks (configurable size: 1000 chars default)
3. **Query**: Semantic search using vector embeddings
4. **Delete**: Removes all chunks for a document by ID prefix

```python
# From chroma_backend.py (lines 37-65)
def chunk_documents(self, documents: List[str], 
                    document_ids: Optional[List[str]] = None,
                    source: str = "upload") -> List[Dict]:
    """Process documents into chunks with embeddings."""
    
    for doc_id, doc_text in zip(document_ids, documents):
        # Simple sentence-based chunking
        chunks = self._chunk_text(doc_text)
        
        for chunk_idx, chunk_text in enumerate(chunks):
            if not chunk_text.strip():
                continue
            
            chunk_id = f"{doc_id}-chunk-{chunk_idx}"
            metadata = {
                "chunk_index": chunk_idx,
                "document_id": doc_id,
                "document_name": source
            }
            
            collection.add(
                documents=[chunk_text],
                ids=[chunk_id],
                metadatas=[metadata]
            )
```

[Source: chroma_backend.py]

**Chunking Strategy:**
- Splits text by sentences (`'. '` delimiter)
- Respects chunk size limit (default: 1000 chars)
- Maintains sentence boundaries for semantic coherence

[Source: chroma_backend.py]

### Backend Factory (`factory.py`)

Provides backend selection via environment variable `LIBRARIAN_BACKEND`.

```python
# From factory.py
def get_backend(backend_type: str, collection_name: str, db_path: str):
    """Factory function to create backend instance."""
    if backend_type == "chroma":
        return ChromaBackend(collection_name, db_path)
    elif backend_type == "chonkie":
        return ChonkieBackend(collection_name, db_path)  # Phase 2
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")
```

[Source: factory.py]

**Phase 2 Enhancement:**
The architecture supports easy backend swapping by setting `LIBRARIAN_BACKEND=chonkie` environment variable with no tool code changes needed.

[Source: README.md]

---

## 🤖 6. AI Layer (`ai_layer_interface.py`)

Abstract interface for result aggregation and response synthesis.

### Default Implementation (`DefaultAILayer`)

**Key Operations:**

1. **Format Query**: Transforms user query into optimized search parameters
2. **Aggregate Results**: Synthesizes multiple chunks into coherent response with citations
3. **Build Context**: Determines optimal chunks based on inferred user intent

```python
# From ai_layer_interface.py (lines 57-108)
def aggregate_results(self, chunks: List[Dict], query: str = None) -> Dict:
    """Aggregate search results into coherent response."""
    
    if not chunks:
        return {
            "response": "No relevant documents found for your query.",
            "num_chunks": 0,
            "citations": []
        }
    
    # Sort by rank and take top chunks
    top_chunks = sorted(chunks, key=lambda x: x.get("rank", 999))[:5]
    
    # Build response from chunk texts
    response_parts = []
    for i, chunk in enumerate(top_chunks):
        text = chunk.get("text", "")
        if len(text) > 500:
            text = text[:500] + "..."
        
        response_parts.append(f"[{i+1}] {text}")
    
    response = "\n\n".join(response_parts)
    
    # Build citations list with document names
    citations = []
    for i, chunk in enumerate(top_chunks):
        metadata = chunk.get("metadata", {})
        doc_name = metadata.get("document_name", "Unknown Document")
        score = chunk.get("similarity_score", 0)
        citations.append(f"[{i+1}] {doc_name} (Relevance: {score:.2f})")
    
    return {
        "response": response,
        "citations": citations,
        "num_chunks": len(chunks),
        "top_results": [...]
    }
```

[Source: ai_layer_interface.py]

**Citation Format:**
The AI layer generates citations in the format `[Source: document_name.md]` as required by the librarian persona.

[Source: IMPLEMENTATION_SUMMARY.md]

---

## ⚙️ 7. Configuration Layer (`mcp_server/config/`)

### Settings (`settings.py`)

Centralized configuration with environment variable support.

```python
# From settings.py (lines 14-35)
class Settings:
    """Configuration settings for the Librarian MCP Server."""
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    
    SAFE_DIR = os.getenv("LIBRARIAN_SAFE_DIR", str(Path.home()))
    DOCUMENTS_DIR = os.getenv("LIBRARIAN_DOCUMENTS_DIR")
    CHROMA_PATH = os.getenv("LIBRARIAN_CHROMA_PATH")
    METADATA_PATH = os.getenv("LIBRARIAN_METADATA_PATH")
    
    # Backend selection
    BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chroma")
    
    # Document processing
    MAX_DOCUMENT_SIZE = int(os.getenv("LIBRARIAN_MAX_DOCUMENT_SIZE", "10000000"))  # 10MB
    CHUNK_SIZE = int(os.getenv("LIBRARIAN_CHUNK_SIZE", "1000"))
    
    DEFAULT_EXTENSIONS: Set[str] = {
        ".md", ".txt", ".py", ".js", ".ts", 
        ".json", ".yaml", ".yml", ".toml", ".rst", ".html"
    }
    
    # Security
    MAX_OUTPUT_CHARS = int(os.getenv("LIBRARIAN_MAX_OUTPUT_CHARS", "8000"))
    COMMAND_TIMEOUT = int(os.getenv("LIBRARIAN_COMMAND_TIMEOUT", "15"))
```

[Source: settings.py]

---

## 🔄 Data Flow: How a Search Query Works

Here's the complete flow from user query to response:

```
1. User Query → FastMCP Tool Call (search_library)
   └─> librarian_mcp.py (entry point)

2. search_library() in library_tools.py
   ├─> get_backend() → ChromaBackend
   ├─> backend.query(query_text, limit=5)
   │   └─> ChromaDB semantic search with vector embeddings
   └─> get_ai_layer() → DefaultAILayer

3. AI Layer Aggregation (ai_layer_interface.py)
   ├─> Sort results by similarity score
   ├─> Build response from top 5 chunks
   └─> Generate citations with document names

4. Return Response to User
   └─> Format: "Found X relevant chunks.\n\n[Response]\n\n**Sources:**\n[Citations]"
```

[Source: library_tools.py, ai_layer_interface.py]

---

## 🔒 Security Architecture Summary

The MCP server implements **multiple layers of security**:

1. **Ignore Patterns** (`ignore_patterns.py`): 94 exclusion patterns for sensitive files
2. **Command Whitelisting** (`cli_tools.py`): Only approved binaries can execute
3. **Path Validation** (`cli_tools.py`): Prevents directory traversal attacks
4. **Output Truncation** (`cli_tools.py`): Limits output to 8000 chars
5. **Dangerous Flag Blocking** (`cli_tools.py`): Blocks dangerous command combinations
6. **File Size Limits** (`document_manager.py`): Maximum 10MB per document
7. **Extension Whitelisting** (`cli_tools.py`): Only supported document types

[Source: cli_tools.py, ignore_patterns.py, document_manager.py]

---

## 📊 Summary of Key Python Files

| File | Purpose | Lines | Key Features |
|------|---------|-------|--------------|
| `librarian_mcp.py` | Entry point | 123 | FastMCP server, tool registration |
| `library_tools.py` | Library tools | 352 | 7 tools, lazy initialization pattern |
| `cli_tools.py` | CLI tools | 417 | 6 tools, multi-layer security |
| `document_manager.py` | Core logic | 410 | Lifecycle management, change detection |
| `metadata_store.py` | Metadata tracking | 154 | JSON-based persistence |
| `ignore_patterns.py` | Security exclusions | 185 | Gitignore-style matching |
| `chroma_backend.py` | Vector storage | 271 | ChromaDB integration, chunking |
| `base.py` | Backend interface | 48 | Abstract base class |
| `ai_layer_interface.py` | Result synthesis | 136 | Citation generation |
| `settings.py` | Configuration | 57 | Environment variable support |

[Source: All Python files in mcp_server/ directory]

---

This architecture provides a **production-ready, secure MCP server** with complete document lifecycle management, semantic search capabilities, and robust security boundaries. The design follows **separation of concerns**, uses **dependency injection**, and supports **future extensibility** (e.g., Phase 2 Chonkie integration).

---
## qwen3.5 4b 4 bit

# How the MCP Server Works - Deep Technical Analysis

Based on my analysis of the Python programs in the system, here's a comprehensive explanation of how the Librarian MCP Server works, with citations to the actual source code.

---

## 🏗️ **Overall Architecture**

The Librarian MCP Server is a unified server that provides AI models with two main capabilities:
1. **Library Tools** - Semantic document search and management via ChromaDB
2. **CLI Tools** - Secure command execution and file access

The architecture follows a **layered design** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server (FastMCP)                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  librarian_mcp.py (Entry Point)                      │  │
│  │  - Parses arguments                                 │  │
│  │  - Creates FastMCP instance                         │  │
│  │  - Registers library tools                          │  │
│  │  - Registers CLI tools                              │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Tools Layer (mcp_server/tools/)                     │  │
│  │  - library_tools.py (7 tools)                       │  │
│  │  - cli_tools.py (6 tools)                           │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Core Layer (mcp_server/core/)                       │  │
│  │  - document_manager.py (lifecycle management)        │  │
│  │  - metadata_store.py (change tracking)               │  │
│  │  - ignore_patterns.py (security filtering)           │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Backend Layer (mcp_server/backend/)                 │  │
│  │  - base.py (abstract interface)                      │  │
│  │  - chroma_backend.py (ChromaDB implementation)       │  │
│  │  - chonkie_backend.py (Phase 2 - intelligent chunking)│  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  AI Layer (mcp_server/ai_layer/)                     │  │
│  │  - ai_layer_interface.py (result aggregation)        │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Config Layer (mcp_server/config/)                   │  │
│  │  - settings.py (centralized configuration)           │  │
│  │  - librarian_prompt.py (system prompt)               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 **Key Component Analysis**

### **1. Entry Point: `librarian_mcp.py`**

This is the main server entry point that initializes the FastMCP server:

```python
#!/usr/bin/env python3
"""
Librarian MCP Server - Unified librarian and CLI access server.
"""
import sys
import argparse
from pathlib import Path

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: fastmcp not installed. Run: pip install fastmcp")
    sys.exit(1)

from mcp_server.tools.library_tools import register_library_tools
from mcp_server.tools.cli_tools import register_cli_tools
from mcp_server.config.librarian_prompt import get_librarian_instructions

def main():
    args = parse_arguments()
    
    # Update settings from command line arguments
    settings.Settings.SAFE_DIR = args.safe_dir
    settings.Settings.DOCUMENTS_DIR = args.documents_dir
    settings.Settings.CHROMA_PATH = args.chroma_path
    settings.Settings.METADATA_PATH = args.metadata_path
    
    # Create MCP server with librarian persona
    instructions = get_librarian_instructions(...)
    
    mcp = FastMCP("librarian-mcp", instructions=instructions)
    
    # Register tool groups
    register_library_tools(mcp)
    register_cli_tools(mcp, args.safe_dir)
    
    # Run server
    mcp.run()
```

**Key Points:**
- Uses **FastMCP** as the base framework for MCP protocol compliance
- Accepts command-line arguments for configurable paths
- Loads system prompt from `librarian_prompt.py`
- Registers both library and CLI tool groups
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py`](file:///home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py)

---

### **2. Backend Abstraction Layer**

The backend layer provides **extensible storage** with an abstract interface:

#### **Base Interface (`base.py`)**

```python
class DocumentBackend(ABC):
    """Abstract base class for document backends."""
    
    @abstractmethod
    def chunk_documents(documents, document_ids, source) -> List[Dict]:
        """Process documents into chunks with embeddings."""
        pass
    
    @abstractmethod
    def query(query_text: str, limit: int = 5) -> List[Dict]:
        """Perform semantic search."""
        pass
    
    @abstractmethod
    def delete_documents(document_id: str):
        """Remove all chunks for a document."""
        pass
    
    @abstractmethod
    def get_stats() -> Dict:
        """Get backend statistics."""
        pass
```

**Key Points:**
- Abstract base class defines the interface for all backends
- Supports **pluggable architecture** - can swap backends without changing tool code
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/base.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/base.py)

#### **Factory Pattern (`factory.py`)**

```python
def get_backend(backend_type: str = "chroma", **kwargs) -> 'DocumentBackend':
    """Get configured backend instance."""
    if backend_type == "chonkie":
        from .chonkie_backend import ChonkieBackend
        return ChonkieBackend(**kwargs)
    elif backend_type == "chroma":
        from .chroma_backend import ChromaBackend
        return ChromaBackend(**kwargs)
    else:
        raise ValueError(f"Unsupported backend type: {backend_type}")
```

**Key Points:**
- Factory pattern enables easy backend selection
- Backend type is configurable via environment variable `LIBRARIAN_BACKEND`
- Supports both **ChromaDB** (current) and **Chonkie** (Phase 2)
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/factory.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/factory.py)

#### **ChromaDB Implementation (`chroma_backend.py`)**

```python
class ChromaBackend(DocumentBackend):
    """ChromaDB backend for document storage and retrieval."""
    
    def __init__(self, collection_name: str = None, db_path: str = None):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(anonymized_telemetry=False, allow_reset=True)
        )
        self._ensure_collection()
    
    def chunk_documents(self, documents, document_ids, source):
        # Simple sentence-based chunking
        chunks = self._chunk_text(doc_text)
        
        for chunk_idx, chunk_text in enumerate(chunks):
            chunk_id = f"{doc_id}-chunk-{chunk_idx}"
            metadata = {
                "chunk_index": chunk_idx,
                "document_id": doc_id,
                "document_name": source
            }
            
            collection.add(
                documents=[chunk_text],
                ids=[chunk_id],
                metadatas=[metadata]
            )
    
    def query(self, query_text: str, limit: int = 5) -> List[Dict]:
        # Perform semantic search with ChromaDB
        results = collection.query(query_texts=[query_text], n_results=limit)
        
        # Format results with similarity scores
        formatted = []
        for i, doc in enumerate(docs):
            formatted.append({
                "chunk_id": ids[i],
                "text": doc,
                "metadata": metadatas[i],
                "similarity_score": 1 / (distances[i] + 1e-8),
                "rank": i + 1
            })
    
    def delete_documents(self, document_id: str):
        # Remove all chunks for this document
        to_delete = [chunk_id for chunk_id in all_chunks.get('ids', [])
                     if chunk_id.startswith(f"{document_id}-chunk-")]
        collection.delete(ids=to_delete)
```

**Key Points:**
- Uses **ChromaDB PersistentClient** for local vector database
- Implements **sentence-based chunking** (currently simple, will be replaced by Chonkie)
- Returns results with **similarity scores** for ranking
- Supports **metadata** for document tracking
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/chroma_backend.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/chroma_backend.py)

#### **Chonkie Implementation (`chonkie_backend.py`)**

```python
class ChonkieBackend(ChromaBackend):
    """Backend using Chonkie for intelligent chunking."""
    
    def __init__(self, collection_name: str = None, db_path: str = None,
                 chunk_size: int = 1000, min_chunk_size: int = 50):
        super().__init__(collection_name, db_path)
        
        # Initialize Chonkie chunker
        self.chunker = RecursiveChunker(
            chunk_size=chunk_size,
            min_characters_per_chunk=min_chunk_size
        )
    
    def chunk_documents(self, documents, document_ids, source):
        # Use Chonkie for intelligent chunking
        chonkie_chunks = self.chunker(doc_text)
        
        for chunk_idx, chunk in enumerate(chonkie_chunks):
            chunk_id = f"{doc_id}-chunk-{chunk_idx}"
            metadata = {
                "chunk_index": chunk_idx,
                "document_id": doc_id,
                "document_name": source,
                "token_count": chunk.token_count,
                "char_count": len(chunk.text),
                "chunking_method": "chonkie_recursive"
            }
            
            collection.add(documents=[chunk.text], ids=[chunk_id], metadatas=[metadata])
```

**Key Points:**
- Inherits from `ChromaBackend` for shared functionality
- Uses **Chonkie's RecursiveChunker** for intelligent chunking
- Adds metadata about **token count** and **character count**
- Provides **semantic-aware chunking** that respects document structure
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/chonkie_backend.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/chonkie_backend.py)

---

### **3. Document Manager (`document_manager.py`)**

The document manager handles the complete document lifecycle:

```python
class DocumentManager:
    """Manages document lifecycle: discovery, ingestion, updates, removal."""
    
    def __init__(self, backend, metadata_store, ignore_patterns):
        self.backend = backend
        self.metadata = metadata_store
        self.ignore_patterns = ignore_patterns
    
    def discover_documents(self, path, extensions, recursive):
        """Discover all documents in a directory."""
        # Use rglob for recursive search
        documents.extend(path.rglob(f"*{ext}"))
        
        # Filter out ignored files
        if self.ignore_patterns:
            documents = self.ignore_patterns.filter_paths(documents)
        
        return documents
    
    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def add_document(self, file_path: Path, source):
        """Add a single document to the library."""
        # Check file size
        if file_path.stat().st_size > settings.MAX_DOCUMENT_SIZE:
            return {"status": "error", "error": "Document exceeds max size"}
        
        # Read document
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Calculate checksum
        file_meta = self.get_file_metadata(file_path)
        
        # Check if already exists (using checksum)
        existing = self.metadata.get_by_path(str(file_path))
        if existing and existing['checksum'] == file_meta['checksum']:
            return {"status": "unchanged", "document_id": existing['document_id']}
        
        # Add to backend
        doc_id = file_meta['checksum'][:16]  # Use first 16 chars as ID
        chunks = self.backend.chunk_documents([content], [doc_id], source)
        
        # Store metadata
        self.metadata.add({
            "document_id": doc_id,
            "path": str(file_path),
            "name": file_meta['name'],
            "checksum": file_meta['checksum'],
            "size": file_meta['size'],
            "chunk_count": len(chunks),
            "indexed_at": datetime.now().isoformat()
        })
    
    def remove_document(self, document_id: str):
        """Remove a document and all its chunks."""
        self.backend.delete_documents(document_id)
        self.metadata.delete(document_id)
        return True
    
    def sync_directory(self, path, extensions, recursive):
        """Sync a directory: add new, update changed, remove deleted."""
        # Discover documents
        documents = self.discover_documents(path, extensions, recursive)
        
        # Process each document
        for doc_path in documents:
            result = self.add_document(doc_path)
            # Check for changes
            if result['status'] == 'unchanged':
                # Update metadata
                self.metadata.update(doc_id, new_data)
```

**Key Points:**
- **Lazy initialization** of backend, metadata store, and ignore patterns
- Uses **SHA-256 checksums** for change detection
- Supports **recursive discovery** with extension filtering
- Applies **ignore patterns** (from `.librarianignore`) to filter files
- Returns status dictionaries: `{'status': 'added|unchanged|error', ...}`
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/core/document_manager.py`](file:///home/peter/development/librarian-mcp/mcp_server/core/document_manager.py)

---

### **4. Metadata Store (`metadata_store.py`)**

Tracks which documents have been processed:

```python
class MetadataStore:
    """Stores document metadata for change tracking."""
    
    def __init__(self, metadata_path: str = None):
        self.metadata_path = Path(metadata_path or settings.METADATA_PATH)
        self.index_file = self.metadata_path / "index.json"
        self._index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load index from disk."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def add(self, metadata: Dict):
        """Add document metadata."""
        if 'document_id' not in metadata:
            raise ValueError("Metadata must contain 'document_id'")
        
        self._index[metadata['document_id']] = metadata
        self._save_index()
    
    def get(self, document_id: str) -> Optional[Dict]:
        """Get metadata by document ID."""
        return self._index.get(document_id)
    
    def get_by_path(self, path: str) -> Optional[Dict]:
        """Get metadata by file path."""
        normalized_path = str(Path(path).resolve())
        for doc in self._index.values():
            if Path(doc.get('path', '')).resolve() == Path(normalized_path).resolve():
                return doc
        return None
    
    def delete(self, document_id: str):
        """Remove document metadata."""
        if document_id in self._index:
            del self._index[document_id]
            self._save_index()
    
    def get_all(self) -> List[Dict]:
        """Get all indexed documents."""
        return list(self._index.values())
    
    def update(self, document_id: str, metadata: Dict):
        """Update document metadata."""
        if document_id in self._index:
            self._index[document_id].update(metadata)
            self._save_index()
```

**Key Points:**
- Stores metadata in **JSON format** (`metadata/index.json`)
- Supports **get by path** for change detection
- Provides **backup before clearing** (safety feature)
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/core/metadata_store.py`](file:///home/peter/development/librarian-mcp/mcp_server/core/metadata_store.py)

---

### **5. Ignore Patterns (`ignore_patterns.py`)**

Security layer that filters out sensitive files:

```python
class IgnorePatterns:
    """Manages and applies ignore patterns (gitignore-style)."""
    
    def __init__(self, root_path: str = None, ignore_file: str = ".librarianignore"):
        self.root_path = Path(root_path or settings.PROJECT_ROOT).resolve()
        self.ignore_file_path = self.root_path / ignore_file
        self.patterns: List[str] = []
        self.negation_patterns: List[str] = []
        
        self._load_patterns()
    
    def _load_patterns(self):
        """Load patterns from the ignore file."""
        if not self.ignore_file_path.exists():
            # Use default patterns
            self.patterns = [
                "venv/", ".venv/", "virtualenv/",
                "__pycache__/", "*.pyc", "*.pyo",
                "node_modules/", ".git/",
                "*.egg-info/", ".eggs/", "dist/", "build/",
                ".env", "*.env", "credentials.*", "*.key", "*.pem",
                "chroma_db/", "metadata/",
                "*.log", "*.tmp", "logs/", "tmp/",
                ".DS_Store", "Thumbs.db",
                "*.sqlite", "*.db", "*.sqlite3"
            ]
            return
        
        # Load from .librarianignore file
        with open(self.ignore_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith('!'):
                    self.negation_patterns.append(line[1:])  # Negation
                else:
                    self.patterns.append(line)
    
    def is_ignored(self, file_path: Path) -> bool:
        """Check if a file path matches any ignore pattern."""
        file_path = file_path.resolve()
        rel_path = str(file_path.relative_to(self.root_path))
        
        # Check negation patterns first (exceptions to ignore rules)
        for pattern in self.negation_patterns:
            if self._matches_pattern(rel_path, pattern):
                return False  # Explicitly NOT ignored
        
        # Check ignore patterns
        for pattern in self.patterns:
            if self._matches_pattern(rel_path, pattern):
                return True  # Ignored
        
        return False
    
    def filter_paths(self, paths: List[Path]) -> List[Path]:
        """Filter a list of paths, removing ignored ones."""
        return [p for p in paths if not self.is_ignored(p)]
```

**Key Points:**
- Uses **gitignore-style patterns** (supports wildcards, negation)
- Loads patterns from **`.librarianignore`** file
- Has **94 built-in exclusion patterns** for security
- Supports **negation patterns** (exceptions to rules)
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/core/ignore_patterns.py`](file:///home/peter/development/librarian-mcp/mcp_server/core/ignore_patterns.py)

---

### **6. Library Tools (`library_tools.py`)**

MCP tools for library operations:

```python
def register_library_tools(mcp):
    """Register all library tools with the MCP server."""
    
    @mcp.tool()
    def search_library(query: str, limit: int = 5) -> str:
        """Search the library semantically and return aggregated results."""
        backend = get_backend()
        ai_layer = get_ai_layer()
        
        # Query backend
        results = backend.query(query_text=query, limit=limit)
        
        # Aggregate results with citations
        aggregated = ai_layer.aggregate_results(results, query)
        
        response = f"Found {aggregated['num_chunks']} relevant chunks.\n\n"
        response += aggregated['response']
        
        if aggregated.get('citations'):
            response += "\n\n**Sources:**\n" + "\n".join(aggregated['citations'])
        
        return response
    
    @mcp.tool()
    def sync_documents(path: str, extensions: str = None, recursive: bool = True) -> str:
        """Sync all documents from a directory into the library."""
        doc_manager = get_doc_manager()
        
        ext_set = set(e.strip() for e in extensions.split(',')) if extensions else None
        
        results = doc_manager.sync_directory(path, ext_set, recursive)
        
        report = [
            f"Sync completed for directory: {path}",
            f"  Added: {results['added']}",
            f"  Updated: {results['updated']}",
            f"  Unchanged: {results['unchanged']}",
            f"  Removed: {results['removed']}",
        ]
        
        if results.get('ignored', 0) > 0:
            report.append(f"  Ignored: {results['ignored']} (excluded by .librarianignore)")
        
        return "\n".join(report)
    
    @mcp.tool()
    def add_document(path: str) -> str:
        """Add a single document to the library."""
        doc_manager = get_doc_manager()
        result = doc_manager.add_document(Path(path))
        
        if result['status'] == 'added':
            return f"Added document '{result['name']}' with {result['chunk_count']} chunks."
        elif result['status'] == 'unchanged':
            return f"Document already exists and is unchanged."
        elif result['status'] == 'error':
            return f"Failed to add document: {result.get('error', 'Unknown error')}"
    
    @mcp.tool()
    def remove_document(document_id: str) -> str:
        """Remove a document and all its chunks from the library."""
        doc_manager = get_doc_manager()
        if doc_manager.remove_document(document_id):
            return f"Removed document {document_id}"
        else:
            return f"Failed to remove document {document_id}"
    
    @mcp.tool()
    def list_indexed_documents() -> str:
        """List all documents currently indexed in the library."""
        doc_manager = get_doc_manager()
        documents = doc_manager.list_indexed()
        
        if not documents:
            return "No documents indexed in the library."
        
        lines = [f"Total indexed documents: {len(documents)}\n"]
        for doc in sorted(documents, key=lambda x: x.get('indexed_at', ''), reverse=True):
            lines.append(f"  • {doc.get('name', 'Unknown')}")
            lines.append(f"    ID: {doc.get('document_id', 'N/A')}")
            lines.append(f"    Path: {doc.get('path', 'N/A')}")
            lines.append(f"    Chunks: {doc.get('chunk_count', 0)}")
            lines.append(f"    Size: {doc.get('size', 0):,} bytes")
            lines.append(f"    Indexed: {doc.get('indexed_at', 'N/A')}")
            lines.append("")
        
        return "\n".join(lines)
    
    @mcp.tool()
    def get_document_status(path: str) -> str:
        """Check if a document is indexed and up-to-date."""
        doc_manager = get_doc_manager()
        status = doc_manager.get_document_status(path)
        
        if status['status'] == 'not_found':
            return f"File not found: {path}"
        elif status['status'] == 'not_indexed':
            return f"Document not indexed: {path}"
        elif status['status'] == 'current':
            return f"Document is current.\n  Name: {status.get('name', 'Unknown')}\n  ID: {status['document_id']}\n  Chunks: {status['chunk_count']}\n  Indexed: {status['indexed_at']}"
        elif status['status'] == 'outdated':
            return f"Document is outdated and needs updating: {path}"
```

**Key Points:**
- Uses **lazy initialization** pattern for backends, metadata, and document manager
- Implements **semantic search** with result aggregation
- Returns **citations** in the format `[Source: document_name.md]`
- Provides comprehensive **status reporting**
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/tools/library_tools.py`](file:///home/peter/development/librarian-mcp/mcp_server/tools/library_tools.py)

---

### **7. CLI Tools (`cli_tools.py`)**

MCP tools for CLI operations with security:

```python
def register_cli_tools(mcp, safe_dir: str):
    """Register all CLI tools with the MCP server."""
    global SAFE_WORKING_DIR
    SAFE_WORKING_DIR = safe_dir
    
    @mcp.tool()
    def execute_command(command: str, args: list[str] = [], cwd: str = None) -> str:
        """Execute a whitelisted command safely inside the allowed directory."""
        safe, reason = is_safe_command(command, args)
        if not safe:
            return f"[security error]\n{reason}"
        
        final_cwd = cwd if cwd else SAFE_WORKING_DIR
        real_final_cwd = os.path.realpath(final_cwd)
        safe_base_real = os.path.realpath(SAFE_WORKING_DIR)
        
        if not real_final_cwd.startswith(safe_base_real):
            return f"[security error]\nWorking directory must be inside {SAFE_WORKING_DIR}"
        
        full_cmd = [command] + args
        
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                cwd=final_cwd,
                timeout=DEFAULT_TIMEOUT_SECONDS,
                shell=False
            )
            
            output_text = ""
            if result.stdout:
                output_text += f"[stdout]\n{result.stdout}\n"
            if result.stderr:
                output_text += f"[stderr]\n{result.stderr}\n"
            output_text += f"[return code]\n{result.returncode}\n"
            
            return truncate_output(output_text) if output_text.strip() else "[no output]"
        except subprocess.TimeoutExpired:
            return f"[timeout]\nCommand timed out after {DEFAULT_TIMEOUT_SECONDS} seconds."
        except FileNotFoundError:
            return f"[error]\nCommand not found: {command}"
        except PermissionError:
            return f"[error]\nPermission denied for command: {command}"
        except Exception as e:
            return f"[error]\nExecution failed: {str(e)}"
    
    @mcp.tool()
    def read_document(path: str, start_line: int = None, end_line: int = None,
                     head: int = None, tail: int = None, max_chars: int = None) -> str:
        """Read contents of a document inside the allowed directory."""
        safe, resolved = is_safe_path(path, SAFE_WORKING_DIR)
        if not safe:
            return f"[security error]\n{resolved}"
        
        if not os.path.isfile(resolved):
            return f"[error]\nFile not found: {resolved}"
        
        ext = Path(resolved).suffix.lower()
        if ext not in DOCUMENT_EXTENSIONS:
            return f"[error]\nUnsupported file type: {ext}."
        
        try:
            with open(resolved, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            
            # Determine which lines to read
            if head is not None:
                selected_lines = lines[:head]
                range_info = f"(first {head} lines)"
            elif tail is not None:
                selected_lines = lines[-tail:] if tail > 0 else []
                range_info = f"(last {tail} lines)"
            elif start_line is not None or end_line is not None:
                start = start_line if start_line is not None else 1
                end = end_line if end_line is not None else len(lines)
                selected_lines = lines[start-1:end]
                range_info = f"(lines {start}-{end})"
            else:
                selected_lines = lines
                range_info = f"(all {len(lines)} lines)"
            
            selected_text = "".join(selected_lines)
            if max_chars and len(selected_text) > max_chars:
                selected_text = selected_text[:max_chars] + "\n[output truncated]"
            
            return selected_text + range_info
```

**Key Points:**
- **Security features**:
  - Command **whitelisting** (only approved binaries allowed)
  - **Directory sandboxing** (all operations in `SAFE_WORKING_DIR`)
  - **Timeout protection** (15s default)
  - **Output truncation** (8000 chars max)
  - **Dangerous flag blocking** (prevents misuse of safe commands)
- **File reading** supports line ranges, head, tail, and max chars
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/tools/cli_tools.py`](file:///home/peter/development/librarian-mcp/mcp_server/tools/cli_tools.py)

---

### **8. AI Layer (`ai_layer_interface.py`)**

Handles query formatting and result aggregation:

```python
class AILayer(ABC):
    """Abstract base class for AI-powered document processing."""
    
    @abstractmethod
    def format_query(raw_query: str, context: Dict = None) -> Dict:
        """Transform user query into optimized search parameters."""
        pass
    
    @abstractmethod
    def aggregate_results(chunks: List[Dict], query: str = None) -> Dict:
        """Synthesize multiple chunk results into coherent response."""
        pass
    
    @abstractmethod
    def build_context(user_intent: str) -> Dict:
        """Determine optimal chunks based on inferred user intent."""
        pass


class DefaultAILayer(AILayer):
    """Basic AI layer that synthesizes search results for AI consumption."""
    
    def format_query(self, raw_query: str, context: Dict = None) -> Dict:
        """Format query for search."""
        return {
            "text": raw_query.strip(),
            "type": "semantic",
            "limit": 5,
            **(context or {})
        }
    
    def aggregate_results(self, chunks: List[Dict], query: str = None) -> Dict:
        """Aggregate search results into coherent response."""
        if not chunks:
            return {
                "response": "No relevant documents found for your query.",
                "num_chunks": 0,
                "citations": []
            }
        
        # Sort by rank and take top chunks
        top_chunks = sorted(chunks, key=lambda x: x.get("rank", 999))[:5]
        
        # Build response from chunk texts
        response_parts = []
        for i, chunk in enumerate(top_chunks):
            text = chunk.get("text", "")
            if len(text) > 500:
                text = text[:500] + "..."
            
            response_parts.append(f"[{i+1}] {text}")
        
        response = "\n\n".join(response_parts)
        
        # Build citations list with document names
        citations = []
        for i, chunk in enumerate(top_chunks):
            metadata = chunk.get("metadata", {})
            doc_name = metadata.get("document_name", "Unknown Document")
            score = chunk.get("similarity_score", 0)
            citations.append(f"[{i+1}] {doc_name} (Relevance: {score:.2f})")
        
        return {
            "response": response,
            "citations": citations,
            "num_chunks": len(chunks),
            "top_results": [chunk.get("chunk_id", "") for chunk in top_chunks]
        }
    
    def build_context(self, user_intent: str) -> Dict:
        """Build context for search."""
        return {
            "depth": 1,
            "breadth": 3
        }
```

**Key Points:**
- Implements **abstract interface** for extensibility
- **Aggregates results** with citations
- Truncates long chunks to **500 characters**
- Returns **similarity scores** for ranking
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/ai_layer/ai_layer_interface.py`](file:///home/peter/development/librarian-mcp/mcp_server/ai_layer/ai_layer_interface.py)

---

### **9. Configuration (`settings.py`)**

Centralized configuration:

```python
class Settings:
    """Configuration settings for the Librarian MCP Server."""
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    
    # Safe directory for CLI operations (can be overridden via CLI args or env)
    SAFE_DIR = os.getenv("LIBRARIAN_SAFE_DIR", str(Path.home()))
    
    # Document storage
    DOCUMENTS_DIR = os.getenv("LIBRARIAN_DOCUMENTS_DIR", str(PROJECT_ROOT / "documents"))
    
    # ChromaDB
    CHROMA_PATH = os.getenv("LIBRARIAN_CHROMA_PATH", str(PROJECT_ROOT / "chroma_db"))
    CHROMA_COLLECTION = os.getenv("LIBRARIAN_CHROMA_COLLECTION", "documents")
    
    # Metadata storage
    METADATA_PATH = os.getenv("LIBRARIAN_METADATA_PATH", str(PROJECT_ROOT / "metadata"))
    
    # Backend selection
    BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chroma")
    
    # Chonkie (Phase 2)
    CHONKIE_URL = os.getenv("LIBRARIAN_CHONKIE_URL", "http://localhost:8000")
    
    # Document processing
    MAX_DOCUMENT_SIZE = int(os.getenv("LIBRARIAN_MAX_DOCUMENT_SIZE", "10000000"))  # 10MB
    CHUNK_SIZE = int(os.getenv("LIBRARIAN_CHUNK_SIZE", "1000"))
    
    # Allowed document extensions
    DEFAULT_EXTENSIONS: Set[str] = {".md", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".rst", ".html"}
    
    # Security
    MAX_OUTPUT_CHARS = int(os.getenv("LIBRARIAN_MAX_OUTPUT_CHARS", "8000"))
    COMMAND_TIMEOUT = int(os.getenv("LIBRARIAN_COMMAND_TIMEOUT", "15"))
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        Path(cls.DOCUMENTS_DIR).mkdir(parents=True, exist_ok=True)
        Path(cls.CHROMA_PATH).mkdir(parents=True, exist_ok=True)
        Path(cls.METADATA_PATH).mkdir(parents=True, exist_ok=True)
```

**Key Points:**
- Uses **environment variables** for configuration
- Supports **override via command-line arguments**
- Creates required directories automatically
- **Citation**: [Source: `/home/peter/development/librarian-mcp/mcp_server/config/settings.py`](file:///home/peter/development/librarian-mcp/mcp_server/config/settings.py)

---

## 🔄 **Data Flow Summary**

### **Document Ingestion Flow:**

1. **Discovery**: `DocumentManager.discover_documents()` scans directory
2. **Filtering**: `IgnorePatterns.filter_paths()` removes excluded files
3. **Reading**: `DocumentManager.add_document()` reads file content
4. **Checksum**: `calculate_checksum()` computes SHA-256 hash
5. **Comparison**: Checksum compared against existing metadata
6. **Chunking**: `ChromaBackend.chunk_documents()` splits into chunks
7. **Embedding**: ChromaDB creates vector embeddings
8. **Storage**: Chunks stored in ChromaDB collection
9. **Metadata**: Document metadata saved to JSON file
10. **Response**: Status returned to user

### **Search Flow:**

1. **Query**: User provides search query
2. **Format**: `DefaultAILayer.format_query()` prepares query
3. **Backend**: `ChromaBackend.query()` performs semantic search
4. **Results**: Top 5 chunks returned with similarity scores
5. **Aggregate**: `DefaultAILayer.aggregate_results()` synthesizes response
6. **Citations**: Document names and scores included
7. **Response**: Formatted response returned to user

---

## 📋 **Summary of Key Python Programs**

| File | Purpose | Key Features |
|------|---------|--------------|
| `librarian_mcp.py` | Server entry point | FastMCP instance, tool registration |
| `base.py` | Abstract interface | DocumentBackend ABC class |
| `factory.py` | Backend factory | Pluggable backend selection |
| `chroma_backend.py` | ChromaDB backend | Vector storage, sentence chunking |
| `chonkie_backend.py` | Chonkie backend | Intelligent chunking (Phase 2) |
| `document_manager.py` | Lifecycle management | Discovery, add, update, remove, sync |
| `metadata_store.py` | Change tracking | JSON-based metadata storage |
| `ignore_patterns.py` | Security filtering | Gitignore-style pattern matching |
| `ai_layer_interface.py` | Result aggregation | Citation generation, response synthesis |
| `settings.py` | Configuration | Environment variables, defaults |
| `library_tools.py` | Library tools | 7 MCP tools for document management |
| `cli_tools.py` | CLI tools | 6 MCP tools with security |

---

## 🔒 **Security Implementation**

The server implements multiple security layers:

1. **Directory Sandboxing**: All CLI operations restricted to `SAFE_WORKING_DIR`
2. **Command Whitelisting**: Only approved binaries can be executed
3. **Path Validation**: Prevents directory traversal attacks
4. **Timeout Protection**: Commands terminate after timeout
5. **Output Truncation**: Protects LLM context window
6. **Dangerous Flag Blocking**: Prevents misuse of safe commands
7. **File Size Limits**: Maximum document size enforced
8. **Extension Whitelisting**: Only supported document types allowed
9. **Ignore Patterns**: 94+ exclusion patterns for sensitive files

---

## 🎯 **How It All Works Together**

The Librarian MCP Server operates as follows:

1. **Initialization**: `librarian_mcp.py` creates FastMCP instance and registers tools
2. **Configuration**: Settings loaded from environment variables
3. **Lazy Initialization**: Backend, metadata, and document manager created on first use
4. **Tool Execution**: User invokes MCP tool → Python function called → Backend processed → Result returned
5. **Response Formatting**: AI layer aggregates results with citations
6. **Security Enforcement**: Ignore patterns and security checks applied throughout

The architecture is designed for **extensibility** (new backends, new tools) and **maintainability** (clear separation of concerns, lazy initialization, abstraction layers).

---

**Sources Referenced:**
- [Source: `/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py`](file:///home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/base.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/base.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/factory.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/factory.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/chroma_backend.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/chroma_backend.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/backend/chonkie_backend.py`](file:///home/peter/development/librarian-mcp/mcp_server/backend/chonkie_backend.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/core/document_manager.py`](file:///home/peter/development/librarian-mcp/mcp_server/core/document_manager.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/core/metadata_store.py`](file:///home/peter/development/librarian-mcp/mcp_server/core/metadata_store.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/core/ignore_patterns.py`](file:///home/peter/development/librarian-mcp/mcp_server/core/ignore_patterns.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/ai_layer/ai_layer_interface.py`](file:///home/peter/development/librarian-mcp/mcp_server/ai_layer/ai_layer_interface.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/config/settings.py`](file:///home/peter/development/librarian-mcp/mcp_server/config/settings.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/tools/library_tools.py`](file:///home/peter/development/librarian-mcp/mcp_server/tools/library_tools.py)
- [Source: `/home/peter/development/librarian-mcp/mcp_server/tools/cli_tools.py`](file:///home/peter/development/librarian-mcp/mcp_server/tools/cli_tools.py)
- 