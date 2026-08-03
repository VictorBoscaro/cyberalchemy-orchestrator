# Pair 07 — Human control

Worker: Alexander, Christopher  
Reviewer: Rumelt, Richard  
Finalizer: Alexander, Christopher

## Executive answer

Human control exists, but it is fragmented and mostly observational. A person can inspect pending and recorded work, navigate goals, relationships and evidence, acknowledge one pending proposal, keep a browser-local draft, and manually verify, back up or retire the pilot database.

Those actions do not form one authority-safe control loop. The confirmation button creates only a local marker: it does not authenticate the human, freeze the exact authority or cause the runtime to accept work. The Control Center deliberately cannot apply, retry or reconcile authoritative changes. Its visible draft validation is a browser-only length check, disconnected from the stronger in-process proposal store. Database retirement preserves verified copies, but there is no supported restore command. Most importantly, this investigation itself looks governed in repository records while this seat has no runtime binding receipt.

## Operator matrix

| Human need | What exists | Authority | Practical limit |
|---|---|---|---|
| See | Dispatch overview, pending sheets and history; Control Center attention, catalog, detail, topology, paths and evidence | Read-only; configured owner/auth labels do not authenticate the reader | Current skill relationship coverage is partial; browser proof is historical |
| Understand | Goals, context, roles, topology, evidence source, freshness, unknown/partial warnings and explicit Phase-1 boundary | The UI can explain limits but cannot certify that the operator understood them | Human comprehension, trust, screen-reader experience and complete WCAG remain untested |
| Decide | Linear can acknowledge a readable, unconfirmed pending sheet | No authenticated actor, immutable authority digest or runtime acceptance | The decision is a timestamped marker only; no automatic consumer was found |
| Act | Create marker; save browser-local draft/preferences; run pilot and recovery CLI commands | Marker has no execution authority; Control Center has no authoritative commands | Draft validation is synthetic; pilot actions require expert CLI knowledge |
| Undo / recover | Draft can be manually edited; verified backup and byte-preserving retirement exist | No unconfirm/undo route; retirement requires explicit stopped confirmation and matching backup | Reconfirm refreshes timestamp; no supported restore/reinstate operation exists |

## Claims

- **HC-01 — Read surfaces:** broad observation is implemented, but present completeness is partial and comprehension is unproven.
- **HC-02 — Confirmation:** the marker path is implemented and tested, but it is neither authenticated nor runtime-authoritative and has no undo.
- **HC-03 — Control Center:** withholding authoritative mutation is a real safety property; the visible browser draft does not use the stronger local-store contract.
- **HC-04 — Recovery:** verification, backup and byte-preserving retirement are implemented and tested; restoration remains manual and unspecified.
- **HC-05 — UX evidence:** the historical 204-screenshot matrix proves bounded automated behavior, not current human usability or accessibility.
- **HC-06 — False reassurance:** the declared AS-BUILT topology exists, but this seat lacked the mandatory binding prefix and the live runtime has zero bindings for the parent Dispatch.

Exact evidence, dimension verdicts and missing evidence are preserved in the companion JSON.

## Ordered remedies and what they buy

1. Bind human confirmation to an authenticated principal, exact immutable bytes and a runtime acceptance receipt. This buys proof of who authorized what and that the resulting work actually began from that authority.
2. Fail closed on a missing host binding and show declared-versus-bound-versus-terminal reconciliation. This buys detection of orphaned work and removes false governance reassurance.
3. Connect the UI to one versioned local draft/validation port, or remove the unused stronger store and narrow the claim. This buys honest, recoverable preparation without confusing a length check with validation.
4. Add a receipt-backed restore/reinstate command and rehearse it. This converts recoverable bytes into operational recovery.
5. Resolve or accept the current partial source, refresh browser evidence and complete independent, assistive-technology and human review. This buys current confidence in what operators see and understand.

## Document drift

- The shared UI contract says the human-gate button is disabled, but Linear implements marker confirmation; the implementation README already calls that clause stale.
- Linear says the orchestrator watches or picks up the marker, but no automatic marker consumer exists in code. The older discovery more honestly describes an active session noticing it manually.
- Control Center documents describe versioned local proposal semantics, while the shipping UI uses localStorage and a text-length preview; the in-process store is not exposed.
- Current Control Center tests still expect a complete skill graph although the running source adapter correctly reports an unresolved relationship as partial.
- The pair used the current manifest and the source-drift record; it does not attribute the runtime/service.py change.

## Robot-talk outcome

One round resolved every material issue. The worker accepted the reviewer's stricter boundary between configured labels and authentication, marker and authority, preserved bytes and supported restoration, historical automation and human understanding, and declared governance and runtime binding. No dissent remains.

## Verification

- Current Control Center selection: 28 tests, 26 passed and 2 exposed current source/test drift (`complete` became `partial`; topology `success` became `truncated`).
- Confirmation and recovery selection: 9/9 passed in the isolated pair directory.
- Read-only live runtime query: zero host bindings for this parent Dispatch.
- No browser was launched successfully in this investigation. The reviewer's attempt failed before launch during temporary-path setup; both agents relied only on existing browser evidence.

## Snapshot

- Commit: `63777abd838995c8512bcea806546c3f2ab6add6`
- Current source manifest SHA-256: `82447f792685d81a6a2481c9b70b42dba2bf27a1326066a145407629ab9c330b`
- This pair changed only its JSON and Markdown outputs.
