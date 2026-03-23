"""
CLI tools for the Librarian MCP Server.
Adapted from CLI-MCP-Duplicate with security features preserved.
"""
import os
import subprocess
from pathlib import Path

# Configuration will be set during registration
SAFE_WORKING_DIR = None
LIBRARIAN_WRITE_DIR = ".librarian"  # Subdirectory for write operations (matches data directory)
MAX_OUTPUT_CHARS = 8000
DEFAULT_TIMEOUT_SECONDS = 15
MAX_WRITE_FILE_SIZE = 100000  # 100KB max for write operations

ALLOWED_BINARY_NAMES = {
    "ls", "cd", "pwd", "whoami", "echo", "cat", "find", "grep", "head", "tail",
    "sort", "uniq", "cut", "awk", "date", "hostname", "test", "mkdir",
    "wc", "diff", "stat", "file", "tree"
}

BANNED_FLAG_COMBOS = {
    ("find", "-delete"),
    ("find", "-exec"),
    ("find", "-execdir"),
    ("awk", "system"),
    ("awk", "systime"),
}

DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".md", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".rst", ".html"}


def is_safe_command(cmd: str, args: list) -> tuple[bool, str]:
    """Validate command against whitelist and banned flag combinations."""
    cmd_name = os.path.basename(cmd)

    DANGEROUS_COMMANDS = {
        "rm", "rmdir", "chmod", "chown", "dd", "mkfs", "fdisk",
        "wget", "curl", "nc", "netcat", "ssh", "scp", "rsync",
        "tar", "zip", "unzip", "mount", "umount", "python",
        "python3", "perl", "bash", "sh", "zsh"
    }

    if cmd_name in DANGEROUS_COMMANDS:
        return False, f"Command '{cmd_name}' is explicitly blocked."

    if cmd.startswith('/'):
        binary_name = os.path.basename(cmd)
        if binary_name in DANGEROUS_COMMANDS:
            return False, f"Binary '{binary_name}' is explicitly blocked."
    else:
        if cmd_name not in ALLOWED_BINARY_NAMES:
            return False, f"Command '{cmd_name}' is not in the allowed list."

    args_str = ' '.join(args)
    for banned_cmd, banned_flag in BANNED_FLAG_COMBOS:
        if cmd_name == banned_cmd and banned_flag in args_str:
            return False, f"Flag '{banned_flag}' is not permitted with '{banned_cmd}'."

    return True, "OK"


def is_safe_path(path: str, safe_dir: str) -> tuple[bool, str]:
    """Ensure path stays within safe directory."""
    try:
        base = os.path.realpath(os.path.expanduser(safe_dir))
        if os.path.isabs(path):
            resolved = os.path.realpath(path)
        else:
            resolved = os.path.realpath(os.path.join(base, path))
        if not resolved.startswith(base):
            return False, f"Path traversal detected: '{path}' escapes safe directory."
        return True, resolved
    except Exception as e:
        return False, f"Invalid path: {e}"


def truncate_output(text: str, limit: int = None) -> str:
    """Truncate output to protect LLM context window."""
    max_chars = limit if limit is not None else MAX_OUTPUT_CHARS
    if len(text) > max_chars:
        return text[:max_chars] + f"\n[output truncated — exceeded {max_chars} chars]"
    return text


def register_cli_tools(mcp, safe_dir: str):
    """
    Register all CLI tools with the MCP server.

    Args:
        mcp: FastMCP instance
        safe_dir: Safe working directory for file operations
    """
    global SAFE_WORKING_DIR
    SAFE_WORKING_DIR = safe_dir

    @mcp.tool()
    def execute_command(command: str, args: list[str] = [], cwd: str = None) -> str:
        """
        Execute a whitelisted command safely inside the allowed directory.

        Args:
            command: The binary to execute (e.g. 'ls', 'cat', 'grep')
            args: List of arguments to pass to the command
            cwd: Optional subdirectory to run in (must be inside allowed directory)

        Returns:
            stdout, stderr, return code
        """
        safe, reason = is_safe_command(command, args)
        if not safe:
            return f"[security error]\n{reason}"

        final_cwd = cwd if cwd else SAFE_WORKING_DIR
        real_final_cwd = os.path.realpath(final_cwd)
        safe_base_real = os.path.realpath(SAFE_WORKING_DIR)

        if not real_final_cwd.startswith(safe_base_real):
            return f"[security error]\nWorking directory must be inside {SAFE_WORKING_DIR}"

        full_cmd = [command] + args

        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                cwd=final_cwd,
                timeout=DEFAULT_TIMEOUT_SECONDS,
                shell=False
            )

            output_text = ""
            if result.stdout:
                output_text += f"[stdout]\n{result.stdout}\n"
            if result.stderr:
                output_text += f"[stderr]\n{result.stderr}\n"
            output_text += f"[return code]\n{result.returncode}\n"

            return truncate_output(output_text) if output_text.strip() else "[no output]"

        except subprocess.TimeoutExpired:
            return f"[timeout]\nCommand timed out after {DEFAULT_TIMEOUT_SECONDS} seconds."
        except FileNotFoundError:
            return f"[error]\nCommand not found: {command}"
        except PermissionError:
            return f"[error]\nPermission denied for command: {command}"
        except Exception as e:
            return f"[error]\nExecution failed: {str(e)}"

    @mcp.tool()
    def read_document(path: str, start_line: int = None, end_line: int = None,
                     head: int = None, tail: int = None, max_chars: int = None) -> str:
        """
        Read contents of a document inside the allowed directory.

        Supports reading entire file or specific portions:
        - Line ranges: start_line=1, end_line=10
        - First N lines: head=20
        - Last N lines: tail=20
        - Custom max size: max_chars=20000

        Args:
            path: Absolute or relative path to the document
            start_line: Starting line number (1-based, inclusive)
            end_line: Ending line number (1-based, inclusive)
            head: Read first N lines (overrides start_line/end_line)
            tail: Read last N lines (overrides start_line/end_line)
            max_chars: Maximum characters to return (default: 8000)

        Returns:
            Document contents or error message

        Examples:
            read_document("/path/to/file.txt")           # Entire file (up to 8000 chars)
            read_document("/path/to/file.txt", head=50)   # First 50 lines
            read_document("/path/to/file.txt", tail=50)   # Last 50 lines
            read_document("/path/to/file.txt", start_line=100, end_line=150)  # Lines 100-150
            read_document("/path/to/file.txt", max_chars=20000)  # Up to 20000 chars
        """
        safe, resolved = is_safe_path(path, SAFE_WORKING_DIR)
        if not safe:
            return f"[security error]\n{resolved}"

        if not os.path.isfile(resolved):
            return f"[error]\nFile not found: {resolved}"

        ext = Path(resolved).suffix.lower()
        if ext not in DOCUMENT_EXTENSIONS:
            return f"[error]\nUnsupported file type: {ext}. Allowed: {', '.join(sorted(DOCUMENT_EXTENSIONS))}"

        try:
            with open(resolved, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            # Determine which lines to read
            if head is not None:
                # Read first N lines
                selected_lines = lines[:head]
                range_info = f"(first {head} lines)"
            elif tail is not None:
                # Read last N lines
                selected_lines = lines[-tail:] if tail > 0 else []
                range_info = f"(last {tail} lines)"
            elif start_line is not None or end_line is not None:
                # Read line range
                start = start_line if start_line is not None else 1
                end = end_line if end_line is not None else len(lines)
                # Convert to 0-based indexing
                selected_lines = lines[start-1:end]
                range_info = f"(lines {start}-{end})"
            else:
                # Read entire file
                selected_lines = lines
                range_info = f"(all {len(lines)} lines)"

            # Join lines
            contents = ''.join(selected_lines)

            # Apply max_chars limit if specified (higher limit for partial reads)
            limit = max_chars if max_chars is not None else MAX_OUTPUT_CHARS
            if len(contents) > limit:
                contents = contents[:limit] + f"\n[output truncated — exceeded {limit} chars]"

            return f"[file: {resolved} {range_info}]\n\n{contents}"

        except Exception as e:
            return f"[error]\nCould not read file: {e}"

    @mcp.tool()
    def list_documents(path: str = None, extension: str = None, recursive: bool = True) -> str:
        """
        List documents in the allowed directory.

        Args:
            path: Subdirectory to list (default: root of allowed directory)
            extension: Filter by extension e.g. '.md', '.py' (default: all supported)
            recursive: Whether to recurse into subdirectories (default: True)

        Returns:
            List of document paths with sizes
        """
        base = path if path else SAFE_WORKING_DIR
        safe, resolved = is_safe_path(base, SAFE_WORKING_DIR)
        if not safe:
            return f"[security error]\n{resolved}"

        if not os.path.isdir(resolved):
            return f"[error]\nDirectory not found: {resolved}"

        extensions = {extension.lower()} if extension else DOCUMENT_EXTENSIONS

        try:
            results = []

            if recursive:
                for root, dirs, files in os.walk(resolved):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    for fname in sorted(files):
                        if Path(fname).suffix.lower() in extensions:
                            full_path = os.path.join(root, fname)
                            size = os.path.getsize(full_path)
                            results.append(f"{full_path} ({size} bytes)")
            else:
                for fname in sorted(os.listdir(resolved)):
                    full_path = os.path.join(resolved, fname)
                    if os.path.isfile(full_path) and Path(fname).suffix.lower() in extensions:
                        size = os.path.getsize(full_path)
                        results.append(f"{full_path} ({size} bytes)")

            if not results:
                return f"[no documents found in {resolved}]"

            output = f"[documents in {resolved}]\n" + "\n".join(results)
            output += f"\n\n[total: {len(results)} documents]"
            return truncate_output(output)

        except Exception as e:
            return f"[error]\nCould not list directory: {e}"

    @mcp.tool()
    def search_documents(query: str, path: str = None, extension: str = None, case_sensitive: bool = False) -> str:
        """
        Search for a text string across documents in the allowed directory.
        Returns matching file paths and lines containing the match with line numbers.

        Args:
            query: Text string to search for
            path: Subdirectory to search (default: root of allowed directory)
            extension: Limit search to file type e.g. '.md' (default: all supported)
            case_sensitive: Whether search is case sensitive (default: False)

        Returns:
            Matching files and lines with line numbers
        """
        base = path if path else SAFE_WORKING_DIR
        safe, resolved = is_safe_path(base, SAFE_WORKING_DIR)
        if not safe:
            return f"[security error]\n{resolved}"

        if not os.path.isdir(resolved):
            return f"[error]\nDirectory not found: {resolved}"

        extensions = {extension.lower()} if extension else DOCUMENT_EXTENSIONS
        results = []
        files_searched = 0
        files_matched = 0

        try:
            for root, dirs, files in os.walk(resolved):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for fname in sorted(files):
                    if Path(fname).suffix.lower() not in extensions:
                        continue
                    full_path = os.path.join(root, fname)
                    files_searched += 1
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                            lines = f.readlines()
                        matches = []
                        for i, line in enumerate(lines, 1):
                            haystack = line if case_sensitive else line.lower()
                            needle = query if case_sensitive else query.lower()
                            if needle in haystack:
                                matches.append(f"  line {i}: {line.rstrip()}")
                        if matches:
                            files_matched += 1
                            results.append(f"\n{full_path}:")
                            results.extend(matches[:10])
                            if len(matches) > 10:
                                results.append(f"  ... and {len(matches) - 10} more matches")
                    except Exception:
                        continue

            if not results:
                return f"[no matches found for '{query}' in {files_searched} files]"

            output = f"[search results for '{query}']\n" + "\n".join(results)
            output += f"\n\n[searched {files_searched} files, found matches in {files_matched} files]"
            return truncate_output(output)

        except Exception as e:
            return f"[error]\nSearch failed: {e}"

    @mcp.tool()
    def document_summary(path: str) -> str:
        """
        Get a structural summary of a document without reading full contents.
        Markdown: shows heading hierarchy.
        Python/JS/TS: shows functions and classes defined.
        Text/other: shows line/word count and first few lines.

        Args:
            path: Path to the document

        Returns:
            Structural summary with line numbers
        """
        safe, resolved = is_safe_path(path, SAFE_WORKING_DIR)
        if not safe:
            return f"[security error]\n{resolved}"

        if not os.path.isfile(resolved):
            return f"[error]\nFile not found: {resolved}"

        ext = Path(resolved).suffix.lower()

        try:
            with open(resolved, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            size = os.path.getsize(resolved)
            word_count = sum(len(line.split()) for line in lines)
            output = f"[summary: {resolved}]\n"
            output += f"Size: {size} bytes | Lines: {len(lines)} | Words: {word_count}\n\n"

            if ext == '.md':
                headings = [(i+1, line.rstrip()) for i, line in enumerate(lines)
                           if line.startswith('#')]
                if headings:
                    output += "[headings]\n"
                    for lineno, heading in headings[:50]:
                        output += f"  line {lineno}: {heading}\n"
                else:
                    output += "[no headings found]\n"

            elif ext in {'.py', '.js', '.ts'}:
                definitions = [(i+1, line.rstrip()) for i, line in enumerate(lines)
                              if line.strip().startswith(('def ', 'class ', 'function ', 'const ', 'async def '))]
                if definitions:
                    output += "[definitions]\n"
                    for lineno, defn in definitions[:50]:
                        output += f"  line {lineno}: {defn.strip()}\n"
                else:
                    output += "[no definitions found]\n"

            else:
                output += "[first 10 lines]\n"
                for i, line in enumerate(lines[:10], 1):
                    output += f"  {i}: {line.rstrip()}\n"

            return output

        except Exception as e:
            return f"[error]\nCould not summarize file: {e}"

    @mcp.tool()
    def write_document(path: str, content: str, create_dirs: bool = True) -> str:
        """
        Write content to a file in the librarian workspace.

        This tool creates a two-way communication channel where the librarian
        can write files (analysis results, code changes, documentation updates)
        that you can review and apply.

        ⚡ QUICK PATH REFERENCE ⚡
            Just use the filename or subdirectory path:
            - 'report.md' → writes to librarian workspace
            - 'reports/analysis.md' → creates reports/ subdirectory automatically
            - 'sandbox/findings.md' → creates sandbox/ subdirectory automatically

            ❌ DON'T use: '/.librarian/sandbox/file.md' (wrong!)
            ✅ INSTEAD use: 'sandbox/file.md' or 'file.md' (correct!)

        Args:
            path: File path relative to the librarian workspace (simple format only)
                   - Good: 'report.md', 'analysis/contradictions.md', 'reports/fix.py'
                   - Bad: '/.librarian/sandbox/report.md', '../escape.txt', '/absolute/path.md'
            content: File content to write
            create_dirs: Create parent directories if they don't exist (default: True)

        Returns:
            Success confirmation with file path and size

        Examples:
            write_document('report.md', '# Analysis\\n\\nFindings...')
            write_document('analysis/contradictions.md', 'Detailed analysis...')
            write_document('reports/fix.py', 'def fix():\\n    pass')

        Note: All files are written to the librarian workspace automatically.
              Use simple relative paths - no leading slashes or dot prefixes needed.
        """
        # Validate path BEFORE any processing to give clear error early
        if not path:
            return "[error] Path cannot be empty. Please provide a filename like 'report.md' or 'reports/analysis.md'"

        # SECURITY: Early validation to prevent wasting time on invalid paths
        # Reject paths that look like they're trying to escape or use absolute paths
        if path.startswith('/') or path.startswith('\\'):
            return f"[error] Invalid path format. Use relative paths like 'report.md' or 'reports/analysis.md', not '{path}'"

        if '..' in path:
            return f"[error] Path cannot contain '..' (parent directory reference). Use simple paths like 'report.md', not '{path}'"

        # SECURITY: Strip leading/trailing slashes and whitespace
        clean_path = path.strip().strip('/').strip('\\')

        # SECURITY: Reject paths starting with dot (except for hidden files like .gitignore)
        # This prevents the /.librarian escape vulnerability
        if clean_path.startswith('.'):
            return f"[error] Path cannot start with '.'. Use simple filenames like 'report.md', not '{path}'"

        # SECURITY: Reject paths trying to reference project directory
        if 'librarian-mcp' in clean_path.lower():
            return f"[error] Path contains invalid references. Use simple paths like 'report.md', not '{path}'"

        # SECURITY: Reject complex paths with multiple leading slashes or dots
        if '//' in path or '/./' in path:
            return f"[error] Path contains invalid sequences. Use simple paths like 'reports/analysis.md', not '{path}'"

        # SECURITY: Reject paths that look like absolute paths after stripping
        # Common system directories that shouldn't appear in relative paths
        system_dirs = ['home', 'usr', 'bin', 'etc', 'var', 'tmp', 'root', 'opt']
        first_component = clean_path.split('/')[0] if '/' in clean_path else clean_path
        if first_component.lower() in system_dirs:
            return f"[error] Path looks like absolute path. Use simple paths like 'report.md' or 'sandbox/file.md', not '{path}'"

        # SECURITY: Limit directory depth to prevent complex path structures
        depth = clean_path.count('/')
        if depth > 3:
            return f"[error] Path too deep (max 3 levels). Use simple paths like 'reports/analysis.md', not '{path}'"

        # Always force into librarian/ subdirectory
        normalized_path = f"{LIBRARIAN_WRITE_DIR}/{clean_path}"

        # Validate the combined path is safe
        safe, resolved = is_safe_path(normalized_path, SAFE_WORKING_DIR)
        if not safe:
            return f"[error] Path validation failed. Use simple paths like 'report.md' or 'reports/analysis.md'"

        # Additional check: ensure we're in the librarian subdirectory
        resolved_real = os.path.realpath(resolved)
        safe_dir_real = os.path.realpath(SAFE_WORKING_DIR)
        librarian_dir = os.path.join(safe_dir_real, LIBRARIAN_WRITE_DIR)

        if not resolved_real.startswith(librarian_dir):
            return f"[error] Write would escape allowed directory. Use simple paths like 'report.md', not '{path}'"

        # Check file size limit
        if len(content) > MAX_WRITE_FILE_SIZE:
            return f"[error]\nContent too large: {len(content)} bytes (max: {MAX_WRITE_FILE_SIZE} bytes)"

        # Create parent directories if requested
        file_dir = os.path.dirname(resolved_real)
        if create_dirs and file_dir and not os.path.exists(file_dir):
            try:
                os.makedirs(file_dir, exist_ok=True)
            except Exception as e:
                return f"[error]\nCould not create directory {file_dir}: {e}"

        # Prevent overwriting critical system files (defense in depth)
        critical_patterns = ['password', 'secret', 'key', 'credential', '.env', 'config']
        path_lower = resolved_real.lower()
        for pattern in critical_patterns:
            if pattern in path_lower:
                return f"[security error]\nCannot write to files containing '{pattern}' in path"

        try:
            # Write the file
            with open(resolved_real, 'w', encoding='utf-8') as f:
                f.write(content)

            # Log the write operation for audit trail
            log_entry = f"[write] {resolved_real} ({len(content)} bytes)"
            print(f"[librarian-mcp] {log_entry}")

            return f"[success]\nWrote {len(content)} bytes to {resolved_real}\n"

        except Exception as e:
            return f"[error]\nCould not write file: {e}"

    @mcp.tool()
    def server_info() -> str:
        """
        Returns server configuration, allowed commands, and supported document types.
        """
        librarian_path = os.path.join(SAFE_WORKING_DIR, LIBRARIAN_WRITE_DIR)
        return (
            f"[librarian-mcp server info]\n"
            f"Allowed directory: {SAFE_WORKING_DIR}\n"
            f"Write directory: {librarian_path}\n"
            f"Allowed commands: {', '.join(sorted(ALLOWED_BINARY_NAMES))}\n"
            f"Document extensions: {', '.join(sorted(DOCUMENT_EXTENSIONS))}\n"
            f"Timeout: {DEFAULT_TIMEOUT_SECONDS}s\n"
            f"Max output: {MAX_OUTPUT_CHARS} chars\n"
            f"Max write size: {MAX_WRITE_FILE_SIZE} bytes\n"
        )
