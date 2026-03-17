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
from mcp_server.backend.chroma_backend import ChromaBackend
from mcp_server.config.settings import Settings

def main():
    print("Rebuilding Librarian Library...")
    print(f"Project directory: {Settings.PROJECT_ROOT}")
    print(f"Documents directory: {Settings.DOCUMENTS_DIR}")
    print()

    # Initialize components
    backend = ChromaBackend(collection_name=Settings.CHROMA_COLLECTION)
    metadata = MetadataStore()
    ignore_patterns = IgnorePatterns(str(Settings.PROJECT_ROOT))
    doc_manager = DocumentManager(backend, metadata, ignore_patterns)

    # Sync the project directory
    print("Starting sync...")
    result = doc_manager.sync_directory(
        path=str(Settings.PROJECT_ROOT),
        extensions={'.md', '.txt', '.py', '.json', '.yaml', '.yml', '.toml'},
        recursive=True
    )

    print()
    print("Sync completed!")
    print(f"  Added: {result['added']} documents")
    print(f"  Updated: {result['updated']} documents")
    print(f"  Unchanged: {result['unchanged']} documents")
    print(f"  Removed: {result['removed']} documents")
    print(f"  Ignored: {result['ignored']} files (excluded by .librarianignore)")

if __name__ == "__main__":
    main()
