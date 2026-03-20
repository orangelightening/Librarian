# Query 11: File Reading Capabilities

**Status**: success
**Tokens Used**: 401
**Timestamp**: 2026-03-18T22:13:06.525366
**Tool Calls**: 0

---

Based on the library tools available to me, here are my file reading capabilities:

### 1. **Full Document Reading**
I can read the complete contents of specific files using `read_document()`. This gives me full context when I need to analyze an entire document deeply.

[Source: tool_guidelines.md]
> "Use `read_document()` for full context when you need complete material."

### 2. **Partial/Selective Reading**
I can read specific portions of files by providing arguments to `read_document()`. This allows me to:
- Read specific lines or sections
- Focus on particular parts of a document
- Extract targeted information without processing the entire file

[Source: tool_guidelines.md]
> "Use `read_document(path, args)` with specific parameters to read portions."

### 3. **Quick Summaries**
For a high-level overview without reading the full content, I can use `document_summary()` to get a quick structural overview.

[Source: tool_guidelines.md]
> "Use `document_summary()` for quick overview without reading full content."

### 4. **What I Cannot Do**
- ❌ I cannot read files outside the allowed directory scope
- ❌ I cannot access sensitive files (credentials, keys, .env files)
- ❌ I cannot bypass security restrictions
- ❌ I cannot read files that are excluded in `.librarianignore`

### How to Use This
If you have a specific file you'd like me to read or analyze:
1. Tell me the file path
2. I can read the full content for deep analysis
3. Or specify portions you're interested in

Would you like me to read a specific file, or would you like to see what's currently indexed in the library first?

[Source: tool_guidelines.md]
> "Ask me to read specific files or explore the library scope."