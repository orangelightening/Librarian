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
