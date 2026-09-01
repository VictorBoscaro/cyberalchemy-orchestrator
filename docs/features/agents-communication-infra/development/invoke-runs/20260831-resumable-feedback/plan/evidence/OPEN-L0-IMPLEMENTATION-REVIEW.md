# OPEN-L0 implementation review

Date: 2026-09-01

Unit: `SWU-ACI-OPEN-AUDIT-PROJECTION-L0-001`

Verdict: **PASS / KEEP**

This receipt freezes an independently reviewed, non-authoritative experiment. It proves that the
frozen 0.6.4 audit-opening row can be projected deterministically and compared by two structurally
independent implementations. It does not stamp authority, select architecture option A, B or C,
create a production consumer, or advance a real Run beyond `opening_pending`.

## Reviewed work-pack inputs

| Artifact | SHA-256 |
|---|---|
| `open-l0-work-pack/TASK-OPEN-L0-001.md` | `sha256:d2810caa5eece5534a047dc41f3513667d6e7b47e469d5fa65df5d078e5231e3` |
| `open-l0-work-pack/SWU-ACI-OPEN-AUDIT-PROJECTION-L0-001.json` | `sha256:d5e9a2446db74cf4eeaab6ea83abb42977017c649576dd2538ece07b87780839` |
| `open-l0-work-pack/SWU-ACI-OPEN-AUDIT-PROJECTION-L0-001-code-readiness.json` | `sha256:e25c6c1734e0e35c2c84c2c02500e33d9eb7d5d7cb27f36f5fb21f8e7582ad24` |

The readiness receipt contained exactly the canonical 11 keys and all immutable pins reproduced.

## Reviewed outputs

| Artifact | SHA-256 |
|---|---|
| `implementations/experiments/aci_open_l0/projector.py` | `sha256:5a2628548b82ebd1b1b625bfa9ca8d36af713adb755d3a6cd7e1ebc5e2cae48f` |
| `implementations/experiments/aci_open_l0/independent_oracle.py` | `sha256:334feb909c454105d3cdda3506596d9b93fdd517935aa831ecdc2442fd05efef` |
| `implementations/experiments/aci_open_l0/fixtures/synthetic-input.json` | `sha256:c35ddb903aa7e6b0db243d56f2037b5174b3f7a6f65338a4eedfa3a6bf24d785` |
| `implementations/experiments/aci_open_l0/fixtures/expected-unstamped-row.json` | `sha256:0662d10568ab3b9804ee71bab45b880ebf11cca1e5cbd3989e7467a25160955f` |
| `implementations/experiments/aci_open_l0/fixtures/expected-discrepancy-report.json` | `sha256:458b6624dcb87deb981fb1565b9ce38c511d76fb725247f7ca22694fb97bd1f4` |
| `implementations/tests/experiments/test_aci_open_l0_projection.py` | `sha256:5c09bd47c28c023062e5f29e996f2521797eb88d97ad186e73fc223098199f8c` |

The independent recomputation produced:

- unstamped row: `sha256:1d82b64e52ddb591cefba7c26d3a16604e88efd633457a8a78460939cd248e14`;
- bindings: `sha256:08b6187952975e632c603dc3ce9462a379d55749807eacf1f093644db13c5fa3`;
- discrepancy report: `sha256:8dc00a1cbf55176401ec5de29781109939d79d396fda51d3e141f4a32e1f1af7`;
- composite projection: `sha256:53af5e8b491282ead643050f8d7747c377884d7ea4fae30188c673af1f5ba636`.

## Verification

- focused OPEN-L0 suite: 9 passed;
- Python compilation: PASS;
- full runtime regression: 200 passed;
- `git diff --check`: PASS, apart from pre-existing line-ending warnings;
- projector/oracle shared implementation helpers or imports: none;
- appender, runtime, legacy compiler, database, network, process or other effect use: none;
- surviving CRITICAL or MAJOR findings: none.

Reviewer conclusion: keep the experiment as component evidence only. The authoritative opening route
remains a separate A/B/C architecture decision and a later governed implementation unit.
