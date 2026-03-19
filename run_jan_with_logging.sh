#!/bin/bash
# Launch librarian-mcp server with comprehensive logging for Jan testing

echo "=========================================="
echo "Starting Librarian MCP Server with Logging"
echo "=========================================="
echo ""
echo "This will start the server with detailed logging to help debug MCP tool calls."
echo "Logs will be written to: librarian_mcp_debug.log"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the logging-enhanced server
python librarian_mcp_with_logging.py \
    --safe-dir ~/development \
    --documents-dir ./documents \
    --chroma-path ./chroma_db \
    --metadata-path ./metadata
