# Query 2: Backend Architecture

**Status**: success
**Tokens Used**: 1360
**Timestamp**: 2026-03-18T19:21:41.486672
**Tool Calls**: 8

---

I'll search the library for information about the backend implementation and comparisons with alternatives.


Let me get more specific information about the backend comparison and why it's better.


Let me read the full documentation to get complete details about the backend comparison.


Now let me search for more specific information about the performance comparison table.


Let me check the CONFIGURATION.md file which might have more details about backend selection.


Now I have comprehensive information about the backend. Let me provide a complete answer based on the library content.

Based on the library documentation, here's what I found about the Librarian MCP server's backend implementation:

## Backend Implementation

The **Librarian MCP Server uses Chonkie as its default backend** for document processing and semantic search. [Source: ARCHITECTURE.md], [Source: CONFIGURATION.md]

### Why Chonkie is Better Than Alternatives (ChromaDB Backend)

According to the documentation, here are the key advantages of using **Chonkie over ChromaDB's native backend**:

**[Source: ARCHITECTURE.md]**
```
## ChonkieBackend (Default)

**Purpose**: Intelligent semantic chunking using the Chonkie library

**Key Features**:
- ✅ Semantic boundaries: Respects sentence and paragraph structure
- ✅ Context preservation: Related concepts stay together
- ✅ Intelligent sizing: Adapts to document structure
- ✅ Better search results: Higher quality chunks = better matches
```

### Performance Comparison Summary

The documentation indicates a comparison table exists with the following key differentiators:

**[Source: ARCHITECTURE.md]**
| Feature | ChromaDB Backend | Chonkie Backend |
|---------|-----------------|-----------------|
| Chunking Quality | Basic sentence splitting | Intelligent semantic chunking |
| Search Results | Lower relevance | Higher quality chunks = better matches |
| Maintenance | Custom code required | Uses proven, battle-tested implementation |

### Why Chonkie is Better (Key Reasons)

**[Source: ARCHITECTURE.md]**

1. **Better Search Quality**: "Higher quality chunks = better matches" - The intelligent chunking preserves semantic context and respects document structure, leading to more relevant search results.

2. **Less Maintenance Required**:
   - No custom chunking code needed
   - Active development by Chonkie team
   - Multiple chunking strategies available
   - Battle-tested across many projects

3. **Intelligent Boundaries**: Unlike ChromaDB's simple sentence-based splitting, Chonkie uses recursive chunking that adapts to document structure and preserves related concepts together.

4. **Production Ready**: The default choice for production deployments where search result quality matters most.

### When to Use Each Backend

**[Source: CONFIGURATION.md]**

| Scenario | Recommended Backend |
|----------|-------------------|
| Search quality is important | Chonkie (default) |
| Documents have complex structure | Chonkie |
| Production deployment | Chonkie |
| Processing speed critical | ChromaDB |
| Very simple documents | ChromaDB |
| Testing/development | ChromaDB |

### Technical Implementation

Both backends use **ChromaDB for vector storage**, but differ in the chunking strategy:

**[Source: ARCHITECTURE.md]**
```python
# Chonkie approach (intelligent)
from chonkie import RecursiveChunker
chunker = RecursiveChunker(chunk_size=1000, min_characters_per_chunk=50)
chunks = chunker(document_text)

# ChromaDB approach (simple)
chunks = document_text.split('. ')  # Simple sentence splitting
```

### Deployment Choice: venv vs Docker

The system also uses **venv instead of Docker** for deployment, which provides additional benefits:

**[Source: ARCHITECTURE.md]**
- **Simplicity**: No container complexity, standard Python deployment
- **Performance**: stdio transport (no HTTP overhead), shared memory space
- **Debugging**: Direct Python debugger access, easy log inspection
- **Resource Usage**: Lower memory footprint, no duplicate installations

---

**Would you like me to:**
1. Explain the chunking strategy in more detail?
2. Show how to switch between backends for testing?
3. Explore the backend factory implementation code?