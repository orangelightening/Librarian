#!/bin/bash
# Create a new librarian library with isolated data and configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Usage function
usage() {
    echo "Usage: $0 <library_path> [options]"
    echo ""
    echo "Arguments:"
    echo "  library_path    Path to the library directory (e.g., /home/peter/botany)"
    echo ""
    echo "Options:"
    echo "  --name NAME         Library name (default: directory basename)"
    echo "  --extensions EXTS   Comma-separated extensions (default: .md,.pdf)"
    echo "  --backend BACKEND   Backend to use: chonkie or chroma (default: chonkie)"
    echo ""
    echo "Example:"
    echo "  $0 /home/peter/botany --name botany --extensions .md,.pdf"
    exit 1
}

# Check arguments
if [ -z "$1" ]; then
    usage
fi

LIBRARY_PATH="$1"
shift

# Parse options
LIBRARY_NAME=""
EXTENSIONS=".md,.pdf"
BACKEND="chonkie"

while [ $# -gt 0 ]; do
    case $1 in
        --name)
            LIBRARY_NAME="$2"
            shift 2
            ;;
        --extensions)
            EXTENSIONS="$2"
            shift 2
            ;;
        --backend)
            BACKEND="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate library path
if [ ! -d "$LIBRARY_PATH" ]; then
    echo -e "${RED}Error: Library path does not exist: $LIBRARY_PATH${NC}"
    echo "Please create the directory first: mkdir -p $LIBRARY_PATH"
    exit 1
fi

# Resolve absolute path
LIBRARY_PATH=$(cd "$LIBRARY_PATH" && pwd)

# Default library name
if [ -z "$LIBRARY_NAME" ]; then
    LIBRARY_NAME=$(basename "$LIBRARY_PATH")
fi

# Configuration
LIBRARIAN_DIR="$LIBRARY_PATH/.librarian"
CONFIG_FILE="$LIBRARIAN_DIR/config.json"
IGNORE_FILE="$LIBRARIAN_DIR/.librarianignore"
CHROMA_PATH="$LIBRARIAN_DIR/chroma_db"
METADATA_PATH="$LIBRARIAN_DIR/metadata"
SANDBOX_DIR="$LIBRARIAN_DIR/sandbox"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Creating Librarian Library${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "Library path:    ${GREEN}$LIBRARY_PATH${NC}"
echo -e "Library name:    ${GREEN}$LIBRARY_NAME${NC}"
echo -e "Extensions:      ${GREEN}$EXTENSIONS${NC}"
echo -e "Backend:         ${GREEN}$BACKEND${NC}"
echo ""

# Confirm
read -p "Create library with these settings? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo -e "${RED}Aborted${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 1: Creating directory structure...${NC}"
echo "----------------------------------------------------------------------"

# Create .librarian directory structure
mkdir -p "$CHROMA_PATH"
mkdir -p "$METADATA_PATH"
mkdir -p "$SANDBOX_DIR/reports"

echo -e "${GREEN}✓ Created .librarian directory structure${NC}"

echo ""
echo -e "${YELLOW}Step 2: Creating configuration file...${NC}"
echo "----------------------------------------------------------------------"

# Create config.json
cat > "$CONFIG_FILE" << EOF
{
  "library_name": "$LIBRARY_NAME",
  "library_root": "$LIBRARY_PATH",
  "librarian_dir": "$LIBRARIAN_DIR",
  "allowed_extensions": [$(echo "$EXTENSIONS" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')],
  "chroma_path": "$CHROMA_PATH",
  "metadata_path": "$METADATA_PATH",
  "sandbox_path": "$SANDBOX_DIR",
  "backend": "$BACKEND",
  "chunk_size": 1000,
  "created": "$(date -Iseconds)"
}
EOF

echo -e "${GREEN}✓ Created config.json${NC}"

echo ""
echo -e "${YELLOW}Step 3: Creating .librarianignore file...${NC}"
echo "----------------------------------------------------------------------"

# Create default .librarianignore
cat > "$IGNORE_FILE" << 'EOF'
# Librarian ignore patterns for this library

# Security - NEVER index these
.env
*.env
.env.*
credentials.*
*.key
*.pem
id_rsa
id_ed25519

# Development
venv/
.venv/
virtualenv/
__pycache__/
*.pyc

# Version control
.git/
.svn/
.hg/

# Build artifacts
dist/
build/
target/
*.egg-info/
.eggs/

# Data & Databases (don't index the database!)
chroma_db/
metadata/

# Logs & Temp
*.log
logs/
*.tmp
tmp/
temp/
.cache/

# Binary & Media
*.zip
*.tar
*.tar.gz
*.exe
*.dll
*.so

# Obsidian (if using as vault)
.obsidian/
.obsidian.plugins/

# Librarian's own data
.librarian/

# Add your custom exclusions below
EOF

echo -e "${GREEN}✓ Created .librarianignore${NC}"

echo ""
echo -e "${YELLOW}Step 4: Creating README in librarian sandbox...${NC}"
echo "----------------------------------------------------------------------"

# Create README in sandbox
cat > "$SANDBOX_DIR/README.md" << EOF
# Librarian Sandbox

This directory is the librarian's workspace for writing reports and analysis.

**Librarian can write here**, but cannot write elsewhere in the library.

## What Goes Here

- Analysis reports
- Search results summaries
- Code change suggestions
- Debugging diagnostics
- Task delegation outputs

## Safety

- All writes are limited to this directory
- File size limit: 100KB per file
- Critical file protection enabled
- All operations logged

## Reviews

You review files here before applying changes to your main library.
EOF

echo -e "${GREEN}✓ Created sandbox README${NC}"

echo ""
echo -e "${YELLOW}Step 5: Creating library management scripts...${NC}"
echo "----------------------------------------------------------------------"

# Create library-specific rebuild script
cat > "$LIBRARIAN_DIR/rebuild.sh" << EOF
#!/bin/bash
# Rebuild script for $LIBRARY_NAME library

LIBRARY_PROJECT_DIR="/home/peter/development/librarian-mcp"

echo "Rebuilding $LIBRARY_NAME library..."

# Set library-specific environment
export LIBRARIAN_CHROMA_PATH="$CHROMA_PATH"
export LIBRARIAN_METADATA_PATH="$METADATA_PATH"
export LIBRARIAN_BACKEND="$BACKEND"

cd "\$LIBRARY_PROJECT_DIR"
./scripts/clear_and_rebuild.sh
EOF

chmod +x "$LIBRARIAN_DIR/rebuild.sh"

echo -e "${GREEN}✓ Created rebuild script${NC}"

echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}✅ Library Created Successfully!${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "Library details:"
echo -e "  Name:       ${GREEN}$LIBRARY_NAME${NC}"
echo -e "  Path:       ${GREEN}$LIBRARY_PATH${NC}"
echo -e "  Config:     ${GREEN}$CONFIG_FILE${NC}"
echo -e "  Extensions: ${GREEN}$EXTENSIONS${NC}"
echo -e "  Backend:    ${GREEN}$BACKEND${NC}"
echo ""
echo -e "Data locations:"
echo -e "  ChromaDB:   ${GREEN}$CHROMA_PATH${NC}"
echo -e "  Metadata:   ${GREEN}$METADATA_PATH${NC}"
echo -e "  Sandbox:    ${GREEN}$SANDBOX_DIR${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Add documents to: $LIBRARY_PATH"
echo "2. Rebuild index: $LIBRARIAN_DIR/rebuild.sh"
echo "3. Update MCP server config to point to this library"
echo ""
echo -e "${BLUE}Note: To use this library with the MCP server, update the config:${NC}"
echo "  Set LIBRARIAN_SAFE_DIR=$LIBRARY_PATH"
echo "  Set LIBRARIAN_CHROMA_PATH=$CHROMA_PATH"
echo "  Set LIBRARIAN_METADATA_PATH=$METADATA_PATH"
echo ""
