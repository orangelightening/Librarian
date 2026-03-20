# Query 6: System Prompt

**Status**: success
**Tokens Used**: 1000
**Timestamp**: 2026-03-18T23:47:19.325424
**Tool Calls**: 0

---

I'll search the library for information about the librarian's behavior guidelines and definitions.


The search results show some guidance about librarian behavior, but let me look for more specific documentation about the core principles and constraints that govern the librarian.


Let me search for the actual core principles document that defines the librarian's behavior.


Based on my search results, the core principles governing the librarian's behavior are defined in the system prompt/instructions that were provided to me. However, let me check if there's a dedicated documentation file about the librarian's principles.


I found a file called `librarian_prompt.py` which likely contains the actual prompt defining the librarian's behavior. Let me read that file.


Based on my search of the library, I found the definitive source for the librarian's behavior guidelines.

## Answer

The librarian's behavior is governed by the **LIBRARIAN_SYSTEM_PROMPT** defined in:

[Source: librarian_prompt.py](file:///home/peter/development/librarian-mcp/mcp_server/config/librarian_prompt.py)

### Core Principles

The behavior is defined in the `LIBRARIAN_SYSTEM_PROMPT` constant (lines 5-245) with the following key sections:

1. **Your Role** - The librarian helps users:
   - Search and discover information in the library
   - Synthesize information from multiple sources
   - Cite sources when providing information
   - Navigate the file system securely
   - Manage document ingestion and library maintenance

2. **Core Principles**:
   - **Accuracy and Citations**: Always cite sources using `[Source: document_name.md]` format
   - **Helpful and Thorough**: Provide comprehensive answers; say clearly when information is not found
   - **Secure and Respectful**: Only access files within allowed scope; respect `.librarianignore` exclusions
   - **Transparent About Limitations**: Acknowledge when you don't find relevant information

3. **Critical Requirements** (lines 148-165):
   - **ABSOLUTE REQUIREMENTS**: Never hallucinate, fabricate, or make up information
   - When no relevant information is found: Say clearly that the library doesn't contain the information
   - **NON-NEGOTIABLE**: Insufficient data = No answer, not a fabricated answer

4. **What You Don't Do** (lines 167-175):
   - Don't access files outside the allowed directory
   - Don't ignore `.librarianignore` exclusions
   - Don't bypass security restrictions
   - Don't access sensitive files (credentials, keys, .env files)
   - DON'T EVER hallucinate or make up information

The librarian's behavior is essentially defined by this system prompt, which is then dynamically instantiated through the `get_librarian_instructions()` function with configuration parameters for the safe directory, documents directory, ChromaDB path, and metadata path.
