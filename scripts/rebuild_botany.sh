#!/bin/bash
# Rebuild Botany Library Index
# Run this after adding new documents to /home/peter/botany/

echo "================================"
echo "Rebuilding Botany Library Index"
echo "================================"
echo ""

# Set environment variables for Botany library
export LIBRARIAN_BACKEND="chonkie"
export LIBRARIAN_CHROMA_PATH="/home/peter/botany/.librarian/chroma_db"
export LIBRARIAN_METADATA_PATH="/home/peter/botany/.librarian/metadata"
export LIBRARIAN_SAFE_DIR="/home/peter/botany"
export PYTHONPATH="/home/peter/development/librarian-mcp"

cd /home/peter/development/librarian-mcp

# Activate virtual environment
source venv/bin/activate

echo "📂 Botany Library: /home/peter/botany"
echo "🔄 Syncing documents..."
echo ""

python -c "
import sys
sys.path.insert(0, '/home/peter/development/librarian-mcp')

from mcp_server.backend.chonkie_backend import ChonkieBackend
from mcp_server.core.document_manager import DocumentManager
from mcp_server.core.metadata_store import MetadataStore
from mcp_server.core.ignore_patterns import IgnorePatterns

backend = ChonkieBackend(
    db_path='/home/peter/botany/.librarian/chroma_db',
    collection_name='documents'
)
metadata_store = MetadataStore(metadata_path='/home/peter/botany/.librarian/metadata')
ignore_patterns = IgnorePatterns(root_path='/home/peter/botany')
doc_manager = DocumentManager(backend, metadata_store, ignore_patterns)

print('Syncing /home/peter/botany...')
print()

results = doc_manager.sync_directory(
    path='/home/peter/botany',
    extensions={'.pdf', '.txt', '.md', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.toml', '.rst', '.html', '.docx'},
    recursive=True
)

print()
print('📊 Sync Results:')
print(f\"  ✅ Added: {results['added']}\")
print(f\"  🔄 Updated: {results['updated']}\")
print(f\"  ✓ Unchanged: {results['unchanged']}\")
print(f\"  🗑️  Removed: {results['removed']}\")
print(f\"  ⏭️  Ignored: {results['ignored']}\")

if results['errors']:
    print(f\"\\n⚠️  Errors ({len(results['errors'])}):\")
    for error in results['errors'][:5]:
        print(f\"     {error[:100]}...\")

stats = doc_manager.get_stats()
print()
print('📈 Library Statistics:')
print(f\"  📚 Documents: {stats['total_documents']}\")
print(f\"  🔢 Chunks: {stats['total_chunks']}\")
print(f\"  💾 Size: {stats['total_size']:,} bytes\")
print()

docs = doc_manager.list_indexed()
print('📖 Indexed Documents:')
for doc in docs:
    print(f\"     • {doc['name']} ({doc['chunk_count']} chunks)\")

print()
print('✅ Botany library index rebuilt!')
"

echo ""
echo "================================"
echo "Rebuild Complete!"
echo "================================"
