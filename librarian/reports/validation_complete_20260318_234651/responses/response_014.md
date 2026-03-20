# Query 14: Tool Usage Examples

**Status**: success
**Tokens Used**: 728
**Timestamp**: 2026-03-18T23:47:19.326125
**Tool Calls**: 0

---

Here are 5 practical examples of how you would use the librarian tools in real-world scenarios:

---

### **Example 1: Quick Document Lookup**
**Scenario:** You need to find information about the library's current state.

```bash
# Step 1: Check how many documents are in the library
get_library_stats()

# Step 2: List all indexed documents to see what's available
list_indexed_documents()

# Step 3: Search for specific content
search_library("API authentication")
```

**Result:** You'd get statistics showing 15 documents, a list of all indexed files, and semantic search results about authentication mechanisms.

---

### **Example 2: Finding Code Examples**
**Scenario:** You need to find Python examples of data processing.

```bash
# Step 1: Search the library semantically
search_library("Python data processing examples", limit=10)

# Step 2: For a promising result, get its structure first
document_summary("/path/to/data_processing.py")

# Step 3: Read specific sections if needed
read_document("data_processing.py", head=50)
```

**Result:** You'd find relevant Python files, understand their structure (functions, classes), and read the first 50 lines to see the actual code examples.

---

### **Example 3: File System Exploration**
**Scenario:** You need to find all markdown files in a specific directory.

```bash
# List documents with extension filter
list_documents(path="/docs", extension=".md", recursive=True)

# Or search for specific content
search_documents(query="TODO", path="/docs", extension=".md")
```

**Result:** You'd get a list of all `.md` files in the `/docs` directory, or find specific lines containing "TODO" across markdown files.

---

### **Example 4: Checking Document Status**
**Scenario:** You added a new document and want to verify it's indexed.

```bash
# Check if a document is indexed and up-to-date
get_document_status("/path/to/new_document.md")

# Or sync an entire directory
sync_documents(path="/data", extensions=".py,.md,.txt", recursive=True)
```

**Result:** You'd learn if a document needs re-indexing, or automatically update the library with new Python and markdown files from the `/data` directory.

---

### **Example 5: Advanced Search Strategy**
**Scenario:** You need to find all error handling patterns in code.

```bash
# Step 1: Semantic search for error handling
search_library("error handling patterns", limit=8)

# Step 2: For each result, examine the file structure
document_summary("/path/to/errors.py")

# Step 3: Search for specific error patterns literally
search_documents(query="except", path="/src", extension=".py")

# Step 4: Read specific line ranges if found
read_document("/path/to/errors.py", start_line=100, end_line=150)
```

**Result:** You'd combine semantic search results with literal text searches to find comprehensive error handling patterns, then read specific code sections for detailed analysis.

---

**Key Takeaway:** The librarian tools work best when combined strategically—using semantic search for broad discovery, document summaries for structure, and targeted reads for specific content. Would you like me to demonstrate any of these with actual library content?
