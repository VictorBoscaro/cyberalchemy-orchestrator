from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from implementations.server.runtime.errors import GateBlockedError, IntegrityError
from implementations.server.runtime.cli import run
from implementations.server.runtime.operator_recovery import (
    create_local_pilot_backup,
    retire_local_pilot_database,
    verify_local_pilot_database,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings

REPO = Path(__file__).resolve().parents[3]
GOLDEN_LEDGER = (
    REPO
    / "docs/features/agents-communication-infra/adrs/fixtures/"
    "golden-opening-v0.6.1.yaml"
)


class OperatorRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = self.root / "ledger.yaml"
        shutil.copyfile(GOLDEN_LEDGER, self.ledger)
        self.database = self.root / "pilot.sqlite3"
        self.service = RuntimeService(
            RuntimeSettings(self.database, REPO, self.ledger)
        )
        self.service.open()
        self.service.register_profiles()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_verify_and_online_backup_preserve_journal_identity(self) -> None:
        source = verify_local_pilot_database(self.database, repo_root=REPO)
        backup_path = self.root / "backups" / "pilot.sqlite3"
        backup = create_local_pilot_backup(
            self.database, backup_path, repo_root=REPO
        )
        restored = verify_local_pilot_database(backup_path, repo_root=REPO)

        self.assertEqual(source["identity"], backup["identity"])
        self.assertEqual(source["identity"], restored["identity"])
        self.assertEqual(backup["profiles"], 4)
        self.assertTrue(backup["projection"]["current"])

    def test_backup_refuses_overwrite(self) -> None:
        destination = self.root / "backup.sqlite3"
        destination.write_bytes(b"operator-owned")
        with self.assertRaisesRegex(GateBlockedError, "already exists"):
            create_local_pilot_backup(self.database, destination, repo_root=REPO)
        self.assertEqual(destination.read_bytes(), b"operator-owned")

    def test_supported_cli_verifies_and_backs_up(self) -> None:
        verified = run(
            [
                "verify-local-pilot-database",
                "--database",
                str(self.database),
                "--repo-root",
                str(REPO),
            ]
        )
        destination = self.root / "cli-backup.sqlite3"
        backup = run(
            [
                "backup-local-pilot-database",
                "--source",
                str(self.database),
                "--destination",
                str(destination),
                "--repo-root",
                str(REPO),
            ]
        )
        self.assertEqual(verified["identity"], backup["identity"])
        self.assertTrue(destination.exists())

    def test_failed_source_check_removes_incomplete_backup(self) -> None:
        corrupt = self.root / "corrupt.sqlite3"
        corrupt.write_bytes(b"not a sqlite database")
        destination = self.root / "backup.sqlite3"

        with self.assertRaises(Exception):
            create_local_pilot_backup(corrupt, destination, repo_root=REPO)

        self.assertFalse(destination.exists())
        self.assertEqual(
            list(self.root.glob(f".{destination.name}.incomplete-*")), []
        )

    def test_tampered_database_fails_verification(self) -> None:
        with self.service.database.connect() as conn:
            conn.execute("PRAGMA foreign_keys=OFF")
            conn.execute(
                "UPDATE aggregate_heads SET last_event_id='tampered' WHERE aggregate_id=(SELECT aggregate_id FROM aggregate_heads LIMIT 1)"
            )
        with self.assertRaisesRegex(IntegrityError, "aggregate head"):
            verify_local_pilot_database(self.database, repo_root=REPO)

    def test_substituted_profile_set_fails_verification(self) -> None:
        with self.service.database.connect() as conn:
            conn.execute(
                """
                UPDATE protocol_profiles
                SET authoritative_path='substituted/profile.json'
                WHERE profile_id=(
                  SELECT profile_id FROM protocol_profiles ORDER BY profile_id LIMIT 1
                )
                """
            )
        with self.assertRaisesRegex(IntegrityError, "verified manifest"):
            verify_local_pilot_database(self.database, repo_root=REPO)

    def test_retirement_requires_matching_backup_and_is_recoverable(self) -> None:
        backup_path = self.root / "backup.sqlite3"
        create_local_pilot_backup(self.database, backup_path, repo_root=REPO)
        retirement = self.root / "retired" / "pilot.sqlite3"

        receipt = retire_local_pilot_database(
            self.database,
            retirement,
            verified_backup=backup_path,
            repo_root=REPO,
            confirmed_stopped=True,
        )

        self.assertFalse(self.database.exists())
        self.assertTrue(retirement.exists())
        self.assertTrue(backup_path.exists())
        self.assertTrue(receipt["recoverable"])
        self.assertEqual(
            verify_local_pilot_database(retirement, repo_root=REPO)["identity"],
            verify_local_pilot_database(backup_path, repo_root=REPO)["identity"],
        )

    def test_retirement_refuses_active_sidecar(self) -> None:
        backup_path = self.root / "backup.sqlite3"
        create_local_pilot_backup(self.database, backup_path, repo_root=REPO)
        sidecar = Path(str(self.database) + "-wal")
        sidecar.write_bytes(b"active-or-unrecovered")

        with self.assertRaisesRegex(GateBlockedError, "confirm.*stopped"):
            retire_local_pilot_database(
                self.database,
                self.root / "retired.sqlite3",
                verified_backup=backup_path,
                repo_root=REPO,
            )
        self.assertTrue(self.database.exists())

    def test_retirement_refuses_valid_but_nonmatching_backup(self) -> None:
        other_database = self.root / "other.sqlite3"
        other_service = RuntimeService(
            RuntimeSettings(other_database, REPO, self.ledger)
        )
        other_service.open()
        other_service.register_profiles()

        with self.assertRaisesRegex(GateBlockedError, "does not match"):
            retire_local_pilot_database(
                self.database,
                self.root / "retired.sqlite3",
                verified_backup=other_database,
                repo_root=REPO,
                confirmed_stopped=True,
            )
        self.assertTrue(self.database.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
