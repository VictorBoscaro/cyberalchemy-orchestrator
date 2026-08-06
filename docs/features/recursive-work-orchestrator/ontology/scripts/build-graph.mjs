import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ONTOLOGY_ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const TARGET_ROOT = path.resolve(ONTOLOGY_ROOT, "../../../..");
const UMBRELLA_ROOT = process.env.RWO_UMBRELLA_ROOT
  ? path.resolve(process.env.RWO_UMBRELLA_ROOT)
  : path.resolve(TARGET_ROOT, "../..");
const FILES = {
  ontology: path.join(ONTOLOGY_ROOT, "ONTOLOGY.md"),
  evidence: path.join(ONTOLOGY_ROOT, "evidence/CURRENT-STATE-2026-08-05.json"),
  bridge: path.join(UMBRELLA_ROOT, "cyberAlchemy-v2/development/agent-reasoning-engine/design/rwo-integration/ONTOLOGY-BRIDGE.md"),
  nodes: path.join(ONTOLOGY_ROOT, "nodes/nodes.json"),
  relations: path.join(ONTOLOGY_ROOT, "relations/relations.json"),
  view: path.join(ONTOLOGY_ROOT, "views/current-state.json")
};

const stripInline = (value) => value.trim().replace(/^`|`$/g, "");
const slug = (value) => value
  .toLowerCase()
  .replace(/^rwo:/, "")
  .replace(/[^a-z0-9]+/g, "-")
  .replace(/^-|-$/g, "");
const sourceNodeId = (id) => `rwo:source:${slug(id)}`;
const unique = (values) => [...new Set(values)];
const section = (text, start, end) => {
  const from = text.indexOf(start);
  const to = text.indexOf(end, from + start.length);
  if (from < 0 || to < 0) throw new Error(`cannot resolve section ${start} -> ${end}`);
  return text.slice(from, to);
};
const tableRows = (text) => text
  .split("\n")
  .filter((line) => line.startsWith("|") && !/^\|\s*-/.test(line))
  .map((line) => line.split("|").slice(1, -1).map((cell) => cell.trim()));
const serialize = (value) => `${JSON.stringify(value, null, 2)}\n`;

const proofToRuntime = (proof) => ({
  "freshly-executed": "freshly-executed",
  observed: "observed",
  "execution-unverified": "execution-unverified",
  proposal: "absent",
  hypothesis: "not-applicable"
}[proof] ?? "deferred");

const sourceRuntime = (source) => ({
  E1: "observed",
  E2: "absent",
  "E2-WG": "not-applicable",
  E3: "observed",
  C1: "designed",
  K1: "not-applicable"
}[source.id]);

const sourceStatus = (source) => ({
  E1: "accepted-evidence",
  E2: "deferred",
  "E2-WG": "hypothesis",
  E3: "accepted-evidence",
  C1: "deferred",
  K1: "killed"
}[source.id]);

const sourceForbidden = {
  E1: ["Observed implementation precedent is not RWO realization, host adoption, production operation, or semantic authority."],
  E2: ["Proposal bytes are not implementation, runtime conformance, canonical vocabulary, or promotion."],
  "E2-WG": ["A tracked hypothesis does not select workflow taxonomy or collapse WorkNode into AgentNode."],
  E3: ["Private local ARE evidence does not prove cross-repository compatibility or integrated runtime conformance."],
  C1: ["A reviewed documentation contract does not select owners, accept schemas, or authorize implementation."],
  K1: ["A documented topology prohibition does not prove runtime enforcement by itself."]
};

const residueOwners = {
  "001": "RWO work-state and journal owners",
  "002": "confirmation and Dispatch authority owners",
  "003": "protocol, adapter, and storage owners",
  "004": "work-policy owner",
  "005": "coordination and semantic-governance owners",
  "006": "versioning and replay owners",
  "007": "authorization and effect-boundary owners",
  "008": "validation and evidence owner",
  "009": "Work-contract owner",
  "010": "canonical-definition and promotion owners",
  "011": "ontology source owner then event-contract owner",
  "012": "ontology source owner then mapping-contract owner",
  "013": "ontology source owner then adapter owner",
  "014": "ontology source owner then relation-contract owner",
  "015": "workflow-graph discovery owner",
  "016": "workflow taxonomy owner",
  "017": "identity and runtime-domain owner",
  "018": "protocol and workflow-schema owners",
  "019": "workflow and Bus Contracts owners",
  "020": "group and coordination owner",
  "021": "Run, audit, and closure owners",
  "022": "workflow-state and retry owner",
  "023": "protocol compilation, confirmation, and Dispatch owners",
  "024": "projection, UI, and telemetry owners",
  "025": "reasoning-entry and dispatch authority owners",
  "026": "artifact-admission owner",
  "027": "exact-effect and authorization owners",
  "028": "cross-repository contract owners",
  "029": "validation and evidence owner"
};

const findingResidue = {
  "rwo:finding.current.dispatch-definition": ["rwo:residue.023", "rwo:residue.028"],
  "rwo:finding.current.run-identity": ["rwo:residue.017"],
  "rwo:finding.current.leaf-adapter": ["rwo:residue.013", "rwo:residue.028"],
  "rwo:finding.current.graph-expansion": ["rwo:residue.002", "rwo:residue.008", "rwo:residue.023", "rwo:residue.029"],
  "rwo:finding.current.sequence": ["rwo:residue.023", "rwo:residue.029"],
  "rwo:finding.current.fan-out": ["rwo:residue.020", "rwo:residue.029"],
  "rwo:finding.current.fan-in": ["rwo:residue.005", "rwo:residue.020", "rwo:residue.029"],
  "rwo:finding.current.gate-route": ["rwo:residue.005", "rwo:residue.025", "rwo:residue.029"],
  "rwo:finding.current.sidecar": ["rwo:residue.004", "rwo:residue.013", "rwo:residue.024", "rwo:residue.029"],
  "rwo:finding.current.bounded-repeat": ["rwo:residue.004", "rwo:residue.022", "rwo:residue.029"],
  "rwo:finding.current.protocol": ["rwo:residue.003", "rwo:residue.006", "rwo:residue.018", "rwo:residue.028"],
  "rwo:finding.current.journal": ["rwo:residue.001", "rwo:residue.006", "rwo:residue.028"],
  "rwo:finding.current.effect-adapter": ["rwo:residue.007", "rwo:residue.027", "rwo:residue.028", "rwo:residue.029"],
  "rwo:finding.proposal.implementation-status": ["rwo:residue.008", "rwo:residue.010", "rwo:residue.029"],
  "rwo:finding.hypothesis.agent-node-collapse": Array.from({ length: 10 }, (_, index) => `rwo:residue.${String(index + 15).padStart(3, "0")}`),
  "rwo:finding.bridge.no-second-control-plane": Array.from({ length: 5 }, (_, index) => `rwo:residue.${String(index + 25).padStart(3, "0")}`)
};

const precedentByFinding = {
  "rwo:finding.current.dispatch-definition": ["confirmed-dispatch-row", "Confirmed dispatch row and compiler"],
  "rwo:finding.current.run-identity": ["bound-address", "Bound dispatch address"],
  "rwo:finding.current.leaf-adapter": ["host-hook-translation", "Host-hook translation"],
  "rwo:finding.current.graph-expansion": ["dispatch-launch-plan", "Dispatch groups and launch plan"],
  "rwo:finding.current.sequence": ["declared-handoff", "Declared handoff"],
  "rwo:finding.current.fan-out": ["finite-three-seat-launch", "Finite three-seat launch"],
  "rwo:finding.current.fan-in": ["declared-join", "Declared join"],
  "rwo:finding.current.gate-route": ["typed-handoff-label", "Typed handoff label"],
  "rwo:finding.current.sidecar": ["apt-ui-projection", "APT and UI projection"],
  "rwo:finding.current.bounded-repeat": ["declared-follow-up", "Declared follow-up"],
  "rwo:finding.current.protocol": ["aci-command-event-lanes", "ACI command and event lanes"],
  "rwo:finding.current.journal": ["aci-journal", "ACI accepted journal"],
  "rwo:finding.current.effect-adapter": ["fixed-effect-double", "ARE fixed effect double"]
};

const gates = [
  {
    id: "entry",
    label: "Reasoning entry owner gate",
    owner: "owner-selection-required:reasoning-entry-verdict",
    selection: "unresolved",
    question: "Who owns and versions ReasoningEntryVerdict?",
    residues: ["rwo:residue.025", "rwo:residue.028", "rwo:residue.029"]
  },
  {
    id: "aci-lifecycle",
    label: "ACI lifecycle acceptance gate",
    owner: "ACI lifecycle and journal owner",
    selection: "source-boundary-selected-runtime-conformance-absent",
    question: "Which exact ACI schemas and conformance receipts admit the cross-repository command and journal cut?",
    residues: ["rwo:residue.028", "rwo:residue.029"]
  },
  {
    id: "observation-admission",
    label: "Observation admission owner gate",
    owner: "owner-selection-required:observation-admission",
    selection: "unresolved",
    question: "Who admits lifecycle and external observations into the semantic evaluator?",
    residues: ["rwo:residue.028", "rwo:residue.029"]
  },
  {
    id: "semantic-evaluator",
    label: "Semantic evaluator boundary",
    owner: "Agent Reasoning Engine route",
    selection: "local-L0-only-integrated-conformance-absent",
    question: "Which catalog-applicability, precedence, and challenge-closure owners govern integrated L0 inputs?",
    residues: ["rwo:residue.028", "rwo:residue.029"]
  },
  {
    id: "artifact-admission",
    label: "Artifact admission owner gate",
    owner: "owner-selection-required:artifact-admission",
    selection: "blocked",
    question: "Who admits semantic artifact bytes and which immutable schema is accepted?",
    residues: ["rwo:residue.026", "rwo:residue.028", "rwo:residue.029"]
  },
  {
    id: "exact-effect",
    label: "Exact-effect owner gate",
    owner: "owner-selection-required:exact-effect",
    selection: "unresolved",
    question: "Who owns the exact-effect verdict and exact effect envelope?",
    residues: ["rwo:residue.027", "rwo:residue.028", "rwo:residue.029"]
  },
  {
    id: "effect-adapter",
    label: "Effect adapter boundary",
    owner: "owner-selection-required:effect-adapter",
    selection: "unresolved",
    question: "Which adapter owns attempt evidence and honest-unknown outcomes after ACI intent acceptance?",
    residues: ["rwo:residue.027", "rwo:residue.028", "rwo:residue.029"]
  }
];

const stageGateMap = {
  entry: ["entry"],
  "command-acceptance": ["aci-lifecycle"],
  history: ["aci-lifecycle"],
  "observation-admission": ["observation-admission"],
  "l0-semantics": ["semantic-evaluator"],
  "artifact-admission": ["artifact-admission"],
  "exact-effect": ["exact-effect"],
  "effect-lifecycle": ["aci-lifecycle", "effect-adapter"],
  replay: ["aci-lifecycle", "semantic-evaluator"],
  revalidation: ["entry", "semantic-evaluator"]
};

const stageResidues = {
  entry: ["rwo:residue.025", "rwo:residue.028", "rwo:residue.029"],
  "command-acceptance": ["rwo:residue.028", "rwo:residue.029"],
  history: ["rwo:residue.001", "rwo:residue.006", "rwo:residue.028", "rwo:residue.029"],
  "observation-admission": ["rwo:residue.028", "rwo:residue.029"],
  "l0-semantics": ["rwo:residue.028", "rwo:residue.029"],
  "artifact-admission": ["rwo:residue.026", "rwo:residue.028", "rwo:residue.029"],
  "exact-effect": ["rwo:residue.027", "rwo:residue.028", "rwo:residue.029"],
  "effect-lifecycle": ["rwo:residue.027", "rwo:residue.028", "rwo:residue.029"],
  replay: ["rwo:residue.006", "rwo:residue.028", "rwo:residue.029"],
  revalidation: ["rwo:residue.025", "rwo:residue.028", "rwo:residue.029"]
};

const witnessTarget = {
  F1: "rwo:stage:command-acceptance",
  F2: "rwo:WorkGraph",
  F3: "rwo:FanIn",
  F4: "rwo:Sidecar",
  F5: "rwo:stage:entry",
  F6: "rwo:stage:exact-effect",
  F7: "rwo:stage:replay",
  F8: "rwo:stage:entry"
};

export const buildGraph = async () => {
  const [ontology, evidenceText, bridge] = await Promise.all([
    readFile(FILES.ontology, "utf8"),
    readFile(FILES.evidence, "utf8"),
    readFile(FILES.bridge, "utf8")
  ]);
  const evidence = JSON.parse(evidenceText);
  const nodes = [];
  const relations = [];
  const relationIds = new Set();

  const addNode = (node) => nodes.push({ ...node, authority_effect: "none" });
  const addRelation = ({ predicate, relation_kind, source_node, target_node, owner_route, evidence_refs, cycle_policy = "acyclic", runtime_posture = "designed", properties = {}, description, forbidden_inferences }) => {
    const ordinal = String(relations.length + 1).padStart(3, "0");
    const relation_id = `rwo:relation:${ordinal}-${slug(predicate)}`;
    if (relationIds.has(relation_id)) throw new Error(`duplicate relation ${relation_id}`);
    relationIds.add(relation_id);
    relations.push({
      relation_id,
      predicate,
      relation_kind,
      source_node,
      target_node,
      direction: "directed",
      owner_route,
      evidence_refs: unique(evidence_refs),
      authority_effect: "none",
      cycle_policy,
      runtime_posture,
      properties,
      description,
      forbidden_inferences
    });
  };

  for (const source of evidence.sources) {
    addNode({
      node_id: sourceNodeId(source.id),
      label: `${source.id} — ${source.kind}`,
      node_kind: "evidence-source",
      branch: ["E3", "C1", "K1"].includes(source.id) ? "bridge" : "system",
      description: source.proof_status,
      source_refs: [],
      owner_route: "accepted-research-evidence-closure",
      candidate_status: sourceStatus(source),
      runtime_posture: sourceRuntime(source),
      confidence: {
        evidence_confidence: "high",
        commitment_confidence: ["E1", "E3", "K1"].includes(source.id) ? "accepted-research" : "deferred"
      },
      properties: { ...source },
      residue_refs: source.id === "E2-WG" ? Array.from({ length: 10 }, (_, index) => `rwo:residue.${String(index + 15).padStart(3, "0")}`) : [],
      forbidden_inferences: sourceForbidden[source.id]
    });
  }

  const elementRows = tableRows(section(ontology, "## 3. Element-type catalog", "## 4. Typed-property catalog"))
    .filter((row) => /^`rwo:/.test(row[0]));
  for (const [idCell, label, parentCell, description, sourceSelector] of elementRows) {
    const node_id = stripInline(idCell);
    const parent_type = stripInline(parentCell);
    addNode({
      node_id,
      label,
      node_kind: "architecture-element",
      branch: "system",
      description,
      source_refs: [sourceNodeId("E2")],
      owner_route: "RWO source owner",
      candidate_status: "proposal",
      runtime_posture: "absent",
      confidence: { evidence_confidence: "low", commitment_confidence: "candidate" },
      properties: {
        parent_type: parent_type === "—" ? null : parent_type,
        source_selector: sourceSelector
      },
      residue_refs: [],
      forbidden_inferences: ["A candidate architecture element is not implementation, runtime conformance, or canonical vocabulary."]
    });
    if (parent_type !== "—") {
      addRelation({
        predicate: "specializes",
        relation_kind: "structural",
        source_node: node_id,
        target_node: parent_type,
        owner_route: "RWO source owner",
        evidence_refs: [sourceNodeId("E2")],
        runtime_posture: "designed",
        properties: { transitive_within_type_hierarchy: true },
        description: `${node_id} is a project-local subtype of ${parent_type}.`,
        forbidden_inferences: ["Local subtype structure does not promote either term or imply runtime realization."]
      });
    }
  }

  const residueRows = tableRows(section(ontology, "## 12. Residue", "## 13. Validation status"))
    .filter((row) => /^`rwo:residue\./.test(row[0]));
  for (const [idCell, statementCell, impactCell] of residueRows) {
    const node_id = stripInline(idCell);
    const number = node_id.slice(-3);
    const state = number === "026" ? "blocked" : "open";
    const sourceId = Number(number) <= 14 ? "E2" : Number(number) <= 24 ? "E2-WG" : "C1";
    addNode({
      node_id,
      label: `Residue ${number}`,
      node_kind: "residue",
      branch: Number(number) >= 25 ? "bridge" : "system",
      description: `${stripInline(statementCell)} — ${stripInline(impactCell)}`,
      source_refs: [sourceNodeId(sourceId)],
      owner_route: residueOwners[number],
      candidate_status: state === "blocked" ? "blocked" : "deferred",
      runtime_posture: state === "blocked" ? "blocked" : "not-applicable",
      confidence: { evidence_confidence: "high", commitment_confidence: state === "blocked" ? "blocked" : "deferred" },
      properties: {
        statement: stripInline(statementCell),
        impact_or_status: stripInline(impactCell),
        state
      },
      residue_refs: [],
      forbidden_inferences: ["Open residue is not a closed decision, an assigned owner, or an implementation defect by default."]
    });
  }

  for (const finding of evidence.findings) {
    const recognizedSources = finding.evidence_refs
      .filter((ref) => evidence.sources.some((source) => source.id === ref))
      .map(sourceNodeId);
    addNode({
      node_id: finding.finding_id,
      label: `${finding.status.toUpperCase()} — ${finding.subject_ref}`,
      node_kind: "property-finding",
      branch: finding.finding_id.includes(".bridge.") ? "bridge" : "system",
      description: finding.observed,
      source_refs: recognizedSources,
      owner_route: finding.owner_route,
      candidate_status: "projected",
      runtime_posture: proofToRuntime(finding.proof_status),
      confidence: {
        evidence_confidence: finding.proof_status === "freshly-executed" ? "high" : "medium",
        commitment_confidence: finding.status === "pass" ? "accepted-research" : "deferred"
      },
      properties: {
        profile_ref: finding.profile_ref,
        constraint_ref: finding.constraint_ref,
        expected: finding.expected,
        observed: finding.observed,
        finding_status: finding.status,
        evidence_stage: finding.evidence_stage,
        proof_status: finding.proof_status,
        correspondence: finding.correspondence,
        source_posture: finding.source_posture,
        promotion_effect: finding.promotion_effect,
        evidence_selectors: finding.evidence_refs.filter((ref) => !evidence.sources.some((source) => source.id === ref))
      },
      residue_refs: findingResidue[finding.finding_id] ?? [],
      forbidden_inferences: finding.forbidden_inferences
    });
    addRelation({
      predicate: "evaluates",
      relation_kind: "finding",
      source_node: finding.finding_id,
      target_node: finding.subject_ref,
      owner_route: finding.owner_route,
      evidence_refs: recognizedSources,
      runtime_posture: proofToRuntime(finding.proof_status),
      properties: {
        profile_ref: finding.profile_ref,
        constraint_ref: finding.constraint_ref,
        finding_status: finding.status,
        proof_status: finding.proof_status,
        correspondence: finding.correspondence
      },
      description: `${finding.finding_id} evaluates ${finding.subject_ref} without claiming direct realization.`,
      forbidden_inferences: ["A finding relation does not promote, implement, or authorize its subject."]
    });
    for (const sourceRef of recognizedSources) {
      addRelation({
        predicate: "supports",
        relation_kind: "evidence",
        source_node: sourceRef,
        target_node: finding.finding_id,
        owner_route: "accepted-research-evidence-closure",
        evidence_refs: [sourceRef],
        runtime_posture: proofToRuntime(finding.proof_status),
        properties: { proof_status: finding.proof_status },
        description: `${sourceRef} supports the bounded finding ${finding.finding_id}.`,
        forbidden_inferences: ["Evidence support is not authority, promotion, or later-stage conformance."]
      });
    }
    for (const residueRef of findingResidue[finding.finding_id] ?? []) {
      addRelation({
        predicate: "blocked-by",
        relation_kind: "governance",
        source_node: finding.finding_id,
        target_node: residueRef,
        owner_route: residueOwners[residueRef.slice(-3)],
        evidence_refs: recognizedSources,
        runtime_posture: "blocked",
        properties: {},
        description: `${finding.finding_id} cannot advance beyond its claim ceiling until ${residueRef} is resolved by its owner.`,
        forbidden_inferences: ["The ontology cannot resolve or assign the blocking owner."]
      });
    }

    const precedent = precedentByFinding[finding.finding_id];
    if (precedent) {
      const precedentId = `rwo:precedent:${precedent[0]}`;
      addNode({
        node_id: precedentId,
        label: precedent[1],
        node_kind: "implementation-precedent",
        branch: finding.source_posture === "private-evidence" ? "bridge" : "system",
        description: finding.observed,
        source_refs: recognizedSources,
        owner_route: finding.owner_route,
        candidate_status: "observed",
        runtime_posture: proofToRuntime(finding.proof_status),
        confidence: {
          evidence_confidence: finding.proof_status === "freshly-executed" ? "high" : "medium",
          commitment_confidence: "accepted-research"
        },
        properties: {
          finding_ref: finding.finding_id,
          proof_status: finding.proof_status,
          correspondence: finding.correspondence
        },
        residue_refs: findingResidue[finding.finding_id] ?? [],
        forbidden_inferences: finding.forbidden_inferences
      });
      addRelation({
        predicate: "observes",
        relation_kind: "finding",
        source_node: finding.finding_id,
        target_node: precedentId,
        owner_route: finding.owner_route,
        evidence_refs: recognizedSources,
        runtime_posture: proofToRuntime(finding.proof_status),
        properties: { proof_status: finding.proof_status },
        description: `${finding.finding_id} records the bounded observation represented by ${precedentId}.`,
        forbidden_inferences: ["The observed precedent is not automatically an RWO implementation."]
      });
      addRelation({
        predicate: "corresponds-to",
        relation_kind: "finding",
        source_node: precedentId,
        target_node: finding.subject_ref,
        owner_route: finding.owner_route,
        evidence_refs: recognizedSources,
        runtime_posture: proofToRuntime(finding.proof_status),
        properties: {
          correspondence: finding.correspondence,
          finding_status: finding.status,
          proof_status: finding.proof_status
        },
        description: `${precedentId} has ${finding.correspondence} correspondence to ${finding.subject_ref}.`,
        forbidden_inferences: ["Correspondence weaker than direct realization cannot be reported as implementation conformance."]
      });
    }
  }

  const hypothesisId = "rwo:hypothesis:every-graph-node-agent";
  addNode({
    node_id: hypothesisId,
    label: "Every workflow graph node is an AgentNode",
    node_kind: "hypothesis",
    branch: "system",
    description: "Tracked discovery hypothesis that conflicts with an RWO WorkNode which may be a gate, join, operation, or structural position.",
    source_refs: [sourceNodeId("E2-WG")],
    owner_route: "workflow taxonomy and identity owners",
    candidate_status: "hypothesis",
    runtime_posture: "not-applicable",
    confidence: { evidence_confidence: "high", commitment_confidence: "deferred" },
    properties: { resolution_status: "unresolved", conflicting_subject: "rwo:WorkNode" },
    residue_refs: findingResidue["rwo:finding.hypothesis.agent-node-collapse"],
    forbidden_inferences: ["The hypothesis cannot redefine WorkNode or assign agent identity and authority to every graph position."]
  });
  addRelation({
    predicate: "challenges",
    relation_kind: "contradiction",
    source_node: "rwo:finding.hypothesis.agent-node-collapse",
    target_node: hypothesisId,
    owner_route: "workflow taxonomy and identity owners",
    evidence_refs: [sourceNodeId("E2-WG")],
    runtime_posture: "not-applicable",
    properties: { resolution_status: "unresolved" },
    description: "The accepted finding preserves the unresolved conflict between WorkNode and the every-node-is-AgentNode hypothesis.",
    forbidden_inferences: ["Recording the contradiction does not choose either taxonomy."]
  });

  const bridgeStageRows = tableRows(section(bridge, "## Conditional stage map", "## Required sequence"))
    .filter((row) => row.length >= 7 && row[0] !== "Stage");
  const stageIds = [];
  for (const [stageCell, producer, boundary, consumer, ownerBoundary, failClosed, evidenceStatus] of bridgeStageRows) {
    const stageSlug = slug(stageCell);
    const node_id = `rwo:stage:${stageSlug}`;
    stageIds.push(node_id);
    const blocked = evidenceStatus.toLowerCase().includes("blocked");
    const observed = evidenceStatus.toLowerCase().includes("observed") || evidenceStatus.toLowerCase().includes("witness");
    addNode({
      node_id,
      label: stripInline(stageCell),
      node_kind: "integration-stage",
      branch: "bridge",
      description: `${stripInline(producer)} -> ${stripInline(boundary)} -> ${stripInline(consumer)}`,
      source_refs: [sourceNodeId("E3"), sourceNodeId("C1")],
      owner_route: stripInline(ownerBoundary),
      candidate_status: blocked ? "blocked" : "projected",
      runtime_posture: blocked ? "blocked" : observed ? "observed" : "deferred",
      confidence: { evidence_confidence: "medium", commitment_confidence: blocked ? "blocked" : "deferred" },
      properties: {
        producer: stripInline(producer),
        typed_boundary: stripInline(boundary),
        consumer: stripInline(consumer),
        owner_boundary: stripInline(ownerBoundary),
        fail_closed_condition: stripInline(failClosed),
        evidence_status: stripInline(evidenceStatus)
      },
      residue_refs: stageResidues[stageSlug] ?? ["rwo:residue.028", "rwo:residue.029"],
      forbidden_inferences: ["A documented integration stage does not select its unresolved owner, accept its schema, or prove executable compatibility."]
    });
  }

  for (const gate of gates) {
    addNode({
      node_id: `rwo:gate:${gate.id}`,
      label: gate.label,
      node_kind: "owner-gate",
      branch: "bridge",
      description: gate.question,
      source_refs: [sourceNodeId("E3"), sourceNodeId("C1")],
      owner_route: gate.owner,
      candidate_status: gate.selection === "blocked" ? "blocked" : "deferred",
      runtime_posture: gate.selection === "blocked" ? "blocked" : "deferred",
      confidence: { evidence_confidence: "medium", commitment_confidence: gate.selection === "blocked" ? "blocked" : "deferred" },
      properties: { selection_status: gate.selection, blocking_question: gate.question },
      residue_refs: gate.residues,
      forbidden_inferences: ["An ontology gate node cannot select, impersonate, or authorize the named owner."]
    });
  }

  for (let index = 0; index < stageIds.length - 1; index += 1) {
    addRelation({
      predicate: "precedes",
      relation_kind: "integration",
      source_node: stageIds[index],
      target_node: stageIds[index + 1],
      owner_route: "cross-owner integration contract",
      evidence_refs: [sourceNodeId("E3"), sourceNodeId("C1")],
      runtime_posture: "deferred",
      properties: { documentation_only: true },
      description: `${stageIds[index]} must complete its own gate before ${stageIds[index + 1]} may be considered.`,
      forbidden_inferences: ["Precedence does not transfer a pass, authority, acceptance, or effect permission to the next stage."]
    });
  }

  for (const stageId of stageIds) {
    const stageSlug = stageId.replace("rwo:stage:", "");
    for (const gateId of stageGateMap[stageSlug] ?? []) {
      addRelation({
        predicate: "requires-owner-gate",
        relation_kind: "governance",
        source_node: stageId,
        target_node: `rwo:gate:${gateId}`,
        owner_route: gates.find((gate) => gate.id === gateId).owner,
        evidence_refs: [sourceNodeId("E3"), sourceNodeId("C1")],
        runtime_posture: "blocked",
        properties: { owner_selection_effect: "none" },
        description: `${stageId} depends on a separately owned gate boundary.`,
        forbidden_inferences: ["The relation does not select the owner or treat a proposed gate as a recorded verdict."]
      });
    }
    for (const residueRef of stageResidues[stageSlug] ?? []) {
      addRelation({
        predicate: "blocked-by",
        relation_kind: "governance",
        source_node: stageId,
        target_node: residueRef,
        owner_route: residueOwners[residueRef.slice(-3)],
        evidence_refs: [sourceNodeId("C1")],
        runtime_posture: "blocked",
        properties: {},
        description: `${stageId} remains non-executable while ${residueRef} is open.`,
        forbidden_inferences: ["The graph cannot close cross-owner residue by adjacency or naming similarity."]
      });
    }
  }

  const witnessRows = tableRows(section(bridge, "## Planned discriminating witnesses", "## Validation posture"))
    .filter((row) => /^`F[1-8]`$/.test(row[0]));
  for (const [idCell, discriminationCell, statusCell] of witnessRows) {
    const witnessId = stripInline(idCell);
    const node_id = `rwo:witness:${witnessId.toLowerCase()}`;
    addNode({
      node_id,
      label: witnessId,
      node_kind: "validation-witness",
      branch: "bridge",
      description: stripInline(discriminationCell),
      source_refs: [sourceNodeId("C1")],
      owner_route: "validation and evidence owner",
      candidate_status: "deferred",
      runtime_posture: "absent",
      confidence: { evidence_confidence: "high", commitment_confidence: "deferred" },
      properties: { required_discrimination: stripInline(discriminationCell), current_status: stripInline(statusCell) },
      residue_refs: ["rwo:residue.029"],
      forbidden_inferences: ["A planned witness is not an executed test, conformance receipt, or passing result."]
    });
    addRelation({
      predicate: "requires-witness",
      relation_kind: "validation",
      source_node: witnessTarget[witnessId],
      target_node: node_id,
      owner_route: "validation and evidence owner",
      evidence_refs: [sourceNodeId("C1")],
      runtime_posture: "absent",
      properties: { current_status: "unexecuted" },
      description: `${witnessTarget[witnessId]} requires ${witnessId} before the associated conformance claim may advance.`,
      forbidden_inferences: ["Requiring a witness does not execute or satisfy it."]
    });
  }

  for (const topology of evidence.bridge_summary.killed) {
    const node_id = `rwo:forbidden:${slug(topology)}`;
    addNode({
      node_id,
      label: topology,
      node_kind: "forbidden-topology",
      branch: "bridge",
      description: `Killed integration topology: ${topology}.`,
      source_refs: [sourceNodeId("K1")],
      owner_route: "ACI and exact-effect authority owners",
      candidate_status: "killed",
      runtime_posture: "not-applicable",
      confidence: { evidence_confidence: "high", commitment_confidence: "killed" },
      properties: { disposition: "killed" },
      residue_refs: [],
      forbidden_inferences: ["A killed topology must not be reintroduced by naming it as a convenience adapter or projection.", "The ontology record alone is not runtime enforcement."]
    });
    addRelation({
      predicate: "prohibits",
      relation_kind: "prohibition",
      source_node: sourceNodeId("K1"),
      target_node: node_id,
      owner_route: "ACI and exact-effect authority owners",
      evidence_refs: [sourceNodeId("K1")],
      runtime_posture: "not-applicable",
      cycle_policy: "not-applicable",
      properties: { disposition: "killed" },
      description: `K1 records ${topology} as a forbidden integration topology.`,
      forbidden_inferences: ["A prohibition node is not evidence that every implementation path enforces the constraint."]
    });
  }

  const nodesDocument = {
    schema: "../schemas/node.schema.json",
    package_id: "rwo.current-state-graph@0.1.0",
    ontology_ref: evidence.ontology_ref,
    generated_from: [
      "../ONTOLOGY.md",
      "../evidence/CURRENT-STATE-2026-08-05.json",
      "cyberAlchemy-v2:development/agent-reasoning-engine/design/rwo-integration/ONTOLOGY-BRIDGE.md"
    ],
    authority_effect: "none",
    nodes
  };
  const relationsDocument = {
    schema: "../schemas/relation.schema.json",
    package_id: "rwo.current-state-graph@0.1.0",
    ontology_ref: evidence.ontology_ref,
    authority_effect: "none",
    relations
  };

  const nodeGroups = [...new Set(nodes.map((node) => node.node_kind))].map((kind) => ({
    group_id: slug(kind),
    label: kind,
    node_refs: nodes.filter((node) => node.node_kind === kind).map((node) => node.node_id)
  }));
  const viewDocument = {
    view_id: "rwo:view:current-state",
    view_role: "bridge",
    title: "Recursive Work Orchestrator current state and ARE boundary",
    description: "Queryable candidate view from accepted implementation evidence through property findings and residue to the documentation-only RWO-to-ARE boundary.",
    owner_route: "RWO ontology source owner plus named cross-owner gates",
    source_refs: evidence.sources.map((source) => sourceNodeId(source.id)),
    node_refs: nodes.map((node) => node.node_id),
    relation_refs: relations.map((relation) => relation.relation_id),
    groups: nodeGroups,
    sequences: [
      {
        sequence_id: "RWO-EVIDENCE-FINDING-CONCEPT",
        label: "Executed protocol evidence to bounded architecture finding",
        steps: [sourceNodeId("E1"), "rwo:finding.current.protocol", "rwo:precedent:aci-command-event-lanes", "rwo:WorkProtocol"]
      },
      {
        sequence_id: "RWO-ARE-DOCUMENTATION-BOUNDARY",
        label: "Conditional RWO-to-ARE stage sequence",
        steps: stageIds
      },
      {
        sequence_id: "RWO-OPEN-GRAPH-WITNESS",
        label: "Graph realization gap and required witness",
        steps: ["rwo:WorkGraph", "rwo:witness:f2", "rwo:residue.029"]
      }
    ],
    allowed_readings: [
      "Implementation precedents can be queried separately from the RWO elements they partially resemble.",
      "Proof status, correspondence, and finding status are orthogonal and remain explicit on finding relations.",
      "The ARE path is a documentation-only sequence whose owner gates and witnesses are independently addressable.",
      "Open residue and killed topologies remain visible rather than being smoothed into an implementation recommendation."
    ],
    forbidden_authority_moves: [
      "No node or relation promotes RWO, ARE, ACI, vocabulary, schemas, or owners.",
      "No observed precedent may be rendered as direct RWO realization.",
      "No stage adjacency transfers gate permission or authorizes an effect.",
      "No unexecuted witness may be displayed as passing validation."
    ],
    residue_refs: residueRows.map((row) => stripInline(row[0])),
    authority_effect: "none"
  };

  return { nodesDocument, relationsDocument, viewDocument };
};

export const writeGraph = async () => {
  const { nodesDocument, relationsDocument, viewDocument } = await buildGraph();
  await Promise.all([
    mkdir(path.dirname(FILES.nodes), { recursive: true }),
    mkdir(path.dirname(FILES.relations), { recursive: true }),
    mkdir(path.dirname(FILES.view), { recursive: true })
  ]);
  await Promise.all([
    writeFile(FILES.nodes, serialize(nodesDocument)),
    writeFile(FILES.relations, serialize(relationsDocument)),
    writeFile(FILES.view, serialize(viewDocument))
  ]);
  return {
    nodes: nodesDocument.nodes.length,
    relations: relationsDocument.relations.length,
    groups: viewDocument.groups.length,
    sequences: viewDocument.sequences.length
  };
};

const invokedDirectly = process.argv[1]
  && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;
if (invokedDirectly) {
  console.log(JSON.stringify(await writeGraph()));
}
