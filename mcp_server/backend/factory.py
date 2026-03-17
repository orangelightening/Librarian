"""
Backend factory for creating configured backend instances.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import DocumentBackend

def get_backend(backend_type: str = "chroma", **kwargs) -> 'DocumentBackend':
    """
    Get configured backend instance.

    Args:
        backend_type: Type of backend ("chroma" or "chonkie")
        **kwargs: Additional arguments to pass to backend constructor

    Returns:
        Configured backend instance

    Raises:
        ValueError: If backend_type is not supported
    """
    if backend_type == "chonkie":
        from .chonkie_backend import ChonkieBackend
        return ChonkieBackend(**kwargs)
    elif backend_type == "chroma":
        from .chroma_backend import ChromaBackend
        return ChromaBackend(**kwargs)
    else:
        raise ValueError(
            f"Unsupported backend type: {backend_type}. "
            f"Supported types: 'chroma', 'chonkie'"
        )
