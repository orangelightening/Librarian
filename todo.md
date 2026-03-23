# Librarian MCP Server - TODO List

**Date**: 2026-03-23
**Status**: Active development, v0.3.0 released

---

## 🚨 Priority: CRITICAL - Fix Metadata Directory Bug

### 0. CRITICAL: Duplicate Metadata Directories Causing Stale Index

**Problem**: TWO metadata directories exist, causing tools to read from old index instead of current index.

**Locations found**:
- `/home/peter/development/librarian-mcp/metadata/index.json` (55 documents - current, correct)
- `/home/peter/development/librarian-mcp/.librarian/metadata/index.json` (52 documents - old, stale)

**Symptoms**:
- User rebuilds index, sees 55 documents in rebuild output
- Tools (list_indexed_documents) return 52 documents from March 22
- AI responses cite old/stale information
- Restarting MCP server doesn't fix it (cached in wrong location)

**Root cause**: MetadataStore somehow reading from `.librarian/metadata/` instead of `metadata/`

**Action required**:
1. **IMMEDIATE**: Remove old `.librarian/metadata/` directory
2. **Investigate**: Why does MetadataStore read from wrong location?
3. **Fix**: Ensure only ONE metadata location exists and is used
4. **Prevent**: Add migration/cleanup to remove old locations
5. **Document**: Add to setup/upgrading documentation

**Estimated time**: 2-3 hours (investigation + fix + testing)

**Status**: ✅ FIXED (commit c541f80)

**Fix implemented**:
1. MetadataStore now auto-detects and removes old .librarian/metadata/
2. clear_and_rebuild.sh cleans up both old and new locations
3. Backup created before removal for safety
4. Tested and working correctly

**Result**: Only one metadata location exists, stale index issue resolved

---

## 🎯 Priority: HIGH - Documentation Accuracy

### 1. Fix README.md Inaccuracies About Chonkie Implementation

**Problem**: README.md makes claims about Chonkie's document-type-aware chunking that aren't accurate.

**Lines to fix**:
- Line 191: "Respects document structure" - Misleading (SemanticChunker doesn't know document type)
- Line 249: "Preserves table structures from PDFs" - **FALSE** (pypdf linearizes tables)

**Action required**:
- Remove table handling claim or clarify it's for .md files, not PDFs
- Clarify we use SemanticChunker (one-size-fits-all), not specialized chunkers
- Be honest about what we actually do vs what Chonkie offers

**Estimated time**: 30 minutes

---

### 2. Add Architecture Documentation: PDF + Markdown Strategy

**Problem**: No explanation of why we use PDF + .md combination or our actual Chonkie implementation.

**Sections to add to ARCHITECTURE.md**:
1. **Our Chonkie Implementation** (honest technical details)
   - We use SemanticChunker on all files (not specialized chunkers)
   - pypdf for text extraction (linearizes tables, loses structure)
   - Why this approach is pragmatic and works well

2. **Marker PDF → Markdown Conversion** (why we do this)
   - Marker creates high-quality .md with structure, tables, links preserved
   - AI models prefer .md citations (cleaner text)
   - Storage efficiency: .md is ~1000x smaller than PDF
   - AI supplements .md with PDF when needed (best of both worlds)

3. **Why Not Use Chonkie's Specialized Chunkers?**
   - PDFChunker exists but we have better solution (Marker)
   - Current setup: PDF (human reading) + .md (AI chunking)
   - Future-proof: Multimodal models will read PDFs directly
   - Table handling tradeoff acceptable given other benefits

4. **Quality Comparison Table**
   - Current approach vs Chonkie PDFChunker vs Marker .md
   - Honest assessment of strengths/weaknesses

**Estimated time**: 1-2 hours

---

## 🎯 Priority: HIGH - New PDF Workflow

### 3. Create Automated New PDF Addition Script

**Problem**: When user adds new PDF to library, they need easy way to convert with Marker and clean up.

**Requirements**:
- Script: `scripts/add_pdf_to_library.sh`
- Usage: `./scripts/add_pdf_to_library.sh /path/to/new.pdf /path/to/library`
- Should:
  1. Create temp directory for conversion
  2. Run marker_single on PDF
  3. Move .md file to library (cleanup Marker's subdirectory mess)
  4. Move images to `.librarian/images/`
  5. Delete `_meta.json` files
  6. Move original PDF to library
  7. Rebuild library index
  8. Report success/failure clearly

**Automation opportunities**:
- Could watch directory for new PDFs (inotify)
- Could prompt user for library name if not specified
- Could validate PDF before conversion

**Estimated time**: 2-3 hours

---

### 4. Document Multi-Library Creation Workflow

**Problem**: Need clear documentation for adding/removing libraries.

**Create**: `docs/ADD_DELETE_LIBRARY.md`

**Sections**:
1. **Creating a New Library**
   - Directory structure
   - Environment variables
   - MCP server config template
   - Step-by-step walkthrough

2. **Removing a Library**
   - Stop MCP server
   - Delete library directory (or keep data)
   - Remove MCP server config
   - Clean up any cached data

3. **Library Migration**
   - Moving library to new location
   - Updating paths in MCP config
   - Rebuilding index if needed

4. **Examples**
   - Create research library
   - Create recipe library
   - Delete test library

**Estimated time**: 1 hour

---

## 🎯 Priority: MEDIUM - Documentation Improvements

### 5. Update docs/REBUILD_LIBRARY.md

**Add sections**:
- When to use Marker conversion vs pypdf
- Why PDF + .md combination improves AI responses
- How to check if PDFs have .md versions
- Troubleshooting: Missing .md files

**Estimated time**: 30 minutes

---

### 6. Update docs/MULTI_LIBRARY_SETUP.md

**Add sections**:
- PDF conversion workflow for new libraries
- Storage cost analysis (PDF vs .md)
- Recommended workflow for PDF-heavy libraries

**Estimated time**: 30 minutes

---

## 🎯 Priority: LOW - Nice to Have

### 7. Create Library Management Script

**Script**: `scripts/manage_library.sh`

**Features**:
- `./scripts/manage_library.sh create <name> <path>`
- `./scripts/manage_library.sh delete <name>`
- `./scripts/manage_library.sh list`
- `./scripts/manage_library.sh convert_pdfs <library>`
- Automates all MCP config creation

**Estimated time**: 3-4 hours

---

### 8. Add PDF Quality Metrics

**Idea**: Script to compare PDF vs .md quality

**Features**:
- Count tables in PDF vs .md
- Check for broken images
- Validate links in .md
- Report conversion quality score

**Estimated time**: 2 hours

---

## 📋 Summary

**Must do before next release**:
1. ✅ Fix README.md table handling claim
2. ✅ Add honest architecture documentation
3. ✅ Create add_pdf_to_library.sh script
4. ✅ Document add/delete library workflow

**Should do soon**:
5. Update REBUILD_LIBRARY.md
6. Update MULTI_LIBRARY_SETUP.md

**Nice to have**:
7. Library management script
8. PDF quality metrics

---

## 🎯 Next Session Goals

1. **Priority 1**: Fix README.md (15 min)
2. **Priority 2**: Add architecture documentation (1 hour)
3. **Priority 3**: Create add_pdf_to_library.sh (2 hours)
4. **Priority 4**: Document add/delete library (30 min)

**Total estimated time**: ~4 hours

---

## 📝 Notes

- User feedback: "The models get most from the markdown file (most citations) and supplement from the pdf to produce the response"
- Storage efficiency: .md is ~1000x smaller than PDF with images
- Quality improvement: "HUGE DIFFERENCE" between pypdf and Marker .md
- Tradeoff accepted: Marker sometimes breaks tables crossing page boundaries
- User satisfied with current quality despite not using Chonkie's specialized chunkers

**Key principle**: Be honest about implementation, don't overclaim capabilities.
