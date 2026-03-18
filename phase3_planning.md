# Phase 3 Planning - Multi-User HTTP Server

**Created**: 2026-03-17
**Status**: Planning Phase
**Priority**: High

---

## Overview

Phase 3 transforms the Librarian MCP Server from a single-user local tool into a multi-user networked service. This document outlines planned features, implementation approaches, and architectural decisions for Phase 3 development.

**⚠️ Architecture Update**: Testing revealed that LM Studio's HTTP API does NOT expose MCP tools to the model. Phase 3A now requires **TWO HTTP layers**:
1. **FastMCP HTTP Transport** - For MCP clients (Jan, LM Studio chat)
2. **Direct HTTP API** - For validation scripts and automation (bypasses LM Studio API limitations)

## Core Objectives

1. **Network Access**: Enable HTTP transport for LAN/WAN access
2. **Multi-User Support**: Multiple concurrent users with authentication
3. **Advanced Document Processing**: Document-type specific chunking
4. **Multi-Library Support**: Separate document collections with directed queries
5. **Production Hardening**: Security, monitoring, and reliability

---

## 🎯 Quick Win: Phase 3A + 3H (Immediate Automation)

### The High-ROI Subset

**For single-user deployments**, you can get **80% of Phase 3's automation value** with **20% of the effort** by implementing just:

1. **Phase 3A**: HTTP Transport Foundation
2. **Phase 3H**: Automated Validation Pipeline

### What You Get Right Now

**Automated Validation Without Manual Intervention**:
```bash
# Before: Manual context management, server restarts, tool call cleanup
# After: One script, done

./scripts/run_validation.sh
# → 16 independent HTTP calls
# → Fresh 32k context per query
# → Zero cross-contamination
# → Automated report generation
```

### What You DON'T Need (Yet)

**Skip until you actually need multi-user**:
- ❌ Phase 3B: Authentication & Authorization (single user = no auth needed)
- ❌ Phase 3C: Multi-User Data Isolation (no other users to isolate from)
- ❌ Phase 3D: Concurrency Control (you're not concurrent with yourself)
- ❌ Phase 3E: Production Hardening (local deployment = simpler security)

### Immediate Benefits

**For Development**:
- ✅ **Automated documentation validation** - catch drift immediately
- ✅ **Zero manual context management** - HTTP handles fresh context automatically
- ✅ **Cron-friendly testing** - run overnight, read reports in morning
- ✅ **Regression testing** - verify changes don't break accuracy

**For Quality Assurance**:
- ✅ **Systematic testing** - every validation query gets full 32k context
- ✅ **Repeatable results** - same test, same quality, every time
- ✅ **Historical tracking** - compare accuracy over time
- ✅ **Pre-release validation** - automated testing before documentation updates

### Implementation Priority

**Phase 1: Quick Win (1-2 weeks)**
1. Phase 3A: HTTP Transport - Foundation
2. Phase 3H: Batch Validation - Immediate automation payoff

**Phase 2: Scale (When needed)**
3. Phase 3B-G: Remaining features when multi-user becomes necessary

### The Math

**Quick Win Implementation**:
- Phase 3A: ~1 week (HTTP transport is built into FastMCP)
- Phase 3H: ~1 week (shell script + HTTP integration)
- **Total: 2 weeks for automated validation**

**Full Phase 3 Implementation**:
- All sub-phases: 4-6 weeks
- **Quick Win: 33-50% of the effort, 80% of the automation value**

### Decision Matrix

| Feature | Single User | Multi-User | Priority |
|---------|-------------|------------|----------|
| **Phase 3A: HTTP Transport** | ✅ Essential | ✅ Essential | **DO FIRST** |
| **Phase 3H: Batch Validation** | ✅ High Value | ✅ High Value | **DO FIRST** |
| Phase 3B: Authentication | ❌ Not needed | ✅ Essential | Later |
| Phase 3C: Data Isolation | ❌ Not needed | ✅ Essential | Later |
| Phase 3D: Concurrency Control | ❌ Not needed | ✅ Essential | Later |
| Phase 3E: Production Hardening | ⚠️ Nice to have | ✅ Essential | Later |
| Phase 3F: Document Chunking | ✅ Useful | ✅ Useful | Optional |
| Phase 3G: Multi-Library | ✅ Useful | ✅ Useful | Optional |

### Success Criteria for Quick Win

- [ ] HTTP server operational (`--transport http`)
- [ ] Validation script executes all 16 queries
- [ ] Each query gets fresh context (zero contamination)
- [ ] Automated report generation working
- [ ] Can run via cron with zero manual intervention
- [ ] Response quality consistent across all queries

---

## Phase 3A: Detailed Deliverables

### Architecture Update: Dual HTTP Implementation

**Critical Discovery**: LM Studio's HTTP API does NOT expose MCP tools to the model. The model only has built-in knowledge, not access to MCP tools like `search_library`, `sync_documents`, etc.

**Solution**: Implement **TWO HTTP layers**:

```
┌─────────────────────────────────────────────────────────┐
│                   Librarian HTTP Server                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Layer 1: FastMCP HTTP Transport                        │
│  ├── For MCP clients (Jan, LM Studio chat, Claude)      │
│  ├── Exposes tools via MCP protocol over HTTP           │
│  └── Tools: search_library, sync_documents, etc.        │
│                                                           │
│  Layer 2: Direct HTTP API (NEW!)                        │
│  ├── For validation scripts and automation              │
│  ├── REST endpoints that call tools directly            │
│  └── No MCP protocol - pure HTTP requests               │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Why Both Layers**:
- **Layer 1** enables MCP clients to connect over HTTP instead of stdio
- **Layer 2** enables automated validation scripts (bypassing LM Studio API limitations)

---

### 1. FastMCP HTTP Transport (Layer 1)

**Purpose**: Enable MCP clients to connect over HTTP

**Implementation**:
```python
# mcp_server/librarian_mcp.py
def main():
    mcp = FastMCP("librarian")

    # Register tools...
    register_library_tools(mcp)
    register_cli_tools(mcp, safe_dir)

    # NEW: HTTP transport support
    transport = os.getenv("LIBRARIAN_TRANSPORT", "stdio")
    if transport == "http":
        host = os.getenv("LIBRARIAN_HOST", "0.0.0.0")
        port = int(os.getenv("LIBRARIAN_PORT", "8000"))
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run(transport="stdio")
```

**Configuration**:
```bash
# Environment variables
export LIBRARIAN_TRANSPORT=http
export LIBRARIAN_HOST=0.0.0.0
export LIBRARIAN_PORT=8000

# Or CLI flags
python mcp_server/librarian_mcp.py --transport http --host 0.0.0.0 --port 8000
```

**Deliverable**: MCP-over-HTTP server at `http://localhost:8000` for MCP clients

---

### 2. Direct HTTP API (Layer 2) - NEW!

**Purpose**: Enable validation scripts and automation tools to call librarian tools directly via HTTP

**Implementation**:
```python
# mcp_server/http_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Librarian HTTP API")

# Core business logic (shared with MCP tools)
from mcp_server.core.document_manager import DocumentManager
from mcp_server.backend.factory import get_backend
from mcp_server.core.metadata_store import MetadataStore
from mcp_server.core.ignore_patterns import IgnorePatterns

# Initialize singletons
backend = get_backend()
metadata = MetadataStore()
ignore_patterns = IgnorePatterns()
doc_manager = DocumentManager(backend, metadata, ignore_patterns)

# Request/Response models
class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class SearchResponse(BaseModel):
    results: list
    total_chunks: int

class SyncRequest(BaseModel):
    path: str
    extensions: list[str] = None
    recursive: bool = True

class SyncResponse(BaseModel):
    added: int
    updated: int
    unchanged: int
    removed: int
    errors: list[str]

# HTTP endpoints
@app.post("/search_library", response_model=SearchResponse)
def search_library(request: SearchRequest) -> SearchResponse:
    """
    Search library via HTTP API (bypasses MCP protocol).

    Args:
        request: SearchRequest with query and limit

    Returns:
        SearchResponse with results and metadata
    """
    try:
        results = doc_manager.backend.query(request.query, limit=request.limit)
        return SearchResponse(
            results=results,
            total_chunks=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync_documents", response_model=SyncResponse)
def sync_documents(request: SyncRequest) -> SyncResponse:
    """
    Sync documents via HTTP API (bypasses MCP protocol).

    Args:
        request: SyncRequest with path, extensions, recursive flag

    Returns:
        SyncResponse with sync statistics
    """
    try:
        result = doc_manager.sync_directory(
            path=request.path,
            extensions=set(request.extensions) if request.extensions else None,
            recursive=request.recursive
        )
        return SyncResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    """Get library statistics via HTTP API."""
    try:
        return doc_manager.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "librarian-http-api"}

# Server startup
def run_http_api(host: str = "0.0.0.0", port: int = 8001):
    """Run the HTTP API server."""
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    run_http_api()
```

**Configuration**:
```bash
# Environment variables
export LIBRARIAN_HTTP_API_ENABLED=true
export LIBRARIAN_HTTP_API_HOST=0.0.0.0
export LIBRARIAN_HTTP_API_PORT=8001

# Run separately from MCP transport
python mcp_server/http_api.py --host 0.0.0.0 --port 8001
```

**Or run alongside MCP transport**:
```python
# mcp_server/librarian_mcp.py
def main():
    # ... MCP setup ...

    # Start HTTP API in separate thread if enabled
    if os.getenv("LIBRARIAN_HTTP_API_ENABLED", "false").lower() == "true":
        import threading
        from mcp_server.http_api import run_http_api

        http_thread = threading.Thread(
            target=run_http_api,
            kwargs={
                "host": os.getenv("LIBRARIAN_HTTP_API_HOST", "0.0.0.0"),
                "port": int(os.getenv("LIBRARIAN_HTTP_API_PORT", "8001"))
            },
            daemon=True
        )
        http_thread.start()
        print(f"[librarian] HTTP API running on port {os.getenv('LIBRARIAN_HTTP_API_PORT', '8001')}")

    # Run MCP transport (stdio or HTTP)
    mcp.run(transport=transport, host=host, port=port)
```

**API Endpoints**:
```
POST /search_library    → Semantic search
POST /sync_documents    → Sync directory
GET  /stats            → Library statistics
GET  /health           → Health check
```

**Deliverable**: HTTP API server at `http://localhost:8001` for automation

**Usage Example**:
```bash
# Direct HTTP API call (bypasses LM Studio entirely)
curl -X POST http://localhost:8001/search_library \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the librarian capabilities?", "limit": 5}'

# Response: Direct search results with citations
```

---

### 3. Parse `library_validation.md` Function

**Implementation**:
```python
# scripts/parse_validation.py
import re
from pathlib import Path
from typing import List, Dict

def parse_validation_md(filepath: str = "library_validation.md") -> List[Dict]:
    """
    Parse library_validation.md and extract query metadata.

    Returns:
        List of dicts with keys: number, query, description
    """
    queries = []
    current_query = None

    with open(filepath, 'r') as f:
        for line in f:
            # Match "## Query N: Description"
            if line.startswith("## Query "):
                if current_query:
                    queries.append(current_query)

                match = re.match(r'## Query (\d+): (.+)', line)
                if match:
                    query_num, description = match.groups()
                    current_query = {
                        'number': int(query_num),
                        'description': description.strip(),
                        'query': '',
                        'expected_outcome': ''
                    }

            # Capture query content (code blocks)
            elif line.strip().startswith('Query:'):
                current_query['query'] = line.split('Query:', 1)[1].strip()

    if current_query:
        queries.append(current_query)

    return queries

# CLI interface
if __name__ == "__main__":
    queries = parse_validation_md()
    print(f"Found {len(queries)} validation queries")
    for q in queries:
        print(f"Query {q['number']}: {q['description']}")
```

**Deliverable**: `scripts/parse_validation.py` that extracts validation queries

---

### 3. Batch Query Runner via Direct HTTP API

**Architecture Change**: Call Librarian HTTP API directly, NOT LM Studio API

**Implementation**:
```python
# scripts/run_batch_validation.py
import requests
import json
from pathlib import Path
from typing import List, Dict
from parse_validation import parse_validation_md

class BatchQueryRunner:
    """Run validation queries via Librarian HTTP API (direct tool access)"""

    def __init__(self, api_endpoint: str = "http://localhost:8001"):
        self.api_endpoint = api_endpoint
        self.search_endpoint = f"{api_endpoint}/search_library"

    def run_query(self, query: str, query_num: int) -> Dict:
        """
        Run a single validation query via Librarian HTTP API.

        Args:
            query: The validation query text
            query_num: Query number for tracking

        Returns:
            Dict with response metadata and content
        """
        payload = {
            "query": query,
            "limit": 5
        }

        try:
            response = requests.post(
                self.search_endpoint,
                json=payload,
                timeout=120  # 2 minute timeout
            )
            response.raise_for_status()

            result = response.json()

            # Format results with citations
            formatted_content = self._format_results(result['results'], query)

            return {
                'query_num': query_num,
                'status': 'success',
                'content': formatted_content,
                'total_chunks': result['total_chunks']
            }

        except Exception as e:
            return {
                'query_num': query_num,
                'status': 'error',
                'error': str(e)
            }

    def _format_results(self, results: List[Dict], query: str) -> str:
        """Format search results into librarian-style response with citations"""
        if not results:
            return f"No results found for query: {query}"

        formatted = []
        formatted.append(f"# Search Results for: {query}\n\n")

        for i, result in enumerate(results, 1):
            formatted.append(f"## Result {i}\n")
            formatted.append(f"{result['text']}\n\n")
            formatted.append(f"**Source**: {result.get('metadata', {}).get('source', 'Unknown')}\n")
            formatted.append(f"**Similarity**: {result.get('similarity_score', 0):.2f}\n\n")

        return ''.join(formatted)

    def run_batch(self, queries: List[Dict]) -> List[Dict]:
        """
        Run all validation queries.

        Args:
            queries: List of query dicts from parse_validation_md()

        Returns:
            List of response dicts
        """
        results = []
        total = len(queries)

        for i, query_obj in enumerate(queries, 1):
            print(f"[{i}/{total}] Running Query {query_obj['number']}: {query_obj['description']}")

            result = self.run_query(query_obj['query'], query_obj['number'])
            results.append(result)

            status = "✓" if result['status'] == 'success' else '✗'
            print(f"  {status} Query {query_obj['number']} complete")

        return results

# CLI interface
if __name__ == "__main__":
    import sys

    api_endpoint = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001"

    queries = parse_validation_md()
    runner = BatchQueryRunner(api_endpoint)
    results = runner.run_batch(queries)

    print(f"\nComplete: {len(results)} queries processed")
```

**Key Changes**:
- ✅ Calls `http://localhost:8001/search_library` (Librarian API)
- ❌ No longer calls LM Studio API (doesn't have MCP tools)
- ✅ Direct tool access via HTTP
- ✅ No LLM model needed - pure librarian search

**Deliverable**: `scripts/run_batch_validation.py` that queries librarian directly

---

---

### 4. Response File Writer

**Implementation**:
```python
# scripts/write_responses.py
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class ResponseWriter:
    """Write validation responses to organized directory structure"""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_dir = f"reports/validation_{timestamp}"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (self.output_dir / "responses").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)

    def write_response(self, query_num: int, content: str, metadata: Dict) -> str:
        """
        Write individual response to file.

        Args:
            query_num: Query number
            content: Response content
            metadata: Query metadata (description, tokens, etc.)

        Returns:
            Path to written file
        """
        # Format: response_001.md, response_002.md, etc.
        filename = f"response_{query_num:03d}.md"
        filepath = self.output_dir / "responses" / filename

        # Write response with metadata header
        with open(filepath, 'w') as f:
            f.write(f"# Query {query_num}: {metadata.get('description', 'Unknown')}\n\n")
            f.write(f"**Status**: {metadata.get('status', 'unknown')}\n")
            f.write(f"**Tokens Used**: {metadata.get('tokens_used', 0)}\n")
            f.write(f"**Timestamp**: {datetime.now().isoformat()}\n\n")
            f.write("---\n\n")
            f.write(content)

        return str(filepath)

    def write_all(self, results: List[Dict], queries: List[Dict]) -> List[str]:
        """
        Write all validation responses.

        Args:
            results: List of response dicts from BatchQueryRunner
            queries: List of query dicts for metadata

        Returns:
            List of written file paths
        """
        written = []

        for result in results:
            query_num = result['query_num']

            # Find matching query metadata
            query_meta = next((q for q in queries if q['number'] == query_num), {})

            filepath = self.write_response(
                query_num,
                result.get('content', ''),
                {
                    'description': query_meta.get('description', ''),
                    'status': result['status'],
                    'tokens_used': result.get('tokens_used', 0),
                    'error': result.get('error', '')
                }
            )

            written.append(filepath)

        return written

# CLI interface
if __name__ == "__main__":
    from run_batch_validation import BatchQueryRunner
    from parse_validation import parse_validation_md

    queries = parse_validation_md()
    runner = BatchQueryRunner()
    results = runner.run_batch(queries)

    writer = ResponseWriter()
    written = writer.write_all(results, queries)

    print(f"\nWritten {len(written)} response files to {writer.output_dir}")
```

**Deliverable**: `scripts/write_responses.py` that writes organized response files

---

### 5. Comparison Report Generator

**Implementation**:
```python
# scripts/generate_report.py
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class ReportGenerator:
    """Generate comparison and summary reports for validation results"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.responses_dir = self.output_dir / "responses"

    def analyze_response(self, filepath: Path) -> Dict:
        """
        Analyze individual response for quality metrics.

        Returns:
            Dict with analysis results
        """
        content = filepath.read_text()

        return {
            'file': filepath.name,
            'has_citations': '[Source:' in content,
            'citation_count': content.count('[Source:'),
            'line_count': len(content.split('\n')),
            'char_count': len(content),
            'has_errors': 'error' in content.lower() or 'not found' in content.lower()
        }

    def generate_summary(self) -> Dict:
        """
        Analyze all responses and generate summary statistics.

        Returns:
            Summary dict with metrics
        """
        response_files = sorted(self.responses_dir.glob("response_*.md"))

        if not response_files:
            return {'error': 'No response files found'}

        analyses = [self.analyze_response(f) for f in response_files]

        total_citations = sum(a['citation_count'] for a in analyses)
        files_with_citations = sum(1 for a in analyses if a['has_citations'])
        files_with_errors = sum(1 for a in analyses if a['has_errors'])

        return {
            'total_queries': len(response_files),
            'files_with_citations': files_with_citations,
            'total_citations': total_citations,
            'avg_citations_per_response': total_citations / len(response_files) if response_files else 0,
            'files_with_errors': files_with_errors,
            'timestamp': datetime.now().isoformat()
        }

    def generate_markdown_report(self) -> str:
        """
        Generate comprehensive markdown report.

        Returns:
            Markdown report content
        """
        summary = self.generate_summary()

        report = []
        report.append("# Librarian Validation Report\n")
        report.append(f"**Generated**: {summary['timestamp']}\n")
        report.append("---\n\n")

        # Executive Summary
        report.append("## Executive Summary\n\n")
        report.append(f"- **Total Queries**: {summary['total_queries']}\n")
        report.append(f"- **Responses with Citations**: {summary['files_with_citations']}/{summary['total_queries']}\n")
        report.append(f"- **Total Citations**: {summary['total_citations']}\n")
        report.append(f"- **Average Citations/Response**: {summary['avg_citations_per_response']:.1f}\n")
        report.append(f"- **Responses with Errors**: {summary['files_with_errors']}\n\n")

        # Quality Assessment
        report.append("## Quality Assessment\n\n")
        if summary['files_with_citations'] == summary['total_queries']:
            report.append("✅ **All responses include proper citations**\n\n")
        else:
            missing = summary['total_queries'] - summary['files_with_citations']
            report.append(f"⚠️ **{missing} responses missing citations**\n\n")

        if summary['files_with_errors'] == 0:
            report.append("✅ **No errors detected in responses**\n\n")
        else:
            report.append(f"⚠️ **{summary['files_with_errors']} responses contain errors**\n\n")

        # Detailed Analysis
        report.append("## Detailed Analysis\n\n")
        response_files = sorted(self.responses_dir.glob("response_*.md"))

        for f in response_files:
            analysis = self.analyze_response(f)
            status = "✓" if not analysis['has_errors'] else "✗"

            report.append(f"### {status} {analysis['file']}\n\n")
            report.append(f"- Citations: {analysis['citation_count']}\n")
            report.append(f"- Lines: {analysis['line_count']}\n")
            report.append(f"- Characters: {analysis['char_count']}\n\n")

        return ''.join(report)

    def write_report(self) -> str:
        """
        Generate and write summary report.

        Returns:
            Path to written report
        """
        report_content = self.generate_markdown_report()
        report_path = self.output_dir / "summary_report.md"

        report_path.write_text(report_content)

        # Also write JSON metadata
        metadata_path = self.output_dir / "metadata" / "summary.json"
        metadata_path.write_text(json.dumps(self.generate_summary(), indent=2))

        return str(report_path)

# CLI interface
if __name__ == "__main__":
    import sys

    output_dir = sys.argv[1] if len(sys.argv) > 1 else "reports/validation_latest"
    generator = ReportGenerator(output_dir)

    report_path = generator.write_report()
    print(f"Report generated: {report_path}")
```

**Deliverable**: `scripts/generate_report.py` that creates summary reports

---

### 6. Run Script with Progress Output

**Implementation**:
```bash
#!/bin/bash
# scripts/run_validation.sh

set -e

# Configuration
LIBRARIAN_API="${LIBRARIAN_API:-http://localhost:8001}"
OUTPUT_DIR="reports/validation_$(date +%Y-%m-%d_%H%M%S)"
PARSER_SCRIPT="scripts/parse_validation.py"
RUNNER_SCRIPT="scripts/run_batch_validation.py"
WRITER_SCRIPT="scripts/write_responses.py"
REPORT_SCRIPT="scripts/generate_report.py"

echo "======================================"
echo "Librarian Automated Validation Suite"
echo "======================================"
echo ""
echo "Librarian API Endpoint: $LIBRARIAN_API"
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Check if librarian HTTP API is running
echo "[0/6] Checking Librarian HTTP API..."
if ! curl -s "$LIBRARIAN_API/health" > /dev/null 2>&1; then
    echo "✗ Librarian HTTP API not responding at $LIBRARIAN_API"
    echo ""
    echo "Please start the Librarian HTTP API:"
    echo "  export LIBRARIAN_HTTP_API_ENABLED=true"
    echo "  python mcp_server/librarian_mcp.py --transport http"
    echo ""
    exit 1
fi
echo "✓ Librarian HTTP API is running"
echo ""

# Step 1: Parse validation queries
echo "[1/6] Parsing validation queries..."
python3 $PARSER_SCRIPT
echo "✓ Queries parsed"
echo ""

# Step 2: Run batch validation
echo "[2/6] Running batch validation queries..."
python3 $RUNNER_SCRIPT "$LIBRARIAN_API"
echo "✓ Batch queries complete"
echo ""

# Step 3: Write response files
echo "[3/6] Writing response files..."
python3 $WRITER_SCRIPT --output "$OUTPUT_DIR"
echo "✓ Responses written to $OUTPUT_DIR/responses/"
echo ""

# Step 4: Generate summary report
echo "[4/6] Generating summary report..."
python3 $REPORT_SCRIPT "$OUTPUT_DIR"
echo "✓ Report generated: $OUTPUT_DIR/summary_report.md"
echo ""

# Step 5: Display summary
echo "[5/6] Validation Complete!"
echo "======================================"
echo ""
echo "Results:"
echo "  - Librarian API: $LIBRARIAN_API"
echo "  - Output Directory: $OUTPUT_DIR"
echo "  - Summary Report: $OUTPUT_DIR/summary_report.md"
echo "  - Response Files: $(ls $OUTPUT_DIR/responses/ 2>/dev/null | wc -l) files"
echo ""
echo "View results:"
echo "  cat $OUTPUT_DIR/summary_report.md"
echo ""

# Step 6: Open report if possible
echo "[6/6] Opening summary report..."
if command -v xdg-open > /dev/null; then
    xdg-open "$OUTPUT_DIR/summary_report.md" 2>/dev/null &
elif command -v open > /dev/null; then
    open "$OUTPUT_DIR/summary_report.md" 2>/dev/null &
else
    echo "Manual open: cat $OUTPUT_DIR/summary_report.md"
fi
echo ""
```

**Deliverable**: `scripts/run_validation.sh` with progress tracking and health checks

**Usage**:
```bash
# Default (localhost:8001)
./scripts/run_validation.sh

# Custom endpoint
LIBRARIAN_API=http://localhost:9000 ./scripts/run_validation.sh

# Cron job (daily at 2 AM)
0 2 * * * /path/to/librarian-mcp/scripts/run_validation.sh
```

---

### When to Implement Remaining Phase 3

**Implement Phase 3B-G when**:
- You need to share the librarian with multiple users
- You need user-specific document collections
- You're deploying to a production environment
- You need team collaboration features

**Stay with Quick Win when**:
- Single-user deployment
- Local development environment
- Personal documentation management
- No need for user isolation

---

## Phase 3A: HTTP Transport Foundation

### Objectives
- Replace stdio transport with HTTP/WebSocket server
- Enable network access for local developer teams
- Maintain backward compatibility with stdio mode

### Implementation

**FastMCP HTTP Support** (Already built-in):
```python
# librarian_mcp.py
mcp.run(transport="http", host="0.0.0.0", port=8000)
```

**Configuration**:
```bash
# Environment variable
export LIBRARIAN_TRANSPORT=http
export LIBRARIAN_HOST=0.0.0.0
export LIBRARIAN_PORT=8000

# CLI flags
python mcp_server/librarian_mcp.py \
  --transport http \
  --host 0.0.0.0 \
  --port 8000
```

**Benefits**:
- ✅ Local network access (developer teams)
- ✅ Multiple simultaneous connections
- ✅ No client-side MCP server needed
- ✅ Browser-based testing possible

**Considerations**:
- Requires authentication (Phase 3B)
- Security hardening (Phase 3E)
- Firewall configuration
- SSL/TLS for production

---

## Phase 3B: Authentication & Authorization

### Security Layers

**Regular User Access** (unauthenticated):
- `search_library` ✅
- `list_indexed_documents` ✅
- `get_document_status` ✅
- `get_library_stats` ✅
- `add_document` (to user's namespace) ✅
- `sync_documents` (to user's namespace) ✅

**Admin Access** (authentication required):
- `clear_database` ⚠️ - Destructive operation
- `rebuild_library` ⚠️ - Full database rebuild
- `remove_any_document` ⚠️ - Cross-user document removal
- `manage_users` ⚠️ - User management operations
- `get_audit_log` - Security and compliance auditing
- `get_system_stats` - Cross-user statistics

### Authentication Methods

**API Key Authentication** (Simple):
```python
# Environment variable
LIBRARIAN_API_KEYS="key1:key2:key3"

# Config file
api_keys:
  - admin: "secret-admin-key"
  - user1: "user-key-123"
```

**Password Authentication**:
```python
# Simple password verification
@mcp.tool(admin_only=True)
def clear_database(admin_password: str) -> str:
    if not verify_admin_password(admin_password):
        return "Unauthorized: Admin access required"
```

**JWT Token Authentication** (Advanced):
- User login endpoint
- JWT token generation
- Token validation middleware
- Token refresh mechanism

### User Model

**SQLite User Store**:
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT, -- 'admin' or 'user'
    created_at TIMESTAMP,
    last_login TIMESTAMP
);
```

---

## Phase 3C: Multi-User Data Isolation

### Approach: Per-User Collections

**ChromaDB Collection Strategy**:
```python
# User-prefixed collections
collections = {
    'user1': 'documents_user1',
    'user2': 'documents_user2',
    'user3': 'documents_user3'
}
```

**Benefits**:
- ✅ Complete data isolation
- ✅ No cross-user interference
- ✅ Easy user deletion (drop collection)
- ✅ Per-user statistics

**Metadata Isolation**:
```python
# Per-user metadata stores
metadata/
├── user1_index.json
├── user2_index.json
└── user3_index.json
```

### Namespace Separation

**Document IDs**:
```python
# User-scoped document IDs
user1_doc_id = hashlib.sha256(f"user1:{file_path}").hexdigest()
user2_doc_id = hashlib.sha256(f"user2:{file_path}").hexdigest()
```

**Query Isolation**:
```python
def search_library(query: str, user: str) -> str:
    collection = get_collection(f"documents_{user}")
    return collection.query(query)
```

---

## Phase 3D: Concurrency Control

### Thread-Safe Singletons

**Current Issue**:
```python
# NOT thread-safe
_backend = None
def get_backend():
    global _backend
    if _backend is None:  # Race condition!
        _backend = create_backend()
    return _backend
```

**Fixed Version**:
```python
import threading

_backend = None
_backend_lock = threading.Lock()

def get_backend():
    global _backend
    if _backend is None:
        with _backend_lock:
            if _backend is None:  # Double-check
                _backend = create_backend()
    return _backend
```

### File Locking for Metadata

**Current Issue**:
```python
# NOT safe for concurrent writes
def _save_index(self):
    with open(self.index_file, 'w') as f:
        json.dump(self._index, f)
```

**Fixed Version**:
```python
import fcntl

def _save_index(self):
    with open(self.index_file, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
        json.dump(self._index, f)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)  # Release
```

### Database Transactions

**SQLite for Metadata**:
```python
import sqlite3

def add_document_metadata(self, metadata: dict):
    with self.conn:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO documents (id, metadata) VALUES (?, ?)",
            (metadata['id'], json.dumps(metadata))
        )
        # Automatic commit/rollback
```

---

## Phase 3E: Production Hardening

### HTTPS/TLS Support

**SSL Configuration**:
```python
# Uvicorn SSL config
import uvicorn

uvicorn.run(
    app,
    host="0.0.0.0",
    port=8443,
    ssl_certfile="/path/to/cert.pem",
    ssl_keyfile="/path/to/key.pem"
)
```

### Rate Limiting

**Per-User Rate Limits**:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_user_id)

@mcp.tool()
@limiter.limit("10/minute")
def search_library(query: str) -> str:
    # Rate limited to 10 searches per minute per user
```

### Audit Logging

**Security Audit Trail**:
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    action TEXT, -- 'search', 'add_doc', 'remove_doc'
    timestamp TIMESTAMP,
    details TEXT
);
```

**Log Actions**:
- Document additions/removals
- Admin operations
- Failed authentication attempts
- Large queries

### Monitoring

**Health Checks**:
```python
@mcp.tool()
def health_check() -> str:
    """System health status"""
    return {
        "status": "healthy",
        "database": "connected",
        "users": count_users(),
        "documents": count_documents()
    }
```

---

## Phase 3F: Document-Type Specific Chunking

### Problem Statement

Current RecursiveChunker treats all documents equally, but different document types have different optimal chunking strategies.

### Examples

**PDFs with tables**:
- Need table-aware chunking
- Preserve row/column relationships
- Don't break table structures

**DOCX documents**:
- Have heading structures
- Section-based chunking better
- Respect document hierarchy

**Code files**:
- Should chunk at function/class boundaries
- Preserve code blocks
- Syntax-aware splitting

**Markdown files**:
- Already have semantic structure
- Header-based chunking
- Preserve section relationships

**HTML documents**:
- Tag-based structure
- Element-aware chunking
- Preserve semantic HTML

### Implementation

**File Type Detection**:
```python
DOCUMENT_CHUNKERS = {
    '.pdf': PDFTableChunker(),      # Table-aware, preserves structure
    '.docx': DOCXStructureChunker(), # Heading-aware, respects sections
    '.py': PythonFunctionChunker(),  # Function/class boundaries
    '.js': JavaScriptModuleChunker(),# Module/function boundaries
    '.md': MarkdownSectionChunker(), # Header-based chunking
    '.html': HTMLTagChunker(),       # Tag-aware chunking
    '.txt': RecursiveChunker(),      # Default: current Chonkie
}

def get_chunker_for_file(file_path: str):
    ext = Path(file_path).suffix.lower()
    return DOCUMENT_CHUNKERS.get(ext, RecursiveChunker())
```

**Chonkie Chunkers Available**:
- `RecursiveChunker` (current)
- `SemanticChunker` (requires embeddings)
- `TokenChunker` (fixed token chunks)
- `SentenceChunker` (sentence-based)
- `CodeChunker` (code-aware)
- `PDFChunker` (PDF with tables)
- `MarkdownChunker` (markdown-aware)
- `HTMLChunker` (tag-aware)

### Benefits

- **Better search results**: Code finds full functions, not fragments
- **Preserved structures**: Tables remain intact
- **Respected semantics**: Document structure guides chunking
- **Improved quality**: Specialized handling per document type

---

## Phase 3G: Multi-Library Support

### Use Cases

**Personal Organization**:
- 📚 **Personal projects** vs **Work documents**
- 🎯 **Research papers** vs **Documentation**
- 💻 **Code references** vs **Technical specs**

**Team Collaboration**:
- 👥 **Team A's library** vs **Team B's library**
- 🏢 **Department-specific** collections
- 🔐 **Confidential** vs **Public** documents

**Project Isolation**:
- 📦 **Project Alpha docs**
- 📦 **Project Beta docs**
- 📦 **Shared reference library**

### Architecture: Separate ChromaDB Collections

**Recommended Approach**:
```python
# Each library = separate ChromaDB collection
libraries = {
    'personal': 'documents_personal',
    'work': 'documents_work',
    'project-alpha': 'documents_project_alpha'
}
```

**Benefits**:
- ✅ **True isolation** - completely separate data
- ✅ **Performance** - smaller collections = faster queries
- ✅ **Flexibility** - different chunking per library
- ✅ **Easy management** - delete/export by collection
- ✅ **Natural** - fits ChromaDB's design

### API Design

**Library Management**:
```python
@mcp.tool()
def create_library(name: str, description: str = "") -> str:
    """Create a new document library"""

@mcp.tool()
def list_libraries() -> str:
    """List all available libraries"""

@mcp.tool()
def delete_library(name: str) -> str:
    """Delete a library and all its documents"""

@mcp.tool()
def get_library_stats(library: str = None) -> str:
    """Get statistics for specific library or all libraries"""
```

**Directed Queries**:
```python
@mcp.tool()
def search_library(query: str, library: str = "default") -> str:
    """Search a specific library (default: all libraries)"""

@mcp.tool()
def add_document(path: str, library: str = "default") -> str:
    """Add document to specific library"""

@mcp.tool()
def sync_documents(path: str, library: str = "default") -> str:
    """Sync documents to specific library"""
```

### Configuration

**Library Definitions**:
```python
# config/libraries.yaml
libraries:
  default:
    path: ~/documents
    backend: chonkie
    extensions: ['.md', '.txt', '.py']

  work:
    path: ~/work/docs
    backend: chonkie
    extensions: ['.md', '.pdf', '.docx']

  personal:
    path: ~/personal
    backend: chonkie
    extensions: ['.md', '.txt']
```

### Cross-Library Search

**Implementation**:
```python
def search_all_libraries(query: str) -> str:
    """Search across all libraries"""
    all_results = []
    for library_name in list_libraries():
        collection = get_collection(library_name)
        results = collection.query(query)
        all_results.extend(results)
    return aggregate_results(all_results)
```

---

## Phase 3H: Automated Validation Pipeline

### Overview

Automated validation suite that runs systematic tests against the librarian's documentation accuracy using fresh HTTP requests for each query - no manual context window management required.

### The Problem: Manual Context Management

Current validation testing requires:
- Manual context window monitoring
- Restarting the librarian between queries
- Managing accumulated tool call history
- Context pressure affecting response quality
- Time-consuming manual process

### The Solution: HTTP-Based Fresh Context

**Shell Script Driver**: `scripts/run_validation.sh`

```bash
#!/bin/bash
# run_validation.sh

QUERIES_FILE="library_validation.md"
OUTPUT_DIR="reports/validation_$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

# Extract individual queries from validation.md
# For each query:
#   1. Start fresh LLM context via API
#   2. Inject librarian system prompt
#   3. Run single query
#   4. Write response to response_NNN.md
#   5. Kill context
#   6. Next query - zero contamination
```

### The Key Insight

**LM Studio's API** means each query can be a completely independent HTTP call:

```python
# Each query is just:
response = requests.post("http://localhost:1234/v1/chat/completions",
    json={
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }
)

# Write response to file
# Done. Next query starts completely fresh.
```

### Benefits

- ✅ **Fresh context every time** - No accumulated history
- ✅ **Same system prompt** injected fresh per query
- ✅ **No context pressure** - Full 32k context per query
- ✅ **Maximum quality** - Every query gets full attention
- ✅ **Zero manual intervention** - Set it and forget it
- ✅ **Cron-friendly** - Run overnight, read reports in morning ☕

### Portability Consideration

**Initial Implementation**: LM Studio-specific HTTP API
- Uses `http://localhost:1234/v1/chat/completions` endpoint
- OpenAI-compatible API format

**Phase 3A Enhancement**: HTTP transport for Librarian MCP Server itself makes this portable to:
- ✅ Ollama's HTTP API
- ✅ LocalAI endpoints
- ✅ Any LLM with OpenAI-compatible APIs
- ✅ Cloud APIs (if desired)

**Abstract the Endpoint**:
```bash
# Configurable LLM endpoint
LLM_ENDPOINT="${LLM_ENDPOINT:-http://localhost:1234/v1/chat/completions}"

# Same validation logic, different endpoint
./run_validation.sh --endpoint "$LLM_ENDPOINT"
```

### Implementation

**Validation Script Features**:
```bash
# Run all validation queries
./scripts/run_validation.sh

# Run specific query only
./scripts/run_validation.sh --query 5

# Custom LLM endpoint
./scripts/run_validation.sh --endpoint http://localhost:8080/v1/chat/completions

# Output to custom directory
./scripts/run_validation.sh --output reports/valid_2026-03-18
```

**Report Format**:
```
reports/validation_2026-03-18/
├── response_001.md  # Query 1: What are the librarian's core capabilities?
├── response_002.md  # Query 2: How does the librarian handle document syncing?
├── response_003.md  # Query 3: What tools does the librarian provide?
...
├── summary.md       # Overall pass/fail, issues found, recommendations
└── metadata.json    # Timestamps, query counts, response times
```

**MCP Tool Integration**:
```python
@mcp.tool()
def run_validation_suite(
    queries_file: str = "library_validation.md",
    output_dir: str = None
) -> str:
    """
    Run automated validation suite against library documentation.

    Returns summary report with pass/fail status and recommendations.
    """
    # Execute all validation queries via HTTP
    # Generate summary report
    # Return path to results
```

### Use Cases

**Continuous Validation**:
```bash
# Run daily via cron
0 2 * * * /path/to/librarian-mcp/scripts/run_validation.sh

# Check results in morning
ls -lt reports/validation_*/
```

**Pre-Release Testing**:
```bash
# Validate documentation before release
./scripts/run_validation.sh --output reports/pre_release_test
```

**Regression Testing**:
```bash
# After major changes, verify documentation still accurate
./scripts/run_validation.sh --baseline reports/known_good/
```

### Success Metrics

- [ ] All 16 validation queries pass
- [ ] Zero stale information detected
- [ ] All citations reference actual files
- [ ] No contradictory information
- [ ] Response quality consistent across queries

### Benefits Summary

**For Development**:
- Catch documentation drift immediately
- Verify librarian accuracy automatically
- Test after every documentation change
- Zero manual effort required

**For Users**:
- Confidence in librarian's accuracy
- Up-to-date information guaranteed
- Transparent validation process
- Historical accuracy tracking

**For Quality Assurance**:
- Systematic testing approach
- Repeatable validation process
- Automated regression testing
- Quality metrics over time

---

## Implementation Priority

### Phase 3A: HTTP Transport + Batch Validation (Quick Win)

**Deliverables** (in order):
1. ✅ FastMCP HTTP transport (Layer 1) - `mcp.run(transport="http")`
2. ✅ Direct HTTP API (Layer 2) - FastAPI endpoints for tool access
3. ✅ `parse_validation_md()` function - Extract queries from library_validation.md
4. ✅ Batch query runner via Direct HTTP API - HTTP requests to librarian (NOT LM Studio)
5. ✅ Response file writer - Organized output to `reports/validation_*/`
6. ✅ Comparison report generator - Summary statistics and quality metrics
7. ✅ Run script with progress output - One-command validation

**Files to create**:
- `mcp_server/http_api.py` - Direct HTTP API (FastAPI)
- `scripts/parse_validation.py` - Query parser
- `scripts/run_batch_validation.py` - Batch HTTP query runner (calls librarian API)
- `scripts/write_responses.py` - Response file writer
- `scripts/generate_report.py` - Report generator
- `scripts/run_validation.sh` - Main validation script

**Files to modify**:
- `mcp_server/librarian_mcp.py` - Add HTTP transport + HTTP API startup
- `requirements.txt` - Add FastAPI and uvicorn dependencies

**Dependencies to add**:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
```

**Estimated effort**: 1-2 weeks (7 focused deliverables)

### Phase 3B: Authentication (Security)
1. API key system
2. User model and storage
3. Authentication middleware
4. Login/logout endpoints

### Phase 3C: Multi-User Data Isolation (Safety)
1. User-prefixed collections
2. Per-user metadata stores
3. Namespace separation in queries
4. Cross-user search controls

### Phase 3D: Concurrency Control (Reliability)
1. File locking for metadata
2. Thread-safe singletons
3. Database transactions
4. Retry logic for conflicts

### Phase 3E: Production Hardening (Polish)
1. HTTPS/TLS
2. Rate limiting
3. Audit logging
4. Monitoring and metrics

### Phase 3F: Document-Type Chunking (Advanced)
1. File type detection and routing
2. Specialized chunkers per document type
3. PDF table extraction and chunking
4. Code syntax-aware chunking

### Phase 3G: Multi-Library Support (Organization)
1. Library isolation and management
2. Directed queries to specific libraries
3. Cross-library search capabilities
4. Library permissions and access control

### Phase 3H: Automated Validation Pipeline (Quality Assurance)
1. Shell script driver for validation suite
2. HTTP-based fresh context per query
3. Automated report generation
4. MCP tool integration for on-demand validation
5. Cron-friendly scheduled validation

---

## Technical Decisions

### ChromaDB Multi-Tenancy

**Decision**: Separate collections per user/library

**Rationale**:
- Better performance (smaller collections)
- True data isolation
- Easier management
- Natural fit with ChromaDB architecture

### Metadata Storage Migration

**Current**: JSON files (not thread-safe)
**Phase 3**: SQLite (ACID compliant)

**Migration Path**:
```python
# Migration script
def migrate_metadata_json_to_sqlite():
    # Read all JSON files
    # Create SQLite schema
    # Import data
    # Verify integrity
    # Backup old files
```

### Authentication Storage

**SQLite for user accounts**:
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT,
    created_at TIMESTAMP,
    last_login TIMESTAMP
);
```

**API keys in environment or config file**:
```bash
# Environment variable
LIBRARIAN_API_KEYS="admin:key1,user:key2"

# Config file
api_keys:
  admin: "secret-admin-key"
  users:
    - username: "user1"
      key: "user-key-123"
```

---

## Deployment Architecture

```
[User 1] --|
[User 2] --> HTTP Server --> FastMCP --> Librarian Server --> ChromaDB
[User 3] --|                (Transport Layer)      |
                                                    Metadata Store (SQLite)
                                                    User Store (SQLite)
```

**Components**:
- **HTTP Server**: FastMCP with uvicorn
- **Transport Layer**: HTTP/WebSocket/SSE
- **Librarian Server**: Business logic
- **ChromaDB**: Vector storage (per-user collections)
- **Metadata Store**: SQLite (document tracking)
- **User Store**: SQLite (authentication)

---

## Success Criteria

### Phase 3 Complete

- [ ] HTTP transport working
- [ ] Multi-user authentication implemented
- [ ] Concurrent write safety ensured
- [ ] Document-type specific chunking operational
- [ ] Multi-library support functional
- [ ] Automated validation pipeline operational
- [ ] Security audit passed
- [ ] Production-ready for small teams

### Testing Requirements

- [ ] Load testing (10+ concurrent users)
- [ ] Security testing (authentication, authorization)
- [ ] Performance testing (search latency, indexing speed)
- [ ] Compatibility testing (various MCP clients)
- [ ] Document type testing (PDF, DOCX, code, etc.)
- [ ] Automated validation suite (all 16 queries passing)
- [ ] Regression testing (documentation accuracy over time)

---

## Known Issues & Bugs to Fix

### Bug #1: File Move Detection (NON-CRITICAL)

**Status**: Documented, not affecting functionality
**Impact**: Sync reporting accuracy only
**Priority**: Low
**Location**: `mcp_server/core/document_manager.py` → `sync_directory()`

#### Problem Description

When a file is moved (renamed to different path) with unchanged content, the sync operation incorrectly reports it as "added" instead of "updated."

#### Expected Behavior

```python
# Move: /documents/reco.md → /reco.md
# Expected sync results:
Updated: 1    # Path change detected and updated
Added: 0
Unchanged: 39
Removed: 0
```

#### Actual Behavior

```python
# Move: /documents/reco.md → /reco.md
# Actual sync results:
Updated: 0    # ❌ Should be 1
Added: 1      # ❌ Should be 0
Unchanged: 39
Removed: 0
```

#### Root Cause Analysis

**Current Logic Flow**:
1. Scan filesystem and discover files
2. Calculate SHA-256 checksum for each file
3. Check if checksum exists in metadata
4. If exists → "unchanged"
5. If not exists → "added"

**The Bug**: The logic doesn't detect when a file with the **same checksum** exists at a **different path**.

**What Should Happen**:
```python
for file_path in discovered_files:
    checksum = calculate_sha256(file_path)

    # Check if this checksum already exists
    existing_doc = metadata_store.get_by_checksum(checksum)

    if existing_doc:
        if existing_doc.path != file_path:
            # FILE MOVED! Update path in metadata
            existing_doc.path = file_path
            metadata_store.update(existing_doc)
            stats['updated'] += 1
        else:
            # File unchanged
            stats['unchanged'] += 1
    else:
        # New file
        add_document(file_path)
        stats['added'] += 1
```

#### Why This Matters

**Functionality**: ❌ Not affected - data is correct
- Same document ID preserved ✅
- Path updated correctly in metadata ✅
- Search works properly ✅

**Reporting**: ⚠️ Misleading - sync summary is wrong
- Users see "Added: 1" when nothing was added
- File moves are invisible in sync reports
- Accurate change tracking lost

#### Impact Assessment

**Low Priority** - Non-critical bug:
- ✅ No data corruption
- ✅ No functional issues
- ✅ Search works correctly
- ✅ Document IDs preserved
- ❌ Sync reporting inaccurate
- ❌ Change tracking broken

#### Fix Required

**File**: `mcp_server/core/document_manager.py`

**Method**: `sync_directory()`

**Changes needed**:
1. Add `get_by_checksum()` method to `MetadataStore`
2. Detect file moves by checksum matching
3. Update path when file moved
4. Count as "updated" not "added"

**Estimated effort**: 1-2 hours

---

### Bug #2: Rebuild Not Respecting .librarianignore ✅ FIXED

**Status**: Fixed in commit `[ADD COMMIT HASH]`
**Impact**: Critical - blocked proper rebuild functionality
**Priority**: High

#### Problem Description

The `rebuild_library.py` script was not actually rebuilding - it only ran a sync operation, which preserved all existing documents including those that should be ignored.

#### Root Cause

Missing `clear()` methods:
- `ChromaBackend` had no `clear()` method
- `MetadataStore` had no `clear()` method
- `rebuild_library.py` didn't clear existing data

#### Fix Applied

**Added methods**:
```python
# ChromaBackend.clear()
def clear(self) -> bool:
    """Clear all documents from the collection"""
    all_data = collection.get()
    all_ids = all_data.get('ids', [])
    collection.delete(ids=all_ids)

# MetadataStore.clear()
def clear(self) -> bool:
    """Clear all metadata, with backup"""
    # Backs up existing index
    # Clears in-memory index
    # Saves empty index
```

**Updated rebuild_library.py**:
```python
# NEW: Clear existing data first
backend.clear()
metadata.store.clear()

# THEN: Fresh sync
doc_manager.sync_directory(...)
```

#### Result

✅ `.obsidian` files now properly ignored
✅ True rebuild with fresh ignore patterns
✅ Metadata backup created before clearing
✅ Proper reindexing from scratch

---

## Open Questions

1. **Cross-library search priority**: How important is searching all libraries at once vs. directed queries?

2. **Library permissions**: Should libraries have different access levels (read-only, read-write, admin)?

3. **Document-type chunking**: Should users be able to configure chunking strategies per document type?

4. **Migration path**: Should we provide automated migration from single-library to multi-library setup?

5. **Performance targets**: What are acceptable latency targets for search, indexing, and concurrent users?

---

**Status**: Planning Phase - Ready for Implementation
**Priority**: High
**Estimated Effort**: 4-6 weeks for full Phase 3 implementation
