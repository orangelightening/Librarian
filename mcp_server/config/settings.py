"""
Configuration settings for Librarian MCP Server.
"""
import os
from pathlib import Path
from typing import Literal, Set


class Settings:
    """Configuration settings for the Librarian MCP Server."""

    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent

    # Safe directory for CLI operations (can be overridden via CLI args or env)
    SAFE_DIR = os.getenv("LIBRARIAN_SAFE_DIR", str(Path.home()))

    # Document storage
    DOCUMENTS_DIR = os.getenv("LIBRARIAN_DOCUMENTS_DIR", str(PROJECT_ROOT / "documents"))

    # ChromaDB
    CHROMA_PATH = os.getenv("LIBRARIAN_CHROMA_PATH", str(PROJECT_ROOT / "chroma_db"))
    CHROMA_COLLECTION = os.getenv("LIBRARIAN_CHROMA_COLLECTION", "documents")

    # Metadata storage
    METADATA_PATH = os.getenv("LIBRARIAN_METADATA_PATH", str(PROJECT_ROOT / "metadata"))

    # Backend selection
    BACKEND: Literal["chroma", "chonkie"] = os.getenv("LIBRARIAN_BACKEND", "chonkie")

    # Chonkie (Phase 2)
    CHONKIE_URL = os.getenv("LIBRARIAN_CHONKIE_URL", "http://localhost:8000")

    # Document processing
    MAX_DOCUMENT_SIZE = int(os.getenv("LIBRARIAN_MAX_DOCUMENT_SIZE", "10000000"))  # 10MB
    CHUNK_SIZE = int(os.getenv("LIBRARIAN_CHUNK_SIZE", "1000"))

    # Allowed document extensions
    DEFAULT_EXTENSIONS: Set[str] = {".md", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".rst", ".html"}

    # Security
    MAX_OUTPUT_CHARS = int(os.getenv("LIBRARIAN_MAX_OUTPUT_CHARS", "8000"))
    COMMAND_TIMEOUT = int(os.getenv("LIBRARIAN_COMMAND_TIMEOUT", "15"))

    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        Path(cls.DOCUMENTS_DIR).mkdir(parents=True, exist_ok=True)
        Path(cls.CHROMA_PATH).mkdir(parents=True, exist_ok=True)
        Path(cls.METADATA_PATH).mkdir(parents=True, exist_ok=True)


# Singleton instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()
