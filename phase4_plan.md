# Phase 4 Implementation Plan: Shadow Library + Marker Integration

**Date**: 2026-03-25
**Status**: Ready to implement
**Replaces**: `marker_plan.md` (which became inconsistent through iterative discussions)

---

## Executive Summary

**Goal**: Implement orthogonal shadow library architecture with Marker PDF conversion and single-ChromaDB multi-library support.

**Current State**:
- ✅ HTTP transport working (stdio → HTTP)
- ✅ Remote access validated (LAN)
- ✅ Multi-server architecture (one per library, different ports)
- ✅ Simpler client configs (URL-based)
- ⏳ Shadow library structure created but not populated
- ⏳ Marker integration planned but not implemented

**Target Architecture**:
- All documents (binaries + code) → shadow library
- Single ChromaDB with library identifiers
- One HTTP server per library (ports 8888, 8889, etc.)
- Marker for PDF→MD conversion
- Orthogonal design (no exceptions, consistent handling)

**Key Benefits**:
- Consistent document handling (all files in shadow)
- High-quality search (Marker extraction: 4.0+ relevance scores)
- Multi-library support (single ChromaDB)
- Remote access (HTTP)
- Simple client config (just URLs)

---

## Current Architecture (Working)

### What's Working Now

```
┌─────────────────────────────────────────────────────┐
│                  Client (Jan/LM Studio)             │
│  - Loads AI models (local or cloud)                 │
│  - Holds conversation context                       │
│  - Makes tool calls to Librarian MCP                │
└─────────────────────────────────────────────────────┘
                    │ HTTP
                    ↓
┌─────────────────────────────────────────────────────┐
│           Librarian MCP Server (HTTP)                │
│  - Port 8888: Botany library                        │
│  - Port 8889: Librarian-mcp library                 │
│  - Stateless, atomic tool calls                     │
└─────────────────────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────┐
│              Library-specific storage                │
│  Botany: /home/peter/botany/.librarian/             │
│  Dev: /home/peter/development/librarian-mcp/.librarian/ │
└─────────────────────────────────────────────────────┘
```

### HTTP Configuration

**Server startup** (per library):
```bash
#!/bin/bash
# start_http_botany.sh
export LIBRARIAN_TRANSPORT=http
export LIBRARIAN_PORT=8888
export LIBRARIAN_CHROMA_PATH=/home/peter/botany/.librarian/chroma_db
export LIBRARIAN_SAFE_DIR=/home/peter/botany
# ... start server
```

**Client config** (Jan/LM Studio):
```json
{
  "mcpServers": {
    "librarian-botany": {
      "url": "http://192.168.3.67:8888/mcp"
    }
  }
}
```

**Performance**: No noticeable difference vs stdio (HTTP overhead: ~5ms vs ~1ms)

**Limitations**:
- Tool name collision: Can't run multiple servers simultaneously (models get confused)
- Manual switch: Must stop one server, start another
- Library-specific ChromaDBs (no cross-library search)

---

## Target Architecture (Phase 4)

### Orthogonal Shadow Library Design

```
┌──────────────────────────────────────────────────────┐
│          Source Libraries (Original Documents)       │
│  /home/peter/botany/              (PDFs, docs, etc) │
│  /home/peter/development/         (Code, docs)       │
│  /home/peter/cooking/             (Recipes, etc)      │
└──────────────────────────────────────────────────────┘
                    │
                    │ sync_library() tool
                    │
        ┌───────────┴───────────┐
        │                       │
        ↓                       ↓
┌──────────────┐      ┌──────────────────┐
│   Binaries   │      │   Code/Text      │
│  (PDF, DOCX) │      │  (.py, .md, .js) │
└──────────────┘      └──────────────────┘
        │                       │
        │ [Marker]              │ [Copy]
        ↓                       ↓
┌──────────────────────────────────────────────────────┐
│           Shadow Library (/home/peter/library_shadows/)│
│  ├── botany/                  (Flat, no subdirs)      │
│  │   ├── Plum.md              (Converted PDF)         │
│  │   ├── Forestry.md          (Converted PDF)         │
│  │   └── document_mappings.json                       │
│  ├── librarian-mcp/           (Flat, no subdirs)      │
│  │   ├── README.md            (Copied from source)    │
│  │   ├── cli_tools.py         (Copied from source)    │
│  │   └── document_mappings.json                       │
│  ├── cooking/                 (Flat, no subdirs)      │
│  ├── sandbox/                 (Timestamped conversions)│
│  └── chromadb/                (Single ChromaDB)       │
│      └── chroma.db            (All libraries)         │
└──────────────────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│          MCP Servers (One per library)               │
│  Botany:       http://192.168.3.67:8888/mcp         │
│  Librarian-mcp: http://192.168.3.67:8889/mcp         │
│  Cooking:      http://192.168.3.67:8890/mcp         │
│                                                      │
│  Each server reads from shadow library + ChromaDB    │
└──────────────────────────────────────────────────────┘
```

### Key Design Principles

**Orthogonality**:
- All files → shadow library (no exceptions)
- Binaries: Convert with Marker, save to shadow
- Code: Copy directly to shadow
- Result: Consistent handling, models always read from same location

**Single ChromaDB**:
- One database at `/home/peter/library_shadows/chromadb/`
- Library identifiers in metadata
- Cross-library search possible
- Simpler backup/maintenance

**Flat Structure**:
- No subdirectories in shadow libraries
- All files at root level (e.g., `botany/Plum.md`)
- Timestamps for name collisions (in `sandbox/`)
- Simpler scanning, no recursion needed

**Document Mappings**:
- `document_mappings.json` per library
- Tracks: original path, checksum, conversion type, timestamp
- Handles collisions, detects changes
- Enables change detection and re-sync

---

## Implementation Phases

### Phase 1: Core Marker Extraction (Foundation)

**Goal**: PDF → Markdown conversion pipeline

**Components**:
1. **Marker wrapper function**
   - `convert_pdf_to_markdown(pdf_path, output_dir)`
   - Uses marker_single for conversion
   - Cleans up Marker's subdirectory mess
   - Returns path to cleaned .md file

2. **Document mappings system**
   - `document_mappings.json` per library
   - Tracks conversions: original_path, checksum, type, timestamp
   - Collision detection and resolution

3. **VRAM safety checks**
   - Check available GPU memory before conversion
   - Warn if < 5GB free (Marker recommendation, uses ~3.5GB)
   - Graceful fallback to CPU mode

**Deliverables**:
- `mcp_server/core/marker_extractor.py` (new)
- `mcp_server/core/document_mappings.py` (new)
- Updated `mcp_server/core/document_manager.py`

**Testing**:
- Convert sample PDFs from botany library
- Verify .md quality
- Check VRAM usage
- Test checksum-based change detection

**Estimated time**: 6-8 hours

---

### Phase 2: Shadow Library Management

**Goal**: Copy/sync documents to shadow library

**Components**:
1. **Shadow library manager**
   - `copy_to_shadow(source_file, shadow_path, mappings)`
   - Checksum-based change detection
   - Handles collisions with timestamps
   - Updates document_mappings.json

2. **Library sync function**
   - `sync_library(library_name, source_path, shadow_path)`
   - Scans source directory
   - Converts binaries (PDF, DOCX) with Marker
   - Copies code/text files
   - Removes deleted files from shadow
   - Updates metadata

3. **Shadow library configuration**
   - YAML config per library: `/home/peter/library_shadows/.librarian/config.yaml`
   - Defines: source_path, shadow_path, library_name, file_types

**Deliverables**:
- `mcp_server/core/shadow_manager.py` (new)
- `mcp_server/core/library_config.py` (new)
- Updated `mcp_server/core/document_manager.py`
- Config templates

**Testing**:
- Sync botany library (PDFs → .md)
- Sync librarian-mcp library (code files)
- Verify checksums work
- Test change detection (modify file, re-sync)

**Estimated time**: 8-10 hours

---

### Phase 3: Single ChromaDB Multi-Library

**Goal**: One ChromaDB with library identifiers

**Components**:
1. **ChromaDB migration**
   - Migrate existing library-specific ChromaDBs
   - Add library identifiers to all metadata
   - Consolidate to `/home/peter/library_shadows/chromadb/`

2. **Library-aware queries**
   - `search_library(query, library=None, limit=10)`
   - If `library` specified: search only that library
   - If `library=None`: search all libraries
   - Results include library name in metadata

3. **Backend factory update**
   - Support library-aware initialization
   - Pass library identifier to ChromaDB
   - Update collection naming strategy

**Deliverables**:
- Updated `mcp_server/backend/chroma_backend.py`
- Updated `mcp_server/backend/factory.py`
- Migration script: `scripts/migrate_to_single_chromadb.sh`
- Updated tool: `search_library(query, library=None, limit=10)`

**Testing**:
- Migrate botany ChromaDB
- Search with library filter
- Search across all libraries
- Verify metadata includes library names

**Estimated time**: 4-6 hours

---

### Phase 4: Tool Exposing + Workflow Integration

**Goal**: Complete MCP tool interface

**Components**:
1. **Library management tools**
   - `sync_library(library_name)` - Sync source → shadow
   - `list_libraries()` - List all configured libraries
   - `get_library_status(library_name)` - Check sync status
   - `add_source_file(library_name, file_path)` - Add single file

2. **Server startup scripts**
   - `start_http_botany.sh`
   - `start_http_librarian_mcp.sh`
   - `start_http_cooking.sh`
   - Generic: `start_http_library.sh <library_name>`

3. **Client config templates**
   - `mcp-config-single.json` (one library)
   - `mcp-config-multi.json` (multiple libraries)
   - Documentation for LM Studio, Jan, Claude Desktop

**Deliverables**:
- Updated `mcp_server/tools/library_tools.py`
- Startup scripts in project root
- Config templates in `configs/`
- Documentation: `docs/HTTP_SETUP.md`

**Testing**:
- Test all tools via LM Studio
- Test remote access (wife's PC)
- Verify tool name collision handling
- Performance benchmarking

**Estimated time**: 6-8 hours

---

## Global TODO List

### Priority: CRITICAL (Must have for v1.0)

- [ ] **Phase 1**: Implement Marker extraction (6-8 hours)
  - [ ] Create `marker_extractor.py`
  - [ ] Create `document_mappings.py`
  - [ ] Add VRAM safety checks
  - [ ] Test with sample PDFs

- [ ] **Phase 2**: Shadow library management (8-10 hours)
  - [ ] Create `shadow_manager.py`
  - [ ] Create `library_config.py`
  - [ ] Implement `sync_library()` function
  - [ ] Test with botany + librarian-mcp libraries

- [ ] **Phase 3**: Single ChromaDB (4-6 hours)
  - [ ] Migrate existing ChromaDBs
  - [ ] Add library identifiers to metadata
  - [ ] Update `search_library()` for library filtering
  - [ ] Test cross-library search

- [ ] **Phase 4**: Tool integration (6-8 hours)
  - [ ] Expose `sync_library` as MCP tool
  - [ ] Create startup scripts per library
  - [ ] Create config templates
  - [ ] Test with remote clients

### Priority: HIGH (Should have for v1.1)

- [ ] **Documentation**
  - [ ] Update README.md with HTTP setup
  - [ ] Create `docs/SHADOW_LIBRARY_ARCHITECTURE.md`
  - [ ] Document `sync_library` workflow
  - [ ] Create troubleshooting guide

- [ ] **Error handling**
  - [ ] Graceful handling of Marker failures
  - [ ] Fallback to pypdf if Marker unavailable
  - [ ] Better error messages for sync failures
  - [ ] Logging for debugging

- [ ] **Performance**
  - [ ] Batch conversion for large PDF sets
  - [ ] Parallel sync for multiple libraries
  - [ ] Caching for frequently accessed documents
  - [ ] ChromaDB query optimization

### Priority: MEDIUM (Nice to have for v1.2)

- [ ] **Automation**
  - [ ] Directory watcher for auto-sync (inotify)
  - [ ] Scheduled sync tasks (cron)
  - [ ] Web UI for library management
  - [ ] Progress bars for long operations

- [ ] **Advanced features**
  - [ ] Version history for documents
  - [ ] Diff view for document changes
  - [ ] Tag-based organization
  - [ ] Full-text search within documents

- [ ] **Quality improvements**
  - [ ] PDF quality metrics
  - [ ] Conversion validation
  - [ ] OCR for scanned PDFs
  - [ ] Table extraction improvements

---

## Timeline

### Week 1: Foundation (24-32 hours)
- **Day 1-2**: Phase 1 - Marker extraction (6-8 hours)
- **Day 3-4**: Phase 2 - Shadow library management (8-10 hours)
- **Day 5**: Testing and bug fixes

### Week 2: Integration (18-24 hours)
- **Day 1-2**: Phase 3 - Single ChromaDB (4-6 hours)
- **Day 3-4**: Phase 4 - Tool integration (6-8 hours)
- **Day 5**: Documentation and testing

### Week 3: Polish (10-15 hours)
- **Day 1-2**: HIGH priority items
- **Day 3**: Documentation completion
- **Day 4**: Final testing and validation
- **Day 5**: Release v1.0

### Week 4+: Future enhancements
- MEDIUM priority items
- User feedback integration
- Performance optimization

**Total estimated time**: 52-71 hours for v1.0

---

## Configuration Examples

### Library Configuration (YAML)

```yaml
# /home/peter/library_shadows/.librarian/botany.yaml
name: botany
display_name: "Botany Library"
source_path: /home/peter/botany
shadow_path: /home/peter/library_shadows/botany
library_type: binary_heavy  # PDFs, DOCX, etc.

file_types:
  convert: [pdf, docx, ppt, pptx]
  copy: [md, txt, rst]

chromadb_path: /home/peter/library_shadows/chromadb
metadata_path: /home/peter/library_shadows/.librarian/metadata
```

```yaml
# /home/peter/library_shadows/.librarian/librarian-mcp.yaml
name: librarian-mcp
display_name: "Librarian MCP Development"
source_path: /home/peter/development/librarian-mcp
shadow_path: /home/peter/library_shadows/librarian-mcp
library_type: code_heavy  # Python, JS, Markdown

file_types:
  copy: [py, js, md, txt, yaml, json]
  ignore: [pyc, __pycache__, node_modules]

chromadb_path: /home/peter/library_shadows/chromadb
metadata_path: /home/peter/library_shadows/.librarian/metadata
```

### Library Discovery (Dynamic)

**Libraries are discovered dynamically**, not hardcoded in enums:

```python
# Server reads library configs from /home/peter/library_shadows/.librarian/*.yaml
# No code changes needed to add libraries!

# At startup:
configs = load_library_configs("/home/peter/library_shadows/.librarian/")
# Returns: ["botany", "librarian-mcp", "cooking"]

# Model calls:
list_libraries()
# Returns: {
#   "libraries": [
#     {"name": "botany", "count": 12, "last_sync": "2026-03-24"},
#     {"name": "librarian-mcp", "count": 0, "last_sync": "never"},
#     {"name": "cooking", "count": 5, "last_sync": "2026-03-20"}
#   ]
# }
```

**Benefits of dynamic discovery:**
- ✅ Add libraries by creating YAML config (no code change)
- ✅ No server restart needed (configs reloaded on demand)
- ✅ Scales to unlimited libraries
- ✅ Library list always current

### MCP Client Configuration (HTTP)

```json
{
  "mcpServers": {
    "librarian": {
      "url": "http://192.168.3.67:8888/mcp"
    }
  }
}
```

**Note**: Single server URL, not multiple. Libraries are managed via tool parameters (`search_library(query, library="botany")`), not separate servers.

---

## Known Limitations

### Tool Name Collision (SOLVED in Phase 4)
**Previous problem**: Multiple servers expose same tool names (`search_library`, `list_indexed_documents`, etc.)

**Previous symptoms**: AI models can't distinguish which server to call

**Previous workaround**: Run only one server at a time (manual switching)

**Phase 4 solution**: Single server + library parameter
- ✅ One HTTP server (port 8888)
- ✅ Tools accept `library` parameter: `search_library(query, library="botany")`
- ✅ No tool name collision
- ✅ Models understand parameters better than tool prefixes
- ✅ Scales to unlimited libraries (14 tools total, not 14×N)

### GPU Memory Constraints

**Workaround**:
- v1.0: Manual sync (stop server, sync, restart)
- v2.0: GPU upgrade (16-24GB VRAM) for live sync tool

### No Cross-Library Search (Yet)
**Problem**: Current implementation has library-specific ChromaDBs

**Solution**: Phase 3 implements single ChromaDB with library identifiers

---

## System Prompt Strategy

**Critical requirement**: Models MUST use tools, not give up or rely on training data.

**Problem from previous versions**: Models sometimes answered without searching libraries, making up information instead of using tools.

**Solution**: Enforce tool usage in system prompt with mandatory workflow.

### System Prompt Template

```python
# Instructions to AI models (passed via MCP server instructions)
"""
You are a librarian with access to multiple document libraries via MCP tools.

**CRITICAL: Always use tools for information requests**
- When asked questions, you MUST search the libraries
- NEVER make up answers or rely only on training data
- Minimum workflow: list_libraries() → search_library() → formulate response

**Required first steps for new sessions:**
1. Call list_libraries() to discover available libraries
2. If user asks a question, search at least one library
3. Only then formulate your response

**Tool usage patterns:**
- "What do you have?": list_libraries()
- "Find X in Y": search_library(query="X", library="Y", limit=10)
- "Search everything": search_library(query="X", library=None, limit=10)
- "Compare X across libraries": search_all_libraries(query="X", limit=10)
- "Sync the botany library": sync_library(library="botany")

**Common mistakes to avoid:**
- ❌ Answering without searching libraries first
- ❌ Guessing which library to search (call list_libraries() if unsure)
- ❌ Making up document content (always cite what you find)
- ❌ Giving up if tools fail (try alternative search terms)

**How to handle failures:**
- If search returns no results: Try broader terms or search all libraries
- If library doesn't exist: Call list_libraries() to see what's available
- If sync fails: Check library path and permissions
- If unsure what to do: Call list_libraries() and explain what you find
"""
```

### Tool Enforcement in Code

```python
# In librarian_mcp.py instructions
def get_librarian_instructions():
    return """
    You are a research librarian with access to document libraries.

    **MANDATORY WORKFLOW:**
    1. For new sessions: Always call list_libraries() first
    2. For information requests: Always call search_library() at least once
    3. Only then: Formulate response based on search results

    **NEVER:**
    - Answer questions without searching
    - Make up document content
    - Rely on training data instead of tools
    - Give up without trying alternatives

    **ALWAYS:**
    - Cite sources from search results
    - Explain which library you searched
    - Try broader terms if no results
    - Ask for clarification if unsure
    """
```

---

## Success Criteria

### v1.0 Release (Must have)
- [x] HTTP transport working
- [x] Remote access validated
- [ ] Marker PDF→MD conversion
- [ ] Shadow library sync
- [ ] Single ChromaDB
- [ ] Library management tools
- [ ] System prompt with mandatory tool usage
- [ ] Basic documentation

### v1.1 Release (Should have)
- [ ] Complete documentation
- [ ] Error handling
- [ ] Performance optimizations
- [ ] Troubleshooting guide

### v1.2 Release (Nice to have)
- [ ] Automation (watchers, cron)
- [ ] Web UI
- [ ] Advanced features
- [ ] Quality metrics

---

## Notes

**Architectural clarity**:
- Librarian MCP = MCP server (atomic tools, stateless)
- Client (Jan/LM Studio) = AI models, context, synthesis
- Clean separation: Librarian provides tools, Client provides intelligence

**HTTP vs stdio**:
- HTTP: Better for production, multi-client, remote access
- stdio: Slightly lower latency, simpler for single-user local
- Decision: HTTP as default (stdio still available)

**Why orthogonal design**:
- Consistency: All files handled same way
- Simplicity: Models always read from shadow
- Maintainability: Fewer edge cases
- User insight: "Who cares if we duplicate a few code files"

**Why single ChromaDB**:
- Cross-library search
- Simpler backup
- Easier maintenance
- Better resource utilization

---

**Next step**: Begin Phase 1 implementation when ready.
