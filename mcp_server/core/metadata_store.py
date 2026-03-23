"""
Metadata Store - Tracks processed documents.
"""
import json
import os
import tempfile
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

        # Migration: Check for old .librarian/metadata location and warn
        self._migrate_old_metadata()

        self._index = self._load_index()

    def _migrate_old_metadata(self):
        """Check for and warn about old metadata locations."""
        from ..config.settings import settings

        # Check for old .librarian/metadata location
        project_root = settings.PROJECT_ROOT
        old_metadata_path = project_root / ".librarian" / "metadata"

        if old_metadata_path.exists() and old_metadata_path != self.metadata_path:
            import shutil
            print(f"\n⚠️  WARNING: Old metadata directory found at: {old_metadata_path}")
            print(f"   Current metadata location: {self.metadata_path}")
            print(f"   This can cause stale index issues!")
            print(f"\n   Removing old directory to prevent confusion...")

            try:
                # Back up just in case
                backup_path = project_root / ".librarian" / "metadata.backup"
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                shutil.copytree(old_metadata_path, backup_path)

                # Remove old directory
                shutil.rmtree(old_metadata_path)
                print(f"   ✅ Old metadata directory removed")
                print(f"   📁 Backup saved to: {backup_path}")
                print()
            except Exception as e:
                print(f"   ❌ Error removing old metadata: {e}")
                print()

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
        """Save index to disk using atomic write (temp file + rename)."""
        try:
            # Write to temporary file first
            dir_path = os.path.dirname(self.index_file)
            with tempfile.NamedTemporaryFile(
                mode='w',
                dir=dir_path,
                prefix='.index_',
                suffix='.tmp',
                delete=False
            ) as tmp_file:
                json.dump(self._index, tmp_file, indent=2)
                tmp_path = tmp_file.name

            # Atomic rename (overwrites target if exists)
            os.rename(tmp_path, self.index_file)

        except Exception as e:
            print(f"Error saving metadata index: {e}")
            # Clean up temp file if it exists
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except:
                    pass

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

    def clear(self) -> bool:
        """
        Clear all metadata from the store.

        Returns:
            True if successful, False otherwise
        """
        try:
            count = len(self._index)

            if count > 0:
                # Backup the existing index
                backup_path = self.index_file.with_suffix('.json.bak')
                import shutil
                shutil.copy2(self.index_file, backup_path)
                print(f"Backed up existing index to {backup_path}")

            # Clear the index
            self._index = {}
            self._save_index()

            print(f"Cleared {count} documents from metadata store")
            return True

        except Exception as e:
            print(f"Error clearing metadata store: {e}")
            return False
