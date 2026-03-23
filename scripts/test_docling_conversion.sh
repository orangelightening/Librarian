#!/bin/bash
# Test Docling PDF to Markdown conversion
# Quick test on one PDF to verify it works

echo "================================"
echo "Testing Docling PDF → Markdown Conversion"
echo "================================"
echo ""

BOTANY_DIR="/home/peter/botany"

cd "$BOTANY_DIR"

# Find first PDF
PDF_FILE=$(ls -1 *.pdf 2>/dev/null | head -1)

if [ -z "$PDF_FILE" ]; then
    echo "❌ No PDF files found in $BOTANY_DIR"
    exit 1
fi

echo "📄 Testing with: $PDF_FILE"
echo ""

# Activate venv
source /home/peter/development/librarian-mcp/venv/bin/activate

# Convert first PDF
name="${PDF_FILE%.pdf}"
md_file="${name}.md"

echo "Converting to $md_file..."
echo ""

python -c "
from docling.document_converter import DocumentConverter
import os

converter = DocumentConverter()
result = converter.convert('$PDF_FILE')
markdown = result.document.export_to_markdown()

# Show first 500 characters
print('First 500 characters of output:')
print('---')
print(markdown[:500])
print('...')
print('---')
print(f'Total characters: {len(markdown)}')
print(f'Output file: $md_file')
print(f'Size: {len(markdown)} bytes')

# Save to file
with open('$md_file', 'w') as f:
    f.write(markdown)

print()
print('✅ Test conversion successful!')
print('File saved to:', os.path.abspath('$md_file'))
" || echo "❌ Test failed"

echo ""
echo "================================"
echo "Test Complete!"
echo "================================"
echo ""
echo "If the test looks good, run the full conversion:"
echo "  ./scripts/convert_botany_pdf_to_md.sh"
echo ""
