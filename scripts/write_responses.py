#!/usr/bin/env python3
"""
Write validation responses to organized directory structure.

Creates dated validation reports with response files and metadata.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class ResponseWriter:
    """Write validation responses to organized directory structure"""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
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
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Query {query_num}: {metadata.get('description', 'Unknown')}\n\n")
            f.write(f"**Status**: {metadata.get('status', 'unknown')}\n")
            f.write(f"**Tokens Used**: {metadata.get('tokens_used', 0)}\n")
            f.write(f"**Timestamp**: {datetime.now().isoformat()}\n")
            f.write(f"**Tool Calls**: {len(metadata.get('tool_calls', []))}\n\n")
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
                    'tool_calls': result.get('tool_calls', []),
                    'error': result.get('error', '')
                }
            )

            written.append(filepath)

        return written


if __name__ == "__main__":
    import sys

    # Simple test
    output_dir = sys.argv[1] if len(sys.argv) > 1 else None

    writer = ResponseWriter(output_dir)
    print(f"✓ Response writer initialized")
    print(f"  Output directory: {writer.output_dir}")
    print(f"  Responses: {writer.output_dir / 'responses'}")
    print(f"  Metadata: {writer.output_dir / 'metadata'}")
