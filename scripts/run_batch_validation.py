#!/usr/bin/env python3
"""
Run validation queries via LM Studio HTTP API with MCP tool access.

Executes each validation query with librarian system prompt and MCP integrations.
"""
import requests
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from parse_validation import parse_validation_md

# Load environment variables
load_dotenv()


class BatchQueryRunner:
    """Run validation queries via LM Studio HTTP API with MCP tool access"""

    def __init__(self):
        self.api_endpoint = os.getenv("LM_STUDIO_API_ENDPOINT", "http://localhost:1234/api/v1/chat")
        self.api_token = os.getenv("LM_STUDIO_API_TOKEN")
        self.model = os.getenv("LM_STUDIO_MODEL", "unsloth/qwen3.5-9b")

        # Load librarian system prompt
        prompt_path = Path("prompt.md")
        if not prompt_path.exists():
            raise FileNotFoundError(f"System prompt file not found: {prompt_path}")

        self.system_prompt = prompt_path.read_text()

        if not self.api_token:
            raise ValueError("LM_STUDIO_API_TOKEN not found in environment")

    def run_query(self, query: str, query_num: int) -> Dict:
        """
        Run a single validation query via LM Studio HTTP API.

        Args:
            query: The validation query text
            query_num: Query number for tracking

        Returns:
            Dict with response metadata and content
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        # LM Studio API format with system prompt injection
        payload = {
            "model": self.model,
            "input": f"{self.system_prompt}\n\n{query}",  # System prompt + query
            "integrations": [
                {
                    "type": "plugin",
                    "id": "mcp/librarian"
                }
            ],
            "store": False  # Atomic operation - no context carried over
        }

        try:
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=120  # 2 minute timeout
            )
            response.raise_for_status()

            result = response.json()

            # Extract content from LM Studio API response format
            content_parts = []
            tool_calls = []

            for item in result.get('output', []):
                if item.get('type') == 'message':
                    content_parts.append(item.get('content', ''))
                elif item.get('type') == 'tool_call':
                    tool_calls.append({
                        'tool': item.get('tool'),
                        'arguments': item.get('arguments'),
                        'output': item.get('output', '')
                    })

            formatted_content = '\n'.join(content_parts)

            return {
                'query_num': query_num,
                'status': 'success',
                'content': formatted_content,
                'tool_calls': tool_calls,
                'tokens_used': result.get('stats', {}).get('total_output_tokens', 0)
            }

        except Exception as e:
            return {
                'query_num': query_num,
                'status': 'error',
                'error': str(e)
            }

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

            status = "✓" if result['status'] == 'success' else "✗"
            tokens = result.get('tokens_used', 0)
            print(f"  {status} Query {query_obj['number']} complete ({tokens} tokens)")

        return results


if __name__ == "__main__":
    try:
        queries = parse_validation_md()
        runner = BatchQueryRunner()
        results = runner.run_batch(queries)

        # Summary
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = sum(1 for r in results if r['status'] == 'error')

        print()
        print("=" * 50)
        print(f"Complete: {len(results)} queries processed")
        print(f"  Success: {success_count}")
        print(f"  Errors:  {error_count}")
        print("=" * 50)

        if error_count > 0:
            print()
            print("Errors:")
            for r in results:
                if r['status'] == 'error':
                    print(f"  Query {r['query_num']}: {r.get('error', 'Unknown error')}")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"✗ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)
