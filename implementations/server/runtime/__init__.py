"""Descriptor-bounded ACI local runtime core.

The package is intentionally inert on import.  It neither opens a database nor
enables HTTP serving; callers must construct :class:`RuntimeService` explicitly.
"""

from .service import RuntimeService, RuntimeSettings

__all__ = ["RuntimeService", "RuntimeSettings"]
