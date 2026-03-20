# Document-Type Specific Chunking with Chonkie

**Created**: 2026-03-20
**Status**: Planned
**Priority**: Medium
**Effort Estimate**: 1-2 weeks

---

## Overview

Implement document-type specific chunking strategies using the Chonkie backend. Different document types have different optimal chunking strategies - code should chunk at function boundaries, markdown at headers, PDFs should preserve tables, etc.

## Problem Statement

Current RecursiveChunker treats all documents equally, but different document types have different optimal chunking strategies:

**PDFs with tables**:
- Need table-aware chunking
- Preserve row/column relationships
- Don't break table structures

**DOCX documents**:
- Have heading structures
- Section-based chunking better
- Respect document hierarchy

**Code files**:
- Should chunk at function/class boundaries
- Preserve code blocks
- Syntax-aware splitting

**Markdown files**:
- Already have semantic structure
- Header-based chunking
- Preserve section relationships

**HTML documents**:
- Tag-based structure
- Element-aware chunking
- Preserve semantic HTML

## Implementation

### File Type Detection

```python
# mcp_server/backend/chonkie_backend.py

from chonkie import Chunker

DOCUMENT_CHUNKERS = {
    '.pdf': PDFChunker,           # Table-aware, preserves structure
    '.docx': DOCXChunker,         # Heading-aware, respects sections
    '.py': PythonCodeChunker,     # Function/class boundaries
    '.js': JavaScriptCodeChunker, # Module/function boundaries
    '.md': MarkdownChunker,       # Header-based chunking
    '.html': HTMLChunker,         # Tag-aware chunking
    '.txt': RecursiveChunker,     # Default: sentence-based
}

def get_chunker_for_file(file_path: str) -> Chunker:
    """Get appropriate chunker for file type"""
    ext = Path(file_path).suffix.lower()
    chunker_class = DOCUMENT_CHUNKERS.get(ext, RecursiveChunker)

    # Initialize chunker with default parameters
    return chunker_class(
        chunk_size=1000,
        chunk_overlap=200
    )
```

### Chonkie Chunkers Available

From the Chonkie SDK:
- `RecursiveChunker` - Current default, sentence-based
- `SemanticChunker` - Requires embeddings, semantic boundaries
- `TokenChunker` - Fixed token chunks
- `SentenceChunker` - Sentence-based
- `CodeChunker` - Code-aware (for .py, .js, .ts, etc.)
- `PDFChunker` - PDF with table preservation
- `MarkdownChunker` - Markdown header-aware
- `HTMLChunker` - HTML tag-aware

### Backend Integration

```python
# mcp_server/backend/chonkie_backend.py

class ChonkieBackend(DocumentBackend):
    def __init__(self, collection_name: str = "documents", db_path: str = "./chroma_db"):
        # Initialize Chonkie with default chunker
        self.default_chunker = RecursiveChunker(
            chunk_size=1000,
            chunk_overlap=200
        )
        # ... rest of initialization

    def chunk_documents(self, documents: List[Document], document_ids: List[str], source: str = None) -> Dict[str, Any]:
        """Chunk documents using type-specific chunkers"""
        all_chunks = []

        for doc, doc_id in zip(documents, document_ids):
            # Get chunker for this file type
            chunker = get_chunker_for_file(doc.file_path)

            # Chunk with type-specific strategy
            chunks = chunker.chunk(doc.content)

            # Create chunk metadata
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    'text': chunk.text,
                    'metadata': {
                        'source': source or doc.file_path,
                        'document_id': doc_id,
                        'chunk_index': i,
                        'file_type': Path(doc.file_path).suffix,
                        'chunking_strategy': chunker.__class__.__name__
                    }
                })

        # Embed and add to ChromaDB
        # ... existing embedding logic

        return {
            'total_chunks': len(all_chunks),
            'documents_processed': len(documents)
        }
```

## Benefits

- **Better search results**: Code finds full functions, not fragments
- **Preserved structures**: Tables remain intact
- **Respected semantics**: Document structure guides chunking
- **Improved quality**: Specialized handling per document type

## Configuration

Optional: Allow users to configure chunking per type:

```python
# config/chunking.yaml
chunking_strategies:
  pdf:
    chunk_size: 1500
    chunk_overlap: 300
    preserve_tables: true

  code:
    chunk_size: 800
    chunk_overlap: 100
    respect_function_boundaries: true

  markdown:
    chunk_size: 1200
    chunk_overlap: 200
    header_based: true
```

## Testing

Test chunking quality with different document types:

```bash
# Test PDF chunking
python scripts/test_chunking.py --type pdf --file sample.pdf

# Test code chunking
python scripts/test_chunking.py --type code --file sample.py

# Test markdown chunking
python scripts/test_chunking.py --type md --file sample.md
```

## Success Criteria

- [ ] Different document types use appropriate chunkers
- [ ] Code files chunk at function/class boundaries
- [ ] Markdown files chunk at headers
- [ ] PDF tables preserved intact
- [ ] Search results improve for code queries
- [ ] No regression in text file chunking

## Dependencies

- Chonkie SDK (already installed)
- File type detection via `pathlib`
- Document type handlers

## Implementation Steps

1. Add `get_chunker_for_file()` function to `chonkie_backend.py`
2. Import Chonkie chunker classes
3. Modify `chunk_documents()` to use type-specific chunkers
4. Add file type metadata to chunks
5. Test with different document types
6. Validate search quality improvements

## Future Enhancements

- User-configurable chunking strategies
- Automatic chunk size optimization
- Hybrid chunking (semantic + structure-based)
- Chunk quality metrics
