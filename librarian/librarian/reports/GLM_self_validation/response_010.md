# Query 10: How does semantic search work in the librarian-mcp system?

Semantic search in the librarian-mcp system is implemented through a multi-stage architecture that combines vector embeddings, intelligent chunking, and AI-powered result aggregation.

## Architecture Overview

The semantic search process follows this flow:

1. **User Query** → `search_library(query="...", limit=5)`
2. **Backend Processing** → `Backend.query(query_text, limit)`
3. **ChromaDB Semantic Search** → Vector similarity matching
4. **Result Return** → Top chunks with scores
5. **AI Aggregation** → Sort, build response, generate citations
6. **Formatted Output** → Results with source citations `[Source: ARCHITECTURE.md]`

## Document Chunking

Documents are processed into searchable chunks using one of two backends:

### Chonkie Backend (Default)
- **Intelligent semantic-aware chunking** with configurable parameters
- Uses `RecursiveChunker(chunk_size=1000, min_characters_per_chunk=50)`
- Creates 1000-character segments with a minimum of 50 characters per chunk
- Respects sentence and paragraph structure naturally
- Avoids cutting through the middle of concepts or sentences `[Source: ARCHITECTURE.md]`

### ChromaDB Backend (Optional)
- Simple sentence-based chunking (original implementation)
- Splits by sentence boundaries
- More predictable chunk sizes but less semantic awareness `[Source: ARCHITECTURE.md]`

Backend selection is configured via the `LIBRARIAN_BACKEND` environment variable:
- `chonkie` (default): Intelligent semantic chunking
- `chroma`: Simple sentence-based chunking

## Vector Embedding & Storage

All document chunks are embedded as vectors and stored in ChromaDB, which serves as the vector database backend `[Source: ARCHITECTURE.md]` `[Source: README.md]`.

## Search Process

When a user performs a semantic search:

1. The query text is embedded into a vector
2. ChromaDB performs **vector similarity matching**
3. Top chunks (default: 5) are returned with similarity scores
4. Results are ranked by similarity score `[Source: ARCHITECTURE.md]`

## Result Aggregation

The **AILayer** aggregates the search results to provide a coherent response:

- **Sorts chunks** by similarity score
- **Builds a coherent response** from relevant chunks
- **Generates automatic citations** for each source document
- **Returns formatted results** with source references and relevance scores `[Source: ARCHITECTURE.md]`

## Key Features

- **Semantic understanding**: Not just text matching - the system understands meaning through vector embeddings
- **Citation generation**: Every answer references source documents automatically
- **Relevance scoring**: Results are ranked by semantic similarity to the query
- **Configurable chunking**: Balance between semantic quality and processing speed
- **Two backend options**: Choose between Chonkie (semantic quality) or ChromaDB (speed) based on needs `[Source: README.md]` `[Source: ARCHITECTURE.md]`

## Why Chonkie is Preferred

Chonkie's semantic-aware chunking provides better search quality because:
- It maintains context within chunks
- It respects natural language boundaries
- It preserves semantic coherence of content
- It results in more relevant search results `[Source: ARCHITECTURE.md]`
