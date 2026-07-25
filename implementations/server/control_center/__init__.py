"""Phase 1 Skill & Dispatch Control Center.

The package owns presentation-neutral read models and local, non-authoritative
draft operations.  It deliberately has no dependency on an authoritative writer.
"""

from .api import create_router
from .evidence import FixtureEvidenceProvider, UnavailableEvidenceProvider
from .local_store import LocalControlCenterStore
from .service import ControlCenterService

__all__ = [
    "ControlCenterService",
    "FixtureEvidenceProvider",
    "LocalControlCenterStore",
    "UnavailableEvidenceProvider",
    "create_router",
]
