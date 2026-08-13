# Post-change amendment review — Stage-A bootstrap contract

**Reviewed artifact:** `bootstrap-contract.json`  
**Reviewed SHA-256:** `0F5F0B55380D12367050982EE72D8E871099F5A6A29CFFA2DDC12FF624563EBF`  
**Verdict:** **PASS**

## Verification

The amendment truthfully treats the interrupted filesystem state as evidence, not authorship or
implementation authority. It records the first reconciler timeout, incomplete arrays, the fresh
finalizer's BLOCK and incorrect occurrence targeting, and the absence of an attributable legacy or
host-hook production receipt. It does not retrofit either unknown diff to an old owner or invent an
ACI, ledger, bridge, or governed-run receipt.

The frozen recovery inputs match the current filesystem exactly:

| path | current SHA-256 | bytes | full diff SHA-256 |
|---|---:|---:|---:|
| `stage-a/baseline.json` | `199D8E12D5365831D9148FE69A70C2616DFA7D11FBDB4B1F7730A843423579DC` | 106001 | `217148D33F02692C3FFD9B98C5E9FA6BA6DDE8F0F3624F6848A49261B6D2F674` |
| `implementations/server/runtime/legacy.py` | `0EF6C4EE96199CE9EA73102EE9922DE35DB79AF1A7E9EA5495743329AB1F8728` | 5431 | `6B7143BE7546A556696F0F4A4DBD6FFA0DD875504904138250CA566D40BC796B` |
| `implementations/server/runtime/host_dispatch_hook.py` | `9448A3259149F08EC3F32D7428A2CBFE0413FAA4C5D816504DE42442A81FA5B0` | 33135 | `C6D8CB52FA6780FDF62F31D0130C6CB479F9A1357C182A1597D532C1961F2447` |

The diff digests were independently recomputed using each declared PowerShell `Out-String`/UTF-8
basis. The legacy diff is limited to adding `0.6.4` to the whitelist and adjacent error. The host
diff is limited to registry/resolver imports, canonical compatibility-route synthesis, the registry
schema, attached `capability_route`, and close-time route-digest continuity. These are the exact
approved intent boundaries; adoption still requires independent line-by-line adjudication.

Recovery ownership is disjoint and fail-closed:

- a fresh baseline-repair owner may change only `baseline.json`, must preserve the original
  baseline observations verbatim, quarantine only invalid reconciliation residue, and block if any
  frozen input changes;
- separate fresh read-only auditors decide `ADOPT` or `REIMPLEMENT` for legacy and host-hook bytes;
- separate fresh adoption owners either adopt the unchanged exact frozen bytes under a new,
  non-authorship receipt or restore only the frozen unattributed hunks before implementing the
  approved bounded intent;
- mismatch, ambiguous overlap, incomplete clean-byte recovery, or changing protected bytes blocks;
  original-baseline/user hunks and independently attributable producer hunks remain preserved;
- a fresh independent post-adoption reviewer must PASS the repaired baseline, both adjudications,
  both attributable receipts, intent conformance, intervening-hunk accounting, and preservation
  before any fixture resume, test, or integrity work.

Timeout and interruption remain non-terminal residue and transfer neither authorship nor authority.
The graph keeps recovery and adoption ahead of tests, tests ahead of integrity, and integrity ahead
of the frozen multi-lens terminal review. No test or integrity result is claimed by this amendment or
this review.

The approved parent remains frozen at
`2D9C9C3B3ACD66D0A0C11DF69F2BC9265B45A3384BB7C317D7F76F78CB342051`, and the prior terminal
SA-01 review PASS at
`9CFEFA575DB22467BB3C3BC7F91CDDA94838EA0E7B6BEFBF836D1AB84EBAE7F7` is not broadened: the new
amendment changes only recovery from the later interrupted state. The contract may proceed to the
baseline-repair owner and the two independent adoption paths. This PASS approves only the amended
recovery contract at the reviewed hash; it is not implementation, test, integrity, or terminal
Stage-A approval evidence.
