# Query 14: Tool Usage Examples

**Status**: success
**Tokens Used**: 885
**Timestamp**: 2026-03-18T21:01:50.575555
**Tool Calls**: 0

---

Here are 5 practical examples of how you'd use the Librarian tools in real-world scenarios:

---

## **Example 1: Onboarding New Documentation**

**Scenario:** You've just received a new project with 20 markdown files that need to be added to your knowledge base.

```bash
# Instead of manually adding each file, sync an entire directory
sync_documents(path="./docs", extensions=".md,.txt")
```

This automatically:
- Adds all new `.md` and `.txt` files from `./docs`
- Updates any modified documents
- Removes deleted files (keeping the library in sync)

**Follow-up:** Check what was indexed:
```bash
list_indexed_documents()  # See all indexed docs with metadata
get_library_stats()       # Get counts of documents and chunks
```

---

## **Example 2: Researching a Specific Topic**

**Scenario:** You need to understand how authentication is implemented across your codebase.

```bash
# Semantic search for conceptual understanding
search_library(query="authentication implementation security")
```

Then dive deeper into specific results:
```bash
read_document(path="./docs/auth.md")           # Full context
document_summary(path="./src/auth.py")         # Quick structure overview
search_documents(query="JWT token", extension=".py")  # Literal code search
```

**Benefit:** You get both high-level understanding and precise code locations.

---

## **Example 3: Finding Outdated or Missing Documentation**

**Scenario:** A developer reports that the API documentation doesn't match the current implementation.

```bash
# Check if a specific file is indexed and up-to-date
get_document_status(path="./docs/api.md")

# Search for discrepancies
search_documents(query="deprecated endpoint", extension=".md,.py")

# Compare with actual code
list_documents(path="./src/api/", recursive=true)
```

**Action:** If the doc is outdated, you can:
- Update it via `sync_documents()` if the file changed on disk
- Or manually add corrections using `add_document()` for new files

---

## **Example 4: Building a Knowledge Base from Scratch**

**Scenario:** You're starting a new project and want to ingest all relevant code and docs.

```bash
# First, explore what's available
list_documents(path="./", recursive=true)

# Sync the entire project structure
sync_documents(path="./project-root", extensions=".md,.py,.js,.ts")

# Verify everything is indexed
get_library_stats()  # Should show your document count

# Search to understand the domain
search_library(query="project architecture overview")
```

**Pro tip:** Use `document_summary()` on key files to quickly understand their structure without reading everything.

---

## **Example 5: Maintenance and Cleanup**

**Scenario:** You've reorganized your project and need to update the library.

```bash
# Check which documents might be out of sync
get_document_status(path="./docs/old-guide.md")

# Remove obsolete documentation
remove_document(document_id="doc-123")  # Get ID from list_indexed_documents()

# Re-sync after cleanup
sync_documents(path="./docs", extensions=".md")

# Verify library health
get_library_stats()
```

**Best practice:** Always check `list_indexed_documents()` before removing to ensure you're deleting the right document.

---

## **Quick Reference Cheat Sheet**

| Task | Primary Tool | When to Use |
|------|-------------|-------------|
| Add many files at once | `sync_documents()` | Directory updates, onboarding |
| Find concepts semantically | `search_library()` | Research, understanding topics |
| Find exact code/text | `search_documents()` | Code search, literal matches |
| Understand file structure | `document_summary()` | Quick overview without reading |
| Check document freshness | `get_document_status()` | Maintenance, validation |
| Get library overview | `list_indexed_documents()` | Auditing, verification |

---

Would you like me to demonstrate any of these examples with actual commands on your current workspace? I can show you what's in your library and walk through a real scenario.