#!/bin/bash
# Generate Jan MCP configuration for a librarian library

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    echo "Usage: $0 <library_path> <mcp_name>"
    echo ""
    echo "Generate Jan MCP configuration for a library."
    echo ""
    echo "Arguments:"
    echo "  library_path    Path to the library directory"
    echo "  mcp_name        Name for the MCP server (e.g., botany_librarian)"
    echo ""
    echo "Example:"
    echo "  $0 /home/peter/botany botany_librarian"
    exit 1
}

if [ -z "$1" ] || [ -z "$2" ]; then
    usage
fi

LIBRARY_PATH="$1"
MCP_NAME="$2"

# Validate library exists
if [ ! -d "$LIBRARY_PATH" ]; then
    echo "Error: Library path does not exist: $LIBRARY_PATH"
    exit 1
fi

LIBRARIAN_DIR="$LIBRARY_PATH/.librarian"
if [ ! -d "$LIBRARIAN_DIR" ]; then
    echo "Error: Not a valid librarian library (missing .librarian directory)"
    exit 1
fi

CONFIG_FILE="$LIBRARIAN_DIR/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Library config not found: $CONFIG_FILE"
    exit 1
fi

# Extract paths from config
LIBRARY_ROOT=$(grep -o '"library_root"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
CHROMA_PATH=$(grep -o '"chroma_path"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
METADATA_PATH=$(grep -o '"metadata_path"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
BACKEND=$(grep -o '"backend"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)

LIBRARIAN_MCP_DIR="/home/peter/development/librarian-mcp"
PYTHON_BIN="$LIBRARIAN_MCP_DIR/venv/bin/python"
MCP_SCRIPT="$LIBRARIAN_MCP_DIR/mcp_server/librarian_mcp.py"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Jan MCP Configuration${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "MCP Name:     ${GREEN}$MCP_NAME${NC}"
echo -e "Library:      ${GREEN}$LIBRARY_PATH${NC}"
echo ""

# Generate JSON config
echo -e "${YELLOW}Jan MCP Configuration (JSON):${NC}"
echo ""
echo '{'
echo '  "mcpServers": {'
echo "    \"$MCP_NAME\": {"
echo '      "command": "'"$PYTHON_BIN"'",'
echo '      "args": ["'"$MCP_SCRIPT"'"],'
echo '      "env": {'
echo "        \"LIBRARIAN_SAFE_DIR\": \"$LIBRARY_ROOT\","
echo "        \"LIBRARIAN_CHROMA_PATH\": \"$CHROMA_PATH\","
echo "        \"LIBRARIAN_METADATA_PATH\": \"$METADATA_PATH\","
echo "        \"LIBRARIAN_BACKEND\": \"$BACKEND\""
echo '      }'
echo '    }'
echo '  }'
echo '}'

echo ""
echo -e "${YELLOW}Setup Instructions:${NC}"
echo ""
echo "1. Open Jan Settings"
echo "2. Go to MCP Servers"
echo "3. Add new MCP server with name: $MCP_NAME"
echo "4. Use configuration above"
echo "5. Create/use assistant: botany_librarian"
echo "6. Assign botany_librarian assistant to $MCP_NAME MCP server"
echo ""
echo -e "${GREEN}✅ Configuration generated!${NC}"
echo ""
