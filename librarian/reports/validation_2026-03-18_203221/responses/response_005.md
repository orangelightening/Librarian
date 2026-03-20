# Query 5: Configuration

**Status**: success
**Tokens Used**: 883
**Timestamp**: 2026-03-18T21:01:50.574737
**Tool Calls**: 4

---

I'll search the library for information about configuring backends in the Librarian system.


Let me search for more specific information about backend configuration and settings.


Let me read the settings file to get complete configuration details.


Now let me check the README for user-facing documentation about backend configuration.


Perfect! Now I have comprehensive information about backend configuration. Let me provide a complete answer to the user.

---

Based on the library documentation, here's how to configure which backend the Librarian uses:

## Backend Configuration Options

The Librarian supports **two backends**:

### 1. **Chonkie Backend** (Default)
- 🧠 **Intelligent semantic chunking** - Respects document structure
- 🎯 Better search results with context-aware boundaries  
- 📊 Enhanced metadata including token counts and character counts
- 🚀 Production-ready, battle-tested chunking library

### 2. **ChromaDB Backend** (Optional)
- ⚡ Fast processing with quick sentence-based chunking
- 🎛️ Simple & predictable consistent chunk sizes
- 🔧 Great fallback option when speed matters most

---

## How to Configure

Set the `LIBRARIAN_BACKEND` environment variable:

```bash
# Use Chonkie (default)
export LIBRARIAN_BACKEND=chonkie

# Use ChromaDB
export LIBRARIAN_BACKEND=chroma
```

The configuration is centralized in [`mcp_server/config/settings.py`](file:///home/peter/development/librarian-mcp/mcp_server/config/settings.py):

```python
BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")
```

**Default**: `chonkie` (if not specified)

---

## Additional Configuration Options

The settings file also includes other configurable parameters you may want to adjust:

| Setting | Environment Variable | Default | Description |
|---------|---------------------|---------|-------------|
| Safe directory | `LIBRARIAN_SAFE_DIR` | `$HOME` | Directory for CLI operations |
| Documents storage | `LIBRARIAN_DOCUMENTS_DIR` | `<project>/documents` | Where documents are stored |
| ChromaDB path | `LIBRARIAN_CHROMA_PATH` | `<project>/chroma_db` | ChromaDB database location |
| Collection name | `LIBRARIAN_CHROMA_COLLECTION` | `documents` | ChromaDB collection name |
| Max document size | `LIBRARIAN_MAX_DOCUMENT_SIZE` | 10MB | Maximum file size to process |
| Chunk size | `LIBRARIAN_CHUNK_SIZE` | 1000 | Characters per chunk |
| Max output chars | `LIBRARIAN_MAX_OUTPUT_CHARS` | 8000 | Output truncation limit |

---

## Migration Between Backends

The system is designed for easy migration:
- ✅ No code changes needed - just change the environment variable
- ✅ Both backends respect security equally (94+ exclusion patterns, sandboxing)
- ✅ Chonkie backend provides better search relevance
- ✅ ChromaDB backend offers faster processing when needed

**Sources:**
[Source: settings.py], [Source: README.md]