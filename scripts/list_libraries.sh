#!/bin/bash
# List all librarian libraries

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Librarian Libraries${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Find all .librarian directories
FOUND=0

# Use find to locate all librarian directories, avoid duplicates
find "$HOME" /home/peter 2>/dev/null -maxdepth 3 -type d -name ".librarian" | sort -u | while read -r librarian_dir; do
    search_path="$(dirname "$librarian_dir")"

    if [ -f "$search_path/.librarian/config.json" ]; then
        FOUND=1
        CONFIG="$search_path/.librarian/config.json"

        # Extract info
        NAME=$(grep -o '"library_name"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG" | cut -d'"' -f4)
        EXTENSIONS=$(grep -o '"allowed_extensions"[[:space:]]*:[[:space:]]*\[[^]]*\]' "$CONFIG" | sed 's/","/, /g' | tr -d '["]')
        BACKEND=$(grep -o '"backend"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG" | cut -d'"' -f4)

        # Count documents
        METADATA_DIR=$(grep -o '"metadata_path"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG" | cut -d'"' -f4)
        if [ -f "$METADATA_DIR/index.json" ]; then
            COUNT=$(jq 'length' "$METADATA_DIR/index.json" 2>/dev/null || echo "0")
        else
            COUNT="0"
        fi

        echo -e "${GREEN}Library: $NAME${NC}"
        echo "  Path:        $search_path"
        echo "  Documents:   $COUNT"
        echo "  Extensions:  $EXTENSIONS"
        echo "  Backend:     $BACKEND"
        echo ""
    fi
done

if [ $FOUND -eq 0 ]; then
    echo -e "${YELLOW}No libraries found.${NC}"
    echo ""
    echo "Create a library with:"
    echo "  ./scripts/create_library.sh /path/to/library"
else
    echo -e "${YELLOW}Switch libraries:${NC}"
    echo "  ./scripts/use_library.sh /path/to/library"
    echo ""
    echo -e "${YELLOW}Generate Jan MCP config:${NC}"
    echo "  ./scripts/generate_jan_config.sh /path/to/library mcp_name"
fi

echo ""
