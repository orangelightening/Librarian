# MCP Configuration Templates

**Ready-to-use JSON configs for Jan MCP Server**

## Dev Library Template

Copy and paste this into Jan's MCP configuration window:

```json
{
  "active": true,
  "args": [
    "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"
  ],
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "env": {
    "LIBRARIAN_BACKEND": "chonkie",
    "LIBRARIAN_CHROMA_PATH": "/home/peter/development/librarian-mcp/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/home/peter/development/librarian-mcp/.librarian/metadata",
    "LIBRARIAN_SAFE_DIR": "/home/peter/development/librarian-mcp",
    "PYTHONPATH": "/home/peter/development/librarian-mcp"
  }
}
```

**Purpose:** Development documentation and code
**Directory:** `/home/peter/development/librarian-mcp`
**Data:** `.librarian/chroma_db` and `.librarian/metadata`

---

## Botany Library Template

Copy and paste this into Jan's MCP configuration window:

```json
{
  "active": true,
  "args": [
    "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"
  ],
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "env": {
    "LIBRARIAN_BACKEND": "chonkie",
    "LIBRARIAN_CHROMA_PATH": "/home/peter/botany/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/home/peter/botany/.librarian/metadata",
    "LIBRARIAN_SAFE_DIR": "/home/peter/botany",
    "PYTHONPATH": "/home/peter/development/librarian-mcp"
  }
}
```

**Purpose:** Agricultural science PDFs (Agronomy, Forestry, Pomology)
**Directory:** `/home/peter/botany`
**Data:** `.librarian/chroma_db` and `.librarian/metadata`

---

## Custom Library Template

To create a new library, copy this template and update the paths:

```json
{
  "active": true,
  "args": [
    "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"
  ],
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "env": {
    "LIBRARIAN_BACKEND": "chonkie",
    "LIBRARIAN_CHROMA_PATH": "/YOUR/LIBRARY/PATH/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/YOUR/LIBRARY/PATH/.librarian/metadata",
    "LIBRARIAN_SAFE_DIR": "/YOUR/LIBRARY/PATH",
    "PYTHONPATH": "/home/peter/development/librarian-mcp"
  }
}
```

**Replace:**
- `/YOUR/LIBRARY/PATH` with your library directory (3 places)

---

## Quick Setup Steps

1. **Create library directory:**
   ```bash
   mkdir -p /path/to/your/library
   ```

2. **Add documents:**
   ```bash
   cp *.pdf *.md /path/to/your/library/
   ```

3. **Configure MCP:**
   - Copy the appropriate template above
   - Update paths for your library
   - Paste into Jan's MCP configuration

4. **Start using:**
   - Activate the MCP server in Jan
   - Use `sync_documents(path)` to index
   - Search with `search_library(query)`

---

## Environment Variable Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `LIBRARIAN_BACKEND` | Chunking backend | `chonkie` (PDF support) |
| `LIBRARIAN_CHROMA_PATH` | Vector database | `/path/.librarian/chroma_db` |
| `LIBRARIAN_METADATA_PATH` | Document metadata | `/path/.librarian/metadata` |
| `LIBRARIAN_SAFE_DIR` | Library directory | `/path/to/library` |
| `PYTHONPATH` | Code location | `/home/peter/development/librarian-mcp` |

---

## Notes

- **Always use absolute paths** - No relative paths or `~`
- **One library per MCP server** - Toggle servers on/off as needed
- **Data is isolated** - Each `.librarian/` is independent
- **Auto-creation** - `.librarian/` directories created automatically

---

## Troubleshooting

**Server won't start:**
- Verify Python path: `/home/peter/development/librarian-mcp/venv/bin/python`
- Check PYTHONPATH: `/home/peter/development/librarian-mcp`
- Ensure directory exists and is writable

**No documents found:**
- Run `sync_documents(path)` first
- Check directory contains supported files (.pdf, .md, .txt, etc.)
- Verify LIBRARIAN_SAFE_DIR points to correct location

**Poor search results:**
- Documents must be indexed with `sync_documents()`
- Try different query terms
- Increase limit: `search_library(query, limit=20)`
