# Response 15: Troubleshooting - Librarian Not Finding Documents

## Summary

When the librarian isn't finding documents you know exist, several common issues may be at play. This guide provides diagnostic steps and solutions for the most frequent problems.

---

## Common Causes and Solutions

### 1. Document Not Yet Indexed

**Problem**: The document exists on disk but isn't in the library yet.

**Symptoms**:
- File exists when you search for it
- No results for searches in that file
- `get_document_status()` returns "not_indexed"

**Solutions**:

**Option A: Add document manually**
```
"Add the file /path/to/my-document.md to the library"
```

**Option B: Sync a directory**
```
"Sync the directory ~/project/docs to the library"
```

**Option C: Use CLI directly**
```bash
python scripts/ingest.py --path ~/project/docs
```

[Source: search_library]

---

### 2. Document Status Issues

**Problem**: The document exists but has checksum mismatch or indexing issues.

**Symptoms**:
- `get_document_status()` returns "outdated"
- Document shows as "current" but searches fail

**Solutions**:

**Step 1: Check document status**
```
"Check the status of /path/to/my-document.md"
```

**Possible responses:**
- `status: current` - Document is properly indexed
- `status: outdated` - File has been modified since last sync
- `status: not_indexed` - Document was never added
- `status: not_found` - File no longer exists

**Step 2: Re-sync the directory**
```
"Sync the directory ~/project/docs to update changes"
```

**Step 3: Verify sync results**
```
"List all indexed documents"
```

[Source: search_library]

---

### 3. Document in .librarianignore

**Problem**: The file is being excluded by ignore patterns.

**Symptoms**:
- File exists but never appears in search results
- Sync reports "Ignored: X files"
- File matches known ignore patterns

**Solutions**:

**Step 1: Check what's being ignored**
```bash
cat .librarianignore
```

**Common ignored patterns:**
- `.env`, `.pem`, `.p12` - Credential files
- `*.key`, `*.pem`, `id_rsa` - Private keys
- Build artifacts, temporary files
- System files

**Step 2: View sync output**
```
"Show me the output from the last sync"
```

The sync output will show:
- `Added: X documents`
- `Updated: Y documents`
- `Ignored: Z files (excluded by .librarianignore)`

**Step 3: Modify .librarianignore**
```bash
# Edit .librarianignore
# Add a comment to comment out the pattern
# # *.log
```

**Step 4: Re-sync**
```
"Sync the directory again"
```

[Source: search_library]

---

### 4. File Outside Allowed Directory

**Problem**: The file path is outside the whitelisted safe directory.

**Symptoms**:
- Error when trying to search/modify file
- "Security error" or "path not allowed" messages

**Solutions**:

**Step 1: Check allowed directory**
```
"Show me the server configuration"
```

Look for `LIBRARIAN_SAFE_DIR` in the response.

**Step 2: Verify file path**
Ensure your file is within the allowed directory structure.

**Step 3: Reconfigure if needed**
```bash
# Edit setup_mcp.sh or use command line
./setup_mcp.sh --safe-dir /path/to/your/project
```

**Step 4: Restart the server**
After configuration changes, restart the MCP server.

[Source: ARCHITECTURE.md]

---

### 5. Unsupported File Type

**Problem**: The file extension isn't supported by the librarian.

**Symptoms**:
- File isn't indexed during sync
- File appears in "ignored" count
- Error when trying to add file

**Supported extensions**:
- `.md` - Markdown
- `.txt` - Plain text
- `.py` - Python
- `.json` - JSON
- `.yaml`, `.yml` - YAML
- `.toml` - TOML

**Solutions**:

**Option A: Add to sync explicitly**
```
"Add the file /path/to/file.py to the library"
```

**Option B: Modify sync extensions**
```bash
# Edit setup_mcp.sh to add more extensions
# Or use the library tool with explicit extensions
```

**Option C: Convert to supported format**
Convert unsupported files (like `.html`, `.js`, etc.) to a supported format.

[Source: search_library]

---

## Diagnostic Workflow

When a document isn't found, follow these steps in order:

### Step 1: Verify File Existence
```bash
ls /path/to/file
# Or use the librarian:
"Does the file /path/to/file exist?"
```

### Step 2: Check Library Contents
```
"List all indexed documents"
# Look for your file in the list
```

### Step 3: Check Document Status
```
"Check the status of /path/to/file"
```

### Step 4: Search for File Content
```
"Search for the word 'xyz' in all files"
# If file exists, it should appear
```

### Step 5: Check Ignore Patterns
```bash
cat .librarianignore
```

### Step 6: Re-sync
```
"Sync the directory again"
```

---

## Quick Reference Table

| Problem | Quick Fix |
|---------|-----------|
| Document not indexed | `add_document(path)` or `sync_documents(path)` |
| Document outdated | `sync_documents(path)` to update |
| File ignored | Check `.librarianignore`, modify if needed |
| Wrong directory | Verify path is in allowed scope |
| Unsupported format | Convert to `.md`, `.py`, `.txt`, etc. |
| Search returns nothing | Try broader terms, verify indexing |

---

## Summary of Diagnostic Tools

| Tool | Use When |
|------|----------|
| `list_indexed_documents()` | What's in the library? |
| `get_document_status(path)` | Is a specific file indexed? |
| `search_documents(query)` | Can I find content? |
| `list_documents(path)` | What files exist on disk? |
| `get_library_stats()` | Overview of library state |

---

## Summary

The most common reasons the librarian doesn't find documents are:
1. Document hasn't been indexed yet
2. Document was modified and needs re-sync
3. Document is ignored by `.librarianignore`
4. File is outside allowed directory
5. File type isn't supported

The diagnostic workflow of checking indexing status, verifying file existence, and re-syncing typically resolves most issues.

---
**Primary Sources:**
- `/home/peter/development/librarian-mcp/USER_GUIDE.md`
- `/home/peter/development/librarian-mcp/ARCHITECTURE.md`
- `/home/peter/development/librarian-mcp/README.md`