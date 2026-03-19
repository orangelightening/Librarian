#!/usr/bin/env python3
"""
Generate comprehensive validation report from results JSON.
"""
import json
import sys
from pathlib import Path
from datetime import datetime
import re


def extract_citations(text: str) -> list:
    """Extract citation markers from text."""
    pattern = r'\[Source:\s*([^\]]+)\]'
    matches = re.findall(pattern, text)
    return matches


def analyze_result(result: dict) -> dict:
    """Analyze a single validation result."""
    content = result.get('content', '')
    citations = extract_citations(content)

    return {
        'query_num': result['query_num'],
        'status': result['status'],
        'tokens_used': result.get('tokens_used', 0),
        'citation_count': len(citations),
        'citations': citations,
        'content_length': len(content),
        'has_tool_calls': len(result.get('tool_calls', [])) > 0
    }


def generate_report(results_file: str, output_dir: str):
    """Generate comprehensive validation report."""

    # Load results
    with open(results_file, 'r') as f:
        data = json.load(f)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Analyze all results
    analyses = [analyze_result(r) for r in data['results']]

    # Calculate statistics
    total_queries = len(analyses)
    successful_queries = sum(1 for a in analyses if a['status'] == 'success')
    total_tokens = sum(a['tokens_used'] for a in analyses)
    avg_tokens = total_tokens / total_queries if total_queries > 0 else 0

    total_citations = sum(a['citation_count'] for a in analyses)
    responses_with_citations = sum(1 for a in analyses if a['citation_count'] > 0)
    avg_citations = total_citations / total_queries if total_queries > 0 else 0

    responses_with_tool_calls = sum(1 for a in analyses if a['has_tool_calls'])

    # Generate summary report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""# Librarian Validation Report
**Generated**: {timestamp}

---

## Executive Summary

- **Total Queries**: {total_queries}
- **Success Rate**: {successful_queries}/{total_queries} ({100*successful_queries/total_queries:.0f}%)
- **Total Tokens**: {total_tokens:,}
- **Average Tokens/Query**: {avg_tokens:.0f}
- **Responses with Citations**: {responses_with_citations}/{total_queries}
- **Total Citations**: {total_citations}
- **Average Citations/Response**: {avg_citations:.1f}
- **Responses with Tool Calls**: {responses_with_tool_calls}/{total_queries}

---

## Quality Assessment

"""

    if responses_with_citations == total_queries:
        report += "✅ **All responses include proper citations**\n\n"
    elif responses_with_citations >= total_queries * 0.8:
        report += f"⚠️  **{total_queries - responses_with_citations} responses missing citations**\n\n"
    else:
        report += f"❌ **{total_queries - responses_with_citations} responses missing citations**\n\n"

    report += f"**Citation Coverage**: {100*responses_with_citations/total_queries:.0f}%\n"

    # Detailed analysis
    report += "\n---\n\n## Detailed Analysis\n\n"

    for i, (query, analysis) in enumerate(zip(data['queries'], analyses), 1):
        status_icon = "✓" if analysis['status'] == 'success' else "✗"
        report += f"### {status_icon} Query {i}: {query['description']}\n\n"
        report += f"- **Citations**: {analysis['citation_count']}\n"
        report += f"- **Tokens**: {analysis['tokens_used']}\n"
        report += f"- **Content Length**: {analysis['content_length']:,} characters\n"
        report += f"- **Has Citations**: {'Yes' if analysis['citation_count'] > 0 else 'No'}\n"
        report += f"- **Tool Calls**: {'Yes' if analysis['has_tool_calls'] else 'No'}\n"

        if analysis['citations']:
            report += f"- **Sources**: {', '.join(analysis['citations'][:5])}"
            if len(analysis['citations']) > 5:
                report += f" (+{len(analysis['citations']) - 5} more)"
            report += "\n"

        report += "\n"

    # Save summary report
    summary_file = output_path / "summary_report.md"
    with open(summary_file, 'w') as f:
        f.write(report)

    print(f"✓ Report generated: {summary_file}")

    # Save individual response files
    responses_dir = output_path / "responses"
    responses_dir.mkdir(exist_ok=True)

    for query, result in zip(data['queries'], data['results']):
        filename = f"response_{query['number']:03d}.md"
        response_file = responses_dir / filename

        content = f"""# Query {query['number']}: {query['description']}

**Status**: {result['status']}
**Tokens Used**: {result.get('tokens_used', 0)}
**Timestamp**: {datetime.now().isoformat()}
**Tool Calls**: {len(result.get('tool_calls', []))}

---

{result.get('content', 'No content')}
"""
        with open(response_file, 'w') as f:
            f.write(content)

    print(f"✓ Responses written to {responses_dir}")
    print(f"  Total files: {len(data['queries'])}")

    print()
    print("=" * 50)
    print("VALIDATION COMPLETE")
    print("=" * 50)
    print(f"Output Directory: {output_dir}")
    print(f"Summary Report: {summary_file}")
    print(f"Response Files: {len(data['queries'])} files")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_validation_report.py <results.json> [output_dir]")
        sys.exit(1)

    results_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "librarian/reports/validation_final"

    generate_report(results_file, output_dir)
