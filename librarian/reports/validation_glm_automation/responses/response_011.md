# Query 11: File Reading Capabilities

**Status**: success
**Tokens Used**: 1934
**Timestamp**: 2026-03-19T15:01:49.664319
**Tool Calls**: 0

---

Based on my available tools, I have the following **file reading capabilities**:

## `read_document` Tool

I can read files with these parameters:
- **`path`** - The file path to read
- **`start_line`** - Begin reading from a specific line number
- **`end_line`** - Stop reading at a specific line number
- **`head`** - Read from the beginning of the file
- **`tail`** - Read from the end of the file
- **`max_chars`** - Limit the number of characters returned

## What This Means for You

**Yes, I can read specific portions of files** in several ways:

1. **Line ranges** - Read only lines 50-100 of a file
2. **Beginning** - Grab the first N lines or characters with `head`
3. **End** - Get the last N lines or characters with `tail`
4. **Character limits** - Read up to a specific character count
5. **Full file** - Read an entire document (subject to character limits)

## Other Related File Tools

I also have:
- **`document_summary(path)`** - Get an overview/summary of a file without reading it fully
- **`list_documents(path, extension, recursive)`** - Browse and discover files
- **`search_documents(query, path, extension, case_sensitive)`** - Search for literal text within files

---

**Would you like me to demonstrate?** If you tell me a file you'd like to explore, I can:
- Show you a summary of it
- Read specific line ranges
- Search for content within it
- Or just read portions of it based on what you need

What file would you like me to look at?
