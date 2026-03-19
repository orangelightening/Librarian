# Chonkie Backend Migration Guide

## Overview

The librarian-mcp now supports **two backends** for document processing:

1. **ChromaDB Backend** (default) - Original implementation with custom chunking
2. **Chonkie Backend** (new) - Intelligent semantic chunking using Chonkie library

## What is Chonkie?

**Chonkie** is a lightweight, intelligent chunking library that provides:
- ✅ Semantic-aware chunking (understands document structure)
- ✅ Multiple chunking strategies (recursive, semantic, token-based, etc.)
- ✅ Better chunk boundaries (doesn't break mid-sentence or mid-concept)
- ✅ Actively maintained and battle-tested
- ✅ Less code for us to maintain

## Benefits of Chonkie Backend

### Better Chunk Quality
- **Semantic boundaries**: Chunks respect sentence and paragraph boundaries
- **Context preservation**: Related concepts stay together
- **Intelligent sizing**: Adapts to document structure
- **Better search results**: Higher quality chunks = better matches

### Less Maintenance
- **No custom chunking code**: We use Chonkie's proven implementation
- **Active development**: Chonkie team maintains and improves chunking
- **More strategies**: Easy to switch between chunking methods
- **Battle-tested**: Used by many projects, thoroughly tested

## Performance Comparison

| Feature | ChromaDB Backend | Chonkie Backend |
|---------|-----------------|-----------------|
| Chunking Quality | Good (custom) | Better (semantic) |
| Code Maintenance | ~1000 LOC | ~50 LOC |
| Chunking Strategies | 1 (fixed) | 8+ (flexible) |
| Active Development | Custom code | Chonkie team |
| Processing Speed | Fast | Fast |
| Search Relevance | Good | Better |

## How to Switch Backends

### Option 1: Environment Variable (Recommended)

```bash
# Set environment variable before starting the server
export LIBRARIAN_BACKEND=chonkie

# Start the server
./setup_mcp.sh
```

### Option 2: Modify Configuration

Edit `mcp_server/config/settings.py`:

```python
# Change from:
BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chroma")

# To:
BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")
```

### Option 3: Command Line Argument

```bash
./setup_mcp.sh
```

Then in your MCP client configuration, add the environment variable:

```json
{
  "mcpServers": {
    "librarian": {
      "command": "/home/peter/development/librarian-mcp/venv/bin/python",
      "args": [
        "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py",
        "--safe-dir",
        "/home/peter/development/librarian-mcp"
      ],
      "env": {
        "PYTHONPATH": "/home/peter/development/librarian-mcp",
        "LIBRARIAN_BACKEND": "chonkie"
      }
    }
  }
}
```

## Migration Steps

### For New Users

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set backend to Chonkie
export LIBRARIAN_BACKEND=chonkie

# 3. Start the server
./setup_mcp.sh

# 4. Add your documents
# Use the MCP tools to sync your documents
```

### For Existing Users

**Good news**: No migration needed! Your existing ChromaDB database works with both backends.

```bash
# 1. Install updated dependencies
pip install -r requirements.txt

# 2. Optionally test with Chonkie first
export LIBRARIAN_BACKEND=chonkie
./setup_mcp.sh

# 3. Test in your MCP client
# Try searching and adding documents

# 4. If satisfied, make it permanent
# Add export LIBRARIAN_BACKEND=chonkie to your shell profile (~/.bashrc or ~/.zshrc)
```

## What Changes When You Switch

### Document Processing

**ChromaDB Backend**:
- Fixed-size chunks (1000 characters)
- Simple sentence splitting
- No semantic awareness

**Chonkie Backend**:
- Intelligent chunk sizes (respects document structure)
- Semantic boundary detection
- Configurable strategies (recursive, semantic, etc.)
- Better context preservation

### Storage

**Both backends** use the same:
- ChromaDB database location
- Collection structure
- Metadata format
- Document IDs

**Result**: You can switch back and forth without losing data!

### Search

**Both backends** use the same:
- ChromaDB vector storage
- Embedding functions
- Search algorithm

**Result**: Search works the same, but Chonkie chunks provide better results due to higher quality input.

## Testing the Chonkie Backend

### Quick Test

```bash
# Install test dependencies
pip install -r requirements.txt

# Run integration test
python scripts/test_chonkie_backend_integration.py
```

### Test in MCP Client

1. Start the server with Chonkie backend:
```bash
export LIBRARIAN_BACKEND=chonkie
./setup_mcp.sh
```

2. In your MCP client (Jan, LM Studio, etc.):
```
"Get library stats"
```

3. Add a document:
```
"Add the file README.md to the library"
```

4. Search for content:
```
"What features does the librarian provide?"
```

## Troubleshooting

### Issue: "ImportError: No module named 'chonkie'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Backend still using ChromaDB chunking"

**Solution**: Check that environment variable is set:
```bash
echo $LIBRARIAN_BACKEND
# Should output: chonkie
```

If not set correctly:
```bash
export LIBRARIAN_BACKEND=chonkie
./setup_mcp.sh
```

### Issue: "Performance slower than before"

**Note**: Chonkie chunking may be slightly slower due to more sophisticated algorithms, but this is typically offset by:
- Better search relevance (fewer searches needed)
- Higher quality results
- More accurate responses

**If performance is critical**: You can switch back to ChromaDB backend anytime:
```bash
export LIBRARIAN_BACKEND=chroma
./setup_mcp.sh
```

## Advanced Configuration

### Adjust Chunk Size

Edit `mcp_server/config/settings.py`:

```python
# Chonkie chunking parameters
CHONKIE_CHUNK_SIZE = int(os.getenv("LIBRARIAN_CHUNK_SIZE", "1000"))  # Default: 1000 tokens
CHONKIE_MIN_CHUNK_SIZE = int(os.getenv("LIBRARIAN_MIN_CHUNK_SIZE", "50"))  # Default: 50 characters
```

### Use Different Chunking Strategies

The Chonkie backend currently uses `RecursiveChunker`, but you can modify `mcp_server/backend/chonkie_backend.py` to use other chunkers:

```python
from chonkie import SemanticChunker  # Requires embeddings
from chonkie import TokenChunker     # Fixed token chunks
from chonkie import SentenceChunker  # Sentence-based
```

**Note**: SemanticChunker requires embeddings and may be slower.

## FAQ

### Q: Will I lose my existing documents?

**A**: No! Both backends use the same ChromaDB database. Your documents are safe.

### Q: Can I switch back to ChromaDB backend?

**A**: Yes! Just change the environment variable or remove it:
```bash
export LIBRARIAN_BACKEND=chroma
./setup_mcp.sh
```

### Q: Which backend should I use?

**A**:
- **New users**: Start with Chonkie backend (better results out of the box)
- **Existing users**: Test Chonkie, switch if you like it
- **Performance critical**: Stay with ChromaDB backend (faster chunking)
- **Quality focused**: Use Chonkie backend (better search relevance)

### Q: Is Chonkie backend production-ready?

**A**: Yes! All tests pass, it's stable, and it's ready for production use.

### Q: How do I know which backend I'm using?

**A**:
```bash
# Check environment variable
echo $LIBRARIAN_BACKEND

# Or in your MCP client
"Get library stats"
# Look for "Backend: chromadb" or "Backend: chonkie_recursive"
```

## Support

If you encounter issues:
1. Check the integration test: `python scripts/test_chonkie_backend_integration.py`
2. Review this guide
3. Check `CHONKIE_INTEGRATION.md` for technical details
4. Report issues with backend type, error message, and steps to reproduce

---

## A Poetic Tribute to Chonkie 🦛

*During the Phase 2 integration, GLM-4 was asked to write a poem about Chonkie. The result captures the spirit of intelligent chunking perfectly.*

### The Hippo of Smart Chunks

In data streams where fragments flow,
A mighty creature guides the flow.
With hippo grace and wisdom vast,
Chonkie leads the breaking fast.

No careless cuts, no jagged lines,
It reads the text and understands
Where sentences begin and end,
Where concepts pause, where thoughts extend.

While fixed-size chunks may thoughts sever,
This hippo keeps them all together.
Respecting boundaries, meaning clear,
Semantic paths for search to steer.

From PDF pages, deep and wide,
Through code blocks and tables' pride,
It processes with gentle might,
Transforming day and into night.

Eight strategies within its pack,
Recursive, semantic—no lack
Of options for the data wise,
Each chunk a perfect, sized surprise.

Light and swift, it moves with grace,
Small docs in mere blink embrace.
Large volumes yield to steady pace,
No burden heavy on the chase.

The custom code of yesteryear,
One thousand lines of maintenance fear,
Now fifty lines of wrapper shine,
The hippo's power, refined design.

Battle-tested, strong and true,
Active devs keep it renewed.
When searching needs a relevant spark,
This hippo hits the right remark.

So sing the praise of Chonkie bold,
The mighty chunker, wise and old (well, modern!).
A hippo champion in the stream,
Making semantic split supreme.

🦛✨

*Generated by GLM-4, March 16, 2026*
*Query: "Please write me a poem about chonkie. The company emoji is a hippopotamus. Derive information from the library for context."*

---

**Last Updated**: 2026-03-16
**Backend Version**: Chonkie 1.6.0
**Status**: Production Ready ✅
