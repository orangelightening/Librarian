#!/bin/bash
# Switch librarian MCP to use a specific library

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Usage
usage() {
    echo "Usage: $0 <library_path>"
    echo ""
    echo "Switch the librarian MCP server to use a specific library."
    echo ""
    echo "Arguments:"
    echo "  library_path    Path to the library directory"
    echo ""
    echo "Example:"
    echo "  $0 /home/peter/botany"
    exit 1
}

# Check arguments
if [ -z "$1" ]; then
    usage
fi

LIBRARY_PATH="$1"

# Validate library exists
if [ ! -d "$LIBRARY_PATH" ]; then
    echo -e "${RED}Error: Library path does not exist: $LIBRARY_PATH${NC}"
    exit 1
fi

# Validate .librarian directory exists
LIBRARIAN_DIR="$LIBRARY_PATH/.librarian"
if [ ! -d "$LIBRARIAN_DIR" ]; then
    echo -e "${RED}Error: Not a valid librarian library (missing .librarian directory)${NC}"
    exit 1
fi

# Validate config exists
CONFIG_FILE="$LIBRARIAN_DIR/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: Library config not found: $CONFIG_FILE${NC}"
    exit 1
fi

# Read library name from config
LIBRARY_NAME=$(grep -o '"library_name"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Switching to Library${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "Library: ${GREEN}$LIBRARY_NAME${NC}"
echo -e "Path:   ${GREEN}$LIBRARY_PATH${NC}"
echo ""

# Extract paths from config
CHROMA_PATH=$(grep -o '"chroma_path"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
METADATA_PATH=$(grep -o '"metadata_path"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
BACKEND=$(grep -o '"backend"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)

echo -e "${YELLOW}Library Configuration:${NC}"
echo "  ChromaDB:  $CHROMA_PATH"
echo "  Metadata:  $METADATA_PATH"
echo "  Backend:   $BACKEND"
echo ""

# Create or update mcp config for this library
MCP_CONFIG_DIR="$HOME/.config/claude"
MCP_CONFIG_FILE="$MCP_CONFIG_DIR/claude_desktop_config.json"

if [ ! -f "$MCP_CONFIG_FILE" ]; then
    echo -e "${YELLOW}Note: Claude MCP config not found at $MCP_CONFIG_FILE${NC}"
    echo "You'll need to manually update your MCP client configuration."
    echo ""
    echo "Required settings:"
    echo "  LIBRARIAN_SAFE_DIR=$LIBRARY_PATH"
    echo "  LIBRARIAN_CHROMA_PATH=$CHROMA_PATH"
    echo "  LIBRARIAN_METADATA_PATH=$METADATA_PATH"
    echo "  LIBRARIAN_BACKEND=$BACKEND"
else
    echo -e "${YELLOW}Note: MCP config automation not yet implemented${NC}"
    echo "Please update your MCP client configuration manually:"
    echo ""
    echo "Required settings:"
    echo "  LIBRARIAN_SAFE_DIR=$LIBRARY_PATH"
    echo "  LIBRARIAN_CHROMA_PATH=$CHROMA_PATH"
    echo "  LIBRARIAN_METADATA_PATH=$METADATA_PATH"
    echo "  LIBRARIAN_BACKEND=$BACKEND"
fi

echo ""
echo -e "${GREEN}✅ Library configuration ready${NC}"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "1. Restart your MCP server after updating configuration"
echo "2. Verify library is loaded: ask 'How many documents are indexed?'"
echo ""
