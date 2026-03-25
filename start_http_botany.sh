#!/bin/bash
# Start Librarian MCP in HTTP mode with full configuration

cd /home/peter/development/librarian-mcp
source venv/bin/activate

# All configuration via environment variables
export LIBRARIAN_TRANSPORT=http
export LIBRARIAN_HOST=0.0.0.0
export LIBRARIAN_PORT=8888

# Paths and settings
export LIBRARIAN_BACKEND=chonkie
export LIBRARIAN_CHROMA_PATH=/home/peter/botany/.librarian/chroma_db
export LIBRARIAN_METADATA_PATH=/home/peter/botany/.librarian/metadata
export LIBRARIAN_SAFE_DIR=/home/peter/botany
export PYTHONPATH=/home/peter/development/librarian-mcp

echo "Starting Librarian MCP Server in HTTP mode..."
echo "URL: http://0.0.0.0:8888"
echo "Backend: chonkie"
echo "ChromaDB: /home/peter/botany/.librarian/chroma_db"
echo "Metadata: /home/peter/botany/.librarian/metadata"
echo "Safe Dir: /home/peter/botany"
echo ""

python mcp_server/librarian_mcp.py \
  --safe-dir /home/peter/botany \
  --transport http \
  --host 0.0.0.0 \
  --port 8888
