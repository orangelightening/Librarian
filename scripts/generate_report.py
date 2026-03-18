#!/usr/bin/env python3
"""
Generate comparison and summary reports for validation results.

Analyzes responses for quality metrics and generates comprehensive reports.
"""
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

        Args:
            filepath: Path to response file

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

        if 'error' in summary:
            return f"# Validation Report\n\nError: {summary['error']}"

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
            report.append(f"- **Citations**: {analysis['citation_count']}\n")
            report.append(f"- **Lines**: {analysis['line_count']}\n")
            report.append(f"- **Characters**: {analysis['char_count']}\n")
            report.append(f"- **Has Citations**: {'Yes' if analysis['has_citations'] else 'No'}\n")
            report.append(f"- **Has Errors**: {'Yes' if analysis['has_errors'] else 'No'}\n\n")

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


if __name__ == "__main__":
    import sys

    output_dir = sys.argv[1] if len(sys.argv) > 1 else "reports/validation_latest"

    try:
        generator = ReportGenerator(output_dir)
        report_path = generator.write_report()
        print(f"✓ Report generated: {report_path}")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
        sys.exit(1)
