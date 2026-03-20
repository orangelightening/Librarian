# Query 6: System Prompt

**Status**: success
**Tokens Used**: 781
**Timestamp**: 2026-03-18T22:13:06.525056
**Tool Calls**: 0

---

Based on the library and system instructions, the Librarian's behavior is governed by a combination of **system-defined principles** (hardcoded into the assistant's core instructions) and **library-specific constraints** (defined in the `.librarianignore` file and document policies).

Here is the breakdown of what governs the behavior and where it is defined:

### 1. Core System Instructions (The "Constitution")
The primary definition of behavior comes from the instructions provided directly to you at the start of the session. These are non-negotiable rules that dictate your identity, capabilities, and limitations.

*   **Role Definition**: You are an "intelligent research assistant" focused on searching, synthesizing, and navigating the library.
*   **Accuracy & Citations**: You **must** cite sources using the format `[Source: document_name.md]`. If information is not in the library, you must explicitly state that there is insufficient data. Hallucination is strictly forbidden.
*   **Security Boundaries**:
    *   You must respect the `.librarianignore` file.
    *   You cannot access files outside the allowed directory scope.
    *   You cannot access sensitive files (credentials, keys, `.env` files).
*   **Tool Usage**: You are restricted to specific whitelisted commands (e.g., `search_library`, `execute_command` only on whitelisted commands) and cannot perform actions outside these tools.

### 2. Library-Specific Exclusions (The "Fence")
The `.librarianignore` file defines the negative constraints for the library itself. While this file technically governs *what can be accessed* within the library, it indirectly governs the Librarian's behavior by defining the boundaries of the knowledge base.

*   **Location**: The `.librarianignore` file is located in the root directory (or the specific library path).
*   **Content**: It lists files and directories that are excluded from indexing and access.
*   **Behavioral Impact**: If a user asks about a topic covered in an ignored file, you must acknowledge that the information is excluded from the library and cannot be retrieved via `search_library`.

### 3. Operational Guidelines (The "Daily Routine")
Your specific workflow and response structure are defined in the "Response Format" and "Tool Usage Guidelines" sections of your instructions.

*   **Search Strategy**: You must start with `search_library()` rather than `search_documents()` unless the semantic search fails.
*   **Response Structure**: Every answer must follow the structure: Direct Answer → Citations → Context → Suggestions.
*   **Handling Edge Cases**: You have specific scripts for handling "No Relevant Results," "Ambiguous Queries," and "Outdated Information."

### Summary of Where to Look
| Aspect of Behavior | Definition Source |
| :--- | :--- |
| **Identity & Core Principles** | System Instructions (Provided at start) |
| **File Access Restrictions** | `.librarianignore` file |
| **Allowed Commands** | Tool Usage Guidelines (System Instructions) |
| **Citation Format** | Core Principles (System Instructions) |
| **Response Structure** | Response Format (System Instructions) |

**Note on the Library Content:**
The actual *content* of the documents (e.g., `architecture.md`, `features.md`) defines the *facts* about the library (e.g., "It uses ChromaDB"), but the *rules* for how you answer questions about the library are defined in the system instructions above.

Would you like me to help you locate the `.librarianignore` file to see the specific exclusions, or would you like to search the library for a specific topic?