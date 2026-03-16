#!/bin/bash
#
# Librarian MCP Server Startup Script
#
# Usage:
#   ./setup_mcp.sh [options]
#
# Options:
#   --safe-dir PATH       Allowed directory for CLI operations
#   --documents-dir PATH  Document storage location
#   --chroma-path PATH    ChromaDB data directory
#   --metadata-path PATH  Metadata storage directory

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default paths
SAFE_DIR="${HOME}"
DOCUMENTS_DIR="${SCRIPT_DIR}/documents"
CHROMA_PATH="${SCRIPT_DIR}/chroma_db"
METADATA_PATH="${SCRIPT_DIR}/metadata"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --safe-dir)
            SAFE_DIR="$2"
            shift 2
            ;;
        --documents-dir)
            DOCUMENTS_DIR="$2"
            shift 2
            ;;
        --chroma-path)
            CHROMA_PATH="$2"
            shift 2
            ;;
        --metadata-path)
            METADATA_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Ensure directories exist
mkdir -p "$DOCUMENTS_DIR"
mkdir -p "$CHROMA_PATH"
mkdir -p "$METADATA_PATH"

# Activate virtual environment if it exists
if [ -d "${SCRIPT_DIR}/venv" ]; then
    echo "Activating virtual environment..."
    source "${SCRIPT_DIR}/venv/bin/activate"
else
    echo "Warning: Virtual environment not found at ${SCRIPT_DIR}/venv"
    echo "Create one with: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
fi

# Start the MCP server
echo "Starting Librarian MCP Server..."
echo "  Safe directory: ${SAFE_DIR}"
echo "  Documents: ${DOCUMENTS_DIR}"
echo "  ChromaDB: ${CHROMA_PATH}"
echo "  Metadata: ${METADATA_PATH}"
echo ""

python "${SCRIPT_DIR}/mcp_server/librarian_mcp.py" \
    --safe-dir "${SAFE_DIR}" \
    --documents-dir "${DOCUMENTS_DIR}" \
    --chroma-path "${CHROMA_PATH}" \
    --metadata-path "${METADATA_PATH}"
