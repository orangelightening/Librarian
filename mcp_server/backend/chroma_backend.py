# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
ChromaDB backend implementation.
"""
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from .base import DocumentBackend


class ChromaBackend(DocumentBackend):
    """ChromaDB backend for document storage and retrieval."""

    def __init__(self, collection_name: str = None, db_path: str = None):
        """
        Initialize ChromaDB backend.

        Args:
            collection_name: Name of the collection (default: from settings)
            db_path: Path to ChromaDB data directory (default: from settings)
        """
        from ..config.settings import settings

        self.collection_name = collection_name or settings.CHROMA_COLLECTION
        self.db_path = db_path or settings.CHROMA_PATH

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist."""
        try:
            self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Warning: Could not ensure collection exists: {e}")

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
        if not document_ids:
            import uuid
            document_ids = [str(uuid.uuid4()) for _ in documents]

        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        processed_chunks = []

        for doc_id, doc_text in zip(document_ids, documents):
            # Simple sentence-based chunking
            chunks = self._chunk_text(doc_text)

            for chunk_idx, chunk_text in enumerate(chunks):
                if not chunk_text.strip():
                    continue

                chunk_id = f"{doc_id}-chunk-{chunk_idx}"
                metadata = {
                    "chunk_index": chunk_idx,
                    "document_id": doc_id,
                    "document_name": source
                }

                try:
                    collection.add(
                        documents=[chunk_text],
                        ids=[chunk_id],
                        metadatas=[metadata]
                    )

                    processed_chunks.append({
                        "id": chunk_id,
                        "text": chunk_text,
                        "metadata": metadata
                    })
                except Exception as e:
                    print(f"Error adding chunk {chunk_id}: {e}")
                    continue

        return processed_chunks

    def _chunk_text(self, text: str, chunk_size: int = None) -> List[str]:
        """
        Split text into chunks.

        Args:
            text: Text to chunk
            chunk_size: Target chunk size in characters

        Returns:
            List of text chunks
        """
        from ..config.settings import settings

        chunk_size = chunk_size or settings.CHUNK_SIZE

        if not text or len(text) <= chunk_size:
            return [text] if text else []

        # Simple sentence-based chunking
        chunks = []
        current_chunk = []

        # Split by sentences (rough approximation)
        sentences = text.split('. ')

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Add period back if it's not the last sentence
            if current_chunk or len(current_chunk) > 0:
                test_text = '. '.join(current_chunk + [sentence])
            else:
                test_text = sentence

            if len(test_text) > chunk_size and current_chunk:
                # Current chunk is full, save it
                chunks.append('. '.join(current_chunk))
                current_chunk = [sentence]
            else:
                current_chunk.append(sentence)

        # Don't forget the last chunk
        if current_chunk:
            chunks.append('. '.join(current_chunk))

        return chunks

    def query(self, query_text: str, limit: int = 5) -> List[Dict]:
        """
        Perform semantic search.

        Args:
            query_text: Search query
            limit: Maximum results

        Returns:
            List of relevant chunks with scores
        """
        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        try:
            results = collection.query(
                query_texts=[query_text],
                n_results=limit
            )
        except Exception as e:
            print(f"Query error: {e}")
            return []

        formatted = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metadatas = results.get("metadatas", [{}])[0]
            distances = results.get("distances", [])[0]
            ids = results.get("ids", [])[0]

            for i, doc in enumerate(docs):
                formatted.append({
                    "chunk_id": ids[i] if i < len(ids) else f"unknown-{i}",
                    "text": doc,
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                    "similarity_score": 1 / (distances[i] + 1e-8) if i < len(distances) else 0.0,
                    "rank": i + 1
                })

        return formatted

    def delete_documents(self, document_id: str):
        """
        Remove all chunks for a document.

        Args:
            document_id: Document ID to delete
        """
        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        try:
            # Get all chunks for this document
            all_chunks = collection.get()
            to_delete = [chunk_id for chunk_id in all_chunks.get('ids', [])
                         if chunk_id.startswith(f"{document_id}-chunk-")]

            if to_delete:
                collection.delete(ids=to_delete)
                print(f"Deleted {len(to_delete)} chunks for document {document_id}")
        except Exception as e:
            print(f"Error deleting document {document_id}: {e}")

    def get_stats(self) -> Dict:
        """
        Get backend statistics.

        Returns:
            Dictionary with backend statistics
        """
        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        return {
            "backend": "chromadb",
            "collection": self.collection_name,
            "total_chunks": collection.count(),
            "db_path": self.db_path
        }

    def clear(self) -> bool:
        """
        Clear all documents from the collection.

        Returns:
            True if successful, False otherwise
        """
        try:
            collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )

            # Get current count
            count = collection.count()

            if count > 0:
                # Get all document IDs
                all_data = collection.get()
                all_ids = all_data.get('ids', [])

                if all_ids:
                    # Delete all documents by ID
                    collection.delete(ids=all_ids)
                    print(f"Cleared {len(all_ids)} chunks from collection '{self.collection_name}'")
                else:
                    print(f"Collection '{self.collection_name}' is already empty")
            else:
                print(f"Collection '{self.collection_name}' is already empty")

            return True

        except Exception as e:
            print(f"Error clearing collection: {e}")
            return False
