#!/usr/bin/env python3
"""
Parse library_validation.md and extract validation queries.

Extracts query metadata including number, description, and the actual query text.
"""
import re
from pathlib import Path
from typing import List, Dict


def parse_validation_md(filepath: str = "library_validation.md") -> List[Dict]:
    """
    Parse library_validation.md and extract query metadata.

    Args:
        filepath: Path to library_validation.md

    Returns:
        List of dicts with keys: number, description, query
    """
    queries = []
    current_query = None
    in_code_block = False
    query_lines = []

    with open(filepath, 'r') as f:
        for line in f:
            # Match "## Query N: Description"
            if line.startswith("## Query "):
                if current_query:
                    current_query['query'] = ''.join(query_lines).strip()
                    queries.append(current_query)
                    query_lines = []

                match = re.match(r'## Query (\d+): (.+)', line)
                if match:
                    query_num, description = match.groups()
                    current_query = {
                        'number': int(query_num),
                        'description': description.strip(),
                        'query': ''
                    }
                in_code_block = False

            # Look for code block start after **Query**:
            elif current_query and line.strip() == '**Query**:':
                continue

            elif line.strip().startswith('```') and current_query:
                if not in_code_block:
                    in_code_block = True
                else:
                    in_code_block = False

            elif in_code_block and current_query:
                # Capture the query text inside code block
                query_lines.append(line)

    # Don't forget the last query
    if current_query:
        current_query['query'] = ''.join(query_lines).strip()
        queries.append(current_query)

    return queries


if __name__ == "__main__":
    import sys

    filepath = sys.argv[1] if len(sys.argv) > 1 else "library_validation.md"

    try:
        queries = parse_validation_md(filepath)
        print(f"✓ Found {len(queries)} validation queries in {filepath}")
        print()

        for q in queries:
            print(f"Query {q['number']}: {q['description']}")
            if q['query']:
                preview = q['query'][:80] + "..." if len(q['query']) > 80 else q['query']
                print(f"  {preview}")
            print()

    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error parsing file: {e}")
        sys.exit(1)
