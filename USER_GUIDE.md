# Librarian MCP Server - User Guide

## What is the Librarian?

The Librarian is an AI assistant that helps you search and organize your documents. Think of it as having a personal research assistant who has read all your documents and can instantly find relevant information.

**What it does:**
- ✅ Searches your documents semantically (understands meaning, not just keywords)
- ✅ Reads specific files when you need full context
- ✅ Lists and browses your file collection
- ✅ Provides citations so you know where information came from
- ✅ Respects your privacy (won't access sensitive files)

---

## MCP Client Configuration

To use the Librarian, you need to configure your MCP client (Jan, LM Studio, Claude Desktop, etc.) with the following settings.

### JSON Configuration

**For Jan:**
```json
{
  "mcpServers": {
    "librarian": {
      "command": "/home/peter/development/librarian-mcp/venv/bin/python",
      "args": [
        "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py",
        "--safe-dir",
        "/home/peter/development/librarian-mcp"
      ],
      "env": {
        "PYTHONPATH": "/home/peter/development/librarian-mcp"
      }
    }
  }
}
```

**For LM Studio:**
```json
{
  "mcpServers": {
    "librarian": {
      "command": "/home/peter/development/librarian-mcp/venv/bin/python",
      "args": [
        "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py",
        "--safe-dir",
        "/home/peter/development/librarian-mcp"
      ],
      "env": {
        "PYTHONPATH": "/home/peter/development/librarian-mcp"
      }
    }
  }
}
```

**For Claude Desktop:**
```json
{
  "mcpServers": {
    "librarian": {
      "command": "/home/peter/development/librarian-mcp/venv/bin/python",
      "args": [
        "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py",
        "--safe-dir",
        "/home/peter/development/librarian-mcp"
      ],
      "env": {
        "PYTHONPATH": "/home/peter/development/librarian-mcp"
      }
    }
  }
}
```

### Configuration Options

**`--safe-dir`**: The directory the Librarian can access
- Change this to limit where the Librarian can look
- Example: `--safe-dir ~/Documents` (only access Documents folder)
- Default: `--safe-dir ~/` (access entire home directory)

**Full path customization:**
```json
{
  "mcpServers": {
    "librarian": {
      "command": "/home/peter/development/librarian-mcp/venv/bin/python",
      "args": [
        "/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py",
        "--safe-dir", "/home/peter/Documents",
        "--documents-dir", "/home/peter/development/librarian-mcp/documents",
        "--chroma-path", "/home/peter/development/librarian-mcp/chroma_db"
      ],
      "env": {
        "PYTHONPATH": "/home/peter/development/librarian-mcp"
      }
    }
  }
}
```

### Important: Use the Venv Python Path

**Always use the venv python path:** `/home/peter/development/librarian-mcp/venv/bin/python`

This ensures the MCP server has access to all required packages (fastmcp, chromadb, etc.).

### Verifying Your Setup

**Check the venv python exists:**
```bash
ls -la /home/peter/development/librarian-mcp/venv/bin/python
```

**Test the MCP server manually:**
```bash
cd /home/peter/development/librarian-mcp
./setup_mcp.sh
```

If the server starts successfully, your configuration is correct!

### Important Notes

**Always use the venv python:** The server must use the venv's python to access required packages. Using system python will cause import errors.

**PYTHONPATH is required:** The environment variable must be set so Python can find the mcp_server module.

**Customizing paths:** You can change `--safe-dir` to limit where the librarian can access (e.g., `~/Documents` instead of the entire project).

---

## Quick Start

### 1. Start the Server

```bash
cd /home/peter/development/librarian-mcp
./setup_mcp.sh
```

The server is now running and ready to help!

### 2. Add Your Documents

```bash
# Add all markdown files from a directory
python scripts/ingest.py --path ~/Documents --extensions .md

# Add specific file types
python scripts/ingest.py --path ~/project --extensions .md,.txt,.py

# Add everything
python scripts/ingest.py --path ~/Documents
```

### 3. Use the Librarian

In your AI chat interface (Jan, LM Studio, etc.), just ask:

```
"Search for information about project architecture"
"What do my documents say about testing?"
"Find all documents mentioning security"
"List all documents in the library"
```

---

## Controlling What Gets Indexed

### The `.librarianignore` File

**Location:** `/home/peter/development/librarian-mcp/.librarianignore`

This file tells the Librarian what **NOT** to index. It works like `.gitignore` - any file or directory matching a pattern in this file will be completely ignored.

**What's ignored by default:**
- Passwords and credentials (`.env`, `*.key`, `credentials.*`)
- Virtual environments (`venv/`, `node_modules/`)
- Git repositories (`.git/`)
- Databases (`*.db`, `chroma_db/`)
- Logs and temporary files
- Binary files (images, PDFs, executables)

### Adding Your Own Exclusions

**Edit the `.librarianignore` file:**

```gitignore
# Ignore my private documents
documents/private/
work/confidential/

# Ignore specific file types
*.tmp
*.draft
backup/

# Ignore specific directories
archives/
old-projects/
```

**Pattern examples:**
- `*.log` - Ignore all `.log` files
- `temp/` - Ignore any directory named `temp`
- `*.secret` - Ignore files ending in `.secret`
- `documents/private/` - Ignore that specific path

### Why Use `.librarianignore`?

**Privacy:** Keep sensitive information out of the index
**Performance:** Don't waste time indexing temporary files
**Relevance:** Only index what you actually want to search

---

## Talking to the Librarian

### Important: Setting Up the Persona

**The librarian persona may need to be set in your model's system prompt.**

Some MCP clients don't automatically pass the librarian persona to the AI model. If the model responds as "Claude" or a generic AI assistant instead of as the Librarian, you need to add the librarian instructions to your model's system prompt.

**In Jan:**
1. Go to Model Settings
2. Find "System Prompt" or "Custom Instructions"
3. Add the librarian persona (see below - "Librarian System Prompt" section)

**Test if it's working:**
- Ask: "Who are you?"
- Expected: "I am the Librarian..."
- If you get "I'm Claude..." then you need to add the system prompt

---

## Librarian System Prompt

**Copy and paste this into your model's System Prompt in Jan:**

```
You are the Librarian, an intelligent research assistant with access to a curated document library and secure file system tools.

## Your Role
- Search and Discover: Find relevant information in the library using semantic search
- Synthesize: Combine information from multiple sources into coherent answers
- Cite Sources: Always reference which documents provided information
- Navigate: Help users explore the file system securely
- Manage: Assist with document ingestion and library maintenance

## Core Principles

### Accuracy and Citations
- ALWAYS cite sources when providing information from the library
- Use the format: [Source: document_name.md]
- Distinguish between library content and general knowledge

### Helpful and Thorough
- Provide comprehensive answers based on available library content
- If the library doesn't contain relevant information, say so clearly
- Suggest follow-up searches or related topics

### Secure and Respectful
- Only access files and directories within the allowed scope
- Respect the .librarianignore file - excluded content is off-limits
- Never attempt to bypass security restrictions
- Protect sensitive information (credentials, private keys, etc.)

## Available Tools

### Library Tools
- search_library(query, limit): Semantic search over documents
- sync_documents(path, extensions, recursive): Sync directory to library
- add_document(path): Add single document to library
- remove_document(document_id): Remove document from library
- list_indexed_documents(): List all indexed documents
- get_document_status(path): Check document status
- get_library_stats(): Get library statistics

### CLI Tools
- execute_command(command, args, cwd): Execute whitelisted commands
- read_document(path): Read file contents
- list_documents(path, extension, recursive): List files
- search_documents(query, path, extension): Search file contents
- document_summary(path): Get file structure summary

You are helpful, accurate, and respectful of boundaries.
```

**After adding this, the model should respond as the Librarian instead of as Claude.**

---

## Talking to the Librarian

### Natural Language is Best

The Librarian understands natural language. Just ask like you would ask a person:

**Good examples:**
```
"What do my documents say about API design?"
"Find information about error handling"
"Show me documents related to testing"
"What's the architecture of the system?"
```

**Avoid:**
- ❌ Specific search syntax (the Librarian does semantic search)
- ❌ Boolean operators (AND, OR, NOT)
- ❌ Complex queries (keep it conversational)

### Getting Better Results

**Be specific:**
- ❌ "Tell me about it"
- ✅ "What do the documents say about database migration?"

**Provide context:**
- ❌ "How do I fix it?"
- ✅ "How do I fix authentication errors in the API?"

**Follow up:**
- "That's helpful, can you show me more details from the architecture document?"
- "Can you search for related information about deployment?"

### Understanding Citations

The Librarian always tells you where information came from:

```
Based on the library, the system uses ChromaDB for vector storage.

[Source: architecture.md]
Documents are chunked into 1000-character segments...

[Source: features.md]
Change detection uses SHA-256 checksums...
```

**Why cite sources?**
- Lets you verify information
- Helps you find the full document
- Builds trust in the answers

---

## Available Commands

### Library Commands

**Search:**
```
"Search for [topic]"
"Find documents about [subject]"
"What do we have on [topic]?"
```

**Add Documents:**
```
"Add the file ~/notes/ideas.md to the library"
"Sync the directory ~/Documents"
```

**Check Status:**
```
"List all indexed documents"
"Get library statistics"
"Is the file ~/readme.md indexed?"
"Show me what's in the library"
```

**Manage Documents:**
```
"Remove document [document-id]"
"Check if ~/document.md is up to date"
```

### File System Commands

**Read Files:**
```
"Read the file ~/config.yaml"
"Show me the contents of readme.md"
```

**List Files:**
```
"List all markdown files in ~/Documents"
"Show me Python files in ~/project"
```

**Search Within Files:**
```
"Search for 'TODO' in all markdown files"
"Find 'error' in ~/project/src/"
```

**File Summary:**
```
"Give me a summary of ~/document.md"
"What's the structure of main.py?"
```

---

## Common Workflows

### Research a Topic

```
You: "What do my documents say about microservices?"

Librarian: [Provides answer with citations from multiple documents]

You: "Can you show me more details from the architecture document?"

Librarian: [Reads the full document and provides more context]
```

### Find a Specific Document

```
You: "List all indexed documents"

Librarian: [Shows all documents with IDs]

You: "Read the file ~/docs/api-reference.md"
```

### Add New Documents

```
You: "Add the file ~/new-research/paper.md to the library"

Librarian: "Added document 'paper.md' with 5 chunks. Document ID: abc123"
```

### Keep Library Updated

```
You: "Sync the directory ~/Documents"

Librarian: "Sync completed for directory: ~/Documents
  Added: 3 documents
  Updated: 1 documents
  Unchanged: 15 documents
  Ignored: 47 (excluded by .librarianignore)"
```

---

## Privacy and Security

### What the Librarian CANNOT Do

**File system safety:**
- ❌ Cannot delete files
- ❌ Cannot modify files
- ❌ Cannot create new files
- ❌ Cannot access files outside allowed directories

**Command restrictions:**
- ❌ Cannot run dangerous commands (rm, chmod, etc.)
- ❌ Cannot access system directories
- ❌ Cannot run commands outside allowed directory

### What Gets Stored

**Indexed:**
- Document text content
- File metadata (name, path, size, modification time)
- Checksums (for change detection)

**NOT stored:**
- File contents in original form
- Passwords or credentials (unless in plain text documents)
- Anything matching `.librarianignore` patterns

### Best Practices

**DO:**
✅ Keep sensitive files in `.librarianignore`
✅ Use `.env` files for credentials (auto-ignored)
✅ Review what gets indexed
✅ Keep your `.librarianignore` updated

**DON'T:**
❌ Store passwords in plain text documents
❌ Index entire home directory
❌ Ignore warnings about ignored files
❌ Put sensitive data in indexed locations

---

## Tips and Tricks

### 1. Start Small

Begin with a focused collection of documents:
```
python scripts/ingest.py --path ~/project/docs --extensions .md
```

### 2. Organize by Topic

Keep related documents together:
```
~/Documents/work/
~/Documents/personal/
~/Documents/projects/
```

### 3. Use Descriptive Filenames

Good:
```
api-design-doc.md
meeting-notes-2025-03-15.md
architecture-v2.md
```

Avoid:
```
doc1.md
notes.txt
stuff.md
```

### 4. Regular Updates

Keep your library current:
```
# Add new documents
python scripts/ingest.py --path ~/Documents

# The Librarian automatically detects changes and updates
```

### 5. Test Your Ignore Patterns

Check what's being ignored:
```
# Add a test file
touch ~/Documents/test-secret.txt

# Try to ingest
python scripts/ingest.py --path ~/Documents

# Check the output - "Ignored: X (excluded by .librarianignore)"
```

---

## Troubleshooting

### "I don't get any results"

**Try:**
- Use more general terms
- Rephrase your question
- Check if relevant documents are indexed: `list_indexed_documents()`
- Try broader search terms

### "The librarian ignored my document"

**Check:**
- Is the file in `.librarianignore`?
- Does it match an ignore pattern?
- Is it a supported file type? (`.md`, `.txt`, `.py`, etc.)

### "How do I see what's indexed?"

```
"List all indexed documents"
"Get library statistics"
```

### "The librarian can't find my file"

**Make sure:**
- The file is in the allowed directory
- The file type is supported
- The file isn't ignored by `.librarianignore`
- You've ingested the directory: `python scripts/ingest.py --path ~/path`

---

## Getting Help

### Check What's Available

```
"Server info" - Shows configuration and allowed commands
"List indexed documents" - Shows what's in the library
"Get library stats" - Shows statistics
```

### Review Documentation

- `.librarianignore` - Edit to control what gets indexed
- Output of `sync_documents` - Shows what happened during sync
- Citation information - Shows source documents

---

## Advanced: Customizing Behavior

### Change Allowed Directory

Edit `setup_mcp.sh` or use command line:
```bash
./setup_mcp.sh --safe-dir ~/Documents
```

### Change Document Storage

```bash
./setup_mcp.sh --documents-dir ~/my-library
```

### Change Ignored Patterns

Edit `.librarianignore` and re-sync:
```bash
# Edit .librarianignore
# Then re-run sync
python scripts/ingest.py --path ~/Documents
```

---

## Summary

The Librarian is your personal research assistant. It:
- ✅ Understands natural language
- ✅ Searches semantically (finds related concepts)
- ✅ Always cites sources
- ✅ Respects your privacy
- ✅ Works with your existing documents

**Start simple:** Add a few documents, try some searches, and expand from there!

**Remember:** The `.librarianignore` file is your friend - use it to control what gets indexed and keep sensitive information private.

---

**Need help?** Check the output of `server_info` or review this guide for common workflows.
