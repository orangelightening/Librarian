# Query 10: Search Architecture

**Status**: success
**Tokens Used**: 1178
**Timestamp**: 2026-03-18T19:21:41.487266
**Tool Calls**: 6

---

I'll search the library for information about how semantic search works in the librarian-MCP system.


Great! I found relevant information about semantic search implementation. Let me read the full content of the architecture document to provide you with complete details.


Let me check what documents are currently indexed in the library and search for architecture-related files.


Perfect! I can see ARCHITECTURE.md is indexed. Let me read it to get the complete details about semantic search implementation.


Let me read more of the architecture document to get complete details about semantic search.


Now let me also check the README.md for additional context about semantic search.


Perfect! Now I have comprehensive information about how semantic search works in the librarian-MCP system. Let me provide you with a complete answer based on the library content.

---

Based on the library, **semantic search** in the Librarian MCP system is implemented using a sophisticated dual-backend architecture that combines intelligent document chunking with vector similarity matching. Here's how it works:

## Core Components

### 1. **Backend Architecture** [Source: ARCHITECTURE.md]
The system uses an abstract `DocumentBackend` interface with two implementation options:

- **ChonkieBackend (Default)**: Intelligent semantic chunking that respects document structure, sentence boundaries, and context preservation
- **ChromaDB Backend**: Simple sentence-based chunking for faster processing when speed is prioritized over quality

### 2. **Chunking Strategy** [Source: ARCHITECTURE.md]
Documents are processed into chunks before embedding:

```python
# Chonkie (default) - Intelligent semantic chunking
chunker = RecursiveChunker(
    chunk_size=1000,           # ~1000 character segments
    min_characters_per_chunk=50  # Minimum chunk size
)
chunks = chunker(document_text)

# ChromaDB fallback - Simple sentence splitting  
chunks = document_text.split('. ')
```

### 3. **Vector Embedding & Storage** [Source: ARCHITECTURE.md]
Chunks are stored in **ChromaDB vector store**:

```python
collection.add(
    documents=[chunk_text],
    ids=[chunk_id],
    metadatas=[metadata]
)
```

Each chunk is embedded as a vector, enabling semantic similarity matching rather than simple text matching.

### 4. **Search Query Flow** [Source: ARCHITECTURE.md]
When you call `search_library(query="...")`:

```
User query → Backend.query(query_text, limit)
    ↓ [ChromaDB semantic search]
    ↓ [vector similarity matching]
    ↓ [return top 5 chunks with scores]
    ↓ AILayer.aggregate_results(chunks, query)
    ↓ [sort by similarity score]
    ↓ [build response from chunks]
    ↓ [generate citations]
```

### 5. **Result Aggregation** [Source: ARCHITECTURE.md]
The AI Layer processes results:
- Sorts chunks by similarity score
- Builds coherent responses from relevant chunks
- Generates automatic citations in format `[Source: document_name.md]`
- Returns top N results (default: 5, configurable via `limit` parameter)

## Key Features

### **Intelligent Chunking** [Source: ARCHITECTURE.md]
The Chonkie backend provides:
- ✅ Semantic boundaries that respect sentence and paragraph structure
- ✅ Context preservation keeping related concepts together
- ✅ Intelligent sizing that adapts to document complexity
- ✅ Better search results through higher quality chunks

### **Change Detection** [Source: ARCHITECTURE.md]
Documents are tracked via SHA-256 checksums, ensuring modified documents are automatically re-indexed.

### **Backend Selection** [Source: README.md]
Switch backends instantly via environment variable:
```bash
export LIBRARIAN_BACKEND=chonkie  # Default - best quality
export LIBRARIAN_BACKEND=chroma   # Fast fallback option
```

## Summary

Semantic search works by:
1. **Chunking** documents intelligently (Chonkie) or simply (ChromaDB)
2. **Embedding** chunks as vectors in ChromaDB
3. **Matching** queries against vector similarity
4. **Aggregating** results with AI-driven sorting and citation generation

This approach enables the librarian to understand semantic meaning rather than just matching keywords, providing more accurate and contextually relevant search results.