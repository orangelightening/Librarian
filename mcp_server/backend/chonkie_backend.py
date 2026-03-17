"""
Chonkie-based document backend.
Uses Chonkie for intelligent chunking, ChromaDB for storage.
"""
from typing import List, Dict, Optional
from chonkie import RecursiveChunker
from .chroma_backend import ChromaBackend


class ChonkieBackend(ChromaBackend):
    """Backend using Chonkie for intelligent chunking."""

    def __init__(self, collection_name: str = None, db_path: str = None,
                 chunk_size: int = 1000, min_chunk_size: int = 50):
        """
        Initialize Chonkie backend.

        Args:
            collection_name: ChromaDB collection name
            db_path: ChromaDB database path
            chunk_size: Target chunk size in tokens
            min_chunk_size: Minimum characters per chunk
        """
        super().__init__(collection_name, db_path)

        self.chunk_size = chunk_size
        self.min_chunk_size = min_chunk_size

        # Initialize Chonkie chunker
        self.chunker = RecursiveChunker(
            chunk_size=chunk_size,
            min_characters_per_chunk=min_chunk_size
        )

    def chunk_documents(self, documents: List[str],
                       document_ids: Optional[List[str]] = None,
                       source: str = "upload") -> List[Dict]:
        """
        Process documents using Chonkie chunking.

        This replaces the custom chunking in ChromaBackend with
        Chonkie's intelligent semantic-aware chunking.

        Args:
            documents: List of document text strings
            document_ids: Optional IDs for tracking
            source: Source identifier

        Returns:
            List of created chunks with metadata
        """
        if not document_ids:
            import uuid
            document_ids = [str(uuid.uuid4()) for _ in documents]

        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        processed_chunks = []

        for doc_id, doc_text in zip(document_ids, documents):
            # Use Chonkie for intelligent chunking
            chonkie_chunks = self.chunker(doc_text)

            for chunk_idx, chunk in enumerate(chonkie_chunks):
                if not chunk.text.strip():
                    continue

                chunk_id = f"{doc_id}-chunk-{chunk_idx}"
                metadata = {
                    "chunk_index": chunk_idx,
                    "document_id": doc_id,
                    "document_name": source,
                    "token_count": chunk.token_count,
                    "char_count": len(chunk.text),
                    "chunking_method": "chonkie_recursive"
                }

                try:
                    collection.add(
                        documents=[chunk.text],
                        ids=[chunk_id],
                        metadatas=[metadata]
                    )

                    processed_chunks.append({
                        "id": chunk_id,
                        "text": chunk.text,
                        "metadata": metadata
                    })
                except Exception as e:
                    print(f"Error adding chunk {chunk_id}: {e}")
                    continue

        return processed_chunks

    def get_backend_info(self) -> Dict:
        """Get information about the backend configuration."""
        return {
            "backend_type": "chonkie",
            "chunking_method": "recursive",
            "chunk_size": self.chunk_size,
            "min_chunk_size": self.min_chunk_size,
            "collection_name": self.collection_name,
            "db_path": self.db_path
        }
