#!/bin/bash
# Script to check and restart Librarian MCP servers
# Note: MCP servers with stdio transport must be restarted through Jan

echo "================================"
echo "Librarian MCP Server Status"
echo "================================"
echo ""

# Check running librarian processes
echo "📊 Running Librarian MCP Servers:"
ps aux | grep "python.*librarian_mcp" | grep -v grep | while read line; do
    pid=$(echo "$line" | awk '{print $2}')
    echo "  PID: $pid"
    echo "  Command: $line"
    echo ""
done

if ! ps aux | grep "python.*librarian_mcp" | grep -v grep > /dev/null; then
    echo "  No librarian MCP servers running"
fi

echo ""
echo "================================"
echo "How to Restart Librarian MCP"
echo "================================"
echo ""
echo "MCP servers with stdio transport run under Jan (or LM Studio)."
echo "To restart the server with updated code:"
echo ""
echo "Option 1: Toggle in Jan (Recommended)"
echo "  1. Open Jan → Settings → MCP Servers"
echo "  2. Find 'librarian mcp for dev library'"
echo "  3. Toggle 'active' from true → false → true"
echo "  4. Jan will restart the server automatically"
echo ""
echo "Option 2: Restart Jan"
echo "  1. Close Jan completely"
echo "  2. Reopen Jan"
echo "  3. Server will start with updated code"
echo ""
echo "================================"
echo "Recent Changes (v0.3.0)"
echo "================================"
echo ""
echo "✅ Fixed: Environment variables now take precedence"
echo "✅ Fixed: Write directory changed to .librarian/sandbox/"
echo "✅ Fixed: Path validation rejects insecure paths"
echo ""
echo "Expected write location for dev library:"
echo "  /home/peter/development/librarian-mcp/.librarian/sandbox/"
echo ""
echo "Expected write location for botany library:"
echo "  /home/peter/botany/.librarian/sandbox/"
echo ""
