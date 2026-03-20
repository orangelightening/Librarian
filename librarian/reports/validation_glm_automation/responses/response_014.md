# Query 14: Tool Usage Examples

**Status**: success
**Tokens Used**: 2013
**Timestamp**: 2026-03-19T15:01:49.664504
**Tool Calls**: 1

---

Based on the Librarian's capabilities, here are 5 practical examples of how you would use the tools:

---

## 1. **Research a Technical Topic Across Your Library**

**Scenario:** You're working on a project using React and want to understand best practices for state management.

```bash
# Use semantic search to find relevant information
search_library("React state management best practices", limit=10)
```

**What happens:** The Librarian searches across all 528 indexed chunks in your library, finds semantically relevant content about React patterns, hooks, context API, and state management libraries, and synthesizes an answer with proper citations.

---

## 2. **Sync a New Documentation Directory**

**Scenario:** You just downloaded the Kubernetes documentation and want to add all those markdown files to your library for future reference.

```bash
# Bulk sync an entire directory recursively
sync_documents(
  path="/path/to/kubernetes/docs",
  extensions=[".md"],
  recursive=true
)
```

**What happens:** The Librarian walks through the entire directory structure, finds all markdown files, chunks them appropriately, and adds them to your ChromaDB collection for semantic search.

---

## 3. **Add a Single Important Document**

**Scenario:** Your team just published an architecture decision record (ADR) that you want to reference frequently.

```bash
# Add a single document to the library
add_document(path="/home/peter/projects/myapp/docs/adr-001-caching.md")
```

**What happens:** The Librarian processes just this one file, chunks it, and indexes it. You can now search for "caching strategy" and get results from this ADR.

---

## 4. **Find Specific Code Patterns or Commands**

**Scenario:** You need to find where you documented a specific Docker command or configuration pattern.

```bash
# Literal text search for exact matches
search_documents(
  query="docker run --mount type=bind",
  path="/home/peter/development",
  extension=".md",
  case_sensitive=false
)
```

**What happens:** Unlike semantic search, this does a literal text search to find exact matches of the Docker command syntax across your markdown files.

---

## 5. **Clean Up Your Library**

**Scenario:** You've deprecated an old project and want to remove its documentation from your search index to keep results relevant.

```bash
# List current documents to find what to remove
list_indexed_documents()

# Then remove specific documents by ID
remove_document(document_id="doc_12345")
```

**What happens:** The Librarian shows you all indexed documents with their IDs and paths, then lets you cleanly remove outdated content so your searches only return current, relevant information.

---

## Bonus: Check What's in Your Library

```bash
# Get library statistics
get_library_stats()
```

**Current Status:** Your library has **528 chunks** stored in ChromaDB at `/home/peter/development/librarian-mcp/chroma_db`, ready for semantic search across your documentation.

---

Would you like me to demonstrate any of these examples with actual searches from your current library?
