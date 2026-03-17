#!/bin/bash
#
# Clear and Rebuild Librarian Library
#
# This script completely clears the database and rebuilds it from scratch.
# Useful for:
# - Switching backends (ChromaDB <-> Chonkie)
# - Starting fresh with new .librarianignore rules
# - Database corruption recovery
# - Testing different chunking strategies

set -e  # Exit on error

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "======================================================================"
echo "Clear and Rebuild Librarian Library"
echo "======================================================================"
echo "Project: $PROJECT_ROOT"
echo ""

# Check if LIBRARIAN_BACKEND is set
if [ -z "$LIBRARIAN_BACKEND" ]; then
    echo "⚠️  LIBRARIAN_BACKEND not set (defaulting to chroma)"
    echo "💡 Set with: export LIBRARIAN_BACKEND=chonkie"
    echo ""
fi

# Confirm destruction
read -p "⚠️  This will DELETE all documents in the library. Continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Aborted"
    exit 1
fi

echo ""
echo "Step 1: Clearing database..."
echo "----------------------------------------------------------------------"

# Remove database directories
if [ -d "$PROJECT_ROOT/chroma_db" ]; then
    echo "Removing chroma_db..."
    rm -rf "$PROJECT_ROOT/chroma_db"
fi

if [ -d "$PROJECT_ROOT/metadata" ]; then
    echo "Removing metadata..."
    rm -rf "$PROJECT_ROOT/metadata"
fi

echo "✅ Database cleared"
echo ""

echo "Step 2: Rebuilding library..."
echo "----------------------------------------------------------------------"
echo "Backend: ${LIBRARIAN_BACKEND:-chroma (default)}"
echo ""

# Activate virtual environment
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
else
    echo "❌ Virtual environment not found at $PROJECT_ROOT/venv"
    exit 1
fi

# Run rebuild script
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
python3 "$SCRIPT_DIR/rebuild_library.py"

echo ""
echo "======================================================================"
echo "✅ Library rebuild complete!"
echo "======================================================================"
echo ""
echo "📚 Your library has been rebuilt with:"
echo "   Backend: ${LIBRARIAN_BACKEND:-chroma (default)}"
echo "   Database: $PROJECT_ROOT/chroma_db"
echo "   Metadata: $PROJECT_ROOT/metadata"
echo ""
echo "💡 Restart your MCP server to use the new library:"
echo "   ./setup_mcp.sh"
echo ""
