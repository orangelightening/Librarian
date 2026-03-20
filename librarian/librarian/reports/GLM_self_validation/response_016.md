# Query 16: What is the write_document tool and how does it enable two-way communication?

The `write_document` tool is a unique feature of the librarian-mcp system that creates a two-way communication channel between users and the AI librarian. Unlike traditional read-only MCP servers, the librarian can write persistent files to a dedicated workspace for your review and use.

## What is write_document?

The `write_document` tool allows the librarian to write files to a dedicated `/librarian/` workspace subdirectory within the allowed directory. This creates a bidirectional communication channel where:

1. **Librarian → User**: Delivers analysis results, code changes, and documentation updates
2. **User → Librarian**: Reviews content, provides feedback, and requests refinements
3. **User Controls Application**: You decide what changes to apply to your actual project

### Tool Signature

```python
write_document(
    path: str,           # File path relative to /librarian/
    content: str,        # File content to write
    create_dirs: bool = True  # Create parent directories if needed
)
```

**Example**:
```python
write_document('reports/fix.py', 'def fix_bug():\n    return "fixed"')
```

---

## How It Enables Two-Way Communication

### Traditional Read-Only MCP Servers

```
User Query → Server Reads → Response Lost
                              ↑
                         (Copy/paste required)
```

### Librarian-MCP with Two-Way Communication

```
User Query → Librarian Researches → Writes to /librarian/
                                         ↓
                                    User Reviews
                                         ↓
                                    Applies Changes
```

### Communication Patterns

**Pattern 1: Analysis Delivery**
```
User: "Review all exception handling in backend/"
Librarian: [Searches code, provides summary]
User: "Write your findings to /librarian/exception-analysis.md"
Librarian: [Writes detailed report with file paths and line numbers]
User: [Reads /librarian/exception-analysis.md]
User: [Applies approved changes based on analysis]
```

**Pattern 2: Iterative Refinement**
```
User: "Create a refactoring plan for the auth module"
Librarian: [Writes /librarian/refactor-plan-v1.md]
User: "Add more detail on migration steps"
Librarian: [Writes /librarian/refactor-plan-v2.md with verification]
```

**Pattern 3: Task Breakdown**
```
User: "Analyze the entire codebase for security issues"
Librarian: "That's a large task. I'll break it into parts:"
Librarian: [Writes /librarian/security-part1-backend.md]
Librarian: [Writes /librarian/security-part2-core.md]
Librarian: [Writes /librarian/security-part3-tools.md]
User: [Reviews each part independently]
```

---

## Key Features

### Persistent Analysis with Version Tracking

- **No more copying/pasting long responses** - Large analyses are saved as files
- **Version tracking support** - Use v1, v2, v3 naming conventions
- **Persistent storage** - Files remain available between sessions
- **Organized output** - Use subdirectories like `/librarian/reports/`, `/librarian/analysis/` `[Source: README.md]`

### User Control and Review

**User → Librarian: Review and Apply**

You retain full control over what gets applied:
- **Read files** written by the Librarian using `read_document()`
- **Review the content** and decide whether to apply changes
- **Modify files manually** in your editor before applying
- **Delete files** in the `/librarian/` directory at any time `[Source: Tools.md]`

**Example Workflow**:
```
User: "Analyze exception handling in backend/, write to /librarian/analysis.md"
Librarian: [Searches code, writes detailed report]
User: [Reads /librarian/analysis.md to review findings]
User: [Applies approved code changes based on analysis]
User: [Deletes /librarian/analysis.md when done]
```

---

## Security Model

The `write_document` tool maintains strict security boundaries with **7 layers of protection** `[Source: Tools.md]`:

### Layer 1: Subdirectory Restriction
Writes are **only allowed** in the `/librarian/` subdirectory.

```python
# Path validation enforces librarian/ subdirectory
librarian_dir = os.path.join(safe_dir, "librarian")
if not resolved_path.startswith(librarian_dir):
    return "[security error] Write operations only allowed in /librarian/"
```

**What This Means**:
- ❌ Cannot write to project source files
- ❌ Cannot write to system configuration files
- ❌ Cannot write anywhere in the filesystem
- ✅ Can only write to `/librarian/` workspace

### Layer 2: File Size Limits
Maximum **100KB per write operation** to prevent memory issues and context overflow.

```python
MAX_WRITE_FILE_SIZE = 100000  # 100KB
if len(content) > MAX_WRITE_FILE_SIZE:
    return "[error] Content exceeds maximum file size of 100KB"
```

**Note**: This is separate from document ingestion limits (10MB) `[Source: CONFIGURATION.md]`

### Layer 3: Path Sanitization
Multiple security checks on the file path:

```python
# Path cannot be empty
if not path:
    return "[security error] Path cannot be empty"

# Strip leading/trailing slashes and whitespace
clean_path = path.strip().strip('/').strip('\\')

# Reject paths trying to escape librarian workspace
# Check if path contains project directory name or parent directory
```

### Layer 4: Critical File Protection
Blocks writing to files with sensitive filename patterns:

```python
critical_patterns = ['password', 'secret', 'key', 'credential', '.env', 'config']
path_lower = resolved_real.lower()
for pattern in critical_patterns:
    if pattern in path_lower:
        return f"[security error] Cannot write to files containing '{pattern}' in path"
```

**Blocked Patterns**:
- Files containing: `password`, `secret`, `key`, `credential`, `.env`, `config`
- Even within `/librarian/` subdirectory, these filenames are blocked `[Source: Tools.md]`

### Layer 5: Directory Traversal Protection
Uses the same `is_safe_path()` validation as read operations:

```python
# Critical security check - prevents ../ attacks
if not resolved.startswith(base):
    return False, f"Path outside safe directory"
```

Prevents directory traversal attacks like:
- `../../etc/passwd`
- `/etc/hosts`
- `../../../../sensitive_file`

### Layer 6: Safe Directory Enforcement
Must stay within the `LIBRARIAN_SAFE_DIR` boundary:

```python
safe_dir_real = os.path.realpath(SAFE_WORKING_DIR)
librarian_dir = os.path.join(safe_dir_real, LIBRARIAN_WRITE_DIR)

if not resolved_real.startswith(librarian_dir):
    return f"[security error] Write operations only allowed in /librarian/ subdirectory"
```

All write operations are constrained within the configured safe directory boundary.

### Layer 7: Audit Logging
All write operations are logged to console:

```python
print(f"[librarian-mcp] [write] {resolved_path} ({len(content)} bytes)")
```

This provides:
- **Visibility**: You can see all files being written
- **Audit Trail**: Complete record of write operations
- **Debugging**: Helps track write activity `[Source: Tools.md]`

---

## Security Boundaries

### What Can Be Written To

✅ **Allowed in `/librarian/` workspace**:
- Analysis results and reports
- Code change suggestions
- Documentation updates
- Debugging diagnostics
- Task delegation outputs
- Refactoring plans
- Validation reports
- Any content for your review `[Source: Tools.md]`

### What Cannot Be Written To

❌ **Restricted**:
- Files outside `/librarian/` subdirectory
- System configuration files
- Files with sensitive names (password, secret, key, credential, .env, config)
- Files larger than 100KB
- Files outside safe directory boundary
- Project source files directly (must go through `/librarian/` first) `[Source: Tools.md]`

**Important**: The librarian **cannot write anywhere in the filesystem** - only within the `/librarian/` workspace subdirectory.

---

## Context Window Management

### Understanding Context Usage

The librarian generates the complete response in context **before writing to disk**. Large analyses (even if written successfully to files) consume LLM context window.

**Why this matters**:
- Breaking tasks into smaller chunks ensures better performance
- Avoids context overflow with large responses
- Prevents memory issues `[Source: prompt_patterns.md]`

### Best Practices for Optimal Performance

1. **Break large tasks into chunks**:
   ```
   "Analyze backend/chroma_backend.py only, write to /librarian/chroma-analysis.md"
   "Now analyze backend/chonkie_backend.py, write to /librarian/chonkie-analysis.md"
   ```

2. **Request summary in chat, full details to file**:
   ```
   "Give me a brief summary in chat, but write the complete detailed analysis to /librarian/full-analysis.md"
   ```

3. **Use version tracking for iterative refinement**:
   ```
   "Write version 1 to /librarian/analysis-v1.md"
   "Then update with more details in /librarian/analysis-v2.md"
   ```

---

## Use Cases

### When to Use write_access

✅ **Code reviews and refactoring plans**
✅ **Security audit results**
✅ **Documentation updates**
✅ **Debugging diagnostics**
✅ **Multi-file analysis reports**
✅ **Task delegation outputs**

### When to Keep It Brief

❌ **Simple questions** that don't need persistent storage
❌ **Quick lookups** where a chat response is sufficient
❌ **Real-time debugging** where you need immediate feedback

---

## Workflow Example

Here's a complete two-way communication workflow:

```
Step 1: User Requests Analysis
User: "Analyze exception handling in backend/, identify all generic Exception catches"

Step 2: Librarian Researches
Librarian: [Uses search_documents() to find 'except Exception' patterns]
Librarian: [Analyzes 15 instances across 8 files]
Librarian: "Found 15 instances. 5 are critical security risks. Should I write detailed analysis?"

Step 3: User Requests Persistent File
User: "Yes, write it to /librarian/exception-analysis.md"

Step 4: Librarian Writes File
Librarian: [write_document('/librarian/exception-analysis.md', detailed_analysis)]
Librarian: "Written analysis with file paths, line numbers, severity ratings, and recommendations"

Step 5: User Reviews
User: [read_document('/librarian/exception-analysis.md')]
User: "The analysis looks good. I'll apply the critical fixes first."

Step 6: User Applies Changes
User: [Manually applies code changes based on analysis]
User: "I've fixed the critical issues. Can you verify?"

Step 7: Iterative Improvement
User: "Write a follow-up report on the remaining issues to /librarian/exception-followup.md"
Librarian: [Writes updated analysis]

Step 8: Cleanup
User: [Deletes /librarian/exception-analysis.md when done]
```

---

## Summary

The `write_document` tool enables true two-way communication by:

1. **Write access to `/librarian/` workspace** - Librarian can write persistent files
2. **Persistent analysis with version tracking** - v1, v2, v3 patterns support iterative work
3. **User control** - You review before applying changes to your actual project
4. **Security boundaries** - Writes only in `/librarian/` subdirectory, not anywhere in filesystem
5. **7 layers of protection** - Comprehensive security model
6. **File size limit** - 100KB per write to prevent context overflow
7. **Context window awareness** - Large tasks should be broken into chunks

This transforms the librarian from a simple search tool into an active development partner that can deliver analysis, code changes, and documentation for your review - enabling real collaboration workflows that aren't possible with read-only MCP servers `[Source: README.md]`, `[Source: Tools.md]`.
