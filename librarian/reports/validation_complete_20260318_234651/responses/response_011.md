# Query 11: File Reading Capabilities

**Status**: success
**Tokens Used**: 476
**Timestamp**: 2026-03-18T23:47:19.325848
**Tool Calls**: 0

---

Let me check the library's document reading capabilities and what's available.


Based on the library content, here's what I found about file reading capabilities:

## File Reading Capabilities

The Librarian has **targeted, secure file reading capabilities** designed for precise access rather than blind full-file reads:

### **Primary Reading Tool: `read_document()`**

This tool supports reading specific portions of files:

1. **Line ranges**: `start_line=1, end_line=10` - Read specific lines
2. **Head**: `head=50` - Read first N lines
3. **Tail**: `tail=50` - Read last N lines  
4. **Custom ranges**: `start_line=100, end_line=150` - Custom line ranges
5. **Character limits**: `max_chars=20000` - Up to 20,000 characters
6. **Default limit**: 8,000 characters (truncates large files)

### **Pre-Reading Tool: `document_summary()`**

Before reading large files, the Librarian recommends using `document_summary()` which provides:
- Markdown: Heading hierarchy
- Python/JS/TS: Functions and classes defined
- Text/other: Line/word count and first few lines

### **File System Search Tools**

- `list_documents()` - List documents in directories with sizes
- `search_documents()` - Literal text search across files
- `execute_command()` - Execute whitelisted commands (ls, cat, grep, etc.)

### **Key Design Principles**

1. **No blind full-file reads** - The system is designed to prevent truncation issues by targeting specific sections
2. **Security sandboxing** - Only operates within allowed directories
3. **`.librarianignore` respect** - Excluded content is inaccessible
4. **Citation requirement** - Every answer must reference source documents

**Would you like me to demonstrate reading a specific file section, or explore what documents are available in the library?**
