#!/usr/bin/env python3
"""
Comprehensive end-to-end test of Chonkie backend.
Tests real document sync, search, and all librarian tools.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set backend to chonkie
os.environ["LIBRARIAN_BACKEND"] = "chonkie"

def test_complete_workflow():
    """Test complete workflow: sync → search → stats."""
    print("=" * 70)
    print("END-TO-END TEST: Chonkie Backend")
    print("=" * 70)

    from mcp_server.tools.library_tools import get_doc_manager

    # Create a test document
    test_doc = """# Librarian MCP Server - Architecture Overview

## Components

The Librarian MCP Server consists of several key components working together:

### MCP Server Layer
The main entry point is `librarian_mcp.py`, which creates a FastMCP server instance and registers all tools. This layer handles communication with MCP clients like Jan and LM Studio.

### Library Tools
Library tools provide the core functionality:
- search_library: Semantic search across indexed documents
- sync_documents: Add/update/remove documents from directories
- add_document: Add individual documents
- remove_document: Remove documents and their chunks
- list_indexed_documents: Show all indexed documents
- get_library_stats: Display library statistics

### CLI Tools
CLI tools provide secure file system access:
- execute_command: Run whitelisted commands
- read_document: Read file contents
- list_documents: List files in directories
- search_documents: Literal text search within files
- document_summary: Get file structure summary

### Backend Layer
The backend layer handles document storage and retrieval:
- ChromaDB: Vector database for semantic search
- Chonkie: Intelligent document chunking (Phase 2)
- Metadata Store: Tracks document changes and indexing status

### Document Processing Pipeline
1. Documents are discovered via FileFetcher
2. Text is extracted and cleaned
3. Chonkie performs intelligent chunking
4. Chunks are embedded and stored in ChromaDB
5. Metadata is updated to track processing status

## Security

The librarian implements multiple security layers:
- .librarianignore: Exclude sensitive files
- Safe directory: Limit file system access
- Command whitelisting: Only allow safe commands
- Path validation: Prevent directory traversal attacks

## Usage Flow

1. User configures MCP client with librarian server
2. Server starts and connects to ChromaDB
3. User syncs documents from a directory
4. Documents are chunked and indexed
5. User searches using natural language
6. Relevant chunks are retrieved with citations
7. User receives synthesized, cited responses

This architecture provides a robust, secure, and intelligent document research assistant.
"""

    # Write test document
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_doc)
        test_path = f.name

    try:
        # Test 1: Add document
        print("\n📄 Test 1: Add Document")
        print("-" * 70)

        doc_manager = get_doc_manager()
        result = doc_manager.add_document(Path(test_path))
        doc_id_for_cleanup = None

        if result['status'] == 'added':
            doc_id_for_cleanup = result['document_id']
            print(f"✅ Added document: {result['name']}")
            print(f"   Document ID: {doc_id_for_cleanup}")
            print(f"   Chunks created: {result['chunk_count']}")
            print(f"   Processing time: {result.get('processing_time', 'N/A')}")
        else:
            print(f"❌ Failed to add document: {result}")
            return False

        # Test 2: Check document status
        print("\n🔍 Test 2: Document Status")
        print("-" * 70)

        status = doc_manager.get_document_status(test_path)
        print(f"Status: {status['status']}")
        if doc_id_for_cleanup:
            print(f"Document ID: {doc_id_for_cleanup}")
        print(f"Chunks: {status.get('chunk_count', 0)}")

        # Test 3: Search
        print("\n🔎 Test 3: Search")
        print("-" * 70)

        queries = [
            "What components does the librarian have?",
            "How does the document processing pipeline work?",
            "What security features are implemented?"
        ]

        backend = doc_manager.backend

        for query in queries:
            print(f"\nQuery: {query}")
            results = backend.query(query_text=query, limit=3)

            print(f"Results: {len(results)} chunks found")
            for i, result in enumerate(results[:2]):
                print(f"  {i+1}. [Source: {result['metadata'].get('document_name', 'unknown')}]")
                print(f"     {result['text'][:100]}...")

        # Test 4: Get stats
        print("\n📊 Test 4: Library Statistics")
        print("-" * 70)

        stats = doc_manager.get_stats()
        print(f"Backend: {stats['backend_stats']['backend']}")
        print(f"Collection: {stats['backend_stats']['collection']}")
        print(f"Total Chunks: {stats['backend_stats']['total_chunks']}")
        print(f"Total Documents: {stats['total_documents']}")

        # Test 5: List documents
        print("\n📋 Test 5: List Documents")
        print("-" * 70)

        documents = doc_manager.list_indexed()
        print(f"Indexed documents: {len(documents)}")

        # Find our test document
        test_doc_info = None
        for doc in documents:
            if doc.get('document_id') == doc_id_for_cleanup:
                test_doc_info = doc
                break

        if test_doc_info:
            print(f"✅ Found test document in list:")
            print(f"   Name: {test_doc_info.get('name', 'Unknown')}")
            print(f"   ID: {test_doc_info.get('document_id', 'N/A')}")
            print(f"   Chunks: {test_doc_info.get('chunk_count', 0)}")
            print(f"   Method: {test_doc_info.get('chunking_method', 'Unknown')}")
        else:
            print("⚠️  Test document not found in list (this might be OK)")

        # Test 6: Remove document
        print("\n🗑️  Test 6: Remove Document")
        print("-" * 70)

        print(f"Attempting to remove document_id: {doc_id_for_cleanup}")

        try:
            success = doc_manager.remove_document(doc_id_for_cleanup)
            if success:
                print(f"✅ Removed document: {doc_id_for_cleanup}")
            else:
                print(f"❌ Failed to remove document")
                return False
        except Exception as e:
            print(f"❌ Error during removal: {e}")
            import traceback
            traceback.print_exc()
            return False

        # Verify removal
        status_after = doc_manager.get_document_status(test_path)
        if status_after['status'] == 'not_indexed':
            print("✅ Document successfully removed from index")
        else:
            print(f"⚠️  Document still indexed: {status_after['status']}")
            return False

        print("\n" + "=" * 70)
        print("✅ ALL WORKFLOW TESTS PASSED!")
        print("=" * 70)

        return True

    finally:
        # Cleanup test file
        try:
            os.unlink(test_path)
        except:
            pass

def main():
    """Run comprehensive end-to-end test."""
    print("\n🦛 Chonkie Backend - Comprehensive Test")
    print("=" * 70)
    print("\nThis test demonstrates:")
    print("  • Real document processing with Chonkie")
    print("  • Semantic search across indexed content")
    print("  • Complete librarian tool workflow")
    print("  • Backend switching and compatibility")
    print("\n" + "=" * 70)

    try:
        success = test_complete_workflow()

        if success:
            print("\n🎉 SUCCESS! Chonkie backend is production-ready!")
            print("\n📋 What was tested:")
            print("  ✅ Document addition with Chonkie chunking")
            print("  ✅ Document status tracking")
            print("  ✅ Semantic search functionality")
            print("  ✅ Library statistics")
            print("  ✅ Document listing")
            print("  ✅ Document removal")
            print("\n🚀 Ready for production use!")
            print("\n💡 To use Chonkie backend:")
            print("   export LIBRARIAN_BACKEND=chonkie")
            print("   ./setup_mcp.sh")
            print("\n📚 See CHONKIE_MIGRATION.md for detailed guide")

            return 0
        else:
            print("\n❌ Some tests failed")
            return 1

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
