#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(scriptDir, "..");

const paths = {
  ontology: resolve(packageRoot, "ontology.json"),
  ontologySchema: resolve(packageRoot, "schemas/ontology.schema.json"),
  view: resolve(packageRoot, "views/typed-coordinated-work-atlas.json"),
  viewSchema: resolve(packageRoot, "schemas/view.schema.json"),
  example: resolve(packageRoot, "examples/all-operators.pipeline.json"),
  exampleSchema: resolve(packageRoot, "schemas/pipeline-instance.schema.json"),
};

const failures = [];
const checks = [];

function check(condition, message) {
  if (!condition) failures.push(message);
}

function pass(name, detail) {
  checks.push({ name, status: "pass", detail });
}

async function readJson(path) {
  const bytes = await readFile(path);
  return { bytes, value: JSON.parse(bytes.toString("utf8")) };
}

function digest(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function uniqueBy(items, key, catalog) {
  const seen = new Set();
  for (const item of items) {
    check(item && typeof item[key] === "string", `${catalog} contains an item without string ${key}`);
    if (!item || typeof item[key] !== "string") continue;
    check(!seen.has(item[key]), `${catalog} contains duplicate ${key} ${item[key]}`);
    seen.add(item[key]);
  }
  return seen;
}

function collectSourceRefs(value, refs = []) {
  if (typeof value === "string") {
    if (/^source:[a-z0-9._-]+#[a-z0-9._-]+$/.test(value)) refs.push(value);
    return refs;
  }
  if (Array.isArray(value)) {
    for (const item of value) collectSourceRefs(item, refs);
    return refs;
  }
  if (value && typeof value === "object") {
    for (const item of Object.values(value)) collectSourceRefs(item, refs);
  }
  return refs;
}

function slugifyHeading(text) {
  return text
    .replace(/<[^>]*>/g, "")
    .replace(/[`*_~]/g, "")
    .toLocaleLowerCase("en")
    .normalize("NFKD")
    .replace(/[^\p{Letter}\p{Number}\s-]/gu, "")
    .trim()
    .replace(/[\s-]+/g, "-");
}

function markdownAnchors(text) {
  const anchors = new Set();
  const duplicateCounts = new Map();
  for (const line of text.split(/\r?\n/)) {
    const match = /^(#{1,6})\s+(.+?)\s*#*\s*$/.exec(line);
    if (!match) continue;
    const base = slugifyHeading(match[2]);
    const count = duplicateCounts.get(base) ?? 0;
    duplicateCounts.set(base, count + 1);
    anchors.add(count === 0 ? base : `${base}-${count}`);
  }
  return anchors;
}

function hasAncestor(typeId, ancestorId, typeMap) {
  let current = typeMap.get(typeId);
  const visited = new Set();
  while (current) {
    if (current.id === ancestorId) return true;
    if (!current.parent || visited.has(current.parent)) return false;
    visited.add(current.parent);
    current = typeMap.get(current.parent);
  }
  return false;
}

function findDirectedCycles(nodes, edges) {
  const adjacency = new Map(nodes.map((node) => [node.id, []]));
  for (const edge of edges) adjacency.get(edge.from)?.push(edge.to);
  const cycles = [];
  const active = [];
  const activeSet = new Set();
  const complete = new Set();

  function visit(node) {
    if (activeSet.has(node)) {
      const start = active.indexOf(node);
      cycles.push(new Set(active.slice(start)));
      return;
    }
    if (complete.has(node)) return;
    active.push(node);
    activeSet.add(node);
    for (const target of adjacency.get(node) ?? []) visit(target);
    active.pop();
    activeSet.delete(node);
    complete.add(node);
  }

  for (const node of adjacency.keys()) visit(node);
  return cycles;
}

const [ontologyDoc, ontologySchemaDoc, viewDoc, viewSchemaDoc, exampleDoc, exampleSchemaDoc] =
  await Promise.all([
    readJson(paths.ontology),
    readJson(paths.ontologySchema),
    readJson(paths.view),
    readJson(paths.viewSchema),
    readJson(paths.example),
    readJson(paths.exampleSchema),
  ]);

const ontology = ontologyDoc.value;
const view = viewDoc.value;
const example = exampleDoc.value;

check(ontologySchemaDoc.value.$schema === "https://json-schema.org/draft/2020-12/schema", "ontology schema is not JSON Schema 2020-12");
check(viewSchemaDoc.value.$schema === "https://json-schema.org/draft/2020-12/schema", "view schema is not JSON Schema 2020-12");
check(exampleSchemaDoc.value.$schema === "https://json-schema.org/draft/2020-12/schema", "example schema is not JSON Schema 2020-12");
check(ontology.schema_version === "rwo-architecture-property-ontology/v1", "unexpected ontology schema_version");
check(view.schema_version === "rwo-view-projection/v1", "unexpected view schema_version");
check(example.schema_version === "rwo-illustrative-pipeline/v1", "unexpected example schema_version");
check(ontology.ontology?.ontology_type === "architecture-property", "ontology_type must be architecture-property");
check(ontology.ontology?.selection_source === "inferred", "selection_source must preserve inferred routing evidence");
check(ontology.ontology?.selection_confidence === "high", "selection_confidence must be high");
check(ontology.ontology?.branch === "system", "architecture-property must derive the system branch here");
check(ontology.ontology?.authority_effect === "none", "ontology authority_effect must be none");
check(ontology.ontology?.runtime_conformance === "unsupported", "runtime conformance must remain unsupported");
check(ontology.ontology?.promotion_status === "not-granted", "promotion status must remain not-granted");
pass("routing-and-claim-ceiling", "architecture-property/system, inferred-high, proposal-only, no authority or runtime effect");

const sourceIds = uniqueBy(ontology.sources, "id", "sources");
const sourceMap = new Map(ontology.sources.map((source) => [source.id, source]));
for (const sourceId of ontology.source_precedence) {
  check(sourceIds.has(sourceId), `source_precedence refers to unknown ${sourceId}`);
}

const sourceAnchors = new Map();
const sourceDigestResults = [];
for (const source of ontology.sources) {
  const sourcePath = resolve(packageRoot, source.path);
  try {
    const bytes = await readFile(sourcePath);
    const observedDigest = digest(bytes);
    check(observedDigest === source.sha256, `source digest mismatch for ${source.id}: expected ${source.sha256}, observed ${observedDigest}`);
    sourceDigestResults.push({ id: source.id, sha256: observedDigest });
    if (source.path.endsWith(".md")) sourceAnchors.set(source.id, markdownAnchors(bytes.toString("utf8")));
  } catch (error) {
    failures.push(`cannot read source ${source.id} at ${source.path}: ${error.message}`);
  }
}

const allSourceRefs = [
  ...collectSourceRefs(ontology),
  ...collectSourceRefs(view),
  ...collectSourceRefs(example),
];
for (const ref of allSourceRefs) {
  const hashIndex = ref.indexOf("#");
  const sourceId = ref.slice(0, hashIndex);
  const selector = ref.slice(hashIndex + 1);
  check(sourceMap.has(sourceId), `source ref ${ref} names an unknown source`);
  const anchors = sourceAnchors.get(sourceId);
  if (anchors) check(anchors.has(selector), `source ref ${ref} names a missing Markdown heading`);
}
pass("source-traceability", `${sourceDigestResults.length} pinned sources and ${allSourceRefs.length} source selectors checked`);

const ownerIds = uniqueBy(ontology.owner_routes, "id", "owner_routes");
const ownerMap = new Map(ontology.owner_routes.map((owner) => [owner.id, owner]));
const typeIds = uniqueBy(ontology.element_types, "id", "element_types");
const typeMap = new Map(ontology.element_types.map((type) => [type.id, type]));
const propertyIds = uniqueBy(ontology.properties, "id", "properties");
const relationIds = uniqueBy(ontology.relations, "id", "relations");
const shieldIds = uniqueBy(ontology.shields, "id", "shields");
const operatorIds = uniqueBy(ontology.constraint_operators, "id", "constraint_operators");
const constraintIds = uniqueBy(ontology.constraints, "id", "constraints");
const profileIds = uniqueBy(ontology.profiles, "id", "profiles");
const projectionIds = uniqueBy(ontology.observation_projections, "id", "observation_projections");
const premiseIds = uniqueBy(ontology.premises, "id", "premises");
const residueIds = uniqueBy(ontology.residue, "id", "residue");

for (const type of ontology.element_types) {
  if (type.parent) check(typeIds.has(type.parent), `${type.id} has unknown parent ${type.parent}`);
  const lineage = new Set([type.id]);
  let parent = type.parent;
  while (parent) {
    check(!lineage.has(parent), `type hierarchy cycle at ${type.id} through ${parent}`);
    if (lineage.has(parent)) break;
    lineage.add(parent);
    parent = typeMap.get(parent)?.parent;
  }
}

for (const property of ontology.properties) {
  for (const subject of property.subjects) check(typeIds.has(subject), `${property.id} has unknown subject ${subject}`);
  for (const target of property.value_domain?.target_types ?? []) check(typeIds.has(target), `${property.id} has unknown value target ${target}`);
  check(ownerIds.has(property.owner_route), `${property.id} has unknown owner route ${property.owner_route}`);
  check(typeof property.forbidden_inference === "string" && property.forbidden_inference.length > 0, `${property.id} lacks a forbidden inference`);
}

for (const relation of ontology.relations) {
  for (const sourceType of relation.source_types) check(typeIds.has(sourceType), `${relation.id} has unknown source type ${sourceType}`);
  for (const targetType of relation.target_types) check(typeIds.has(targetType), `${relation.id} has unknown target type ${targetType}`);
  check(ownerIds.has(relation.owner_route), `${relation.id} has unknown owner route ${relation.owner_route}`);
  if (relation.transitive) check(relation.id === "rwo:r.specializes", `${relation.id} is transitive but only specializes may be transitive in v0.1.0`);
}

for (const owner of ontology.owner_routes) {
  if (owner.residue_ref) check(residueIds.has(owner.residue_ref), `${owner.id} names unknown residue ${owner.residue_ref}`);
}
check(typeIds.has("rwo:LeafBinding"), "formal endpoint type rwo:LeafBinding is missing");
check(typeIds.has("rwo:PropertyConstraint"), "formal endpoint type rwo:PropertyConstraint is missing");
check(typeIds.has("rwo:RelationConstraint"), "formal endpoint type rwo:RelationConstraint is missing");
check(typeIds.has("rwo:EvidenceReference"), "formal endpoint type rwo:EvidenceReference is missing");
check(relationIds.has("rwo:r.has-contract"), "uniform contract relation rwo:r.has-contract is missing");
pass("ontology-catalogs", `${typeIds.size} types, ${propertyIds.size} properties, ${relationIds.size} relations, and ${shieldIds.size} shields are reference-closed`);

const expectedConstraints = Array.from({ length: 12 }, (_, index) => `RWO-I${String(index + 1).padStart(2, "0")}`);
for (const expected of expectedConstraints) check(constraintIds.has(expected), `missing required constraint ${expected}`);
for (const constraint of ontology.constraints) {
  check(operatorIds.has(constraint.operator_ref), `${constraint.id} has unknown operator ${constraint.operator_ref}`);
  for (const subject of constraint.subjects) check(typeIds.has(subject), `${constraint.id} has unknown subject ${subject}`);
  for (const relation of constraint.relation_refs ?? []) check(relationIds.has(relation), `${constraint.id} has unknown relation ${relation}`);
  for (const property of constraint.property_refs ?? []) check(propertyIds.has(property), `${constraint.id} has unknown property ${property}`);
  for (const shield of constraint.shield_refs ?? []) check(shieldIds.has(shield), `${constraint.id} has unknown shield ${shield}`);
  check(ownerIds.has(constraint.owner_route), `${constraint.id} has unknown owner route ${constraint.owner_route}`);
}
for (const profile of ontology.profiles) {
  for (const constraint of profile.constraint_refs) check(constraintIds.has(constraint), `${profile.id} has unknown constraint ${constraint}`);
  check(profile.current_evidence_status !== "pass", `${profile.id} must not claim a pass without findings and evidence`);
}
const coreProfile = ontology.profiles.find((profile) => profile.id === "rwo:profile.core-v0");
check(coreProfile, "core profile is missing");
if (coreProfile) check(expectedConstraints.every((id) => coreProfile.constraint_refs.includes(id)), "core profile does not cover all RWO-I01 through RWO-I12");
for (const projection of ontology.observation_projections) check(ownerIds.has(projection.owner_route), `${projection.id} has unknown owner route ${projection.owner_route}`);
check(ontology.finding_contract.type_ref === "rwo:PropertyFinding", "finding contract must use rwo:PropertyFinding");
check(ontology.finding_contract.absence_rule.toLowerCase().includes("never pass"), "finding absence rule must forbid pass from missing evidence");
check(profileIds.size === 3, `expected three profiles, found ${profileIds.size}`);
check(projectionIds.size === 8, `expected eight observation projections, found ${projectionIds.size}`);
pass("profiles-and-findings", `${operatorIds.size} operators, ${constraintIds.size} constraints, ${profileIds.size} profiles, and ${projectionIds.size} projections checked`);

for (const premise of ontology.premises) {
  check(["low", "medium", "high"].includes(premise.evidence_confidence), `${premise.id} has invalid evidence confidence`);
  check(["low", "medium", "high"].includes(premise.commitment_confidence), `${premise.id} has invalid commitment confidence`);
  check(typeof premise.falsification === "string" && premise.falsification.length > 0, `${premise.id} lacks falsification criteria`);
}
for (let index = 1; index <= 14; index += 1) {
  const requiredResidue = `rwo:residue.${String(index).padStart(3, "0")}`;
  check(residueIds.has(requiredResidue), `missing source residue ${requiredResidue}`);
}
for (const packageResidue of ["rwo:residue.015", "rwo:residue.016", "rwo:residue.017"]) {
  check(residueIds.has(packageResidue), `missing package drift residue ${packageResidue}`);
}
for (const residue of ontology.residue) {
  check(residue.status === "open", `${residue.id} was silently resolved`);
  check(ownerIds.has(residue.owner_route), `${residue.id} has unknown owner route ${residue.owner_route}`);
}
const promotionOwner = ownerMap.get("rwo:owner.ontology-promotion");
check(promotionOwner?.status === "unresolved", "ontology promotion owner must remain unresolved");
check(promotionOwner?.residue_ref === "rwo:residue.010", "ontology promotion owner must route to rwo:residue.010");
pass("confidence-and-residue", `${premiseIds.size} premises retain separate evidence/commitment confidence; 14 source questions and 3 package-drift records remain open`);

const viewLensIds = uniqueBy(view.lenses, "id", "view lenses");
const expectedLenses = ["rwo:lens.structure", "rwo:lens.flow", "rwo:lens.ownership-proof"];
for (const lensId of expectedLenses) check(viewLensIds.has(lensId), `view is missing ${lensId}`);
check(view.lenses.filter((lens) => lens.landing).length === 1, "view must have exactly one landing lens");
check(view.lenses.find((lens) => lens.landing)?.id === "rwo:lens.structure", "Structure must be the landing lens");
for (const lens of view.lenses) {
  for (const ref of lens.semantic_refs) check(typeIds.has(ref), `${lens.id} has unknown semantic ref ${ref}`);
  for (const ref of lens.relation_refs) check(relationIds.has(ref), `${lens.id} has unknown relation ref ${ref}`);
}
for (const ref of view.inspector.semantic_refs) check(typeIds.has(ref), `Inspector has unknown semantic ref ${ref}`);
for (const ref of view.inspector.shield_refs) check(shieldIds.has(ref), `Inspector has unknown shield ref ${ref}`);
let viewImplementationDigest = null;
try {
  const implementationBytes = await readFile(resolve(dirname(paths.view), view.view.implementation_ref));
  viewImplementationDigest = digest(implementationBytes);
  check(viewImplementationDigest === view.view.implementation_sha256, `view implementation digest mismatch: expected ${view.view.implementation_sha256}, observed ${viewImplementationDigest}`);
} catch (error) {
  failures.push(`cannot read view implementation ${view.view.implementation_ref}: ${error.message}`);
}
const negativeControlIds = uniqueBy(view.negative_controls, "id", "negative controls");
check(negativeControlIds.size >= 10, "view must preserve at least ten negative controls");
for (const control of view.negative_controls) {
  check(control.required_result === "KILL", `${control.id} does not fail closed`);
  for (const ref of control.shield_refs) check(shieldIds.has(ref), `${control.id} has unknown shield ref ${ref}`);
}
check(view.view.removable === true, "Atlas view must remain removable");
check(!ontologyDoc.bytes.toString("utf8").includes("rwo:view."), "core ontology depends on a removable view ID");
check(!ontologyDoc.bytes.toString("utf8").includes("rwo:lens."), "core ontology depends on a removable lens ID");
check(!ontologyDoc.bytes.toString("utf8").includes("rwo:nc."), "core ontology depends on a removable negative-control ID");
pass("removable-atlas-view", `${viewLensIds.size} synchronized lenses, ${negativeControlIds.size} fail-closed mutants, and one digest-pinned HTML candidate reference the core without core writeback`);

const definitionIds = uniqueBy(example.work_definitions, "work_ref", "example work definitions");
const definitionMap = new Map(example.work_definitions.map((definition) => [definition.work_ref, definition]));
const graphIds = uniqueBy(example.graphs, "id", "example graphs");
const graphMap = new Map(example.graphs.map((graph) => [graph.id, graph]));
check(definitionIds.has(example.root_orchestrator.invokes_work_ref), "root orchestrator invokes an unknown WorkDefinition");
check(definitionMap.get(example.root_orchestrator.invokes_work_ref)?.type === "rwo:CompositeWorkDefinition", "root orchestrator must invoke a composite pipeline definition");

for (const definition of example.work_definitions) {
  check(typeIds.has(definition.type), `${definition.work_ref} has unknown type ${definition.type}`);
  check(Array.isArray(definition.command_contract) && definition.command_contract.length > 0, `${definition.work_ref} lacks a command contract`);
  check(Array.isArray(definition.event_contract) && definition.event_contract.length > 0, `${definition.work_ref} lacks an event contract`);
  if (definition.type === "rwo:LeafWorkDefinition") {
    check(definition.body_kind === "leaf", `${definition.work_ref} leaf type/body mismatch`);
    check(!graphIds.has(definition.body_ref), `${definition.work_ref} leaf body points to a WorkGraph`);
  } else if (definition.type === "rwo:CompositeWorkDefinition") {
    check(definition.body_kind === "composite", `${definition.work_ref} composite type/body mismatch`);
    check(graphIds.has(definition.body_ref), `${definition.work_ref} composite body does not resolve to a WorkGraph`);
  }
}

const observedCompositionForms = new Set();
for (const graph of example.graphs) {
  const ownerDefinition = definitionMap.get(graph.owner_work_ref);
  check(ownerDefinition?.type === "rwo:CompositeWorkDefinition", `${graph.id} owner is not a CompositeWorkDefinition`);
  check(ownerDefinition?.body_ref === graph.id, `${graph.id} does not match its owner's body_ref`);
  const nodeIds = uniqueBy(graph.nodes, "id", `${graph.id} nodes`);
  const edgeIds = uniqueBy(graph.edges, "id", `${graph.id} edges`);
  for (const node of graph.nodes) {
    check(definitionIds.has(node.work_ref), `${graph.id}/${node.id} references unknown work ${node.work_ref}`);
    check(definitionMap.get(node.work_ref)?.type !== "rwo:OrchestratorKernel", `${graph.id}/${node.id} nests an OrchestratorKernel`);
  }
  for (const edge of graph.edges) {
    check(nodeIds.has(edge.from), `${graph.id}/${edge.id} has unknown source ${edge.from}`);
    check(nodeIds.has(edge.to), `${graph.id}/${edge.id} has unknown target ${edge.to}`);
    check(typeof edge.event_selector === "string" && edge.event_selector.length > 0, `${graph.id}/${edge.id} lacks an event selector`);
    check(typeof edge.input_mapping === "string" && edge.input_mapping.length > 0, `${graph.id}/${edge.id} lacks an input mapping`);
    check(typeIds.has(edge.composition_form), `${graph.id}/${edge.id} has unknown composition form ${edge.composition_form}`);
    check(hasAncestor(edge.composition_form, "rwo:CompositionForm", typeMap), `${graph.id}/${edge.id} composition form is not a CompositionForm subtype`);
    observedCompositionForms.add(edge.composition_form);
  }
  for (const form of graph.composition_forms) {
    check(typeIds.has(form), `${graph.id} declares unknown composition form ${form}`);
    check(hasAncestor(form, "rwo:CompositionForm", typeMap), `${graph.id} declares non-composition type ${form}`);
    observedCompositionForms.add(form);
  }
  const routesByNode = new Map();
  for (const edge of graph.edges.filter((candidate) => candidate.route_label)) {
    const labels = routesByNode.get(edge.from) ?? new Set();
    check(!labels.has(edge.route_label), `${graph.id}/${edge.from} has duplicate gate route ${edge.route_label}`);
    labels.add(edge.route_label);
    routesByNode.set(edge.from, labels);
  }
  for (const fanIn of graph.fan_in_policies) {
    check(nodeIds.has(fanIn.target_node), `${graph.id}/${fanIn.id} has unknown fan-in target ${fanIn.target_node}`);
    for (const source of fanIn.source_nodes) check(nodeIds.has(source), `${graph.id}/${fanIn.id} has unknown fan-in source ${source}`);
    check(JSON.stringify([...fanIn.source_nodes].sort()) === JSON.stringify([...fanIn.canonical_input_order].sort()), `${graph.id}/${fanIn.id} canonical input order is not total over fan-in sources`);
    const joinEdges = graph.edges.filter((edge) => edge.join_group === fanIn.id);
    check(joinEdges.length === fanIn.source_nodes.length, `${graph.id}/${fanIn.id} does not have one edge per fan-in source`);
  }
  for (const sidecar of graph.sidecars) {
    check(nodeIds.has(sidecar.node_ref), `${graph.id} has unknown sidecar node ${sidecar.node_ref}`);
    check(nodeIds.has(sidecar.primary_node_ref), `${graph.id} has unknown sidecar primary ${sidecar.primary_node_ref}`);
    check(sidecar.node_ref !== sidecar.primary_node_ref, `${graph.id} sidecar equals its primary`);
    for (const controlEdge of sidecar.control_edges) check(edgeIds.has(controlEdge), `${graph.id} sidecar has unknown control edge ${controlEdge}`);
  }
  const boundedCycleSets = graph.bounded_cycles.map((cycle) => new Set(cycle.node_refs));
  for (const cycle of graph.bounded_cycles) {
    check(cycle.max_rounds > 0, `${graph.id}/${cycle.id} has no positive bound`);
    check(nodeIds.has(cycle.decision_node), `${graph.id}/${cycle.id} has unknown decision node`);
    check(edgeIds.has(cycle.repeat_edge), `${graph.id}/${cycle.id} has unknown repeat edge`);
    check(edgeIds.has(cycle.exhaustion_edge), `${graph.id}/${cycle.id} has unknown exhaustion edge`);
    check(graph.edges.find((edge) => edge.id === cycle.exhaustion_edge)?.exhaustion === true, `${graph.id}/${cycle.id} exhaustion edge is not explicitly marked`);
    check(cycle.no_next_attempt_after_exhaustion === true, `${graph.id}/${cycle.id} does not forbid a next attempt after exhaustion`);
  }
  for (const observedCycle of findDirectedCycles(graph.nodes, graph.edges)) {
    const covered = boundedCycleSets.some((declared) => [...observedCycle].every((node) => declared.has(node)));
    check(covered, `${graph.id} contains an undeclared or unbounded cycle over ${[...observedCycle].join(", ")}`);
  }
}

const requiredForms = ["rwo:Sequence", "rwo:FanOut", "rwo:FanIn", "rwo:Gate", "rwo:Sidecar", "rwo:BoundedRepeat", "rwo:ExplicitComposition"];
for (const form of requiredForms) check(observedCompositionForms.has(form), `illustrative example does not cover ${form}`);
pass("illustrative-recursive-pipeline", `${definitionIds.size} WorkDefinitions and ${graphIds.size} nested WorkGraphs cover all seven composition forms with one root kernel`);

const result = {
  validation: failures.length === 0 ? "pass" : "fail",
  ontology_id: ontology.ontology.id,
  ontology_sha256: digest(ontologyDoc.bytes),
  view_sha256: digest(viewDoc.bytes),
  view_implementation_sha256: viewImplementationDigest,
  example_sha256: digest(exampleDoc.bytes),
  counts: {
    sources: sourceIds.size,
    source_selectors: allSourceRefs.length,
    owner_routes: ownerIds.size,
    element_types: typeIds.size,
    typed_properties: propertyIds.size,
    relations: relationIds.size,
    shields: shieldIds.size,
    constraint_operators: operatorIds.size,
    constraints: constraintIds.size,
    profiles: profileIds.size,
    observation_projections: projectionIds.size,
    premises: premiseIds.size,
    residue: residueIds.size,
    view_lenses: viewLensIds.size,
    negative_controls: negativeControlIds.size,
    example_work_definitions: definitionIds.size,
    example_graphs: graphIds.size
  },
  source_digests: sourceDigestResults,
  checks,
  unsupported: [
    "implementation existence",
    "runtime conformance",
    "delivery and replay behavior",
    "external-effect occurrence",
    "browser behavior beyond the tested HTML digest and viewport configurations",
    "accessibility conformance",
    "human comprehension",
    "ontology promotion"
  ],
  claim_ceiling: "A pass establishes candidate package integrity and included finite-fixture consistency only.",
  failures
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
if (failures.length > 0) process.exitCode = 1;
