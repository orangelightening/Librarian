# Prompt Development Roadmap

## Overview

This document outlines the specialist prompts to be developed for the Librarian MCP system. These prompts extend the base System_prompt with task-specific capabilities, transforming the Librarian from a general research assistant into a specialized technical partner.

**Philosophy:** System_prompt establishes the Librarian persona; Specialist_prompts provide targeted expertise for specific tasks.

---

## Prompt Architecture

### How Prompts Combine

```
System_prompt (base persona)
    +
Specialist_prompt (task expertise)
    =
Contextualized Librarian with specialized capabilities
```

### Integration Pattern

1. **Always start with System_prompt** - Establishes core Librarian persona
2. **Add Specialist_prompt** - Provides task-specific guidance
3. **Maintain consistency** - Specialist prompts reinforce System_prompt principles
4. **Preserve tool usage** - All specialist prompts use Librarian tools

### Example Usage

```python
# For debugging task
context = System_prompt + Debugging_prompt
# Result: Librarian with debugging expertise

# For documentation audit
context = System_prompt + Documentation_audit_prompt
# Result: Librarian with documentation validation capabilities
```

---

## Priority 1: Core Specialist Prompts

### 1. Debugging Prompt

**Purpose:** Transform Librarian into systematic code investigator and debugger

**Capabilities Needed:**
- Trace code flow across multiple files
- Identify root causes of failures
- Analyze error patterns and stack traces
- Suggest specific fixes with line numbers
- Verify fix effectiveness

**Key Behaviors:**
1. **Systematic Investigation**
   - Start with error message/stack trace
   - Trace backward through call chain
   - Identify failure point
   - Examine surrounding context
   - Check related code paths

2. **Root Cause Analysis**
   - Distinguish symptoms vs. causes
   - Identify environmental factors
   - Check configuration issues
   - Examine data flow
   - Validate assumptions

3. **Fix Verification**
   - Propose specific changes
   - Explain why fix works
   - Identify potential side effects
   - Suggest testing approach

**Prompt Structure:**
```
## Debugging Protocol

When investigating issues:
1. Gather information (errors, logs, stack traces)
2. Trace code flow using search_documents and read_document
3. Identify root cause with evidence
4. Propose specific fix with file paths and line numbers
5. Explain reasoning and potential side effects
6. Write analysis to /librarian/debug/[topic].md

## Response Format
### Issue: [problem]
### Root Cause: [specific cause with file:line references]
### Evidence: [code snippets showing the problem]
### Proposed Fix: [specific changes]
### Testing: [how to verify fix]
```

**Test Cases:**
- Document sync failures
- Search returning no results
- Chunking errors
- Permission issues
- Configuration problems

---

### 2. Contradiction Detection Prompt

**Purpose:** Identify discrepancies between documentation and implementation

**Capabilities Needed:**
- Compare documentation claims against code reality
- Find outdated documentation
- Identify missing documentation
- Detect conflicting information
- Suggest documentation updates

**Key Behaviors:**
1. **Claim Extraction**
   - Extract specific claims from documentation
   - Identify behavioral specifications
   - List documented features and parameters

2. **Reality Verification**
   - Search code for actual implementation
   - Verify documented behavior matches code
   - Check for undocumented features
   - Validate parameter descriptions

3. **Discrepancy Reporting**
   - List contradictions found
   - Cite specific code locations
   - Suggest documentation corrections
   - Prioritize by severity

**Prompt Structure:**
```
## Contradiction Detection Protocol

When validating documentation:
1. Read documentation and extract claims
2. Search code for implementation
3. Compare documented vs. actual behavior
4. Document discrepancies with evidence
5. Write report to /librarian/audit/[doc_name]_audit.md

## Report Format
### Documentation: [doc file]
### Claim: [what documentation says]
### Reality: [what code actually does]
### Discrepancy: [specific difference]
### Evidence: [code snippets]
### Suggestion: [how to fix docs]
```

**Test Cases:**
- README tool descriptions vs. actual tools
- API documentation vs. implementation
- Configuration docs vs. actual settings
- Security claims vs. actual restrictions
- Feature descriptions vs. capabilities

---

### 3. Code Review Prompt

**Purpose:** Systematic code review with focus on specific issues

**Capabilities Needed:**
- Find problematic patterns (e.g., broad exception catches)
- Identify security issues
- Detect code smells
- Suggest improvements
- Prioritize findings by severity

**Key Behaviors:**
1. **Pattern Recognition**
   - Search for known anti-patterns
   - Identify security vulnerabilities
   - Find performance issues
   - Detect maintainability concerns

2. **Contextual Analysis**
   - Understand code purpose
   - Consider project constraints
   - Assess impact of changes
   - Validate against best practices

3. **Structured Reporting**
   - Categorize findings by type
   - Prioritize by severity
   - Provide specific examples
   - Suggest concrete improvements

**Prompt Structure:**
```
## Code Review Protocol

When reviewing code:
1. Understand context and purpose
2. Search for specific patterns to investigate
3. Analyze findings with code evidence
4. Prioritize by severity and impact
5. Write report to /librarian/reviews/[topic].md

## Categories
- Security: vulnerabilities, exposure risks
- Performance: inefficiencies, bottlenecks
- Maintainability: complexity, clarity
- Correctness: bugs, edge cases
- Standards: naming, structure, conventions

## Report Format
### Category: [type]
### Severity: [critical/high/medium/low]
### Location: [file:line]
### Issue: [specific problem]
### Evidence: [code snippet]
### Recommendation: [specific fix]
### Impact: [what changes if fixed]
```

**Test Cases:**
- Exception handling patterns
- Input validation
- Error handling
- Security practices
- Code organization

---

## Priority 2: Enhancement Prompts

### 4. Documentation Audit Prompt

**Purpose:** Comprehensive documentation quality assessment

**Capabilities Needed:**
- Assess documentation completeness
- Identify missing sections
- Evaluate clarity and accuracy
- Check for consistency
- Suggest improvements

**Key Behaviors:**
1. **Completeness Check**
   - Verify all documented features exist
   - Check for undocumented features
   - Validate examples work
   - Assess coverage depth

2. **Quality Assessment**
   - Evaluate clarity
   - Check accuracy
   - Verify consistency
   - Assess organization

3. **Improvement Suggestions**
   - Identify gaps
   - Suggest additions
   - Recommend reorganization
   - Propose examples

**Prompt Structure:**
```
## Documentation Audit Protocol

When auditing documentation:
1. Read documentation thoroughly
2. Cross-reference with code implementation
3. Assess completeness, accuracy, clarity
4. Identify gaps and inconsistencies
5. Write audit report to /librarian/audit/docs_audit.md

## Audit Dimensions
- Completeness: All features covered?
- Accuracy: Claims match reality?
- Clarity: Explanations understandable?
- Consistency: No contradictions?
- Examples: Code samples work?

## Report Format
### Document: [name]
### Dimension: [completeness/accuracy/etc]
### Findings: [specific issues]
### Evidence: [examples]
### Recommendations: [specific improvements]
```

---

### 5. Dependency Tracing Prompt

**Purpose:** Track dependencies across codebase

**Capabilities Needed:**
- Trace import dependencies
- Map function call chains
- Identify circular dependencies
- Find unused code
- Visualize relationships

**Key Behaviors:**
1. **Dependency Mapping**
   - Follow import chains
   - Track function calls
   - Identify dependencies
   - Map relationships

2. **Analysis**
   - Find circular dependencies
   - Identify coupling issues
   - Detect unused code
   - Assess impact of changes

3. **Visualization**
   - Create dependency graphs
   - Show call chains
   - Highlight problem areas
   - Suggest refactoring

**Prompt Structure:**
```
## Dependency Tracing Protocol

When tracing dependencies:
1. Start with target file/function
2. Follow imports and calls using search_documents
3. Map relationships using read_document
4. Identify patterns and issues
5. Write analysis to /librarian/analysis/deps_[topic].md

## Analysis Focus
- Import chains: What depends on what?
- Call graphs: Who calls whom?
- Circular deps: Where are the loops?
- Unused code: What's never called?
- Coupling: How tightly connected?

## Report Format
### Target: [file/function]
### Dependencies: [list]
### Call Chain: [sequence]
### Issues: [circular deps, coupling]
### Recommendations: [refactoring suggestions]
```

---

### 6. Refactoring Planner Prompt

**Purpose:** Plan and document refactoring efforts

**Capabilities Needed:**
- Analyze current code structure
- Identify refactoring opportunities
- Plan step-by-step changes
- Assess risks and benefits
- Create migration guides

**Key Behaviors:**
1. **Opportunity Identification**
   - Find code smells
   - Identify duplication
   - Spot complexity hotspots
   - Detect architectural issues

2. **Planning**
   - Break down refactoring into steps
   - Order changes by dependency
   - Identify test points
   - Assess rollback options

3. **Documentation**
   - Create refactoring plan
   - Document each step
   - Explain rationale
   - Provide validation checks

**Prompt Structure:**
```
## Refactoring Planning Protocol

When planning refactoring:
1. Analyze current code structure
2. Identify improvement opportunities
3. Create detailed step-by-step plan
4. Assess risks and benefits
5. Write plan to /librarian/plans/refactor_[topic].md

## Planning Steps
1. Assessment: Current state analysis
2. Goals: What we're improving
3. Steps: Ordered changes with dependencies
4. Tests: Validation points
5. Rollback: How to undo if needed

## Report Format
### Current State: [analysis]
### Goals: [objectives]
### Step 1: [specific change]
   - Files: [what to change]
   - Changes: [specific modifications]
   - Tests: [how to verify]
   - Rollback: [how to undo]
### Risk Assessment: [potential issues]
### Expected Benefits: [improvements]
```

---

## Priority 3: Specialized Prompts

### 7. Performance Analysis Prompt

**Purpose:** Identify performance bottlenecks and optimization opportunities

**Capabilities:**
- Analyze code for inefficiencies
- Identify slow operations
- Suggest optimizations
- Benchmark suggestions
- Profile guidance

---

### 8. Security Audit Prompt

**Purpose:** Security-focused code review

**Capabilities:**
- Find security vulnerabilities
- Check input validation
- Identify exposure risks
- Suggest security improvements
- Validate security claims

---

### 9. Test Coverage Prompt

**Purpose:** Analyze test coverage and gaps

**Capabilities:**
- Identify untested code
- Suggest test cases
- Find edge cases
- Validate test quality
- Recommend testing strategy

---

### 10. Migration Guide Prompt

**Purpose:** Create migration guides for version updates

**Capabilities:**
- Compare versions
- Identify breaking changes
- Create migration steps
- Document deprecations
- Provide examples

---

## Development Workflow

### Phase 1: Core Prompts (Days 1-3)

1. **Debugging Prompt**
   - Write prompt
   - Test with known issues
   - Validate against real bugs
   - Refine based on results

2. **Contradiction Detection Prompt**
   - Write prompt
   - Test on documentation
   - Validate findings
   - Measure accuracy

3. **Code Review Prompt**
   - Write prompt
   - Test on codebase
   - Validate findings
   - Assess usefulness

### Phase 2: Enhancement Prompts (Days 4-6)

4. **Documentation Audit Prompt**
5. **Dependency Tracing Prompt**
6. **Refactoring Planner Prompt**

### Phase 3: Specialized Prompts (Days 7-10)

7. **Performance Analysis Prompt**
8. **Security Audit Prompt**
9. **Test Coverage Prompt**
10. **Migration Guide Prompt**

---

## Testing Protocol

### For Each Specialist Prompt:

1. **Write Initial Prompt**
   - Start with template structure
   - Add specific behaviors
   - Include response format

2. **Unit Test**
   - Create simple test case
   - Verify prompt works
   - Check output format

3. **Integration Test**
   - Test with System_prompt
   - Verify compatibility
   - Check tool usage

4. **Real-World Test**
   - Use on actual task
   - Assess quality
   - Measure effectiveness

5. **Iterate**
   - Refine based on results
   - Adjust behaviors
   - Improve format

6. **Document**
   - Write test results
   - Note limitations
   - Record successes

---

## Quality Criteria

### Effective Specialist Prompts Must:

✅ **Extend System_prompt** - Not replace it
✅ **Use Librarian tools** - Leverage search_library, read_document, etc.
✅ **Produce structured output** - Tables, bullets, clear sections
✅ **Cite sources** - Always reference documentation
✅ **Write reports** - Use /librarian/ workspace for outputs
✅ **Be specific** - Provide file paths, line numbers, code snippets
✅ **Explain reasoning** - Show evidence and logic
✅ **Suggest actions** - Concrete next steps

### Avoid:

❌ **Duplicating System_prompt** - Build on it, don't repeat
❌ **Ignoring tools** - Must use search_library, read_document
❌ **Vague recommendations** - Be specific with file:line references
❌ **Missing citations** - Always cite sources
❌ **No output** - Must write analysis to /librarian/

---

## File Organization

### Prompt Files:
```
Prompt_craft/Specialist_prompts/
├── debugging_prompt.md
├── contradiction_detection_prompt.md
├── code_review_prompt.md
├── documentation_audit_prompt.md
├── dependency_tracing_prompt.md
├── refactoring_planner_prompt.md
├── performance_analysis_prompt.md
├── security_audit_prompt.md
├── test_coverage_prompt.md
└── migration_guide_prompt.md
```

### Test Results:
```
librarian/reports/specialist_prompt_tests/
├── debugging_test_YYYYMMDD/
├── contradiction_detection_test_YYYYMMDD/
├── code_review_test_YYYYMMDD/
└── [etc.]
```

---

## Success Metrics

### For Each Specialist Prompt:

- **Accuracy** - Findings are correct
- **Completeness** - Doesn't miss obvious issues
- **Specificity** - Provides file:line references
- **Actionability** - Suggests concrete fixes
- **Clarity** - Easy to understand output
- **Efficiency** - Uses tools appropriately

### Overall Success:

- **10 specialist prompts** developed and tested
- **80%+ accuracy** on test cases
- **Usable output** - Real-world value
- **Integrated** - Works with System_prompt
- **Documented** - Test results and limitations known

---

## Next Steps

1. **Start with Debugging Prompt** (highest value, most used)
2. **Test thoroughly** before moving to next
3. **Document findings** as you go
4. **Iterate based on results**
5. **Build prompt library** over time

**Goal:** By end of Day 10, have 10 tested specialist prompts ready for production use.

---

*Last Updated: 2026-03-20*
*Status: Planning - Ready to begin development*
