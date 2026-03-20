# Query 5: Configuration

**Status**: success
**Tokens Used**: 1589
**Timestamp**: 2026-03-18T19:21:41.486917
**Tool Calls**: 14

---

I'll search the library for information about configuring backends and available options.


Let me search for more specific information about backend configuration and settings.


Let me read the settings file to get complete configuration details.


Let me search for the settings file directly.


Let me list the documents to find configuration-related files.


Now let me read the backend factory to understand how backends are selected.


Let me also check the documentation for more context on configuration.


Let me search the library for documentation about configuration.


Let me read the configuration documentation file that was mentioned in the search results.


Let me check the CLI tools to see how configuration is handled.


Based on my research of the library, I can now provide you with comprehensive information about configuring backends. Let me compile this into a clear answer.

---

## How to Configure Backend Selection and Available Options

Based on the library documentation, here's how backend configuration works:

### **Available Backends**

The Librarian MCP Server supports two backend options:

1. **[Chonkie Backend](mcp_server/backend/chonkie_backend.py)** - Default option
2. **[ChromaDB Backend](mcp_server/backend/chroma_backend.py)** - Alternative option

[Source: mcp_server/config/settings.py]

### **Configuration Methods**

Configuration is applied in this order (later overrides earlier):

1. **Code defaults** (in `settings.py`)
2. **Environment variables** (`LIBRARIAN_*`)
3. **Command-line arguments** (`--*`)

[Source: search results from library]

### **How to Set the Backend**

#### **Method 1: Environment Variable (Recommended)**

Set the `LIBRARIAN_BACKEND` environment variable before starting the server:

```bash
# Use Chonkie backend (default)
export LIBRARIAN_BACKEND=chonkie

# Or use ChromaDB backend
export LIBRARIAN_BACKEND=chroma
```

[Source: mcp_server/config/settings.py]

#### **Method 2: Command-Line Argument**

When starting the server, you can override via CLI:

```bash
python -m mcp_server --backend chonkie
# or
python -m mcp_server --backend chroma
```

[Source: search results from library]

### **Backend Selection Logic**

The backend factory (`factory.py`) uses this logic:

```python
def get_backend(backend_type: str = "chroma", **kwargs):
    if backend_type == "chonkie":
        return ChonkieBackend(**kwargs)
    elif backend_type == "chroma":
        return ChromaBackend(**kwargs)
    else:
        raise ValueError(f"Unsupported backend type: {backend_type}")
```

[Source: mcp_server/backend/factory.py]

### **Other Configuration Options**

The `settings.py` file provides these configurable options via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LIBRARIAN_SAFE_DIR` | `$HOME` | Safe directory for CLI operations |
| `LIBRARIAN_DOCUMENTS_DIR` | `$PROJECT_ROOT/documents` | Document storage location |
| `LIBRARIAN_CHROMA_PATH` | `$PROJECT_ROOT/chroma_db` | ChromaDB database path |
| `LIBRARIAN_CHROMA_COLLECTION` | `documents` | ChromaDB collection name |
| `LIBRARIAN_METADATA_PATH` | `$PROJECT_ROOT/metadata` | Metadata storage location |
| `LIBRARIAN_MAX_DOCUMENT_SIZE` | `10000000` (10MB) | Maximum document size |
| `LIBRARIAN_CHUNK_SIZE` | `1000` | Chunk size for processing |
| `LIBRARIAN_MAX_OUTPUT_CHARS` | `8000` | Maximum output characters |
| `LIBRARIAN_COMMAND_TIMEOUT` | `15` seconds | Command execution timeout |

[Source: mcp_server/config/settings.py]

### **Important Notes**

- Both backends respect the same security layers (directory sandboxing, output truncation, timeouts, etc.)
- The default backend is **chonkie** as specified in the settings
- You can verify your current configuration by checking the `settings.BACKEND` value or examining which backend is being used during initialization

[Source: mcp_server/config/settings.py]

---

Would you like me to:
1. Explain the differences between Chonkie and ChromaDB backends?
2. Help you check your current backend configuration?
3. Show you how to switch between backends dynamically?