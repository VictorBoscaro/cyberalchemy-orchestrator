from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]


class RegisterDispatchCopyDriftTests(unittest.TestCase):
    def read(self, host: str, skill: str, file: str = "SKILL.md") -> bytes:
        return (REPO / f".{host}/skills/{skill}/{file}").read_bytes()

    def test_appenders_are_byte_identical(self) -> None:
        copies = [self.read(host, "register-dispatch", "append-dispatch.cjs") for host in ("claude", "agents", "codex")]
        self.assertEqual(copies[1:], copies[:1] * 2)

    def test_register_skill_migration_contract_is_semantically_equal(self) -> None:
        def facts(raw: bytes) -> dict[str, object]:
            text = raw.decode("utf-8")
            return {
                "current_schema": "0.7.0" in text,
                "current_registry": "implementations/contracts/dispatch-type-registry.v2.json" in text,
                "opening_role_ref": bool(re.search(r"\| `agent_role_registry_ref` \| .*accepted ref selected", text)),
                "close_role_ref": bool(re.search(r"\| `agent_role_registry_ref` \| .*repeat the opening ref", text)),
                "identity_key": bool(re.search(r"\| `agent_name` \|", text)),
            }

        copies = [facts(self.read(host, "register-dispatch")) for host in ("claude", "agents", "codex")]
        self.assertEqual(copies[1:], copies[:1] * 2)
        self.assertTrue(all(copies[0].values()), copies[0])

    def test_strategy_registry_authority_paragraph_is_equal(self) -> None:
        def authority(raw: bytes) -> str:
            text = raw.decode("utf-8")
            match = re.search(
                r"Treat the returned route as one unit\.(.*?)registry is available only for explicit historical verification and never authorizes a new row\.",
                text,
                re.DOTALL,
            )
            self.assertIsNotNone(match)
            return " ".join(match.group(0).split())

        copies = [authority(self.read(host, "domainspec-subagents-strategy")) for host in ("claude", "agents", "codex")]
        self.assertEqual(copies[1:], copies[:1] * 2)
        self.assertIn("dispatch-type-registry.v2.json", copies[0])
        self.assertIn("immutable v1", copies[0])


if __name__ == "__main__":
    unittest.main()
