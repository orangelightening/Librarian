"""
AI Layer Abstraction Interface.
Handles query formatting, result aggregation, and response synthesis.
"""
from abc import ABC, abstractmethod
from typing import List, Dict


class AILayer(ABC):
    """Abstract base class for AI-powered document processing."""

    @abstractmethod
    def format_query(self, raw_query: str, context: Dict = None) -> Dict:
        """
        Transform user query into optimized search parameters.

        Args:
            raw_query: User's original query text
            context: Optional additional context (e.g., user preferences)

        Returns:
            Formatted query object with enhanced search parameters
        """
        pass

    @abstractmethod
    def aggregate_results(self, chunks: List[Dict], query: str = None) -> Dict:
        """
        Synthesize multiple chunk results into coherent response.

        Args:
            chunks: List of retrieved document chunks
            query: Original query text

        Returns:
            Aggregated response with reasoning and citations
        """
        pass

    @abstractmethod
    def build_context(self, user_intent: str) -> Dict:
        """
        Determine optimal chunks based on inferred user intent.

        Args:
            user_intent: User's information need description

        Returns:
            Context building parameters
        """
        pass


class DefaultAILayer(AILayer):
    """Basic AI layer that synthesizes search results for AI consumption."""

    def format_query(self, raw_query: str, context: Dict = None) -> Dict:
        """
        Format query for search.

        Args:
            raw_query: User's original query text
            context: Optional additional context

        Returns:
            Formatted query object
        """
        return {
            "text": raw_query.strip(),
            "type": "semantic",
            "limit": 5,
            **(context or {})
        }

    def aggregate_results(self, chunks: List[Dict], query: str = None) -> Dict:
        """
        Aggregate search results into coherent response.

        Args:
            chunks: List of retrieved document chunks
            query: Original query text

        Returns:
            Aggregated response with citations
        """
        if not chunks:
            return {
                "response": "No relevant documents found for your query.",
                "num_chunks": 0,
                "citations": []
            }

        # Sort by rank and take top chunks
        top_chunks = sorted(chunks, key=lambda x: x.get("rank", 999))[:5]

        # Build response from chunk texts
        response_parts = []
        for i, chunk in enumerate(top_chunks):
            text = chunk.get("text", "")
            # Truncate very long chunks
            if len(text) > 500:
                text = text[:500] + "..."

            response_parts.append(f"[{i+1}] {text}")

        response = "\n\n".join(response_parts)

        # Build citations list with document names
        citations = []
        for i, chunk in enumerate(top_chunks):
            metadata = chunk.get("metadata", {})
            doc_name = metadata.get("document_name", "Unknown Document")
            score = chunk.get("similarity_score", 0)
            citations.append(f"[{i+1}] {doc_name} (Relevance: {score:.2f})")

        return {
            "response": response,
            "citations": citations,
            "num_chunks": len(chunks),
            "top_results": [chunk.get("chunk_id", "") for chunk in top_chunks]
        }

    def build_context(self, user_intent: str) -> Dict:
        """
        Build context for search.

        Args:
            user_intent: User's information need description

        Returns:
            Context parameters
        """
        return {
            "depth": 1,
            "breadth": 3
        }
