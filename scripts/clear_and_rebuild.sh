#!/bin/bash
#
# Clear and Rebuild Librarian Library
#
# This script clears the search index (ChromaDB + metadata) and rebuilds it from source documents.
# **Source documents are never deleted** - only the search index is cleared and rebuilt.
# Useful for:
# - Switching backends (ChromaDB <-> Chonkie)
# - Starting fresh with new .librarianignore rules
# - Database corruption recovery
# - Testing different chunking strategies
# - Updating index after major documentation changes

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

# Confirm rebuild
read -p "⚠️  This will clear the search index and rebuild it from source documents. Continue? (yes/no): " confirm
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
echo "✅ Search index rebuild complete!"
echo "======================================================================"
echo ""
echo "📚 Your search index has been rebuilt:"
echo "   Backend: ${LIBRARIAN_BACKEND:-chroma (default)}"
echo "   Database: $PROJECT_ROOT/chroma_db"
echo "   Metadata: $PROJECT_ROOT/metadata"
echo "   Source documents: untouched ✓"
echo ""
echo "💡 Restart your MCP server to use the updated index:"
echo "   ./setup_mcp.sh"
echo ""
