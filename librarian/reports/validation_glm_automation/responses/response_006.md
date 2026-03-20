# Query 6: System Prompt

**Status**: success
**Tokens Used**: 3424
**Timestamp**: 2026-03-19T15:01:49.663991
**Tool Calls**: 7

---

The Librarian's behavior is governed by the **`prompt.md` file** located in the project root directory. [Source: ARCHITECTURE.md]

This comprehensive system prompt defines:

### What's Defined in prompt.md:
1. **Role Definition** - Establishes the Librarian as an intelligent research assistant with access to a curated document library and secure file system tools [Source: prompt.md]

2. **Core Behavioral Principles**:
   - **Accuracy and Citations** - Always cite sources using `[Source: document_name.md]` format
   - **Helpful and Thorough** - Provide comprehensive answers based on available library content
   - **Secure and Respectful** - Respect `.librarianignore` exclusions and security boundaries
   - **Transparent About Limitations** - Acknowledge when information is unavailable [Source: prompt.md]

3. **Tool Usage Guidelines** - Detailed instructions for using all 14 available tools (7 library, 5 file system, 2 system) with specific parameters and best practices [Source: prompt.md, ARCHITECTURE.md]

4. **Security Boundaries** - Clear restrictions on file access, credential handling, and what the Librarian must never do (including never hallucinating information) [Source: prompt.md]

5. **Response Format** - Structured approach for providing answers with direct responses, citations, context, and suggestions [Source: prompt.md]

The ARCHITECTURE.md document confirms that **"All librarian behavior is governed by `prompt.md`"** and notes that this ensures "consistent, accurate, and well-cited responses" across all interactions. [Source: ARCHITECTURE.md]
