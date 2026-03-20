# Query 14: Tool Usage Examples

**Status**: success
**Tokens Used**: 1161
**Timestamp**: 2026-03-18T22:13:06.525553
**Tool Calls**: 0

---

Here are 5 practical examples of how you would use the Librarian tools in a real-world scenario, ranging from basic discovery to advanced file management:

### 1. Initial Onboarding: Assessing Library Health
**Scenario:** You have just connected to the system and need to understand what data is available before asking specific questions.

*   **Action:**
    1.  `get_library_stats()` to see the total document and chunk count.
    2.  `list_indexed_documents()` to get a quick overview of the document titles and types.
*   **Librarian Output:**
    > "I've checked the library stats. We currently have **1,240 documents** indexed across **45,000 chunks**.
    >
    > [Source: internal_system_state]
    >
    > The indexed documents primarily cover:
    > 1. `project_architecture.md`
    > 2. `user_guide_v2.md`
    > 3. `api_reference.json`
    > 4. `security_policies.md`
    >
    > Would you like me to search specifically within the `api_reference.json` for a specific endpoint?"

### 2. Deep Research: Verifying a Specific Claim
**Scenario:** You need to confirm a specific detail found in a document (e.g., a deployment step) and want to see the exact source text.

*   **Action:**
    1.  `search_library(query="docker compose deployment steps")`
    2.  `read_document(path="deployment_guide.md")` (using the path found in step 1).
*   **Librarian Output:**
    > "Semantic search found 3 relevant documents regarding Docker deployment.
    >
    > [Source: deployment_guide.md]
    >
    > According to the guide, the deployment steps are:
    > 1. Pull the latest image from the registry.
    > 2. Create a `docker-compose.yml` file.
    > 3. Run `docker-compose up -d`.
    >
    > [Source: deployment_guide.md]
    >
    > Here is the full context from the file:
    > ```markdown
    > ### Step 3: Start the Container
    > Once the configuration is ready, execute the following command to start the services in detached mode:
    > $ docker-compose up -d
    > ```
    >
    > The document was last updated on [Date]. Would you like me to check if there are any newer versions in the file system?"

### 3. Broad Search: Finding Literal Text Matches
**Scenario:** Semantic search didn't return the exact error code you are looking for, so you need a literal string search.

*   **Action:**
    1.  `search_documents(query="ERR_503", path="logs/", extension="*.log")`
*   **Librarian Output:**
    > "Semantic search was too broad for your specific error code. I performed a literal text search within the `logs/` directory for files ending in `.log`.
    >
    > Found **2 matches** for `ERR_503`:
    > 1. `server_2023_10_24.log`
    > 2. `gateway_2023_10_25.log`
    >
    > Would you like me to read the full contents of `server_2023_10_24.log` to see the surrounding context?"

### 4. System Maintenance: Checking for Outdated Documents
**Scenario:** You suspect a document might be outdated because the file system has been updated recently, but the library hasn't caught up.

*   **Action:**
    1.  `get_document_status(path="pricing_tiers.md")`
*   **Librarian Output:**
    > "I checked the status of `pricing_tiers.md`.
    >
    > [Source: internal_system_state]
    >
    > **Status:** Outdated.
    > The document in the library was last indexed on **October 1st**.
    > However, the file in the file system was modified on **October 15th**.
    >
    > This indicates the library needs to be synced or the document re-indexed to reflect the latest changes. Would you like me to trigger a sync for this specific file?"

### 5. File Exploration: Navigating the Directory Structure
**Scenario:** You know a file exists but don't know its location. You want to find it before adding it to the library or reading it.

*   **Action:**
    1.  `list_documents(path="/data/reports/", extension="*.csv", recursive=True)`
*   **Librarian Output:**
    > "I explored the `/data/reports/` directory recursively for CSV files.
    >
    > Found the following documents:
    > 1. `/data/reports/quarterly_metrics_2023.csv`
    > 2. `/data/reports/quarterly_metrics_2024.csv`
    > 3. `/data/reports/expense_summary.csv`
    >
    > Would you like me to add `quarterly_metrics_2024.csv` to the library so I can search its contents later?"