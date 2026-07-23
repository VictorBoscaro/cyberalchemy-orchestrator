"""Exact authoritative profile import and runtime registration planning."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import canonical_bytes, digest_bytes, parse_strict_json
from .errors import IntegrityError


@dataclass(frozen=True)
class VerifiedProfile:
    profile_id: str
    profile_version: str
    authoritative_path: str
    authoritative_file_digest: str
    canonical_digest: str
    canonical_size_bytes: int
    request: dict[str, Any]


class ProfileImporter:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root).resolve()

    def load_manifest(self, manifest_path: Path) -> list[VerifiedProfile]:
        manifest_path = Path(manifest_path).resolve()
        manifest = parse_strict_json(manifest_path.read_bytes())
        if manifest.get("status") != "registered-independent-pass-cycle-5":
            raise IntegrityError("profile manifest lacks independent cycle-5 PASS")
        profiles = [self.verify_entry(entry) for entry in manifest["profiles"]]
        if len(profiles) != 4:
            raise IntegrityError("exactly four profiles are required")
        return profiles

    def verify_entry(self, entry: dict[str, Any]) -> VerifiedProfile:
        if entry.get("review_status") != "PASS":
            raise IntegrityError("profile registration review is not PASS")
        source = (self.repo_root / entry["authoritative_profile_path"]).resolve()
        if self.repo_root not in source.parents:
            raise IntegrityError("authoritative profile escapes repository root")
        raw = source.read_bytes()
        if digest_bytes(raw) != entry["authoritative_file_digest"]:
            raise IntegrityError("authoritative profile raw digest mismatch")
        request = parse_strict_json(raw)
        canonical = canonical_bytes(request)
        if (
            digest_bytes(canonical) != entry["canonical_digest"]
            or len(canonical) != entry["canonical_size_bytes"]
        ):
            raise IntegrityError("authoritative profile canonical binding mismatch")
        if (
            request.get("profile_id") != entry["profile_id"]
            or request.get("profile_version") != entry["profile_version"]
        ):
            raise IntegrityError("authoritative profile identity mismatch")
        mirror = (
            self.repo_root
            / "docs/features/agents-communication-infra"
            / entry["local_review_mirror"]["path"]
        ).resolve()
        mirror_raw = mirror.read_bytes()
        if (
            digest_bytes(mirror_raw)
            != entry["local_review_mirror"]["file_digest"]
            or canonical_bytes(parse_strict_json(mirror_raw)) != canonical
        ):
            raise IntegrityError("non-authoritative review mirror is not canonical-equal")
        return VerifiedProfile(
            profile_id=entry["profile_id"],
            profile_version=entry["profile_version"],
            authoritative_path=entry["authoritative_profile_path"],
            authoritative_file_digest=entry["authoritative_file_digest"],
            canonical_digest=entry["canonical_digest"],
            canonical_size_bytes=entry["canonical_size_bytes"],
            request=request,
        )

    @staticmethod
    def event_bindings(profiles: list[VerifiedProfile]) -> dict[str, tuple[str, str]]:
        registry = next(
            profile
            for profile in profiles
            if profile.profile_id == "aci.event-schema-canonicalizer-registry"
        )
        canonicalizer = registry.request["closed_contract"]["canonicalizer"]
        if (
            canonicalizer["profile_id"] != "aci.canonical-json"
            or canonicalizer["profile_version"] != "1"
            or canonicalizer["profile_digest"]
            != "sha256:6ed22971449c8ea911f9b885d26b01e6eb2e77f208cd8bc6419dff31d97b7ade"
        ):
            raise IntegrityError("imported canonicalizer contract mismatch")
        return {
            item["event_type"]: (item["schema_ref"], item["schema_digest"])
            for item in registry.request["closed_contract"]["registered_event_schemas"]
        }
