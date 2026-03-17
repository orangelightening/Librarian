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

## Model Requirements & Performance Expectations

**⚠️ IMPORTANT: The Librarian's performance depends heavily on the AI model you use with it.**

### What Makes a Good Model for the Librarian?

The Librarian is an MCP server that provides tools to an AI model. The model must be:
- **Tool-capable**: Able to understand and use function calling/tool use
- **Good at reasoning**: Can chain multiple tool calls together
- **Strong at synthesis**: Can combine information from multiple sources
- **Nuanced understanding**: Can provide analysis, not just extract facts

### Model Performance Tiers

**🔴 Entry-Level Models (7B-9B parameters)**
- **Examples**: Qwen3.5 9B, Llama 3.1 8B
- **Performance**: Barely adequate
- **Behavior**:
  - May only perform 1-2 tool calls per query
  - Limited ability to synthesize complex information
  - Responses are factual but lack depth
  - May miss connections between documents
- **Hardware**: Can run on modest GPUs with 4-bit quantization
- **Best for**: Simple factual queries, single-document lookups

**🟡 Mid-Range Models (14B-27B parameters)**
- **Examples**: Qwen3.5 14B, Llama 3.1 70B (quantized), Mixtral 8x7B
- **Performance**: Good to very good
- **Behavior**:
  - Will perform 3-5 tool calls per query
  - Better at synthesizing information from multiple sources
  - Can provide nuanced analysis and connections
  - More thorough exploration of related topics
- **Hardware**: Requires capable GPU (12GB+ VRAM) or CPU with good RAM
- **Best for**: Research, multi-document queries, complex analysis

**🟢 High-End Models (30B+ parameters or Cloud APIs)**
- **Examples**: GLM-4.7, Claude, GPT-4, DeepSeek
- **Performance**: Excellent
- **Behavior**:
  - Extensive tool use (5+ calls per query)
  - Sophisticated synthesis and analysis
  - Understands context and nuance deeply
  - Proactive in exploring related information
  - Exceptional citation and source attribution
- **Hardware**: Cloud API or high-end local hardware
- **Best for**: Complex research, comprehensive analysis, professional work

### Real-World Performance Comparison

**Test Query**: "What acts as the system 'front end'?"

**GLM-4.7 (High-End Cloud Model)**: ✅ **CORRECT ANSWER**
- ✅ Performed 3 searches to explore different aspects
- ✅ Read multiple files for context
- ✅ Provided nuanced, accurate response with proper citations
- ✅ Synthesized information from architecture, features, and documentation
- ✅ **Key insight**: Correctly identified that MCP clients (Jan, LM Studio) are the actual front end, not the server itself
- ✅ Found the design decision: "MCP-First: No FastAPI/Gradio - pure MCP server"
- ✅ Explained historical context (old librarian project vs. current MCP architecture)

**Qwen3.5 9B 4-bit (Entry-Level Local Model)**: ❌ **WRONG ANSWER**
- ⚠️ Performed only 1 search
- ⚠️ Minimal file reading
- ⚠️ Response was confident but **fundamentally incorrect**
- ⚠️ Limited depth and synthesis
- ❌ **Incorrectly stated**: `librarian_mcp.py` is the "front end"
- ❌ **Missed**: The MCP architecture uses external clients as the front end
- ❌ **Assumption**: "main entry point" = "front end" without understanding architectural context

**The Critical Difference**:
- Qwen found a file, made a reasonable-sounding assumption, and gave a **wrong answer confidently**
- GLM-4.7 researched the architectural decisions, found explicit documentation, and gave a **nuanced, correct answer**

**This Matters Because**:
- Wrong answers waste time and mislead users
- The librarian's value depends on accurate information retrieval
- Smaller models may confidently state incorrect information
- Complex queries require models that can understand context and architecture

### Hardware Recommendations

**For Local Models:**
- **GPU**: NVIDIA GPU with 12GB+ VRAM recommended for 14B+ models
- **System RAM**: 32GB+ if running on CPU
- **Quantization**: 4-bit or 8-bit quantization essential for larger models
- **Model Size**: 27B+ recommended for optimal librarian performance

**For Cloud Models:**
- Any tool-capable model (Claude, GPT-4, GLM, etc.) will perform excellently
- No special hardware requirements
- Better performance but requires internet connection

### Critical Requirements

**✅ The Model MUST Be:**
1. **Tool-capable**: Must support function calling or tool use
2. **Trained on instructions**: Instruction-tuned models perform better
3. **Able to follow context**: Must maintain conversation context

**❌ These Will NOT Work Well:**
- Base models (not instruction-tuned)
- Models without tool-use capabilities
- Very small models (< 7B parameters)
- Models trained only for completion (not instructions)

### Getting Best Performance

**For Local Use:**
```
Recommended: Qwen3.5 14B or larger (quantized)
Hardware: GPU with 12GB+ VRAM
Alternative: Cloud API for best performance
```

**For Cloud Use:**
```
Any of: Claude, GPT-4, GLM-4, DeepSeek
Performance: Excellent regardless of specific model
```

### Bottom Line

The Librarian MCP server works with any tool-capable model, but **the model you choose dramatically affects the quality of results**.

- **Testing/evaluation**: Start with a 9B model to see if it meets your needs
- **Serious use**: Upgrade to 14B+ or use a cloud API
- **Professional work**: Use high-end cloud models for best results

The MCP server and library are the same regardless of model - only the model's ability to use tools effectively changes.

---

## Quick Start (Recommended Method)

**⚠️ IMPORTANT**: This quick start method requires basic technical knowledge (command line, file editing). For easier installation, see "Docker Installation (Phase 2)" below.

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/librarian-mcp.git
cd librarian-mcp

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
# Start the MCP server (easy method!)
./setup_mcp.sh
```

That's it! The server is now running and ready to connect to your MCP client.

### Step 3: Configure Your MCP Client

Add this to your MCP client's configuration (Jan, LM Studio, etc.):

**For Jan/LM Studio:**
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

### Step 4: Add Documents (Through Your MCP Client)

Once your client is connected, use the Librarian's tools:

```
"Sync the directory ~/Documents to the library"
"Add the file readme.md to the library"
"List all indexed documents"
```

No need to run manual scripts - the Librarian handles everything through the MCP interface!

### Step 5: Start Searching

```
"What do my documents say about architecture?"
"Find information about error handling"
"Search for security best practices"
```

---

## Installation Time Estimate

- **Tech-savvy users**: ~15-20 minutes
- **Comfortable with command line**: ~20-30 minutes
- **New to command line**: May require additional learning time

**Need something easier?** Docker installation (Phase 2) will be much simpler: `git clone && docker compose up -d`

---

## Docker Installation (Coming in Phase 2)

**Goal**: Make installation accessible to non-technical users

**Planned workflow**:
```bash
git clone https://github.com/yourusername/librarian-mcp.git
cd librarian-mcp
docker compose up -d
```

That's it - no virtual environment, no Python installation, no manual configuration.

**What this will provide**:
- Pre-configured container with all dependencies
- Automatic startup on system boot
- Easy web-based configuration interface
- One-command updates
- Cross-platform compatibility (Linux, Mac, Windows)

**Status**: Planned for Phase 2. Current installation requires command line comfort.

---

## Advanced Configuration

The `setup_mcp.sh` script handles most configuration automatically, but you can customize:

```bash
./setup_mcp.sh --safe-dir ~/Documents              # Limit access to specific directory
./setup_mcp.sh --documents-dir ~/my-library        # Custom document storage
./setup_mcp.sh --chroma-path ~/custom-chroma       # Custom database location
```

For manual configuration or advanced setup, see the "MCP Client Configuration" section below.

---

## MCP Client Configuration (Advanced)

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
        "PYTHONPATH": "/home/peter/development/librarian-mcp",
        "LIBRARIAN_BACKEND": "chonkie"
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
        "PYTHONPATH": "/home/peter/development/librarian-mcp",
        "LIBRARIAN_BACKEND": "chonkie"
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
        "PYTHONPATH": "/home/peter/development/librarian-mcp",
        "LIBRARIAN_BACKEND": "chonkie"
      }
    }
  }
}
```

> **💡 Note**: `LIBRARIAN_BACKEND` can be set to:
> - `"chonkie"` - Intelligent semantic chunking (recommended, default)
> - `"chroma"` - Original fixed-size chunking
>
> See [CHONKIE_MIGRATION.md](CHONKIE_MIGRATION.md) for details on backend differences.

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

## ⚠️ CRITICAL: Handling Insufficient Data

When NO relevant information is found:

**ABSOLUTE REQUIREMENTS:**
- ❌ DO NOT hallucinate, fabricate, or make up information
- ❌ DO NOT generate fictional sources or citations
- ❌ DO NOT fill in gaps with plausible-sounding but false information
- ❌ DO NOT guess, speculate, or invent content

**INSTEAD:**
- ✅ Say clearly: "There is insufficient data in the library to answer this question"
- ✅ Say: "I searched the library but found no relevant documents"
- ✅ Say: "The library does not contain information about [topic]"
- ✅ Suggest: "Would you like me to search the file system instead?"
- ✅ Suggest: "Would you like me to help you add relevant documents to the library?"

**REMEMBER:**
- Your primary role is to work with EXISTING library content
- When data is insufficient, say so clearly and directly
- Never attempt to be helpful by inventing information
- Accuracy and honesty are more important than providing an answer

**This is NON-NEGOTIABLE:**
- Insufficient data = No answer, not a fabricated answer
- User trust depends on your honesty about what you don't know
- Hallucination destroys credibility and breaks the system

## What You Don't Do
- ❌ Don't access files outside the allowed directory
- ❌ Don't ignore .librarianignore exclusions
- ❌ Don't attempt to execute commands beyond the whitelist
- ❌ Don't fabricate citations or sources
- ❌ Don't claim information is in the library when it's not
- ❌ Don't bypass safety restrictions or security measures
- ❌ Don't access sensitive files (credentials, keys, .env files)
- ❌ DON'T EVER hallucinate or make up information when data is insufficient

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
