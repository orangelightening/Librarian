#!/bin/bash
# Librarian MCP Server Installation Script
# This script detects your installation directory and outputs the correct configuration

set -e

INSTALL_DIR=$(pwd)
VENV_PYTHON="$INSTALL_DIR/venv/bin/python"
MCP_SERVER="$INSTALL_DIR/mcp_server/librarian_mcp.py"

echo "======================================"
echo "Librarian MCP Server Installation"
echo "======================================"
echo ""
echo "Installation Directory: $INSTALL_DIR"
echo ""

# Check if virtual environment exists
if [ ! -d "$INSTALL_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Virtual environment already exists"
fi

# Check if dependencies are installed
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Python executable not found at $VENV_PYTHON"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "======================================"
echo "MCP Client Configuration"
echo "======================================"
echo ""
echo "Use the following configuration for your MCP client:"
echo ""
echo "--------------------------------------"
echo "For Jan (~/.config/Jan/MCP/servers.json):"
echo "--------------------------------------"
cat <<EOF
{
  "mcpServers": {
    "librarian": {
      "command": "$VENV_PYTHON",
      "args": [
        "$MCP_SERVER",
        "--safe-dir", "$INSTALL_DIR"
      ]
    }
  }
}
EOF

echo ""
echo "--------------------------------------"
echo "For LM Studio (Settings → MCP Servers):"
echo "--------------------------------------"
cat <<EOF
{
  "mcpServers": {
    "librarian": {
      "command": "$VENV_PYTHON",
      "args": [
        "$MCP_SERVER",
        "--safe-dir", "$INSTALL_DIR"
      ]
    }
  }
}
EOF

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Copy the configuration above to your MCP client"
echo "2. Add documents: python scripts/ingest.py --path /path/to/docs"
echo "3. Start searching!"
echo ""
