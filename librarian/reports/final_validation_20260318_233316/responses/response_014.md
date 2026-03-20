# Query 14: Tool Usage Examples

**Status**: success
**Tokens Used**: 725
**Timestamp**: 2026-03-18T23:33:16.593723
**Tool Calls**: 0

---

Here are 5 practical examples of how you would use the Librarian tools in real-world scenarios, demonstrating the typical workflow:

### Example 1: Researching a Specific Topic
**Scenario:** You want to understand how the team handles API versioning in their documentation.

1.  **Semantic Search:**
    ```bash
    search_library("API versioning strategy", limit=5)
    ```
    *This finds relevant documents semantically, not just by keyword.*

2.  **Review Results:**
    The search returns `api-design.md` and `changelog.md`.

3.  **Deep Dive (Targeted Reading):**
    Since `api-design.md` is likely long, you don't read it all at once.
    ```bash
    document_summary("api-design.md")
    # Then read specific sections:
    read_document("api-design.md", start_line=45, end_line=80)
    ```

### Example 2: Finding a Specific String or Code
**Scenario:** You need to find all instances where the `user_id` parameter is used in Python scripts.

1.  **Literal Text Search:**
    ```bash
    search_documents("user_id", extension=".py", case_sensitive=true)
    ```
    *This finds exact matches across files, unlike semantic search which understands context.*

2.  **Contextual Reading:**
    For each file returned, you use `document_summary` to check if it's relevant, then `read_document` to see the specific line usage.

### Example 3: Monitoring Document Health
**Scenario:** You added a new `config.yaml` file yesterday but haven't seen it in your library yet.

1.  **Check Status:**
    ```bash
    get_document_status("/path/to/config.yaml")
    ```
    *This tells you if the document is indexed and if it matches the file on disk.*

2.  **Sync if Needed:**
    If the status shows it's outdated or missing, you run a sync on the directory:
    ```bash
    sync_documents("/project/configs", extensions=".yaml", recursive=true)
    ```

### Example 4: Exploring a New Project Directory
**Scenario:** A new developer joins and you need to onboard them to the codebase structure.

1.  **List Documents:**
    ```bash
    list_documents("/new-project", extension=".md", recursive=true)
    ```
    *This gives you a complete inventory of all markdown files in the project.*

2.  **Synthesize Knowledge:**
    You pick up `README.md`, `CONTRIBUTING.md`, and `ARCHITECTURE.md` to give them a comprehensive overview.

### Example 5: Cleaning Up the Library
**Scenario:** You realize a document `deprecated-feature.md` is no longer relevant and needs removal.

1.  **Identify Document ID:**
    ```bash
    list_indexed_documents()
    ```
    *This lists all documents in the library with their IDs.*

2.  **Remove Document:**
    ```bash
    remove_document("doc_id_12345")
    ```
    *This cleans up the library index.*

---

**Would you like to try one of these examples right now?** I can help you search the library for something specific, or we can simulate a workflow to see how the tools interact.
