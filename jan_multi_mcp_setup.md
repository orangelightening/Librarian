# Multi-MCP Setup Guide for Jan

**Created**: 2026-03-22
**Purpose**: Run multiple librarian libraries simultaneously in Jan

---

## Overview

Each librarian library requires its own **MCP server instance** because MCP servers have single-configuration environments. To use multiple libraries in Jan, you create multiple MCP servers and assign them to different assistants.

## Architecture

```
Jan Application
├── Assistant: botany_librarian
│   ├── System Prompt: Botany-focused
│   └── MCP Server: botany_librarian
│       └── Library: /home/peter/botany
│
└── Assistant: project_librarian
    ├── System Prompt: Development-focused
    └── MCP Server: project_librarian
        └── Library: /home/peter/development/librarian-mcp
```

**Key Points:**
- Each library = One MCP server
- Each MCP server has unique environment variables
- Each assistant uses its dedicated MCP server
- Libraries are completely isolated

## Setup Process

### Step 1: Create Libraries

If you haven't already, create your libraries:

```bash
cd /home/peter/development/librarian-mcp

# Botany library
./scripts/create_library.sh /home/peter/botany \
  --name botany \
  --extensions .md,.pdf

# Project library
./scripts/create_library.sh /home/peter/development/librarian-mcp \
  --name librarian-mcp \
  --extensions .md,.txt,.py,.js,.ts,.json,.yaml,.yml,.toml,.rst,.html
```

### Step 2: Generate Jan MCP Configurations

```bash
cd /home/peter/development/librarian-mcp

# Botany library MCP
./scripts/generate_jan_config.sh /home/peter/botany botany_librarian

# Project library MCP
./scripts/generate_jan_config.sh /home/peter/development/librarian-mcp project_librarian
```

Each command outputs JSON configuration for Jan.

### Step 3: Add MCP Servers in Jan

**For Botany Library:**

1. Open Jan
2. Settings → MCP Servers
3. Click "Add Server"
4. Name: `botany_librarian`
5. Configuration:
```json
{
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "args": ["/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"],
  "env": {
    "LIBRARIAN_SAFE_DIR": "/home/peter/botany",
    "LIBRARIAN_CHROMA_PATH": "/home/peter/botany/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/home/peter/botany/.librarian/metadata",
    "LIBRARIAN_BACKEND": "chonkie"
  }
}
```

**For Project Library:**

1. Click "Add Server" again
2. Name: `project_librarian`
3. Configuration:
```json
{
  "command": "/home/peter/development/librarian-mcp/venv/bin/python",
  "args": ["/home/peter/development/librarian-mcp/mcp_server/librarian_mcp.py"],
  "env": {
    "LIBRARIAN_SAFE_DIR": "/home/peter/development/librarian-mcp",
    "LIBRARIAN_CHROMA_PATH": "/home/peter/development/librarian-mcp/.librarian/chroma_db",
    "LIBRARIAN_METADATA_PATH": "/home/peter/development/librarian-mcp/.librarian/metadata",
    "LIBRARIAN_BACKEND": "chonkie"
  }
}
```

### Step 4: Create Assistants

**Botany Librarian Assistant:**

1. Settings → Assistants
2. Create New Assistant
3. Name: `botany_librarian`
4. System Prompt:
```markdown
You are a botanical research librarian with access to a curated library of botany PDFs and markdown files. You help users search for and discover information about plants, agriculture, and gardening. Always cite your sources using the format: Source: document_name. You write analysis reports to /librarian/reports/ for user review.
```
5. **MCP Servers**: Enable ONLY `botany_librarian` MCP

**Project Librarian Assistant:**

1. Create New Assistant
2. Name: `project_librarian`
3. System Prompt:
```markdown
You are a software development librarian with access to the Librarian MCP Server project documentation. You help users understand the codebase, architecture, and configuration. Always cite your sources using the format: Source: document_name. You write analysis reports to /librarian/reports/ for user review.
```
5. **MCP Servers**: Enable ONLY `project_librarian` MCP

### Step 5: Index Each Library

```bash
# Botany library (after PDF support is added)
/home/peter/botany/.librarian/rebuild.sh

# Project library
/home/peter/development/librarian-mcp/.librarian/rebuild.sh
```

### Step 6: Restart MCP Servers

In Jan:
1. Settings → MCP Servers
2. Toggle `botany_librarian` OFF → ON
3. Toggle `project_librarian` OFF → ON
4. Start new chats

## Verification

**Test Botany Library:**
```
[New chat with botany_librarian assistant]
User: How many documents are indexed?
Librarian: There are X documents in the library.

User: What do you have about plants?
Librarian: [Searches botany library, not project library]
```

**Test Project Library:**
```
[New chat with project_librarian assistant]
User: How many documents are indexed?
Librarian: There are Y documents in the library.

User: What's the architecture?
Librarian: [Searches project library, not botany library]
```

## Library Isolation

**Each library is completely isolated:**

| Component | Botany Library | Project Library |
|-----------|---------------|-----------------|
| Documents | /home/peter/botany | /home/peter/development/librarian-mcp |
| ChromaDB | /home/peter/botany/.librarian/chroma_db | /home/peter/development/librarian-mcp/.librarian/chroma_db |
| Metadata | /home/peter/botany/.librarian/metadata | /home/peter/development/librarian-mcp/.librarian/metadata |
| Sandbox | /home/peter/botany/.librarian/sandbox | /home/peter/development/librarian-mcp/.librarian/sandbox |
| MCP Server | botany_librarian | project_librarian |
| Assistant | botany_librarian | project_librarian |

**No cross-contamination:** The botany librarian cannot access project documentation, and vice versa.

## Managing Multiple Libraries

### List All Libraries

```bash
cd /home/peter/development/librarian-mcp
./scripts/list_libraries.sh
```

### Switch Libraries

No need to switch! Each assistant has its own dedicated MCP server and library. Just:
1. Start a new chat
2. Select the appropriate assistant
3. That assistant's MCP server loads the correct library

### Add New Library

1. Create the library:
```bash
./scripts/create_library.sh /path/to/new-library --name my-library
```

2. Generate MCP config:
```bash
./scripts/generate_jan_config.sh /path/to/new-library my_library_librarian
```

3. Add MCP server in Jan using generated config

4. Create new assistant in Jan

5. Index the new library

## Troubleshooting

### Issue: Wrong library loaded

**Cause:** Assistant assigned to wrong MCP server

**Solution:**
1. Settings → Assistants
2. Edit the assistant
3. Ensure correct MCP server is enabled
4. Ensure other MCP servers are DISABLED for this assistant

### Issue: Both assistants show same document count

**Cause:** Both MCP servers pointing to same library

**Solution:**
1. Check MCP server environment variables
2. Ensure `LIBRARIAN_CHROMA_PATH` and `LIBRARIAN_METADATA_PATH` are different
3. Restart MCP servers after correcting

### Issue: "No documents found"

**Cause:** Library not indexed yet

**Solution:**
```bash
# Rebuild the specific library
/path/to/library/.librarian/rebuild.sh
```

## Best Practices

### DO:
✅ Create one MCP server per library
✅ Name MCP servers clearly: `{library}_librarian`
✅ Create dedicated assistants for each library
✅ Keep system prompts focused on library content
✅ Test isolation between libraries

### DON'T:
❌ Try to use one MCP server for multiple libraries
❌ Enable multiple library MCPs for one assistant
❌ Share ChromaDB or metadata between libraries
❌ Forget to restart MCP servers after configuration changes

## Example Use Cases

### Use Case 1: Research + Development

**Botany Research Library:**
- Assistant: `botany_librarian`
- MCP: `botany_librarian`
- Content: PDF research papers, botanical guides
- Purpose: Research and reference

**Development Library:**
- Assistant: `dev_librarian`
- MCP: `dev_librarian`
- Content: Code documentation, APIs, architecture
- Purpose: Development support

### Use Case 2: Personal + Work

**Personal Library:**
- Assistant: `personal_librarian`
- MCP: `personal_librarian`
- Location: `~/Documents`
- Purpose: Personal knowledge base

**Work Library:**
- Assistant: `work_librarian`
- MCP: `work_librarian`
- Location: `~/Work/Documents`
- Purpose: Work documentation

## Advanced: Dynamic Library Switching (Not Recommended)

You might wonder: *Can I switch libraries without multiple MCP servers?*

**Answer:** Not really. MCP servers are designed to be single-configuration. Dynamic switching would require:
1. Modifying the MCP server to reload configuration
2. Restarting the MCP server on every library change
3. Complex state management
4. Slow performance

**Better approach:** Multiple MCP servers (as documented here) - clean, fast, reliable.

## Summary

**Multi-library setup in Jan:**
1. Create libraries with `create_library.sh`
2. Generate MCP configs with `generate_jan_config.sh`
3. Add MCP servers in Jan (one per library)
4. Create assistants (one per library/MCP)
5. Index each library independently
6. Use appropriate assistant for each library

**Result:** Clean isolation, focused assistants, reliable operation.

---

*This architecture scales to any number of libraries. Each library gets its own MCP server and assistant.*
