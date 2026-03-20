# Response 10: How Semantic Search Works in the Librarian-MCP System

## Summary

The librarian-mcp implements semantic search using a **two-stage pipeline**: document chunking followed by vector similarity matching in ChromaDB. This enables meaningful, context-aware search rather than simple keyword matching.

## Architecture Overview

```
User Query
    ↓
Query Embedding (vector representation)
    ↓
ChromaDB Vector Similarity Search
    ↓
Top N Chunks Returned (with similarity scores)
    ↓
AILayer Aggregation
    ↓
Formatted Response with Citations
```

## Stage 1: Document Chunking

Documents are split into smaller, meaningful segments before embedding:

### Backend Options

The system supports two backends for chunking:

**1. Chonkie Backend (Default)**
- **Intelligent semantic-aware chunking** using Chonkie library
- **Recursive chunking**: Splits documents intelligently based on structure
- **Configuration**:
  ```python
  chunk_size = 1000  # Target chunk size in characters
  min_chunk_size = 50  # Minimum characters per chunk
  ```
- **Benefits**:
  - Respects sentence and paragraph boundaries
  - Preserves context and related concepts
  - Avoids breaking mid-thought
  - Better search relevance

[Source: chonkie_backend.py]

**2. ChromaDB Backend (Fallback)**
- **Simple sentence-by-sentence splitting**
- **Fixed-size chunks**: 1000-character segments
- **No semantic awareness**: Treats all text uniformly
- **Use case**: When processing speed is prioritized over search quality

[Source: CHONKIE_MIGRATION.md]

## Stage 2: Vector Embedding and Storage

Each chunk is converted to a vector representation and stored in ChromaDB:

### Embedding Process

1. **Text to Vector**: Each chunk text is converted to a numerical vector using ChromaDB's embedding function
2. **Metadata Tagging**: Each vector is tagged with:
   - Document ID
   - Chunk index (position within document)
   - Character/token count
   - Chunking method used
   - Source file name

3. **Vector Storage**: All vectors are stored in ChromaDB with cosine similarity enabled

[Source: chonkie_backend.py]

## Stage 3: Semantic Search Execution

When a user searches:

### Query Processing

1. **Query Embedding**: The search query text is converted to a vector
2. **Vector Similarity**: ChromaDB calculates cosine similarity between the query vector and all stored chunk vectors
3. **Top Results**: The system returns the top N chunks (default 5) with their similarity scores

### Ranking

Chunks are ranked by:
- **Cosine similarity score**: Higher scores = more relevant
- **Contextual relevance**: Semantically similar content appears first

[Source: search_library results]

## Stage 4: Result Aggregation

The **AILayer** aggregates search results into a coherent response:

### Aggregation Process

1. **Sort by Similarity**: Results are ordered from highest to lowest similarity score
2. **Build Response**: Content from relevant chunks is combined into a coherent answer
3. **Generate Citations**: Each source document is cited automatically
4. **Format Output**: Results are returned in a structured format

### Output Format

```
Found 5 relevant chunks.

[1] Chunk text excerpt... [Source: ARCHITECTURE.md]
[2] Chunk text excerpt... [Source: README.md]
...
```

[Source: search_library results]

## Key Technical Components

### ChromaDB Configuration

- **Collection**: Documents collection for chunk storage
- **Similarity**: Cosine similarity (configured in metadata)
- **Storage**: Persistent vector database

[Source: chonkie_backend.py]

### Metadata Structure

Each chunk is stored with metadata including:
- `chunk_index`: Position within the document
- `document_id`: Unique document identifier
- `document_name`: Source filename
- `token_count`: Number of tokens in the chunk
- `char_count`: Number of characters in the chunk
- `chunking_method`: How the chunk was created

[Source: chonkie_backend.py]

## Benefits of Semantic Search

1. **Context-Aware**: Finds content based on meaning, not just keywords
2. **Flexible**: Works across different terminology and phrasing
3. **Accurate**: Returns relevant chunks even with different wording
4. **Scalable**: Handles large document collections efficiently

## Summary

The librarian-mcp's semantic search system works by:
1. **Chunking** documents into semantic segments (Chonkie or simple)
2. **Embedding** each chunk into a vector representation
3. **Storing** vectors in ChromaDB with cosine similarity
4. **Searching** with query vectors to find similar chunks
5. **Aggregating** results into a coherent response with citations

This approach enables the Librarian to understand and retrieve information based on meaning rather than simple text matching.

---
**Primary Sources**:
- `/home/peter/development/librarian-mcp/mcp_server/backend/chonkie_backend.py`
- `/home/peter/development/librarian-mcp/ARCHITECTURE.md`
- `/home/peter/development/librarian-mcp/PHASE2/CHONKIE_MIGRATION.md`