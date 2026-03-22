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
Chonkie-based document backend.
Uses Chonkie Pipeline for intelligent file-type-aware chunking, ChromaDB for storage.
"""
from typing import List, Dict, Optional
from pathlib import Path
from chonkie import Pipeline, SemanticChunker
from .chroma_backend import ChromaBackend


class ChonkieBackend(ChromaBackend):
    """Backend using Chonkie Pipeline for intelligent semantic chunking."""

    def __init__(self, collection_name: str = None, db_path: str = None,
                 chunk_size: int = 512, embedding_model: str = "minishlab/potion-base-32M"):
        """
        Initialize Chonkie backend.

        Args:
            collection_name: ChromaDB collection name
            db_path: ChromaDB database path
            chunk_size: Target chunk size in tokens
            embedding_model: Embedding model for semantic chunking
        """
        super().__init__(collection_name, db_path)

        self.chunk_size = chunk_size
        self.embedding_model = embedding_model

    def chunk_documents(self, documents: List[str],
                       document_ids: Optional[List[str]] = None,
                       source: str = "upload") -> List[Dict]:
        """
        Process documents using Chonkie semantic chunking (legacy interface).

        DEPRECATED: Use chunk_files() instead for file-type-aware processing.
        This method processes pre-extracted text and applies semantic chunking.

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
            # Use SemanticChunker directly for pre-extracted text
            chunker = SemanticChunker(
                chunk_size=self.chunk_size,
                embedding_model=self.embedding_model
            )

            chunks = chunker(doc_text)

            for chunk_idx, chunk in enumerate(chunks):
                if not chunk.text.strip():
                    continue

                chunk_id = f"{doc_id}-chunk-{chunk_idx}"
                metadata = {
                    "chunk_index": chunk_idx,
                    "document_id": doc_id,
                    "document_name": source,
                    "token_count": chunk.token_count,
                    "char_count": len(chunk.text),
                    "chunking_method": "chonkie_semantic"
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

    def chunk_files(self, file_paths: List[str], source: str = "upload") -> List[Dict]:
        """
        Process files using Chonkie with file-type-aware processing.

        This is the RECOMMENDED method for indexing files. It uses Chonkie's
        SemanticChunker for intelligent semantic chunking:
        - PDFs: Extract using docling, then semantic chunking
        - Markdown: Process as markdown, then semantic chunking
        - Code (.py, .js, etc.): Process as code, then semantic chunking
        - Other text: Process as plain text, then semantic chunking

        Args:
            file_paths: List of file paths to process
            source: Source identifier (e.g., library path)

        Returns:
            List of created chunks with metadata
        """
        import uuid
        from chonkie import SemanticChunker

        # Get collection
        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        processed_chunks = []
        chunker = SemanticChunker(
            chunk_size=self.chunk_size,
            embedding_model=self.embedding_model
        )

        for file_path in file_paths:
            path_obj = Path(file_path)
            if not path_obj.exists():
                print(f"Warning: File not found: {file_path}")
                continue

            # Extract text based on file type
            ext = path_obj.suffix.lower()
            try:
                if ext == '.pdf':
                    # Try multiple PDF extraction methods
                    text = None

                    # Method 1: Try pypdf (simple text extraction)
                    try:
                        import pypdf
                        with open(file_path, 'rb') as f:
                            pdf_reader = pypdf.PdfReader(f)
                            text = ''
                            for page in pdf_reader.pages:
                                text += page.extract_text() + '\n'
                        if text.strip():
                            print(f"Extracted text using pypdf: {len(text)} characters")
                    except Exception as e:
                        print(f"pypdf failed: {e}")

                    # Method 2: Fall back to docling if pypdf fails
                    if not text or not text.strip():
                        try:
                            from docling.document_converter import DocumentConverter
                            converter = DocumentConverter()
                            result = converter.convert(file_path)
                            text = result.document.export_to_markdown()
                            if text.strip():
                                print(f"Extracted text using docling: {len(text)} characters")
                        except Exception as e:
                            print(f"docling failed: {e}")

                    if not text or not text.strip():
                        raise Exception("All PDF extraction methods failed")
                elif ext == '.docx':
                    # Use python-docx for DOCX
                    from docx import Document as DocxDocument
                    doc = DocxDocument(file_path)
                    text = '\n'.join([para.text for para in doc.paragraphs])
                else:
                    # For text-based files, read directly
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        text = f.read()

                if not text.strip():
                    print(f"Warning: No text extracted from {file_path}")
                    continue

                # Chunk the text using SemanticChunker
                doc_id = str(uuid.uuid4())
                chunks = chunker(text)

                for chunk_idx, chunk in enumerate(chunks):
                    if not chunk.text.strip():
                        continue

                    chunk_id = f"{doc_id}-chunk-{chunk_idx}"
                    metadata = {
                        "chunk_index": chunk_idx,
                        "document_id": doc_id,
                        "document_name": path_obj.name,
                        "source_file": str(path_obj),
                        "token_count": chunk.token_count,
                        "char_count": len(chunk.text),
                        "chunking_method": "chonkie_semantic",
                        "file_type": ext
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

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

        return processed_chunks

    def get_backend_info(self) -> Dict:
        """Get information about the backend configuration."""
        return {
            "backend_type": "chonkie",
            "chunking_method": "semantic_pipeline",
            "chunk_size": self.chunk_size,
            "embedding_model": self.embedding_model,
            "collection_name": self.collection_name,
            "db_path": self.db_path,
            "file_type_aware": True,
            "supported_extensions": [
                ".pdf", ".docx", ".md", ".txt",
                ".py", ".js", ".ts", ".json",
                ".yaml", ".yml", ".toml", ".rst", ".html"
            ]
        }
