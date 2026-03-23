"""
Ignore pattern matcher for librarian.
Uses gitignore-style patterns to filter files.
"""
import os
from pathlib import Path
from typing import List, Set
import fnmatch


class IgnorePatterns:
    """Manages and applies ignore patterns (gitignore-style)."""

    def __init__(self, root_path: str = None, ignore_file: str = ".librarianignore"):
        """
        Initialize ignore patterns.

        Args:
            root_path: Root directory for pattern matching
            ignore_file: Name of the ignore file
        """
        from ..config.settings import settings

        self.root_path = Path(root_path or settings.PROJECT_ROOT).resolve()
        self.ignore_file_path = self.root_path / ignore_file
        self.patterns: List[str] = []
        self.negation_patterns: List[str] = []

        self._load_patterns()

    def _load_patterns(self):
        """Load patterns from the ignore file."""
        if not self.ignore_file_path.exists():
            # No ignore file, use default patterns
            self.patterns = [
                "venv/", ".venv/", "virtualenv/",
                "__pycache__/", "*.pyc", "*.pyo",
                "__init__.py",  # Skip empty package markers
                "node_modules/", ".git/",
                "*.egg-info/", ".eggs/", "dist/", "build/",
                ".env", "*.env", "credentials.*", "*.key", "*.pem",
                "chroma_db/", "metadata/",
                "*.log", "*.tmp", "logs/", "tmp/",
                ".DS_Store", "Thumbs.db",
                "*.sqlite", "*.db", "*.sqlite3"
            ]
            return

        try:
            with open(self.ignore_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    # Handle negation patterns (patterns starting with !)
                    if line.startswith('!'):
                        self.negation_patterns.append(line[1:])
                    else:
                        self.patterns.append(line)

        except Exception as e:
            print(f"Warning: Could not load ignore file: {e}")
            # Fall back to defaults
            self.patterns = [
                "venv/", ".venv/", "node_modules/", ".git/",
                "__init__.py",  # Skip empty package markers
                "*.key", "*.pem", ".env", "credentials.*"
            ]

    def is_ignored(self, file_path: Path) -> bool:
        """
        Check if a file path matches any ignore pattern.

        Args:
            file_path: Path to check

        Returns:
            True if file should be ignored
        """
        file_path = file_path.resolve()
        rel_path = str(file_path.relative_to(self.root_path))

        # Check negation patterns first (exceptions to ignore rules)
        for pattern in self.negation_patterns:
            if self._matches_pattern(rel_path, pattern):
                return False  # Explicitly NOT ignored

        # Check ignore patterns
        for pattern in self.patterns:
            if self._matches_pattern(rel_path, pattern):
                return True  # Ignored

        return False  # Not ignored

    def _matches_pattern(self, rel_path: str, pattern: str) -> bool:
        """
        Check if a relative path matches a pattern.

        Args:
            rel_path: Relative path from root
            pattern: Gitignore-style pattern

        Returns:
            True if path matches pattern
        """
        # Normalize path separators to forward slashes
        normalized_path = rel_path.replace(os.sep, '/')

        # Directory pattern (ends with /)
        if pattern.endswith('/'):
            # Remove trailing slash for matching
            pattern = pattern[:-1]
            # Check if any path component matches the pattern
            path_parts = normalized_path.split('/')
            return pattern in path_parts

        # Wildcard pattern
        if '*' in pattern or '?' in pattern or '[' in pattern:
            # Match against filename and full path
            filename = normalized_path.split('/')[-1]
            if fnmatch.fnmatch(filename, pattern):
                return True
            if fnmatch.fnmatch(normalized_path, pattern):
                return True
            # Also check if any parent directory matches
            path_parts = normalized_path.split('/')
            for i in range(len(path_parts)):
                subdir = '/'.join(path_parts[:i+1])
                if fnmatch.fnmatch(subdir, pattern):
                    return True
            return False

        # Exact directory name match (pattern is just a directory name)
        if '/' not in pattern:
            path_parts = normalized_path.split('/')
            if pattern in path_parts:
                return True

        # Exact path match with trailing slash
        if normalized_path.startswith(pattern + '/'):
            return True

        # Exact filename match
        if '/' + normalized_path == '/' + pattern or normalized_path == pattern:
            return True

        return False

    def filter_paths(self, paths: List[Path]) -> List[Path]:
        """
        Filter a list of paths, removing ignored ones.

        Args:
            paths: List of paths to filter

        Returns:
            Filtered list (non-ignored paths only)
        """
        return [p for p in paths if not self.is_ignored(p)]

    def get_ignored_count(self, paths: List[Path]) -> int:
        """
        Count how many paths would be ignored.

        Args:
            paths: List of paths to check

        Returns:
            Number of ignored paths
        """
        return sum(1 for p in paths if self.is_ignored(p))


def get_ignore_patterns(root_path: str = None) -> IgnorePatterns:
    """
    Get or create ignore patterns instance.

    Args:
        root_path: Root directory for patterns

    Returns:
        IgnorePatterns instance
    """
    return IgnorePatterns(root_path)
