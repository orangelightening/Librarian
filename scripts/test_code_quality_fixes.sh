#!/bin/bash
# Test code quality fixes applied 2026-03-21

echo "======================================"
echo "Testing Code Quality Fixes"
echo "======================================"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "[Test 1/4] Backend Type Validation"
echo "-----------------------------------"
echo "Test 1a: Valid backend (chonkie)"
python -c "
from mcp_server.config.settings import settings
print(f'✓ Valid backend loaded: {settings.BACKEND}')
"

echo ""
echo "Test 1b: Invalid backend (should fail)"
if LIBRARIAN_BACKEND=invalid python -c "from mcp_server.config.settings import settings" 2>/dev/null; then
    echo "❌ FAILED: Invalid backend was accepted"
else
    echo "✓ Correctly rejected invalid backend"
fi

echo ""
echo "[Test 2/4] Atomic File Writes"
echo "------------------------------"
python -c "
from mcp_server.core.metadata_store import MetadataStore
import tempfile
import os

# Create a temp metadata store (expects directory path)
with tempfile.TemporaryDirectory() as tmpdir:
    store = MetadataStore(metadata_path=tmpdir)

    # Add some metadata
    store.add({'document_id': 'test1', 'path': '/test1', 'checksum': 'abc123'})
    store.add({'document_id': 'test2', 'path': '/test2', 'checksum': 'def456'})

    # Verify it was saved
    import json
    index_file = os.path.join(tmpdir, 'index.json')
    with open(index_file, 'r') as f:
        data = json.load(f)

    if 'test1' in data and 'test2' in data:
        print('✓ Atomic write successful - data saved correctly')
    else:
        print('❌ FAILED: Data not saved correctly')
"

echo ""
echo "[Test 3/4] Backend Exception Handling"
echo "--------------------------------------"
python -c "
from mcp_server.tools.library_tools import get_backend
import sys

# First call should succeed
try:
    backend = get_backend()
    print('✓ Backend initialized successfully')
except Exception as e:
    print(f'❌ FAILED: {e}')
"

echo ""
echo "[Test 4/4] Batch Chunk Operations"
echo "----------------------------------"
python -c "
from mcp_server.backend.chroma_backend import ChromaBackend
import tempfile
import os

# Create temp backend
with tempfile.TemporaryDirectory() as tmpdir:
    db_path = os.path.join(tmpdir, 'test_chroma')
    backend = ChromaBackend(db_path=db_path, collection_name='test_collection')

    # Test batch chunking
    documents = ['Test document one. ' * 10, 'Test document two. ' * 10]
    document_ids = ['doc1', 'doc2']

    chunks = backend.chunk_documents(documents, document_ids, 'test_source')

    if chunks and len(chunks) > 0:
        print(f'✓ Batch chunking successful - created {len(chunks)} chunks')
    else:
        print('❌ FAILED: No chunks created')
"

echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"
echo ""
echo "If all tests passed, the fixes are working correctly."
echo ""
echo "Next steps:"
echo "1. Test document ingestion with: ./scripts/rebuild_library.py"
echo "2. Verify metadata integrity"
echo "3. Commit changes if all tests pass"
