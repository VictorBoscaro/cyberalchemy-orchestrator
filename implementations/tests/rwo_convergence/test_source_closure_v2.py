from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from implementations.rwo_convergence.canonical import TreeMember, tree_digest
from implementations.rwo_convergence.source_closure_v2 import (
    GROUP_ORDER,
    SourceClosureError,
    build_source_closure_v2,
    verify_source_closure_v2,
)


class SourceClosureV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.repository = base / "repository"
        self.snapshot = base / "accepted-snapshot"
        self.repository.mkdir()
        self.snapshot.mkdir()

        self.python_members = [f"python/p{index:02d}.py" for index in range(26)]
        self.shared_members = [f"shared/s{index:02d}.py" for index in range(26)]
        for path in self.python_members + self.shared_members:
            self._write(self.repository, path, f"# {path}\n")

        self._write(self.repository, "implementations/rwo-rust/Cargo.toml", "[package]\nname='fixture'\n")
        self._write(self.repository, "implementations/rwo-rust/Cargo.lock", "# lock\n")
        self._write(self.repository, "implementations/rwo-rust/src/lib.rs", "pub fn fixture() {}\n")
        self._write(
            self.repository,
            "implementations/rwo-rust/src/bin/fixture.rs",
            "fn main() {}\n",
        )

        self._write(self.repository, "implementations/rwo-sidecar-go/go.mod", "module fixture\n")
        self._write(self.repository, "implementations/rwo-sidecar-go/go.sum", "")
        self._write(self.repository, "implementations/rwo-sidecar-go/sidecar.go", "package fixture\n")
        self._write(
            self.repository,
            "implementations/rwo-sidecar-go/cmd/rwo-local-runtime/main.go",
            "package main\nfunc main() {}\n",
        )
        self._write(
            self.repository,
            "implementations/rwo-sidecar-go/testdata/case/input.json",
            "{}\n",
        )
        self._write(
            self.repository,
            "implementations/rwo-sidecar-go/README.md",
            "not executable source\n",
        )

        self._write(
            self.repository,
            "implementations/rwo_convergence/comparator.py",
            "from .provenance import VALUE\nRESULT = VALUE\n",
        )
        self._write(
            self.repository,
            "implementations/rwo_convergence/provenance.py",
            "from .canonical import VALUE\n",
        )
        self._write(
            self.repository,
            "implementations/rwo_convergence/canonical.py",
            "VALUE = 1\n",
        )

        for path in (
            self.python_members[0],
            self.shared_members[0],
            "implementations/rwo-rust/Cargo.toml",
            "implementations/rwo-sidecar-go/go.mod",
            "implementations/rwo_convergence/comparator.py",
        ):
            data = (self.repository / path).read_bytes()
            self._write_bytes(self.snapshot, path, data)

        self.successor_design = {
            "schema_version": "rwo.runner-source-closure-design/v2",
            "groups": [
                {
                    "group_id": "AX-PYTHON",
                    "member_count": 26,
                    "members": list(self.python_members),
                },
                {
                    "group_id": "AX-RUST",
                    "expansion": [
                        "implementations/rwo-rust/Cargo.toml",
                        "implementations/rwo-rust/Cargo.lock",
                        "implementations/rwo-rust/src/**",
                    ],
                },
                {
                    "group_id": "AX-CROSS-LANGUAGE",
                    "required_members": ["implementations/rwo_convergence/comparator.py"],
                },
                {
                    "group_id": "AX-GO",
                    "required_roots": [
                        "implementations/rwo-sidecar-go/go.mod",
                        "implementations/rwo-sidecar-go/go.sum",
                        "all current .go files including cmd/rwo-local-runtime/main.go",
                        "implementations/rwo-sidecar-go/testdata/**",
                    ],
                },
                {
                    "group_id": "AX-SHARED-DISPATCH",
                    "member_source": "the exact 26-member current profile list",
                },
            ],
        }
        self.profile = {
            "schema_version": "rwo.runner-profile/v1",
            "runners": [
                {
                    "runner_id": "RUN-PYTHON-REFERENCE",
                    "source_members": list(self.python_members[:18]),
                },
                {
                    "runner_id": "RUN-SHARED-DISPATCH-CHILD-LOCAL",
                    "source_members": list(self.shared_members),
                },
            ],
        }
        self.prior_closure = {
            "schema_version": "rwo.runner-source-closure/v1",
            "runner_groups": [
                {
                    "axis_id": "AX-SHARED-DISPATCH",
                    "required_source_members": list(self.shared_members[:12]),
                }
            ],
        }

    def tearDown(self) -> None:
        self._tmp.cleanup()

    @staticmethod
    def _write(root: Path, path: str, text: str) -> None:
        SourceClosureV2Tests._write_bytes(root, path, text.encode("utf-8"))

    @staticmethod
    def _write_bytes(root: Path, path: str, data: bytes) -> None:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def _accepted_binding(self) -> dict[str, object]:
        rows: list[TreeMember] = []
        for path in sorted(
            (item.relative_to(self.snapshot).as_posix() for item in self.snapshot.rglob("*") if item.is_file()),
            key=lambda value: value.encode("utf-8"),
        ):
            data = (self.snapshot / path).read_bytes()
            rows.append(TreeMember(path, len(data), hashlib.sha256(data).hexdigest()))
        return {
            "lock_sha256": "1" * 64,
            "tree_sha256": tree_digest(rows),
            "member_count": len(rows),
            "snapshot_locator": "fixture-accepted-snapshot",
        }

    def _source_bindings(self) -> list[dict[str, object]]:
        path = self.python_members[0]
        data = (self.repository / path).read_bytes()
        return [
            {
                "role": "fixture-design",
                "path": path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
            }
        ]

    def _build(
        self,
        *,
        design: dict[str, object] | None = None,
        profile: dict[str, object] | None = None,
        accepted_binding: dict[str, object] | None = None,
    ) -> tuple[dict[str, object], dict[str, object]]:
        return build_source_closure_v2(
            self.repository,
            self.snapshot,
            successor_design=design or self.successor_design,
            current_profile=profile or self.profile,
            prior_closure=self.prior_closure,
            accepted_binding=accepted_binding or self._accepted_binding(),
            source_bindings=self._source_bindings(),
            closure_id="fixture-closure",
        )

    def test_builds_exact_groups_delta_and_pure_comparator_closure(self) -> None:
        closure, delta = self._build()

        self.assertEqual(list(GROUP_ORDER), [item["group_id"] for item in closure["groups"]])
        groups = {item["group_id"]: item for item in closure["groups"]}
        self.assertEqual(26, groups["AX-PYTHON"]["member_count"])
        self.assertEqual(14, len(groups["AX-SHARED-DISPATCH"]["omission_witnesses"]))
        self.assertEqual(
            [
                "implementations/rwo_convergence/canonical.py",
                "implementations/rwo_convergence/comparator.py",
                "implementations/rwo_convergence/provenance.py",
            ],
            groups["AX-CROSS-LANGUAGE"]["members"],
        )
        self.assertFalse(
            groups["AX-CROSS-LANGUAGE"]["comparator_capability_audit"]["execution_attempted"]
        )
        self.assertEqual(
            "excluded-runtime-input",
            groups["AX-GO"]["child_executable_disposition"]["status"],
        )
        self.assertIn(
            "implementations/rwo-sidecar-go/cmd/rwo-local-runtime/main.go",
            groups["AX-GO"]["members"],
        )
        self.assertNotIn(
            "implementations/rwo-sidecar-go/README.md",
            groups["AX-GO"]["members"],
        )
        self.assertGreater(delta["added_count"], 0)
        self.assertEqual(0, delta["removed_count"])
        self.assertEqual("none", delta["authority_effect"])
        verify_source_closure_v2(self.repository, closure)

    def test_live_schema_accepts_live_shape_without_loosening(self) -> None:
        closure, _ = self._build()
        schema_path = (
            Path(__file__).resolve().parents[2]
            / "rwo_convergence"
            / "schemas"
            / "runner-source-closure-v2.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fixture = copy.deepcopy(closure)
        fixture["accepted_snapshot_binding"]["member_count"] = 85
        Draft202012Validator(schema).validate(fixture)

    def test_verifier_rejects_deletion(self) -> None:
        closure, _ = self._build()
        (self.repository / self.python_members[1]).unlink()
        with self.assertRaisesRegex(SourceClosureError, "does not exist"):
            verify_source_closure_v2(self.repository, closure)

    def test_verifier_rejects_mutation(self) -> None:
        closure, _ = self._build()
        self._write(self.repository, self.python_members[2], "# mutated\n")
        with self.assertRaisesRegex(SourceClosureError, "drift"):
            verify_source_closure_v2(self.repository, closure)

    def test_unsafe_member_path_blocks(self) -> None:
        design = copy.deepcopy(self.successor_design)
        design["groups"][0]["members"][0] = "../escape.py"
        with self.assertRaisesRegex(SourceClosureError, "normalized and repository-relative"):
            self._build(design=design)

    def test_dynamic_comparator_import_blocks(self) -> None:
        self._write(
            self.repository,
            "implementations/rwo_convergence/comparator.py",
            "import importlib\nRESULT = importlib.import_module('x')\n",
        )
        with self.assertRaisesRegex(SourceClosureError, "forbidden comparator capability"):
            self._build()

    def test_runner_launcher_import_blocks(self) -> None:
        self._write(
            self.repository,
            "implementations/rwo_convergence/comparator.py",
            "from .runners import run\n",
        )
        self._write(self.repository, "implementations/rwo_convergence/runners.py", "def run(): pass\n")
        with self.assertRaisesRegex(SourceClosureError, "runner-launcher"):
            self._build()

    def test_each_of_fourteen_shared_omission_members_is_mandatory(self) -> None:
        for path in self.shared_members[12:]:
            with self.subTest(path=path):
                profile = copy.deepcopy(self.profile)
                profile["runners"][1]["source_members"].remove(path)
                with self.assertRaisesRegex(SourceClosureError, "exactly 26"):
                    self._build(profile=profile)

    def test_go_local_runtime_main_is_mandatory(self) -> None:
        (self.repository / "implementations/rwo-sidecar-go/cmd/rwo-local-runtime/main.go").unlink()
        with self.assertRaisesRegex(SourceClosureError, "rwo-local-runtime/main.go"):
            self._build()

    def test_accepted_snapshot_binding_drift_blocks(self) -> None:
        binding = self._accepted_binding()
        binding["tree_sha256"] = "0" * 64
        with self.assertRaisesRegex(SourceClosureError, "tree digest mismatch"):
            self._build(accepted_binding=binding)

    def test_source_binding_drift_blocks(self) -> None:
        binding = self._accepted_binding()
        original = self._source_bindings
        try:
            self._source_bindings = lambda: [
                {
                    "role": "fixture-design",
                    "path": self.python_members[0],
                    "sha256": "0" * 64,
                    "size_bytes": os.stat(self.repository / self.python_members[0]).st_size,
                }
            ]
            with self.assertRaisesRegex(SourceClosureError, "source binding drift"):
                self._build(accepted_binding=binding)
        finally:
            self._source_bindings = original


if __name__ == "__main__":
    unittest.main()
