#!/usr/bin/env python3
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

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

    parser.add_argument(
        '--transport',
        default='stdio',
        choices=['stdio', 'http'],
        help='Transport protocol: stdio or http (default: stdio)'
    )

    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host for HTTP transport (default: 0.0.0.0)'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port for HTTP transport (default: 8000)'
    )

    return parser.parse_args()


def main():
    """Main entry point for the Librarian MCP Server."""
    args = parse_arguments()

    # Update settings from command line arguments or environment variables
    from mcp_server.config import settings
    import os

    # Support environment variables for configuration
    safe_dir = args.safe_dir or os.getenv('LIBRARIAN_SAFE_DIR', str(Path.home()))
    documents_dir = args.documents_dir or os.getenv('LIBRARIAN_DOCUMENTS_DIR')
    chroma_path = args.chroma_path or os.getenv('LIBRARIAN_CHROMA_PATH')
    metadata_path = args.metadata_path or os.getenv('LIBRARIAN_METADATA_PATH')

    # Transport configuration
    transport = os.getenv('LIBRARIAN_TRANSPORT', args.transport)
    host = os.getenv('LIBRARIAN_HOST', args.host)
    port = int(os.getenv('LIBRARIAN_PORT', str(args.port)))

    # Update settings
    if safe_dir:
        settings.Settings.SAFE_DIR = safe_dir
        os.environ['LIBRARIAN_SAFE_DIR'] = safe_dir

    if documents_dir:
        settings.Settings.DOCUMENTS_DIR = documents_dir
        os.environ['LIBRARIAN_DOCUMENTS_DIR'] = documents_dir

    if chroma_path:
        settings.Settings.CHROMA_PATH = chroma_path
        os.environ['LIBRARIAN_CHROMA_PATH'] = chroma_path

    if metadata_path:
        settings.Settings.METADATA_PATH = metadata_path
        os.environ['LIBRARIAN_METADATA_PATH'] = metadata_path

    # Ensure directories exist
    settings.Settings.ensure_directories()

    # Create MCP server with librarian persona
    instructions = get_librarian_instructions(
        safe_dir=safe_dir,
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
    register_cli_tools(mcp, safe_dir)

    # Print startup info
    print(f"Librarian MCP Server starting...", file=sys.stderr)
    print(f"  Transport: {transport}", file=sys.stderr)
    print(f"  Safe directory: {safe_dir}", file=sys.stderr)
    print(f"  Documents: {settings.Settings.DOCUMENTS_DIR}", file=sys.stderr)
    print(f"  ChromaDB: {settings.Settings.CHROMA_PATH}", file=sys.stderr)
    print(f"  Metadata: {settings.Settings.METADATA_PATH}", file=sys.stderr)

    if transport == 'http':
        print(f"  HTTP server: http://{host}:{port}", file=sys.stderr)

    # Run server with appropriate transport
    if transport == 'http':
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
