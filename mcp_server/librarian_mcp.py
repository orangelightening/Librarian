#!/usr/bin/env python3
"""
Librarian MCP Server - Unified librarian and CLI access server.

This server provides:
- Library tools: Search, sync, and manage documents in ChromaDB
- CLI tools: Secure command execution and file access

Usage:
    python mcp_server/librarian_mcp.py [options]

Options:
    --safe-dir PATH       Allowed directory for CLI operations (default: ~/)
    --documents-dir PATH  Document storage location (default: ./documents)
    --chroma-path PATH    ChromaDB data directory (default: ./chroma_db)
    --metadata-path PATH  Metadata storage directory (default: ./metadata)
"""
import sys
import argparse
from pathlib import Path

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: fastmcp not installed. Run: pip install fastmcp")
    sys.exit(1)

from mcp_server.tools.library_tools import register_library_tools
from mcp_server.tools.cli_tools import register_cli_tools
from mcp_server.config.librarian_prompt import get_librarian_instructions


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Librarian MCP Server - Document library and CLI access",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--safe-dir',
        default=str(Path.home()),
        help='Allowed directory for CLI operations (default: ~/)'
    )

    parser.add_argument(
        '--documents-dir',
        default=None,
        help='Document storage location (default: ./documents)'
    )

    parser.add_argument(
        '--chroma-path',
        default=None,
        help='ChromaDB data directory (default: ./chroma_db)'
    )

    parser.add_argument(
        '--metadata-path',
        default=None,
        help='Metadata storage directory (default: ./metadata)'
    )

    return parser.parse_args()


def main():
    """Main entry point for the Librarian MCP Server."""
    args = parse_arguments()

    # Update settings from command line arguments
    from mcp_server.config import settings
    import os

    if args.safe_dir:
        settings.Settings.SAFE_DIR = args.safe_dir
        os.environ['LIBRARIAN_SAFE_DIR'] = args.safe_dir

    if args.documents_dir:
        settings.Settings.DOCUMENTS_DIR = args.documents_dir
        os.environ['LIBRARIAN_DOCUMENTS_DIR'] = args.documents_dir

    if args.chroma_path:
        settings.Settings.CHROMA_PATH = args.chroma_path
        os.environ['LIBRARIAN_CHROMA_PATH'] = args.chroma_path

    if args.metadata_path:
        settings.Settings.METADATA_PATH = args.metadata_path
        os.environ['LIBRARIAN_METADATA_PATH'] = args.metadata_path

    # Ensure directories exist
    settings.Settings.ensure_directories()

    # Create MCP server with librarian persona
    instructions = get_librarian_instructions(
        safe_dir=args.safe_dir,
        documents_dir=settings.Settings.DOCUMENTS_DIR,
        chroma_path=settings.Settings.CHROMA_PATH,
        metadata_path=settings.Settings.METADATA_PATH
    )

    mcp = FastMCP(
        "librarian-mcp",
        instructions=instructions
    )

    # Register tool groups
    register_library_tools(mcp)
    register_cli_tools(mcp, args.safe_dir)

    # Print startup info
    print(f"Librarian MCP Server starting...", file=sys.stderr)
    print(f"  Safe directory: {args.safe_dir}", file=sys.stderr)
    print(f"  Documents: {settings.Settings.DOCUMENTS_DIR}", file=sys.stderr)
    print(f"  ChromaDB: {settings.Settings.CHROMA_PATH}", file=sys.stderr)
    print(f"  Metadata: {settings.Settings.METADATA_PATH}", file=sys.stderr)

    # Run server
    mcp.run()


if __name__ == "__main__":
    main()
