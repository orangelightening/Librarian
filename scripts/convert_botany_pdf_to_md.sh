#!/bin/bash
# Convert PDFs to Markdown using pypdf (already installed)
# Creates structured Markdown with page-by-page organization

BOTANY_DIR="/home/peter/botany"
LIBRARIAN_DIR="/home/peter/development/librarian-mcp"

echo "================================"
echo "Botany Library: PDF → Markdown Conversion"
echo "================================"
echo ""

# Check if botany directory exists
if [ ! -d "$BOTANY_DIR" ]; then
    echo "❌ Error: $BOTANY_DIR does not exist"
    exit 1
fi

cd "$BOTANY_DIR"

# Count PDFs
PDF_COUNT=$(ls -1 *.pdf 2>/dev/null | wc -l)
if [ "$PDF_COUNT" -eq 0 ]; then
    echo "❌ No PDF files found in $BOTANY_DIR"
    exit 1
fi

echo "📂 Found $PDF_COUNT PDF files to convert"
echo ""

# Activate virtual environment
source "$LIBRARIAN_DIR/venv/bin/activate"

# Step 1: Convert PDFs to Markdown
echo "================================"
echo "Step 1: Converting PDFs to Markdown"
echo "================================"
echo ""

CONVERTED=0
FAILED=0

for pdf in *.pdf; do
    if [ -f "$pdf" ]; then
        name="${pdf%.pdf}"
        md_file="${name}.md"

        echo "📄 Converting $pdf → $md_file"

        # Use pypdf to convert with proper Markdown structure
        # CRITICAL: Keep PDF file open while iterating pages
        python -c "
import sys
from pathlib import Path

def pdf_to_markdown(pdf_path, md_path):
    try:
        import pypdf

        # Open PDF and keep it open during extraction
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = pypdf.PdfReader(pdf_file)

        with open(md_path, 'w', encoding='utf-8') as f:
            # Document title
            f.write(f'# {pdf_path.stem}\n\n')
            f.write(f'**Source:** {pdf_path.name}\n\n')
            f.write(f'**Pages:** {len(pdf_reader.pages)}\n\n')
            f.write('---\n\n')

            # Extract each page while PDF is still open
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text and text.strip():
                    f.write(f'## Page {page_num}\n\n')
                    f.write(text)
                    f.write('\n\n')

        # Close PDF file
        pdf_file.close()
        return True

    except Exception as e:
        print(f'    Error: {e}', file=sys.stderr)
        return False

result = pdf_to_markdown(Path('$pdf'), Path('$md_file'))
sys.exit(0 if result else 1)
" 2>&1

        if [ $? -eq 0 ]; then
            # Verify file was created and has content
            if [ -f "$md_file" ] && [ -s "$md_file" ]; then
                SIZE=$(wc -c < "$md_file")
                echo "  ✅ Success ($SIZE bytes)"
                CONVERTED=$((CONVERTED + 1))
            else
                echo "  ❌ Failed (file not created or empty)"
                FAILED=$((FAILED + 1))
            fi
        else
            echo "  ❌ Failed (conversion error)"
            FAILED=$((FAILED + 1))
        fi
    fi
done

echo ""
echo "✅ Conversion complete: $CONVERTED succeeded, $FAILED failed"
echo ""

# Step 2: Remove old .txt files
echo "================================"
echo "Step 2: Removing old .txt files"
echo "================================"
echo ""

TXT_COUNT=$(ls -1 *.txt 2>/dev/null | wc -l)
if [ "$TXT_COUNT" -gt 0 ]; then
    echo "Found $TXT_COUNT .txt files to remove:"
    ls -1 *.txt | head -10
    echo ""
    echo "Deleting..."
    rm -f *.txt
    echo "✅ Removed $TXT_COUNT .txt files"
else
    echo "No .txt files found (already cleaned?)"
fi

echo ""

# Step 3: Rebuild library index
echo "================================"
echo "Step 3: Rebuilding Botany Library Index"
echo "================================"
echo ""

bash "$LIBRARIAN_DIR/scripts/rebuild_botany.sh"

echo ""
echo "================================"
echo "Conversion Complete!"
echo "================================"
echo ""
echo "📊 Summary:"
echo "  • PDFs converted: $CONVERTED"
echo "  • PDFs failed: $FAILED"
echo "  • .txt files removed: $TXT_COUNT"
echo "  • Library index rebuilt"
echo ""
echo "✅ Botany library now uses Markdown files for better AI responses!"
echo ""
