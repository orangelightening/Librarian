"""
Metadata Store - Tracks processed documents.
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class MetadataStore:
    """Stores document metadata for change tracking."""

    def __init__(self, metadata_path: str = None):
        """
        Initialize metadata store.

        Args:
            metadata_path: Path to metadata directory
        """
        from ..config.settings import settings

        self.metadata_path = Path(metadata_path or settings.METADATA_PATH)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.metadata_path / "index.json"
        self._index = self._load_index()

    def _load_index(self) -> Dict:
        """Load index from disk."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading metadata index: {e}")
                return {}
        return {}

    def _save_index(self):
        """Save index to disk."""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self._index, f, indent=2)
        except Exception as e:
            print(f"Error saving metadata index: {e}")

    def add(self, metadata: Dict):
        """
        Add document metadata.

        Args:
            metadata: Document metadata dictionary
        """
        if 'document_id' not in metadata:
            raise ValueError("Metadata must contain 'document_id'")

        self._index[metadata['document_id']] = metadata
        self._save_index()

    def get(self, document_id: str) -> Optional[Dict]:
        """
        Get metadata by document ID.

        Args:
            document_id: Document ID

        Returns:
            Metadata dictionary or None
        """
        return self._index.get(document_id)

    def get_by_path(self, path: str) -> Optional[Dict]:
        """
        Get metadata by file path.

        Args:
            path: File path

        Returns:
            Metadata dictionary or None
        """
        normalized_path = str(Path(path).resolve())
        for doc in self._index.values():
            if Path(doc.get('path', '')).resolve() == Path(normalized_path).resolve():
                return doc
        return None

    def delete(self, document_id: str):
        """
        Remove document metadata.

        Args:
            document_id: Document ID
        """
        if document_id in self._index:
            del self._index[document_id]
            self._save_index()

    def get_all(self) -> List[Dict]:
        """
        Get all indexed documents.

        Returns:
            List of all metadata dictionaries
        """
        return list(self._index.values())

    def update(self, document_id: str, metadata: Dict):
        """
        Update document metadata.

        Args:
            document_id: Document ID
            metadata: Updated metadata fields
        """
        if document_id in self._index:
            self._index[document_id].update(metadata)
            self._save_index()

    def count(self) -> int:
        """
        Get total number of indexed documents.

        Returns:
            Number of documents
        """
        return len(self._index)
