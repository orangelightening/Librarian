
## Query how does the metadata_store.py work?

### glm-4.7 running in Jan as librarian in thinking mode

I'll search for information about metadata_store.py in the library and file system.
I found information about `metadata_store.py`. Let me read the full file to give you a complete explanation.
## Metadata Store Overview

`metadata_store.py` implements a **persistent document metadata tracking system** that records information about processed documents. It's used by the Document Manager to track which documents have been indexed, when they were last modified, and their processing status.

[Source: /home/peter/development/librarian-mcp/mcp_server/core/metadata_store.py]

---

## Core Components

### **Initialization**
```python
def __init__(self, metadata_path: str = None)
```
- Creates a metadata directory (defaults to `settings.METADATA_PATH`)
- Sets up an `index.json` file to store metadata
- Loads existing metadata from disk on startup

### **Storage Structure**
- Uses a simple JSON file (`index.json`) stored in the metadata directory
- Metadata is a dictionary where **document_id** is the key
- Automatically saves to disk after any modification

---

## Key Methods

| Method | Purpose |
|--------|---------|
| `add(metadata)` | Add new document metadata (requires `document_id`) |
| `get(document_id)` | Retrieve metadata by document ID |
| `get_by_path(path)` | Find metadata by file path (resolves paths for comparison) |
| `delete(document_id)` | Remove document from index |
| `update(document_id, metadata)` | Update existing metadata fields |
| `get_all()` | Return all indexed documents |
| `count()` | Get total number of indexed documents |
| `clear()` | Remove all metadata (with backup) |

---

## How Change Tracking Works

The metadata store supports **change detection** by storing:
- `document_id` - Unique identifier
- `path` - File path to the document
- `last_modified` - Timestamp of last change
- `sha256` - Hash of file contents for integrity checking
- Other custom metadata fields

When a file is processed, the system can:
1. Look up the file by path using `get_by_path()`
2. Compare the stored hash/last_modified with the current file
3. Decide whether to skip, update, or re-index

---

## Usage Example

```python
from mcp_server.core.metadata_store import MetadataStore

# Initialize store
store = MetadataStore()

# Add document metadata
store.add({
    'document_id': 'doc_123',
    'path': '/path/to/document.md',
    'last_modified': '2024-01-15T10:30:00',
    'sha256': 'abc123...'
})

# Lookup by path
metadata = store.get_by_path('/path/to/document.md')

# Update metadata
store.update('doc_123', {'last_modified': '2024-01-16T09:00:00'})

# Get all documents
all_docs = store.get_all()
```

---

## Integration

The MetadataStore is used by:
- **DocumentManager** - For document lifecycle management
- **Library tools** - For checking document status and managing updates

[Source: /home/peter/development/librarian-mcp/mcp_server/core/document_manager.py]

---

Would you like me to explain:
1. How it integrates with the DocumentManager for change detection?
2. What metadata fields are typically stored?
3. How the backup/clear mechanism works?

### qwen3.5 9b 4 bit quant running in lmstudio as librarian in thinking mode



### qwen3.5 4b 4 bit quant running in lmstudio as librarian in thinking mode



## Overview

The `MetadataStore` class is designed to **track processed documents** for change detection and lifecycle management in the MCP server. [Source: metadata_store.py]

## Core Functionality

### 1. **Initialization**
```python
def __init__(self, metadata_path: str = None):
```
- Creates a persistent metadata store using JSON files
- Initializes a metadata directory (defaults to `settings.METADATA_PATH`)
- Loads an existing index or creates a new empty one [Source: metadata_store.py]

### 2. **Data Persistence**
- Stores document metadata in `index.json` within the metadata path
- Automatically saves changes to disk after every operation [Source: metadata_store.py]

### 3. **Key Operations**

| Method | Purpose |
|--------|---------|
| `add(metadata)` | Add new document metadata (requires `document_id`) |
| `get(document_id)` | Retrieve metadata by document ID |
| `get_by_path(path)` | Find metadata by file path (path resolution) |
| `update(id, metadata)` | Update existing document metadata |
| `delete(document_id)` | Remove document from tracking |
| `get_all()` | List all tracked documents |
| `count()` | Get total number of indexed documents |
| `clear()` | Clear all metadata (with backup) | [Source: metadata_store.py]

## Architecture Pattern

The class follows a **singleton-like pattern** when used with the module-level `get_metadata()` function, which caches a single instance for the application lifetime. [Source: metadata_store.py]

## Use Cases

1. **Change Tracking**: Stores document hashes, timestamps, and paths to detect modifications
2. **Document Lifecycle Management**: Works with `DocumentManager` to handle ingestion, updates, and removals
3. **Integration with ChromaDB**: Provides metadata context for vector database operations [Source: metadata_store.py]

## Key Design Decisions

- **Path Resolution**: Normalizes paths using `Path.resolve()` before comparison
- **Error Handling**: Gracefully handles file I/O errors with informative print messages
- **Backup on Clear**: Creates `.json.bak` backup before clearing the entire index [Source: metadata_store.py]

Would you like me to show you how it integrates with `DocumentManager`, or would you like to see examples of the metadata structure stored in `index.json`?


### qwen3.5 4b 4 bit quant running in lmstudio as librarian in thinking mode
## How `metadata_store.py` Works

The `MetadataStore` class in `metadata_store.py` is responsible for **tracking processed documents** and managing their lifecycle metadata. Here's how it works:

### Core Purpose
```python
"""Metadata Store - Tracks processed documents."""
```
It maintains an index of document metadata for change tracking and lifecycle management.

### Key Features

**1. Storage Mechanism**
- Stores metadata in a JSON file (`index.json`) at the configured metadata path
- Uses a dictionary (`self._index`) to track document metadata
- Automatically creates the metadata directory if it doesn't exist

**2. Main Methods**

| Method | Purpose |
|--------|---------|
| `add(metadata)` | Add document metadata to the index |
| `get(document_id)` | Retrieve metadata by document ID |
| `get_by_path(path)` | Retrieve metadata by file path |
| `update(document_id, metadata)` | Update existing document metadata |
| `delete(document_id)` | Remove document metadata |
| `get_all()` | Get all indexed documents |
| `count()` | Get total number of indexed documents |
| `clear()` | Remove all metadata (with backup) |

**3. Important Constraints**
- All metadata must include a `document_id` field (otherwise raises ValueError)
- Path comparisons are normalized using `Path().resolve()` to handle path differences
- The `clear()` method backs up the existing index before clearing

### Usage Pattern
```python
from mcp_server.core.metadata_store import MetadataStore

# Get or create the metadata store
metadata = MetadataStore()

# Add a document
metadata.add({'document_id': 'abc123', 'path': '/path/to/file.md', 'status': 'indexed'})

# Get metadata
doc_info = metadata.get('abc123')

# Update metadata
metadata.update('abc123', {'status': 'updated'})

# Get all documents
all_docs = metadata.get_all()
```

This metadata store works in tandem with the `DocumentManager` class to track the complete document lifecycle: discovery, ingestion, updates, and removal.

Would you like me to show you how the DocumentManager uses this metadata store, or do you have other questions about the system?

## Query 2 more complex

Describe the interaction between the metadata_store.py and document_manager.py. Investigate any other connections and explain?

## GLM

I'll help you understand the interaction between metadata_store.py and document_manager.py. Let me start by searching the library for information about these files.
Based on my analysis of the codebase, I can now provide a comprehensive explanation of the interaction between `metadata_store.py` and `document_manager.py`, along with other connected components.

## Core Interaction: DocumentManager ↔ MetadataStore

### 1. **Dependency Relationship**
`DocumentManager` depends on `MetadataStore` as a core component. The relationship is established in the constructor:

```python
# From document_manager.py
def __init__(self, backend, metadata_store: MetadataStore = None, ignore_patterns: IgnorePatterns = None):
    self.backend = backend
    self.metadata = metadata_store or MetadataStore()  # Creates new if None
    self.ignore_patterns = ignore_patterns or IgnorePatterns()
```

[Source: /home/peter/development/librarian-mcp/mcp_server/core/document_manager.py]

### 2. **MetadataStore: The Data Layer**

`MetadataStore` provides persistent storage for document metadata with these key responsibilities:
- **Storage**: Maintains an in-memory index backed by a JSON file (`metadata/index.json`)
- **CRUD Operations**: Add, get, update, delete, and list document metadata
- **Change Detection**: Stores checksums to track document modifications
- **Query Methods**: Look up documents by ID or file path

[Source: /home/peter/development/librarian-mcp/mcp_server/core/metadata_store.py]

Key methods used by DocumentManager:
- `add()` - Stores new document metadata
- `get_by_path()` - Finds metadata by file path
- `get_all()` - Retrieves all indexed documents
- `delete()` - Removes metadata entries

### 3. **DocumentManager: The Business Logic Layer**

`DocumentManager` orchestrates document lifecycle operations and delegates metadata persistence to `MetadataStore`:

**Critical Interactions:**

#### **Adding Documents (`add_document`)**
```python
# Check if already exists
existing = self.metadata.get_by_path(str(file_path))
if existing:
    if existing['checksum'] == file_meta['checksum']:
        return {"status": "unchanged", ...}  # No change needed
    else:
        self.remove_document(existing['document_id'])  # Remove old version

# Add to backend, then store metadata
self.metadata.add({
    "document_id": doc_id,
    "path": str(file_path),
    "checksum": file_meta['checksum'],
    ...
})
```

[Source: /home/peter/development/librarian-mcp/mcp_server/core/document_manager.py]

#### **Removing Documents (`remove_document`)**
```python
# Remove from backend
self.backend.delete_documents(document_id)
# Remove metadata
self.metadata.delete(document_id)
```

[Source: /home/peter/development/librarian-mcp/mcp_server/core/document_manager.py]

#### **Syncing Directories (`sync_directory`)**
```python
# Get current metadata
indexed = self.metadata.get_all()
indexed_paths = {str(Path(doc['path']).resolve()) for doc in indexed}
# ... process documents ...
# Remove documents that no longer exist
for path in indexed_paths - current_paths:
    doc = self.metadata.get_by_path(path)
    if doc:
        self.remove_document(doc['document_id'])
```

[Source: /home/peter/development/librarian-mcp/mcp_server/core/document_manager.py]

#### **Checking Status (`get_document_status`)**
```python
indexed = self.metadata.get_by_path(str(file_path))
current_checksum = self.calculate_checksum(file_path)
if indexed['checksum'] == current_checksum:
    return {"status": "current", ...}
else:
    return {"status": "outdated", ...}
```

[Source: /home/peter/development/librarian-mcp/mcp_server/core/document_manager.py]

## Other Connections

### 4. **Integration Layer: library_tools.py**

The `library_tools.py` file acts as a bridge between the MCP server interface and the core components:

```python
def get_doc_manager():
    """Get or create document manager instance."""
    global _doc_manager
    if _doc_manager is None:
        _doc_manager = DocumentManager(get_backend(), get_metadata())
    return _doc_manager
```

[Source: /home/peter/development/librarian-mcp/mcp_server/tools/library_tools.py]

This pattern uses **lazy initialization** and **singleton pattern** to ensure only one instance of each component exists.

### 5. **IgnorePatterns Integration**

`DocumentManager` also depends on `IgnorePatterns` for filtering:

```python
def discover_documents(self, path: str, extensions: Set[str] = None, recursive: bool = True):
    documents = []
    # ... glob operations ...
    # Filter out ignored files
    if self.ignore_patterns:
        documents = self.ignore_patterns.filter_paths(documents)
    return documents
```

[Source: /home/peter/development/librarian-mcp/mcp_server/core/document_manager.py]

### 6. **Backend Integration**

`DocumentManager` requires a `backend` parameter (e.g., ChromaBackend) to perform:
- Document chunking
- Vector storage
- Search operations

The metadata store is independent of the backend choice, allowing flexibility.

## Data Flow Diagram

```
User Request (MCP Tool)
    ↓
library_tools.py (MCP interface)
    ↓
DocumentManager (business logic)
    ├─→ MetadataStore (metadata persistence)
    ├─→ Backend (document storage & search)
    └─→ IgnorePatterns (file filtering)
```

## Key Design Patterns

1. **Separation of Concerns**: 
   - `MetadataStore`: Pure metadata storage
   - `DocumentManager`: Business logic and orchestration
   - `Backend`: Vector storage and retrieval

2. **Dependency Injection**: Both `MetadataStore` and `IgnorePatterns` can be injected or auto-created

3. **Lazy Initialization**: Components are created only when needed via factory functions in `library_tools.py`

4. **Immutable Document IDs**: IDs are derived from checksums (first 16 chars), ensuring consistency

## External Usage

These components are used in:
- **Scripts**: `scripts/rebuild_library.py`, `scripts/ingest.py`
- **MCP Server**: Exposed via tools like `sync_documents`, `add_document`, `remove_document`

The architecture allows the system to efficiently track document changes, avoid redundant processing, and maintain consistency between the vector database and metadata store.


## Qwen3.5 9b
## Interaction Between `metadata_store.py` and `document_manager.py`

### Core Relationship

**`document_manager.py` is the orchestrator that uses `metadata_store.py` as its metadata persistence layer.**

[Source: document_manager.py]
```python
def __init__(self, backend, metadata_store: MetadataStore = None, ignore_patterns: IgnorePatterns = None):
    self.backend = backend
    self.metadata = metadata_store or MetadataStore()  # Creates new if None
    self.ignore_patterns = ignore_patterns or IgnorePatterns()
```

---

### Detailed Interaction Flow

#### **1. `metadata_store.py` - The Persistence Layer**

[Source: metadata_store.py]
- Stores document metadata in a JSON file (`index.json`) in the configured `METADATA_PATH` directory
- Provides CRUD operations for document metadata:
  - `add()` - Add new document metadata
  - `get()` / `get_by_path()` - Retrieve metadata by ID or path
  - `update()` - Update existing metadata
  - `delete()` - Remove document metadata
  - `clear()` - Clear all metadata with backup

#### **2. `document_manager.py` - The Lifecycle Manager**

[Source: document_manager.py]
- Uses `metadata_store` to track document state across operations
- Key interaction points:

**A. During Document Addition (`add_document`):**
```python
# Check if already exists using metadata store
existing = self.metadata.get_by_path(str(file_path))
if existing:
    if existing['checksum'] == file_meta['checksum']:
        # Unchanged - return existing doc_id
        pass
    else:
        # Changed - remove old version via metadata store
        self.remove_document(existing['document_id'])

# ... after processing, add new metadata
self.metadata.add({
    "document_id": doc_id,
    "path": str(file_path),
    "name": file_meta['name'],
    "checksum": file_meta['checksum'],
    "size": file_meta['size'],
    "modified": file_meta['modified'],
    "chunk_count": len(chunks),
    "indexed_at": datetime.now().isoformat()
})
```

**B. During Document Removal (`remove_document`):**
```python
# Remove from backend
self.backend.delete_documents(document_id)

# Remove metadata
self.metadata.delete(document_id)
```

---

### Other Connected Components

#### **3. `ignore_patterns.py` - File Filtering Layer**

[Source: ignore_patterns.py]
- Imported by `document_manager.py`:
  ```python
  from .metadata_store import MetadataStore
  from .ignore_patterns import IgnorePatterns
  ```
- Used in `discover_documents()` to filter out unwanted files before processing
- Creates a `.librarianignore` file with patterns like:
  - `venv/`, `.venv/`, `node_modules/`, `.git/`
  - Sensitive files: `.env`, `*.key`, `*.pem`, `credentials.*`

**Interaction Flow:**
```python
def discover_documents(self, path, extensions, recursive=True):
    # ... discover all files ...
    
    # Filter out ignored files
    if self.ignore_patterns:
        documents = self.ignore_patterns.filter_paths(documents)
    
    return documents
```

#### **4. Backend Layer (`chroma_backend.py` / `chonkie_backend.py`)**

[Source: backend/factory.py]
- Document Manager delegates chunking and storage to the backend
- Two backends supported: ChromaDB (current) and Chonkie (Phase 2)
- Backend receives document content from Manager, returns chunks

**Interaction Flow:**
```python
def add_document(self, file_path, source=None):
    # ... read file, calculate checksum ...
    
    # Add to backend
    doc_id = file_meta['checksum'][:16]
    chunks = self.backend.chunk_documents(
        documents=[content],
        document_ids=[doc_id],
        source=source_name
    )
    
    # Store metadata in MetadataStore
    self.metadata.add({...})
```

#### **5. Configuration (`settings.py`)**

[Source: settings.py]
- Provides configuration for all components:
  - `METADATA_PATH` - Directory where metadata_store.json files are stored
  - `CHROMA_PATH` - ChromaDB storage location
  - `DEFAULT_EXTENSIONS` - File extensions to process
  - `MAX_DOCUMENT_SIZE` - Size limit for documents

---

### Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    Document Manager (Orchestrator)           │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │ discover_documents│    │add_document      │               │
│  │ remove_document   │◄──►│ sync_directory   │               │
│  └──────────────────┘    └──────────────────┘               │
│         │                    │                               │
│         │ uses               │ uses                          │
│         ▼                    ▼                               │
│  ┌────────────────────┐  ┌────────────────────┐             │
│  │   Metadata Store    │  │      Backend       │             │
│  │ (JSON index.json)   │  │  (ChromaDB/        │             │
│  │ - Document IDs      │  │   Chonkie)         │             │
│  │ - Checksums         │  │ - Chunking         │             │
│  │ - Metadata          │  │ - Vector storage   │             │
│  └────────────────────┘  └────────────────────┘             │
│         │                    │                               │
│         │                    ▼                               │
│         └───────────► Ignore Patterns (File Filtering)       │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Metadata Store as Source of Truth** - Tracks document state, checksums, and lifecycle
2. **Document Manager as Orchestrator** - Coordinates all operations across components
3. **Backend Abstraction** - Allows swapping between ChromaDB and Chonkie backends
4. **Ignore Patterns for Security** - Filters sensitive files before processing

---

Would you like me to explore any specific interaction in more detail, such as the change detection mechanism or how the sync process works?


### qwen3.5 4b 


Based on my analysis of the codebase, here's a comprehensive explanation of how these two components interact:

---

### **Core Relationship: Dependency & Coordination**

**`document_manager.py` depends on `metadata_store.py`** - The DocumentManager uses MetadataStore to track document state and manage lifecycle.

---

### **Detailed Interaction Flow**

#### **1. Initialization**
```python
# document_manager.py: Line 18-21
def __init__(self, backend, metadata_store: MetadataStore = None, ...):
    self.backend = backend
    self.metadata = metadata_store or MetadataStore()  # Creates new if None
    self.ignore_patterns = ignore_patterns or IgnorePatterns()
```

**Connection:** DocumentManager receives a `MetadataStore` instance (or creates one), establishing the dependency.

---

#### **2. Document Addition with Checksum Validation**
**Flow:** `add_document()` → `get_file_metadata()` → `calculate_checksum()` → `metadata.add()`

```python
# document_manager.py: Lines 116-187
def add_document(self, file_path: Path, source: str = None) -> Dict:
    # Get file metadata including checksum
    file_meta = self.get_file_metadata(file_path)
    
    # Check if already exists
    existing = self.metadata.get_by_path(str(file_path))
    if existing:
        if existing['checksum'] == file_meta['checksum']:
            return {"status": "unchanged", ...}
        else:
            # Document changed, remove old version
            self.remove_document(existing['document_id'])
    
    # Add to backend
    doc_id = file_meta['checksum'][:16]
    
    # Store metadata in MetadataStore
    self.metadata.add({
        "document_id": doc_id,
        "path": str(file_path),
        "name": file_meta['name'],
        "checksum": file_meta['checksum'],
        "size": file_meta['size'],
        "modified": file_meta['modified'],
        "chunk_count": len(chunks),
        "indexed_at": datetime.now().isoformat()
    })
```

**Key Points:**
- MetadataStore tracks document state by **checksum** (SHA-256)
- Prevents duplicate documents with identical content
- Supports update detection (checksum mismatch triggers removal + re-add)

---

#### **3. Change Detection Mechanism**
**`get_document_status()`** uses MetadataStore to compare file metadata with stored metadata:

```python
# document_manager.py: Lines 189-230
def get_document_status(self, path: str) -> Dict:
    file_meta = self.get_file_metadata(path)
    stored = self.metadata.get_by_path(path)
    
    if not stored:
        return {"status": "not_indexed", ...}
    
    # Compare checksums
    if file_meta['checksum'] != stored['checksum']:
        return {"status": "outdated", ...}
    
    return {"status": "current", ...}
```

---

#### **4. Directory Sync with Metadata Tracking**
**`sync_directory()`** uses MetadataStore to detect additions, updates, and removals:

```python
# document_manager.py: Lines 232-290
def sync_directory(self, path: str, extensions: Set[str], recursive: bool):
    # Discover all documents
    documents = self.discover_documents(path, extensions, recursive)
    
    # Filter ignored files
    if self.ignore_patterns:
        documents = self.ignore_patterns.filter_paths(documents)
    
    # Process each document
    added = 0
    updated = 0
    unchanged = 0
    removed = 0
    errors = []
    
    for doc_path in documents:
        status = self.get_document_status(str(doc_path))
        
        if status['status'] == 'not_indexed' or status['status'] == 'outdated':
            # Add or update document
            result = self.add_document(doc_path)
            if result['status'] == 'added':
                added += 1
            elif result['status'] == 'unchanged':
                unchanged += 1
        else:
            # Check if file was deleted
            if not doc_path.exists():
                self.remove_document(status['document_id'])
                removed += 1
```

---

#### **5. Removal Operations**
```python
# document_manager.py: Lines 190-204
def remove_document(self, document_id: str) -> bool:
    # Remove from backend
    self.backend.delete_documents(document_id)
    
    # Remove metadata
    self.metadata.delete(document_id)
    
    return True
```

**Connection:** MetadataStore keeps track of document removals for cleanup.

---

### **Other Connected Components**

#### **1. `ignore_patterns.py`**
- **Imported by:** `document_manager.py` (Line 8)
- **Function:** Filters documents based on `.librarianignore` patterns
- **Integration:** Used in `discover_documents()` to exclude unwanted files

#### **2. `chroma_backend.py`**
- **Imported by:** `document_manager.py` (via `backend` parameter)
- **Function:** Stores document chunks and embeddings in ChromaDB
- **Integration:** 
  - `chunk_documents()` - Splits documents into searchable chunks
  - `query()` - Performs semantic search
  - `delete_documents()` - Removes chunks when document is removed

#### **3. `settings.py`**
- **Imported by:** Both modules
- **Function:** Configuration for paths, chunk sizes, allowed extensions
- **Connection:** Provides constants like `METADATA_PATH`, `CHUNK_SIZE`, `DEFAULT_EXTENSIONS`

#### **4. `ai_layer/ai_layer_interface.py`**
- **Imported by:** `library_tools.py`
- **Function:** Aggregates search results and builds citations
- **Connection:** Works with backend query results to provide user-facing responses

---

### **Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────┐
│                    User/CLI/MCP Tools                       │
│  (library_tools.py, cli_tools.py)                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      DocumentManager                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Methods: discover, add, remove, sync, status        │  │
│  └───────────────────┬──────────────────────────────────┘  │
│                      │                                     │
│  ┌───────────────────┴──────────────────────────────────┐  │
│  │  Backend (ChromaBackend)                             │  │
│  │  - chunk_documents()                                │  │
│  │  - query()                                          │  │
│  │  - delete_documents()                               │  │
│  └───────────────────┬──────────────────────────────────┘  │
│                      │                                     │
│  ┌───────────────────┴──────────────────────────────────┐  │
│  │  MetadataStore                                      │  │
│  │  - add() / get() / delete() / get_by_path()         │  │
│  │  - Tracks document state by checksum                │  │
│  └──────────────────────────────────────────────────────┘  │
│                      │                                     │
│  ┌───────────────────┴──────────────────────────────────┐  │
│  │  IgnorePatterns                                     │  │
│  │  - filter_paths()                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### **Key Design Patterns**

1. **Singleton Pattern:** Both `MetadataStore` and `DocumentManager` use lazy initialization via `get_metadata()` and `get_doc_manager()` in `library_tools.py`

2. **Dependency Injection:** `DocumentManager` receives `backend` and `metadata_store` as parameters, allowing flexible backend configuration

3. **Abstract Backend Interface:** `base.py` defines the `DocumentBackend` ABC, with `ChromaBackend` and `ChonkieBackend` as implementations

4. **Checksum-Based Deduplication:** Uses SHA-256 checksums to detect document changes without full content comparison

---

### **Summary**

The `metadata_store.py` and `document_manager.py` interact through a **cooperative lifecycle management** pattern:
- **MetadataStore** acts as the "source of truth" for document state
- **DocumentManager** orchestrates the workflow, using metadata to detect changes and manage document lifecycle
- Together with the backend and ignore patterns, they form a robust document ingestion and synchronization system

This architecture enables efficient change detection, deduplication, and automatic library synchronization while maintaining a clear separation of concerns between document lifecycle management (DocumentManager) and state tracking (MetadataStore).