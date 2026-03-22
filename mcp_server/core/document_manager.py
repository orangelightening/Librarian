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
Document Manager - Handles complete document lifecycle.
"""
from pathlib import Path
from typing import List, Dict, Optional, Set
import hashlib
import uuid
from datetime import datetime

from .metadata_store import MetadataStore
from .ignore_patterns import IgnorePatterns


class DocumentManager:
    """Manages document lifecycle: discovery, ingestion, updates, removal."""

    def __init__(self, backend, metadata_store: MetadataStore = None, ignore_patterns: IgnorePatterns = None):
        """
        Initialize document manager.

        Args:
            backend: DocumentBackend instance
            metadata_store: MetadataStore instance (creates new if None)
            ignore_patterns: IgnorePatterns instance (creates new if None)
        """
        self.backend = backend
        self.metadata = metadata_store or MetadataStore()
        self.ignore_patterns = ignore_patterns or IgnorePatterns()

    def discover_documents(
        self,
        path: str,
        extensions: Set[str] = None,
        recursive: bool = True
    ) -> List[Path]:
        """
        Discover all documents in a directory.

        Args:
            path: Root directory to scan
            extensions: File extensions to include (e.g., {'.md', '.txt', '.py'})
            recursive: Whether to scan subdirectories

        Returns:
            List of document Path objects
        """
        from ..config.settings import settings

        extensions = extensions or settings.DEFAULT_EXTENSIONS
        path_obj = Path(path).resolve()

        if not path_obj.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        if not path_obj.is_dir():
            # Single file, return it if extension matches
            if path_obj.suffix.lower() in extensions:
                return [path_obj]
            return []

        documents = []

        if recursive:
            for ext in extensions:
                # Use rglob for recursive search
                documents.extend(path_obj.rglob(f"*{ext}"))
        else:
            for ext in extensions:
                # Use glob for non-recursive search
                documents.extend(path_obj.glob(f"*{ext}"))

        # Filter out ignored files
        if self.ignore_patterns:
            documents = self.ignore_patterns.filter_paths(documents)

        return documents

    def calculate_checksum(self, file_path: Path) -> str:
        """
        Calculate SHA-256 checksum of a file.

        Args:
            file_path: Path to file

        Returns:
            Hexadecimal checksum string
        """
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
        except Exception as e:
            print(f"Error calculating checksum for {file_path}: {e}")
            return ""

        return sha256_hash.hexdigest()

    def get_file_metadata(self, file_path: Path) -> Dict:
        """
        Get metadata about a file.

        Args:
            file_path: Path to file

        Returns:
            Dictionary with file metadata
        """
        try:
            stat = file_path.stat()
            return {
                "path": str(file_path.resolve()),
                "name": file_path.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "checksum": self.calculate_checksum(file_path)
            }
        except Exception as e:
            print(f"Error getting file metadata for {file_path}: {e}")
            return {}

    def add_document(self, file_path: Path, source: str = None) -> Dict:
        """
        Add a single document to the library.

        Args:
            file_path: Path to the document
            source: Optional source identifier

        Returns:
            Processing result with chunk count and document ID
        """
        from ..config.settings import settings

        file_path = Path(file_path).resolve()

        if not file_path.exists():
            return {
                "status": "error",
                "error": f"Document not found: {file_path}"
            }

        # Check file size
        try:
            if file_path.stat().st_size > settings.MAX_DOCUMENT_SIZE:
                return {
                    "status": "error",
                    "error": f"Document exceeds maximum size of {settings.MAX_DOCUMENT_SIZE} bytes"
                }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Cannot access file: {e}"
            }

        # Read document
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            return {
                "status": "error",
                "error": f"Cannot read file: {e}"
            }

        if not content.strip():
            return {
                "status": "error",
                "error": "File is empty"
            }

        # Get metadata
        file_meta = self.get_file_metadata(file_path)

        if not file_meta or not file_meta.get('checksum'):
            return {
                "status": "error",
                "error": "Could not calculate file checksum"
            }

        # Check if already exists
        existing = self.metadata.get_by_path(str(file_path))
        if existing:
            if existing['checksum'] == file_meta['checksum']:
                return {
                    "status": "unchanged",
                    "document_id": existing['document_id'],
                    "name": existing['name'],
                    "chunk_count": existing.get('chunk_count', 0)
                }
            else:
                # Document changed, remove old version
                self.remove_document(existing['document_id'])

        # Add to backend
        doc_id = file_meta['checksum'][:16]  # Use first 16 chars of checksum as ID
        source_name = source or str(file_path)

        try:
            chunks = self.backend.chunk_documents(
                documents=[content],
                document_ids=[doc_id],
                source=source_name
            )
        except Exception as e:
            return {
                "status": "error",
                "error": f"Backend error: {e}"
            }

        # Store metadata
        self.metadata.add({
            "document_id": doc_id,
            "path": str(file_path),
            "name": file_meta['name'],
            "checksum": file_meta['checksum'],
            "size": file_meta['size'],
            "modified": file_meta['modified'],
            "chunk_count": len(chunks),
            "indexed_at": datetime.now().isoformat(),
            "source": source or str(file_path.parent)  # Track source directory for safe sync
        })

        return {
            "status": "added",
            "document_id": doc_id,
            "chunk_count": len(chunks),
            "name": file_meta['name']
        }

    def add_document_pipeline(self, file_path: Path, source: str = None) -> Dict:
        """
        Add a document using Chonkie Pipeline (file-type-aware processing).

        This is the RECOMMENDED method for adding documents. It uses Chonkie's
        Pipeline API to automatically detect file types and apply appropriate
        processing for PDFs, DOCX, Markdown, code, etc.

        Args:
            file_path: Path to document
            source: Source identifier

        Returns:
            Status dictionary with document_id, chunk_count, etc.
        """
        from ..config.settings import settings

        file_path = Path(file_path).resolve()

        if not file_path.exists():
            return {
                "status": "error",
                "error": f"Document not found: {file_path}"
            }

        # Check file size
        try:
            if file_path.stat().st_size > settings.MAX_DOCUMENT_SIZE:
                return {
                    "status": "error",
                    "error": f"Document exceeds maximum size of {settings.MAX_DOCUMENT_SIZE} bytes"
                }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Cannot access file: {e}"
            }

        # Check file extension is supported
        ext = file_path.suffix.lower()
        if ext not in settings.DEFAULT_EXTENSIONS:
            return {
                "status": "error",
                "error": f"Unsupported file type: {ext}. Supported: {', '.join(sorted(settings.DEFAULT_EXTENSIONS))}"
            }

        # Get metadata
        file_meta = self.get_file_metadata(file_path)

        if not file_meta or not file_meta.get('checksum'):
            return {
                "status": "error",
                "error": "Could not calculate file checksum"
            }

        # Check if already exists
        existing = self.metadata.get_by_path(str(file_path))
        if existing:
            if existing['checksum'] == file_meta['checksum']:
                return {
                    "status": "unchanged",
                    "document_id": existing['document_id'],
                    "name": existing['name'],
                    "chunk_count": existing.get('chunk_count', 0)
                }
            else:
                # Document changed, remove old version
                self.remove_document(existing['document_id'])

        # Use Chonkie Pipeline to process the file
        source_name = source or str(file_path)

        try:
            chunks = self.backend.chunk_files(
                file_paths=[str(file_path)],
                source=source_name
            )
        except Exception as e:
            return {
                "status": "error",
                "error": f"Backend error: {e}"
            }

        if not chunks:
            return {
                "status": "error",
                "error": "No chunks generated from document"
            }

        # Use first chunk's document_id (generated by backend)
        doc_id = chunks[0]['metadata']['document_id'] if chunks else str(uuid.uuid4())

        # Store metadata
        self.metadata.add({
            "document_id": doc_id,
            "path": str(file_path),
            "name": file_meta['name'],
            "checksum": file_meta['checksum'],
            "size": file_meta['size'],
            "modified": file_meta['modified'],
            "chunk_count": len(chunks),
            "indexed_at": datetime.now().isoformat(),
            "source": source or str(file_path.parent),
            "chunking_method": "chonkie_semantic_pipeline"
        })

        return {
            "status": "added",
            "document_id": doc_id,
            "chunk_count": len(chunks),
            "name": file_meta['name']
        }

    def remove_document(self, document_id: str) -> bool:
        """
        Remove a document and all its chunks.

        Args:
            document_id: Document ID

        Returns:
            True if successful
        """
        try:
            # Remove from backend
            self.backend.delete_documents(document_id)

            # Remove metadata
            self.metadata.delete(document_id)

            return True
        except Exception as e:
            print(f"Error removing document {document_id}: {e}")
            return False

    def sync_directory(
        self,
        path: str,
        extensions: Set[str] = None,
        recursive: bool = True
    ) -> Dict:
        """
        Sync a directory: add new, update changed, remove deleted.

        Args:
            path: Directory to sync
            extensions: File extensions to include
            recursive: Whether to scan subdirectories

        Returns:
            Summary of sync operation
        """
        # Discover all documents
        try:
            from pathlib import Path

            # First, get all potential files (before filtering)
            # We need to count ignored files
            from ..config.settings import settings
            ext_list = extensions or settings.DEFAULT_EXTENSIONS
            path_obj = Path(path).resolve()

            all_candidates = []
            if recursive:
                for ext in ext_list:
                    all_candidates.extend(path_obj.rglob(f"*{ext}"))
            else:
                for ext in ext_list:
                    all_candidates.extend(path_obj.glob(f"*{ext}"))

            # Now apply ignore filters
            if self.ignore_patterns:
                ignored_count = self.ignore_patterns.get_ignored_count(all_candidates)
                documents = self.ignore_patterns.filter_paths(all_candidates)
            else:
                ignored_count = 0
                documents = all_candidates

        except Exception as e:
            return {
                "added": 0,
                "updated": 0,
                "unchanged": 0,
                "removed": 0,
                "ignored": 0,
                "errors": [f"Discovery error: {e}"]
            }

        # Get current metadata
        indexed = self.metadata.get_all()
        indexed_paths = {str(Path(doc['path']).resolve()): doc for doc in indexed}

        # Resolve sync path for source tracking
        sync_path_resolved = str(path_obj.resolve())

        results = {
            "added": 0,
            "updated": 0,
            "unchanged": 0,
            "removed": 0,
            "ignored": ignored_count,
            "errors": []
        }

        current_paths = set()  # Track paths found in current scan

        # Process each document
        for doc_path in documents:
            current_paths.add(str(doc_path.resolve()))

            try:
                # Use Pipeline-based document processing
                result = self.add_document_pipeline(doc_path, source=str(path_obj))

                if result['status'] == 'added':
                    results['added'] += 1
                elif result['status'] == 'unchanged':
                    results['unchanged'] += 1
                elif result['status'] == 'error':
                    results['errors'].append(f"{doc_path}: {result.get('error', 'Unknown error')}")
            except Exception as e:
                results['errors'].append(f"{doc_path}: {str(e)}")

        # Remove documents that no longer exist
        # IMPORTANT: Only remove documents that were indexed from THIS directory (source tracking)
        for path, doc in indexed_paths.items():
            if path not in current_paths:
                # Check if this document was indexed from the same source directory
                doc_source = doc.get('source', '')

                # Skip documents without source tracking (legacy data)
                if not doc_source or doc_source == 'NO_SOURCE':
                    continue

                # Resolve doc_source to absolute path for comparison
                try:
                    doc_source_resolved = str(Path(doc_source).resolve())
                except:
                    continue

                # Only remove if this document was indexed from the sync directory
                if doc_source_resolved == sync_path_resolved:
                    if self.remove_document(doc['document_id']):
                        results['removed'] += 1
                    else:
                        results['errors'].append(f"{path}: Failed to remove")

        return results

    def get_document_status(self, path: str) -> Dict:
        """
        Check if a document is indexed and up-to-date.

        Args:
            path: Path to the document

        Returns:
            Status information
        """
        file_path = Path(path).resolve()

        if not file_path.exists():
            return {"status": "not_found"}

        indexed = self.metadata.get_by_path(str(file_path))

        if not indexed:
            return {"status": "not_indexed"}

        current_checksum = self.calculate_checksum(file_path)

        if indexed['checksum'] == current_checksum:
            return {
                "status": "current",
                "document_id": indexed['document_id'],
                "chunk_count": indexed.get('chunk_count', 0),
                "indexed_at": indexed.get('indexed_at', ''),
                "name": indexed.get('name', '')
            }
        else:
            return {
                "status": "outdated",
                "document_id": indexed['document_id'],
                "reason": "File has been modified",
                "name": indexed.get('name', '')
            }

    def list_indexed(self) -> List[Dict]:
        """
        List all indexed documents.

        Returns:
            List of document metadata
        """
        return self.metadata.get_all()

    def get_stats(self) -> Dict:
        """
        Get document manager statistics.

        Returns:
            Statistics dictionary
        """
        indexed = self.metadata.get_all()

        total_size = sum(doc.get('size', 0) for doc in indexed)
        total_chunks = sum(doc.get('chunk_count', 0) for doc in indexed)

        return {
            "total_documents": len(indexed),
            "total_chunks": total_chunks,
            "total_size": total_size,
            "backend_stats": self.backend.get_stats()
        }
