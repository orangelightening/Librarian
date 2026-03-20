# Query 10: Search Architecture

**Status**: success
**Tokens Used**: 392
**Timestamp**: 2026-03-18T23:33:16.593418
**Tool Calls**: 0

---

Based on the library, here's how semantic search works in the librarian-mcp system:

## Core Architecture

**[Source: architecture.md]**
The system uses **ChromaDB** for vector storage and implements semantic search through the following pipeline:

1. **Document Chunking**: Documents are chunked into segments (typically 1000 characters) using either:
   - **Chonkie** (default): Intelligent semantic-aware chunking that respects document structure
   - **Simple approach**: Sentence-based splitting for basic documents

2. **Vector Embedding**: Each chunk is converted to a vector embedding using ChromaDB's default embedding function

3. **Vector Storage**: Chunks are stored in ChromaDB with metadata including:
   - Document ID and path
   - Chunk index and size
   - Token and character counts

4. **Semantic Search**: When you search, the system:
   - Converts your query to a vector
   - Performs vector similarity matching in ChromaDB
   - Returns top 5 results ranked by similarity score

5. **Result Aggregation**: The AI layer aggregates the chunks, sorts them by relevance, and builds a coherent response with automatic citations

**[Source: features.md]**
The system also includes automatic change detection via SHA-256 checksums, ensuring modified documents are re-indexed automatically.

Would you like me to explain any specific aspect in more detail, such as the chunking strategy or how citations are generated?
