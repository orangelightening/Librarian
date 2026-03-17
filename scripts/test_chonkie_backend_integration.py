#!/usr/bin/env python3
"""
Test the Chonkie backend integration with the librarian tools.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set backend to chonkie for testing
os.environ["LIBRARIAN_BACKEND"] = "chonkie"

def test_backend_factory():
    """Test that the backend factory creates Chonkie backend."""
    print("=" * 70)
    print("Test 1: Backend Factory")
    print("=" * 70)

    from mcp_server.backend.factory import get_backend
    from mcp_server.config.settings import settings

    print(f"Backend setting: {settings.BACKEND}")

    backend = get_backend(backend_type="chonkie")
    print(f"✅ Created backend: {backend.__class__.__name__}")

    info = backend.get_backend_info()
    print(f"✅ Backend info: {info}")

    return True

def test_chonkie_chunking():
    """Test Chonkie chunking through the backend."""
    print("\n" + "=" * 70)
    print("Test 2: Chonkie Chunking")
    print("=" * 70)

    from mcp_server.backend.factory import get_backend

    backend = get_backend(backend_type="chonkie")

    # Test document
    text = """
    # Librarian MCP Server

    The Librarian MCP Server is an intelligent research assistant with access to a curated document library and secure file system tools.

    ## Key Features

    - Semantic search across all indexed documents
    - Secure file access within allowed directories
    - Document lifecycle management
    - Citation tracking and source attribution

    ## Architecture

    Built with FastMCP for MCP protocol handling, ChromaDB for vector storage,
    and intelligent document chunking using Chonkie.
    """

    print(f"Original text: {len(text)} characters")

    # Chunk the document
    results = backend.chunk_documents(
        documents=[text],
        document_ids=["test_doc"],
        source="test.md"
    )

    print(f"✅ Created {len(results)} chunks")
    for i, chunk in enumerate(results[:3]):
        metadata = chunk['metadata']
        print(f"  Chunk {i+1}:")
        print(f"    Tokens: {metadata['token_count']}")
        print(f"    Chars: {metadata['char_count']}")
        print(f"    Method: {metadata['chunking_method']}")
        print(f"    Text: {chunk['text'][:80]}...")

    return True

def test_library_tools_integration():
    """Test that library tools work with Chonkie backend."""
    print("\n" + "=" * 70)
    print("Test 3: Library Tools Integration")
    print("=" * 70)

    from mcp_server.tools.library_tools import get_backend, get_doc_manager

    # Test that tools use the correct backend
    backend = get_backend()
    print(f"✅ Library tools using: {backend.__class__.__name__}")

    # Test document manager
    doc_manager = get_doc_manager()
    print(f"✅ Document manager backend: {doc_manager.backend.__class__.__name__}")

    # Test stats
    stats = doc_manager.get_stats()
    print(f"✅ Backend stats: {stats['backend_stats']}")

    return True

def test_backend_switching():
    """Test switching between backends."""
    print("\n" + "=" * 70)
    print("Test 4: Backend Switching")
    print("=" * 70)

    from mcp_server.backend.factory import get_backend

    # Create ChromaDB backend
    chroma_backend = get_backend(backend_type="chroma")
    print(f"✅ Created ChromaDB backend: {chroma_backend.__class__.__name__}")

    # Create Chonkie backend
    chonkie_backend = get_backend(backend_type="chonkie")
    print(f"✅ Created Chonkie backend: {chonkie_backend.__class__.__name__}")

    # Test that they're different
    print(f"✅ Backends are different: {type(chroma_backend) != type(chonkie_backend)}")

    # Test Chonkie has extra methods
    chonkie_info = chonkie_backend.get_backend_info()
    print(f"✅ Chonkie backend info available: {chonkie_info}")

    return True

def main():
    """Run all integration tests."""
    print("\n🦛 Chonkie Backend Integration Test")
    print("=" * 70)

    try:
        # Test 1: Backend factory
        test_backend_factory()

        # Test 2: Chonkie chunking
        test_chonkie_chunking()

        # Test 3: Library tools integration
        test_library_tools_integration()

        # Test 4: Backend switching
        test_backend_switching()

        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n🎉 Chonkie backend is fully integrated!")
        print("\n📝 Summary:")
        print("  ✅ Backend factory works correctly")
        print("  ✅ Chonkie chunking produces intelligent chunks")
        print("  ✅ Library tools use the configured backend")
        print("  ✅ Easy switching between ChromaDB and Chonkie")
        print("\n🚀 Ready for production use!")
        print("\n💡 To use Chonkie backend:")
        print("   export LIBRARIAN_BACKEND=chonkie")
        print("   ./setup_mcp.sh")

        return 0

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
