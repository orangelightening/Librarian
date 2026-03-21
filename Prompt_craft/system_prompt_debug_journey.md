# System Prompt Debug Journey

**Date**: 2026-03-20 → 2026-03-21
**Issue**: Model refusing to search library before answering questions
**Status**: ✅ RESOLVED

---

## The Problem

Small models (Qwen 4b, 7B, 9B) were refusing to answer questions without searching the library first, violating the explicit instruction: "ALWAYS search before refusing."

**Test query that consistently failed:**
```
User: "What is the System_prompt?"
Model: "I don't have information about System_prompt in my library"
[NO SEARCH PERFORMED - VIOLATED INSTRUCTION]
```

**Adding "file" keyword worked:**
```
User: "What is the System_prompt file?"
Model: [searches library] → finds System_prompt.md → answers correctly
```

---

## What Didn't Work

### 1. Duplicating Instructions
**Attempt**: Added same "ALWAYS search" warning at end of prompt (line 257)
**Result**: NO IMPROVEMENT - model still refused without searching

### 2. Model Parameter Adjustments
**Attempt**: User adjusted temperature, top_p, other parameters
**Result**: NO IMPROVEMENT - behavior unchanged

### 3. Adding Explicit Examples
**Attempt**: Considered adding concrete examples of when to search
**Result**: Not attempted - prompt already too long

### 4. Markdown Formatting
**Attempt**: Used formatted markdown with headers, bold, bullet points
**Result**: Models interpreted as "reference document" not "directives to execute"

### 5. Thinking Mode Hypothesis
**Initial theory**: Small models need thinking mode to process complex conditional instructions
**Testing**: Model WAS in thinking mode, still failed
**Conclusion**: Not a thinking mode issue, but a prompt formatting issue

---

## What Finally Worked

### The Winning Formula

**File**: `test2_system_prompt.md` → promoted to `System_prompt.md`

**Key changes:**

1. **First Sentence Instruction**
   ```
   You are the Librarian... ALWAYS DO A search_library at the start of any response.
   ```
   - Critical instruction in the VERY FIRST sentence
   - Model reads first sentence carefully
   - Immediate behavioral trigger

2. **Plain Text Format (No Markdown)**
   ```
   CRITICAL RULES
   ALWAYS USE search_library BEFORE answering questions...
   ```
   - Plain prose signals "directives" not "reference document"
   - ALL CAPS for emphasis instead of **bold markdown**
   - Short declarative sentences instead of bullet lists
   - No ### headers (headers signal "document" not "command")

3. **Integrated Critical Rules**
   ```
   CRITICAL RULES
   ALWAYS USE search_library...
   When you call tools you must use lowercase true false...
   If you use True or False the tool will FAIL...
   ```
   - Boolean format instruction embedded in CRITICAL RULES block
   - Not a separate section that gets skipped
   - High-attention placement

4. **Reinforcement in Multiple Places**
   - Line 1: "ALWAYS DO A search_library at the start of any response"
   - CRITICAL RULES section: "ALWAYS USE search_library..."
   - WHAT YOU DON'T DO: "Don't forget to do a search_library as your first step"

5. **Simple Direct Language**
   ```
   NOT True NOT False ever.
   ```
   - Short, punchy, unambiguous
   - Easy for small models to process
   - Clear consequences: "tool will FAIL"

---

## Test Results

### Before Fix (formatted markdown prompt)
- GLM (thinking): ✓ Works
- Qwen 4b 4-bit: ~ Partial (50%)
- Qwen 4b 8-bit: ✗ Fails consistently
- Qwen 9B Q5_K_M: ~ Partial (50%)

### After Fix (plain text prompt)
- All models: ✓ Works
- Thinking mode ON: ✓ Works
- Thinking mode OFF: ✓ Works
- Jan: ✓ Works
- LM Studio: ✓ Works
- **3 out of 3 queries in new contexts**: ✓ Works

---

## Key Learnings

### 1. Prompt Formatting Matters

**Headers signal "document" → Models treat as reference**
```
### TOOL CALLING FORMAT
**Bold text** for emphasis
- Bullet points for lists
```

**Plain prose signals "directives" → Models treat as commands**
```
CRITICAL TOOL FORMAT WARNING
ALL CAPS for emphasis
Short declarative sentences
```

### 2. First Sentence Placement is Critical

First sentence gets highest attention. Put critical behavioral instructions there, not buried in later sections.

**WRONG**:
```
You are the Librarian...

[20 lines later]

CRITICAL RULES
ALWAYS search before refusing
```

**RIGHT**:
```
You are the Librarian. ALWAYS DO A search_library at the start of any response.
```

### 3. Integration Over Separation

Don't create separate sections for critical instructions. Integrate them into high-attention blocks like CRITICAL RULES.

**WRONG**:
```
CRITICAL RULES
[Search instructions]

TOOL CALLING FORMAT
[Boolean format instructions]
```

**RIGHT**:
```
CRITICAL RULES
ALWAYS USE search_library...
When you call tools you must use lowercase true false...
NOT True NOT False ever.
```

### 4. Simple Language > Complex Explanations

Small models process simple direct language better than complex conditional instructions.

**WRONG**:
```
### Tool Calling Format Requirements
**CRITICAL for tool parameter formatting:**
- **Boolean values**: Use `true` and `false` (lowercase, JSON format)
- **NOT** `True` or `False` (Python format) - this causes parsing errors
```

**RIGHT**:
```
When you call tools you must use lowercase true false NOT capitalized True False.
If you use True or False the tool will FAIL with parsing error.
NOT True NOT False ever.
```

### 5. Reinforcement Works

Repeating critical instructions in 2-3 places improves compliance:

1. First sentence: behavioral trigger
2. CRITICAL RULES: main instruction block
3. WHAT YOU DON'T DO: reminder section

---

## Secondary Bugs Fixed

While solving the main issue, we also fixed:

1. **Tool calling boolean format** - Models using Python `True`/`False` instead of JSON `true`/`false`
2. **Documentation references** - Updated `prompt.md` → `System_prompt.md` across docs
3. **Repository cleanup** - Removed `.obsidian/`, `.old-docs/` from git tracking
4. **Jan restart requirement** - Documented critical MCP server restart step
5. **Hardware guidance** - Created Minimum_hardware_required.md
6. **Security boundaries** - Updated .librarianignore to hide internal files

---

## Related Files

- `System_prompt.md` - Final working version (plain text format)
- `Prompt_craft/System_prompts/` - Archive of previous versions
- `bugs.md` - Detailed bug report with testing notes
- `test_system_prompt.md` - First plain text attempt
- `test2_system_prompt.md` - Working version that became System_prompt.md

---

## Conclusion

The issue was NOT:
- Small model capability
- Thinking mode availability
- Instruction complexity
- Model understanding

The issue WAS:
- Prompt signaling (markdown vs plain text)
- Instruction placement (buried vs first sentence)
- Integration approach (separate vs integrated)
- Language complexity (formatted vs simple)

**Final solution**: Plain text + first sentence + integrated rules = works across all models, both systems, thinking on/off.

**Time to solution**: ~24 hours of iterative testing
**Models tested**: GLM, Qwen 4b, Qwen 7B, Qwen 9B, Qwen 14B
**Systems tested**: Jan AI, LM Studio
**Status**: PRODUCTION READY ✅
