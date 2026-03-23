#!/bin/bash
# Test script for write_document security validation

echo "================================"
echo "Testing write_document Security"
echo "================================"
echo ""

# Check if librarian server is running
echo "📊 Checking Librarian MCP Server Status:"
if ps aux | grep -q "[p]ython.*librarian_mcp"; then
    echo "  ✅ Librarian MCP server is running"
    echo ""
    echo "⚠️  Remember to toggle the server OFF/ON in Jan to load updated code!"
else
    echo "  ❌ Librarian MCP server is NOT running"
    echo ""
    echo "Start it in Jan → Settings → MCP Servers → Toggle librarian mcp for dev library"
fi

echo ""
echo "================================"
echo "Test Cases for write_document"
echo "================================"
echo ""

echo "✅ VALID PATHS (Should SUCCEED):"
echo "  1. write_document('test.md', 'Hello world')"
echo "     → Expected: .librarian/test.md"
echo ""
echo "  2. write_document('sandbox/test.md', 'Hello world')"
echo "     → Expected: .librarian/sandbox/test.md"
echo ""
echo "  3. write_document('reports/analysis.md', 'Hello world')"
echo "     → Expected: .librarian/reports/analysis.md"
echo ""

echo "❌ INVALID PATHS (Should FAIL with clear error):"
echo "  1. write_document('/home/peter/botany/test.md', 'Hello')"
echo "     → Expected: ERROR - 'Path looks like absolute path'"
echo ""
echo "  2. write_document('../escape.md', 'Hello')"
echo "     → Expected: ERROR - 'Path cannot contain ..'"
echo ""
echo "  3. write_document('/.librarian/sandbox/file.md', 'Hello')"
echo "     → Expected: ERROR - 'Path cannot start with .'"
echo ""

echo "================================"
echo "After Testing"
echo "================================"
echo ""
echo "Check where files actually were written:"
echo "  ls -la /home/peter/development/librarian-mcp/.librarian/"
echo ""
echo "Expected valid files:"
echo "  .librarian/test.md"
echo "  .librarian/sandbox/test.md"
echo "  .librarian/reports/analysis.md"
echo ""
echo "Should NOT exist:"
echo "  .librarian/home/  (directory structure from bad path)"
echo ""
