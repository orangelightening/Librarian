#!/usr/bin/env python3
"""
Automated validation with tool execution.

Bypasses Jan's MCP-over-API limitations by:
1. Sending queries to GLM-4.7 via API
2. Parsing tool calls from model response
3. Executing actual librarian-mcp tools via Python
4. Sending tool results back to model
5. Collecting final answers

Compatible with existing generate_validation_report.py
"""
import requests
import json
import os
import sys
import re
import ast
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import librarian-mcp components directly
from mcp_server.core.document_manager import DocumentManager
from mcp_server.core.metadata_store import MetadataStore
from mcp_server.core.ignore_patterns import IgnorePatterns
from mcp_server.backend.factory import get_backend
from mcp_server.config.settings import Settings

# Jan API configuration
JAN_API_URL = "http://127.0.0.1:1337/v1/chat/completions"
JAN_API_KEY = os.getenv("JAN_API_KEY", "no-key")
MODEL = "glm-4.7"


class ToolExecutor:
    """Execute librarian-mcp tools directly via Python."""

    def __init__(self):
        """Initialize librarian components."""
        print("Initializing librarian-mcp components...")

        self.backend = get_backend(
            backend_type=Settings.BACKEND,
            collection_name=Settings.CHROMA_COLLECTION,
            db_path=Settings.CHROMA_PATH
        )

        self.metadata = MetadataStore()
        self.ignore_patterns = IgnorePatterns(str(Settings.PROJECT_ROOT))
        self.doc_manager = DocumentManager(self.backend, self.metadata, self.ignore_patterns)

        print(f"✓ Backend: {Settings.BACKEND}")
        print(f"✓ Documents: {Settings.DOCUMENTS_DIR}")
        print()

    def execute_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """
        Execute a librarian tool and return the result.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments as dict

        Returns:
            Dict with success status and result/error message
        """
        try:
            if tool_name == "search_library":
                query = arguments.get("query", "")
                limit = arguments.get("limit", 5)
                results = self.doc_manager.backend.query(query, limit=limit)

                # Format results
                formatted = [
                    f"- {r['text'][:100]}... (score: {r['similarity_score']:.2f})"
                    for r in results
                ]
                return {"success": True, "result": "\n".join(formatted)}

            elif tool_name == "list_indexed_documents":
                docs = self.doc_manager.list_indexed()
                formatted = [
                    f"- {doc['name']}: {doc['document_id']}"
                    for doc in docs
                ]
                return {"success": True, "result": "\n".join(formatted)}

            elif tool_name == "get_library_stats":
                stats = self.doc_manager.backend.get_stats()
                return {"success": True, "result": json.dumps(stats, indent=2)}

            elif tool_name == "server_info":
                info = {
                    "backend": Settings.BACKEND,
                    "documents_dir": str(Settings.DOCUMENTS_DIR),
                    "chroma_path": str(Settings.CHROMA_PATH),
                    "metadata_path": str(Settings.METADATA_PATH),
                    "safe_dir": str(Settings.SAFE_DIR)
                }
                return {"success": True, "result": json.dumps(info, indent=2)}

            elif tool_name == "list_documents":
                path = arguments.get("path", str(Settings.PROJECT_ROOT))
                extension = arguments.get("extension", "")
                recursive = arguments.get("recursive", True)

                # Simple document listing
                docs_path = Path(path)
                if extension:
                    files = list(docs_path.rglob(f"*{extension}")) if recursive else list(docs_path.glob(f"*{extension}"))
                else:
                    files = list(docs_path.rglob("*.*")) if recursive else list(docs_path.glob("*.*"))

                # Filter by supported extensions
                supported = {'.html', '.js', '.json', '.md', '.py', '.rst', '.toml', '.ts', '.txt', '.yaml', '.yml'}
                files = [f for f in files if f.suffix in supported]

                formatted = [f"- {f.name} ({f.stat().st_size:,} bytes)" for f in files[:20]]
                return {"success": True, "result": "\n".join(formatted)}

            elif tool_name == "read_document":
                path = arguments.get("path", "")
                if not path:
                    return {"success": False, "error": "No path provided"}

                # Try to resolve the file path
                file_path = Path(path)

                # If not found, try in project root
                if not file_path.exists():
                    file_path = Path(Settings.PROJECT_ROOT) / path

                # If still not found, try in mcp_server directory
                if not file_path.exists():
                    file_path = Path(Settings.PROJECT_ROOT) / "mcp_server" / path

                # If still not found, try common doc names
                if not file_path.exists():
                    # Map common doc names to actual files
                    doc_map = {
                        "architecture.md": "ARCHITECTURE.md",
                        "security.md": "SECURITY.md",
                        "readme.md": "README.md",
                        "user_guide.md": "USER_GUIDE.md",
                    }
                    lower_path = path.lower()
                    if lower_path in doc_map:
                        file_path = Path(Settings.PROJECT_ROOT) / doc_map[lower_path]

                if not file_path.exists():
                    # List available files to help the model
                    try:
                        available_files = list(Path(Settings.PROJECT_ROOT).glob("*.md"))
                        file_list = ", ".join([f.name for f in available_files[:10]])
                        return {
                            "success": False,
                            "error": f"File not found: {path}. Available documentation files: {file_list}"
                        }
                    except:
                        return {"success": False, "error": f"File not found: {path}"}

                # Read file with options
                head = arguments.get("head")
                tail = arguments.get("tail")
                max_chars = arguments.get("max_chars", 2000)

                content = file_path.read_text()

                # Apply head/tail
                if head:
                    lines = content.split('\n')[:int(head)]
                    content = '\n'.join(lines)
                elif tail:
                    lines = content.split('\n')[int(-tail):]
                    content = '\n'.join(lines)

                # Apply max_chars
                if max_chars:
                    content = content[:int(max_chars)]

                return {"success": True, "result": content}

            elif tool_name == "search_documents":
                query = arguments.get("query", "")
                path = arguments.get("path", str(Settings.PROJECT_ROOT))
                extension = arguments.get("extension", "")
                case_sensitive = arguments.get("case_sensitive", False)

                # Use grep-like search through files
                import subprocess
                try:
                    cmd = ["grep", "-r", query, path]
                    if extension:
                        cmd.extend(["--include", f"*{extension}"])
                    if not case_sensitive:
                        cmd.insert(1, "-i")

                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    matches = result.stdout.split('\n')[:10]
                    matches = [m for m in matches if m and '.git' not in m]
                    return {"success": True, "result": "\n".join(matches) if matches else "No matches found"}
                except:
                    return {"success": False, "error": "Search failed"}

            elif tool_name == "document_summary":
                path = arguments.get("path", "")
                if not path:
                    return {"success": False, "error": "No path provided"}

                file_path = Path(path)
                if not file_path.exists():
                    return {"success": False, "error": f"File not found: {path}"}

                # Generate simple summary
                content = file_path.read_text()
                lines = len(content.split('\n'))
                words = len(content.split())
                chars = len(content)

                summary = f"File: {file_path.name}\n"
                summary += f"Lines: {lines:,}\n"
                summary += f"Words: {words:,}\n"
                summary += f"Characters: {chars:,}\n"
                summary += f"Extension: {file_path.suffix}"

                return {"success": True, "result": summary}

            elif tool_name == "add_document":
                path = arguments.get("path", "")
                if not path:
                    return {"success": False, "error": "No path provided"}

                file_path = Path(path)
                if not file_path.exists():
                    return {"success": False, "error": f"File not found: {path}"}

                result = self.doc_manager.add_document(str(file_path))
                return {"success": True, "result": json.dumps(result, indent=2)}

            elif tool_name == "sync_documents":
                path = arguments.get("path", str(Settings.PROJECT_ROOT))
                extensions = arguments.get("extensions", "")
                recursive = arguments.get("recursive", True)

                ext_list = extensions.split(',') if extensions else None
                result = self.doc_manager.sync_directory(str(path), ext_list, recursive)

                summary = f"Added: {result.get('added', 0)}, Updated: {result.get('updated', 0)}, Removed: {result.get('removed', 0)}, Ignored: {result.get('ignored', 0)}"
                return {"success": True, "result": summary}

        except Exception as e:
            return {"success": False, "error": str(e)}


class GLMValidator:
    """Validate librarian using GLM-4.7 with tool execution."""

    def __init__(self):
        """Initialize validator."""
        # Load validation queries
        sys.path.insert(0, str(Path(__file__).parent))
        from parse_validation import parse_validation_md

        self.queries = parse_validation_md()
        print(f"✓ Loaded {len(self.queries)} validation queries")

        # Load system prompt with tool list
        self.system_prompt = self._build_prompt_with_tools()
        print(f"✓ System prompt: {len(self.system_prompt):,} chars")

        # Initialize tool executor
        self.tool_executor = ToolExecutor()

        print()

    def _build_prompt_with_tools(self) -> str:
        """Build system prompt with tool list included."""
        # Load simple prompt
        simple_prompt = Path("simple_prompt.md").read_text()

        # Add comprehensive tool list
        tool_list = """

## YOUR AVAILABLE TOOLS (14 Tools)

When you need to use tools, format your tool calls EXACTLY like this:

**Tool Used:** `tool_name`
**Arguments:** `{"param": "value"}`

Then STOP and wait for me to execute the tool and provide the result.

### Library Management Tools (7)
1. **search_library(query, limit)** - Semantic search with AI aggregation
2. **sync_documents(path, extensions, recursive)** - Bulk directory sync
3. **add_document(path)** - Add single document
4. **remove_document(document_id)** - Remove by document ID
5. **list_indexed_documents()** - List all documents
6. **get_document_status(path)** - Check document status
7. **get_library_stats()** - Get library statistics

### File System Tools (5)
8. **read_document(path, start_line, end_line, head, tail, max_chars)** - Read files
9. **write_document(path, content, create_dirs)** - Write to /librarian/ workspace
10. **list_documents(path, extension, recursive)** - List files
11. **search_documents(query, path, extension, case_sensitive)** - Literal text search
12. **document_summary(path)** - Get file overview

### System Tools (2)
13. **execute_command(command, args, cwd)** - Execute whitelisted commands
14. **server_info()** - Get server configuration

**CRITICAL**:
- ONLY indicate the tool name and arguments
- DO NOT make up or hallucinate tool results
- DO NOT continue your response after calling a tool
- WAIT for the actual tool result before continuing

**File Locations**:
- Documentation files are in the project root: ARCHITECTURE.md, README.md, SECURITY.md, etc.
- Source code is in: mcp_server/
- DO NOT guess file paths - use full paths or search first

"""

        return simple_prompt + tool_list

    def parse_tool_call(self, content: str) -> Optional[Tuple[str, Dict]]:
        """
        Parse tool call from model response.

        Looks for patterns like:
        - **Tool Used:** `tool_name` (with markdown bold)
        - Tool Used: `tool_name` (without bold)
        - Arguments: {...}
        """
        # Try to find tool name (handle markdown bold **)
        patterns = [
            r'\*\*Tool Used:\*\*\s*`(\w+)`',  # With bold
            r'Tool Used:\s*`(\w+)`',          # Without bold
            r'\*\*Tool Used:\*\*\s*(\w+)',     # With bold, no backticks
            r'Tool Used:\s*(\w+)'             # Without bold, no backticks
        ]

        tool_name = None
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                tool_name = match.group(1)
                break

        if not tool_name:
            return None

        # Try to find arguments
        args_patterns = [
            r'\*\*Arguments:\*\*\s*`({[^}]+})`',  # With bold
            r'Arguments:\s*`({[^}]+})`',            # Without bold
            r'\*\*Arguments:\*\*\s*({[^}]+})',     # With bold, no backticks
            r'Arguments:\s*({[^}]+})'              # Without bold, no backticks
        ]

        arguments = {}
        for pattern in args_patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    arguments = json.loads(match.group(1))
                except:
                    pass
                break

        return (tool_name, arguments)

    def call_glm_api(self, messages: List[Dict]) -> Dict:
        """Call GLM-4.7 API."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {JAN_API_KEY}"
        }

        payload = {
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "temperature": 0.5
        }

        try:
            response = requests.post(
                JAN_API_URL,
                headers=headers,
                json=payload,
                timeout=120
            )

            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}: {response.text}"}

            result = response.json()

            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0]['message']
                return {
                    "content": message.get('content', ''),
                    "tokens": result.get('usage', {}).get('total_tokens', 0)
                }
            else:
                return {"error": "No response content"}

        except Exception as e:
            return {"error": str(e)}

    def run_query(self, query_obj: Dict) -> Dict:
        """
        Run a single validation query with tool execution.

        Args:
            query_obj: Query dict from parse_validation_md()

        Returns:
            Result dict compatible with generate_validation_report.py
        """
        query_num = query_obj['number']
        query_text = query_obj['query']

        print(f"[{query_num}/16] {query_obj['description']}")
        print(f"  Query: {query_text[:60]}...")

        # Build messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query_text}
        ]

        # Track conversation and tool calls
        conversation_turns = 0
        max_turns = 10  # Allow more tool calls
        tool_calls = []

        while conversation_turns < max_turns:
            conversation_turns += 1

            # Call API
            response = self.call_glm_api(messages)

            if "error" in response:
                return {
                    'query_num': query_num,
                    'status': 'error',
                    'content': f"API Error: {response['error']}",
                    'tokens_used': 0,
                    'tool_calls': tool_calls
                }

            content = response['content']
            tokens_used = response['tokens']

            # Check if model wants to call a tool
            tool_call = self.parse_tool_call(content)

            if tool_call:
                # Execute the tool
                tool_name, arguments = tool_call
                print(f"  → Tool: {tool_name}")

                tool_calls.append({
                    "name": tool_name,
                    "arguments": arguments
                })

                # Execute tool
                result = self.tool_executor.execute_tool(tool_name, arguments)

                # Add tool result to conversation
                tool_result_text = f"Tool Result: {result.get('result', result.get('error', 'Unknown error'))}"
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": tool_result_text})

                # If tool failed, break
                if not result.get('success'):
                    # Return error response
                    return {
                        'query_num': query_num,
                        'status': 'error',
                        'content': f"{content}\n\nTool Error: {result.get('error', 'Unknown error')}",
                        'tokens_used': tokens_used,
                        'tool_calls': tool_calls
                    }

            else:
                # No more tool calls, this is the final answer
                return {
                    'query_num': query_num,
                    'status': 'success',
                    'content': content,
                    'tokens_used': tokens_used,
                    'tool_calls': tool_calls
                }

        # Max turns reached
        return {
            'query_num': query_num,
            'status': 'error',
            'content': "Maximum conversation turns exceeded",
            'tokens_used': tokens_used,
            'tool_calls': tool_calls
        }

    def run_validation(self) -> Dict:
        """Run all validation queries."""
        print("=" * 70)
        print("GLM-4.7 Automated Validation with Tool Execution")
        print("=" * 70)
        print()

        results = []

        for query_obj in self.queries:
            result = self.run_query(query_obj)
            results.append(result)

            status_icon = "✓" if result['status'] == 'success' else "✗"
            print(f"  {status_icon} Complete ({result['tokens_used']} tokens, {len(result['tool_calls'])} tools)")
            print()

        return {
            'queries': self.queries,
            'results': results
        }


if __name__ == "__main__":
    import time

    start_time = time.time()
    validator = GLMValidator()

    # Run validation
    validation_data = validator.run_validation()

    # Save results
    output_file = "validation_with_tool_execution.json"
    with open(output_file, 'w') as f:
        json.dump(validation_data, f, indent=2)

    elapsed = time.time() - start_time

    # Summary
    success_count = sum(1 for r in validation_data['results'] if r['status'] == 'success')
    total_tokens = sum(r['tokens_used'] for r in validation_data['results'])

    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
    print(f"Time: {elapsed:.1f} seconds")
    print(f"Results: {success_count}/{len(validation_data['results'])} successful")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Output: {output_file}")
    print()
    print("To generate report:")
    print(f"  python scripts/generate_validation_report.py {output_file}")
    print()
