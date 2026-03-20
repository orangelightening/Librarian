# Validation Scripts Sequencing Guide

## Overview

This guide documents the execution order and usage notes for all librarian-mcp validation scripts. The scripts are designed to validate the librarian's ability to answer questions about itself using its own tools (search_library, read_document, write_document).

---

## Prerequisites

Before running any validation scripts, ensure:

1. **Librarian MCP Server is Running**
   - Start via Jan UI MCP client configuration
   - Or use: `./setup_mcp.sh`

2. **Library is Indexed**
   - Core documentation must be indexed: `README.md`, `ARCHITECTURE.md`, `SECURITY.md`, `CONFIGURATION.md`
   - Check status: Use `get_library_stats()` tool
   - Expected: ~54 documents indexed

3. **Model Has Tool Access**
   - Model MUST be able to see and use MCP tools
   - Jan UI: ✅ Tools properly exposed
   - Jan API: ❌ Tools NOT properly exposed (format mismatch)

---

## Execution Strategies

### Strategy A: Large Context Models (GLM-4.7, 200k+ tokens)

**Use Batch Prompts** - Run all queries in one context window sequentially

| Batch | File               | Queries | Context Required |
| ----- | ------------------ | ------- | ---------------- |
| 1     | `batch1_prompt.md` | 1-3     | 200k tokens      |
| 2     | `batch2_prompt.md` | 4-6     | 200k tokens      |
| 3     | `batch3_prompt.md` | 7-9     | 200k tokens      |
| 4     | `batch4_prompt.md` | 10-12   | 200k tokens      |
| 5     | `batch5_prompt.md` | 13-15   | 200k tokens      |
| 6     | `batch6_prompt.md` | 16      | 200k tokens      |

**Usage:**
1. Open Jan UI chat with GLM-4.7
2. Copy contents of `batch1_prompt.md`
3. Paste into chat
4. Wait for "Batch 1 complete" message
5. Continue with `batch2_prompt.md` in same context window
6. Repeat through batch 6

**Advantages:**
- Faster execution (all queries in single session)
- Model can build on previous context
- Less copy-paste overhead

**Caveats:**
- Cross-contamination possible (model may reference earlier queries)
- Not truly atomic validation
- Requires large context window

---

### Strategy B: Small Context Models (4B, ~8k tokens)

**Use Atomic Scripts** - Run each query in isolation

| Query | File | Topic |
|-------|------|-------|
| 1-3 | See batch scripts | System overview, backends, tools |
| 4-6 | See batch scripts | Phase 2, Chonkie, search types |
| 7 | `query_07_deployment.md` | Deployment architecture |
| 8 | `query_08_file_types.md` | Supported file types |
| 9 | `query_09_search_capabilities.md` | Search capabilities |
| 10 | `query_10_semantic_search.md` | Semantic search mechanics |
| 11 | `query_11_reading_files.md` | File reading capabilities |
| 12 | `query_12_phase_changes.md` | Phase 1 vs Phase 2 changes |
| 13 | `query_13_differentiation.md` | Unique differentiators |
| 14 | `query_14_practical_examples.md` | 5 practical use cases |
| 15 | `query_15_troubleshooting.md` | Troubleshooting tips |
| 16 | `query_16_write_access.md` | Write access feature |

**Usage:**
1. Open new chat session (clean context)
2. Copy contents of single query script
3. Paste into chat
4. Wait for completion message
5. **Close chat session**
6. Open new chat session for next query

**Advantages:**
- Truly atomic validation (no cross-contamination)
- Works with small context windows
- More rigorous testing of tool discovery

**Caveats:**
- More tedious (16 separate chat sessions)
- Slower execution
- More copy-paste overhead

---

## File Locations

**All validation scripts are in one directory:**

```
/home/peter/development/librarian-mcp/validation_scripts/
├── sequencing_scripts.md          # This guide document
├── batch1_prompt.md               # Queries 1-3
├── batch2_prompt.md               # Queries 4-6
├── batch3_prompt.md               # Queries 7-9
├── batch4_prompt.md               # Queries 10-12
├── batch5_prompt.md               # Queries 13-15
├── batch6_prompt.md               # Query 16
├── query_07_deployment.md         # Deployment architecture
├── query_08_file_types.md         # Supported file types
├── query_09_search_capabilities.md # Search capabilities
├── query_10_semantic_search.md    # Semantic search mechanics
├── query_11_reading_files.md      # File reading capabilities
├── query_12_phase_changes.md      # Phase 1 vs Phase 2 changes
├── query_13_differentiation.md    # Unique differentiators
├── query_14_practical_examples.md # 5 practical use cases
├── query_15_troubleshooting.md    # Troubleshooting tips
└── query_16_write_access.md       # Write access feature
```

**Note:** Queries 1-6 are only in batch prompts, not as individual atomic scripts.

---

## Expected Output

All validation responses are written to:

```
librarian/reports/self_validation/
├── response_001.md
├── response_002.md
├── response_003.md
├── response_004.md
├── ...
└── response_016.md
```

Each response file contains:
- Model's answer to the query
- Citations to source documents using `[Source: document.md]` format
- Tool usage (search_library, read_document, write_document)

---

## Atomic Design Notes

### What "Atomic" Means

Each validation script is:
- **Self-contained**: Complete instructions in one file
- **No cross-references**: Does not reference other batches or queries
- **Independent**: Can run in isolated chat session
- **Complete**: Includes query text, instructions, expected criteria, completion signal

### Why Atomic Matters

1. **Clean Testing**: Each query tests model's ability to discover information independently
2. **No Context Bias**: Model can't rely on previous queries in same session
3. **Model Agnostic**: Works with any model/context size
4. **Parallel Execution**: Could theoretically run multiple queries in parallel

### Cross-Contamination Warning

When using **Strategy A** (batch prompts in same context window), be aware:
- Model may reference earlier queries: "As mentioned in Query 2..."
- This is acceptable for testing but not for atomic validation
- For rigorous testing, use **Strategy B** (atomic scripts in separate sessions)

---

## Known Issues

### Documentation Note: Tool Count

**Query 3** validation confirmed the librarian-mcp system has **14 tools** (not 13 as originally documented).

**All 14 Tools:**
1. search_library
2. sync_documents
3. add_document
4. remove_document
5. list_indexed_documents
6. get_document_status
7. get_library_stats
8. read_document
9. list_documents
10. search_documents
11. document_summary
12. execute_command
13. write_document
14. server_info

**Note:** The `write_document` tool (Phase 2 feature) was missing from earlier documentation counts. The system correctly identifies all 14 tools via `server_info()` and direct tool inspection.

---

## Interpreting Results

### Success Indicators

✅ **Good Response:**
- Uses `search_library` tool FIRST (not file searching)
- Provides comprehensive answer
- Includes proper citations: `[Source: ARCHITECTURE.md]`
- Answers match expected criteria in script

❌ **Poor Response:**
- Searches files using `list_documents` or `read_document` directly
- No citations or incorrect citations
- Misses key points from expected criteria
- Hallucinates information not in documentation

### Quality Scoring

Rate each response on:
1. **Tool Usage**: Did it use `search_library` first?
2. **Completeness**: Did it cover all expected criteria?
3. **Citations**: Are sources properly cited?
4. **Accuracy**: Is information correct per documentation?

**Scale:**
- 10/10: Perfect - all criteria met, excellent citations
- 8/10: Good - minor gaps or citation issues
- 6/10: Fair - some criteria missing, weak citations
- 4/10: Poor - missed key points, wrong tools used
- 2/10: Failed - didn't use tools, hallucinated

---

## Quick Reference

### All 16 Queries

| # | Topic | Script |
|---|-------|--------|
| 1 | System overview | batch1_prompt.md |
| 2 | Backend architecture | batch1_prompt.md |
| 3 | Tool count (BUG: 14 not 13) | batch1_prompt.md |
| 4 | Phase 2 completion | batch2_prompt.md |
| 5 | Chonkie benefits | batch2_prompt.md |
| 6 | Search types | batch2_prompt.md |
| 7 | Deployment architecture | query_07_deployment.md |
| 8 | File type support | query_08_file_types.md |
| 9 | Search capabilities | query_09_search_capabilities.md |
| 10 | Semantic search | query_10_semantic_search.md |
| 11 | File reading | query_11_reading_files.md |
| 12 | Phase changes | query_12_phase_changes.md |
| 13 | Differentiation | query_13_differentiation.md |
| 14 | Practical examples | query_14_practical_examples.md |
| 15 | Troubleshooting | query_15_troubleshooting.md |
| 16 | Write access | query_16_write_access.md |

---

## Troubleshooting

### "Model can't find documents"

**Cause:** `.librarianignore` is excluding core documentation

**Fix:**
```bash
# Check .librarianignore excludes
cat .librarianignore

# Ensure core docs are NOT excluded:
# - README.md ✅ Should be INDEXED
# - ARCHITECTURE.md ✅ Should be INDEXED
# - SECURITY.md ✅ Should be INDEXED
# - CONFIGURATION.md ✅ Should be INDEXED

# Rebuild library if needed
rm -rf chroma_db metadata
./setup_mcp.sh
```

### "Model isn't using tools"

**Cause:** Model not receiving tool definitions from MCP system

**Fix:**
- Use Jan UI (not API) - API doesn't expose tools properly
- Restart MCP client in Jan UI
- Check prompt_jan.md has explicit tool list with "DO NOT search files" instruction

### "Response files not being created"

**Cause:** `write_document` tool failing or permissions issue

**Fix:**
```bash
# Ensure directory exists
mkdir -p librarian/reports/self_validation

# Check write permissions
ls -la librarian/reports/self_validation/

# Test write_document manually via chat
```

---

## Summary

- **Total Queries:** 16
- **Batch Scripts:** 6 (batch1-6_prompt.md)
- **Atomic Scripts:** 10 (query_07-16.md)
- **Strategy A:** Use batch prompts for GLM-4.7 (fast, large context)
- **Strategy B:** Use atomic scripts for 4B models (slow, small context, truly atomic)
- **Output:** `librarian/reports/self_validation/response_NNN.md`
- **Known Bug:** Criteria expect 13 tools but system has 14 (write_document)
