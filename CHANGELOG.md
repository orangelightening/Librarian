# Changelog

All notable changes to Librarian MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-22

### Added
- **PDF Support**: Full PDF processing with pypdf and docling fallback
- **Multi-Library Architecture**: Support for multiple independent document collections
- **File-Type-Aware Chunking**: Different processing for PDFs, DOCX, Markdown, and code files
- **Token-Based Chunking**: 512-token chunks using Chonkie SemanticChunker
- **User Documentation**: Multi-library setup guide and MCP config templates
- **Enhanced Metadata**: Source tracking and file type information

### Changed
- **Default Backend**: Chonkie is now the recommended backend (was ChromaDB)
- **Chunking Quality**: Semantic coherence replaces simple character-based splitting
- **Document Manager**: Uses `add_document_pipeline()` for file-type-aware processing
- **PDF Extraction**: pypdf for fast extraction, docling for complex layouts/OCR

### Fixed
- **Path Validation**: IgnorePatterns now work with any root directory
- **Multi-Library Isolation**: Each library has independent `.librarian/` directory
- **UUID Generation**: Fixed uuid5() error in Chonkie backend

### Technical
- **ChonkieBackend**: New backend using Chonkie's SemanticChunker
- **Pipeline Processing**: File-type-aware text extraction before chunking
- **Metadata Store**: Per-library metadata isolation
- **Ignore Patterns**: Configurable root path for multi-library support

## [0.2.1] - Previous Release

### Features
- ChromaDB backend with character-based chunking
- Basic document management (add, remove, sync)
- Semantic search with ChromaDB embeddings
- CLI tools with security features
- MCP tool integration

---

## Migration Guide

### From v0.2.1 to v0.3.0

**Breaking Changes**: None - backward compatible

**Recommended Changes**:
1. **Switch to Chonkie backend**: Set `LIBRARIAN_BACKEND=chonkie` in environment
2. **Re-index documents**: Run `sync_documents()` to use improved chunking
3. **Update MCP configs**: Use new templates from `docs/MCP_CONFIG_TEMPLATES.md`

**Multi-Library Setup**:
1. Create separate directories for each library
2. Configure one MCP server per library
3. Toggle servers on/off as needed (or use separate assistants)

**PDF Support**:
- PDFs now indexed automatically with Chonkie backend
- Tables and complex layouts handled via docling
- No manual text extraction required

---

## Future Plans

### v0.4.0 (Planned)
- Tool prefixing to support multiple libraries simultaneously
- Unified MCP server with library selection parameter
- Improved chunking strategies for code files
- Web UI for library management

### v1.0.0 (Roadmap)
- REST API for library operations
- Real-time sync with file system watcher
- Advanced analytics and usage metrics
- Cloud backup/sync options
