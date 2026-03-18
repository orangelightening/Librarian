#!/bin/bash
# Librarian Automated Validation Suite
#
# Runs systematic validation tests against library documentation
# via LM Studio HTTP API with MCP tool access.

set -e

# Configuration
LM_STUDIO_API="${LM_STUDIO_API:-http://localhost:1234/api/v1/chat}"
OUTPUT_DIR="reports/validation_$(date +%Y-%m-%d_%H%M%S)"
PARSER_SCRIPT="scripts/parse_validation.py"
RUNNER_SCRIPT="scripts/run_batch_validation.py"
WRITER_SCRIPT="scripts/write_responses.py"
REPORT_SCRIPT="scripts/generate_report.py"

echo "======================================"
echo "Librarian Automated Validation Suite"
echo "======================================"
echo ""
echo "LM Studio API: $LM_STUDIO_API"
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "✗ Error: .env file not found"
    echo "  Please create .env with LM_STUDIO_API_TOKEN"
    exit 1
fi

# Step 0: Check LM Studio API is accessible
echo "[0/7] Checking LM Studio API..."
if ! curl -s "$LM_STUDIO_API" > /dev/null 2>&1; then
    echo "✗ LM Studio API not responding at $LM_STUDIO_API"
    echo ""
    echo "Please ensure LM Studio is running and API is enabled."
    exit 1
fi
echo "✓ LM Studio API is accessible"
echo ""

# Step 1: Parse validation queries
echo "[1/7] Parsing validation queries..."
python3 $PARSER_SCRIPT
echo "✓ Queries parsed"
echo ""

# Step 2: Run batch validation
echo "[2/7] Running batch validation queries..."
python3 $RUNNER_SCRIPT
echo "✓ Batch validation complete"
echo ""

# Step 3: Create output directory
echo "[3/7] Creating output directory..."
mkdir -p "$OUTPUT_DIR/responses"
mkdir -p "$OUTPUT_DIR/metadata"
echo "✓ Output directory created: $OUTPUT_DIR"
echo ""

# Step 4: Write response files
echo "[4/7] Writing response files..."
python3 $WRITER_SCRIPT --output "$OUTPUT_DIR"
echo "✓ Responses written to $OUTPUT_DIR/responses/"
echo ""

# Step 5: Generate summary report
echo "[5/7] Generating summary report..."
python3 $REPORT_SCRIPT "$OUTPUT_DIR"
echo "✓ Report generated: $OUTPUT_DIR/summary_report.md"
echo ""

# Step 6: Display summary statistics
echo "[6/7] Validation Complete!"
echo "======================================"
echo ""
echo "Results:"
echo "  - LM Studio API: $LM_STUDIO_API"
echo "  - Output Directory: $OUTPUT_DIR"
echo "  - Summary Report: $OUTPUT_DIR/summary_report.md"
echo "  - Response Files: $(ls $OUTPUT_DIR/responses/*.md 2>/dev/null | wc -l) files"
echo ""

# Count success/errors
SUCCESS_COUNT=$(grep -c "✓ Query.*complete" "$OUTPUT_DIR/responses/"* 2>/dev/null || echo "0")
ERROR_COUNT=$(grep -c "✗ Query.*complete" "$OUTPUT_DIR/responses/"* 2>/dev/null || echo "0")

echo "Statistics:"
echo "  - Success: $SUCCESS_COUNT"
echo "  - Errors: $ERROR_COUNT"
echo ""

# Step 7: Open report if possible
echo "[7/7] Opening summary report..."
if command -v xdg-open > /dev/null; then
    xdg-open "$OUTPUT_DIR/summary_report.md" 2>/dev/null &
elif command -v open > /dev/null; then
    open "$OUTPUT_DIR/summary_report.md" 2>/dev/null &
else
    echo "Manual open: cat $OUTPUT_DIR/summary_report.md"
fi
echo ""

echo "✓ Validation complete!"
echo ""
echo "View results:"
echo "  cat $OUTPUT_DIR/summary_report.md"
echo ""
