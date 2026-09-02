from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
INSTALLER = REPO / "tools/install-register-dispatch-runtime.ps1"
LEGACY = REPO / "implementations/contracts/legacy/register-dispatch-runtime-package.v1"


class RegisterDispatchInstallerTests(unittest.TestCase):
    def run_installer(self, target: Path, *switches: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(INSTALLER), "-Target", str(target), *switches],
            cwd=REPO,
            text=True,
            capture_output=True,
        )
        if check and completed.returncode != 0:
            self.fail(f"installer failed ({completed.returncode})\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}")
        return completed

    def new_repo(self, root: Path) -> None:
        (root / ".git").mkdir(parents=True)

    def test_v2_installs_then_checks_in_clean_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.new_repo(target)
            self.run_installer(target)
            result = self.run_installer(target, "-Check")
            self.assertIn("verified register-dispatch runtime 0.7.0", result.stdout)

    def test_frozen_v1_projection_checks_in_clean_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.new_repo(target)
            for source in LEGACY.rglob("*"):
                if source.is_file() and source.name != "register-dispatch-runtime-package.v1.json":
                    destination = target / source.relative_to(LEGACY)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
            destination_manifest = target / "implementations/contracts/register-dispatch-runtime-package.v1.json"
            destination_manifest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(LEGACY / "register-dispatch-runtime-package.v1.json", destination_manifest)
            result = self.run_installer(target, "-LegacyVerification", "-Check")
            self.assertIn("verified frozen recoverable v1 projection 0.6.4", result.stdout)
            self.assertIn("original root-v1 manifest authority is not verified or reconstructed", result.stdout)

    def test_v2_selection_mix_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.new_repo(target)
            self.run_installer(target)
            selection_path = target / "implementations/contracts/agent-role-registry-selection.json"
            selection = json.loads(selection_path.read_text(encoding="utf-8"))
            selection["selected_ref"]["version"] = "2"
            selection_path.write_text(json.dumps(selection), encoding="utf-8")
            result = self.run_installer(target, "-Check", check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("digest mismatch: implementations/contracts/agent-role-registry-selection.json", result.stderr)


if __name__ == "__main__":
    unittest.main()
