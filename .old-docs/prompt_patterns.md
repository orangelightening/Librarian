# Librarian Prompt Patterns

**Purpose**: Reusable prompt patterns for effective librarian interaction

**How to use**: Copy these patterns and adapt them to your specific needs

---

## Pattern 1: Validation with Self-Reflection

### Description
Ask the librarian to provide a response, then critique its own response against expected criteria, and recommend documentation improvements.

### Template
```
[Your main query here]

Follow-up: Given the expected response [list expected criteria], evaluate your response. Recommend changes to the documentation to improve comprehension and correctness of the library. Include file and line references if possible.
```

### Example Usage
```
Query: "What is the librarian-mcp system?"

Follow-up: Given the expected response:
- Phase 2 complete (not planned)
- Chonkie as default backend
- 13 tools (7 library + 4 file system + 2 system)
- prompt.md mentioned as system prompt

Evaluate your response. Recommend changes to the documentation to improve comprehension and correctness. Include file and line references if possible.
```

### When to Use
- Validating documentation accuracy
- Testing librarian's understanding of the system
- Getting self-reflective critique of librarian responses
- Identifying documentation gaps

---

## Pattern 2: Comparative Analysis

### Description
Ask the librarian to compare two or more documents and identify differences, contradictions, or gaps.

### Template
```
Compare [document A] and [document B] in terms of [specific aspect].
Identify any contradictions, gaps, or differences between them.
Provide specific file and line references.
```

### Example Usage
```
Compare README.md and CONFIGURATION.md in terms of backend selection.
Identify any contradictions, gaps, or differences between them.
Provide specific file and line references.
```

### When to Use
- Finding contradictions between documentation files
- Ensuring consistency across docs
- Identifying which doc is more authoritative for a topic
- Validating that documentation agrees with implementation

---

## Pattern 3: Tracing and Investigation

### Description
Ask the librarian to trace a specific feature, function, or behavior across multiple files.

### Template
```
Trace how [feature/function] is implemented across the codebase.
Show the flow from [entry point] through [intermediate layers] to [implementation].
Include file names, line numbers, and relevant code snippets.
```

### Example Usage
```
Trace how document ingestion works across the codebase.
Show the flow from user query through document manager to backend to ChromaDB storage.
Include file names, line numbers, and relevant code snippets.
```

### When to Use
- Understanding complex data flows
- Debugging by tracing execution paths
- Learning how features are implemented
- Identifying which files handle specific functionality

---

## Pattern 4: Gap Analysis

### Description
Ask the librarian to identify what's missing from documentation or implementation.

### Template
```
Review [documentation area] and identify:
1. What topics are covered
2. What topics are missing or incomplete
3. What information is outdated
4. What would improve comprehension

Provide specific recommendations with file and line references.
```

### Example Usage
```
Review all documentation related to backend selection and identify:
1. What topics are covered
2. What topics are missing or incomplete
3. What information is outdated
4. What would improve comprehension

Provide specific recommendations with file and line references.
```

### When to Use
- Finding documentation gaps
- Planning documentation updates
- Ensuring comprehensive coverage
- Identifying areas needing improvement

---

## Pattern 5: Code Review Assistant

### Description
Ask the librarian to analyze code for specific issues, patterns, or improvements.

### Template
```
Review [file or directory] for [specific concern].
Identify all instances of [what you're looking for].
Provide file names, line numbers, and code snippets.
Suggest improvements if applicable.
```

### Example Usage
```
Review mcp_server/backend/ for exception handling patterns.
Identify all instances where generic Exception is caught instead of specific exceptions.
Provide file names, line numbers, and code snippets.
Suggest improvements if applicable.
```

### When to Use
- Code reviews
- Finding bugs or anti-patterns
- Identifying refactoring opportunities
- Security audits

---

## Pattern 6: Consistency Check

### Description
Ask the librarian to verify consistency between implementation and documentation.

### Template
```
Check if [document] accurately reflects the current implementation in [code file].
Identify any discrepancies between what the document says and what the code does.
Provide specific file names, line numbers, and examples.
```

### Example Usage
```
Check if README.md accurately reflects the current backend implementation in mcp_server/config/settings.py.
Identify any discrepancies between what README says and what the code actually does.
Provide specific file names, line numbers, and examples.
```

### When to Use
- Validating documentation matches code
- Finding outdated documentation
- Ensuring implementation matches specs
- Pre-release documentation checks

---

## Pattern 7: Security Audit

### Description
Ask the librarian to perform a focused security review.

### Template
```
Perform a security review of [area or feature].
Identify all security measures in place.
Check for potential vulnerabilities or missing protections.
Provide file names, line numbers, and security best practices if issues are found.
```

### Example Usage
```
Perform a security review of the execute_command tool.
Identify all security measures in place.
Check for potential vulnerabilities or missing protections.
Provide file names, line numbers, and security best practices if issues are found.
```

### When to Use
- Security audits
- Identifying potential vulnerabilities
- Verifying security controls are in place
- Finding gaps in security coverage

---

## Pattern 8: Documentation Improvement

### Description
Ask the librarian to suggest specific improvements to documentation.

### Template
```
Review [document] and suggest improvements for:
- Clarity and comprehensibility
- Organization and structure
- Completeness of coverage
- Accuracy of technical details
- Missing examples or use cases

Provide specific suggestions with file and line references where applicable.
```

### Example Usage
```
Review CONFIGURATION.md and suggest improvements for:
- Clarity and comprehensibility
- Organization and structure
- Completeness of coverage
- Accuracy of technical details
- Missing examples or use cases

Provide specific suggestions with file and line references where applicable.
```

### When to Use
- Improving documentation quality
- Making docs more user-friendly
- Adding missing content
- Pre-publication documentation review

---

## Pattern 9: Impact Analysis

### Description
Ask the librarian to analyze what would break if you make a specific change.

### Template
```
Analyze the impact of changing [specific thing] in the codebase.
Identify all files that would be affected.
Describe what would break and what would need updating.
Provide file names and line numbers.
```

### Example Usage
```
Analyze the impact of changing the chunk size from 1000 to 2000 characters.
Identify all files that would be affected.
Describe what would break and what would need updating.
Provide file names and line numbers.
```

### When to Use
- Pre-refactoring analysis
- Understanding change impact
- Risk assessment for changes
- Planning refactoring work

---

## Pattern 10: Exploratory Search

### Description
Ask the librarian to explore a topic and provide comprehensive coverage.

### Template
```
Provide a comprehensive explanation of [topic or feature].
Include:
- How it works
- Where it's implemented
- Key design decisions
- Examples of usage
- Connections to related features

Use citations from relevant source files.
```

### Example Usage
```
Provide a comprehensive explanation of how the ignore patterns system works.
Include:
- How it's implemented
- Where the patterns are stored
- How patterns are matched
- Examples of built-in patterns
- Security implications

Use citations from relevant source files.
```

### When to Use
- Learning new features
- Understanding complex systems
- Getting comprehensive overviews
- Onboarding to new codebases

---

## Example Dialogues

These real-world examples show how the patterns work in practice.

### Dialogue 1: Contradiction Detection (Pattern 2)

**User**: Compare README.md and CONFIGURATION.md in terms of backend selection. Identify any contradictions, gaps, or differences.

**Librarian**:
> I've analyzed both documents regarding backend selection:
>
> **README.md** (lines 24-40):
> - States Chonkie is the DEFAULT backend
> - Mentions ChromaDB backend is optional
> - Focuses on practical usage
>
> **CONFIGURATION.md** (lines 67-95):
> - States Chonkie is the DEFAULT backend (via environment variable)
> - ChromaDB backend is also available
> - Provides detailed environment variable configuration
> - Includes performance comparison
>
> **No contradictions found** - Both documents agree that Chonkie is default and ChromaDB is optional.
>
> **Gap identified**: Neither document explicitly states that `LIBRARIAN_BACKEND` defaults to "chonkie" in the code itself (settings.py line 29).

**User**: Good, that gap is real. Check settings.py line 29 and confirm what the actual default is.

**Librarian**:
> You're correct to question this. Checking `settings.py` line 29:
>
> ```python
> BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")
> ```
>
> ✅ **Confirmed**: The code sets "chonkie" as the default value (third parameter to `os.getenv()`).
>
> **Documentation is accurate** - both README.md and CONFIGURATION.md correctly state Chonkie is the default backend.
>
> **Recommendation**: Documentation is consistent with implementation. No changes needed.

---

### Dialogue 2: Code Review Assistant (Pattern 5)

**User**: Review mcp_server/backend/ for exception handling patterns. Identify all instances where generic Exception is caught instead of specific exceptions.

**Librarian**:
> I've searched the backend directory for exception handling:
>
> **chroma_backend.py**:
> - Line 133: `except Exception as e` - Generic catch during embedding operations [Source: chroma_backend.py:133]
> - Line 156: `except Exception as e` - Generic catch during query operations [Source: chroma_backend.py:156]
>
> **chonkie_backend.py**:
> - Line 31: `except Exception as e` - Generic catch in chunking operations [Source: chonkie_backend.py:31]
>
> **factory.py**:
> - Line 30: `raise ValueError(...)` - Proper exception type for unsupported backend [Source: factory.py:30]
>
> **Issue**: Generic `Exception` catches in backend operations may hide specific errors (ChromaDB connection errors, chunking failures, etc.).
>
> **Recommendations**:
> 1. `chroma_backend.py:133` - Catch `chromadb.errors.*` exceptions specifically
> 2. `chroma_backend.py:156` - Catch `chromadb.errors.*` exceptions specifically
> 3. `chonkie_backend.py:31` - Catch chunking-specific exceptions from Chonkie library
> 4. This would make debugging easier and error handling more precise.

**User**: Excellent analysis. What specific ChromaDB exceptions should we use for lines 133 and 156?

**Librarian**:
> Looking at ChromaDB's exception hierarchy and common usage patterns:
>
> **Line 133** (embedding operations):
> ```python
> except chromadb.errors.DuplicateIDException:
>     # Handle duplicate chunk IDs
> except chromadb.errors.InvalidDimensionException:
>     # Handle embedding dimension mismatches
> except Exception as e:
>     # Fallback for unexpected errors
> ```
>
> **Line 156** (query operations):
> ```python
> except chromadb.errors.InvalidCollectionException:
>     # Handle collection doesn't exist
> except chromadb.errors.NoIndexException:
>     # Handle collection not indexed
> ```
>
> **Files to update**:
> - `mcp_server/backend/chroma_backend.py:133`
> - `mcp_server/backend/chroma_backend.py:156`
>
> These specific exceptions would make it easier to diagnose ChromaDB-specific issues during embedding and query operations.

---

### Dialogue 3: Gap Analysis (Pattern 4)

**User**: Review all documentation related to backend selection and identify what topics are covered, what's missing, and what would improve comprehension.

**Librarian**:
> **Documentation Coverage Analysis**:
>
> **README.md** (lines 24-40):
> - ✅ Mentions Chonkie is default
> - ✅ Mentions ChromaDB is optional
> - ❌ Doesn't explain WHEN to use each backend
>
> **CONFIGURATION.md** (lines 67-95):
> - ✅ States Chonkie is default
> - ✅ Provides environment variable setup
> - ❌ Limited guidance on backend selection criteria
>
> **CHONKIE_MIGRATION.md** (PHASE2/CHONKIE_MIGRATION.md):
> - ✅ Explains what Chonkie is
> - ✅ Performance comparison table
> - ❌ Not referenced in main documentation
>
> **Gaps Identified**:
> 1. **Decision criteria**: No clear guidance on when to use Chonkie vs ChromaDB
> 2. **Use cases**: No concrete examples of when each backend shines
> 3. **Migration path**: How to switch from ChromaDB to Chonkie (or vice versa)
> 4. **Performance tradeoffs**: Specific benchmarks or expectations
>
> **Recommendations**:
> 1. Add "Backend Selection Guide" section to README.md
> 2. Include use case examples for each backend
> 3. Add simple decision tree: "Use Chonkie if... Use ChromaDB if..."
> 4. Link to CHONKIE_MIGRATION.md for more details
>
> **Files to update**:
> - `README.md` - Add backend selection guidance
> - `CONFIGURATION.md` - Expand backend selection section

---

### Dialogue 4: Consistency Check (Pattern 6)

**User**: Check if README.md accurately reflects the current backend implementation in settings.py. Identify discrepancies.

**Librarian**:
> Checking README.md claims against settings.py implementation:
>
> **README.md line 24-27** claims:
> > "ChonkieBackend (Default): Intelligent semantic chunking"
> > "ChromaDB Backend (Optional): Simple sentence-based chunking"
>
> **settings.py line 29** implements:
> ```python
> BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")
> ```
>
> ✅ **Accurate**: README correctly states Chonkie is the default
>
> **Additional findings**:
> - README.md doesn't mention the Literal type hint
> - README.md doesn't explain how to verify current backend
>
> **Minor discrepancy**: README says "Simple sentence-based chunking" for ChromaDB, but examining `chroma_backend.py:73-90` shows it uses sentence splitting with '. ' delimiter, which is accurate.
>
> **Recommendation**: Add verification instruction:
> "To verify current backend: `python -c 'from mcp_server.config.settings import settings; print(settings.BACKEND)'`"
>
> **Overall**: Documentation is accurate, no critical discrepancies found.

---

### Dialogue 5: Security Audit (Pattern 7)

**User**: Perform a security review of the execute_command tool. Identify all security measures in place and check for potential vulnerabilities.

**Librarian**:
> **Security Review: execute_command Tool** [Source: mcp_server/tools/cli_tools.py]
>
> **Security Measures Implemented**:
>
> **1. Command Whitelisting** (lines 14-18):
> ```python
> ALLOWED_BINARY_NAMES = {
>     "ls", "cd", "pwd", "whoami", "echo", "cat", "find", "grep",
>     "head", "tail", "sort", "uniq", "cut", "awk", "date", "hostname"
> }
> ```
> - ✅ Only 17 approved binaries
> - ✅ Dangerous commands explicitly blocked (lines 35-40)
>
> **2. Dangerous Flag Combinations** (lines 20-26):
> ```python
> BANNED_FLAG_COMBOS = {
>     ("find", "-delete"), ("find", "-exec"),
>     ("find", "-execdir"), ("awk", "system"),
>     ("awk", "systime")
> }
> ```
> - ✅ Prevents command injection via flags
>
> **3. Directory Sandboxing** (lines 109-117):
> ```python
> def is_safe_command(command, args):
>     cmd_name = os.path.basename(cmd)
>     if cmd_name in DANGEROUS_COMMANDS:
>         return False, f"Command '{cmd_name}' is explicitly blocked."
> ```
>
> **4. Path Validation** (lines 61-73):
> ```python
> def is_safe_path(path: str, safe_dir: str):
>     resolved = os.path.realpath(path)
>     if not resolved.startswith(base):
>         return False, f"Path traversal detected"
> ```
> - ✅ Prevents directory traversal
>
> **5. Timeout Protection** (line 127):
> ```python
> timeout=DEFAULT_TIMEOUT_SECONDS
> ```
> - ✅ Prevents runaway commands (15 second default)
>
> **6. Output Truncation** (lines 76-81):
> - ✅ Limits output to protect LLM context
>
> **Potential Vulnerabilities**:
> ⚠️ **Line 109**: `is_safe_command()` checks if command is whitelisted, but doesn't validate that the command at `cmd.startswith('/')` is still whitelisted (could be bypassed with absolute paths to whitelisted binaries)
>
> **Recommendation**: Add validation: Even absolute paths to whitelisted commands should be verified against the whitelist after basename extraction.
>
> **Files to check**:
> - `mcp_server/tools/cli_tools.py:109-117`

**User**: Good catch! Can you show me the exact code for line 109?

**Librarian**:
> ```python
> # Line 109
> def is_safe_command(command: str, args: list) -> tuple[bool, str]:
>     cmd_name = os.path.basename(cmd)
>     if cmd_name in DANGEROUS_COMMANDS:
>         return False, f"Command '{cmd_name}' is explicitly blocked."
> ```
>
> The issue is that if `command` is `/usr/bin/ls`, then `cmd_name` becomes "ls" and passes the whitelist check, even though the absolute path might be a different `ls` binary outside the safe directory.

---

### Dialogue 6: Documentation Improvement (Pattern 8)

**User**: Review ARCHITECTURE.md and suggest improvements for clarity and comprehensiveness.

**Librarian**:
> **Architecture.md Review**:
>
> **Strengths**:
> - ✅ Excellent ASCII diagrams showing system layers
> - ✅ Clear separation of concerns explained
> - ✅ Backend factory pattern well documented
> - ✅ Data flow diagrams helpful
>
> **Areas for Improvement**:
>
> **1. Missing: Architecture Evolution** (no specific line reference, gap in content):
> - No section explaining how Phase 1 evolved to Phase 2
> - Would help users understand historical context
> - **Suggestion**: Add "Architecture Evolution" section with timeline
>
> **2. Line 248: Backend selection decision tree is mentioned but not shown**:
> > "When to use each backend"
> - **Suggestion**: Add visual decision tree:
> ```
>   Need semantic chunking?
>   ├── YES → Chonkie backend
>   └── NO → ChromaDB backend
>   ```
>
> **3. Lines 89-120: File structure lists backend files but doesn't explain their relationships**:
> - chonkie_backend.py inherits from chroma_backend.py
> - factory.py creates instances
> - base.py defines the interface
> - **Suggestion**: Add inheritance diagram or relationship section
>
> **4. Missing: Error handling strategies** (gap in content):
> - No explanation of what happens when ChromaDB is down
> - No fallback mechanisms documented
> - **Suggestion**: Add "Error Handling and Fault Tolerance" section
>
> **Files to update**:
> - `ARCHITECTURE.md` - Add the 4 suggested sections
>
> **Estimated effort**: 30-45 minutes to implement all improvements

---

### Dialogue 7: Debugging Assistant (Pattern 3)

**User**: I'm getting an error when syncing documents. The error message says "Permission denied" but I don't know which file is causing it. Can you help me debug this?

**Librarian**:
> I can help you debug this. Let me trace the document sync flow to understand where permission errors occur.
>
> **Sync Flow Tracing** [Source: document_manager.py, sync_directory method]:
>
> The `sync_directory()` method (lines 125-180) follows this sequence:
> 1. Discovers documents using `discover_documents()`
> 2. For each document, calls `add_document()`
> 3. `add_document()` opens the file for reading
> 4. Calculates checksum
> 5. Passes to backend for chunking
>
> **Potential Permission Error Points**:
> - **Line 142**: `with open(file_path, 'r', encoding='utf-8') as f` - File open operation
> - **Line 156**: Checksum calculation requires file read access
> - **backend/chroma_backend.py:102**: `collection.add()` - ChromaDB write access
> - **metadata/index.json**: Metadata store write access
>
> **Most Likely Cause**: The error occurs at document_manager.py:142 when trying to open a file that the process doesn't have read permissions for.
>
> **Debugging Steps**:
> 1. Check which files are in the sync directory
> 2. Verify file permissions on suspect files
> 3. Check if .librarianignore is incorrectly excluding needed files
> 4. Verify LIBRARIAN_SAFE_DIR allows access to target directory

**User**: Good analysis. I'm syncing `/home/peter/documents` and my safe directory is `/home/peter/development`. Could that be the issue?

**Librarian**:
> **Found the Issue!**
>
> **Root Cause**: Directory sandboxing violation [Source: cli_tools.py, lines 61-73]
>
> The `is_safe_path()` function enforces:
> ```python
> def is_safe_path(path: str, safe_dir: str):
>     resolved = os.path.realpath(path)
>     base = os.path.realpath(safe_dir)
>     if not resolved.startswith(base):
>         return False, f"Path traversal detected"
> ```
>
> **Your Configuration**:
> - `LIBRARIAN_SAFE_DIR=/home/peter/development`
> - Syncing from: `/home/peter/documents`
> - `/home/peter/documents` does NOT start with `/home/peter/development`
>
> **This is NOT a permission error** - it's a security boundary. The sync operation is blocked because `/home/peter/documents` is outside the safe directory.
>
> **Solution Options**:
>
> **Option 1**: Expand safe directory to include documents
> ```bash
> export LIBRARIAN_SAFE_DIR=/home/peter
> # Restart server
> ```
>
> **Option 2**: Move documents into safe directory
> ```bash
> mv /home/peter/documents /home/peter/development/documents
> # Then sync from new location
> ```
>
> **Option 3**: Create symlink in safe directory
> ```bash
> ln -s /home/peter/documents /home/peter/development/documents-link
> # Sync from the link
> ```
>
> **Recommendation**: Option 1 is cleanest if you trust all directories under `/home/peter`. Option 2 is most secure if you want to keep strict boundaries.

**User**: I'll use Option 1. That makes sense. The error message was misleading though - it said "Permission denied" when it was really a security boundary.

**Librarian**:
> **Good observation** - this is a documentation/UX improvement opportunity!
>
> **Current Error Handling** [Source: cli_tools.py:69-73]:
> ```python
> if not resolved.startswith(base):
>     return False, f"Path traversal detected"
> ```
>
> When tools receive `False` from `is_safe_path()`, they may show generic "Permission denied" errors instead of the specific security message.
>
> **Recommended Improvement**:
> Update error messages in library_tools.py to be more specific:
> ```python
> # In sync_directory()
> if not is_safe_path(path, safe_dir)[0]:
>     return {
>         'status': 'error',
>         'message': f'Security boundary: {path} is outside safe directory {safe_dir}'
>     }
> ```
>
> **Files to Update**:
> - `mcp_server/tools/library_tools.py` - sync_directory(), add_document()
> - `mcp_server/tools/cli_tools.py` - read_document(), list_documents()
>
> This would make debugging much easier by showing the actual security boundary violation instead of generic permission errors.

---

### Dialogue 8: Task Delegation with Write Access (Pattern 9)

**User**: I need to refactor the exception handling in the backend code. Can you find all instances where we catch generic Exception and suggest specific exceptions?

**Librarian**:
> I'll search the backend/ directory for generic exception handling patterns.
>
> **Analysis Results** [Source: mcp_server/backend/]:
>
> **chroma_backend.py**:
> - Line 133: `except Exception as e` - During embedding operations
> - Line 189: `except Exception as e` - During query operations
>
> **chonkie_backend.py**:
> - Line 31: `except Exception as e` - During chunking operations
>
> **factory.py**:
> - Line 30: `raise ValueError(...)` - Proper exception type ✅
>
> **Issue**: Generic `Exception` catches may hide specific errors (ChromaDB connection failures, chunking errors, etc.) and make debugging harder.
>
> **Recommendations**:
> 1. chroma_backend.py:133 - Catch `chromadb.errors.DuplicateIDException`
> 2. chroma_backend.py:189 - Catch `chromadb.errors.InvalidCollectionException`
> 3. chonkie_backend.py:31 - Catch chunking-specific exceptions from Chonkie library

**User**: That's helpful, but I need the specific code for each fix. Can you write this analysis to a file?

**Librarian**:
> I'll write a detailed refactoring plan to `/librarian/backend-exception-refactor.md`.
>
> [Writes file with complete analysis]
>
> **File created**: `/librarian/backend-exception-refactor.md` (2,847 bytes)
>
> The file includes:
> - Current code snippets for each instance
> - Recommended specific exception types
> - Complete replacement code blocks
> - Rationale for each change
> - Testing recommendations

**User**: [Reads the file using `read_document('/librarian/backend-exception-refactor.md')`]

**User**: Good analysis! I'll implement these changes. Can you also check the core/ directory for the same issue?

**Librarian**:
> [Searches core/ directory for generic exception handling]
>
> **core/document_manager.py**:
> - Line 156: `except Exception as e` - File read errors
> - Line 203: `except Exception as e` - Checksum calculation errors
>
> **core/metadata_store.py**:
> - Line 89: `except Exception as e` - JSON parsing errors
> - Line 134: `except Exception as e` - File write errors
>
> I'll append these findings to the existing analysis file.

**User**: Wait, don't overwrite the previous analysis. Create a new file.

**Librarian**:
> You're absolutely right. I'll write a separate analysis for core/ directory.
>
> [Writes new file]
>
> **File created**: `/librarian/core-exception-refactor.md` (2,341 bytes)
>
> This way you can review and apply changes for each module independently.

**User**: Perfect. Now I can work through backend/ first, then core/. This write access is much better than copying everything from chat.

**Librarian**:
> Exactly! The write access creates a persistent, organized workflow:
> 1. I write detailed analysis to `/librarian/` files
> 2. You review at your own pace
> 3. You apply changes based on recommendations
> 4. Files remain available for reference or version control
> 5. I can write v2, v3 files for updated analysis
>
> No more copying/pasting long responses or losing context in chat history.

---

## Tips for Effective Patterns

### Be Specific
- ❌ "Tell me about security"
- ✅ "Perform a security review of command execution with focus on timeout mechanisms"

### Provide Context
- ❌ "Check the backend"
- ✅ "Compare Chonkie backend and ChromaDB backend in terms of chunking quality"

### Ask for Citations
- Always request file names and line numbers
- This makes verification possible
- Allows you to check the librarian's work

### Use Follow-up Questions
- Don't accept incomplete answers
- Ask for clarification: "You mentioned X but didn't cite sources. Can you provide file references?"
- Drill down: "Line 50 of which file? Can you show me the code?"

### Request Recommendations
- Ask: "What would improve this documentation?"
- Ask: "Is this information missing from any docs?"
- Ask: "Where should this be documented?"

---

## Building Custom Patterns

When creating your own patterns, include:

1. **Clear Objective** - What you want to accomplish
2. **Specific Scope** - What files/areas to focus on
3. **Deliverables** - What you want in the response
4. **Verification** - How to verify the answer is correct
5. **References** - Request file names and line numbers

### Template for Creating Patterns
```
**Pattern Name**: [Descriptive name]

**Objective**: [What you want to accomplish]

**Prompt Template**:
[Your reusable prompt template here]

**Example Usage**:
[Concrete example of how to use it]

**When to Use**:
- Scenario 1
- Scenario 2

**Expected Deliverables**:
- [What the response should include]
- [How it should be structured]
```

---

## Pattern Catalog Quick Reference

| Pattern | Purpose | Best For |
|---------|---------|----------|
| Validation with Self-Reflection | Test + critique | Documentation validation, accuracy checks |
| Comparative Analysis | Compare docs | Finding contradictions, ensuring consistency |
| Tracing and Investigation | Follow data flows | Understanding architecture, debugging |
| Gap Analysis | Find missing info | Documentation planning, completeness checks |
| Code Review Assistant | Analyze code | Finding bugs, refactoring opportunities |
| Consistency Check | Docs vs code | Validating accuracy, finding outdated info |
| Security Audit | Review security | Security reviews, vulnerability assessment |
| Documentation Improvement | Suggest enhancements | Improving quality, adding content |
| Impact Analysis | Change effects | Risk assessment, planning changes |
| Exploratory Search | Comprehensive overview | Learning, understanding features |

---

**Remember**: These patterns are templates. Adapt them to your specific needs, and always request file names and line numbers for verification! 📚✨
