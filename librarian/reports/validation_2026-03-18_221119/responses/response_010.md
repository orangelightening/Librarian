# Query 10: Search Architecture

**Status**: success
**Tokens Used**: 274
**Timestamp**: 2026-03-18T22:13:06.525307
**Tool Calls**: 0

---

Based on the library content, the implementation of semantic search in the librarian-mcp system relies on **ChromaDB** for vector storage and **Chonkie** for document chunking.

Here are the specific details:

**Vector Database and Embeddings**
The system uses ChromaDB to store vector embeddings, which allow for semantic matching rather than just exact keyword matching.
[Source: architecture.md]
> "Semantic search is implemented using ChromaDB vector embeddings."

**Document Chunking Strategy**
To enable effective semantic search, documents are broken down into manageable segments before embedding.
[Source: architecture.md]
> "Documents are chunked into 1000-character segments and embedded using ChromaDB's default embedding function."

**Integration Workflow**
The process involves:
1.  **Chunking:** Using Chonkie to split documents into 1000-character pieces.
2.  **Embedding:** Converting these chunks into numerical vectors.
3.  **Storage:** Storing the vectors in ChromaDB.
4.  **Search:** Querying ChromaDB to find the most similar chunks based on semantic similarity.

Would you like me to explore the specific configuration of the Chonkie integration or details about the automatic change detection mechanism that updates these vectors?