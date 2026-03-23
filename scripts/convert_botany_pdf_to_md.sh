#!/bin/bash
# Convert PDFs to Markdown using Marker (GPU-free, excellent quality)
# Marker preserves structure, tables, images, links, and formatting

BOTANY_DIR="/home/peter/botany"
LIBRARIAN_DIR="/home/peter/development/librarian-mcp"

echo "================================"
echo "Botany Library: PDF → Markdown Conversion (Marker)"
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

        # Use Marker to convert (preserves structure, tables, images, links)
        marker "$pdf" -o "$md_file" 2>&1

        if [ $? -eq 0 ]; then
            # Verify file was created and has content
            if [ -f "$md_file" ] && [ -s "$md_file" ]; then
                SIZE=$(wc -c < "$md_file")
                LINES=$(wc -l < "$md_file")
                echo "  ✅ Success ($SIZE bytes, $LINES lines)"
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

# Step 2: Remove old .txt files and backup files
echo "================================"
echo "Step 2: Removing old .txt and backup files"
echo "================================"
echo ""

TXT_COUNT=$(ls -1 *.txt 2>/dev/null | wc -l)
BACKUP_COUNT=$(ls -1 *1.md 2>/dev/null | wc -l)

if [ "$TXT_COUNT" -gt 0 ] || [ "$BACKUP_COUNT" -gt 0 ]; then
    if [ "$TXT_COUNT" -gt 0 ]; then
        echo "Found $TXT_COUNT .txt files to remove"
        rm -f *.txt
        echo "✅ Removed .txt files"
    fi

    if [ "$BACKUP_COUNT" -gt 0 ]; then
        echo "Found $BACKUP_COUNT backup files (*1.md) to remove"
        rm -f *1.md
        echo "✅ Removed backup files"
    fi
else
    echo "No old files found (already cleaned?)"
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
echo "  • Old files removed: $((TXT_COUNT + BACKUP_COUNT))"
echo "  • Library index rebuilt"
echo ""
echo "✅ Botany library now uses high-quality Markdown from Marker!"
echo ""
echo "📝 Note: Marker extracts images as separate files (_page_*_Picture_*.jpeg)"
echo ""
