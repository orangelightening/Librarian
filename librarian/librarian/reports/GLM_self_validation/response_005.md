# Response 005: How do I configure which backend the librarian uses and what are the options?

## Overview

The Librarian MCP Server supports a **dual backend architecture** with two configurable backend options. Backend selection is controlled via the `LIBRARIAN_BACKEND` environment variable, which can be set before starting the server [Source: ARCHITECTURE.md, settings.py].

---

## Available Backend Options

### Option 1: Chonkie Backend (Default)

**Backend Type**: `chonkie`

**Description**: Intelligent semantic chunking using the Chonkie library's `RecursiveChunker` [Source: ARCHITECTURE.md]

**Key Features**:
- ✅ Semantic boundaries that respect document structure (paragraphs, sections, headers)
- ✅ Context preservation - related ideas stay together in chunks
- ✅ Intelligent sizing that adapts to natural content boundaries
- ✅ Enhanced metadata (token counts, character counts, chunking method)
- ✅ Better search results - higher quality chunks = better semantic matches [Source: ARCHITECTURE.md]

**Best For**:
- Most document types (technical docs, articles, books)
- When search result quality is important
- When documents have complex structure
- Production deployment (default choice) [Source: ARCHITECTURE.md, README.md]

**Configuration**:
```bash
export LIBRARIAN_BACKEND=chonkie  # This is the default
./setup_mcp.sh
```

---

### Option 2: ChromaDB Backend

**Backend Type**: `chroma`

**Description**: Simple sentence-based chunking (original implementation) [Source: ARCHITECTURE.md]

**Key Features**:
- ✅ Fast processing - quick chunking
- ✅ Simple approach - splits by sentence boundaries
- ✅ Predictable - consistent chunk sizes
- ✅ Reliable - well-tested implementation [Source: ARCHITECTURE.md]

**Best For**:
- Processing speed is more important than search quality
- Very simple documents without complex structure
- Fallback option if Chonkie has issues
- Testing and development [Source: ARCHITECTURE.md]

**Configuration**:
```bash
export LIBRARIAN_BACKEND=chroma
./setup_mcp.sh
```

---

## Configuration Methods

### Method 1: Environment Variable (Recommended)

The preferred method is to set the `LIBRARIAN_BACKEND` environment variable before starting the server [Source: settings.py, ARCHITECTURE.md]:

```bash
# Set backend to Chonkie (default)
export LIBRARIAN_BACKEND=chonkie
./setup_mcp.sh

# Or set backend to ChromaDB
export LIBRARIAN_BACKEND=chroma
./setup_mcp.sh
```

**Advantages**:
- ✅ No code changes required
- ✅ Easy to switch backends
- ✅ Works with both backends sharing the same ChromaDB database
- ✅ Temporary configuration (doesn't persist across sessions)

---

### Method 2: Modify Configuration File

You can also modify the default backend by editing `mcp_server/config/settings.py` [Source: settings.py]:

```python
# Change from:
BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chroma")

# To:
BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")
```

**Advantages**:
- ✅ Sets a permanent default
- ✅ No need to set environment variable each time

**Disadvantages**:
- ❌ Requires code changes
- ❌ Not as flexible as environment variable

---

### Method 3: Backend Factory (Programmatic)

The backend is selected via the `get_backend()` factory function in `mcp_server/backend/factory.py` [Source: factory.py]:

```python
def get_backend(backend_type: str = "chroma", **kwargs) -> 'DocumentBackend':
    """
    Get configured backend instance.

    Args:
        backend_type: Type of backend ("chroma" or "chonkie")
        **kwargs: Additional arguments to pass to backend constructor

    Returns:
        Configured backend instance

    Raises:
        ValueError: If backend_type is not supported
    """
    if backend_type == "chonkie":
        from .chonkie_backend import ChonkieBackend
        return ChonkieBackend(**kwargs)
    elif backend_type == "chroma":
        from .chroma_backend import ChromaBackend
        return ChromaBackend(**kwargs)
    else:
        raise ValueError(
            f"Unsupported backend type: {backend_type}. "
            f"Supported types: 'chroma', 'chonkie'"
        )
```

**Note**: This method is primarily used internally by the server. For normal use, use Method 1 (environment variable).

---

## Backend Configuration Settings

### Environment Variables

All backend-related configuration is handled via environment variables in `mcp_server/config/settings.py` [Source: settings.py]:

```python
class Settings:
    """Configuration settings for the Librarian MCP Server."""

    # Backend selection
    BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")

    # Chonkie (Phase 2)
    CHONKIE_URL = os.getenv("LIBRARIAN_CHONKIE_URL", "http://localhost:8000")

    # Document processing
    CHUNK_SIZE = int(os.getenv("LIBRARIAN_CHUNK_SIZE", "1000"))

    # ChromaDB
    CHROMA_PATH = os.getenv("LIBRARIAN_CHROMA_PATH", str(PROJECT_ROOT / "chroma_db"))
    CHROMA_COLLECTION = os.getenv("LIBRARIAN_CHROMA_COLLECTION", "documents")

    # Metadata storage
    METADATA_PATH = os.getenv("LIBRARIAN_METADATA_PATH", str(PROJECT_ROOT / "metadata"))
```

**Available Environment Variables**:

| Variable | Description | Default |
|----------|-------------|---------|
| `LIBRARIAN_BACKEND` | Backend selection (`chroma` or `chonkie`) | `chonkie` |
| `LIBRARIAN_CHONKIE_URL` | Chonkie server URL | `http://localhost:8000` |
| `LIBRARIAN_CHUNK_SIZE` | Target chunk size (characters) | `1000` |
| `LIBRARIAN_CHROMA_PATH` | ChromaDB database path | `PROJECT_ROOT/chroma_db` |
| `LIBRARIAN_CHROMA_COLLECTION` | ChromaDB collection name | `documents` |
| `LIBRARIAN_METADATA_PATH` | Metadata storage path | `PROJECT_ROOT/metadata` |

---

## Chonkie Chunking Options

The Chonkie backend currently uses `RecursiveChunker`, but you can modify `mcp_server/backend/chonkie_backend.py` to use other chunkers [Source: CHONKIE_INTEGRATION.md]:

```python
# Available chunkers from Chonkie:
from chonkie import RecursiveChunker  # Default - recursive with semantic boundaries
from chonkie import SemanticChunker   # Requires embeddings, semantic grouping
from chonkie import TokenChunker      # Fixed token chunks
from chonkie import SentenceChunker    # Sentence-based chunks
```

**Note**: `SemanticChunker` requires embeddings and may be slower.

---

## Which Backend Should I Use?

### Use Chonkie (Default) When:

- ✅ Search result quality matters most
- ✅ Documents have complex structure (headings, paragraphs, sections)
- ✅ You want semantic understanding and context preservation
- ✅ Production deployment with focus on relevance
- ✅ Working with technical documentation, articles, books [Source: README.md, ARCHITECTURE.md]

**Advantages**:
- Better search relevance through semantic boundaries
- Context-aware chunking preserves meaning
- Enhanced metadata for better search
- Actively maintained by Chonkie team
- Less maintenance (no custom chunking code) [Source: ARCHITECTURE.md, CHONKIE_INTEGRATION.md]

**Disadvantages**:
- Slightly slower processing than ChromaDB
- Requires Chonkie dependency

---

### Use ChromaDB Backend When:

- ✅ Processing speed is critical
- ✅ Documents are very simple (flat structure)
- ✅ Testing and development scenarios
- ✅ Fallback option if Chonkie has issues [Source: README.md, ARCHITECTURE.md]

**Advantages**:
- Faster processing speed
- Simple, predictable chunking
- Well-tested implementation
- No additional dependencies beyond ChromaDB [Source: ARCHITECTURE.md]

**Disadvantages**:
- Poorer search relevance (may break semantic boundaries)
- Less context preservation
- More code maintenance (custom chunking logic)

---

## Switching Backends

### Seamless Migration

One of the key design decisions is that **existing ChromaDB databases work with both backends**, meaning [Source: CHONKIE_MIGRATION.md]:

- ✅ Users can switch between backends without losing data
- ✅ Existing libraries continue to function
- ✅ Gradual migration is supported
- ✅ No re-indexing required

### Migration Steps

**For New Users**:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set backend to Chonkie (or chroma)
export LIBRARIAN_BACKEND=chonkie

# 3. Start the server
./setup_mcp.sh

# 4. Add your documents
# Use the MCP tools to sync your documents
```

**For Existing Users**:
- **Good news**: No migration needed! Your existing ChromaDB database works with both backends
- Simply change the environment variable and restart the server
- Your existing documents will work with the new backend immediately [Source: CHONKIE_MIGRATION.md]

### Performance Trade-offs

| Aspect | Phase 1 (ChromaDB) | Phase 2 (Chonkie Default) |
|--------|-------------------|---------------------------|
| **Chunking Quality** | Simple sentence split | Semantic, context-aware |
| **Search Relevance** | Good | **Better** (main benefit) |
| **Processing Speed** | Faster | Slightly slower |
| **Code Maintenance** | Higher (1000+ lines) | Lower (~50 lines wrapper) |
| **Active Development** | Manual updates | Chonkie team updates |
| **Metadata** | Basic | Enhanced (token counts, etc.) |
| **Production Ready** | ✅ | ✅ |

**Trade-off Decision**: The slight decrease in processing speed is worth the significant improvement in search relevance and reduction in maintenance burden [Source: CHONKIE_MIGRATION.md].

---

## Checking Your Current Backend

To verify which backend is active:

```bash
# Check environment variable
echo $LIBRARIAN_BACKEND

# Or check via library stats
# Use the MCP client to run "get library stats"
# Look for "Backend: chromadb" or "Backend: chonkie_recursive"
```

---

## Troubleshooting

### Issue: Backend Not Changing

**Problem**: Changed `LIBRARIAN_BACKEND` environment variable but backend didn't change.

**Solution**: Make sure to:
1. Set the environment variable **before** starting the server
2. Restart the MCP server after changing the variable
3. Check that the variable is exported (use `export`, not just assignment) [Source: CHONKIE_INTEGRATION.md]

### Issue: Backend Import Error

**Problem**: "ModuleNotFoundError: No module named 'chonkie'"

**Solution**: Install Chonkie dependency:
```bash
pip install chonkie
```

---

## Summary

**Configuration**: Set `LIBRARIAN_BACKEND` environment variable to either `chonkie` (default) or `chroma` before starting the server [Source: settings.py].

**Recommendation**: Use Chonkie for production deployments where search quality matters. Use ChromaDB only for speed-critical scenarios or as a fallback [Source: README.md, ARCHITECTURE.md].

**Seamless Switching**: Both backends use the same ChromaDB database, so you can switch between them at any time without losing data or re-indexing documents [Source: CHONKIE_MIGRATION.md].
