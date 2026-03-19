#!/usr/bin/env python3
"""
Rebuild the librarian library from scratch.
Syncs the project directory while respecting .librarianignore.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.core.document_manager import DocumentManager
from mcp_server.core.metadata_store import MetadataStore
from mcp_server.core.ignore_patterns import IgnorePatterns
from mcp_server.backend.factory import get_backend
from mcp_server.config.settings import Settings

def main():
    print("=" * 70)
    print("Rebuilding Librarian Library")
    print("=" * 70)
    print(f"Project directory: {Settings.PROJECT_ROOT}")
    print(f"Documents directory: {Settings.DOCUMENTS_DIR}")
    print(f"Backend: {Settings.BACKEND}")
    print()

    # Initialize components using backend factory
    backend = get_backend(
        backend_type=Settings.BACKEND,
        collection_name=Settings.CHROMA_COLLECTION,
        db_path=Settings.CHROMA_PATH
    )

    # Show backend info
    if hasattr(backend, 'get_backend_info'):
        info = backend.get_backend_info()
        print(f"Using backend: {info.get('backend_type', 'unknown')}")
        if 'chunking_method' in info:
            print(f"Chunking method: {info['chunking_method']}")
        print()

    metadata = MetadataStore()
    ignore_patterns = IgnorePatterns(str(Settings.PROJECT_ROOT))
    doc_manager = DocumentManager(backend, metadata, ignore_patterns)

    # Clear existing data for true rebuild
    print("Clearing existing library...")
    print("-" * 70)
    backend.clear()
    metadata.clear()
    print()

    # Sync the project directory
    print("Starting sync...")
    result = doc_manager.sync_directory(
        path=str(Settings.PROJECT_ROOT),
        extensions={'.md', '.txt', '.py', '.json', '.yaml', '.yml', '.toml'},
        recursive=True
    )

    print()
    print("=" * 70)
    print("Sync Completed!")
    print("=" * 70)
    print(f"  Added: {result['added']} documents")
    print(f"  Updated: {result['updated']} documents")
    print(f"  Unchanged: {result['unchanged']} documents")
    print(f"  Removed: {result['removed']} documents")
    print(f"  Ignored: {result.get('ignored', 0)} files (excluded by .librarianignore)")

    if result['errors']:
        print()
        print(f"⚠️  Errors: {len(result['errors'])}")
        for error in result['errors'][:5]:
            print(f"    - {error}")
        if len(result['errors']) > 5:
            print(f"    ... and {len(result['errors']) - 5} more")

    print()
    print("📚 Library ready!")

if __name__ == "__main__":
    main()
