# Query 14: Give me 5 practical examples of how you would use the librarian tools in practice.

Here are 5 practical examples demonstrating different ways to use the librarian-mcp tools across various scenarios:

## Example 1: Code Quality Analysis (Code Investigator)

**Scenario**: You want to find all instances of poor exception handling in your backend codebase.

**Workflow**:
```
User: "Search the codebase for all places where we catch Exception instead of specific exceptions"
Librarian: [Uses search_documents() to find all 'except Exception' patterns]
Librarian: [Analyzes the results and provides a summary]
Librarian: "Found 15 instances across 8 files. Here are the most critical ones..."

User: "Write your detailed analysis to /librarian/exception-analysis.md"
Librarian: [Uses write_document() to create a comprehensive report]
Librarian: "Written detailed report with file paths, line numbers, and recommendations"

User: [Reads /librarian/exception-analysis.md to review findings]
User: [Applies approved code changes based on librarian's recommendations]
```

**Tools Used**:
- `search_documents()` - Find literal patterns in code
- `write_document()` - Create persistent analysis report
- `read_document()` - User reviews the report

**Why This Works**: The librarian traces code across multiple files, provides specific locations with citations, and writes a reviewable report that you can apply at your own pace `[Source: README.md]`

---

## Example 2: Documentation Synchronization and Change Detection

**Scenario**: You've just added a new documentation directory and want to keep it indexed in the library automatically.

**Workflow**:
```
User: "I just added /home/peter/docs/v2 with 50 new markdown files. Sync them."
Librarian: [Uses sync_documents(path="/home/peter/docs/v2", extensions=".md")]
Librarian: "Discovered 50 documents. Calculating checksums..."
Librarian: "50 new documents indexed. 0 modifications detected."

[Two weeks later...]

User: "I updated several docs. Sync again."
Librarian: [Uses sync_documents() with automatic change detection]
Librarian: "Discovered 50 documents. 8 modified documents detected."
Librarian: "Re-indexing modified documents..."

[User can verify status anytime]
User: "Check the status of /home/peter/docs/v2/architecture.md"
Librarian: [Uses get_document_status()]
Librarian: "Document is indexed and up-to-date. Last modified: 2024-01-15"
```

**Tools Used**:
- `sync_documents()` - Bulk add/update with automatic change detection
- `get_document_status()` - Verify document indexing status
- `get_library_stats()` - View overall library health

**Why This Works**: Automatic SHA-256 checksum detection identifies exactly which files changed without manual tracking `[Source: document_manager.py]`

---

## Example 3: Targeted File Investigation with Precision Reading

**Scenario**: You need to investigate a specific error in a large configuration file but don't want to read the entire 10,000-line file.

**Workflow**:
```
User: "There's an error around line 5000 in nginx.conf. What's in that section?"
Librarian: [Uses read_document(path="/etc/nginx/nginx.conf", start_line=4980, end_line=5020)]
Librarian: "Here's lines 4980-5020. I can see a misconfiguration in the server block..."

User: "What about the beginning of the file to understand the global config?"
Librarian: [Uses read_document(path="/etc/nginx/nginx.conf", head=30)]
Librarian: "Here are the first 30 lines showing the global directives..."

User: "Check the last 20 lines to see if there are any closing brackets issues"
Librarian: [Uses read_document(path="/etc/nginx/nginx.conf", tail=20)]
Librarian: "Found it! Line 9995 is missing a closing brace."

User: "Write a summary of the issues and fixes to /librarian/nginx-fix.md"
Librarian: [Uses write_document() to create fix documentation]
```

**Tools Used**:
- `read_document()` with `start_line`, `end_line` - Targeted investigation
- `read_document()` with `head` - Understand structure
- `read_document()` with `tail` - Check file ending
- `write_document()` - Document the fix

**Why This Works**: Instead of reading massive files, you can target specific sections for efficient debugging `[Source: librarian-mcp]`

---

## Example 4: Semantic Research Across Technical Documentation

**Scenario**: You're researching how different database systems handle transactions and need information from various docs.

**Workflow**:
```
User: "How do PostgreSQL, MySQL, and MongoDB handle distributed transactions?"
Librarian: [Uses search_library() with semantic understanding]
Librarian: "Found 8 relevant chunks across your documentation..."

Librarian: "Based on the library, here's what I found:

**PostgreSQL**: Uses two-phase commit (2PC) protocol for distributed transactions.
[Source: postgres/architecture.md]

**MySQL**: Supports XA transactions for distributed systems.
[Source: mysql/transactions.md]

**MongoDB**: Uses multi-document ACID transactions since version 4.0.
[Source: mongodb/replication.md]

Would you like me to write a comparison table?"

User: "Yes, write a detailed comparison to /librarian/transaction-comparison.md"
Librarian: [Uses write_document() with aggregated information]
Librarian: "Created comprehensive comparison with implementation details and trade-offs"
```

**Tools Used**:
- `search_library()` - Semantic search across all documents
- `write_document()` - Create aggregated research output
- `list_indexed_documents()` - Verify coverage if needed

**Why This Works**: Semantic search understands meaning rather than just keywords, automatically combining information from multiple sources with proper citations `[Source: README.md]`, `[Source: ARCHITECTURE.md]`

---

## Example 5: Documentation Validation and Consistency Check

**Scenario**: You want to verify that your README documentation matches the actual implementation.

**Workflow**:
```
User: "Validate that the README.md claims match the actual implementation"
Librarian: [Uses search_library() to find README features]
Librarian: [Uses document_summary() and read_document() to check implementation]

Librarian: "I found 3 discrepancies:

**Issue 1**: README states 13 tools, but I count 14 production tools.
[Source: README.md] vs [Source: Tools.md]

**Issue 2**: README mentions Chonkie as 'upcoming', but it's the default backend.
[Source: README.md] vs [Source: ARCHITECTURE.md]

**Issue 3**: Security section lists 90+ exclusion patterns, but implementation has 94+.
[Source: README.md] vs [Source: security/exclusions.py]

Should I write a detailed validation report?"

User: "Write a full validation report to /librarian/documentation-validation.md"
Librarian: [Uses write_document() with detailed findings]
Librarian: "Created validation report with all discrepancies, suggested fixes, and file references"

User: "Now check if there are any TODO comments that should be cleaned up"
Librarian: [Uses search_documents(query="TODO")]
Librarian: "Found 12 TODO comments across 6 files. Listing them..."

User: "Add this to the validation report"
Librarian: [Reads existing report, appends TODO findings, writes back]
```

**Tools Used**:
- `search_library()` - Find documentation claims
- `document_summary()` - Understand code structure
- `read_document()` - Check specific implementations
- `search_documents()` - Find literal patterns (TODOs)
- `write_document()` - Create and update validation reports
- `list_indexed_documents()` - Verify document coverage

**Why This Works**: The librarian can systematically validate documentation against implementation, find contradictions, and suggest improvements `[Source: library_validation.md]`

---

## Summary of Tool Categories Demonstrated

1. **Code Investigation**: `search_documents()` for pattern finding
2. **Document Management**: `sync_documents()`, `get_document_status()`, `add_document()`
3. **Targeted Reading**: `read_document()` with line ranges, head, tail
4. **Semantic Research**: `search_library()` with AI aggregation
5. **Validation & Analysis**: Combined tools with `write_document()` for persistent results

Each example demonstrates the librarian's unique combination of semantic understanding, precise file access, and two-way communication - capabilities that go beyond simple search and enable real development workflows.
