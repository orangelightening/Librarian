"""
Abstract backend interface for document storage and retrieval.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class DocumentBackend(ABC):
    """Abstract base class for document backends."""

    @abstractmethod
    def chunk_documents(self, documents: List[str], document_ids: Optional[List[str]] = None, source: str = "upload") -> List[Dict]:
        """
        Process documents into chunks with embeddings.

        Args:
            documents: List of document text strings
            document_ids: Optional IDs for tracking
            source: Source identifier

        Returns:
            List of created chunks with metadata
        """
        pass

    @abstractmethod
    def query(self, query_text: str, limit: int = 5) -> List[Dict]:
        """
        Perform semantic search.

        Args:
            query_text: Search query
            limit: Maximum results

        Returns:
            List of relevant chunks with scores
        """
        pass

    @abstractmethod
    def delete_documents(self, document_id: str):
        """Remove all chunks for a document."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict:
        """Get backend statistics."""
        pass
