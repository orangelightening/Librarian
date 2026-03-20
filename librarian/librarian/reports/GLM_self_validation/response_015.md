# Query 15: What should I do if the librarian isn't finding documents I know exist?

If you're experiencing issues where the librarian isn't finding documents that you know exist, here's a systematic troubleshooting approach with diagnostic steps and solutions.

## Diagnostic Steps

### Step 1: Check What's Currently Indexed

**Tool**: `list_indexed_documents()`

First, verify what's actually in the library:

```
User: "List all indexed documents"
Librarian: [Returns list of all documents with metadata]
```

This shows you:
- Document names and paths
- When they were indexed
- Their current status
- Total document count

**What to Look For**:
- Is the document in the list at all?
- When was it last indexed?
- Is it marked as outdated?

---

### Step 2: Verify Document Status

**Tool**: `get_document_status(path)`

Check the specific status of the missing document:

```
User: "Check the status of /home/peter/docs/important-file.md"
Librarian: [Returns status information]
```

**Possible Responses**:

| Status | Meaning | Next Step |
|--------|---------|-----------|
| `not_found` | Document doesn't exist in library | Add document with `add_document()` |
| `indexed` | Document is indexed and up-to-date | Issue is with search query (see below) |
| `outdated` | Document exists but has been modified | Sync with `sync_documents()` |
| `error` | Indexing error occurred | Check file permissions and size |

---

### Step 3: Search the File System

**Tools**: `list_documents()`, `search_documents()`

Verify the file exists in the file system and can be accessed:

```
User: "List documents in /home/peter/docs/"
Librarian: [Uses list_documents() to show files]

User: "Search for 'important' in /home/peter/docs/"
Librarian: [Uses search_documents() for literal text search]
```

**What This Checks**:
- File exists and is accessible
- Path is within allowed directory scope
- File isn't being filtered by exclusion patterns

---

### Step 4: Check Library Statistics

**Tool**: `get_library_stats()`

Get overall library health information:

```
User: "Get library statistics"
Librarian: [Returns stats including document counts, backend info]
```

**What to Look For**:
- Total documents indexed
- Backend being used (Chonkie vs ChromaDB)
- Any error messages or warnings

---

## Common Causes and Solutions

### Cause 1: Document Not Yet Indexed

**Symptoms**:
- Document exists in file system
- `get_document_status()` returns `not_found`
- Document not in `list_indexed_documents()` output

**Solutions**:

**Option A - Add Single Document**:
```bash
User: "Add /home/peter/docs/important-file.md to the library"
Librarian: [Uses add_document(path)]
Librarian: "Document added and indexed successfully"
```

**Option B - Sync Directory**:
```bash
User: "Sync /home/peter/docs/ to add all documents"
Librarian: [Uses sync_documents(path="/home/peter/docs")]
Librarian: "Discovered 15 documents. 12 new, 3 modified"
```

---

### Cause 2: Document Status Issues (Outdated)

**Symptoms**:
- Document exists in library
- `get_document_status()` returns `outdated`
- Search results are from old version

**Solution**:
```bash
User: "The document shows as outdated. Resync it."
Librarian: [Uses sync_documents(path) or re-indexes the specific file]
Librarian: "Document updated and re-indexed with latest changes"
```

This automatically happens when you use `sync_documents()` - it detects changes via SHA-256 checksums `[Source: document_manager.py]`

---

### Cause 3: File Excluded by `.librarianignore`

**Symptoms**:
- File exists in file system
- Not found by `list_documents()` or `sync_documents()`
- File matches exclusion patterns

**Solution**: Check if your file is being excluded:

**Common Built-in Exclusions** `[Source: ignore_patterns.py]`:

**Security** (always excluded):
- `.env`, `*.env`, credentials
- `*.key`, `*.pem`
- `id_rsa`, `id_ed25519`

**Development**:
- `venv/`, `.venv/`, `virtualenv/`
- `node_modules/`
- `__pycache__/`, `*.pyc`

**Databases**:
- `chroma_db/`
- `metadata/`
- `*.db`, `*.sqlite`

**Check Your `.librarianignore`**:
```bash
User: "Read the .librarianignore file"
Librarian: [Uses read_document() to show patterns]
```

**If File Should Be Indexed**:
- Remove the exclusion pattern from `.librarianignore`
- Or use negation pattern to allow it (e.g., `!.env.example`)
- Then re-sync the directory

---

### Cause 4: Permission or Path Issues

**Symptoms**:
- File exists but can't be accessed
- Error messages about permissions or path access
- File is outside allowed directory scope

**Solutions**:

**Check Path**:
```bash
User: "Verify the path to important-file.md"
Librarian: [Verifies path is within allowed directory]
```

**Check Permissions**:
- Ensure the librarian process has read access to the file
- Verify file is in a directory the librarian is allowed to access
- Check that the path resolves correctly (no symlinks causing issues)

---

### Cause 5: File Too Large

**Symptoms**:
- Add or sync operations fail with size error
- File exceeds maximum document size

**Configuration** `[Source: document_manager.py]`:
```bash
# Default: 10MB
export LIBRARIAN_MAX_DOCUMENT_SIZE=10000000
```

**Solutions**:
- Increase the max size limit if needed:
  ```bash
  export LIBRARIAN_MAX_DOCUMENT_SIZE=50000000  # 50 MB
  ```
- Or split large files into smaller chunks
- Consider if the entire file needs to be indexed

---

### Cause 6: Poor Search Query

**Symptoms**:
- Document is indexed and up-to-date
- `get_document_status()` returns `indexed`
- But semantic search doesn't find it

**Solutions**:

**Refine Your Query**:
- Use more specific terms related to the content
- Try different keywords or concepts
- Use natural language queries

**Example**:
```
Poor Query: "information"
Better Query: "How does the system handle distributed transactions?"
```

**Use Literal Search**:
```bash
User: "Search for 'specific-phrase' in all documents"
Librarian: [Uses search_documents() for exact text match]
```

**Increase Result Limit**:
```bash
User: "Search for 'topic' with more results"
Librarian: [Uses search_library(query="topic", limit=10)]
```

---

## Troubleshooting Workflow Example

Here's a complete troubleshooting example:

```
User: "I can't find anything about 'API authentication' but I know it's in the docs"

User: "What's indexed?"
Librarian: [list_indexed_documents()] → Shows 45 documents

User: "Check status of docs/auth.md"
Librarian: [get_document_status()] → Status: "outdated"

User: "Sync the docs/ directory"
Librarian: [sync_documents(path="docs/")]
Librarian: "Discovered 50 documents. 5 modified, 1 new"

User: "Now search for 'API authentication' again"
Librarian: [search_library(query="API authentication")]
Librarian: "Found 3 relevant chunks about API authentication..."

User: "Great! What was the issue?"
Librarian: "The auth.md file was outdated. After resyncing, it was re-indexed with the latest content."
```

---

## Quick Reference: Troubleshooting Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `list_indexed_documents()` | See all indexed docs | Check what's in library |
| `get_document_status(path)` | Check specific doc status | Verify document state |
| `list_documents(path)` | Browse file system | Find files to index |
| `search_documents(query)` | Literal text search | Find specific phrases |
| `add_document(path)` | Add single document | Quick additions |
| `sync_documents(path)` | Sync directory | Bulk updates |
| `get_library_stats()` | Library health | Check overall status |

---

## Prevention Tips

1. **Regular Syncing**: Run `sync_documents()` after adding new files
2. **Monitor Status**: Periodically check `get_document_status()` on key docs
3. **Review Exclusions**: Check `.librarianignore` to ensure important files aren't excluded
4. **Refine Queries**: Use specific, natural language queries for best semantic search results
5. **Check Stats**: Use `get_library_stats()` to monitor library health

By following this systematic approach, you can diagnose and resolve most issues where documents aren't being found.
