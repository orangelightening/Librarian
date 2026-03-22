#!/bin/bash
# Rebuild script for librarian-mcp library

LIBRARY_PROJECT_DIR="/home/peter/development/librarian-mcp"

echo "Rebuilding librarian-mcp library..."

# Set library-specific environment
export LIBRARIAN_CHROMA_PATH="/home/peter/development/librarian-mcp/.librarian/chroma_db"
export LIBRARIAN_METADATA_PATH="/home/peter/development/librarian-mcp/.librarian/metadata"
export LIBRARIAN_BACKEND="chonkie"

cd "$LIBRARY_PROJECT_DIR"
./scripts/clear_and_rebuild.sh
