# POLICY-000 DomainSpec integrated review

Date: 2026-09-01

Verdict: **PASS / KEEP**

This receipt reviews the normative DomainSpec amendment for the pure POLICY-000/L0 execution-policy
oracle. It proves specification coherence only. It does not prove an implementation, persist policy
artifacts, authorize a runtime plan/request/effect, select product budgets or grants, synthesize
cutover evidence, or advance POLICY-001/L1, POLICY-002/L2 or POLICY-003/L3.

## Reviewed normative artifacts

| Artifact | SHA-256 | Verdict |
|---|---|---|
| `specs/domain.md` | `sha256:986bb2db5e602ad81df576e04f84d49643c31769098c278ae936ada55eb2714d` | KEEP |
| `specs/SPEC.md` | `sha256:37337699cf8313e13ed162ce495fdbeaa6aed8bd16fbc4f7c4aede59613bfd30` | KEEP |
| `specs/TEST-SPEC.md` | `sha256:6bb27f65fe11c02c0b9f6ade6ad11b14b046a1c689b248e68c3902dcabdeeb51` | KEEP |
| `specs/rules.md` | `sha256:8c0010dfe88026060127f80a4ee08ea10051f95bd288b9244d6f596e65c75047` | KEEP |
| `specs/interfaces.md` | `sha256:c257dd59a1a895c8007d4fa4f041bab038086bb3d439bd9e5c3d0977d84f8cde` | KEEP |
| `specs/architecture.md` | `sha256:3ac37b4f1d85b28d0d6d48daa37fa82dc90d009d93c9e5f165c82b7a3363a510` | KEEP |
| `specs/glossary.md` | `sha256:9bfb5f4d27da40489209dfe273a48164f88ba195b110a20017db4eb9965d5816` | KEEP |

## Governing technical evidence

- `TECH-POLICY-D0.md`:
  `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e`;
- `TECH-D0-REVIEW.md`:
  `sha256:43ba27747ccaa54d6a4cc49ed3102ea582423f19f1ad6a69f5de7d6e5f291179`.

## Independent checks

- Concept Registry to glossary coverage: 145/145, with no missing, extra or duplicate IDs;
- local links and anchors: 1,208 checked, zero failures;
- POLICY-000 tests: `T-ACI-POL0-1` through `T-ACI-POL0-8`, unique and linked to headings;
- reviewed canonical literals: seven of seven SHA-256 goldens independently reproduced;
- integer domain: signed 64-bit bounds explicit for budgets, child processes and fence epochs;
- reference boundary: exact caller-supplied target bytes and owner-contract digest verification,
  with no parser I/O or invented universal credential schema;
- filesystem boundary: lexical path grammar and `link_policy=deny` at L0; physical
  symlink/junction/reparse/containment enforcement remains POLICY-003/L3;
- authority firewall: zero external calls/effects and no production authority from harness/oracle;
- CONF-001 baseline: uniformly bounded at durable `opening_pending`, one pending/unclaimed opening
  intent and zero external action;
- `git diff --check`: PASS, apart from informational line-ending warnings.

No CRITICAL, MAJOR or MINOR finding survived the final independent review.
