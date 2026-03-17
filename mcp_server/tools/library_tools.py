"""
Library tools for the Librarian MCP Server.
"""
from pathlib import Path
from typing import Set

from ..core.document_manager import DocumentManager
from ..core.metadata_store import MetadataStore
from ..backend.chroma_backend import ChromaBackend
from ..ai_layer.ai_layer_interface import DefaultAILayer

# Lazy initialization
_backend = None
_metadata = None
_doc_manager = None
_ai_layer = None


def get_backend():
    """Get or create backend instance based on settings."""
    global _backend
    if _backend is None:
        from ..config.settings import settings
        from ..backend.factory import get_backend as create_backend

        _backend = create_backend(
            backend_type=settings.BACKEND,
            collection_name=settings.CHROMA_COLLECTION,
            db_path=settings.CHROMA_PATH
        )
    return _backend


def get_metadata():
    """Get or create metadata store instance."""
    global _metadata
    if _metadata is None:
        _metadata = MetadataStore()
    return _metadata


def get_doc_manager():
    """Get or create document manager instance."""
    global _doc_manager
    if _doc_manager is None:
        _doc_manager = DocumentManager(get_backend(), get_metadata())
    return _doc_manager


def get_ai_layer():
    """Get or create AI layer instance."""
    global _ai_layer
    if _ai_layer is None:
        _ai_layer = DefaultAILayer()
    return _ai_layer


def register_library_tools(mcp):
    """
    Register all library tools with the MCP server.

    Args:
        mcp: FastMCP instance
    """

    @mcp.tool()
    def search_library(query: str, limit: int = 5) -> str:
        """
        Search the library semantically and return aggregated results.

        Args:
            query: Search query text
            limit: Maximum number of results (default: 5)

        Returns:
            Aggregated search results with citations
        """
        try:
            backend = get_backend()
            ai_layer = get_ai_layer()

            results = backend.query(query_text=query, limit=limit)
            aggregated = ai_layer.aggregate_results(results, query)

            response = f"Found {aggregated['num_chunks']} relevant chunks.\n\n"
            response += aggregated['response']

            if aggregated.get('citations'):
                response += "\n\n**Sources:**\n" + "\n".join(aggregated['citations'])

            return response

        except Exception as e:
            return f"Search failed: {str(e)}"

    @mcp.tool()
    def sync_documents(path: str, extensions: str = None, recursive: bool = True) -> str:
        """
        Sync all documents from a directory into the library.
        Adds new documents, updates changed ones, removes deleted ones.

        Args:
            path: Directory path to sync
            extensions: Comma-separated list of extensions (e.g., '.md,.txt,.py')
            recursive: Scan subdirectories (default: True)

        Returns:
            Summary of sync operation
        """
        try:
            doc_manager = get_doc_manager()

            ext_set = None
            if extensions:
                ext_set = set(e.strip() for e in extensions.split(','))

            results = doc_manager.sync_directory(path, ext_set, recursive)

            report = [
                f"Sync completed for directory: {path}",
                f"  Added: {results['added']}",
                f"  Updated: {results['updated']}",
                f"  Unchanged: {results['unchanged']}",
                f"  Removed: {results['removed']}",
            ]

            if results.get('ignored', 0) > 0:
                report.append(f"  Ignored: {results['ignored']} (excluded by .librarianignore)")

            if results['errors']:
                report.append(f"  Errors: {len(results['errors'])}")
                for error in results['errors'][:5]:
                    report.append(f"    - {error}")
                if len(results['errors']) > 5:
                    report.append(f"    ... and {len(results['errors']) - 5} more errors")

            return "\n".join(report)

        except Exception as e:
            return f"Sync failed: {str(e)}"

    @mcp.tool()
    def add_document(path: str) -> str:
        """
        Add a single document to the library.

        Args:
            path: Path to the document file

        Returns:
            Result of the add operation
        """
        try:
            doc_manager = get_doc_manager()
            result = doc_manager.add_document(Path(path))

            if result['status'] == 'added':
                return f"Added document '{result['name']}' with {result['chunk_count']} chunks. Document ID: {result['document_id']}"
            elif result['status'] == 'unchanged':
                return f"Document already exists and is unchanged. Document ID: {result['document_id']}"
            elif result['status'] == 'error':
                return f"Failed to add document: {result.get('error', 'Unknown error')}"
            else:
                return f"Unexpected result: {result}"

        except Exception as e:
            return f"Failed to add document: {str(e)}"

    @mcp.tool()
    def remove_document(document_id: str) -> str:
        """
        Remove a document and all its chunks from the library.

        Args:
            document_id: ID of the document to remove

        Returns:
            Result of the remove operation
        """
        try:
            doc_manager = get_doc_manager()

            if doc_manager.remove_document(document_id):
                return f"Removed document {document_id}"
            else:
                return f"Failed to remove document {document_id}"

        except Exception as e:
            return f"Failed to remove document: {str(e)}"

    @mcp.tool()
    def list_indexed_documents() -> str:
        """
        List all documents currently indexed in the library.

        Returns:
            List of indexed documents with metadata
        """
        try:
            doc_manager = get_doc_manager()
            documents = doc_manager.list_indexed()

            if not documents:
                return "No documents indexed in the library."

            lines = [f"Total indexed documents: {len(documents)}\n"]

            for doc in sorted(documents, key=lambda x: x.get('indexed_at', ''), reverse=True):
                lines.append(f"  • {doc.get('name', 'Unknown')}")
                lines.append(f"    ID: {doc.get('document_id', 'N/A')}")
                lines.append(f"    Path: {doc.get('path', 'N/A')}")
                lines.append(f"    Chunks: {doc.get('chunk_count', 0)}")
                lines.append(f"    Size: {doc.get('size', 0):,} bytes")
                lines.append(f"    Indexed: {doc.get('indexed_at', 'N/A')}")
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return f"Failed to list documents: {str(e)}"

    @mcp.tool()
    def get_document_status(path: str) -> str:
        """
        Check if a document is indexed and up-to-date.

        Args:
            path: Path to the document

        Returns:
            Document status information
        """
        try:
            doc_manager = get_doc_manager()
            status = doc_manager.get_document_status(path)

            if status['status'] == 'not_found':
                return f"File not found: {path}"
            elif status['status'] == 'not_indexed':
                return f"Document not indexed: {path}"
            elif status['status'] == 'current':
                return (
                    f"Document is current.\n"
                    f"  Name: {status.get('name', 'Unknown')}\n"
                    f"  ID: {status['document_id']}\n"
                    f"  Chunks: {status['chunk_count']}\n"
                    f"  Indexed: {status['indexed_at']}"
                )
            elif status['status'] == 'outdated':
                return (
                    f"Document is outdated (file modified).\n"
                    f"  Name: {status.get('name', 'Unknown')}\n"
                    f"  ID: {status['document_id']}\n"
                    f"  Reason: {status['reason']}"
                )
            else:
                return f"Unknown status: {status}"

        except Exception as e:
            return f"Failed to get document status: {str(e)}"

    @mcp.tool()
    def get_library_stats() -> str:
        """
        Get statistics about the library.

        Returns:
            Library statistics
        """
        try:
            doc_manager = get_doc_manager()
            stats = doc_manager.get_stats()

            report = [
                "Library Statistics",
                f"  Backend: {stats['backend_stats']['backend']}",
                f"  Collection: {stats['backend_stats']['collection']}",
                f"  Total Chunks: {stats['backend_stats']['total_chunks']}",
                f"  Total Documents: {stats['total_documents']}",
                f"  Total Size: {stats['total_size']:,} bytes ({stats['total_size'] / 1024 / 1024:.2f} MB)",
            ]

            return "\n".join(report)

        except Exception as e:
            return f"Failed to get library stats: {str(e)}"

    @mcp.tool()
    def list_available_tools() -> str:
        """
        List all available MCP tools and their parameters.

        Returns:
            List of tools with descriptions and parameters
        """
        try:
            # Get the MCP instance to list tools
            import inspect
            from ..tools import library_tools, cli_tools

            tools_info = []

            # Library tools
            library_tool_funcs = [
                ('search_library', library_tools.search_library),
                ('sync_documents', library_tools.sync_documents),
                ('add_document', library_tools.add_document),
                ('remove_document', library_tools.remove_document),
                ('list_indexed_documents', library_tools.list_indexed_documents),
                ('get_document_status', library_tools.get_document_status),
                ('get_library_stats', library_tools.get_library_stats),
            ]

            # CLI tools
            cli_tool_funcs = [
                ('execute_command', cli_tools.execute_command),
                ('read_document', cli_tools.read_document),
                ('list_documents', cli_tools.list_documents),
                ('search_documents', cli_tools.search_documents),
                ('document_summary', cli_tools.document_summary),
            ]

            all_tools = library_tool_funcs + cli_tool_funcs

            for tool_name, tool_func in all_tools:
                # Get function signature
                sig = inspect.signature(tool_func)

                # Get docstring
                doc = inspect.getdoc(tool_func) or "No description"

                # Parse parameters
                params = []
                for param_name, param in sig.parameters.items():
                    if param_name != 'self':
                        param_type = param.annotation if param.annotation != inspect.Parameter.empty else 'any'
                        default = param.default if param.default != inspect.Parameter.empty else 'required'
                        params.append(f"  - {param_name}: {param_type} (default: {default})")

                tools_info.append(f"\n📦 {tool_name}")
                tools_info.append(f"   {doc.split(chr(10))[0] if doc else 'No description'}")

                if params:
                    tools_info.append("   Parameters:")
                    tools_info.extend(params)
                else:
                    tools_info.append("   Parameters: (none)")

            return "Available MCP Tools:\n" + "\n".join(tools_info)

        except Exception as e:
            return f"Failed to list tools: {str(e)}"
