# Static Analysis Architecture

**Created**: 2026-03-21
**Status**: Documented design, not yet implemented

---

## Overview

This document describes the architecture for integrating static code analysis tools with the Librarian MCP Server. The approach separates **analysis execution** (run by scripts/tools) from **semantic search** (provided by Librarian MCP).

---

## Architecture Principle

**Librarian MCP provides semantic search of validated analysis reports, not code analysis itself.**

### Why This Approach?

1. **Models hallucinate during code analysis** - Proven by testing (see glm_code_analysis.md)
2. **Static analysis tools are reliable** - Purpose-built for finding specific issues
3. **Human verification ensures accuracy** - Prevents false positives in reports
4. **Semantic search adds value** - Models can search and retrieve relevant findings

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│  Static Analysis Tools (Executed by Scripts)          │
├──────────────────────────────────────────────────────┤
│  Tool              | Purpose                          │
│  ────────────────────────────────────────────────────│
│  ruff              | Linting, style, code quality     │
│  mypy              | Type checking                    │
│  bandit            | Security vulnerability scanning   │
│  pytest            | Test execution                   │
│  pytest-cov        | Test coverage measurement         │
│  pylint            | Additional linting rules         │
└──────────────┬─────────────────────────────────────────┘
               │
               │ scripts/run_static_analysis.sh
               │
               ▼
        ┌──────────────┐
        │  Verification │ ← Human (Claude) validates findings
        └──────┬───────┘
               │
               ▼
┌──────────────────────────────────────────────────────┐
│  /librarian/reports/ (Human-Readable Reports)         │
├──────────────────────────────────────────────────────┤
│  ruff_report.md              Linting issues           │
│  bandit_report.md            Security findings        │
│  type_check_report.md        Type errors              │
│  test_results.md             Test execution results   │
│  coverage_report.md          Test coverage percentage │
└──────────────┬─────────────────────────────────────────┘
               │
               │ Indexed by Librarian MCP
               │
               ▼
┌──────────────────────────────────────────────────────┐
│  Librarian MCP (Semantic Search Layer)               │
├──────────────────────────────────────────────────────┤
│  User queries:                                       │
│  - "What security issues did bandit find?"           │
│  - "Show me all type errors in document_manager"     │
│  - "What's the test coverage for backend code?"      │
│  - "Are there any high-severity linting issues?"     │
└──────────────────────────────────────────────────────┘
```

---

## Implementation

### Step 1: Install Analysis Tools

```bash
# Add to requirements.txt or install separately
pip install ruff mypy bandit pytest pytest-cv pylint
```

### Step 2: Create Analysis Script

**File**: `scripts/run_static_analysis.sh`

```bash
#!/bin/bash
# Run all static analysis tools and generate reports

set -e

REPORT_DIR="librarian/reports"
mkdir -p "$REPORT_DIR"

echo "======================================"
echo "Running Static Analysis"
echo "======================================"

# Linting with ruff
echo "[1/5] Running ruff..."
ruff check mcp_server/ > "$REPORT_DIR/ruff_report.txt" 2>&1 || true
# Convert to markdown
echo "# Ruff Linting Report" > "$REPORT_DIR/ruff_report.md"
echo "" >> "$REPORT_DIR/ruff_report.md"
cat "$REPORT_DIR/ruff_report.txt" >> "$REPORT_DIR/ruff_report.md"

# Type checking with mypy
echo "[2/5] Running mypy..."
mypy mcp_server/ > "$REPORT_DIR/type_check_report.txt" 2>&1 || true
echo "# Type Check Report (mypy)" > "$REPORT_DIR/type_check_report.md"
echo "" >> "$REPORT_DIR/type_check_report.md"
cat "$REPORT_DIR/type_check_report.txt" >> "$REPORT_DIR/type_check_report.md"

# Security scanning with bandit
echo "[3/5] Running bandit..."
bandit -r mcp_server/ -f txt > "$REPORT_DIR/bandit_report.txt" 2>&1 || true
echo "# Security Scan Report (bandit)" > "$REPORT_DIR/bandit_report.md"
echo "" >> "$REPORT_DIR/bandit_report.md"
cat "$REPORT_DIR/bandit_report.txt" >> "$REPORT_DIR/bandit_report.md"

# Test execution
echo "[4/5] Running tests..."
pytest --cov=mcp_server --cov-report=term > "$REPORT_DIR/test_results.txt" 2>&1 || true
echo "# Test Results" > "$REPORT_DIR/test_results.md"
echo "" >> "$REPORT_DIR/test_results.md"
cat "$REPORT_DIR/test_results.txt" >> "$REPORT_DIR/test_results.md"

# Additional linting with pylint (optional)
echo "[5/5] Running pylint..."
pylint mcp_server/ > "$REPORT_DIR/pylint_report.txt" 2>&1 || true
echo "# Pylint Report" > "$REPORT_DIR/pylint_report.md"
echo "" >> "$REPORT_DIR/pylint_report.md"
cat "$REPORT_DIR/pylint_report.txt" >> "$REPORT_DIR/pylint_report.md"

echo ""
echo "======================================"
echo "Analysis complete!"
echo "Reports saved to: $REPORT_DIR"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Review reports for accuracy"
echo "2. Fix critical issues"
echo "3. Rebuild librarian index: ./scripts/clear_and_rebuild.sh"
```

### Step 3: Make Script Executable

```bash
chmod +x scripts/run_static_analysis.sh
```

### Step 4: Run Analysis

```bash
# From project root
./scripts/run_static_analysis.sh
```

### Step 5: Review and Verify

**Important**: Human review is critical before rebuilding index:

1. Check each report for false positives
2. Verify severity levels are appropriate
3. Remove or annotate any findings that are not actual issues
4. Add context or explanations where helpful

### Step 6: Rebuild Librarian Index

```bash
./scripts/clear_and_rebuild.sh
```

Now the analysis reports are searchable via Librarian MCP.

---

## Usage Examples

After reports are generated and indexed:

### Example 1: Security Review
```
User: "What security issues did bandit find?"
Librarian: Retrieves relevant sections from bandit_report.md
```

### Example 2: Type Errors
```
User: "Show me all type errors in document_manager.py"
Librarian: Searches type_check_report.md for document_manager references
```

### Example 3: Test Coverage
```
User: "What's the test coverage for the backend module?"
Librarian: Retrieves coverage statistics from test_results.md
```

### Example 4: Linting Issues
```
User: "Are there any high-severity ruff issues in the tools directory?"
Librarian: Searches ruff_report.md for tools/ directory issues
```

---

## Configuration

### Ruff Configuration

**File**: `pyproject.toml` or `ruff.toml`

```toml
[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py
```

### MyPy Configuration

**File**: `mypy.ini` or `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "chromadb.*"
ignore_missing_imports = true
```

### Bandit Configuration

**File**: `.bandit` or command-line args

```yaml
# .bandit
exclude_dirs:
  - '/venv'
  - '/tests'
skips:
  - 'B101'  # Allow assert statements (used in tests)
```

---

## Report Format

Each report should follow this structure for optimal searchability:

```markdown
# [Tool Name] Report

**Date**: [ISO 8601 date]
**Tool Version**: [version]
**Scope**: [files/directories analyzed]

---

## Executive Summary

[Brief overview of findings]

- Total Issues: [count]
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]

---

## Findings by Severity

### Critical Issues

[Detailed findings]

### High Severity Issues

[Detailed findings]

### Medium Severity Issues

[Detailed findings]

### Low Severity Issues

[Detailed findings]

---

## Files Analyzed

[List of files with issue counts per file]

---

## Recommendations

[Prioritized action items]
```

---

## Best Practices

### DO:
✅ Run analysis before commits
✅ Review reports for false positives
✅ Fix critical issues immediately
✅ Keep reports in version control
✅ Rebuild index after report updates
✅ Use consistent report formats

### DON'T:
❌ Let models generate code analysis (they hallucinate)
❌ Commit reports without human verification
❌ Ignore security findings
❌ Use reports as the only quality measure (complement with tests)
❌ Let reports grow stale (regenerate regularly)

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install ruff mypy bandit pytest pytest-cov
      - name: Run ruff
        run: ruff check mcp_server/
      - name: Run mypy
        run: mypy mcp_server/
      - name: Run bandit
        run: bandit -r mcp_server/
      - name: Run tests
        run: pytest --cov=mcp_server
```

---

## Maintenance

### Regular Tasks

1. **Weekly**: Run full analysis suite
2. **Before releases**: Comprehensive analysis and review
3. **After major changes**: Targeted analysis on changed files
4. **Monthly**: Update tool versions and configurations

### Report Cleanup

- Remove outdated reports (keep last 3 months)
- Archive historical reports separately if needed for trend analysis
- Maintain index of reports by date

---

## Troubleshooting

### Issue: Reports not found by librarian

**Cause**: Librarian index not rebuilt after adding reports

**Solution**:
```bash
./scripts/clear_and_rebuild.sh
```

### Issue: Too many false positives

**Cause**: Tool configuration too strict

**Solution**: Adjust tool config files (ruff.toml, mypy.ini, etc.)

### Issue: Analysis takes too long

**Cause**: Full repository analysis on every run

**Solution**: Add incremental analysis option
```bash
# Only analyze changed files
git diff --name-only HEAD~1 | grep '\.py$' | xargs ruff check
```

---

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
- [glm_code_analysis.md](glm_code_analysis.md) - Example of model hallucination in code analysis
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development workflow (if exists)

---

*This architecture prioritizes accuracy over automation. Human verification prevents false positives while semantic search makes findings easily accessible.*
