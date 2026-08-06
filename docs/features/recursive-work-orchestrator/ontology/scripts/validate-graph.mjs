import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildGraph } from "./build-graph.mjs";

const ONTOLOGY_ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const TARGET_ROOT = path.resolve(ONTOLOGY_ROOT, "../../../..");
const UMBRELLA_ROOT = path.resolve(TARGET_ROOT, "../..");
const FILES = {
  ontology: "ONTOLOGY.md",
  evidence: "evidence/CURRENT-STATE-2026-08-05.json",
  nodes: "nodes/nodes.json",
  relations: "relations/relations.json",
  view: "views/current-state.json",
  nodeSchema: "schemas/node.schema.json",
  relationSchema: "schemas/relation.schema.json",
  viewSchema: "schemas/view.schema.json",
  invalidAuthority: "fixtures/invalid-authority-effect.json",
  invalidEndpoint: "fixtures/invalid-endpoint.json"
};

const readJson = async (relativePath) => JSON.parse(await readFile(path.join(ONTOLOGY_ROOT, relativePath), "utf8"));
const serialize = (value) => `${JSON.stringify(value, null, 2)}\n`;
const unique = (values) => values.length === new Set(values).size;
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const push = (errors, at, message) => errors.push(`${at}: ${message}`);

const validateClosedSchema = (value, schema, at, errors) => {
  if (schema.const !== undefined && value !== schema.const) {
    push(errors, at, `must equal ${JSON.stringify(schema.const)}`);
    return;
  }
  if (schema.enum && !schema.enum.includes(value)) {
    push(errors, at, `must be one of ${schema.enum.join(", ")}`);
    return;
  }
  if (schema.type === "object") {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      push(errors, at, "must be an object");
      return;
    }
    for (const key of schema.required ?? []) {
      if (!(key in value)) push(errors, `${at}.${key}`, "is required");
    }
    if (schema.additionalProperties === false) {
      const allowed = new Set(Object.keys(schema.properties ?? {}));
      for (const key of Object.keys(value)) {
        if (!allowed.has(key)) push(errors, `${at}.${key}`, "is not allowed");
      }
    }
    for (const [key, propertySchema] of Object.entries(schema.properties ?? {})) {
      if (key in value) validateClosedSchema(value[key], propertySchema, `${at}.${key}`, errors);
    }
    return;
  }
  if (schema.type === "array") {
    if (!Array.isArray(value)) {
      push(errors, at, "must be an array");
      return;
    }
    if (schema.minItems !== undefined && value.length < schema.minItems) {
      push(errors, at, `must contain at least ${schema.minItems} item(s)`);
    }
    if (schema.uniqueItems && !unique(value.map((item) => JSON.stringify(item)))) {
      push(errors, at, "must contain unique items");
    }
    if (schema.items) {
      value.forEach((item, index) => validateClosedSchema(item, schema.items, `${at}[${index}]`, errors));
    }
    return;
  }
  if (schema.type === "string") {
    if (typeof value !== "string") {
      push(errors, at, "must be a string");
      return;
    }
    if (schema.minLength !== undefined && value.length < schema.minLength) {
      push(errors, at, `must have length >= ${schema.minLength}`);
    }
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) {
      push(errors, at, `must match ${schema.pattern}`);
    }
  }
};

const validateEndpoint = (relation, nodeIds, errors, at) => {
  if (!nodeIds.has(relation.source_node)) push(errors, `${at}.source_node`, `unknown ${relation.source_node}`);
  if (!nodeIds.has(relation.target_node)) push(errors, `${at}.target_node`, `unknown ${relation.target_node}`);
};

const validateSourceHashes = async (errors) => {
  const checks = [
    {
      at: "sources.rwo-design",
      path: path.join(TARGET_ROOT, "docs/features/recursive-work-orchestrator/DESIGN.md"),
      expected: "28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419"
    },
    {
      at: "sources.are-architecture",
      path: path.join(UMBRELLA_ROOT, "cyberAlchemy-v2/development/agent-reasoning-engine/design/ARCHITECTURE.md"),
      expected: "1958758a104c19af9966fd1460097c18fbf919e480da45e5c8dcc0b5f4ffe0de"
    },
    {
      at: "sources.aci-binding",
      path: path.join(UMBRELLA_ROOT, "cyberAlchemy-v2/development/agent-reasoning-engine/design/aci-reasoning-binding/ARCHITECTURE.md"),
      expected: "02eaede41676bcf19e45cb8cf9b7130bddf297d6ae786d81fdb67ee456bb2c8c"
    },
    {
      at: "sources.accepted-findings",
      path: path.join(UMBRELLA_ROOT, "ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/findings.md"),
      expected: "734a3122359f8cefd0c13fee36b6b2caabf5d158693b588a3678f138bd1941c1"
    },
    {
      at: "sources.evidence-closure",
      path: path.join(UMBRELLA_ROOT, "ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/receipts/evidence-closure.json"),
      expected: "cfe590f7bf0e3cbde75a38e15fcc93f9954ae23a0dce7ca5b45913dfac07c73f"
    },
    {
      at: "sources.final-audit",
      path: path.join(UMBRELLA_ROOT, "ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/audit-final.md"),
      expected: "bcf7b4d97eea7e126454bc84e1946dac7518dca7bfa51ac8b6652e7b347a1050"
    }
  ];
  for (const check of checks) {
    const actual = sha256(await readFile(check.path));
    if (actual !== check.expected) push(errors, check.at, `hash mismatch: ${actual}`);
  }
};

export const validateGraph = async () => {
  const errors = [];
  const [nodesDocument, relationsDocument, view, nodeSchema, relationSchema, viewSchema, evidence, invalidAuthority, invalidEndpoint] = await Promise.all([
    readJson(FILES.nodes),
    readJson(FILES.relations),
    readJson(FILES.view),
    readJson(FILES.nodeSchema),
    readJson(FILES.relationSchema),
    readJson(FILES.viewSchema),
    readJson(FILES.evidence),
    readJson(FILES.invalidAuthority),
    readJson(FILES.invalidEndpoint)
  ]);

  const built = await buildGraph();
  if (serialize(nodesDocument) !== serialize(built.nodesDocument)) push(errors, "nodes", "generated output is stale");
  if (serialize(relationsDocument) !== serialize(built.relationsDocument)) push(errors, "relations", "generated output is stale");
  if (serialize(view) !== serialize(built.viewDocument)) push(errors, "view", "generated output is stale");

  for (const [documentName, document] of [["nodes", nodesDocument], ["relations", relationsDocument]]) {
    if (document.package_id !== "rwo.current-state-graph@0.1.0") push(errors, `${documentName}.package_id`, "unexpected package ID");
    if (document.ontology_ref !== evidence.ontology_ref) push(errors, `${documentName}.ontology_ref`, "must match evidence ontology_ref");
    if (document.authority_effect !== "none") push(errors, `${documentName}.authority_effect`, "must remain none");
  }

  const nodeIds = nodesDocument.nodes.map((node) => node.node_id);
  if (!unique(nodeIds)) push(errors, "nodes", "node_id values must be unique");
  const nodeIdSet = new Set(nodeIds);
  const sourceNodeSet = new Set(nodesDocument.nodes.filter((node) => node.node_kind === "evidence-source").map((node) => node.node_id));
  const residueNodeSet = new Set(nodesDocument.nodes.filter((node) => node.node_kind === "residue").map((node) => node.node_id));
  nodesDocument.nodes.forEach((node, index) => {
    validateClosedSchema(node, nodeSchema, `nodes[${index}]`, errors);
    for (const sourceRef of node.source_refs ?? []) {
      if (!sourceNodeSet.has(sourceRef)) push(errors, `nodes[${index}].source_refs`, `unknown evidence node ${sourceRef}`);
    }
    for (const residueRef of node.residue_refs ?? []) {
      if (!residueNodeSet.has(residueRef)) push(errors, `nodes[${index}].residue_refs`, `unknown residue node ${residueRef}`);
    }
  });

  const relationIds = relationsDocument.relations.map((relation) => relation.relation_id);
  if (!unique(relationIds)) push(errors, "relations", "relation_id values must be unique");
  const relationIdSet = new Set(relationIds);
  relationsDocument.relations.forEach((relation, index) => {
    validateClosedSchema(relation, relationSchema, `relations[${index}]`, errors);
    validateEndpoint(relation, nodeIdSet, errors, `relations[${index}]`);
    for (const evidenceRef of relation.evidence_refs ?? []) {
      if (!sourceNodeSet.has(evidenceRef)) push(errors, `relations[${index}].evidence_refs`, `unknown evidence node ${evidenceRef}`);
    }
    if (relation.properties?.correspondence === "direct-realization") {
      push(errors, `relations[${index}].properties.correspondence`, "direct realization exceeds accepted evidence");
    }
  });

  validateClosedSchema(view, viewSchema, "view", errors);
  for (const sourceRef of view.source_refs ?? []) {
    if (!sourceNodeSet.has(sourceRef)) push(errors, "view.source_refs", `unknown evidence node ${sourceRef}`);
  }
  for (const nodeRef of view.node_refs ?? []) {
    if (!nodeIdSet.has(nodeRef)) push(errors, "view.node_refs", `unknown ${nodeRef}`);
  }
  for (const relationRef of view.relation_refs ?? []) {
    if (!relationIdSet.has(relationRef)) push(errors, "view.relation_refs", `unknown ${relationRef}`);
  }
  for (const [index, group] of (view.groups ?? []).entries()) {
    for (const nodeRef of group.node_refs ?? []) {
      if (!nodeIdSet.has(nodeRef)) push(errors, `view.groups[${index}]`, `unknown ${nodeRef}`);
    }
  }
  for (const [index, sequence] of (view.sequences ?? []).entries()) {
    for (const nodeRef of sequence.steps ?? []) {
      if (!nodeIdSet.has(nodeRef)) push(errors, `view.sequences[${index}]`, `unknown ${nodeRef}`);
    }
  }
  if (new Set(view.node_refs).size !== nodeIdSet.size) push(errors, "view.node_refs", "current-state view must cover every node exactly once");
  if (new Set(view.relation_refs).size !== relationIdSet.size) push(errors, "view.relation_refs", "current-state view must cover every relation exactly once");

  const findingIds = new Set(evidence.findings.map((finding) => finding.finding_id));
  const findingNodeIds = new Set(nodesDocument.nodes.filter((node) => node.node_kind === "property-finding").map((node) => node.node_id));
  if (findingIds.size !== findingNodeIds.size || [...findingIds].some((id) => !findingNodeIds.has(id))) {
    push(errors, "findings", "every accepted finding must be materialized exactly once");
  }
  for (const finding of evidence.findings) {
    const evaluates = relationsDocument.relations.filter((relation) => relation.source_node === finding.finding_id && relation.predicate === "evaluates");
    if (evaluates.length !== 1 || evaluates[0].target_node !== finding.subject_ref) {
      push(errors, finding.finding_id, "must have exactly one evaluates relation to its subject");
    }
    const supports = relationsDocument.relations.filter((relation) => relation.target_node === finding.finding_id && relation.predicate === "supports");
    if (supports.length === 0) push(errors, finding.finding_id, "must have at least one evidence support relation");
  }

  for (const source of evidence.sources) {
    const expectedId = `rwo:source:${source.id.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;
    if (!sourceNodeSet.has(expectedId)) push(errors, "sources", `missing evidence node ${expectedId}`);
  }
  const requiredKinds = new Map([
    ["architecture-element", 41],
    ["implementation-precedent", 13],
    ["evidence-source", 6],
    ["property-finding", 16],
    ["hypothesis", 1],
    ["residue", 29],
    ["integration-stage", 10],
    ["owner-gate", 7],
    ["validation-witness", 8],
    ["forbidden-topology", 6]
  ]);
  for (const [kind, expected] of requiredKinds) {
    const actual = nodesDocument.nodes.filter((node) => node.node_kind === kind).length;
    if (actual !== expected) push(errors, `node-kind.${kind}`, `expected ${expected}, got ${actual}`);
  }
  if ([...residueNodeSet].some((id) => !/^rwo:residue\.[0-9]{3}$/.test(id))) push(errors, "residue", "invalid residue ID");
  for (let index = 1; index <= 29; index += 1) {
    const id = `rwo:residue.${String(index).padStart(3, "0")}`;
    if (!residueNodeSet.has(id)) push(errors, "residue", `missing ${id}`);
  }
  for (let index = 1; index <= 8; index += 1) {
    const id = `rwo:witness:f${index}`;
    const node = nodesDocument.nodes.find((candidate) => candidate.node_id === id);
    if (!node || node.runtime_posture !== "absent" || node.properties.current_status !== "unexecuted") {
      push(errors, "witnesses", `${id} must exist and remain unexecuted`);
    }
  }

  const invalidAuthorityErrors = [];
  validateClosedSchema(invalidAuthority, relationSchema, "fixture.invalid-authority", invalidAuthorityErrors);
  if (invalidAuthorityErrors.length === 0) push(errors, "fixtures.invalid-authority", "negative fixture unexpectedly passed");
  const invalidEndpointErrors = [];
  validateClosedSchema(invalidEndpoint, relationSchema, "fixture.invalid-endpoint", invalidEndpointErrors);
  validateEndpoint(invalidEndpoint, nodeIdSet, invalidEndpointErrors, "fixture.invalid-endpoint");
  if (invalidEndpointErrors.length === 0) push(errors, "fixtures.invalid-endpoint", "negative fixture unexpectedly passed");

  await validateSourceHashes(errors);
  const result = {
    status: errors.length === 0 ? "pass" : "fail",
    package_id: nodesDocument.package_id,
    ontology_ref: evidence.ontology_ref,
    nodes: nodesDocument.nodes.length,
    relations: relationsDocument.relations.length,
    views: 1,
    groups: view.groups.length,
    source_nodes: sourceNodeSet.size,
    finding_nodes: findingNodeIds.size,
    residue_nodes: residueNodeSet.size,
    direct_realization_relations: relationsDocument.relations.filter((relation) => relation.properties?.correspondence === "direct-realization").length,
    negative_fixtures: 2,
    source_hash_checks: 6,
    errors
  };
  return result;
};

const result = await validateGraph();
console.log(JSON.stringify(result, null, 2));
if (result.status !== "pass") process.exitCode = 1;
