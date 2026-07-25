const root = document.querySelector("#app");
const params = new URLSearchParams(location.search);
const variant = (document.documentElement.dataset.variant || params.get("variant") || "A").toUpperCase();
const forcedState = params.get("state");
const forcedTheme = params.get("theme");
const API = "/v1/control-center";
const requestBase = {scope_id: "repo", request_id: `cc-${variant}`, schema_version: "1"};
const variantNames = {A: "Signal Deck", B: "Ops Rail", C: "Guided Ledger"};
const ui = {
  kind: "skill", query: "", selected: null, catalog: [], detail: null, topology: null,
  theme: forcedTheme || localStorage.getItem("cc-theme") || "light",
  density: localStorage.getItem("cc-density") || "comfortable",
};
document.documentElement.dataset.variant = variant;
document.documentElement.dataset.theme = ui.theme;
document.documentElement.dataset.density = ui.density;

const esc = value => String(value ?? "").replace(/[&<>"']/g, c =>
  ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
const query = values => {
  const out = new URLSearchParams();
  Object.entries(values).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") return;
    (Array.isArray(value) ? value : [value]).forEach(item => out.append(key, item));
  });
  return out.toString();
};
const $ = selector => document.querySelector(selector);

root.innerHTML = `
<a class="skip-link" href="#workspace">Skip to workspace</a>
<div class="app-shell">
  <header class="command-bar">
    <a class="brand" href="../index.html" aria-label="Skill Control Center home">
      <span class="brand-mark" aria-hidden="true">⌁</span>
      <span>Skill Control Center<small>${variantNames[variant]} · Phase 1</small></span>
    </a>
    <div class="scope-chip" data-testid="cc-scope">
      <span class="pulse" aria-hidden="true"></span>
      <span><b>cyberalchemy-orchestrator</b><small>Local read model · @VictorBoscaro</small></span>
    </div>
    <div class="preferences" aria-label="Local display preferences">
      <label><span>Theme</span><select id="theme-select"><option value="light">Light</option><option value="dark">Dark</option></select></label>
      <label><span>Density</span><select id="density-select"><option value="comfortable">Comfortable</option><option value="compact">Compact</option></select></label>
    </div>
    <nav class="variant-switcher" aria-label="Interface variants">
      ${["A","B","C"].map(v => `<a ${v === variant ? 'aria-current="page"' : ""} href="../${v.toLowerCase()}/index.html">${v}</a>`).join("")}
    </nav>
  </header>

  <main id="workspace" class="workspace" tabindex="-1">
    <section class="surface attention-surface" data-testid="cc-attention" aria-labelledby="attention-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Step 01" : "Current pulse"}</span><h1 id="attention-title">Needs attention</h1></div>
        <span id="attention-count" class="metric">…</span>
      </header>
      <div id="source-health" data-testid="cc-source-health" class="health-chip"><span aria-hidden="true">◇</span> Checking sources</div>
      <ul id="attention-list" class="attention-list"><li class="quiet">Loading operational signals…</li></ul>
    </section>

    <section class="surface catalog-surface" aria-labelledby="catalog-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Step 02" : "Inventory"}</span><h2 id="catalog-title">Skills and dispatches</h2></div>
        <span id="result-count" class="metric">…</span>
      </header>
      <form id="search-form" role="search" class="search-row">
        <label for="search">Search the catalog</label>
        <div><input id="search" data-testid="cc-search" type="search" placeholder="Name, purpose or path"><button type="submit" class="primary">Search</button></div>
      </form>
      <fieldset id="filters" data-testid="cc-filters" class="filter-tabs">
        <legend>Object type</legend>
        <label><input type="radio" name="kind" value="skill" checked><span>Skills</span></label>
        <label><input type="radio" name="kind" value="dispatch"><span>Dispatches</span></label>
      </fieldset>
      <div id="catalog-list" data-testid="cc-catalog" class="catalog-list" role="listbox" aria-label="Catalog results">
        <div class="quiet">Loading catalog…</div>
      </div>
      <footer class="selection-bar">
        <span data-testid="cc-selection" id="selection">No selection</span>
        <span class="selection-actions">
          <button data-testid="cc-open-detail" id="open-detail" type="button" class="secondary" disabled>Open detail</button>
          <button data-testid="cc-open-topology" id="open-topology" type="button" class="tertiary" disabled>See relationships</button>
        </span>
      </footer>
    </section>

    <aside class="surface detail-surface" aria-labelledby="detail-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Step 03" : "Inspector"}</span><h2 id="detail-title" tabindex="-1">Detail and evidence</h2></div>
        <button data-testid="cc-back" id="back" type="button" class="tertiary" hidden>Back</button>
      </header>
      <div id="detail-body" data-testid="cc-detail" class="detail-body">
        <div class="zero-state"><span aria-hidden="true">↳</span><b>Choose an object</b><p>Selection is safe. Detail opens only when you ask.</p></div>
      </div>
    </aside>

    <section class="surface topology-surface" aria-labelledby="topology-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Step 04" : "Map"}</span><h2 id="topology-title">Relationships and paths</h2></div>
        <span id="topology-meta" class="metric">Choose an object</span>
      </header>
      <div class="topology-toolbar">
        <label>Model<select id="model"><option value="skill-relations">Skill relations</option><option value="dispatch-lineage">Dispatch hierarchy</option><option value="intra-dispatch">Dispatch workflow</option></select></label>
        <button id="load-topology" type="button" class="secondary" disabled>Load map</button>
      </div>
      <div class="topology-layout">
        <div id="graph" data-testid="cc-topology" class="graph" aria-hidden="true"><div class="zero-state">The map appears after an explicit action.</div></div>
        <div class="semantic-panel">
          <div data-testid="cc-topology-table" class="table-wrap">
            <table><caption>Complete semantic alternative to the visual map</caption><thead><tr><th>From</th><th>Relationship</th><th>To</th></tr></thead><tbody id="topology-table"><tr><td colspan="3">No relationships loaded.</td></tr></tbody></table>
          </div>
          <form id="path-form" data-testid="cc-path-form" class="path-form">
            <label>From<input id="path-source" autocomplete="off"></label>
            <label>To<input id="path-target" autocomplete="off"></label>
            <label>Maximum<select id="path-limit"><option value="3">3 paths</option><option value="1">1 path</option></select></label>
            <button type="submit" class="primary">Find path</button>
          </form>
          <div id="path-result" data-testid="cc-path-result" class="path-result">Bounded to 4 levels and 3 paths.</div>
        </div>
      </div>
    </section>

    <section id="fixture-state" class="surface fixture-surface" hidden aria-labelledby="fixture-title"></section>
  </main>
  <div id="status" data-testid="cc-status-live" class="live-status" role="status" aria-live="polite"></div>
</div>`;

$("#theme-select").value = ui.theme;
$("#density-select").value = ui.density;

function announce(message) {
  const node = $("#status");
  node.textContent = message;
  node.classList.add("visible");
  clearTimeout(announce.timer);
  announce.timer = setTimeout(() => node.classList.remove("visible"), 1800);
}
async function get(path, values = {}) {
  const response = await fetch(`${API}${path}?${query({...requestBase, ...values})}`);
  const body = await response.json();
  if (!response.ok) throw new Error(body?.error?.message || body?.data?.field_errors?.join(", ") || `HTTP ${response.status}`);
  return body;
}
function setPreference(kind, value) {
  localStorage.setItem(`cc-${kind}`, value);
  document.documentElement.dataset[kind] = value;
  announce(`${kind} saved locally`);
}

const stateCopy = {
  "loading": ["Loading without losing context", "The current scope and selection remain stable while the read completes."],
  "empty": ["Complete result · nothing here", "This scope is empty. It is not unavailable and it does not mean unused."],
  "no-match": ["No matches", "Keep the active query visible and clear filters to return to the catalog."],
  "focal-lineage": ["Focused lineage ready", "The visual map and semantic table carry the same node and relationship identities."],
  "observed-overlay": ["Observed evidence", "12 accepted invocations · complete window · fresh source. Counts are proof-bound."],
  "stale-degraded": ["Stale source", "Last ingest 18h ago · SLA 4h · origin telemetry cache. Existing facts remain visible."],
  "partial-error": ["Partial · lower bound", "9 observed events retained. One source partition is missing; do not infer a total."],
  "invalid-endpoint": ["Endpoint outside coverage", "The named endpoint is absent from this complete model. Query and selection are unchanged."],
  "truncated-path": ["Path result truncated", "Limit reached at depth 4. Returned evidence IDs remain inspectable; more paths may exist."],
  "draft-dirty": ["Unsaved local draft", "Target and base revision are retained. Review the diff before saving."],
  "draft-saved": ["Draft saved locally", "Local revision 2 is ready for non-authoritative validation."],
  "validating": ["Validating preview", "Draft editing is protected while validator v1 checks this local proposal."],
  "valid": ["Valid preview · non-authoritative", "The preview passed validator v1. It grants no authority and changes nothing."],
  "invalid": ["Invalid preview · non-authoritative", "A required description is missing. The finding is linked to the retained field."],
  "save-failed": ["Local save failed", "Input is retained and the stored revision did not change. Review and try saving locally again."],
  "local-conflict": ["Local revision conflict", "Stored revision 3 differs from caller revision 2. Review the retained proposal."],
  "read-api-unavailable": ["Read interface unavailable", "host_id, auth_contract_id and route_owner_id must all be bound before any read request."],
};
function renderFixtureState(id) {
  const panel = $("#fixture-state");
  const [title, copy] = stateCopy[id] || stateCopy.loading;
  panel.hidden = false;
  panel.innerHTML = `<div class="fixture-state-card" data-testid="cc-state-${esc(id)}">
    <div class="state-symbol" aria-hidden="true">${["invalid","save-failed","read-api-unavailable"].includes(id) ? "!" : id.includes("draft") || id === "validating" || id === "valid" ? "✦" : "◇"}</div>
    <div><span class="kicker">Evidence fixture · ${esc(id)}</span><h2 id="fixture-title">${esc(title)}</h2><p>${esc(copy)}</p>
      <dl><div><dt>Scope</dt><dd>cyberalchemy-orchestrator</dd></div><div><dt>Owner</dt><dd>@VictorBoscaro</dd></div><div><dt>Authority</dt><dd>Read / local preview only</dd></div></dl>
    </div>
  </div>`;
  document.body.classList.add("fixture-mode");
}

async function loadAttention() {
  try {
    const body = await get("/attention", {window_start_utc: "2026-01-01T00:00:00Z", window_end_utc: "2026-12-31T23:59:59Z", limit: 6});
    const items = body.data?.items || [];
    $("#attention-count").textContent = String(items.length);
    $("#source-health").innerHTML = `<span aria-hidden="true">${body.completeness === "complete" ? "◆" : "△"}</span> ${body.completeness === "complete" ? "Complete source coverage" : "Partial · lower bound"}`;
    $("#attention-list").innerHTML = items.length ? items.slice(0, variant === "B" ? 8 : 3).map(item =>
      `<li><span class="signal-mark" aria-hidden="true"></span><div><b>${esc(item.kind?.replaceAll("-", " ") || "Signal")}</b><p>${esc(item.reason || "Needs inspection")}</p></div></li>`).join("") :
      `<li class="quiet">Nothing needs attention in this scope.</li>`;
  } catch (error) {
    $("#attention-list").innerHTML = `<li class="quiet"><b>Read interface unavailable</b><p>${esc(error.message)}</p></li>`;
    $("#source-health").innerHTML = `<span aria-hidden="true">!</span> Unavailable · no zero inferred`;
    $("#source-health").classList.add("warning");
  }
}

async function loadCatalog() {
  const list = $("#catalog-list");
  list.setAttribute("aria-busy", "true");
  list.innerHTML = `<div class="quiet">Loading without losing context…</div>`;
  try {
    const body = await get("/catalog", {query: ui.query, object_kinds: ui.kind, limit: 50});
    ui.catalog = body.data?.matches || [];
    $("#result-count").textContent = `${ui.catalog.length} results`;
    list.innerHTML = ui.catalog.length ? ui.catalog.map(row => `
      <div class="catalog-item" role="option" tabindex="0" aria-selected="${ui.selected?.object_id === row.object_id}" data-id="${esc(row.object_id)}">
        <span class="object-kind">${row.object_kind === "skill" ? "S" : "D"}</span>
        <button type="button"><b>${esc(row.display_label)}</b><small>${esc(row.description || row.path || "No description")}</small></button>
        <span class="usage-proof"><i aria-hidden="true"></i> Usage ${esc(row.evidence_summary?.logical_invocation_count ?? (row.evidence_summary?.evidence_classes || [row.evidence_summary?.completeness || "not reported"]).join(", "))}</span>
      </div>`).join("") : `<div class="zero-state"><b>No matches</b><p>Adjust the search or clear the active filter.</p></div>`;
  } catch (error) {
    list.innerHTML = `<div class="zero-state"><b>Read interface unavailable</b><p>${esc(error.message)}</p></div>`;
  } finally {
    list.removeAttribute("aria-busy");
  }
}

function clearDependent(message = "Choose an object, then open detail explicitly.") {
  ui.detail = null; ui.topology = null;
  $("#detail-body").innerHTML = `<div class="zero-state"><b>Identity changed</b><p>${esc(message)}</p></div>`;
  $("#back").hidden = true;
  $("#topology-meta").textContent = "Choose an object";
  $("#graph").innerHTML = `<div class="zero-state">The map appears after an explicit action.</div>`;
  $("#topology-table").innerHTML = `<tr><td colspan="3">No relationships loaded.</td></tr>`;
  $("#path-result").textContent = "Choose endpoints for a bounded path query.";
  $("#path-source").value = ""; $("#path-target").value = "";
}
function selectObject(id) {
  if (ui.selected?.object_id !== id) clearDependent("The selected identity changed; dependent evidence was cleared.");
  ui.selected = ui.catalog.find(item => item.object_id === id);
  document.querySelectorAll(".catalog-item").forEach(row => row.setAttribute("aria-selected", String(row.dataset.id === id)));
  $("#selection").textContent = ui.selected ? `${ui.selected.object_kind} · ${ui.selected.display_label}` : "No selection";
  ["#open-detail", "#open-topology", "#load-topology"].forEach(selector => $(selector).disabled = !ui.selected);
  $("#path-source").value = id;
  announce(`${ui.selected.display_label} selected. Choose an explicit action.`);
}
function draftMarkup(identity) {
  const key = `cc-draft:${identity.object_id}`;
  const saved = localStorage.getItem(key) || "";
  return `<section data-testid="cc-draft" class="draft-card">
    <header><div><span class="kicker">Local proposal</span><h3>Draft and diff preview</h3></div><span id="draft-status" data-testid="cc-draft-status" class="status-pill">Clean</span></header>
    <label for="draft-text">Proposed description</label>
    <textarea id="draft-text" placeholder="Describe a local proposal">${esc(saved)}</textarea>
    <label for="draft-diff">Preview</label><pre id="draft-diff">No changes.</pre>
    <div class="button-row"><button id="save-draft" type="button" class="secondary">Save locally</button><button id="validate-draft" type="button" class="tertiary">Validate preview</button></div>
  </section>`;
}
function bindDraft() {
  const text = $("#draft-text"), diff = $("#draft-diff"), status = $("#draft-status");
  const key = `cc-draft:${ui.selected.object_id}`;
  text.addEventListener("input", () => {
    diff.textContent = `- current description\n+ ${text.value || "(empty)"}`;
    status.textContent = "Unsaved";
  });
  $("#save-draft").addEventListener("click", () => {
    localStorage.setItem(key, text.value);
    status.textContent = "Saved locally";
    announce("Draft saved only in this browser");
  });
  $("#validate-draft").addEventListener("click", () => {
    status.textContent = "Validating…";
    text.disabled = true;
    setTimeout(() => {
      text.disabled = false;
      status.textContent = `${text.value.trim().length >= 8 ? "Valid" : "Invalid"} preview · non-authoritative`;
      announce(status.textContent);
    }, 180);
  });
}
async function openDetail() {
  if (!ui.selected) return;
  const requestedIdentity = `${ui.selected.object_kind}:${ui.selected.object_id}`;
  const evidenceParams = {claim_id: "times-used", window_start_utc: "2026-01-01T00:00:00Z", window_end_utc: "2026-12-31T23:59:59Z"};
  const [body, evidenceBody] = await Promise.all([
    get(`/objects/${encodeURIComponent(ui.selected.object_kind)}/${encodeURIComponent(ui.selected.object_id)}`, evidenceParams),
    get(`/evidence/${encodeURIComponent(ui.selected.object_kind)}/${encodeURIComponent(ui.selected.object_id)}`, evidenceParams),
  ]);
  if (`${ui.selected?.object_kind}:${ui.selected?.object_id}` !== requestedIdentity) return;
  const detail = body.data || {}, identity = detail.identity || {}, evidence = detail.evidence || {};
  const evidenceClasses = (evidence.evidence_classes || evidenceBody.evidence_classes || []).join(", ")
    || (evidence.logical_invocation_count == null ? "unknown-or-unavailable" : "not reported");
  const providers = (evidenceBody.source_facts || evidence.source_facts || []).map(fact => fact.source_id).filter(Boolean);
  const usage = evidence.logical_invocation_count == null ? "Unknown" : evidence.logical_invocation_count;
  ui.detail = detail;
  $("#detail-body").innerHTML = `
    <article class="identity-card">
      <span class="status-pill">${esc(identity.object_kind || ui.selected.object_kind)}</span>
      <h3>${esc(identity.display_label || ui.selected.display_label)}</h3>
      <p>${esc(identity.description || "No description registered.")}</p><code>${esc(identity.path || identity.object_id)}</code>
    </article>
    <dl class="fact-grid">
      <div><dt>Owner</dt><dd>${esc(identity.owner || "@VictorBoscaro")}</dd></div>
      <div><dt>Read state</dt><dd>${esc(detail.query_state || "success")}</dd></div>
      <div><dt>Observed usage</dt><dd>${esc(usage)}</dd></div>
      <div><dt>Freshness</dt><dd>${esc(evidence.freshness || "unknown")}</dd></div>
    </dl>
    <section data-testid="cc-evidence" class="evidence-card">
      <span aria-hidden="true">◇</span><div><b>${esc(evidenceBody.result_state)} · ${esc(evidenceClasses)}</b><p><strong>Provider:</strong> ${esc(providers.join(", ") || "not reported")}</p><p>${esc(evidenceBody.warnings?.[0] || evidence.source_facts?.[0]?.safe_reason || "No provider warning.")}</p></div>
    </section>
    ${draftMarkup(identity)}
    <section data-testid="cc-authoritative-route-unavailable" class="authority-boundary">
      <span aria-hidden="true">┆</span><div><b>Safe end of Phase 1</b><p>Local drafts can be saved and validated. Authoritative change routes are unavailable and tracked in SCC-BL-001–003.</p></div>
    </section>`;
  bindDraft();
  $("#back").hidden = false;
  $(".detail-surface").scrollIntoView({behavior: "smooth", block: "start"});
  $("#detail-title").focus();
  announce("Detail opened");
}

function nodeId(node) { return node.id || node.dispatch_id || node.group_id; }
function edgeEnds(edge) {
  return [edge.source_id || edge.parent_id || edge.from_group_id, edge.target_id || edge.child_id || edge.to_group_id];
}
function renderTopology(data) {
  const nodes = data?.nodes || [], edges = data?.edges || [];
  $("#topology-meta").textContent = `${nodes.length} nodes · ${edges.length} relationships`;
  if (!nodes.length) {
    $("#graph").innerHTML = `<div class="zero-state">No relationships in this bounded view.</div>`;
    $("#topology-table").innerHTML = `<tr><td colspan="3">No relationships.</td></tr>`;
    return;
  }
  const width = 720, height = 390, positions = new Map();
  nodes.forEach((node, index) => {
    const columns = variant === "B" ? 3 : variant === "C" ? 2 : 5;
    const col = index % columns, row = Math.floor(index / columns);
    positions.set(nodeId(node), {x: 90 + col * (540 / Math.max(columns - 1, 1)), y: 70 + row * 92});
  });
  const lines = edges.map(edge => {
    const [from, to] = edgeEnds(edge), a = positions.get(from), b = positions.get(to);
    return a && b ? `<path data-evidence-id="${esc(edge.evidence_id || "")}" class="edge ${edge.edge_kind === "named_reference" ? "mention" : ""}" d="M${a.x},${a.y} C${a.x},${(a.y+b.y)/2} ${b.x},${(a.y+b.y)/2} ${b.x},${b.y}"/>` : "";
  }).join("");
  const points = nodes.map(node => {
    const id = nodeId(node), p = positions.get(id), focus = id === data.focus_id;
    return `<g data-node-id="${esc(id)}" class="graph-node ${focus ? "focus" : ""}"><rect x="${p.x-62}" y="${p.y-18}" width="124" height="36" rx="10"/><text x="${p.x}" y="${p.y+4}" text-anchor="middle">${esc(String(node.display_label || node.label || id).slice(0, 17))}</text></g>`;
  }).join("");
  $("#graph").innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Complementary relationship map">${lines}${points}</svg>`;
  $("#topology-table").innerHTML = edges.length ? edges.map(edge => {
    const [from, to] = edgeEnds(edge);
    const label = edge.edge_kind === "named_reference" ? "Mention" : edge.edge_kind === "explicit_path" ? "Explicit path reference" : edge.edge_kind || edge.kind;
    return `<tr data-evidence-id="${esc(edge.evidence_id || "")}"><td>${esc(from)}</td><td>${esc(label)}</td><td>${esc(to)}</td></tr>`;
  }).join("") : nodes.map(node => `<tr><td>${esc(nodeId(node))}</td><td>Focal node</td><td>—</td></tr>`).join("");
}
async function loadTopology() {
  if (!ui.selected) return;
  const requestedIdentity = `${ui.selected.object_kind}:${ui.selected.object_id}`;
  let model = $("#model").value;
  if (ui.selected.object_kind === "skill") model = "skill-relations";
  else if (model === "skill-relations") model = "dispatch-lineage";
  $("#model").value = model;
  const values = {focus_id: ui.selected.object_id, direction: "both", depth: 1, node_limit: 40};
  if (model === "skill-relations") values.edge_kinds = ["explicit_path", "named_reference"];
  if (model === "dispatch-lineage") values.edge_kinds = "parent_dispatch_id";
  if (model === "intra-dispatch") { values.dispatch_id = ui.selected.object_id; values.edge_kinds = ["sequential", "zig-zag", "feedback"]; }
  const body = await get(`/topology/${model}`, values);
  if (`${ui.selected?.object_kind}:${ui.selected?.object_id}` !== requestedIdentity) return;
  ui.topology = body.data;
  renderTopology(body.data);
  $(".topology-surface").scrollIntoView({behavior: "smooth", block: "start"});
  announce(`${model} loaded`);
}

$("#theme-select").addEventListener("change", event => setPreference("theme", event.target.value));
$("#density-select").addEventListener("change", event => setPreference("density", event.target.value));
$("#search-form").addEventListener("submit", event => { event.preventDefault(); ui.query = $("#search").value.trim(); loadCatalog(); announce("Search updated"); });
$("#filters").addEventListener("change", event => { ui.kind = event.target.value; ui.selected = null; clearDependent("The object filter changed; select a new identity."); $("#selection").textContent = "No selection"; ["#open-detail","#open-topology","#load-topology"].forEach(s => $(s).disabled = true); loadCatalog(); });
$("#catalog-list").addEventListener("click", event => { const row = event.target.closest(".catalog-item"); if (row) selectObject(row.dataset.id); });
$("#catalog-list").addEventListener("keydown", event => { const row = event.target.closest(".catalog-item"); if (row && ["Enter"," "].includes(event.key)) { event.preventDefault(); selectObject(row.dataset.id); } });
$("#open-detail").addEventListener("click", () => openDetail().catch(error => announce(error.message)));
$("#open-topology").addEventListener("click", () => loadTopology().catch(error => announce(error.message)));
$("#load-topology").addEventListener("click", () => loadTopology().catch(error => announce(error.message)));
$("#back").addEventListener("click", () => { $(".catalog-surface").scrollIntoView(); document.querySelector(`.catalog-item[data-id="${CSS.escape(ui.selected.object_id)}"]`)?.focus(); });
$("#path-form").addEventListener("submit", async event => {
  event.preventDefault();
  const requestedIdentity = `${ui.selected?.object_kind}:${ui.selected?.object_id}`;
  const model = $("#model").value;
  const payload = {...requestBase, model, source_id: $("#path-source").value.trim(), target_id: $("#path-target").value.trim(), direction: "outbound", allowed_edge_kinds: model === "skill-relations" ? ["explicit_path","named_reference"] : model === "dispatch-lineage" ? ["parent_dispatch_id"] : ["sequential","zig-zag","feedback"], max_depth: 4, max_paths: Number($("#path-limit").value)};
  if (model === "intra-dispatch") payload.dispatch_id = ui.selected?.object_id;
  try {
    const response = await fetch(`${API}/path-query`, {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify(payload)});
    const body = await response.json(), data = body.data || {};
    if (`${ui.selected?.object_kind}:${ui.selected?.object_id}` !== requestedIdentity) return;
    renderPathResult(data);
    announce("Path query completed");
  } catch (error) {
    if (`${ui.selected?.object_kind}:${ui.selected?.object_id}` === requestedIdentity) $("#path-result").textContent = `Path query unavailable: ${error.message}`;
  }
});
function renderPathResult(data) {
  document.querySelectorAll(".path-hit").forEach(node => node.classList.remove("path-hit"));
  const paths = data.paths || [], limited = data.query_state === "truncated" || data.more_paths_exist;
  if (!["success", "truncated"].includes(data.query_state) || !paths.length) {
    $("#path-result").innerHTML = `<b>${esc(data.query_state || "unavailable")}</b><p>No path asserted beyond available coverage and declared limits.</p>`;
    return;
  }
  const evidenceIds = new Set(), nodeIds = new Set();
  paths.forEach(path => {
    (path.edges || []).forEach(edge => evidenceIds.add(edge.evidence_id));
    (path.node_ids || []).forEach(id => nodeIds.add(id));
  });
  document.querySelectorAll("[data-evidence-id]").forEach(node => { if (evidenceIds.has(node.dataset.evidenceId)) node.classList.add("path-hit"); });
  document.querySelectorAll("[data-node-id]").forEach(node => { if (nodeIds.has(node.dataset.nodeId)) node.classList.add("path-hit"); });
  $("#path-result").innerHTML = `<b>${paths.length} ordered path(s)${limited ? " · truncated by declared limit" : ""}</b><ol>${paths.map(path => `<li><span>${path.node_ids.map(esc).join(" → ")}</span>${path.edges.map(edge => `<code>${esc(edge.evidence_id)}</code>`).join("")}</li>`).join("")}</ol>`;
}

if (forcedState) {
  renderFixtureState(forcedState);
  $("#attention-count").textContent = "fixture";
  $("#result-count").textContent = "fixture";
  $("#source-health").innerHTML = `<span aria-hidden="true">◇</span> Deterministic evidence state`;
} else {
  Promise.all([loadAttention(), loadCatalog()]).then(() => announce("Control Center ready"));
}
