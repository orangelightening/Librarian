# Documentation Rewrite Plan

## 🚨 Critical Issue Identified

**Problem**: The librarian is providing **outdated information** about the system because documentation describes Phase 1 (ChromaDB-only) while the system is actually Phase 2 complete (ChromaDB + Chonkie backends).

**Impact**: System credibility is at risk. Users asking "what is the librarian system" get answers describing the old architecture, not the current one.

**Root Cause**: Documentation was written during Phase 1 and never updated after Phase 2 completion.

---

## Current Documentation Assessment

### ❌ Files Requiring Complete Rewrite

| File | Current Status | Problem |
|------|---------------|---------|
| `IMPLEMENTATION_SUMMARY.md` | Describes Phase 1 only | Says "ChromaDB implementation" with no mention of Chonkie backend option |
| `README.md` | Phase 1 content | No mention of backend selection, Chonkie, or Phase 2 completion |
| `SECURITY_AND_BOUNDARIES.md` | Mostly accurate but incomplete | Security content is good, but doesn't mention current system capabilities |

### ✅ Files That Are Accurate

| File | Status | Notes |
|------|--------|-------|
| `prompt.md` | ✅ Accurate | Current system prompt (KEEP at root) |
| `Poem_Chonkie_Hippo_Spontaneous.md` | ✅ Accurate | Chonkie poem (KEEP at root, mention in README) |
| `CHONKIE_INTEGRATION.md` | ✅ Accurate | Describes Phase 2 testing and implementation plan |
| `CHONKIE_MIGRATION.md` | ✅ Accurate | Explains how to use Chonkie backend |
| `CLAUDE.md` | ✅ Accurate | Development guidance, current state |
| `QUICKSTART.md` | ⚠️ Partially accurate | Basic setup works, but doesn't mention backend options |
| `Tools.md` | ✅ Accurate | Current tool list |
| `USER_GUIDE.md` | ⚠️ Needs review | May have outdated content |
| `phase3_planning.md` | ✅ Accurate | Future planning document |

### 🗑️ Files Already Archived

- `PHASE2.md` - Moved to `.old-docs/` (Phase 2 plan, now complete)
- `reco.md` - Moved to `.old-docs/` (Original integration recommendations)
- `status-2026-03-16.md` - Moved to `.old-docs/` (Phase 2 milestone snapshot)
- `responses.md`, `Response 2.md`, `prompt.md`, `Indexed_files.md` - Historical

---

## Proposed New Documentation Structure

### Core Documentation (Root Level)

```
librarian-mcp/
├── README.md                    # Main entry point (REWRITE)
├── ARCHITECTURE.md              # NEW: System architecture overview
├── QUICKSTART.md                # Already good, minor updates
├── CONFIGURATION.md             # NEW: Configuration options
├── SECURITY.md                  # NEW: Security model (rename from SECURITY_AND_BOUNDARIES.md)
├── CLAUDE.md                    # Keep as-is (developer guidance)
├── Tools.md                     # Keep as-is (tool reference)
├── USER_GUIDE.md                # Review and update if needed
│
├── PHASE2/                      # NEW: Phase 2 documentation
│   ├── CHONKIE_INTEGRATION.md   # Move from root
│   └── CHONKIE_MIGRATION.md     # Move from root
│
└── phase3_planning.md           # Future planning (keep)
```

### Delete/Archive

- `IMPLEMENTATION_SUMMARY.md` → Archive to `.old-docs/` (historical Phase 1 doc)
- `SECURITY_AND_BOUNDARIES.md` → Replace with `SECURITY.md`

---

## Detailed Rewrite Plan

### 1. `README.md` (Complete Rewrite)

**Purpose**: Main project entry point

**Required Sections**:
- Brief description (what it does)
- Current status (Phase 2 complete)
- Key features (including dual backend support)
- Quick start (3 steps to running)
- Backend selection (Chonkie default, ChromaDB optional)
- Why venv instead of Docker (close coupling, simplicity)
- The Chonkie poem (selling point - shows AI creativity)
- MCP client configuration
- Links to detailed docs

**Key Points to Emphasize**:
- ✅ Phase 2 COMPLETE
- ✅ **Chonkie is DEFAULT backend** (intelligent semantic chunking)
- ✅ ChromaDB backend available as fallback option
- ✅ **venv approach simplifies system** and enables close Chonkie-ChromaDB coupling
- ✅ Backend selection via environment variable
- ✅ Production-ready

**Remove**:
- Phase 1 references
- "Future" tense for Chonkie (it's implemented now)

---

### 2. `ARCHITECTURE.md` (NEW FILE)

**Purpose**: Complete technical architecture overview

**Sections**:
1. High-Level Architecture
   - MCP protocol layer
   - Tools layer (Library + CLI)
   - Core business logic
   - Backend abstraction layer
   - AI layer

2. Backend Architecture
   - Abstract interface (`base.py`)
   - Backend factory (`factory.py`)
   - **Chonkie backend (DEFAULT, intelligent semantic chunking)**
   - ChromaDB backend (optional, simple chunking)
   - How to switch backends

3. Document Lifecycle
   - Discovery → Filtering → Chunking → Embedding → Storage
   - Change detection (SHA-256 checksums)
   - Sync operations

4. Security Model
   - `.librarianignore` patterns
   - Command whitelisting
   - Directory sandboxing
   - Output truncation

5. Data Flow
   - Document ingestion flow
   - Search query flow
   - Response aggregation

6. Technology Stack
   - FastMCP (MCP server framework)
   - ChromaDB (vector database)
   - Chonkie (semantic chunking)
   - Python 3.13

---

### 3. `CONFIGURATION.md` (NEW FILE)

**Purpose**: Complete configuration reference

**Sections**:
1. Environment Variables
   - `LIBRARIAN_BACKEND` (chroma/chonkie)
   - `LIBRARIAN_SAFE_DIR`
   - `LIBRARIAN_DOCUMENTS_DIR`
   - `LIBRARIAN_CHROMA_PATH`
   - `LIBRARIAN_METADATA_PATH`
   - `LIBRARIAN_MAX_DOCUMENT_SIZE`
   - `LIBRARIAN_CHUNK_SIZE`
   - `LIBRARIAN_MAX_OUTPUT_CHARS`
   - `LIBRARIAN_COMMAND_TIMEOUT`

2. Command-Line Arguments
   - `--safe-dir`
   - `--documents-dir`
   - `--chroma-path`
   - `--metadata-path`

3. Backend Selection
   - **Chonkie is DEFAULT** (intelligent chunking, better search results)
   - ChromaDB backend available (simple chunking, faster processing)
   - When to use each backend
   - How to switch via `LIBRARIAN_BACKEND` environment variable

4. Why venv Instead of Docker
   - **Simpler installation** (no Docker complexity)
   - **Close coupling** between Chonkie and ChromaDB
   - **Better performance** (stdio transport vs HTTP overhead)
   - **Easier debugging** (direct Python access)
   - **Lower resource usage** (no container overhead)

5. `.librarianignore` File
   - Pattern syntax
   - Built-in patterns
   - Custom patterns

---

### 4. `SECURITY.md` (Rewrite of SECURITY_AND_BOUNDARIES.md)

**Purpose**: Security model and boundaries

**Keep From Original**:
- Librarian persona principles
- `.librarianignore` documentation
- Command whitelisting details

**Add**:
- Current tool count (13 tools total: 7 library + 6 CLI)
- Backend isolation (both backends respect security)
- File size limits
- Timeout protections

**Update**:
- Remove any "planned" features (Chonkie is implemented)
- Update any references to "current" system

---

### 5. `QUICKSTART.md` (Minor Updates)

**Changes Required**:
- Add note about backend selection
- Update feature list to mention Chonkie option
- Ensure all commands work with current system

---

### 6. Archive `IMPLEMENTATION_SUMMARY.md`

**Action**: Move to `.old-docs/`

**Reason**: This document describes Phase 1 implementation. It's historically interesting but misleading as current documentation.

---

## Implementation Todo List

### Phase 1: Planning ✅ (THIS DOCUMENT)
- [x] Assess current documentation state
- [x] Identify outdated content
- [x] Propose new structure
- [x] Create detailed rewrite plan

### Phase 2: Create New Core Documents
- [ ] Write `ARCHITECTURE.md` (new comprehensive technical overview)
- [ ] Write `CONFIGURATION.md` (new configuration reference)
- [ ] Rewrite `README.md` (emphasize Phase 2 complete, dual backends)
- [ ] Rewrite `SECURITY.md` (update and rename from SECURITY_AND_BOUNDARIES.md)

### Phase 3: Update Existing Documents
- [ ] Review and update `QUICKSTART.md` (add backend selection note)
- [ ] Review `USER_GUIDE.md` (update if needed)
- [ ] Verify `Tools.md` is current (likely already good)

### Phase 4: Organize Phase 2 Documentation
- [ ] Create `PHASE2/` directory
- [ ] Move `CHONKIE_INTEGRATION.md` to `PHASE2/`
- [ ] Move `CHONKIE_MIGRATION.md` to `PHASE2/`

### Phase 5: Archive and Cleanup
- [ ] Move `IMPLEMENTATION_SUMMARY.md` to `.old-docs/`
- [ ] Delete `SECURITY_AND_BOUNDARIES.md` (replaced by `SECURITY.md`)
- [ ] Verify all old docs mention current state correctly

### Phase 6: Verification
- [ ] Test librarian with query: "What is the librarian-mcp system?"
- [ ] Verify librarian describes Phase 2 system correctly
- [ ] Verify librarian mentions both backends
- [ ] Verify librarian cites correct documentation files
- [ ] Rebuild library with new documentation
- [ ] Test multiple queries to ensure accuracy

---

## Success Criteria

### Must Have (Non-Negotiable)
1. ✅ Librarian describes **Phase 2 complete system** (not Phase 1)
2. ✅ Librarian mentions **both backends** are available
3. ✅ Librarian explains **backend selection** is possible
4. ✅ All citations reference **current architecture**
5. ✅ No documentation describes Chonkie as "planned" or "future"

### Should Have (Important)
1. ✅ Clear architecture overview in one place (`ARCHITECTURE.md`)
2. ✅ Complete configuration reference (`CONFIGURATION.md`)
3. ✅ Security model clearly documented
4. ✅ Quick start actually works with current system

### Nice to Have (Enhancements)
1. ✅ Performance comparison between backends
2. ✅ Use case examples for each backend
3. ✅ Migration guide from Phase 1 to Phase 2
4. ✅ Troubleshooting section

---

## Key Facts to Emphasize in All Documentation

### Current System State (Phase 2 Complete)
- ✅ **Chonkie DEFAULT Backend**: Intelligent semantic chunking out of the box
- ✅ **ChromaDB Optional**: Simple chunking available via `LIBRARIAN_BACKEND=chroma`
- ✅ **Backend Factory Pattern**: Switch backends via environment variable
- ✅ **13 MCP Tools**: 7 library tools + 6 CLI tools
- ✅ **Semantic Search**: Vector embeddings via ChromaDB
- ✅ **Change Detection**: SHA-256 checksums
- ✅ **Security Boundaries**: `.librarianignore` with 94+ patterns
- ✅ **venv Not Docker**: Simplified deployment, close Chonkie-ChromaDB coupling
- ✅ **Production Ready**: Fully deployed and tested
- ✅ **AI Creativity**: See "Poem_Chonkie_Hippo_Spontaneous.md" for example

### What Changed from Phase 1 to Phase 2
- **Added**: Chonkie backend (`chonkie_backend.py`) - **NOW DEFAULT**
- **Added**: Backend factory (`factory.py`)
- **Enhanced**: Intelligent semantic chunking (Chonkie vs simple sentence chunking)
- **Enhanced**: Better search results through semantic chunk boundaries
- **Maintained**: All existing ChromaDB backend functionality (as optional fallback)
- **Maintained**: All security features
- **Maintained**: All tools and interfaces
- **Deployed**: venv-based installation (not Docker) for simplicity and close coupling

### What DIDN'T Change
- Document manager (`document_manager.py`)
- Metadata store (`metadata_store.py`)
- Ignore patterns (`ignore_patterns.py`)
- Library tools (`library_tools.py`)
- CLI tools (`cli_tools.py`)
- AI layer (`ai_layer_interface.py`)
- Configuration (`settings.py`)
- MCP server entry point (`librarian_mcp.py`)

---

## Notes

- **reco.md**: Already archived to `.old-docs/` ✅
- **PHASE2.md**: Already archived to `.old-docs/` ✅
- **prompt.md**: Keep at root (current system prompt) ✅
- **Poem_Chonkie_Hippo_Spontaneous.md**: Keep at root (selling point, mention in README) ✅
- **Default backend**: **Chonkie** (intelligent chunking) - CHANGE FROM `settings.py`
- **ChromaDB backend**: Available as optional fallback via `LIBRARIAN_BACKEND=chroma`
- **venv vs Docker**: venv approach enables close coupling, simpler deployment
- **Code is truth**: Verify all statements against actual implementation

---

## Next Steps

1. **Review this plan** - Ensure it addresses all issues
2. **Execute Phase 2** - Create new core documents
3. **Execute Phase 3** - Update existing documents
4. **Execute Phase 4** - Organize Phase 2 docs
5. **Execute Phase 5** - Archive and cleanup
6. **Execute Phase 6** - Verify and test

**Estimated Time**: 2-3 hours for complete rewrite and verification

**Priority**: CRITICAL - System credibility depends on accurate documentation
