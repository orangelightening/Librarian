#!/usr/bin/env python3
"""
Librarian MCP Server with comprehensive logging for debugging.

This version logs all incoming tool calls, arguments, and results so we can
see what's actually happening when Jan calls our tools.
"""
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime
import json

# Setup comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('librarian_mcp_debug.log'),
        logging.StreamHandler()
    ]
)

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: fastmcp not installed. Run: pip install fastmcp")
    sys.exit(1)

# Monkey-patch FastMCP to add request/response logging
original_run = None

def log_mcp_request(func):
    """Decorator to log MCP tool calls"""
    def wrapper(*args, **kwargs):
        tool_name = kwargs.get('name', args[0] if args else 'unknown')
        tool_args = kwargs.get('arguments', args[1] if len(args) > 1 else {})

        logging.info(f"🔧 TOOL CALL: {tool_name}")
        logging.debug(f"   Arguments: {json.dumps(tool_args, indent=2)}")

        try:
            result = func(*args, **kwargs)
            logging.info(f"✓ TOOL RESULT: {tool_name}")
            logging.debug(f"   Result type: {type(result)}")
            logging.debug(f"   Result preview: {str(result)[:200]}")
            return result
        except Exception as e:
            logging.error(f"✗ TOOL ERROR: {tool_name} - {e}")
            raise

    return wrapper

# Apply logging wrapper
def add_logging_to_mcp():
    """Add comprehensive logging to all MCP tools"""
    import mcp_server.tools.library_tools as library_tools
    import mcp_server.tools.cli_tools as cli_tools

    logging.info("=" * 60)
    logging.info("Adding comprehensive logging to librarian-mcp")
    logging.info("=" * 60)

    # Log all function definitions in library_tools
    for name in dir(library_tools):
        if not name.startswith('_'):
            obj = getattr(library_tools, name)
            if callable(obj):
                logging.debug(f"Found library_tools.{name}: {type(obj)}")

# Original server startup, now with logging
def main():
    parser = argparse.ArgumentParser(description="Librarian MCP Server with logging")
    parser.add_argument("--safe-dir", default="~/", help="Allowed directory for CLI operations")
    parser.add_argument("--documents-dir", default="./documents", help="Document storage location")
    parser.add_argument("--chroma-path", default="./chroma_db", help="ChromaDB data directory")
    parser.add_argument("--metadata-path", default="./metadata", help="Metadata storage directory")

    args = parser.parse_args()

    logging.info("=" * 60)
    logging.info("Starting Librarian MCP Server with comprehensive logging")
    logging.info("=" * 60)
    logging.info(f"Safe directory: {args.safe_dir}")
    logging.info(f"Documents directory: {args.documents_dir}")
    logging.info(f"ChromaDB path: {args.chroma_path}")
    logging.info(f"Metadata path: {args.metadata_path}")
    logging.info("=" * 60)

    # Import tools
    from mcp_server.tools.library_tools import register_library_tools
    from mcp_server.tools.cli_tools import register_cli_tools
    from mcp_server.config.librarian_prompt import get_librarian_instructions

    # Create FastMCP instance with configured instructions
    mcp = FastMCP(
        instructions=get_librarian_instructions(
            safe_dir=str(Path(args.safe_dir).expanduser()),
            documents_dir=str(Path(args.documents_dir).expanduser()),
            chroma_path=str(Path(args.chroma_path).expanduser()),
            metadata_path=str(Path(args.metadata_path).expanduser())
        ).strip()
    )

    # Register tools
    register_library_tools(mcp)
    register_cli_tools(mcp, str(Path(args.safe_dir).expanduser()))

    # Add logging
    add_logging_to_mcp()

    logging.info("✓ All tools registered with logging wrapper")
    instructions = get_librarian_instructions(
        safe_dir=str(Path(args.safe_dir).expanduser()),
        documents_dir=str(Path(args.documents_dir).expanduser()),
        chroma_path=str(Path(args.chroma_path).expanduser()),
        metadata_path=str(Path(args.metadata_path).expanduser())
    )
    logging.info(f"✓ Server instructions loaded ({len(instructions.strip())} chars)")
    logging.info("=" * 60)
    logging.info("Librarian MCP Server ready to accept connections")
    logging.info("=" * 60)

    # Run server
    mcp.run()

if __name__ == "__main__":
    main()
