#!/bin/bash
# Start Librarian MCP in HTTP mode for librarian-mcp library

cd /home/peter/development/librarian-mcp
source venv/bin/activate

# All configuration via environment variables
export LIBRARIAN_TRANSPORT=http
export LIBRARIAN_HOST=0.0.0.0
export LIBRARIAN_PORT=8889

# Paths and settings for librarian-mcp library
export LIBRARIAN_BACKEND=chonkie
export LIBRARIAN_CHROMA_PATH=/home/peter/library_shadows/chromadb
export LIBRARIAN_METADATA_PATH=/home/peter/library_shadows/.librarian/metadata
export LIBRARIAN_SAFE_DIR=/home/peter/development/librarian-mcp
export PYTHONPATH=/home/peter/development/librarian-mcp

echo "Starting Librarian MCP Server in HTTP mode..."
echo "Library: librarian-mcp"
echo "URL: http://0.0.0.0:8889"
echo "Backend: chonkie"
echo "ChromaDB: /home/peter/library_shadows/chromadb"
echo "Metadata: /home/peter/library_shadows/.librarian/metadata"
echo "Safe Dir: /home/peter/development/librarian-mcp"
echo ""

python mcp_server/librarian_mcp.py \
  --safe-dir /home/peter/development/librarian-mcp \
  --transport http \
  --host 0.0.0.0 \
  --port 8889
