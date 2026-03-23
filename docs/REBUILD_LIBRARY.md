# Rebuilding Library Indices

**When and how to rebuild your Librarian library indices.**

## When to Rebuild

### Automatic Rebuild (Recommended)
The librarian system automatically detects changes during `sync_documents()`:
- ✅ New files → Added automatically
- ✅ Modified files → Updated automatically (based on checksum)
- ✅ Deleted files → Removed automatically
- ✅ Unchanged files → Skipped (for efficiency)

**You usually don't need to manually rebuild.**

### Manual Rebuild (When Needed)

Rebuild manually when:
- 🔧 **Converted PDFs to text** - After running `pdftotext` or similar
- 📁 **Added many files manually** - Batch import of new documents
- 🐛 **Metadata corruption suspected** - Index seems inconsistent
- 🔄 **Switched backends** - Changed from ChromaDB to Chonkie or vice versa
- 📝 **Updated .librarianignore** - Added new exclusion patterns

## Rebuild Scripts

### Botany Library

**Location:** `scripts/rebuild_botany.sh`

**Usage:**
```bash
cd /home/peter/development/librarian-mcp
./scripts/rebuild_botany.sh
```

**What it does:**
- Scans `/home/peter/botany/` for all supported file types
- Indexes PDFs, text files, markdown, code, etc.
- Shows sync results (added, updated, unchanged, removed, ignored)
- Displays final statistics and document list

**Output example:**
```
📊 Sync Results:
  ✅ Added: 8
  🔄 Updated: 0
  ✓ Unchanged: 5
  🗑️  Removed: 0
  ⏭️  Ignored: 27,295

📈 Library Statistics:
  📚 Documents: 13
  🔢 Chunks: 252
  💾 Size: 1,234,567 bytes
```

### Dev Library (Custom Script)

To rebuild other libraries, create a custom script:

```bash
#!/bin/bash
export LIBRARIAN_BACKEND="chonkie"
export LIBRARIAN_CHROMA_PATH="/path/to/library/.librarian/chroma_db"
export LIBRARIAN_METADATA_PATH="/path/to/library/.librarian/metadata"
export LIBRARIAN_SAFE_DIR="/path/to/library"
export PYTHONPATH="/home/peter/development/librarian-mcp"

cd /home/peter/development/librarian-mcp
source venv/bin/activate

python -c "
from mcp_server.backend.chonkie_backend import ChonkieBackend
from mcp_server.core.document_manager import DocumentManager
from mcp_server.core.metadata_store import MetadataStore
from mcp_server.core.ignore_patterns import IgnorePatterns

backend = ChonkieBackend(
    db_path='/path/to/library/.librarian/chroma_db',
    collection_name='documents'
)
metadata_store = MetadataStore(metadata_path='/path/to/library/.librarian/metadata')
ignore_patterns = IgnorePatterns(root_path='/path/to/library')
doc_manager = DocumentManager(backend, metadata_store, ignore_patterns)

results = doc_manager.sync_directory(
    path='/path/to/library',
    extensions={'.pdf', '.txt', '.md', '.py', '.js', '.ts'},
    recursive=True
)

print(f'Added: {results[\"added\"]}, Updated: {results[\"updated\"]}')
"
```

## PDF to Text Conversion

**Why convert PDFs to text?**

AI models give better responses when they can:
1. **Search** indexed PDF chunks (semantic search)
2. **Read** full text files for complete context

**Conversion improves response quality significantly.**

### Conversion Script

```bash
# Install pdftotext
sudo apt-get install pdftotext  # Ubuntu/Debian
brew install pdftotext           # macOS

# Convert PDFs to text
cd /home/peter/botany
pdftotext Plum.pdf Plum.txt
pdftotext Agronomy.pdf Agronomy.txt
pdftotext Forestry.pdf Forestry.txt
pdftotext Pomology.pdf Pomology.txt
```

**After conversion:**
1. Keep both `.pdf` and `.txt` files
2. Run rebuild script: `./scripts/rebuild_botany.sh`
3. AI can now read full text for better responses

## File Exclusions

### Using .librarianignore

Place `.librarianignore` in the **root of your library** (not in `.librarian/` subdirectory):

**Example:** `/home/peter/botany/.librarianignore`

```
# Obsidian vault
.obsidian/

# Development files
venv/
__pycache__/
*.pyc

# Don't index database
chroma_db/
metadata/

# Librarian's own data
.librarian/

# Add custom exclusions below
```

### Important Notes

- **Location:** `.librarianignore` goes in library root (e.g., `/home/peter/botany/`)
- **Not:** `.librarian/.librarianignore` (wrong location!)
- **Patterns:** Gitignore-style patterns
- **Directories:** End with `/` to ignore entire directory
- **Files:** Use `*.txt` patterns for file extensions

## Troubleshooting

### Rebuild Script Fails

**Problem:** `python: command not found`

**Solution:** Script now activates virtual environment automatically. Make sure you're in the project directory:
```bash
cd /home/peter/development/librarian-mcp
./scripts/rebuild_botany.sh
```

### Files Not Being Ignored

**Problem:** `.obsidian/` files are still being indexed

**Solution:** Move `.librarianignore` to library root:
```bash
# Wrong location:
mv /home/peter/botany/.librarian/.librarianignore /home/peter/botany/.librarianignore

# Rebuild to apply changes:
./scripts/rebuild_botany.sh
```

### AI Cites .txt Instead of .pdf

**This is expected and desirable!**

When you have both `Plum.pdf` and `Plum.txt`:
- AI searches **both** files (chunks from PDF, full text from .txt)
- AI **cites .txt** for readability (better context)
- Search results include content from **both sources**

This is **correct behavior** - the AI has better information and gives better responses.

## Best Practices

1. **Convert important PDFs to text** - Improves AI responses significantly
2. **Keep original PDFs** - For reference and archival
3. **Use sync_documents()** - Automatic rebuild, handles changes gracefully
4. **Manual rebuild** - Only when needed (after conversions, large imports)
5. **Test after rebuild** - Search for known content to verify indexing

## Quick Reference

```bash
# Convert PDF to text
pdftotext document.pdf document.txt

# Rebuild library index
./scripts/rebuild_botany.sh

# Check indexed documents
# (In Jan MCP)
list_indexed_documents()

# Test search
search_library("your query here")
```
