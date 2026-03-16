#!/usr/bin/env python3
"""
Bulk document ingestion script.

Usage:
    python scripts/ingest.py --path /path/to/docs --extensions .md,.txt
    python scripts/ingest.py --path ~/documents --extensions .py --recursive

This script scans a directory for documents and adds them to the library.
New documents are added, modified documents are updated, deleted documents are removed.
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.core.document_manager import DocumentManager
from mcp_server.core.metadata_store import MetadataStore
from mcp_server.backend.chroma_backend import ChromaBackend


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Ingest documents into the library",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--path',
        required=True,
        help='Directory or file to ingest'
    )

    parser.add_argument(
        '--extensions',
        help='Comma-separated extensions (e.g., .md,.txt,.py)'
    )

    parser.add_argument(
        '--recursive',
        action='store_true',
        default=True,
        help='Recursive scan (default: True)'
    )

    parser.add_argument(
        '--no-recursive',
        action='store_false',
        dest='recursive',
        help='Non-recursive scan'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    print(f"Librarian Document Ingestion")
    print(f"=" * 50)

    # Initialize components
    print(f"Initializing components...")
    backend = ChromaBackend()
    metadata = MetadataStore()
    doc_manager = DocumentManager(backend, metadata)

    # Parse extensions
    ext_set = None
    if args.extensions:
        ext_set = set(args.extensions.split(','))
        print(f"Extensions: {', '.join(sorted(ext_set))}")
    else:
        print(f"Extensions: all supported types")

    # Check if path is a file or directory
    path_obj = Path(args.path).resolve()

    if not path_obj.exists():
        print(f"Error: Path not found: {args.path}")
        sys.exit(1)

    # Process single file
    if path_obj.is_file():
        print(f"\nProcessing single file: {path_obj}")
        result = doc_manager.add_document(path_obj)

        if result['status'] == 'added':
            print(f"✓ Added: {result['name']}")
            print(f"  Document ID: {result['document_id']}")
            print(f"  Chunks: {result['chunk_count']}")
        elif result['status'] == 'unchanged':
            print(f"○ Unchanged: {result['name']}")
            print(f"  Document ID: {result['document_id']}")
        elif result['status'] == 'error':
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)

        return

    # Process directory
    print(f"\nSyncing directory: {path_obj}")
    print(f"Recursive: {args.recursive}")

    results = doc_manager.sync_directory(
        args.path,
        ext_set,
        args.recursive
    )

    # Print results
    print(f"\nResults:")
    print(f"  Added:     {results['added']} documents")
    print(f"  Updated:   {results['updated']} documents")
    print(f"  Unchanged: {results['unchanged']} documents")
    print(f"  Removed:   {results['removed']} documents")

    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for error in results['errors'][:10]:
            print(f"  • {error}")
        if len(results['errors']) > 10:
            print(f"  ... and {len(results['errors']) - 10} more errors")
        sys.exit(1)

    print(f"\n✓ Ingestion complete!")


if __name__ == "__main__":
    main()
