# Prompt Engineering: Structure Over Length

## The Challenge

When running the same validation queries across two different models, we observed dramatically different response patterns:

| Model | Type | Params | Response Style | Size |
|-------|------|--------|----------------|------|
| **GLM-4.7** | LLM | 355B (MoE) | Narrative, explanatory | 2-3x larger |
| **Qwen 3.5** | SLM | 4B (8-bit) | Concise, reference-style | Compact |

**Problem:** GLM-4.7 was producing 2-3x more tokens than Qwen, making responses harder to scan and more expensive to process. Yet both models were accurate and well-cited.

**Challenge:** How to make one prompt work well for both models when they have opposite weaknesses?

---

## The Approach: Structure-Based Prompting

Instead of trying to control verbosity directly (which risks truncating important information), we controlled **format**.

### Key Insight
> **Structure channels verbosity into scannable format.**

Rather than saying "be concise" or "be thorough," we specified **how information should be presented**:

### Structure Requirements Added
- **### Section headers** for organization
- **Tables** for structured data (tools, parameters, comparisons)
- **Bullet points** for lists and features
- **Code blocks** for examples and workflows
- **Bold** for key terms and emphasis

### Content Guidelines
For each tool/feature listed:
1. **What it does** (1 sentence)
2. **Why it matters** (1 sentence)
3. **How it's used** (brief example)

This forced both models into the same presentation format while letting them be themselves.

---

## The Results

### Size Convergence

| Query | Before (GLM:Qwen ratio) | After (GLM:Qwen ratio) | GLM Reduction |
|-------|-------------------------|------------------------|---------------|
| 7 | 2.4x larger | **1.0x (identical!)** | 65% ↓ |
| 8 | 3.0x larger | 1.2x larger | 70% ↓ |
| 9 | 2.9x larger | 1.2x larger | 55% ↓ |

**GLM-4.7 reduced token usage by 55-70% while maintaining quality.**

### Quality Preservation

Both models maintained:
- ✅ All citations intact
- ✅ Complete information coverage
- ✅ Practical examples included
- ✅ Technical details preserved
- ✅ Accuracy unchanged

### Usability Improvement

**Before:**
- GLM: Narrative paragraphs, hard to scan
- Qwen: Terse, sometimes missing context

**After:**
- Both: Structured with headers, tables, bullets
- Both: Scannable and reference-friendly
- Both: Consistent presentation

---

## Why This Works

### For Verbose Models (GLM-4.7)

**Problem:** Tends to over-explain with narrative paragraphs
**Solution:** Structure channels verbosity into organized format
**Result:** Comprehensive but scannable

Example transformation:
```markdown
❌ Before: "The search_library tool is a very important tool that allows
you to search across all the documents in your library using semantic
search which means it understands the meaning..." (wall of text)

✅ After: Table with Purpose/Value/Example columns (structured, scannable)
```

### For Concise Models (Qwen 3.5)

**Problem:** Sometimes too terse, misses "why it matters"
**Solution:** Required structure forces explanation of value
**Result:** Concise but complete

Example transformation:
```markdown
❌ Before: "search_library(query, limit) - Search documents"

✅ After:
| Tool | Purpose | Value | Example |
|------|---------|-------|---------|
| search_library | Semantic search | Finds relevant info beyond keywords | search_library("error patterns") |
```

---

## Key Takeaways

### 1. Structure > Length Controls
Don't tell models "be concise" or "be thorough."
Tell them **"use this format"** and let verbosity organize itself.

### 2. Tables Force Conciseness
When models must fit information into table cells, they self-edit.
This is more effective than length limits.

### 3. Templates Enable Consistency
Both models followed the same structural requirements,
producing consistent output despite different architectural approaches.

### 4. Format Requirements Add Depth
Requiring "What/Why/How" for each item ensures concise models
don't skip important context.

---

## Practical Impact

### Token Savings
- **GLM-4.7**: Using 1/3 the tokens for same information
- **Cost reduction**: Fewer tokens = lower API costs
- **Performance**: Faster processing and response times

### User Experience
- **Scannability**: Headers, tables, bullets make answers easy to navigate
- **Consistency**: Both models produce similar format regardless of underlying style
- **Reference value**: Structured output works better as documentation

### Model Flexibility
- **Same prompt**: Works for both SLM and LLM
- **No trade-offs**: Both models maintain their strengths while minimizing weaknesses
- **Future-proof**: Structure requirements work across model families

---

## The Formula

> **One prompt + Structure requirements = Consistent quality across model sizes**

Whether using a 4B SLM (Qwen) or 355B LLM (GLM-4.7), structure-based prompting
ensures consistent, scannable, well-organized responses.

### Key Requirements
1. Specify format (headers, tables, bullets)
2. Require value explanation ("why it matters")
3. Provide templates for common question types
4. Let models handle their own depth

### Avoid
1. Length limits (risk truncation)
2. "Be concise" (too vague)
3. "Be thorough" (too vague)
4. Model-specific instructions (breaks single-prompt goal)

---

## Conclusion

By focusing on **how information is presented** rather than **how much information**,
we achieved:

- ✅ 55-70% reduction in verbose model output
- ✅ Perfect convergence on some queries (identical file sizes)
- ✅ Improved usability for end users
- ✅ Token savings without quality loss
- ✅ Consistent structure across model architectures

**Structure over length. One prompt to rule them all.**

---

*Validation run: Queries 7-9 on librarian-mcp self-validation suite*
*Models: GLM-4.7 (355B MoE) vs Qwen 3.5 (4B 8-bit quantized)*
*Prompt: one_prompt.md with structure-based formatting requirements*
