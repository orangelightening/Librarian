# Query 14: Tool Usage Examples

**Status**: success
**Tokens Used**: 816
**Timestamp**: 2026-03-18T19:21:41.487554
**Tool Calls**: 0

---

Here are 5 practical examples of how you would use the librarian tools in real-world scenarios:

---

## Example 1: Researching a Topic with Semantic Search

**Scenario:** You want to understand how semantic search works in your current setup.

```bash
# Step 1: Start with semantic search
search_library("semantic search implementation", limit=5)

# Review results and identify relevant documents
# Then read the full context from key sources
read_document("/path/to/search-implementation.md")
```

**What this does:** Finds conceptually related content even if exact keywords aren't used, then lets you dive deep into specific implementations.

---

## Example 2: Adding New Documentation to the Library

**Scenario:** You've written new documentation in `/docs/new-feature-guide.md` and want it searchable.

```bash
# Option A: Add a single document quickly
add_document("/docs/new-feature-guide.md")

# Option B: Sync an entire directory of new docs
sync_documents("/docs", extensions=".md,.txt", recursive=true)
```

**What this does:** Makes your new content immediately available for semantic search without manual indexing.

---

## Example 3: Exploring File System Before Reading

**Scenario:** You need to find all Python files related to "authentication" but don't know the exact filenames.

```bash
# First, list relevant files in a directory
list_documents("/src/auth", extension=".py", recursive=true)

# Then search for specific text patterns
search_documents("password validation", path="/src/auth", extension=".py")

# Finally read the most relevant file
read_document("/src/auth/password_validator.py")
```

**What this does:** Helps you navigate large codebases efficiently by finding files first, then searching content within them.

---

## Example 4: Checking Document Status and Library Health

**Scenario:** You suspect some documents might be outdated or missing from the library.

```bash
# Get overall library statistics
get_library_stats()

# Check specific document status
get_document_status("/docs/api-reference.md")

# List all indexed documents to see what's available
list_indexed_documents()
```

**What this does:** Helps you maintain a healthy, up-to-date library and identify which files need attention.

---

## Example 5: Comprehensive Research with Multiple Sources

**Scenario:** You're writing a report on "error handling patterns" and need information from multiple sources.

```bash
# Start with broad semantic search
search_library("error handling best practices", limit=10)

# For each relevant result, get document summaries first
document_summary("/docs/error-handling.md")
document_summary("/src/utils/validators.py")

# Read full content of key documents
read_document("/docs/error-handling.md", max_chars=20000)
read_document("/src/utils/validators.py", head=100)

# Search for specific error types across all files
search_documents("exception handling", extension=".py")
```

**What this does:** Provides a structured approach to gathering comprehensive information from multiple sources, with proper citations.

---

## Quick Reference Card

| Goal | Primary Tool | Follow-up Tools |
|------|-------------|-----------------|
| Find concepts | `search_library()` | `read_document()`, `document_summary()` |
| Add content | `add_document()` or `sync_documents()` | `get_document_status()` |
| Explore files | `list_documents()` | `search_documents()`, `read_document()` |
| Check status | `get_library_stats()` | `get_document_status()`, `list_indexed_documents()` |
| Deep research | Multiple tools combined | All tools as needed |

---

Would you like me to demonstrate any of these examples with actual library content, or would you prefer to explore a specific use case from your own projects?