# Response to Query 2: What backend does the librarian-mcp use and why is it better than alternatives?

## Backend Technology Overview

The Librarian MCP Server uses **Chonkie** as its default backend for document processing and semantic chunking [Source: ARCHITECTURE.md].

## System Configuration

```bash
export LIBRARIAN_BACKEND=chonkie  # This is the default
```

The system supports two backends:
1. **Chonkie Backend** (default) - Intelligent semantic chunking using Chonkie library
2. **ChromaDB Backend** (optional) - Original implementation with custom chunking [Source: CHONKIE_MIGRATION.md]

## Why Chonkie is Better Than Alternatives

### 1. Semantic-Aware Chunking

**Chonkie** provides intelligent chunking that understands document structure:
- Respects semantic boundaries (sentences, paragraphs, code blocks)
- Avoids cutting in the middle of concepts
- Maintains context for better search relevance [Source: CHONKIE_INTEGRATION.md]

**Comparison with Custom Implementation:**

| Feature | ChromaDB Backend (Custom) | Chonkie Backend |
|---------|--------------------------|-----------------|
| Chunking Quality | Simple sentence splitting | Semantic-aware boundaries |
| Code of Maintention | ~1000 LOC | ~50 LOC (wrapper) |
| Strategies | Fixed-size only | 8 strategies (recursive, semantic, etc.) |
| Context Preservation | Low | High |
| Search Relevance | Lower | Higher [Source: CHONKIE_INTEGRATION.md]

### 2. Active Development and Maintenance

**Chonkie** is actively maintained with:
- Regular updates and bug fixes
- New chunking strategies added
- Performance optimizations
- Battle-tested across many projects [Source: CHONKIE_INTEGRATION.md]

**Benefits:**
- No custom chunking code to maintain
- Access to new features as they're released
- Larger user base = more thorough testing
- Active development team [Source: CHONKIE_INTEGRATION.md]

### 3. Multiple Chunking Strategies

Chonkie offers 8 different chunking strategies:
- Recursive chunking
- Semantic chunking
- To-JSON chunking
- And more...

This flexibility allows users to optimize for different use cases [Source: CHONKIE_INTEGRATION.md].

### 4. Performance Benefits

**Code Reduction:**
- Custom implementation: ~1000 lines of code
- Chonkie wrapper: ~50 lines of code
- Significant reduction in maintenance burden [Source: CHONKIE_INTEGRATION.md]

**Better Search Results:**
- Higher quality chunks = better matches
- More context in search results
- Improved relevance for complex queries [Source: CHONKIE_INTEGRATION.md]

## Performance Comparison Summary

The Chonkie backend provides superior search quality through intelligent chunking, while the ChromaDB backend offers faster but less accurate chunking. For production use where search result quality matters, Chonkie is the recommended choice [Source: CHONKIE_MIGRATION.md].

## Recommendation

- **New users**: Start with Chonkie backend (better results out of the box)
- **Quality focused**: Use Chonkie backend (better search relevance)
- **Performance critical**: Stay with ChromaDB backend (faster chunking)
- **Existing users**: Test Chonkie, switch if you like it [Source: CHONKIE_MIGRATION.md]

## Summary

Chonkie is better than alternatives because it provides semantic-aware chunking, active maintenance, multiple strategies, and significantly reduced maintenance burden compared to custom implementations [Source: CHONKIE_INTEGRATION.md].