# Query 10: Search Architecture

**Status**: success
**Tokens Used**: 1637
**Timestamp**: 2026-03-18T21:01:50.575198
**Tool Calls**: 6

---

I'll help you understand how semantic search works in the librarian-MCP system by searching the library for relevant documentation.


Great! I found relevant information about semantic search in the library. Let me get more detailed documentation by reading the key files that explain this mechanism.


Now let me read the architecture documentation to get complete details about how semantic search works.


Let me check what documents are available in the library first.


Perfect! I can see ARCHITECTURE.md is indexed. Let me read it to get the complete picture of how semantic search works.


Excellent! Now let me also read the AI layer interface to understand how results are aggregated and formatted.


Perfect! Now I have a comprehensive understanding of how semantic search works in the librarian-MCP system. Let me provide you with a detailed explanation based on the library documentation.

---

## How Semantic Search Works in the Librarian-MCP System

Based on the library documentation, here's a complete breakdown of the semantic search mechanism:

### **1. Core Components** [Source: ARCHITECTURE.md]

The system uses **ChromaDB as a vector database** for storing and retrieving document embeddings. The architecture consists of:

- **Document Backend Layer**: Handles chunking and embedding
- **AI Layer**: Aggregates results and formats citations
- **ChromaDB Vector Store**: Stores semantic representations of chunks

### **2. Document Chunking Strategy** [Source: ARCHITECTURE.md]

Documents are split into manageable pieces before being embedded:

#### **Default Backend (Chonkie)** - Intelligent Semantic Chunking:
```python
chunker = RecursiveChunker(chunk_size=1000, min_characters_per_chunk=50)
chunks = chunker(document_text)
```

**Key Features:**
- ✅ **Semantic boundaries**: Respects sentence and paragraph structure
- ✅ **Context preservation**: Related concepts stay together
- ✅ **Intelligent sizing**: Adapts to document complexity
- ✅ **Better search quality**: Higher quality chunks = more accurate matches

#### **Alternative Backend (Chroma)** - Simple Sentence Splitting:
```python
chunks = document_text.split('. ')  # Simple sentence splitting
```

**Use Cases:**
- When processing speed is prioritized over search quality
- For simple documents without complex structure
- As a fallback or for testing

### **3. Vector Embedding & Storage** [Source: ARCHITECTURE.md]

Both backends store chunks in ChromaDB with metadata:

```python
collection.add(
    documents=[chunk_text],
    ids=[chunk_id],
    metadatas=[metadata]
)
```

**Metadata includes:**
- `document_id`: Unique document identifier
- `document_name`: Source file name
- `chunk_index`: Position within the document
- `token_count` / `char_count`: Chunk size metrics
- `chunking_method`: Whether Chonkie or Chroma was used

### **4. Search Query Flow** [Source: ARCHITECTURE.md]

When you perform a semantic search, here's what happens:

```
User query → Backend.query(query_text, limit) 
    ↓ [ChromaDB vector similarity matching]
    ↓ [Returns top 5 chunks with similarity scores]
    ↓ AILayer.aggregate_results(chunks, query)
    ↓ [Sorts by similarity score]
    ↓ [Builds response from chunks]
    ↓ [Generates citations]
    ↓ Formatted response returned to user
```

### **5. Result Aggregation** [Source: ai_layer_interface.py]

The AI Layer processes search results into coherent responses:

```python
def aggregate_results(self, chunks: List[Dict], query: str = None) -> Dict:
    # Sort by rank and take top 5
    top_chunks = sorted(chunks, key=lambda x: x.get("rank", 999))[:5]
    
    # Build response with citations
    for i, chunk in enumerate(top_chunks):
        text = chunk.get("text", "")
        doc_name = metadata.get("document_name")
        
    return {
        "response": formatted_text,
        "citations": ["[1] ARCHITECTURE.md (Relevance: 0.95)"],
        "num_chunks": len(chunks)
    }
```

### **6. Key Advantages** [Source: ARCHITECTURE.md]

- **Semantic Understanding**: Searches understand meaning, not just keywords
- **Configurable Limit**: Default returns top 5 results (adjustable via `limit` parameter)
- **Automatic Citations**: Each result includes source document and relevance score
- **Change Detection**: SHA-256 checksums ensure only modified documents are re-indexed
- **Two Backends**: Choose between quality-focused Chonkie or speed-focused Chroma

### **7. Example Search Flow** [Source: ARCHITECTURE.md]

```
User query: "How does the MCP server work?"
    ↓
Backend.query("How does the MCP server work?", limit=5)
    ↓ [ChromaDB vector similarity matching]
    ↓ Returns chunks with scores like:
    - Chunk from ARCHITECTURE.md (score: 0.95)
    - Chunk from README.md (score: 0.87)
    - Chunk from USER_GUIDE.md (score: 0.72)
    ↓
AILayer aggregates and formats response with citations
    ↓
"Found 5 relevant chunks...

[1] Architecture excerpt... [Source: ARCHITECTURE.md]
[2] Overview excerpt... [Source: README.md]

**Sources:**
[1] ARCHITECTURE.md (Relevance: 0.95)
[2] README.md (Relevance: 0.87)"
```

---

### **Summary**

The librarian-MCP system's semantic search works by:
1. **Chunking documents intelligently** (Chonkie default or Chroma fallback)
2. **Storing chunks as vectors** in ChromaDB with rich metadata
3. **Performing vector similarity matching** when queries arrive
4. **Aggregating top results** and generating automatic citations

This approach enables the librarian to understand semantic meaning rather than just keyword matches, providing more accurate and contextually relevant search results. [Source: ARCHITECTURE.md], [Source: ai_layer_interface.py]