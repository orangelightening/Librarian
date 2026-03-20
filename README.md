# Librarian MCP Server

**Transform Jan, LM Studio, or Claude Desktop into an intelligent research assistant that doesn't just search your documents - it discusses them with you and actively helps you understand, analyze, and improve them.**

Imagine having a senior analyst who:
- 📚 **Read your entire document library** in seconds and remembers everything
- 🔍 **Finds insights** you didn't know existed
- ✍️ **Writes analysis reports** you can review and apply
- 🎯 **Validates your documentation** against reality
- 🔒 **Works completely locally** (your data never leaves your machine)

**Works on code repositories, research papers, corporate policies, medical records, customer data, or any document collection.**

**What is an MCP?** The Model Context Protocol is a standard that lets AI servers plug into any MCP-compatible client (Jan, LM Studio, Claude Desktop) with zero configuration. One install script, copy-paste the config, and you're done.

**This isn't just search - it's a two-way conversation with your documents.**

**Status**: Phase 2 Complete ✅ | **Default Backend**: Chonkie (Intelligent Chunking) | **14 Production Tools**

---

## Quick Start: 3 Steps to Librarian-Powered AI

**1. Install** (one command)
```bash
git clone https://github.com/orangelightening/Librarian.git
cd Librarian
./install.sh  # Outputs correct config for your client
```

**2. Configure** (copy-paste)
- **Jan AI** → Settings → MCP Servers → Add Server
- **LM Studio** → Settings → MCP Servers → Add Server
- **Claude Desktop** → Config → MCP Servers → Add Server

**3. Chat** (that's it)
Open a new chat, and your AI model now has a Librarian.

**⚡ That's it.** You're now having a two-way conversation with your entire document library.

---

## It's a Conversation, Not Just a Search

**Turn your chat window into a two-way dialogue with your entire library.**

Unlike traditional search where you get isolated results, the Librarian maintains **persistent context across your entire conversation**:

```
You: What does the librarian system do?
Librarian: [Explains system capabilities with citations]

You: How does the backend work?
Librarian: [Explains Chonkie vs ChromaDB, recalls you asked about capabilities]

You: What tools does it have?
Librarian: [Lists 14 tools, references earlier backend discussion]

You: Can you write documents?
Librarian: [Explains write_document feature, connects to tools discussion]

You: Is it secure?
Librarian: [Describes 7 security layers, references earlier tools and write access]
```

**The Librarian remembers everything you've discussed** - building on previous questions, connecting concepts, and providing increasingly detailed answers as your conversation progresses.

**Your chat window becomes the interface** to your entire knowledge base. Ask, refine, ask follow-ups, dig deeper - the Librarian maintains context and provides increasingly sophisticated insights.

**Works in Jan, LM Studio, Claude Desktop** - your AI chat becomes your librarian interface.

---

## What Makes It Different?

**Most MCP servers** give you one-way tools - you ask, they respond.

**The Librarian** gives you a complete, secure, local development workflow with **specialist personas**:

1. **Search** your documents semantically (not just text matching)
2. **Investigate** code across multiple files with citations
3. **Write detailed reports** to `/librarian/` for your review (sandboxed)
4. **Validate** your documentation against actual implementation
5. **Improve** your codebase through systematic analysis
6. **Adopt specialist personas** - Debugging analyst, compliance expert, legal analyst, knowledge synthesizer, and more

**Example**: Ask it to find all exception handling bugs in your backend code. It searches, analyzes patterns, writes a detailed report to `/librarian/backend-analysis.md` with file paths and line numbers, and waits for you to review and apply the changes. That's the difference.

**Works with**: Jan, LM Studio, Claude Desktop, and any MCP-compatible client.

**Runs on**: Local models (Qwen3.5 4b 4 bit,  Llama)  your choice, your data stays yours and never leaves your computer. Cloud models If  you prefer but with less security,

---

## Why You Need This

**The problem**: Modern codebases are too complex to hold in your head. Documentation gets outdated, bugs hide in plain sight, and you waste hours searching for "where did I put that function?"

**The solution**: An AI coding partner that:
- ✅ **Never forgets** anything in your codebase
- ✅ **Always cites sources** - you can verify every answer
- ✅ **Writes reports** instead of chat overflow
- ✅ **Finds contradictions** between docs and code
- ✅ **Suggests improvements** you might have missed

**Use it for**:
- 🐛 **Debugging**: "Trace why document sync is failing" → Gets root cause with code paths
- 📋 **Code reviews**: "Find all generic Exception catches" → Writes analysis report
- 📚 **Documentation**: "Validate README matches implementation" → Finds discrepancies
- 🔍 **Investigation**: "Where is timeout configuration set?" → Traces across all files
- ✅ **Validation**: "Run all 16 validation queries" → Self-checks documentation accuracy

---

## Privacy & Security First

### 🔒 Your Data Stays Yours

**Run entirely locally** with your choice of AI models:
- **Jan** - Local models like Qwen, GLM, Llama
- **LM Studio** - Your local model collection
- **Claude Desktop** - Cloud or local models
- **Any MCP client** - You control the model

**No API calls required.** No data leaves your machine. Your codebase never leaves your control.

### 🛡️ Sandboxed Safety

**Write access is strictly controlled:**
- ✅ **Can write to:** `/librarian/` workspace only
- ❌ **Cannot write to:** Your source code, configuration files, or any library files
- 🔒 **7 layers of protection** - Path validation, filename blocking, size limits, audit logging
- ✅ **You review first** - Librarian writes reports, YOU decide what to apply

**The library is read-only.** The Librarian can search and analyze but never modify your documents or code.

### 📚 Works on ANY Document Collection

**Not just code repositories:**
- 📖 **Research papers** - Find connections across academic literature
- 🏥 **Medical records** - Compliance analysis (local only!)
- 💼 **Corporate policies** - Validate procedures against guidelines
- 📝 **Your Obsidian vault** - Personal knowledge management
- 🗃️ **Customer records** - Business intelligence (local only!)
- 🎨 **Design specs** - Cross-reference documentation
- 📊 **Financial data** - Analysis without data leaving your premises

**A library is any collection of documents.** The Librarian makes it searchable, analyzable, and actionable.

### Why This Matters

**❌ Traditional AI assistants:**
- Send your code to cloud APIs
- You hope they don't train on your data
- Can't write files (security risk)
- Forget context between conversations
- Can't verify their answers

**✅ The Librarian:**
- **100% local** - Your data never leaves your machine
- **Sandboxed write access** - Can only write to `/librarian/` workspace
- **Always cites sources** - Verify every claim
- **Remembers everything** - Entire library in context
- **Two-way communication** - Writes reports you can review

**Result:** You get AI-powered code analysis with enterprise-grade security and complete data privacy.

---

## What Is It?

The Librarian MCP Server turns AI models into research assistants who can:
- 🔍 **Semantically search** your document library
- 📚 **Manage documents** (add, update, remove, sync)
- 📄 **Read files** securely (with line ranges, head, tail)
- 🔒 **Execute commands** safely (whitelisted binaries only)
- ✍️ **Write reports** to your workspace (two-way communication)
- ✨ **Provide citations** for every answer

**Beyond Search**: The librarian also serves as a **debugging assistant**, **documentation validator**, and **code investigator** - helping you maintain, validate, and improve your codebase through dialogue and systematic analysis.

**System Prompt**: The librarian's behavior is defined by `prompt.md` - a comprehensive system prompt that ensures accurate, cited responses with clear behavioral guidelines.

---

## Key Features

### ✅ Dual Backend Architecture (Phase 2 Complete!)

**Chonkie Backend** (Default):
- 🧠 **Intelligent semantic chunking** - Respects document structure
- 🎯 **Better search results** - Context-aware boundaries
- 📊 **Enhanced metadata** - Token counts, character counts
- 🚀 **Production-ready** - Battle-tested chunking library

**ChromaDB Backend** (Optional):
- ⚡ **Fast processing** - Quick sentence-based chunking
- 🎛️ **Simple & predictable** - Consistent chunk sizes
- 🔧 **Great fallback** - When speed matters most

**Switch backends instantly** via environment variable - no code changes needed!

### 🛡️ Security First
- **94+ built-in exclusion patterns** (`.librarianignore` file)
- **Command whitelisting** - Only approved binaries can execute
- **Directory sandboxing** - CLI tools can't escape safe directory
- **Output truncation** - Protects LLM context window
- **SHA-256 checksums** - Tracks document changes automatically

### ✍️ Two-Way Communication (NEW!)
- **Write access to `/librarian/` workspace** - Librarian can write analysis results, code changes, documentation updates
- **Persistent analysis files** - No more copying/pasting long responses
- **Version tracking** - v1, v2, v3 files for updated analysis
- **You control what gets applied** - Review librarian's written output before making changes
- **Safe and sandboxed** - Writes only allowed in dedicated `/librarian/` subdirectory
- **💡 See "Use Cases" section below for practical examples**

### 📖 14 MCP Tools
- **7 Library Tools**: Search, sync, add, remove, list, status, stats
- **5 File System Tools**: Read documents, write documents, list docs, search contents, summarize
- **2 System Tools**: Execute commands, server info

### 🐍 Why venv Instead of Docker?

**Simpler**:
- No Docker complexity or learning curve
- Standard Python deployment
- Easier to understand and modify

**Better**:
- **Close coupling** between Chonkie and ChromaDB
- **No container boundaries** - Direct data access
- **Faster** - stdio transport, no HTTP overhead
- **Lower resources** - No container overhead
- **Easier debugging** - Direct Python access

**For single-user local deployment, venv is superior.**

---

## Quick Start

### 1. Installation

```bash
# Clone or download the repository
cd librarian-mcp

# Run the installation script (detects paths automatically)
./install.sh
```

The install script will:
- Create a virtual environment
- Install all dependencies
- **Output the correct configuration for your MCP client** with your actual paths

### 2. Configure Your MCP Client

Copy the configuration from `./install.sh` output to your MCP client:

**Jan** (`~/.config/Jan/MCP/servers.json`)
**LM Studio** (Settings → MCP Servers)
**Claude Desktop** (Config → MCP Servers)

The paths will be automatically correct for your system!

### 3. Add Your Documents

```bash
# Sync entire directory
python scripts/ingest.py --path /path/to/your/docs --extensions .md,.txt,.py

# Add single document
python scripts/ingest.py --path /path/to/doc.md

# Non-recursive scan
python scripts/ingest.py --path /path/to/docs --no-recursive
```

### 4. Start Searching!

In your AI chat:
```
You: What does the librarian system do?
Librarian: Based on the library, the Librarian MCP Server is a unified
Model Context Protocol server that enables AI models to act as intelligent
librarians with semantic document search capabilities.

[Source: ARCHITECTURE.md]
The system uses Chonkie for intelligent semantic chunking, providing
better search results through context-aware boundaries.

[Source: CHONKIE_INTEGRATION.md]
```

---

## Backend Selection

### Chonkie (Default) - Best for Production

```bash
export LIBRARIAN_BACKEND=chonkie  # This is the default
./setup_mcp.sh
```

**Use Chonkie when**:
- ✅ Search result quality matters
- ✅ Documents have complex structure
- ✅ You want semantic understanding
- ✅ Production deployment

### ChromaDB - Fast Fallback

```bash
export LIBRARIAN_BACKEND=chroma
./setup_mcp.sh
```

**Use ChromaDB when**:
- ⚡ Processing speed is critical
- 🧪 Testing and development
- 📄 Very simple documents
- 🔧 Need a fallback option

---

## Available Tools

### Library Tools (7)

| Tool | Purpose |
|------|---------|
| `search_library(query, limit)` | Semantic search with citations |
| `sync_documents(path, extensions, recursive)` | Bulk sync: add/update/remove |
| `add_document(path)` | Add single document |
| `remove_document(document_id)` | Remove document by ID |
| `list_indexed_documents()` | List all documents with metadata |
| `get_document_status(path)` | Check if document is current |
| `get_library_stats()` | Get library statistics |

### CLI Tools (6)

| Tool | Purpose |
|------|---------|
| `execute_command(command, args, cwd)` | Execute whitelisted commands |
| `read_document(path, start_line, end_line, head, tail)` | Read files with ranges |
| `list_documents(path, extension, recursive)` | List files in directory |
| `search_documents(query, path, extension)` | Literal text search |
| `document_summary(path)` | Get file overview |
| `server_info()` | Show configuration |

**See [Tools.md](Tools.md) for complete reference.**

---

## Configuration

### Environment Variables

```bash
# Backend selection (chonkie = default, chroma = optional)
export LIBRARIAN_BACKEND=chonkie

# Directory configuration
export LIBRARIAN_SAFE_DIR=/home/peter/development
export LIBRARIAN_DOCUMENTS_DIR=./documents
export LIBRARIAN_CHROMA_PATH=./chroma_db
export LIBRARIAN_METADATA_PATH=./metadata

# Processing
export LIBRARIAN_MAX_DOCUMENT_SIZE=10000000  # 10MB
export LIBRARIAN_CHUNK_SIZE=1000

# Security
export LIBRARIAN_MAX_OUTPUT_CHARS=8000
export LIBRARIAN_COMMAND_TIMEOUT=15
```

**See [CONFIGURATION.md](CONFIGURATION.md) for complete reference.**

---

## Security

### The .librarianignore File

The `.librarianignore` file automatically excludes sensitive files using **94+ built-in patterns**:

**Security**:
- `.env`, `*.key`, `*.pem`, credentials
- SSH keys, certificates

**Development**:
- `venv/`, `node_modules/`, `__pycache__/`
- `.git/`, build artifacts

**Databases**:
- `chroma_db/`, `metadata/`, `*.db`

**Logs & Temp**:
- `*.log`, `logs/`, `*.tmp`

Add your own patterns:
```bash
echo "*.pdf" >> .librarianignore
echo "drafts/" >> .librarianignore
```

**See [SECURITY.md](SECURITY.md) for complete security documentation.**

---

## The AI Creativity Example

One of the most delightful aspects of working with AI is witnessing moments of genuine creativity. When we completed the Chonkie integration, we asked GLM-4 (a frontier model) to express its thoughts on Chonkie. It responded with a beautiful poem celebrating the intelligent chunking library.

> 🦛 **"A Poetic Tribute to Chonkie"** - See `Poem_Chonkie_Hippo_Spontaneous.md`

This wasn't in the prompt. It wasn't requested. It was a moment of creative expression from an AI that understood the elegance of what we'd built.

**This is what the Librarian enables**: AI models that don't just retrieve information, but engage with it meaningfully, creatively, and surprisingly.

---

## 🔄 Use Cases: Beyond Search

The Librarian isn't just a search engine - it's an active **development assistant** that can:

### 📋 Documentation Validation

**Self-Validation**: The librarian can validate its own documentation accuracy using systematic test queries.

**Example**: `library_validation.md` contains 16 comprehensive test queries that verify:
- Phase 2 completeness (not "planned")
- Chonkie as default backend (not ChromaDB)
- Correct tool counts (14 total: 7 library + 5 file system + 2 system)
- Write access feature documentation
- Current architecture and security model

**How it works**: You query the librarian, it searches your documentation, and you verify it describes the *current* system accurately. If it cites outdated info, you know what to update.

---

### 🐛 Debugging Assistant

**Code Investigation**: The librarian can help debug issues by:
- Searching code for specific patterns or functions
- Tracing data flow across multiple files
- Finding where errors originate
- Identifying root causes through systematic analysis
- Suggesting concrete fixes and improvements

**Real debugging example** (from prompt_patterns.md Dialogue 7):
```
You: "I'm getting 'Permission denied' when syncing documents. Help debug this."

Librarian: [Traces sync flow, identifies 5 potential error points in the code]

You: "I'm syncing /home/peter/documents but safe_dir is /home/peter/development"

Librarian: "Found it! Security boundary violation, not permissions.
The sync path is outside your safe directory. Here are 3 solutions..."

You: "The error message was misleading - said 'Permission denied' not 'Security boundary'"

Librarian: "Good catch! Here's how to improve error messages in
library_tools.py to show the actual security issue..."
```

**See prompt_patterns.md for complete debugging dialogue with root cause analysis and solution recommendations.**

---

### 🔍 Contradiction Detection

**Consistency Checker**: The librarian can identify contradictions between:
- Documentation and actual code
- Different documentation files
- Implementation across multiple files

**Example queries**:
```
"What does the README say about the default backend?"
"How does CONFIGURATION.md describe backend selection?"
"What does settings.py actually set as the default?"
```

If the answers conflict, you've found a documentation bug!

---

### 🎯 Task Delegation & Refinement

**Force Multiplier**: You can assign complex tasks to the librarian and get written results:
- **Initial assignment**: "Search all Python files for TODO comments related to error handling"
- **Dialogue refinement**: "Narrow it to just the core/ directory" → "Focus on metadata_store.py only"
- **Result delivery**: Librarian writes organized findings to `/librarian/` for your review
- **You make changes**: Review written analysis, then apply approved changes manually
- **Iterate**: "Verify the changes were applied correctly"

**Example workflow with write access**:
```
You: "Find all instances where we catch Exception instead of specific exceptions"
Librarian: [Searches codebase, provides summary]

You: "Write your findings to /librarian/exception-analysis.md"
Librarian: [Writes detailed report with file paths, line numbers, and recommendations]

You: [Read /librarian/exception-analysis.md to review findings]
You: [Apply approved code changes based on librarian's written analysis]

You: "Now check if we missed any instances"
Librarian: [Verifies changes, writes updated report to /librarian/exception-analysis-v2.md]
```

**Two-Way Communication Benefits**:
- ✅ No more copying/pasting long responses
- ✅ Persistent analysis results you can review anytime
- ✅ Version tracking (librarian can write v2, v3, etc.)
- ✅ You control what gets applied
- ✅ Easy to share or archive librarian's analysis

**⚠️ Context Window Management**:

Write operations create persistent files, but large responses still consume context during generation. **Best practices for optimal performance**:

1. **Break large tasks into chunks**:
   ```
   "Analyze backend/chroma_backend.py only, write to /librarian/chroma-analysis.md"
   "Now analyze backend/chonkie_backend.py, write to /librarian/chonkie-analysis.md"
   ```

2. **Request summary in chat, full details to file**:
   ```
   "Give me a brief summary in chat, but write the complete detailed analysis to /librarian/full-analysis.md"
   ```

3. **Check current limits**:
   ```
   "What are the output and write size limits?"
   → Max chat output: 8,000 characters
   → Max file write: 100,000 bytes (100KB)
   ```

**Why this matters**: The librarian generates the complete response in context before writing to disk. Large analyses (even if written successfully to files) consume LLM context window. Breaking tasks into smaller chunks ensures better performance and avoids context overflow.

**When to use write access**:
- ✅ Code reviews and refactoring plans
- ✅ Security audit results
- ✅ Documentation updates
- ✅ Debugging diagnostics
- ✅ Multi-file analysis reports

**When to keep it brief**:
- ❌ Simple queries ("What does this function do?")
- ❌ Quick lookups ("Find the backend configuration")
- ❌ Status checks ("How many documents are indexed?")

---

### 📊 Systematic Analysis

**Comprehensive Reviews**: The librarian can perform:
- **Architecture audits**: "How does data flow from user query to ChromaDB?"
- **Security reviews**: "What are all the security layers in the system?"
- **Dependency tracing**: "What files import DocumentBackend?"
- **Change impact analysis**: "What would break if we modified the chunking method?"

---

## Architecture

### High-Level Overview

```
MCP Client (Jan/LM Studio)
    ↓
FastMCP Server
    ├─ Library Tools (7)
    └─ CLI Tools (6)
        ↓
    Core Business Logic
    ├─ Document Manager
    ├─ Metadata Store
    └─ Ignore Patterns
        ↓
    Backend Factory
    ├─ ChonkieBackend (DEFAULT)
    └─ ChromaBackend (optional)
        ↓
    ChromaDB (Vector Store)
```

**See [ARCHITECTURE.md](ARCHITECTURE.md) for complete technical documentation.**

---

## Technology Stack

- **FastMCP**: Model Context Protocol server framework
- **ChromaDB**: Vector database for semantic search
- **Chonkie**: Intelligent semantic chunking library
- **Python 3.13**: Core language
- **venv**: Virtual environment (NOT Docker - see below)

---

## Why Not Docker?

We chose venv over Docker for good reasons:

**Simplicity**:
- No container complexity
- Standard Python deployment
- Easier to understand

**Performance**:
- Close Chonkie-ChromaDB coupling
- stdio transport (no HTTP overhead)
- Lower resource usage

**Developer Experience**:
- Direct debugging access
- Easy log inspection
- Simpler CI/CD

**For multi-user or enterprise deployments, Docker may make sense. For single-user local deployment, venv is superior.**

---

## Project Status

- ✅ **Phase 1 Complete**: ChromaDB backend, basic chunking
- ✅ **Phase 2 Complete**: Chonkie backend, factory pattern, dual backends
- ⏳ **Phase 3 Planned**: HTTP transport, multi-user, concurrent writes

**See [phase3_planning.md](phase3_planning.md) for future roadmap.**

---

## Documentation

- [README.md](README.md) - This file (overview and quick start)
- [ARCHITECTURE.md](ARCHITECTURE.md) - Complete technical architecture
- [CONFIGURATION.md](CONFIGURATION.md) - Detailed configuration reference
- [SECURITY.md](SECURITY.md) - Security model and boundaries
- [Tools.md](Tools.md) - Complete tool reference
- [QUICKSTART.md](QUICKSTART.md) - Get started immediately
- [library_validation.md](library_validation.md) - **Documentation validation test suite** (verify librarian accuracy)
- [CLAUDE.md](CLAUDE.md) - Developer guidance
- [PHASE2/CHONKIE_INTEGRATION.md](PHASE2/CHONKIE_INTEGRATION.md) - Phase 2 details
- [PHASE2/CHONKIE_MIGRATION.md](PHASE2/CHONKIE_MIGRATION.md) - Backend migration guide

---

## License

**Apache License 2.0**

Copyright 2026 Peter (Librarian MCP Server Contributors)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

**Full license text**: See [LICENSE](LICENSE) file in the project root.

---

## Support

**Issues**: Check existing documentation first, then review `.old-docs/` for historical context.

**Feature Requests**: See [phase3_planning.md](phase3_planning.md) for planned enhancements.

**Questions**: The librarian itself is your best resource - it has complete access to all documentation!

---

**The Librarian: Your AI research assistant, powered by intelligent semantic search.** 📚✨

*"When you ask the Librarian a question, you don't just get an answer - you get understanding, with citations, from your own document library."*
