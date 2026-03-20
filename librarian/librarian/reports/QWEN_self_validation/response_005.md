# Query 5: Backend Configuration Options

## How to Configure the Backend and Available Options

The librarian-mcp system supports **two backend implementations** for document processing and semantic search: **ChonkieBackend** (default) and **ChromaDB** (optional).

---

## Backend Selection via Environment Variable

### Primary Configuration Method

The backend is selected using the `LIBRARIAN_BACKEND` environment variable:

```bash
# Default: Chonkie backend
export LIBRARIAN_BACKEND=chonkie

# Switch to ChromaDB backend
export LIBRARIAN_BACKEND=chroma
```

**Configuration Priority** (later overrides earlier):
1. Code defaults (in `settings.py`)
2. Environment variables (`LIBRARIAN_BACKEND`)
3. Command-line arguments (`--backend`) [Source: CONFIGURATION.md]

---

## Available Backend Options

### Option 1: ChonkieBackend (Default)

**File**: `mcp_server/backend/chonkie_backend.py`

**Purpose**: Intelligent semantic chunking using the Chonkie library

**Key Features**:
- ✅ **Semantic boundaries**: Respects sentence and paragraph structure [Source: ARCHITECTURE.md]
- ✅ **Context preservation**: Related concepts stay together [Source: ARCHITECTURE.md]
- ✅ **Intelligent sizing**: Adapts to document structure [Source: ARCHITECTURE.md]
- ✅ **Better search results**: Higher quality chunks = better matches [Source: README.md]

**Configuration**:
- **Default chunk size**: `LIBRARIAN_CHUNK_SIZE=1000` characters
- **Min chunk size**: 50 characters
- **Chunker**: `RecursiveChunker` with semantic boundaries

**Implementation**:
```python
class ChonkieBackend(ChromaBackend):
    def __init__(self, chunk_size: int = 1000, min_chunk_size: int = 50):
        super().__init__()
        self.chunker = RecursiveChunker(
            chunk_size=chunk_size,
            min_characters_per_chunk=min_chunk_size
        )
```

**Use When**:
- Search result quality is important [Source: CONFIGURATION.md]
- Documents have complex structure [Source: CONFIGURATION.md]
- You want semantic understanding [Source: CONFIGURATION.md]
- Production use [Source: CONFIGURATION.md]

**Advantages**:
- Intelligent semantic boundaries [Source: CONFIGURATION.md]
- Better search relevance [Source: CONFIGURATION.md]
- Context preservation [Source: CONFIGURATION.md]
- Adapts to document structure [Source: CONFIGURATION.md]

**Disadvantages**:
- Slightly slower processing [Source: CONFIGURATION.md]
- More complex chunking logic [Source: CONFIGURATION.md]

---

### Option 2: ChromaDB Backend (Optional)

**File**: `mcp_server/backend/chroma_backend.py`

**Purpose**: Fast sentence-based chunking using ChromaDB's default behavior

**Key Features**:
- ✅ **Fast processing**: Quick sentence-based chunking [Source: ARCHITECTURE.md]
- ✅ **Simple chunks**: Predictable chunk sizes [Source: README.md]
- ✅ **Well-tested**: Stable and reliable implementation [Source: README.md]

**Implementation**:
```python
class ChromaBackend(DocumentBackend):
    def chunk_documents(self, documents, document_ids, source):
        # Simple sentence-based chunking
        # Uses ChromaDB's default embedding function
        pass
```

**Use When**:
- Processing speed is critical [Source: CONFIGURATION.md]
- Documents are very simple [Source: CONFIGURATION.md]
- Testing and development [Source: CONFIGURATION.md]
- Fallback option [Source: CONFIGURATION.md]

**Advantages**:
- Fast processing [Source: CONFIGURATION.md]
- Simple predictable chunks [Source: CONFIGURATION.md]
- Well-tested implementation [Source: README.md]

**Disadvantages**:
- Poorer search relevance [Source: CONFIGURATION.md]
- May break semantic boundaries [Source: CONFIGURATION.md]
- Less context preservation [Source: CONFIGURATION.md]

---

## Configuration Examples

### Temporary Switch (Current Session)
```bash
# Set environment variable
export LIBRARIAN_BACKEND=chroma

# Restart MCP server
./setup_mcp.sh
```

### Permanent Switch (All Sessions)
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export LIBRARIAN_BACKEND=chroma' >> ~/.bashrc
source ~/.bashrc
```

### Verify Current Backend
```python
from mcp_server.config.settings import settings
print(f"Current backend: {settings.BACKEND}")
```

---

## No Breaking Changes

**Important**: Both backends work with existing ChromaDB databases:
- Users can switch between backends without losing data [Source: CHONKIE_MIGRATION.md]
- Existing libraries continue to function [Source: CHONKIE_MIGRATION.md]
- Gradual migration is supported [Source: CHONKIE_MIGRATION.md]

---

## Backend Selection Guide Summary

| Aspect | Chonkie (Default) | ChromaDB |
|--------|-------------------|----------|
| **Processing Speed** | Slightly slower | Fast |
| **Search Quality** | Better relevance | Lower relevance |
| **Chunking Strategy** | Semantic boundaries | Sentence-based |
| **Context Preservation** | Excellent | Basic |
| **Complexity** | Higher | Lower |
| **Use Case** | Production, quality-first | Testing, speed-first |

**Recommendation**: Use `chonkie` for better search results in production. Only use `chroma` if you need faster processing speed [Source: CONFIGURATION.md].

---

## Summary

To configure which backend the librarian uses:

1. **Set the `LIBRARIAN_BACKEND` environment variable**:
   - `chonkie` (default) - Recommended for production
   - `chroma` - Faster but lower quality

2. **Restart the MCP server** for changes to take effect

3. **Verify with code** using `settings.BACKEND`

The system supports seamless switching without data loss, and both backends respect all security boundaries equally [Source: SECURITY.md].

---

## References
- [Source: CONFIGURATION.md] - Complete configuration guide
- [Source: ARCHITECTURE.md] - Backend architecture details
- [Source: README.md] - Backend comparison summary
- [Source: CHONKIE_MIGRATION.md] - Migration considerations
- [Source: SECURITY.md] - Backend security guarantees