"""Run the bounded RWO candidate-local prototype checks without network access."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    environment.setdefault("CARGO_NET_OFFLINE", "true")
    environment.setdefault("CARGO_TARGET_DIR", "/tmp/rwo-rust-target")
    environment.setdefault("GOCACHE", "/tmp/rwo-go-build-cache")
    return environment


def _run(label: str, command: list[str], *, cwd: Path) -> None:
    print(f"==> {label}")
    completed = subprocess.run(command, cwd=cwd, env=_environment(), check=False)
    if completed.returncode:
        raise SystemExit(f"{label} failed with exit {completed.returncode}")


def main() -> None:
    _run(
        "Python RWO oracle",
        [
            sys.executable,
            "-m",
            "unittest",
            "implementations.tests.rwo.test_contract_vectors",
            "implementations.tests.rwo.test_kernel_vectors",
            "implementations.tests.rwo.test_cross_language_witness",
            "implementations.tests.rwo.test_prototype",
            "-v",
        ],
        cwd=ROOT,
    )
    _run(
        "Rust raw-admission and semantic core",
        [
            "cargo",
            "test",
            "--manifest-path",
            "implementations/rwo-rust/Cargo.toml",
            "--offline",
        ],
        cwd=ROOT,
    )
    _run(
        "Go gRPC sidecar boundary",
        ["go", "test", "./..."],
        cwd=ROOT / "implementations/rwo-sidecar-go",
    )
    print("RWO candidate-local prototype validation passed.")


if __name__ == "__main__":
    main()
