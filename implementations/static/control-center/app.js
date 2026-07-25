const root = document.querySelector("#app");
const params = new URLSearchParams(location.search);
const variant = (document.documentElement.dataset.variant || params.get("variant") || "A").toUpperCase();
const forcedState = params.get("state");
const forcedTheme = params.get("theme");
const FE_RULES = ["FE-1","FE-2","FE-3","FE-4","FE-5","FE-6","FE-7","FE-8","FE-9","FE-10"];
const FE_FLAGS = Object.fromEntries(FE_RULES.map(rule => [rule, params.get(rule.toLowerCase()) !== "off"]));
const FE_METRICS = Object.fromEntries(FE_RULES.map(rule => [rule, {}]));
function emitFeMetric(rule, event) {
  const bucket = FE_METRICS[rule];
  if (!bucket) return;
  bucket[event] = (bucket[event] || 0) + 1;
  if (rule !== "FE-10") {
    FE_METRICS["FE-10"]["metric-emitted"] = (FE_METRICS["FE-10"]["metric-emitted"] || 0) + 1;
  }
  window.dispatchEvent(new CustomEvent("cc:fe-metric", {detail: {rule, event, count: bucket[event]}}));
}
window.__CC_FE__ = {flags: FE_FLAGS, metrics: FE_METRICS};
const API = "/v1/control-center";
const requestBase = {scope_id: "repo", request_id: `cc-${variant}`, schema_version: "1"};
const variantNames = {A: "Signal Deck", B: "Ops Rail", C: "Guided Ledger"};
const ui = {
  kind: "skill", query: "", selected: null, catalog: [], detail: null, topology: null,
  theme: forcedTheme || localStorage.getItem("cc-theme") || "light",
  density: localStorage.getItem("cc-density") || "comfortable",
  expandedRelationship: null,
  explainMode: false,
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
<a class="skip-link" href="#workspace">Pular para o espaço de trabalho</a>
<div class="app-shell" data-fe-rule="FE-10">
  <header class="command-bar">
    <a class="brand" href="../index.html" aria-label="Skill Control Center home">
      <span class="brand-mark" aria-hidden="true">⌁</span>
      <span>Skill Control Center<small>${variantNames[variant]} · candidata · Fase 1</small></span>
    </a>
    <div class="scope-chip" data-testid="cc-scope">
      <span class="pulse" aria-hidden="true"></span>
      <span><b>cyberalchemy-orchestrator</b><small>Leitura local · @VictorBoscaro</small></span>
    </div>
    <div class="preferences" aria-label="Local display preferences">
      <label><span>Tema</span><select id="theme-select"><option value="light">Claro</option><option value="dark">Escuro</option></select></label>
      <label><span>Densidade</span><select id="density-select"><option value="comfortable">Confortável</option><option value="compact">Compacta</option></select></label>
    </div>
    <nav class="variant-switcher" aria-label="Variantes candidatas" data-fe-rule="FE-8">
      ${["A","B","C"].map(v => `<a ${v === variant ? 'aria-current="page"' : ""} href="../${v.toLowerCase()}/index.html">${v}</a>`).join("")}
    </nav>
  </header>

  <main id="workspace" class="workspace" tabindex="-1">
    <section class="surface attention-surface" data-testid="cc-attention" data-fe-rule="FE-5" aria-labelledby="attention-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Etapa 01" : "Agora"}</span><h1 id="attention-title">Pede atenção</h1></div>
        <span id="attention-count" class="metric">…</span>
      </header>
      <div id="source-health" data-testid="cc-source-health" class="health-chip"><span aria-hidden="true">◇</span> Verificando fontes</div>
      <ul id="attention-list" class="attention-list"><li class="quiet">Carregando sinais operacionais…</li></ul>
    </section>

    <section class="surface catalog-surface" aria-labelledby="catalog-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Etapa 02" : "Inventário"}</span><h2 id="catalog-title">Skills e Dispatches</h2></div>
        <span id="result-count" class="metric">…</span>
      </header>
      <form id="search-form" role="search" class="search-row">
        <label for="search">Buscar no catálogo</label>
        <div><input id="search" data-testid="cc-search" type="search" placeholder="Nome, finalidade ou caminho"><button type="submit" class="primary">Buscar</button></div>
      </form>
      <fieldset id="filters" data-testid="cc-filters" class="filter-tabs">
        <legend>Tipo de objeto</legend>
        <label><input type="radio" name="kind" value="skill" checked><span>Skills</span></label>
        <label><input type="radio" name="kind" value="dispatch"><span>Dispatches</span></label>
      </fieldset>
      <div id="catalog-list" data-testid="cc-catalog" class="catalog-list" role="listbox" aria-label="Catalog results">
        <div class="quiet">Carregando catálogo…</div>
      </div>
      <footer class="selection-bar">
        <span data-testid="cc-selection" id="selection">Nada selecionado</span>
        <span class="selection-actions">
          <button data-testid="cc-open-detail" id="open-detail" type="button" class="secondary" disabled>Abrir detalhe</button>
          <button data-testid="cc-open-topology" id="open-topology" type="button" class="tertiary" disabled>Ver relações</button>
        </span>
      </footer>
    </section>

    <aside class="surface detail-surface" aria-labelledby="detail-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Etapa 03" : "Inspecionar"}</span><h2 id="detail-title" tabindex="-1">Detalhe e evidência</h2></div>
        <button data-testid="cc-back" id="back" type="button" class="tertiary" hidden>Voltar</button>
      </header>
      <div id="detail-body" data-testid="cc-detail" class="detail-body">
        <div class="zero-state"><span aria-hidden="true">↳</span><b>Escolha um objeto</b><p>O detalhe só abre quando você pedir.</p></div>
      </div>
    </aside>

    <section class="surface topology-surface" aria-labelledby="topology-title">
      <header class="surface-header">
        <div><span class="kicker">${variant === "C" ? "Etapa 04" : "Mapa"}</span><h2 id="topology-title">Quem chama quem</h2></div>
        <div class="topology-heading-actions">
          <button id="explain-toggle" data-testid="cc-explain-toggle" type="button" class="tertiary" aria-pressed="false" data-fe-rule="FE-9">? Explicar</button>
          <span id="topology-meta" class="metric">Escolha uma skill</span>
        </div>
      </header>
      <div class="topology-toolbar">
        <label>Modelo<select id="model"><option value="skill-relations">Chamadas entre skills</option><option value="dispatch-lineage">Hierarquia de Dispatch</option><option value="intra-dispatch">Fluxo do Dispatch</option></select></label>
        <button id="load-topology" type="button" class="secondary" disabled>Carregar mapa</button>
      </div>
      <div class="topology-layout">
        <div id="graph" data-testid="cc-topology" class="graph"><div class="zero-state">O mapa aparece após uma ação explícita.</div></div>
        <div class="semantic-panel">
          <section id="call-map" data-testid="cc-call-map" class="call-map" data-fe-rule="FE-1 FE-4 FE-6">
            <div class="zero-state"><b>Selecione uma skill</b><p>Você verá quem a chama e o que ela chama.</p></div>
          </section>
          <div id="relationship-detail" data-testid="cc-relationship-detail" data-fe-rule="FE-3 FE-4 FE-6" class="relationship-detail" hidden></div>
          <div data-testid="cc-topology-table" class="table-wrap">
            <table><caption>Alternativa semântica completa ao mapa</caption><thead><tr><th>Origem</th><th>Relação</th><th>Destino</th></tr></thead><tbody id="topology-table"><tr><td colspan="3">Nenhuma relação carregada.</td></tr></tbody></table>
          </div>
          <form id="path-form" data-testid="cc-path-form" data-fe-rule="FE-7" class="path-form">
            <label>Origem<input id="path-source" autocomplete="off"></label>
            <label>Destino<input id="path-target" autocomplete="off"></label>
            <label>Máximo<select id="path-limit"><option value="3">3 caminhos</option><option value="1">1 caminho</option></select></label>
            <button type="submit" class="primary">Encontrar caminho</button>
          </form>
          <div id="path-result" data-testid="cc-path-result" class="path-result">Limitado a 4 níveis e 3 caminhos.</div>
        </div>
      </div>
    </section>

    <section id="fixture-state" class="surface fixture-surface" hidden aria-labelledby="fixture-title"></section>
  </main>
  <div id="status" data-testid="cc-status-live" class="live-status" role="status" aria-live="polite"></div>
  <div id="tt" class="explain-tooltip" data-fe-rule="FE-2" role="tooltip" hidden></div>
</div>`;

$("#theme-select").value = ui.theme;
$("#density-select").value = ui.density;
$("#explain-toggle").hidden = !FE_FLAGS["FE-9"];
emitFeMetric("FE-8", "candidate-variant-view");

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
  "loading": ["Carregando sem perder contexto", "O escopo e a seleção permanecem estáveis enquanto a leitura termina."],
  "empty": ["Resultado completo · nada aqui", "Este escopo está vazio. Isso não significa indisponível nem sem uso."],
  "no-match": ["Nenhum resultado", "A consulta continua visível; limpe os filtros para voltar ao catálogo."],
  "focal-lineage": ["Linhagem focal pronta", "Mapa visual e tabela semântica carregam as mesmas identidades."],
  "observed-overlay": ["Evidência observada", "12 invocações aceitas · janela completa · fonte recente. A contagem está ligada à prova."],
  "stale-degraded": ["Fonte desatualizada", "Última ingestão há 18h · SLA 4h. Os fatos existentes continuam visíveis."],
  "partial-error": ["Parcial · limite inferior", "9 eventos observados foram retidos. Uma partição falta; não infira o total."],
  "invalid-endpoint": ["Endpoint fora da cobertura", "O endpoint não existe neste modelo completo. Consulta e seleção não mudaram."],
  "truncated-path": ["Caminho truncado", "O limite foi atingido na profundidade 4. As evidências retornadas continuam inspecionáveis."],
  "draft-dirty": ["Rascunho local não salvo", "Alvo e revisão-base foram retidos. Revise o diff antes de salvar."],
  "draft-saved": ["Rascunho salvo localmente", "A revisão local 2 está pronta para validação não autoritativa."],
  "validating": ["Validando prévia", "A edição fica protegida enquanto o validador verifica a proposta local."],
  "valid": ["Prévia válida · não autoritativa", "A prévia passou. Ela não concede autoridade nem muda dados."],
  "invalid": ["Prévia inválida · não autoritativa", "Falta uma descrição obrigatória; o achado aponta para o campo retido."],
  "save-failed": ["Falha ao salvar localmente", "A entrada foi retida e a revisão armazenada não mudou."],
  "local-conflict": ["Conflito de revisão local", "A revisão armazenada 3 difere da revisão 2 do chamador."],
  "read-api-unavailable": ["Interface de leitura indisponível", "Host, autenticação e owner da rota precisam estar vinculados."],
};
function renderFixtureState(id) {
  const panel = $("#fixture-state");
  const [title, copy] = stateCopy[id] || stateCopy.loading;
  panel.hidden = false;
  panel.innerHTML = `<div class="fixture-state-card" data-testid="cc-state-${esc(id)}">
    <div class="state-symbol" aria-hidden="true">${["invalid","save-failed","read-api-unavailable"].includes(id) ? "!" : id.includes("draft") || id === "validating" || id === "valid" ? "✦" : "◇"}</div>
    <div><span class="kicker">Fixture de evidência · ${esc(id)}</span><h2 id="fixture-title">${esc(title)}</h2><p>${esc(copy)}</p>
      <dl><div><dt>Escopo</dt><dd>cyberalchemy-orchestrator</dd></div><div><dt>Owner</dt><dd>@VictorBoscaro</dd></div><div><dt>Autoridade</dt><dd>Somente leitura / prévia local</dd></div></dl>
    </div>
  </div>`;
  document.body.classList.add("fixture-mode");
}

async function loadAttention() {
  try {
    const body = await get("/attention", {window_start_utc: "2026-01-01T00:00:00Z", window_end_utc: "2026-12-31T23:59:59Z", limit: 6});
    const items = body.data?.items || [];
    if (!items.length) emitFeMetric("FE-5", "empty-state-rendered");
    $("#attention-count").textContent = String(items.length);
    $("#source-health").innerHTML = `<span aria-hidden="true">${body.completeness === "complete" ? "◆" : "△"}</span> ${body.completeness === "complete" ? "Cobertura completa das fontes" : "Parcial · limite inferior"}`;
    $("#attention-list").innerHTML = items.length ? items.slice(0, variant === "B" ? 8 : 3).map(item =>
      `<li><span class="signal-mark" aria-hidden="true"></span><div><b>${esc(item.kind?.replaceAll("-", " ") || "Sinal")}</b><p>${esc(item.reason || "Precisa de inspeção")}</p></div></li>`).join("") :
      `<li class="quiet">Nada pede atenção neste escopo.</li>`;
  } catch (error) {
    emitFeMetric("FE-5", "error-state-rendered");
    $("#attention-list").innerHTML = `<li class="quiet"><b>Interface de leitura indisponível</b><p>${esc(error.message)}</p></li>`;
    $("#source-health").innerHTML = `<span aria-hidden="true">!</span> Indisponível · zero não inferido`;
    $("#source-health").classList.add("warning");
  }
}

async function loadCatalog() {
  const list = $("#catalog-list");
  list.setAttribute("aria-busy", "true");
  list.innerHTML = `<div class="quiet">Carregando sem perder contexto…</div>`;
  try {
    const body = await get("/catalog", {query: ui.query, object_kinds: ui.kind, limit: 50});
    ui.catalog = body.data?.matches || [];
    if (!ui.catalog.length) emitFeMetric("FE-5", "empty-state-rendered");
    $("#result-count").textContent = `${ui.catalog.length} resultado(s)`;
    list.innerHTML = ui.catalog.length ? ui.catalog.map(row => `
      <div class="catalog-item" role="option" tabindex="0" aria-selected="${ui.selected?.object_id === row.object_id}" data-id="${esc(row.object_id)}">
        <span class="object-kind">${row.object_kind === "skill" ? "S" : "D"}</span>
        <button type="button"><b>${esc(row.display_label)}</b><small>${esc(row.description || row.path || "Sem descrição")}</small></button>
        <span class="usage-proof"><i aria-hidden="true"></i> Uso ${esc(row.evidence_summary?.logical_invocation_count ?? (row.evidence_summary?.evidence_classes || [row.evidence_summary?.completeness || "não informado"]).join(", "))}</span>
      </div>`).join("") : `<div class="zero-state"><b>Nenhum resultado</b><p>Ajuste a busca ou limpe o filtro ativo.</p></div>`;
  } catch (error) {
    emitFeMetric("FE-5", "error-state-rendered");
    list.innerHTML = `<div class="zero-state"><b>Interface de leitura indisponível</b><p>${esc(error.message)}</p></div>`;
  } finally {
    list.removeAttribute("aria-busy");
  }
}

function clearDependent(message = "Escolha um objeto e abra o detalhe explicitamente.") {
  ui.detail = null; ui.topology = null;
  ui.expandedRelationship = null;
  $("#detail-body").innerHTML = `<div class="zero-state"><b>Identidade alterada</b><p>${esc(message)}</p></div>`;
  $("#back").hidden = true;
  $("#topology-meta").textContent = "Escolha um objeto";
  $("#graph").innerHTML = `<div class="zero-state">O mapa aparece após uma ação explícita.</div>`;
  $("#call-map").innerHTML = `<div class="zero-state"><b>Selecione uma skill</b><p>Você verá quem a chama e o que ela chama.</p></div>`;
  $("#relationship-detail").hidden = true;
  $("#relationship-detail").innerHTML = "";
  $("#topology-table").innerHTML = `<tr><td colspan="3">Nenhuma relação carregada.</td></tr>`;
  $("#path-result").textContent = "Escolha origem e destino para consultar um caminho limitado.";
  $("#path-source").value = ""; $("#path-target").value = "";
}
function selectObject(id) {
  if (ui.selected?.object_id !== id) clearDependent("A seleção mudou; detalhe, evidência e relações anteriores foram limpos.");
  ui.selected = ui.catalog.find(item => item.object_id === id);
  document.querySelectorAll(".catalog-item").forEach(row => row.setAttribute("aria-selected", String(row.dataset.id === id)));
  $("#selection").textContent = ui.selected ? `${ui.selected.object_kind} · ${ui.selected.display_label}` : "Nada selecionado";
  ["#open-detail", "#open-topology", "#load-topology"].forEach(selector => $(selector).disabled = !ui.selected);
  $("#path-source").value = id;
  announce(`${ui.selected.display_label} selecionada. Escolha uma ação.`);
}
function draftMarkup(identity) {
  const key = `cc-draft:${identity.object_id}`;
  const saved = localStorage.getItem(key) || "";
  return `<section data-testid="cc-draft" class="draft-card">
    <header><div><span class="kicker">Proposta local</span><h3>Rascunho e prévia do diff</h3></div><span id="draft-status" data-testid="cc-draft-status" class="status-pill">Limpo</span></header>
    <label for="draft-text">Descrição proposta</label>
    <textarea id="draft-text" placeholder="Descreva uma proposta local">${esc(saved)}</textarea>
    <label for="draft-diff">Prévia</label><pre id="draft-diff">Sem alterações.</pre>
    <div class="button-row"><button id="save-draft" type="button" class="secondary">Salvar localmente</button><button id="validate-draft" type="button" class="tertiary">Validar prévia</button></div>
  </section>`;
}
function bindDraft() {
  const text = $("#draft-text"), diff = $("#draft-diff"), status = $("#draft-status");
  const key = `cc-draft:${ui.selected.object_id}`;
  text.addEventListener("input", () => {
    diff.textContent = `- descrição atual\n+ ${text.value || "(vazio)"}`;
    status.textContent = "Não salvo";
  });
  $("#save-draft").addEventListener("click", () => {
    localStorage.setItem(key, text.value);
    status.textContent = "Salvo localmente";
    announce("Rascunho salvo apenas neste navegador");
  });
  $("#validate-draft").addEventListener("click", () => {
    status.textContent = "Validando…";
    text.disabled = true;
    setTimeout(() => {
      text.disabled = false;
      status.textContent = `Prévia ${text.value.trim().length >= 8 ? "válida" : "inválida"} · não autoritativa`;
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
  const usage = evidence.logical_invocation_count == null ? "Desconhecido" : evidence.logical_invocation_count;
  ui.detail = detail;
  $("#detail-body").innerHTML = `
    <article class="identity-card">
      <span class="status-pill">${esc(identity.object_kind || ui.selected.object_kind)}</span>
      <h3>${esc(identity.display_label || ui.selected.display_label)}</h3>
      <p>${esc(identity.description || "Sem descrição registrada.")}</p><code>${esc(identity.path || identity.object_id)}</code>
    </article>
    <dl class="fact-grid">
      <div><dt>Owner</dt><dd>${esc(identity.owner || "@VictorBoscaro")}</dd></div>
      <div><dt>Estado de leitura</dt><dd>${esc(detail.query_state || "success")}</dd></div>
      <div><dt>Uso observado</dt><dd>${esc(usage)}</dd></div>
      <div><dt>Freshness</dt><dd>${esc(evidence.freshness || "unknown")}</dd></div>
    </dl>
    <section data-testid="cc-evidence" class="evidence-card">
      <span aria-hidden="true">◇</span><div><b>${esc(evidenceBody.result_state)} · ${esc(evidenceClasses)}</b><p><strong>Provider:</strong> ${esc(providers.join(", ") || "não informado")}</p><p>${esc(evidenceBody.warnings?.[0] || evidence.source_facts?.[0]?.safe_reason || "Sem alerta do provider.")}</p></div>
    </section>
    ${draftMarkup(identity)}
    <section data-testid="cc-authoritative-route-unavailable" class="authority-boundary">
      <span aria-hidden="true">┆</span><div><b>Fim seguro da Fase 1</b><p>Rascunhos locais podem ser salvos e validados. Rotas autoritativas continuam indisponíveis e rastreadas em SCC-BL-001–003.</p></div>
    </section>`;
  bindDraft();
  $("#back").hidden = false;
  $(".detail-surface").scrollIntoView({behavior: "smooth", block: "start"});
  $("#detail-title").focus();
  announce("Detalhe aberto");
}

function nodeId(node) { return node.id || node.dispatch_id || node.group_id; }
function edgeEnds(edge) {
  return [edge.source_id || edge.parent_id || edge.from_group_id, edge.target_id || edge.child_id || edge.to_group_id];
}
function relationKind(edge) { return edge.edge_kind || edge.kind || "unknown"; }
function relationLabel(edge) {
  if (relationKind(edge) === "explicit_path") return "Chamada declarada";
  if (relationKind(edge) === "named_reference") return "Menção textual fraca";
  if (relationKind(edge) === "parent_dispatch_id") return "Dispatch pai";
  return relationKind(edge);
}
function renderRelationItems(edges, focusId, nodesById, direction) {
  if (!edges.length) return `<p class="call-empty">Nenhuma chamada declarada nesta direção.</p>`;
  const grouped = new Map();
  edges.forEach(edge => {
    const [from, to] = edgeEnds(edge);
    const relatedId = direction === "incoming" ? from : to;
    const key = `${relatedId}:${relationKind(edge)}`;
    if (!grouped.has(key)) grouped.set(key, {edge, relatedId, count: 0});
    grouped.get(key).count += 1;
  });
  return [...grouped.values()].map(({edge, relatedId, count}) => {
    const related = nodesById.get(relatedId);
    const label = related?.display_label || related?.label || relatedId;
    return `<button type="button" class="relation-item" data-related-id="${esc(relatedId)}"
      data-evidence-id="${esc(edge.evidence_id || "")}" data-direction="${direction}"
      data-tip="${esc(`${relationLabel(edge)} · ${direction === "incoming" ? "entra em" : "sai de"} ${focusId}`)}">
      <span class="direction-glyph" aria-hidden="true">${direction === "incoming" ? "→" : "→"}</span>
      <span><b>${esc(label)}</b><small>${esc(relationLabel(edge))}${count > 1 ? ` · ${count} evidências` : ""}</small></span>
      <span class="quiet-marker" aria-hidden="true">·</span>
    </button>`;
  }).join("");
}
function renderCallMap(data) {
  const panel = $("#call-map"), detail = $("#relationship-detail");
  detail.hidden = true;
  detail.innerHTML = "";
  ui.expandedRelationship = null;
  if (data.model && data.model !== "skill-relations") {
    panel.innerHTML = `<div class="call-disclaimer"><b>Este modelo não representa chamadas de skill.</b><p>Use “Chamadas entre skills” para responder quem chama quem.</p></div>`;
    return;
  }
  const nodes = data.nodes || [], edges = data.edges || [], focusId = data.focus_id;
  const nodesById = new Map(nodes.map(node => [nodeId(node), node]));
  const focusNode = nodesById.get(focusId);
  const incoming = edges.filter(edge => edgeEnds(edge)[1] === focusId && relationKind(edge) === "explicit_path");
  const outgoing = edges.filter(edge => edgeEnds(edge)[0] === focusId && relationKind(edge) === "explicit_path");
  const weakIncoming = edges.filter(edge => edgeEnds(edge)[1] === focusId && relationKind(edge) === "named_reference");
  const weakOutgoing = edges.filter(edge => edgeEnds(edge)[0] === focusId && relationKind(edge) === "named_reference");
  const incomingSkills = new Set(incoming.map(edge => edgeEnds(edge)[0])).size;
  const outgoingSkills = new Set(outgoing.map(edge => edgeEnds(edge)[1])).size;
  const weakSkills = new Set([...weakIncoming.map(edge => edgeEnds(edge)[0]), ...weakOutgoing.map(edge => edgeEnds(edge)[1])]).size;
  panel.innerHTML = `
    <div class="call-map-head">
      <div><span class="kicker">Direção explícita</span><h3>${esc(focusNode?.display_label || focusNode?.label || focusId)}</h3></div>
      <span class="status-pill">${incomingSkills} entram · ${outgoingSkills} saem</span>
    </div>
    <p class="call-disclaimer"><b>“Chama” significa referência explícita no source.</b> Não existe telemetria runtime suficiente para afirmar execução observada. Menções textuais ficam separadas.</p>
    <div class="call-columns">
      <section aria-labelledby="incoming-title">
        <header><span aria-hidden="true">→</span><div><h4 id="incoming-title">Quem chama esta skill</h4><small>${incomingSkills} skill(s) declarada(s)</small></div></header>
        <div class="relation-list">${renderRelationItems(incoming, focusId, nodesById, "incoming")}</div>
      </section>
      <div class="focal-skill" data-node-id="${esc(focusId)}"><span>Skill focal</span><b>${esc(focusNode?.display_label || focusId)}</b></div>
      <section aria-labelledby="outgoing-title">
        <header><span aria-hidden="true">→</span><div><h4 id="outgoing-title">O que esta skill chama</h4><small>${outgoingSkills} skill(s) declarada(s)</small></div></header>
        <div class="relation-list">${renderRelationItems(outgoing, focusId, nodesById, "outgoing")}</div>
      </section>
    </div>
    <details class="weak-relations" data-fe-rule="FE-1" ${FE_FLAGS["FE-1"] ? "" : "open"}>
      <summary>Menções fracas, não chamadas <span>${weakSkills} skills · ${weakIncoming.length + weakOutgoing.length} evidências</span></summary>
      <div class="weak-grid">
        <section><h4>Mencionada por</h4>${renderRelationItems(weakIncoming, focusId, nodesById, "incoming")}</section>
        <section><h4>Menciona</h4>${renderRelationItems(weakOutgoing, focusId, nodesById, "outgoing")}</section>
      </div>
    </details>`;
}
function showRelationship(evidenceId) {
  if (!FE_FLAGS["FE-4"]) return;
  const edge = (ui.topology?.edges || []).find(item => String(item.evidence_id || "") === evidenceId);
  if (!edge) return;
  const [from, to] = edgeEnds(edge);
  const relatedId = from === ui.topology?.focus_id ? to : from;
  const matchingEvidence = (ui.topology?.edges || []).filter(item => {
    const [itemFrom, itemTo] = edgeEnds(item);
    return itemFrom === from && itemTo === to && relationKind(item) === relationKind(edge);
  });
  const detail = $("#relationship-detail");
  ui.expandedRelationship = evidenceId;
  emitFeMetric("FE-4", "relationship-context-revealed");
  emitFeMetric("FE-6", "single-relationship-focus");
  document.querySelectorAll(".relation-item[aria-expanded]").forEach(item => item.removeAttribute("aria-expanded"));
  document.querySelectorAll(`.relation-item[data-evidence-id="${CSS.escape(evidenceId)}"]`).forEach(item => item.setAttribute("aria-expanded", "true"));
  detail.hidden = false;
  detail.setAttribute("tabindex", "-1");
  detail.innerHTML = `<button type="button" class="relationship-close" aria-label="Fechar evidência">×</button>
    <span class="kicker">Por que esta seta existe?</span>
    <h4>${esc(from)} <span aria-hidden="true">→</span> ${esc(to)}</h4>
    <dl><div><dt>Relação</dt><dd>${esc(relationLabel(edge))}</dd></div>
      <div><dt>Força</dt><dd>${relationKind(edge) === "explicit_path" ? "forte · declarada" : "fraca · menção"}</dd></div>
      <div><dt>Evidências</dt><dd>${matchingEvidence.map(item => `<code>${esc(item.evidence_id || "não informada")}</code>`).join("")}</dd></div></dl>
    <button type="button" class="relationship-focus secondary" data-related-id="${esc(relatedId)}">Centralizar ${esc(relatedId)}</button>`;
  detail.focus?.();
}
function closeRelationshipDetail() {
  const detail = $("#relationship-detail");
  if (detail.hidden) return;
  detail.hidden = true;
  emitFeMetric("FE-3", "instant-dismiss");
  ui.expandedRelationship = null;
  document.querySelectorAll(".relation-item[aria-expanded]").forEach(item => item.removeAttribute("aria-expanded"));
}
function renderTopology(data) {
  const nodes = data?.nodes || [], edges = data?.edges || [];
  $("#topology-meta").textContent = `${nodes.length} nós · ${edges.length} relações`;
  if (!nodes.length) {
    $("#graph").innerHTML = `<div class="zero-state"><b>Nenhuma relação</b><p>Esta visão limitada não encontrou conexões.</p></div>`;
    $("#call-map").innerHTML = `<div class="zero-state"><b>Nenhuma chamada declarada</b><p>A ausência vale apenas para a cobertura informada.</p></div>`;
    $("#topology-table").innerHTML = `<tr><td colspan="3">Nenhuma relação.</td></tr>`;
    return;
  }
  const width = 720, height = 390, positions = new Map();
  const focusId = data.focus_id;
  if (data.model === "skill-relations" || edges.some(edge => ["explicit_path", "named_reference"].includes(relationKind(edge)))) {
    const incomingIds = [...new Set(edges.filter(edge => edgeEnds(edge)[1] === focusId).map(edge => edgeEnds(edge)[0]))];
    const outgoingIds = [...new Set(edges.filter(edge => edgeEnds(edge)[0] === focusId).map(edge => edgeEnds(edge)[1]))];
    positions.set(focusId, {x: 360, y: 195});
    incomingIds.forEach((id, index) => positions.set(id, {x: 105, y: 55 + index * (280 / Math.max(incomingIds.length - 1, 1))}));
    outgoingIds.forEach((id, index) => {
      if (!positions.has(id)) positions.set(id, {x: 615, y: 55 + index * (280 / Math.max(outgoingIds.length - 1, 1))});
    });
    const unplaced = nodes.filter(node => !positions.has(nodeId(node)));
    unplaced.forEach((node, index) => positions.set(nodeId(node), {x: 260 + index * 100, y: 350}));
  } else {
    nodes.forEach((node, index) => {
      const columns = variant === "B" ? 3 : variant === "C" ? 2 : 5;
      const col = index % columns, row = Math.floor(index / columns);
      positions.set(nodeId(node), {x: 90 + col * (540 / Math.max(columns - 1, 1)), y: 70 + row * 92});
    });
  }
  const lines = edges.map(edge => {
    const [from, to] = edgeEnds(edge), a = positions.get(from), b = positions.get(to);
    const direction = to === focusId ? "incoming" : from === focusId ? "outgoing" : "other";
    if (!a || !b) return "";
    const dx = b.x - a.x, dy = b.y - a.y, distance = Math.max(Math.hypot(dx, dy), 1);
    const start = {x: a.x + dx / distance * 72, y: a.y + dy / distance * 22};
    const end = {x: b.x - dx / distance * 78, y: b.y - dy / distance * 24};
    return `<path data-evidence-id="${esc(edge.evidence_id || "")}" data-direction="${direction}"
      class="edge ${relationKind(edge) === "named_reference" ? "mention" : ""}"
      marker-end="url(#arrow-${variant})" d="M${start.x},${start.y} C${(a.x+b.x)/2},${start.y} ${(a.x+b.x)/2},${end.y} ${end.x},${end.y}"/>`;
  }).join("");
  const points = nodes.map(node => {
    const id = nodeId(node), p = positions.get(id), focus = id === data.focus_id;
    const label = String(node.display_label || node.label || id);
    return `<g data-node-id="${esc(id)}" data-tip="${esc(focus ? "Skill focal" : "Clique para centralizar esta skill")}"
      class="graph-node ${focus ? "focus" : ""}" tabindex="0" role="button" aria-label="${esc(`${label}${focus ? ", skill focal" : ", centralizar no mapa"}`)}">
      <rect x="${p.x-70}" y="${p.y-20}" width="140" height="40" rx="10"/><text x="${p.x}" y="${p.y+4}" text-anchor="middle">${esc(label.slice(0, 19))}</text></g>`;
  }).join("");
  $("#graph").innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Mapa direcional: entradas à esquerda, skill focal ao centro e saídas à direita">
    <defs><marker id="arrow-${variant}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs>
    <text class="graph-axis-label" x="24" y="24">REFERÊNCIAS QUE ENTRAM</text><text class="graph-axis-label" x="555" y="24">REFERÊNCIAS QUE SAEM</text>${lines}${points}</svg>`;
  renderCallMap({...data, nodes, edges});
  $("#topology-table").innerHTML = edges.length ? edges.map(edge => {
    const [from, to] = edgeEnds(edge);
    return `<tr data-evidence-id="${esc(edge.evidence_id || "")}"><td>${esc(from)}</td><td>${esc(relationLabel(edge))}</td><td>${esc(to)}</td></tr>`;
  }).join("") : nodes.map(node => `<tr><td>${esc(nodeId(node))}</td><td>Nó focal</td><td>—</td></tr>`).join("");
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
  ui.topology = {...body.data, model};
  renderTopology(ui.topology);
  $(".topology-surface").scrollIntoView({behavior: "smooth", block: "start"});
  announce(model === "skill-relations" ? "Mapa de chamadas carregado" : "Topologia carregada");
}

async function focusRelatedSkill(id) {
  if (!id || id === ui.selected?.object_id || $("#model").value !== "skill-relations") return;
  const node = (ui.topology?.nodes || []).find(item => nodeId(item) === id);
  clearDependent("A skill focal mudou; a vizinhança anterior foi recolhida.");
  ui.selected = {
    object_kind: "skill",
    object_id: id,
    display_label: node?.display_label || node?.label || id,
  };
  $("#selection").textContent = `skill · ${ui.selected.display_label}`;
  ["#open-detail", "#open-topology", "#load-topology"].forEach(selector => $(selector).disabled = false);
  $("#path-source").value = id;
  await loadTopology();
}

let explainTimer;
function hideExplainTooltip() {
  clearTimeout(explainTimer);
  $("#tt").hidden = true;
}
function scheduleExplainTooltip(target) {
  if (!FE_FLAGS["FE-2"] || !FE_FLAGS["FE-9"] || !ui.explainMode || !target?.dataset?.tip) return;
  clearTimeout(explainTimer);
  explainTimer = setTimeout(() => {
    const tooltip = $("#tt"), rect = target.getBoundingClientRect();
    tooltip.textContent = target.dataset.tip;
    tooltip.style.left = `${Math.min(window.innerWidth - 280, Math.max(12, rect.left))}px`;
    tooltip.style.top = `${Math.min(window.innerHeight - 90, rect.bottom + 8)}px`;
    tooltip.hidden = false;
    emitFeMetric("FE-2", "secondary-context-revealed");
    emitFeMetric("FE-9", "dwell-explanation-revealed");
  }, 3000);
}

$("#theme-select").addEventListener("change", event => setPreference("theme", event.target.value));
$("#density-select").addEventListener("change", event => setPreference("density", event.target.value));
$("#search-form").addEventListener("submit", event => { event.preventDefault(); ui.query = $("#search").value.trim(); loadCatalog(); announce("Busca atualizada"); });
$("#filters").addEventListener("change", event => { ui.kind = event.target.value; ui.selected = null; clearDependent("O filtro mudou; selecione uma nova identidade."); $("#selection").textContent = "Nada selecionado"; ["#open-detail","#open-topology","#load-topology"].forEach(s => $(s).disabled = true); loadCatalog(); });
$("#catalog-list").addEventListener("click", event => { const row = event.target.closest(".catalog-item"); if (row) selectObject(row.dataset.id); });
$("#catalog-list").addEventListener("keydown", event => { const row = event.target.closest(".catalog-item"); if (row && ["Enter"," "].includes(event.key)) { event.preventDefault(); selectObject(row.dataset.id); } });
$("#open-detail").addEventListener("click", () => openDetail().catch(error => announce(error.message)));
$("#open-topology").addEventListener("click", () => loadTopology().catch(error => announce(error.message)));
$("#load-topology").addEventListener("click", () => loadTopology().catch(error => announce(error.message)));
$("#back").addEventListener("click", () => { $(".catalog-surface").scrollIntoView(); document.querySelector(`.catalog-item[data-id="${CSS.escape(ui.selected.object_id)}"]`)?.focus(); });
$("#call-map").addEventListener("click", event => {
  const relation = event.target.closest(".relation-item");
  if (relation) showRelationship(relation.dataset.evidenceId);
});
$("#call-map").addEventListener("toggle", event => {
  if (event.target.matches(".weak-relations")) emitFeMetric("FE-1", event.target.open ? "structure-expanded" : "structure-collapsed");
}, true);
$("#relationship-detail").addEventListener("click", event => {
  const focus = event.target.closest(".relationship-focus");
  if (focus) {
    focusRelatedSkill(focus.dataset.relatedId).catch(error => announce(error.message));
    return;
  }
  if (!event.target.closest(".relationship-close")) return;
  closeRelationshipDetail();
});
$("#graph").addEventListener("click", event => {
  const node = event.target.closest(".graph-node");
  if (node) focusRelatedSkill(node.dataset.nodeId).catch(error => announce(error.message));
});
$("#graph").addEventListener("keydown", event => {
  const node = event.target.closest(".graph-node");
  if (node && ["Enter", " "].includes(event.key)) {
    event.preventDefault();
    focusRelatedSkill(node.dataset.nodeId).catch(error => announce(error.message));
  }
});
$("#explain-toggle").addEventListener("click", event => {
  ui.explainMode = !ui.explainMode;
  emitFeMetric("FE-9", ui.explainMode ? "explain-mode-enabled" : "explain-mode-disabled");
  event.currentTarget.setAttribute("aria-pressed", String(ui.explainMode));
  event.currentTarget.textContent = ui.explainMode ? "Explicação ativa" : "? Explicar";
  hideExplainTooltip();
  announce(ui.explainMode ? "Modo de explicação ativo: mantenha o ponteiro por 3 segundos." : "Modo de explicação desativado.");
});
document.addEventListener("pointerover", event => scheduleExplainTooltip(event.target.closest("[data-tip]")));
document.addEventListener("pointerout", event => { if (event.target.closest("[data-tip]")) hideExplainTooltip(); });
document.addEventListener("focusin", event => scheduleExplainTooltip(event.target.closest("[data-tip]")));
document.addEventListener("focusout", hideExplainTooltip);
document.addEventListener("click", event => {
  if (!event.target.closest(".relation-item, #relationship-detail")) closeRelationshipDetail();
});
document.addEventListener("keydown", event => {
  if (event.key !== "Escape") return;
  hideExplainTooltip();
  closeRelationshipDetail();
});
$("#path-form").addEventListener("submit", async event => {
  event.preventDefault();
  emitFeMetric("FE-7", "bounded-path-query");
  const requestedIdentity = `${ui.selected?.object_kind}:${ui.selected?.object_id}`;
  const model = $("#model").value;
  const payload = {...requestBase, model, source_id: $("#path-source").value.trim(), target_id: $("#path-target").value.trim(), direction: "outbound", allowed_edge_kinds: model === "skill-relations" ? ["explicit_path","named_reference"] : model === "dispatch-lineage" ? ["parent_dispatch_id"] : ["sequential","zig-zag","feedback"], max_depth: 4, max_paths: Number($("#path-limit").value)};
  if (model === "intra-dispatch") payload.dispatch_id = ui.selected?.object_id;
  try {
    const response = await fetch(`${API}/path-query`, {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify(payload)});
    const body = await response.json(), data = body.data || {};
    if (`${ui.selected?.object_kind}:${ui.selected?.object_id}` !== requestedIdentity) return;
    renderPathResult(data);
    announce("Consulta de caminho concluída");
  } catch (error) {
    if (`${ui.selected?.object_kind}:${ui.selected?.object_id}` === requestedIdentity) $("#path-result").textContent = `Consulta de caminho indisponível: ${error.message}`;
  }
});
function renderPathResult(data) {
  document.querySelectorAll(".path-hit").forEach(node => node.classList.remove("path-hit"));
  const paths = data.paths || [], limited = data.query_state === "truncated" || data.more_paths_exist;
  if (!["success", "truncated"].includes(data.query_state) || !paths.length) {
    $("#path-result").innerHTML = `<b>${esc(data.query_state || "unavailable")}</b><p>Nenhum caminho afirmado além da cobertura e dos limites declarados.</p>`;
    return;
  }
  const evidenceIds = new Set(), nodeIds = new Set();
  paths.forEach(path => {
    (path.edges || []).forEach(edge => evidenceIds.add(edge.evidence_id));
    (path.node_ids || []).forEach(id => nodeIds.add(id));
  });
  document.querySelectorAll("[data-evidence-id]").forEach(node => { if (evidenceIds.has(node.dataset.evidenceId)) node.classList.add("path-hit"); });
  document.querySelectorAll("[data-node-id]").forEach(node => { if (nodeIds.has(node.dataset.nodeId)) node.classList.add("path-hit"); });
  $("#path-result").innerHTML = `<b>${paths.length} caminho(s) ordenado(s)${limited ? " · truncado pelo limite declarado" : ""}</b><ol>${paths.map(path => `<li><span>${path.node_ids.map(esc).join(" → ")}</span>${path.edges.map(edge => `<code>${esc(edge.evidence_id)}</code>`).join("")}</li>`).join("")}</ol>`;
}

if (forcedState) {
  renderFixtureState(forcedState);
  $("#attention-count").textContent = "fixture";
  $("#result-count").textContent = "fixture";
  $("#source-health").innerHTML = `<span aria-hidden="true">◇</span> Deterministic evidence state`;
} else {
  Promise.all([loadAttention(), loadCatalog()]).then(() => announce("Control Center pronto"));
}
