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
