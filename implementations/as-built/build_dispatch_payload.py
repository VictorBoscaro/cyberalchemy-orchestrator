from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "implementations" / "as-built"
MANIFEST = OUT / "source-manifest.json"
DISPATCH_ID = "2026-07-31-implementation-as-built-reconciliation"
MODEL = "gpt-5.6-sol"


COMMON_CONTRACT = """
Work read-only outside implementations/as-built/. Treat code as the primary evidence of implementation state; tests executed in this investigation as proof; existing live host/runtime receipts as operational evidence; accepted decisions as authority; specs/discovery only as intended state and rationale. Never collapse implementation, proof, operation, authority, official adoption, or reconstructibility into one status. Every material claim must cite exact file/line, test command/result, runtime receipt, or decision. Absence of evidence is unknown, not false. Return a concise executive answer plus atomic claims, gaps, document drift, and unresolved disagreement. Do not fix product code or documentation. Do not run a fresh host smoke, launch another agent beyond the declared pair, mutate a real runtime store, or use network access. Tests that mutate state must use an isolated temporary store under C:/tmp/cyberalchemy-as-built/PAIR_ID. Browser behavior may be assessed from existing code/tests/evidence only; otherwise mark it unknown.
""".strip()


PAIRS = [
    {
        "id": "pair-01-system-of-record",
        "question": "What system actually exists, which entrypoints are reachable, and which runtime or store is official, auxiliary, closed, or experimental?",
        "property": "one intelligible system boundary and one source of record",
        "worker": ("Parnas, David", "explorer", "reconstruct the composition and ownership map from executable entrypoints and writers"),
        "reviewer": ("Brooks, Frederick P.", "skeptic", "attack reachability, dead code, closed routes, alternate entrypoints, and competing sources of truth"),
        "predicted": "Parnas runs constructive composition-and-ownership reconstruction from executable entrypoints and writers, while Brooks runs adversarial reachability and competing-source-of-truth falsification on the methodology axis; Parnas's bias toward treating present code as the operative system would be exposed by Brooks's dead-code, closed-route, and alternate-entrypoint counterexamples.",
        "tension_evidence": "Parnas's angle explicitly starts from executable entrypoints and writers; Brooks's angle explicitly attacks reachability, dead code, closed routes, alternate entrypoints, and competing truths.",
        "scope": "implementations composition roots, CLIs, readers, governed runtime, Control Center, local pilot, agent-runtime, and their writers/readers",
        "output": "Map entrypoint -> component -> writes/reads -> reachable state -> authority, plus an explicit disposition question for agent-runtime.",
    },
    {
        "id": "pair-02-host-adoption",
        "question": "Does every real Codex and Claude subagent launch, follow-up, failure, and close obligatorily pass through the governed runtime?",
        "property": "no meaningful work outside reconstructible memory",
        "worker": ("Lamport, Leslie", "explorer", "trace configuration, hook invocation, authorization, lifecycle ordering, and durable receipts"),
        "reviewer": ("Liskov, Barbara", "skeptic", "attack host-version behavior, tool-name mismatches, bypasses, missing events, and simulation-to-production substitution"),
        "predicted": "Lamport runs causal lifecycle tracing from configuration through authorization and durable receipts, while Liskov runs live-host counterexample testing for version drift, tool-name mismatch, bypass, and missing events on the methodology axis; Lamport's bias toward accepting configured or simulated closure as operational closure would be exposed by Liskov's host-observed failures.",
        "tension_evidence": "Lamport's angle traces configuration, hook invocation, ordering, and receipts; Liskov's angle targets precisely the ways configured or unit-tested behavior can diverge from the real host.",
        "scope": ".codex/.claude hook configuration, host dispatch and ingestion hooks, orchestration bridge, existing ledger/runtime receipts, and bounded isolated tests; no fresh live smoke",
        "output": "Observed transition matrix for launch, follow-up, success, failure, and interruption, marking observed/tested/code-only/failed/unknown.",
    },
    {
        "id": "pair-03-authority",
        "question": "Can each accepted or rejected action be traced to a legitimate authorizer, exact limits, and an actual enforcement point?",
        "property": "authority that constrains action rather than merely describing it",
        "worker": ("Hoare, C. A. R.", "explorer", "construct preconditions, capabilities, decisions, and receipts for one accepted and one rejected action"),
        "reviewer": ("Dijkstra, Edsger W.", "skeptic", "attack self-asserted identity, requested-versus-effective authority, mutable evidence, and unenforced fields"),
        "predicted": "Hoare runs constructive precondition-and-receipt derivation for accepted and rejected actions, while Dijkstra runs adversarial enforcement-origin analysis on the methodology axis; Hoare's bias toward equating a complete declared chain with effective authority would be exposed where Dijkstra finds self-asserted identity, mutable evidence, or unenforced limits.",
        "tension_evidence": "Hoare's angle constructs authority from preconditions, capabilities, decisions, and receipts; Dijkstra's angle challenges whether those same claims originate outside the constrained actor and are actually enforced.",
        "scope": "human confirmation, dispatch authority, capabilities, profiles, policies, parent bindings, launch authorization, receipts, and rejection paths",
        "output": "Authority chain for at least one accepted and one rejected action, with every limit mapped to an enforcement point or explicit gap.",
    },
    {
        "id": "pair-04-memory-recovery",
        "question": "After interruption, retry, corruption, or restart, does the harness converge to one recoverable history without orphan or duplicate official work?",
        "property": "durable continuity and unambiguous recovery",
        "worker": ("Deming, W. Edwards", "explorer", "establish durability, idempotency, replay, projection, backup, and recovery guarantees"),
        "reviewer": ("Weick, Karl E.", "skeptic", "construct crash points and ambiguous histories across host, ledger, journal, projections, and operator recovery"),
        "predicted": "Deming runs invariant and convergence analysis over durability, idempotency, replay, projection, backup, and recovery, while Weick runs crash-point and ambiguous-history construction across stores on the methodology axis; Deming's bias toward treating local convergence as end-to-end recoverability would be exposed by Weick's cross-boundary histories that admit multiple meanings.",
        "tension_evidence": "Deming's angle establishes runtime guarantees; Weick's angle injects failures across host, ledger, journal, projections, and operator recovery where those guarantees may cease to compose.",
        "scope": "journal, artifacts, canonicalization, transactions, projections, replay, idempotency, failpoints, local pilot verification, backup, retirement, and cross-store recovery",
        "output": "Failure matrix by lifecycle phase with durable state, recovery action, convergence proof, and uncovered scenarios.",
    },
    {
        "id": "pair-05-handoff-integrity",
        "question": "Do agent handoffs preserve exact content, producer, recipient, order, context, and authority through consumption?",
        "property": "trustworthy transfer of meaning and attribution",
        "worker": ("Wirth, Niklaus", "explorer", "trace manifests, bytes, digests, bindings, reference delivery, reveal delivery, and effective inputs"),
        "reviewer": ("Fowler, Martin", "skeptic", "attack substitution, stale identity, false producer attribution, replay, order drift, and protection of the wrong hash"),
        "predicted": "Wirth runs structural tracing of manifests, bytes, digests, bindings, deliveries, and effective inputs, while Fowler runs semantic substitution and attribution attacks on the methodology axis; Wirth's bias toward treating digest-bound structure as producer-and-consumer truth would be exposed by Fowler's stale-identity, false-attribution, replay, order-drift, and wrong-hash counterexamples.",
        "tension_evidence": "Wirth's angle verifies the minimal bound structures; Fowler's angle attacks whether those structures bind the correct semantic actor and content rather than merely some stable bytes.",
        "scope": "workflow bindings, outputs, BUS/reveal, AgentReferenceDelivery, effective inputs, artifacts, migrations 009-011, and adversarial tests",
        "output": "Handoff matrix for exact content, producer, recipient, authority, integrity, retry behavior, and remaining gap.",
    },
    {
        "id": "pair-06-reconstruction",
        "question": "Can a third party reconstruct why work existed, who did what, what context and references were received, and what evidence supports the result using only durable records?",
        "property": "honest reconstruction of work and reasoning",
        "worker": ("Nonaka, Ikujiro", "explorer", "perform a cold reconstruction across session, dispatch, research, references, observations, claims, and results"),
        "reviewer": ("Bourbaki, Nicolas", "auditor", "remove narrative knowledge and reject inferred joins or collapsed evidence axes such as delivered, accessed, used, and supporting"),
        "predicted": "Nonaka runs constructive cold reconstruction across sessions, dispatches, research, references, observations, claims, and results, while Bourbaki runs formal join and epistemic-type rejection on the methodology axis; Nonaka's bias toward converting distributed records into a coherent narrative would be exposed wherever Bourbaki cannot find a unique durable relation or must collapse delivered, accessed, used, and supporting evidence.",
        "tension_evidence": "Nonaka's angle attempts the complete reconstruction; Bourbaki's angle deliberately removes narrative knowledge and permits only uniquely persisted joins and explicitly typed evidence.",
        "scope": "APT sessions and projections, Session-to-Dispatch links, research capture, Scout/Probe records, reference evidence, claims/checks, queries, and real persisted examples",
        "output": "One cold reconstruction graph, unanswered questions, impermissible inferences, and the first missing link for each gap.",
    },
    {
        "id": "pair-07-human-control",
        "question": "What can a human actually see, understand, decide, change, undo, and recover without false authority or false reassurance?",
        "property": "meaningful and authority-safe human control",
        "worker": ("Alexander, Christopher", "explorer", "map operator journeys and useful affordances across reader, confirmation, Control Center, pilot, and recovery"),
        "reviewer": ("Rumelt, Richard", "skeptic", "attack symbolic buttons, preview-as-apply confusion, unavailable evidence shown as zero, and recovery dependent on undocumented knowledge"),
        "predicted": "Alexander runs constructive operator-journey and affordance mapping, while Rumelt runs authority-and-executability falsification on the methodology axis; Alexander's bias toward treating visible, coherent interaction as effective control would be exposed by Rumelt wherever a button is symbolic, preview resembles apply, unavailable evidence resembles zero, or recovery depends on undocumented knowledge.",
        "tension_evidence": "Alexander's angle evaluates usable journeys across reader, confirmation, Control Center, pilot, and recovery; Rumelt's angle tests whether each apparent control is backed by authority, evidence, and an executable next action.",
        "scope": "dispatch reader, confirmation UI, Control Center APIs/frontends, evidence overlays, preview store, local pilot, backup/retirement, accessibility and browser evidence",
        "output": "Operator matrix for see, understand, decide, act, undo/recover, including authority and practical limits.",
    },
]


def agent_record(name: str, role: str, angle: str, prompt: str, budget: int = 5000):
    return {
        "agent_name": name,
        "role": role,
        "model": MODEL,
        "token_budget": budget,
        "angle": angle,
        "initial_prompt": prompt,
    }


groups = []
pairwise_predictions = []
seat_capability_profiles = []
for pair in PAIRS:
    worker_name, worker_role, worker_angle = pair["worker"]
    reviewer_name, reviewer_role, reviewer_angle = pair["reviewer"]
    pair_contract = COMMON_CONTRACT.replace("PAIR_ID", pair["id"])
    worker_prompt = f"""You are the worker and designated pair finalizer for {pair['id']}. Central question: {pair['question']} Property served: {pair['property']}. Scope: {pair['scope']}. {pair_contract} Start independently from code and executable entrypoints. Run only bounded tests relevant to this question. Return your independent claim packet to the parent, then wait for a parent follow-up containing the reviewer's task name and independent attack. Engage in at most three parent-mediated robot-talk exchanges focused only on material disagreements. Only after the reviewer has had a final chance to accept or preserve dissent, write implementations/as-built/pairs/{pair['id']}.json and .md. Preserve both authors, all unresolved dissent, and the robot-talk history. Required output: {pair['output']}"""
    reviewer_prompt = f"""You are the independent read-only reviewer for {pair['id']}. Central question: {pair['question']} Property served: {pair['property']}. Scope: {pair['scope']}. {pair_contract} Form your attack before reading the worker's claims. Seek counterexamples and evidence that lowers a claim from operational to tested, from tested to code-only, or from authorized to merely declared. Return the independent attack to the parent, then wait for a parent follow-up containing the worker's task name and claims. Participate in at most three parent-mediated robot-talk exchanges. Do not write repository files and do not force consensus; your final response must state which claims are accepted, corrected, or disputed so the worker can preserve them. Required output: {pair['output']}"""
    groups.append(
        {
            "group_id": pair["id"],
            "n": 2,
            "robot_talks": True,
            "anti_bias": "methodology",
            "agents": [
                agent_record(worker_name, worker_role, worker_angle, worker_prompt),
                agent_record(reviewer_name, reviewer_role, reviewer_angle, reviewer_prompt),
            ],
        }
    )
    pairwise_predictions.append(
        {
            "group_id": pair["id"],
            "pair": [worker_name, reviewer_name],
            "predicted_disagreement": pair["predicted"],
            "evidence_for_prediction": pair["tension_evidence"],
        }
    )
    seat_capability_profiles.extend(
        [
            {
                "seat_id": f"{pair['id']}:worker",
                "agent_name": worker_name,
                "read_scope": "frozen source manifest",
                "shell_scope": f"read-only diagnostics and bounded tests; stateful tests only under C:/tmp/cyberalchemy-as-built/{pair['id']}",
                "collaboration_scope": "paired reviewer and parent only; no child agents",
                "write_scope": [
                    f"implementations/as-built/pairs/{pair['id']}.json",
                    f"implementations/as-built/pairs/{pair['id']}.md",
                ],
                "network": "denied",
            },
            {
                "seat_id": f"{pair['id']}:reviewer",
                "agent_name": reviewer_name,
                "read_scope": "frozen source manifest",
                "shell_scope": f"read-only diagnostics and bounded tests; stateful tests only under C:/tmp/cyberalchemy-as-built/{pair['id']}",
                "collaboration_scope": "paired worker and parent only; no child agents",
                "write_scope": [],
                "network": "denied",
            },
        ]
    )

synth_prompt = f"""You are the synthesizer for {DISPATCH_ID}. Read the seven final pair JSON/Markdown packets under implementations/as-built/pairs/ and the frozen source manifest. Before synthesis, validate every pair JSON against implementations/as-built/pair-output-schema.json. If any packet is missing or invalid, write a blocked synthesis-report.json validated against implementations/as-built/synthesis-report-schema.json and do not write AS-BUILT.md. If all seven are valid, draft synthesis-report.json with exactly seven packet digests and a non-empty claim index, validate it against the synthesis schema, and only then write implementations/AS-BUILT.md. Do not redo investigations or silently resolve dissent. Write AS-BUILT.md as a code-first, evidence-bounded snapshot. Sections 1-3 must be self-contained for a non-technical reader: (1) the harness objective—preserve the chain from objective, decision, authority, work, context and evidence to reconstructible continuity; (2) what can actually be trusted today, organized by properties rather than modules; (3) the current frontier and next gains, stating what each task buys. Then provide: real work journey; actual system and official/experimental boundaries; authority and identity; memory, handoffs and recovery; provenance and reconstruction; human control; document drift; next program of work; method and claim index. Keep implementation, proof, operation, authority, official adoption and reconstructibility separate. Every material claim must carry or link a claim_id and evidence. Preserve unknown and disputed findings. Do not edit product code or any document other than implementations/AS-BUILT.md and implementations/as-built/synthesis-report.json."""

groups.append(
    {
        "group_id": "synthesizer",
        "agents": [
            {
                "agent_name": "Meadows, Donella H.",
                "role": "synthesizer",
                "model": MODEL,
                "token_budget": 9000,
                "initial_prompt": synth_prompt,
            }
        ],
    }
)

seat_capability_profiles.append(
    {
        "seat_id": "synthesizer:writer",
        "agent_name": "Meadows, Donella H.",
        "read_scope": "seven validated pair packets, source manifest, output schemas, and claim evidence referenced by packets",
        "shell_scope": "read-only validation of packet presence/digests; no product tests or browser",
        "collaboration_scope": "parent only; no child agents",
        "write_scope": ["implementations/AS-BUILT.md", "implementations/as-built/synthesis-report.json"],
        "network": "denied",
    }
)

pair_ids = [pair["id"] for pair in PAIRS]
connections = [
    {"from": pair["id"], "to": "synthesizer", "type": "sequential"}
    for pair in PAIRS
]
connections.extend(
    {"from": pair_ids[index], "to": pair_ids[index + 1], "type": "sequential"}
    for index in range(len(pair_ids) - 1)
)

dispatch_record = {
    "dispatch_id": DISPATCH_ID,
    "schema_version": "0.6.1",
    "dispatch_type": "others",
    "goal": "Produce a code-first AS-BUILT of the current agent-work harness, separating what exists, what is proven, what runs in real hosts, what is authorized, what is official, and what can be reconstructed.",
    "context": "The repository contains a dispatch reader, governed runtime, provenance runtime, Control Center, host hooks, and an experimental shadow runtime whose documentation and implementation status have drifted. Seven tensioned worker/reviewer pairs investigate end-to-end trust properties, then one synthesizer writes implementations/AS-BUILT.md from their evidence. The user explicitly authorized dispatch without another confirmation on 2026-07-31.",
    "max_loops": 1,
    "final_approver": "parent",
    "meta": True,
    "anti_bias_global": "constructive capability reconstruction versus adversarial claim-boundary falsification across end-to-end harness concerns",
    "working_folder": "implementations/as-built",
    "groups": groups,
    "connections": connections,
}

manifest_digest = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
structural = {
    "projection_schema_version": "cyberalchemy.structural-graph-proposal/v1",
    "revision": "1",
    "objective": dispatch_record["goal"],
    "boundary": "Read-only investigation of implementation and evidence; writes limited to implementations/as-built/** and implementations/AS-BUILT.md.",
    "group_count": 8,
    "seat_count": 15,
    "topology": "seven sequential batches; each batch runs one worker and one reviewer concurrently with parent-mediated robot-talks; synthesizer runs after all seven validated packets",
    "scheduler": {
        "concurrency_limit": 4,
        "parent_slots": 1,
        "batch_order": pair_ids,
        "batch_shape": "worker + reviewer concurrently",
        "pair_protocol": "both return independent positions; parent injects canonical peer task names and exchanges only contested claims; worker finalizes after reviewer disposition",
        "packet_validation": "parent validates schema and hashes after every batch",
    },
    "robot_talks": {"groups": [p["id"] for p in PAIRS], "max_exchanges_per_pair": 3},
    "output_join": "synthesizer consumes only finalized pair packets and preserves unresolved dissent",
    "confirmation_mode": "final_only-explicitly-authorized-by-user-message",
    "budget_envelope": {"pair_seats": 14, "pair_tokens_each": 5000, "synthesizer_tokens": 9000},
}
structural_bytes = json.dumps(structural, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
structural_digest = hashlib.sha256(structural_bytes).hexdigest()

proposal = {
    "projection_schema_version": "cyberalchemy.concrete-dispatch-proposal/v1",
    "revision": "1",
    "structural_ref": "implementations/as-built/structural-proposal.json",
    "structural_digest": structural_digest,
    "dispatch_record": dispatch_record,
    "work_kind": "code-first as-built audit and document synthesis",
    "response_contract_ref": "implementations/as-built/pair-output-schema.json",
    "source_manifest_ref": "implementations/as-built/source-manifest.json",
    "source_manifest_sha256": manifest_digest,
    "source_bindings": json.loads(MANIFEST.read_text(encoding="utf-8"))["files"],
    "write_scope": ["seat-specific scopes in proposed_capability_profiles"],
    "network_scope": "none",
    "sandbox_scope": "repository read; bounded output write only",
    "effective_enforcement": "filesystem diffs and produced artifacts are observable; per-seat tool and model enforcement is non_observable and therefore treated as requested, not effective",
    "requested_provider": "openai",
    "requested_adapter": "codex-collaboration",
    "pairwise_tension": pairwise_predictions,
    "proposed_capability_profiles": seat_capability_profiles,
    "capability_review": {
        "status": "pass-via-external-receipt",
        "receipt_ref": "implementations/as-built/capability-review-receipt.json",
    },
    "check_tension": {
        "status": "both-pass-via-external-receipts",
        "checker_receipt_ref": "implementations/as-built/check-tension-checker-receipt.json",
        "reviewer_receipt_ref": "implementations/as-built/check-tension-reviewer-receipt.json",
    },
    "user_authorization": {
        "date": "2026-07-31",
        "evidence": "User: 'pode criar o payload usando a skill subagents-strategy e disparar. Nao precisa confirmar comigo o dispatch'",
        "scope": "the seven-pair AS-BUILT strategy proposed immediately before this request",
    },
}

claim_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": ["claim_id", "statement", "dimensions", "evidence_for", "evidence_against", "confidence", "missing_evidence", "implication_for_harness"],
    "properties": {
        "claim_id": {"type": "string"},
        "statement": {"type": "string"},
        "dimensions": {
            "type": "object",
            "additionalProperties": False,
            "required": ["implementation", "proof", "operation", "authority", "official_adoption", "reconstructibility"],
            "properties": {
                key: {"enum": ["yes", "partial", "no", "unknown", "disputed"]}
                for key in ["implementation", "proof", "operation", "authority", "official_adoption", "reconstructibility"]
            },
        },
        "evidence_for": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "evidence_against": {"type": "array", "items": {"type": "string"}},
        "confidence": {"enum": ["high", "medium", "low"]},
        "missing_evidence": {"type": "array", "items": {"type": "string"}},
        "implication_for_harness": {"type": "string"},
    },
}

gap_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": ["gap_id", "statement", "property_lost", "smallest_next_action", "what_it_buys", "completion_evidence"],
    "properties": {
        "gap_id": {"type": "string"},
        "statement": {"type": "string"},
        "property_lost": {"type": "string"},
        "smallest_next_action": {"type": "string"},
        "what_it_buys": {"type": "string"},
        "completion_evidence": {"type": "string"},
    },
}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "AS-BUILT pair output",
    "type": "object",
    "additionalProperties": False,
    "required": ["question_id", "scope", "excluded_scope", "worker", "reviewer", "finalizer", "executive_answer", "property_served", "claims", "gaps", "document_drift", "open_disagreements", "robot_talk_history", "commands_executed", "snapshot"],
    "properties": {
        "question_id": {"type": "string"},
        "scope": {"type": "string"},
        "excluded_scope": {"type": "string"},
        "worker": {"type": "string"},
        "reviewer": {"type": "string"},
        "finalizer": {"type": "string"},
        "executive_answer": {"type": "string"},
        "property_served": {"type": "string"},
        "claims": {"type": "array", "minItems": 1, "items": claim_schema},
        "gaps": {"type": "array", "items": gap_schema},
        "document_drift": {"type": "array", "items": {"type": "string"}},
        "open_disagreements": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["claim_id", "worker_position", "reviewer_position", "worker_evidence", "reviewer_evidence"],
                "properties": {
                    "claim_id": {"type": "string"},
                    "worker_position": {"type": "string"},
                    "reviewer_position": {"type": "string"},
                    "worker_evidence": {"type": "array", "items": {"type": "string"}},
                    "reviewer_evidence": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "robot_talk_history": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["round", "contested_claims", "outcome"],
                "properties": {
                    "round": {"type": "integer", "minimum": 1, "maximum": 3},
                    "contested_claims": {"type": "array", "items": {"type": "string"}},
                    "outcome": {"type": "string"},
                },
            },
        },
        "commands_executed": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["command", "exit_code", "result", "write_effects"],
                "properties": {
                    "command": {"type": "string"},
                    "exit_code": {"type": "integer"},
                    "result": {"type": "string"},
                    "write_effects": {"type": "string"},
                },
            },
        },
        "snapshot": {
            "type": "object",
            "additionalProperties": False,
            "required": ["commit", "dirty_state", "source_manifest_sha256"],
            "properties": {
                "commit": {"type": "string"},
                "dirty_state": {"type": "string"},
                "source_manifest_sha256": {"type": "string"},
            },
        },
    },
}

synthesis_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "AS-BUILT synthesis report",
    "type": "object",
    "additionalProperties": False,
    "required": ["status", "source_manifest_sha256", "packets", "missing_or_invalid_packets", "preserved_conflicts", "claim_index"],
    "properties": {
        "status": {"enum": ["complete", "blocked"]},
        "source_manifest_sha256": {"type": "string"},
        "packets": {
            "type": "array",
            "maxItems": 7,
            "uniqueItems": True,
            "items": {
                "type": "object",
                "required": ["question_id", "path", "sha256"],
                "properties": {
                    "question_id": {"type": "string"},
                    "path": {"type": "string"},
                    "sha256": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
        "missing_or_invalid_packets": {"type": "array", "items": {"type": "string"}},
        "preserved_conflicts": {"type": "array", "items": {"type": "string"}},
        "claim_index": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["claim_id", "as_built_section", "evidence"],
                "properties": {
                    "claim_id": {"type": "string"},
                    "as_built_section": {"type": "string"},
                    "evidence": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
        },
    },
    "allOf": [
        {
            "if": {"properties": {"status": {"const": "complete"}}},
            "then": {
                "properties": {
                    "packets": {
                        "minItems": 7,
                        "maxItems": 7,
                        "prefixItems": [
                            {"properties": {"question_id": {"const": pair_id}}}
                            for pair_id in pair_ids
                        ],
                        "items": False,
                    },
                    "claim_index": {"minItems": 1},
                    "missing_or_invalid_packets": {"maxItems": 0},
                }
            },
            "else": {
                "properties": {
                    "packets": {"minItems": 0, "maxItems": 7},
                    "claim_index": {"minItems": 0},
                    "missing_or_invalid_packets": {"minItems": 1},
                }
            },
        },
    ],
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "structural-proposal.json").write_text(json.dumps(structural, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
structural_digest = hashlib.sha256((OUT / "structural-proposal.json").read_bytes()).hexdigest()
proposal["structural_digest"] = structural_digest
(OUT / "dispatch-payload.json").write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "dispatch-record.json").write_text(json.dumps(dispatch_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "pair-output-schema.json").write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "synthesis-report-schema.json").write_text(json.dumps(synthesis_schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(proposal["pair_output_contract_ref"], proposal["pair_output_contract_sha256"]) = (
    "implementations/as-built/pair-output-schema.json",
    hashlib.sha256((OUT / "pair-output-schema.json").read_bytes()).hexdigest(),
)
(proposal["synthesis_contract_ref"], proposal["synthesis_contract_sha256"]) = (
    "implementations/as-built/synthesis-report-schema.json",
    hashlib.sha256((OUT / "synthesis-report-schema.json").read_bytes()).hexdigest(),
)
(OUT / "dispatch-payload.json").write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "pairs").mkdir(parents=True, exist_ok=True)
