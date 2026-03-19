# Librarian MCP Server - Phase 2 Development Plan

## Executive Summary

Phase 1 successfully delivered a fully functional Librarian MCP server with semantic search, document lifecycle management, and secure CLI access. Phase 2 focuses on **improving core functionality** - specifically integrating Chonkie for better document processing and search quality.

## Primary Goal: Chonkie Integration

**Why Chonkie?**
- Complete pipeline with document loading and chunking
- Better semantic understanding of document structure
- Improved handoff to ChromaDB for better search results
- Handles complex document formats intelligently
- Reduces custom code we need to maintain

**Why Not Docker First?**
- Current installation is manageable with AI assistance
- Stdio performance is better than HTTP
- Docker adds complexity for marginal benefit
- Time better spent on improving search quality
- Docker always available as backup if needed later

**Problem**: Current installation requires:
- Command line comfort
- Python knowledge
- Virtual environment setup
- Manual configuration
- ~15-30 minutes for tech-savvy users
- Not accessible to non-technical users

**Solution**: Docker containerization with one-command installation

### Target User Experience

```bash
# That's it - everything else is automatic
git clone https://github.com/yourusername/librarian-mcp.git
cd librarian-mcp
docker compose up -d
```

**What this provides**:
- ✅ Pre-configured container with all dependencies
- ✅ No Python installation required
- ✅ No virtual environment management
- ✅ Automatic startup on system boot (optional)
- ✅ Easy web-based configuration interface
- ✅ One-command updates
- ✅ Cross-platform compatibility (Linux, Mac, Windows)
- ✅ Installation time: ~2-3 minutes

---

## Chonkie Integration Plan

### Architecture

**Current Architecture (Phase 1)**:
```
Document → Custom Chunker → ChromaDB → Search
```

**New Architecture (Phase 2)**:
```
Document → Chonkie Pipeline → ChromaDB → Better Search
```

### Why Chonkie?

**Benefits**:
- ✅ **Smart document loading** - handles PDFs, DOCX, HTML, etc.
- ✅ **Intelligent chunking** - understands document structure
- ✅ **Better semantic boundaries** - doesn't break mid-sentence/mid-concept
- ✅ **Multi-modal support** - handles images, tables, code blocks
- ✅ **Proven pipeline** - battle-tested, actively maintained
- ✅ **Less custom code** - reduces our maintenance burden

**What Chonkie Provides**:
```python
from chonkie import Document, Tokenizer, SemanticChunker

# Document loading
doc = Document.load("path/to/file.pdf")  # PDF, DOCX, HTML, TXT, etc.

# Intelligent chunking
chunker = SemanticChunker(
    tokenizer="gpt-4",
    chunk_size=1000,
    overlap=200
)
chunks = chunker.chunk(doc)

# Ready for ChromaDB
for chunk in chunks:
    chroma_db.add(
        documents=[chunk.text],
        metadatas=[chunk.metadata]
    )
```

### Implementation Strategy

**Step 1: Backend Implementation**

Create `mcp_server/backend/chonkie_backend.py`:

```python
"""
Chonkie-based document backend.
Handles document loading, intelligent chunking, and ChromaDB storage.
"""
from chonkie import Document, SemanticChunker
from .base import ChunkingBackend
from .chroma_backend import ChromaBackend

class ChonkieBackend(ChunkingBackend):
    """Backend using Chonkie for document processing."""

    def __init__(self, collection_name="documents"):
        """
        Initialize Chonkie backend.

        Chonkie handles document loading and chunking,
        then hands off to ChromaDB for storage and search.
        """
        self.chunker = SemanticChunker(
            tokenizer="gpt-4",  # or local model
            chunk_size=1000,
            overlap=200
        )
        self.chroma = ChromaBackend(collection_name)

    def chunk_documents(self, documents, document_ids=None, source="upload"):
        """
        Process documents using Chonkie's intelligent pipeline.

        Args:
            documents: List of document paths or text content
            document_ids: Optional list of document IDs
            source: Source identifier for metadata

        Returns:
            List of chunks with metadata
        """
        all_chunks = []

        for i, doc in enumerate(documents):
            # Load document (Chonkie handles different formats)
            if isinstance(doc, str) and Path(doc).exists():
                document = Document.load(doc)
            else:
                document = Document(text=doc, metadata={"source": source})

            # Intelligent chunking
            chunks = self.chunker.chunk(document)

            # Prepare for ChromaDB
            for chunk in chunks:
                all_chunks.append({
                    "text": chunk.text,
                    "metadata": {
                        "document_id": document_ids[i] if document_ids else f"doc_{i}",
                        "source": source,
                        "chunk_index": chunk.index,
                        "page": chunk.page,
                        "section": chunk.section,
                        **chunk.metadata
                    }
                })

        # Store in ChromaDB
        self.chroma.collection.add(
            documents=[c["text"] for c in all_chunks],
            metadatas=[c["metadata"] for c in all_chunks],
            ids=[f"{c['metadata']['document_id']}_{c['metadata']['chunk_index']}"
                 for c in all_chunks]
        )

        return all_chunks

    def query(self, query_text, limit=5):
        """Query using ChromaDB (same as before)."""
        return self.chroma.query(query_text, limit)

    def delete_documents(self, document_id):
        """Delete document chunks."""
        return self.chroma.delete_documents(document_id)

    def get_stats(self):
        """Get collection statistics."""
        return self.chroma.get_stats()
```

**Step 2: Backend Selection**

Already implemented in our settings! Just need to add Chonkie to requirements:

```python
# mcp_server/config/settings.py
BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chroma")
```

**Step 3: Factory Pattern**

```python
# mcp_server/backend/factory.py
def get_backend():
    """Get configured backend instance."""
    from ..config.settings import settings

    if settings.BACKEND == "chonkie":
        from .chonkie_backend import ChonkieBackend
        return ChonkieBackend()
    else:
        from .chroma_backend import ChromaBackend
        return ChromaBackend()
```

**Step 4: Dependencies**

```bash
# Add to requirements.txt
chonkie>=0.2.0  # Check latest version
```

### Testing Strategy

**Unit Tests**:
```python
def test_chonkie_pdf_loading():
    """Test PDF document loading."""
    backend = ChonkieBackend()
    chunks = backend.chunk_documents(["test/document.pdf"])
    assert len(chunks) > 0
    assert all("text" in c for c in chunks)

def test_chonkie_chunking_quality():
    """Test that chunks respect semantic boundaries."""
    backend = ChonkieBackend()
    doc = "Introduction. \n\nThis is a complete section. \n\nConclusion."
    chunks = backend.chunk_documents([doc])
    # Chonkie should not break mid-sentence
    for chunk in chunks:
        assert not chunk["text"].startswith(" ")
        assert not chunk["text"].endswith(" ")
```

**Integration Tests**:
- Load real PDFs, DOCX, HTML files
- Verify chunk quality
- Check search relevance
- Compare with current ChromaDB chunking

**Performance Tests**:
- Processing speed (docs/second)
- Memory usage
- Search quality improvements

### Expected Benefits

**Better Search Results**:
- More relevant chunks = better matches
- Proper semantic boundaries = coherent context
- Multi-format support = more documents indexed

**Reduced Maintenance**:
- Less custom chunking code
- Chonkie handles edge cases
- Active development and updates

**Enhanced Capabilities**:
- PDF support (with images, tables)
- DOCX support
- HTML/web page support
- Code syntax highlighting preservation

---

## Additional Phase 2 Features (Lower Priority)

### 2. Web-Based Configuration Interface

**Purpose**: Make configuration accessible without editing JSON files

**Features**:
- Visual configuration editor
- Safe directory selection
- Document source management
- Library statistics dashboard
- Search query interface
- Real-time log viewing

**Tech Stack**:
- FastAPI (already in dependencies)
- Simple HTML/JavaScript frontend
- RESTful API for configuration

**Endpoints**:
```
GET  /config          # Get current configuration
POST /config          # Update configuration
GET  /stats           # Library statistics
POST /sync            # Trigger document sync
GET  /logs            # Server logs
```

### 3. Enhanced Backend Options

**Chonkie Integration** (from original Phase 2 plan):
- Implement `mcp_server/backend/chonkie_backend.py`
- Easy backend switching via environment variable
- Improved chunking quality
- Better semantic search results

### 4. Backup and Restore

**Automated Backups**:
- Scheduled database backups
- Export library as JSON/tarball
- One-click restore
- Migration utilities

**Implementation**:
```bash
# Backup
docker exec librarian-mcp python scripts/backup.py --output /backups/librarian-$(date +%Y%m%d).tar.gz

# Restore
docker exec librarian-mcp python scripts/restore.py --input /backups/librarian-20250316.tar.gz
```

### 5. Monitoring and Logging

**Health Monitoring**:
- Container health checks
- Library statistics API
- Performance metrics
- Error tracking

**Logging Improvements**:
- Structured logging (JSON format)
- Log rotation
- Remote logging options (Syslog, etc.)
- Query execution logging

### 6. Multi-User Support

**User Isolation**:
- Separate libraries per user
- Access control lists
- Per-user safe directories
- Usage quotas and limits

**Implementation**:
- User authentication (optional)
- Per-user ChromaDB collections
- Isolated document storage

---

## Development Priorities

### Priority 1: Chonkie Integration (Must Have)
- Implement `chonkie_backend.py`
- Add to requirements.txt
- Backend factory pattern
- Comprehensive testing
- Performance comparison vs. current chunking
- Documentation and migration guide

**Estimated Time**: 1 week

### Priority 2: Search Quality Improvements (Should Have)
- Better chunking strategies
- Improved citation accuracy
- Multi-document synthesis
- Context window optimization
- Query refinement suggestions

**Estimated Time**: 1-2 weeks

### Priority 3: Enhanced Document Processing (Nice to Have)
- PDF with images/tables
- DOCX support
- HTML/web page indexing
- Code file improvements
- Metadata extraction

**Estimated Time**: 1 week

### Priority 4: Backup/Restore (Nice to Have)
- Backup scripts
- Restore functionality
- Export/import utilities

**Estimated Time**: 2-3 days

### Priority 5: Enhanced Monitoring (Nice to Have)
- Health checks
- Statistics API
- Log improvements

**Estimated Time**: 1-2 days

### Priority 6: Docker Installation (Maybe Later)
- Dockerfile and docker-compose.yml
- Installation scripts (Linux/Mac/Windows)
- Documentation updates
- Testing on all platforms
- Only if we have bandwidth after core improvements

**Estimated Time**: 2-3 days (if we do it)

---

## Testing Plan

### Docker Testing
- [ ] Build succeeds on all platforms
- [ ] Container starts correctly
- [ ] Data persistence works
- [ ] MCP client can connect
- [ ] Installation scripts work
- [ ] Resource limits are respected

### Web UI Testing
- [ ] Configuration changes persist
- [ ] Safe directory updates work
- [ ] Document sync triggers correctly
- [ ] Statistics are accurate
- [ ] Logs display properly

### Cross-Platform Testing
- [ ] Ubuntu/Debian Linux
- [ ] macOS (Intel and Apple Silicon)
- [ ] Windows 10/11

---

## Documentation Updates

### New Documentation Files
- `DOCKER_INSTALL.md` - Docker installation guide
- `WEB_UI_GUIDE.md` - Web interface documentation
- `BACKUP_RESTORE.md` - Backup and restore procedures
- `TROUBLESHOOTING.md` - Common issues and solutions

### Updated Documentation
- `README.md` - Emphasize Docker installation
- `USER_GUIDE.md` - Add Docker instructions
- `CLAUDE.md` - Docker-specific guidance

---

## Migration Strategy

### For Existing Users
- Continue supporting manual installation
- Provide migration guide to Docker
- Export/import utilities for data
- Backward compatibility maintained

### For New Users
- Docker installation as default method
- Manual installation as "advanced" option
- Clear installation path recommendations

---

## Success Metrics

### Search Quality
- ✅ **Better relevance**: More accurate search results
- ✅ **Improved citations**: Proper attribution to sources
- ✅ **Coherent chunks**: Semantic boundaries respected
- ✅ **Multi-format support**: PDF, DOCX, HTML indexed correctly

### Performance
- Processing speed: Maintain or improve current throughput
- Memory usage: Reasonable overhead for Chonkie
- Search latency: No regression in query response time

### Reliability
- Document loading success rate > 95%
- No crashes on malformed documents
- Graceful error handling
- Backup/restore tested

### Functionality
- All existing features work with Chonkie backend
- Easy switching between ChromaDB and Chonkie backends
- Migration path for existing libraries

---

## Risks and Mitigations

### Risk: Docker Learning Curve
**Mitigation**: Provide one-line installation scripts, detailed documentation

### Risk: Resource Overhead
**Mitigation**: Use lightweight base image, set resource limits, optimize dependencies

### Risk: File System Permissions
**Mitigation**: Run as non-root user, clear documentation, automated permission fixes

### Risk: MCP Client Integration
**Mitigation**: Test with major clients, provide configuration examples, troubleshooting guide

---

## Timeline

### Phase 2.1: Chonkie Integration (1 week)
- Day 1-2: Backend implementation
- Day 3-4: Testing and validation
- Day 5: Documentation and migration guide

### Phase 2.2: Search Quality Improvements (1-2 weeks)
- Week 1: Chunking optimization, citation improvements
- Week 2: Multi-document synthesis, query refinement

### Phase 2.3: Enhanced Document Processing (1 week)
- PDF/DOCX/HTML support
- Code file improvements
- Metadata extraction

### Phase 2.4: Additional Features (1-2 weeks)
- Backup/restore utilities
- Monitoring and logging improvements

**Total Estimated Time**: 4-6 weeks for core improvements
**Docker**: Only if we have extra bandwidth (not in critical path)

---

## Next Steps

1. **Review Chonkie documentation** - Understand API and capabilities
2. **Prototype Chonkie backend** - Test with sample documents
3. **Compare search quality** - Measure improvements vs. current chunking
4. **Implement production backend** - Full integration with metadata store
5. **Test and validate** - Comprehensive testing across document types
6. **Document migration path** - Help users upgrade from ChromaDB backend

---

**Document Version**: 2.0
**Date**: 2026-03-16
**Status**: Planning Phase - Ready for Implementation
**Priority**: HIGH - Chonkie integration will significantly improve search quality
**Note**: Docker installation deprioritized based on practical assessment
