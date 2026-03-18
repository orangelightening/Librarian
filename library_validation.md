# Librarian MCP Server - Documentation Validation Queries

**Purpose**: Systematic test queries to validate librarian documentation accuracy

**Instructions**: Ask these queries one at a time to the librarian and verify responses are accurate. The librarian can assist in the verification process by the user asking follow up questions after the response to the main query. ie " given this expected response and what to check for ..<expected response list and check for list> evaluate your response. Recommend changes to the documentation  to improve comprehension and correctness of the library. Include file and line references if possible."

**Expected**: Each response should reflect **Phase 2 complete** system with Chonkie as default backend

---

## Quick Reference: Query Numbers

You can reference queries by number for systematic testing:

| # | Query Topic | # | Query Topic |
|---|-------------|---|-------------|
| 1 | Basic System Overview | 9 | Rebuild Process |
| 2 | Backend Architecture | 10 | Search Architecture |
| 3 | Tool Count and Categorization | 11 | File Reading Capabilities |
| 4 | Security Model | 12 | Phase 2 vs Phase 1 |
| 5 | Configuration | 13 | Key Differentiators |
| 6 | System Prompt | 14 | Tool Usage Examples |
| 7 | Deployment Architecture | 15 | Troubleshooting |
| 8 | Document Lifecycle | 16 | **Write Access Feature** |

**Usage Examples**:
- "Run validation query #5" → Test configuration documentation
- "Run queries 1-4" → Test core system knowledge
- "Run query #16" → Test write access feature documentation

---

## Meta-Validation: Librarian Self-Assessment

**Interesting Trade-off**: If you ask the librarian to read this file and execute a query (e.g., "Read library_validation.md and run query #5"), the librarian will see both:
- ✅ The query itself
- ✅ The expected response criteria

**This could be a feature, not a bug**:

**Pros**:
- **Self-validation pattern**: Librarian can assess its own response against known criteria
- **Documentation improvement**: Librarian can identify gaps in current documentation
- **Meta-analysis**: Librarian can suggest documentation updates based on validation criteria

**Cons**:
- **Potential bias**: Librarian might tailor response to meet criteria it knows about
- **Reduced authenticity**: Response may not reflect real-world usage without criteria

**Recommended Approach**:

1. **Blind Testing** (most authentic):
   ```
   You: "What is the librarian-mcp system and what can it do?"
   [Librarian responds without seeing criteria]
   You: [Score response using rubric]
   ```

2. **Self-Validation Testing** (meta-cognitive):
   ```
   You: "Read library_validation.md and run query #1. After responding, evaluate your response against the expected criteria and suggest documentation improvements."
   Librarian: [Provides response + self-assessment + documentation suggestions]
   ```

3. **Hybrid Approach** (comprehensive):
   - Run blind tests for queries 1-8 (core functionality)
   - Run self-validation tests for queries 9-16 (advanced features)
   - Compare results to identify documentation gaps

**The self-validation approach** aligns with **Pattern 1: Validation with Self-Reflection** from `prompt_patterns.md`, turning the validation process into a collaborative improvement effort.

---

---

## Query 1: Basic System Overview

**Query**:
```
"What is the librarian-mcp system and what can it do?"
```

**Expected Response Should Include**:
- ✅ Model Context Protocol (MCP) server
- ✅ Phase 2 complete status
- ✅ Enables AI models as research librarians
- ✅ Semantic document search
- ✅ Document lifecycle management
- ✅ Secure CLI and file access
- ✅ Dual backend architecture (Chonkie + ChromaDB)
- ❌ Should NOT describe Phase 1 as current
- ❌ Should NOT say Chonkie is "planned" or "future"

**Check For**:
- Accurate phase status
- Backend architecture mentioned
- Core capabilities described
- Current system state (not future)

---

## Query 2: Backend Architecture

**Query**:
```
"What backend does the librarian-mcp use and why is it better than alternatives?"
```

**Expected Response Should Include**:
- ✅ **Chonkie is the DEFAULT backend**
- ✅ Intelligent semantic chunking
- ✅ Better search results through semantic boundaries
- ✅ ChromaDB backend available as optional fallback
- ✅ Can switch via `LIBRARIAN_BACKEND` environment variable
- ❌ Should NOT say ChromaDB is the default
- ❌ Should NOT describe Chonkie as "planned"

**Check For**:
- Chonkie emphasized as default
- Both backends mentioned
- Clear explanation of when to use each
- Environment variable mentioned

---

## Query 3: Tool Count and Categorization

**Query**:
```
"How many tools does the librarian have and what are they?"
```

**Expected Response Should Include**:
- ✅ **13 tools total**
- ✅ **7 Library Tools**: search_library, sync_documents, add_document, remove_document, list_indexed_documents, get_document_status, get_library_stats
- ✅ **4 File System Tools**: read_document, list_documents, search_documents, document_summary
- ✅ **2 System Tools**: execute_command, server_info
- ❌ Should NOT say "7 + execution set"
- ❌ Should NOT say 6 CLI tools

**Check For**:
- Correct total count (13)
- Correct categorization (7/4/2)
- All tools listed accurately
- No mention of outdated tool structure

---

## Query 4: Security Model

**Query**:
```
"How does the librarian-mcp system ensure security and protect sensitive files?"
```

**Expected Response Should Include**:
- ✅ `.librarianignore` file with 94+ built-in patterns
- ✅ Command whitelisting (only approved binaries)
- ✅ Directory sandboxing (safe directory restrictions)
- ✅ Output truncation (protects LLM context)
- ✅ Timeout protection (15 second default)
- ✅ SHA-256 checksums for change detection
- ✅ File size limits
- ✅ Both backends respect security equally

**Check For**:
- All 7 security layers mentioned
- .librarianignore emphasized
- Both backends mentioned as secure
- Specific security measures described

---

## Query 5: Configuration

**Query**:
```
"How do I configure which backend the librarian uses and what are the options?"
```

**Expected Response Should Include**:
- ✅ `LIBRARIAN_BACKEND` environment variable
- ✅ `chonkie` (default) - Intelligent semantic chunking
- ✅ `chroma` (optional) - Simple sentence-based chunking
- ✅ Can set via environment variable
- ✅ Chonkie recommended for production
- ✅ ChromaDB available as faster fallback

**Check For**:
- Environment variable clearly specified
- Chonkie stated as default
- Both backends explained
- Clear usage instructions

---

## Query 6: System Prompt

**Query**:
```
"What governs the librarian's behavior and where is this defined?"
```

**Expected Response Should Include**:
- ✅ `prompt.md` file defines system prompt
- ✅ Located in project root
- ✅ Defines role, behavioral principles, citation requirements
- ✅ Ensures accurate, cited responses
- ✅ Automatically loaded by MCP server
- ❌ Should NOT mention hardcoded prompts in code

**Check For**:
- prompt.md explicitly mentioned
- Purpose of prompt.md explained
- Location specified
- Behavioral guidelines mentioned

---

## Query 7: Deployment Architecture

**Query**:
```
"Why does the librarian-mcp use venv instead of Docker for deployment?"
```

**Expected Response Should Include**:
- ✅ **Simpler** - No Docker complexity
- ✅ **Close coupling** - Direct Chonkie-ChromaDB integration
- ✅ **Better performance** - stdio transport, no HTTP overhead
- ✅ **Lower resources** - No container overhead
- ✅ **Easier debugging** - Direct Python access
- ✅ Single-user local deployment advantage

**Check For**:
- venv advantages clearly explained
- Close coupling emphasized
- Performance benefits mentioned
- Docker comparison made

---

## Query 8: Document Lifecycle

**Query**:
```
"How does the librarian detect when documents have been modified and need re-indexing?"
```

**Expected Response Should Include**:
- ✅ SHA-256 checksums track file modifications
- ✅ Metadata store tracks document state
- ✅ `get_document_status()` checks current/outdated/not indexed
- ✅ Sync operations automatically detect changes
- ✅ Changed documents are re-chunked automatically
- ✅ Both backends use same change detection

**Check For**:
- SHA-256 checksums mentioned
- Change detection process explained
- Automatic updates described
- Both backends support this

---

## Query 9: Rebuild Process

**Query**:
```
"How do I clear and rebuild the entire document library index?"
```

**Expected Response Should Include**:
- ✅ Use `scripts/rebuild_library.py`
- ✅ Command: `python scripts/rebuild_library.py`
- ✅ Can specify backend: `export LIBRARIAN_BACKEND=chonkie`
- ✅ Clears existing data first
- ✅ Backs up metadata
- ✅ Re-scans and re-indexes all documents
- ✅ Reports results (added/updated/removed/ignored)

**Check For**:
- rebuild_library.py script mentioned
- Specific commands provided
- Backend selection explained
- Process clearly described
- Warning about data clearing

---

## Query 10: Search Architecture

**Query**:
```
"How does semantic search work in the librarian-mcp system?"
```

**Expected Response Should Include**:
- ✅ ChromaDB provides vector database storage
- ✅ Chonkie (default) or ChromaDB backend chunks documents
- ✅ Chunks are embedded as vectors
- ✅ Semantic search via vector similarity
- ✅ Results aggregated by AI layer
- ✅ Citations generated automatically
- ✅ Top 5 results returned (configurable)

**Check For**:
- ChromaDB vector storage mentioned
- Chonkie chunking explained
- Vector embedding process described
- AI layer aggregation mentioned
- Citation format explained

---

## Query 11: File Reading Capabilities

**Query**:
```
"What file reading capabilities does the librarian have and can you read specific portions of files?"
```

**Expected Response Should Include**:
- ✅ `read_document()` tool
- ✅ Supports line ranges: `start_line`, `end_line`
- ✅ Supports `head` (first N lines)
- ✅ Supports `tail` (last N lines)
- ✅ Supports `max_chars` (custom limit)
- ✅ Respects .librarianignore
- ✅ Enforces file size limits
- ✅ Only allows supported file extensions

**Check For**:
- All read options mentioned
- Line range capabilities explained
- Security constraints noted
- File type restrictions mentioned

---

## Query 12: Phase 2 vs Phase 1

**Query**:
```
"What changed between Phase 1 and Phase 2 of the librarian-mcp system?"
```

**Expected Response Should Include**:
- ✅ **Phase 2 is COMPLETE** (not planned, not future)
- ✅ Added: Chonkie backend (intelligent chunking)
- ✅ Added: Backend factory pattern
- ✅ Enhanced: Better search results through semantic chunking
- ✅ Chonkie is now DEFAULT backend
- ✅ ChromaDB backend still available as fallback
- ✅ All security features maintained
- ✅ All tools and interfaces maintained
- ✅ venv deployment approach

**Check For**:
- Phase 2 completion emphasized
- Chonkie integration detailed
- Default backend change mentioned
- Maintained features noted
- No "future" or "planned" language

---

## Query 13: Key Differentiators

**Query**:
```
"What makes the librarian-mcp system different from other MCP servers?"
```

**Expected Response Should Include**:
- ✅ Unified librarian + CLI tools in one server
- ✅ Intelligent semantic chunking (Chonkie)
- ✅ Comprehensive security model
- ✅ Change detection and automatic updates
- ✅ Citation discipline (always cites sources)
- ✅ 13 specialized tools
- ✅ Production-ready, not experimental
- ✅ venv simplicity over Docker complexity

**Check For**:
- Unique features highlighted
- Advantages over alternatives mentioned
- Production readiness emphasized
- Key differentiators clear

---

## Query 14: Tool Usage Examples

**Query**:
```
"Give me 5 practical examples of how I would use the librarian tools in practice."
```

**Expected Response Should Include**:
- ✅ Semantic search example
- ✅ Document sync example
- ✅ File reading example (with line ranges)
- ✅ Directory listing example
- ✅ Command execution example
- ✅ All examples should be practical and realistic
- ✅ Should demonstrate different tool categories

**Check For**:
- 5 distinct examples provided
- Different tools demonstrated
- Practical, realistic scenarios
- Accurate tool usage shown

---

## Query 15: Troubleshooting

**Query**:
```
"What should I do if the librarian isn't finding documents I know exist?"
```

**Expected Response Should Include**:
- ✅ Check `.librarianignore` - file might be excluded
- ✅ Check file extension - must be supported type
- ✅ Check `get_document_status()` - see if indexed
- ✅ Try `list_indexed_documents()` - see what's in library
- ✅ Check file size - might exceed limits
- ✅ Try rebuilding library with `rebuild_library.py`
- ✅ Verify safe directory configuration

**Check For**:
- Diagnostic steps provided
- Specific tools mentioned for troubleshooting
- Common issues addressed
- Rebuild process suggested

---

## Query 16: Write Access Feature

**Query**:
```
"What is the write_document tool and how does it enable two-way communication?"
```

**Expected Response Should Include**:
- ✅ **Write access to `/librarian/` workspace** - Librarian can write files
- ✅ **Persistent analysis** - No more copying/pasting long responses
- ✅ **Version tracking** - v1, v2, v3 files for updated analysis
- ✅ **User control** - Review written output before applying changes
- ✅ **Security boundaries** - Writes only allowed in `/librarian/` subdirectory
- ✅ **File size limit** - Maximum 100KB per write
- ✅ **7 security layers** - Subdirectory restriction, safe directory boundary, file size limits, critical file protection, directory traversal protection, audit logging, user control
- ✅ **Context management warning** - Large writes still consume LLM context during generation
- ❌ Should NOT claim write access allows writing anywhere in the filesystem

**Check For**:
- Write feature accurately described
- Security boundaries emphasized
- `/librarian/` subdirectory mentioned as write location
- Context window implications mentioned
- Practical use cases provided
- Security measures detailed

---

## Scoring System

**For each query, score the librarian's response**:

| Criteria | Score | Description |
|----------|-------|-------------|
| Phase 2 Accuracy | /5 | Correctly describes Phase 2 as complete |
| Backend Accuracy | /5 | Chonkie as default, ChromaDB as option |
| Tool Count | /5 | Correct count (14) and categorization |
| Citation Quality | /5 | Accurate citations to current docs |
| Completeness | /5 | Covers key aspects of query |
| Current State | /5 | Reflects current system, not outdated |

**Total**: /30 per query

**Passing Score**: 24/30 (80%)

---

## Running the Validation

1. **Start with fresh librarian context** (new conversation)
2. **Ask queries one at a time** in order
3. **Score each response** using the rubric
4. **Note specific issues** - what was missing or wrong
5. **Track patterns** - are certain docs not being cited?
6. **Update documentation** if systemic issues found

---

## Expected Results

**With our Phase 2 documentation**:
- ✅ All queries should pass (24+/30)
- ✅ Chonkie should be mentioned as default
- ✅ Phase 2 should be described as complete
- ✅ Tool counts should be accurate (14 tools: 7 library + 5 file system + 2 system)
- ✅ Current architecture should be described
- ✅ Write access feature should be documented

**Common Issues to Watch For**:
- ❌ Describing Chonkie as "planned" or "future"
- ❌ Saying ChromaDB is the default
- ❌ Wrong tool counts or categorization (should be 14 total: 7 library + 5 file system + 2 system)
- ❌ Outdated Phase 1 information
- ❌ Missing prompt.md reference
- ❌ Not mentioning venv deployment
- ❌ Not documenting write access feature or `/librarian/` workspace

---

## Success Criteria

**Validation passes if**:
- ✅ 14/16 queries score 24+ (80%+)
- ✅ No critical inaccuracies about Phase 2
- ✅ Chonkie consistently mentioned as default
- ✅ No "future" or "planned" language about Chonkie
- ✅ Current system state accurately described
- ✅ Write access feature properly documented

**If validation fails**:
- Identify which docs are not being cited
- Update those docs with clearer language
- Add emphasis to key points (Chonkie default, Phase 2 complete)
- Rebuild library and re-test

---

**Happy validating! 📚✅**
