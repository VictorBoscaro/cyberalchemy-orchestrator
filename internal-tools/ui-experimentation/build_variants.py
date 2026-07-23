# -*- coding: utf-8 -*-
"""
build_variants.py — emit the 10 standalone HTML viewers into variants/.

Every variant shares ONE behavioral engine (so CONST-FE behavior is identical
across all 10): FE-1 density opt-in, FE-2 single #tt/data-tip tooltip system,
FE-3 instant Esc/outside-click dismiss, FE-5 loading/error/empty(pt-BR) states,
FE-6 one focus at a time, FE-9 discreet explain-mode marker.

What differs per variant is FORM ONLY: a unique CSS theme + one of six graph
geometries (columns / rows / radial / orbit / timeline / scatter). This is the
anti-bias axis of the whole build: aesthetic diversity  ⊥  behavioral consistency.

Run: python build_variants.py   (writes variants/*.html + index.html)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VARIANTS = os.path.join(HERE, "variants")

# --------------------------------------------------------------------------- #
# Shared body markup (identical structural contract across all 10 variants).
# --------------------------------------------------------------------------- #
BODY = r"""
<div id="app">
  <aside id="sidebar">
    <div class="side-head">
      <h1 id="brand"></h1>
      <p id="tagline">Dispatches com estrutura de grafo. Fuso: UTC.</p>
    </div>
    <div id="states">
      <div id="st-loading" class="state">Carregando dispatches…</div>
      <div id="st-error" class="state" hidden>
        <p>Nao foi possivel carregar os dados.</p>
        <button id="retry" type="button">Tentar novamente</button>
      </div>
      <div id="st-empty" class="state" hidden>Nenhum dispatch com estrutura para inspecionar.</div>
    </div>
    <ul id="dlist" aria-label="Dispatches estruturados"></ul>
  </aside>

  <main id="main">
    <div id="stage-head">
      <span id="stage-title">Selecione um dispatch</span>
      <span id="stage-meta"></span>
    </div>
    <div id="stage-wrap">
      <div id="stage-empty">Escolha um dispatch a esquerda para ver o grafo dos agentes.</div>
      <svg id="edges" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"></svg>
      <div id="nodes"></div>
      <div id="legend"><span class="dot rev"></span>revisor / cetico / auditor<span class="mark">?</span></div>
    </div>
  </main>
</div>

<div id="scrim" hidden></div>
<aside id="panel" hidden role="dialog" aria-modal="true" aria-labelledby="p-name">
  <button id="p-close" type="button" aria-label="Fechar">&times;</button>
  <div class="p-role" id="p-role"></div>
  <h2 id="p-name"></h2>
  <dl class="p-meta" id="p-meta"></dl>
  <div class="p-angle" id="p-angle-wrap" hidden>
    <div class="p-lbl">Angulo / tensao</div>
    <p id="p-angle"></p>
  </div>
  <div class="p-prompt">
    <button id="p-prompt-toggle" type="button" aria-expanded="false">Revelar prompt inicial completo</button>
    <div id="p-prompt-body" hidden></div>
  </div>
</aside>

<div id="tt" role="tooltip" hidden></div>
<button id="explain" type="button" title="Modo explicacao" aria-pressed="false">?</button>
"""

# --------------------------------------------------------------------------- #
# Shared engine JS (behavior; CONST-FE). Layout is chosen by window.__V__.layout.
# --------------------------------------------------------------------------- #
ENGINE = r"""
(function () {
  "use strict";
  var V = window.__V__ || { layout: "columns" };
  var REV = { skeptic: 1, auditor: 1, reviewer: 1 };
  var $ = function (id) { return document.getElementById(id); };
  var state = { data: null, current: null, focusEl: null };

  // ---- data load: fetch json (served) with file:// script fallback -------
  function load() {
    show("st-loading");
    fetch("../data/dispatches.json")
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(ready)
      .catch(function () {
        if (window.__DISPATCHES__) { ready(window.__DISPATCHES__); }
        else { show("st-error"); }
      });
  }
  function show(id) {
    ["st-loading", "st-error", "st-empty"].forEach(function (s) {
      var el = $(s); if (el) el.hidden = (s !== id);
    });
  }
  function ready(payload) {
    state.data = (payload && payload.dispatches) || [];
    if (!state.data.length) { show("st-empty"); return; }
    show("__none__");
    renderList();
  }

  // ---- helpers -----------------------------------------------------------
  function agentsOf(d) {
    var out = [];
    (d.groups || []).forEach(function (g) {
      (g.agents || []).forEach(function (a) { out.push({ a: a, g: g }); });
    });
    return out;
  }
  function isRev(a) { return !!REV[(a.role || "").toLowerCase()]; }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function nameOf(a) { return a.agent_name || "(sem nome)"; }

  // ---- dispatch list -----------------------------------------------------
  function renderList() {
    var ul = $("dlist");
    ul.innerHTML = "";
    state.data.forEach(function (d, i) {
      var ags = agentsOf(d);
      var revs = ags.filter(function (x) { return isRev(x.a); }).length;
      var li = document.createElement("li");
      li.className = "ditem";
      li.tabIndex = 0;
      li.setAttribute("data-tip", (d.anti_bias_global || (d.groups[0] && d.groups[0].anti_bias) || "sem eixo anti-vies declarado"));
      li.innerHTML =
        '<span class="dtype t-' + esc(d.dispatch_type) + '">' + esc(d.dispatch_type) + "</span>" +
        '<span class="dgoal">' + esc(shorten(d.goal, 96)) + "</span>" +
        '<span class="dstat">' + ags.length + " ag · " + (d.groups.length) + " grp · " +
        (d.connections ? d.connections.length : 0) + " liga · " + revs + " rev</span>";
      li.addEventListener("click", function () { pick(i, li); });
      li.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(i, li); }
      });
      ul.appendChild(li);
    });
  }
  function shorten(s, n) { s = s || ""; return s.length > n ? s.slice(0, n - 1) + "…" : s; }

  function pick(i, li) {
    state.current = state.data[i];
    var prev = document.querySelector(".ditem.sel");
    if (prev) prev.classList.remove("sel");
    if (li) li.classList.add("sel");
    closePanel();
    renderGraph(state.current);
  }

  // ---- geometry: returns {nodes:[{id,type,x,y,label,agent,group,rev}], edges:[{x1,y1,x2,y2,tip}]}
  function geometry(d) {
    var groups = d.groups || [], G = groups.length;
    var nodes = [], gpos = {}, i, j;
    var lay = V.layout;

    function place(gi, group) {
      var agents = group.agents || [], n = agents.length;
      var gx, gy, cx, cy;
      if (lay === "columns") {
        gx = (gi + 1) / (G + 1) * 100; gy = 9; cx = gx; cy = 55;
        nodes.push(gnode(group, gx, gy));
        agents.forEach(function (a, ai) {
          var ay = 24 + (ai + 0.5) / n * 70; anode(a, group, gx, ay);
        });
      } else if (lay === "rows") {
        gy = (gi + 1) / (G + 1) * 100; gx = 8; cx = 55; cy = gy;
        nodes.push(gnode(group, gx, gy));
        agents.forEach(function (a, ai) {
          var ax = 22 + (ai + 0.5) / n * 74; anode(a, group, ax, gy);
        });
      } else if (lay === "radial") {
        var ang = gi / G * 2 * Math.PI - Math.PI / 2;
        cx = 50 + 33 * Math.cos(ang); cy = 50 + 33 * Math.sin(ang);
        nodes.push(gnode(group, cx, cy));
        agents.forEach(function (a, ai) {
          var aa = ai / Math.max(1, n) * 2 * Math.PI;
          var r = n === 1 ? 0 : 11;
          anode(a, group, cx + r * Math.cos(aa), cy + r * Math.sin(aa));
        });
      } else if (lay === "orbit") {
        var rad = 10 + gi * (40 / Math.max(1, G));
        cx = 50; cy = 50 - rad;
        nodes.push(gnode(group, cx, cy));
        agents.forEach(function (a, ai) {
          var oa = (ai + 0.5) / n * 2 * Math.PI - Math.PI / 2;
          anode(a, group, 50 + rad * Math.cos(oa), 50 + rad * Math.sin(oa));
        });
      } else if (lay === "timeline") {
        gx = (gi + 1) / (G + 1) * 100; cx = gx; cy = 50;
        nodes.push(gnode(group, gx, 50));
        agents.forEach(function (a, ai) {
          var side = ai % 2 ? 1 : -1;
          var step = Math.floor(ai / 2) + 1;
          anode(a, group, gx, 50 + side * step * (34 / (Math.floor(n / 2) + 1)));
        });
      } else { // scatter — use unsigned shifts so positions never go negative
        var h = hash(group.group_id + gi);
        cx = clamp(18 + (h % 64)); cy = clamp(16 + ((h >>> 3) % 62));
        nodes.push(gnode(group, cx, cy));
        agents.forEach(function (a, ai) {
          var hh = hash((a.agent_name || "") + group.group_id + ai);
          anode(a, group, clamp(cx + ((hh % 24) - 12)), clamp(cy + (((hh >>> 4) % 24) - 12)));
        });
      }
      gpos[group.group_id] = { x: cx, y: cy };
    }
    function gnode(group, x, y) {
      return { id: "g:" + group.group_id, type: "group", x: x, y: y,
        label: group.group_id, group: group,
        tip: group.anti_bias ? ("anti-vies: " + group.anti_bias) : ("grupo · " + (group.n || (group.agents || []).length) + " agente(s)") };
    }
    function anode(a, group, x, y) {
      nodes.push({ id: "a:" + group.group_id + ":" + nodes.length, type: "agent",
        x: clamp(x), y: clamp(y), label: nameOf(a), agent: a, group: group, rev: isRev(a),
        tip: (a.role || "agente") + (a.model ? (" · " + a.model) : "") });
    }
    for (i = 0; i < G; i++) place(i, groups[i]);

    var edges = [];
    (d.connections || []).forEach(function (c) {
      var f = gpos[c.from], t = gpos[c.to];
      if (f && t) edges.push({ x1: f.x, y1: f.y, x2: t.x, y2: t.y, tip: "aresta " + (c.type || "?") + ": " + c.from + " → " + c.to, type: c.type });
    });
    return { nodes: nodes, edges: edges };
  }
  function clamp(v) { return Math.max(6, Math.min(94, v)); }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = (h * 16777619) >>> 0; } return h; }

  // ---- render graph ------------------------------------------------------
  function renderGraph(d) {
    $("stage-empty").hidden = true;
    $("stage-title").textContent = d.dispatch_id;
    $("stage-meta").textContent = d.dispatch_type + " · " + (d.created ? d.created.slice(0, 10) : "");
    var geo = geometry(d);
    var svg = $("edges"); svg.innerHTML = "";
    geo.edges.forEach(function (e) {
      var mx = (e.x1 + e.x2) / 2, my = (e.y1 + e.y2) / 2 - 8;
      var p = document.createElementNS("http://www.w3.org/2000/svg", "path");
      p.setAttribute("d", "M" + e.x1 + " " + e.y1 + " Q " + mx + " " + my + " " + e.x2 + " " + e.y2);
      p.setAttribute("class", "edge edge-" + (e.type || "x"));
      p.setAttribute("fill", "none");
      p.setAttribute("vector-effect", "non-scaling-stroke");
      p.setAttribute("data-tip", e.tip);
      svg.appendChild(p);
    });
    var host = $("nodes"); host.innerHTML = "";
    geo.nodes.forEach(function (nd) {
      var el = document.createElement("div");
      el.className = "node " + nd.type + (nd.rev ? " rev" : "");
      el.style.left = nd.x + "%"; el.style.top = nd.y + "%";
      el.setAttribute("data-tip", nd.tip);
      el.setAttribute("data-explain", nd.type === "group"
        ? "Grupo de agentes. O eixo anti-vies opoe os angulos para cancelar erro correlacionado."
        : (nd.rev ? "No de revisor/cetico/auditor: julga o trabalho ligado por aresta." : "Agente. Clique para ver prompt, angulo, papel, modelo e orcamento."));
      el.innerHTML = nd.type === "group"
        ? '<span class="g-label">' + esc(nd.label) + "</span>"
        : '<span class="n-role">' + esc((nd.agent.role || "?")).slice(0, 3) + "</span>" +
          '<span class="n-name">' + esc(nd.label) + "</span>";
      if (nd.type === "agent") {
        el.tabIndex = 0;
        el.addEventListener("click", function () { openPanel(nd.agent, nd.group, el); });
        el.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openPanel(nd.agent, nd.group, el); }
        });
      }
      host.appendChild(el);
    });
  }

  // ---- agent panel (FE-1 opt-in prompt, FE-6 single focus) --------------
  function openPanel(a, g, el) {
    closePanel();
    state.focusEl = el; if (el) el.classList.add("active");
    $("p-role").textContent = (a.role || "agente") + (isRev(a) ? " • revisor" : "");
    $("p-role").className = "p-role" + (isRev(a) ? " is-rev" : "");
    $("p-name").textContent = nameOf(a);
    var meta = $("p-meta"); meta.innerHTML = "";
    [["modelo", a.model], ["orcamento", a.token_budget != null ? (a.token_budget + " tok") : null],
     ["grupo", g.group_id]].forEach(function (kv) {
      if (kv[1] == null || kv[1] === "") return;
      meta.innerHTML += "<dt>" + esc(kv[0]) + "</dt><dd>" + esc(kv[1]) + "</dd>";
    });
    var aw = $("p-angle-wrap");
    if (a.angle) { aw.hidden = false; $("p-angle").textContent = a.angle; } else { aw.hidden = true; }
    var body = $("p-prompt-body"), tog = $("p-prompt-toggle");
    body.textContent = a.initial_prompt || "(sem prompt inicial registrado)";
    body.hidden = true; tog.setAttribute("aria-expanded", "false");
    tog.textContent = "Revelar prompt inicial completo";
    $("scrim").hidden = false; $("panel").hidden = false;
    $("panel").scrollTop = 0;
  }
  function closePanel() {
    $("panel").hidden = true; $("scrim").hidden = true;
    if (state.focusEl) { state.focusEl.classList.remove("active"); state.focusEl = null; }
  }

  // ---- tooltip system (FE-2: one #tt + data-tip) -------------------------
  function initTooltip() {
    var tt = $("tt"), on = false;
    document.addEventListener("mouseover", function (e) {
      // FE-9: inside explain-mode a node reveals "what it is + why it matters";
      // otherwise the universal FE-2 tooltip shows secondary/qualifier info.
      var xp = document.body.classList.contains("explain");
      var t = e.target.closest ? e.target.closest(xp ? "[data-explain],[data-tip]" : "[data-tip]") : null;
      if (!t) return;
      var txt = (xp && t.getAttribute("data-explain")) || t.getAttribute("data-tip");
      if (txt) { tt.textContent = txt; tt.hidden = false; on = true; place(e); }
    });
    document.addEventListener("mousemove", function (e) { if (on) place(e); });
    document.addEventListener("mouseout", function (e) {
      var t = e.target.closest ? e.target.closest("[data-tip]") : null;
      if (t) { tt.hidden = true; on = false; }
    });
    function place(e) {
      var x = e.clientX + 14, y = e.clientY + 16;
      if (x + 260 > innerWidth) x = e.clientX - 260;
      if (y + 60 > innerHeight) y = e.clientY - 50;
      tt.style.left = x + "px"; tt.style.top = y + "px";
    }
  }

  // ---- wire-up -----------------------------------------------------------
  function init() {
    document.body.classList.add(V.bodyClass || "");
    $("brand").textContent = V.brand || "Dispatch Viewer";
    $("retry").addEventListener("click", load);
    $("p-close").addEventListener("click", closePanel);
    $("scrim").addEventListener("click", closePanel);   // FE-3 instant outside-click
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closePanel(); }); // FE-3 Esc
    $("p-prompt-toggle").addEventListener("click", function () {   // FE-1 opt-in density
      var b = $("p-prompt-body"), open = b.hidden;
      b.hidden = !open;
      this.setAttribute("aria-expanded", String(open));
      this.textContent = open ? "Ocultar prompt inicial" : "Revelar prompt inicial completo";
    });
    $("explain").addEventListener("click", function () {          // FE-9 discreet explain-mode
      var on = document.body.classList.toggle("explain");
      this.setAttribute("aria-pressed", String(on));
    });
    initTooltip();
    load();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
"""

# --------------------------------------------------------------------------- #
# Shared base CSS (structure only; each theme overrides look heavily).
# --------------------------------------------------------------------------- #
BASE_CSS = r"""
*{box-sizing:border-box}
html,body{height:100%;margin:0}
#app{display:grid;grid-template-columns:320px 1fr;height:100vh;overflow:hidden}
#sidebar{display:flex;flex-direction:column;min-height:0;overflow:hidden}
.side-head{padding:18px 18px 10px}
#brand{margin:0;font-size:18px;letter-spacing:.02em}
#tagline{margin:4px 0 0;font-size:11px;opacity:.7}
#states .state{padding:14px 18px;font-size:13px}
#dlist{list-style:none;margin:0;padding:0 10px 24px;overflow:auto;flex:1;min-height:0}
.ditem{padding:11px 12px;margin:7px 0;cursor:pointer;display:flex;flex-direction:column;gap:5px}
.dtype{font-size:10px;text-transform:uppercase;letter-spacing:.12em;align-self:flex-start}
.dgoal{font-size:13px;line-height:1.35}
.dstat{font-size:10.5px;opacity:.62;letter-spacing:.03em}
#main{position:relative;display:flex;flex-direction:column;min-width:0;overflow:hidden}
#stage-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:14px 20px}
#stage-title{font-size:14px;font-weight:600}
#stage-meta{font-size:11px;opacity:.6}
#stage-wrap{position:relative;flex:1;margin:0 18px 18px;overflow:hidden}
#stage-empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:40px;font-size:14px;opacity:.6}
#edges{position:absolute;inset:0;width:100%;height:100%}
.edge{stroke-width:1.6px;opacity:.85}
#nodes{position:absolute;inset:0}
.node{position:absolute;transform:translate(-50%,-50%);cursor:default;user-select:none;text-align:center}
.node.agent{cursor:pointer}
.node .g-label{font-size:11px;letter-spacing:.04em}
.node .n-role{display:block;font-size:9px;text-transform:uppercase;opacity:.7}
.node .n-name{display:block;font-size:11px;line-height:1.1}
#legend{position:absolute;left:10px;bottom:8px;font-size:10.5px;opacity:.6;display:flex;align-items:center;gap:6px}
#legend .dot{width:9px;height:9px;border-radius:50%;display:inline-block}
#legend .mark{margin-left:auto;opacity:.5}
#scrim{position:fixed;inset:0;background:rgba(4,6,12,.5);backdrop-filter:blur(2px);z-index:40}
#panel{position:fixed;top:0;right:0;height:100vh;width:min(460px,92vw);z-index:50;overflow:auto;padding:26px 26px 40px}
#p-close{position:absolute;top:14px;right:16px;border:0;background:none;font-size:26px;line-height:1;cursor:pointer;color:inherit}
.p-role{font-size:11px;text-transform:uppercase;letter-spacing:.14em;opacity:.7}
#p-name{margin:6px 0 16px;font-size:22px;word-break:break-word}
.p-meta{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0 0 18px;font-size:12.5px}
.p-meta dt{opacity:.55;text-transform:uppercase;font-size:10px;letter-spacing:.08em;align-self:center}
.p-meta dd{margin:0}
.p-angle{margin:0 0 18px}
.p-lbl{font-size:10px;text-transform:uppercase;letter-spacing:.1em;opacity:.6;margin-bottom:5px}
.p-angle p{margin:0;font-size:13.5px;line-height:1.5}
.p-prompt button{width:100%;text-align:left;padding:11px 13px;font:inherit;font-size:12.5px;cursor:pointer}
#p-prompt-body{margin-top:12px;font-size:13px;line-height:1.62;white-space:pre-wrap;word-break:break-word}
#tt{position:fixed;z-index:60;max-width:250px;padding:7px 10px;font-size:11.5px;line-height:1.4;pointer-events:none;border-radius:5px;background:#0b0f1a;color:#e9edf6;box-shadow:0 6px 22px rgba(0,0,0,.4)}
#explain{position:fixed;right:16px;bottom:16px;z-index:35;width:32px;height:32px;border-radius:50%;cursor:pointer;font-weight:700;opacity:.5;border:1px solid currentColor;background:transparent;color:inherit}
#explain[aria-pressed="true"]{opacity:1}
body:not(.explain) .node[data-explain]::after{display:none}
body.explain .node{outline:1px dashed rgba(127,127,127,.5)}
"""

PAGE = """<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<script src="../data/dispatches.js" onerror="void 0"></script>
<script>window.__V__={{layout:"{layout}",brand:{brand!r},bodyClass:"{bodyclass}"}};</script>
<style>
{base}
/* ---- theme: {vid} ---- */
{theme}
</style>
</head><body>
{body}
<script>
{engine}
</script>
</body></html>
"""

# --------------------------------------------------------------------------- #
# 10 themes. Each: id, title, brand, layout geometry, one-liner, CSS theme.
# --------------------------------------------------------------------------- #
THEMES = []

def T(vid, title, brand, layout, oneline, css):
    THEMES.append(dict(vid=vid, title=title, brand=brand, layout=layout, oneline=oneline, css=css))

# 1. BLUEPRINT — cyan technical drawing on navy grid, orthogonal feel.
T("blueprint", "Blueprint · Dispatch Graph", "BLUEPRINT", "columns",
  "planta tecnica: ciano sobre azul-marinho, grade milimetrada, nos como cotas",
r"""
body{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;color:#bfe6ff;
  background:#0a1f33;background-image:linear-gradient(rgba(120,200,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(120,200,255,.07) 1px,transparent 1px);background-size:22px 22px}
#sidebar{background:rgba(6,20,34,.85);border-right:1px solid #1d4d6e}
#brand{color:#7fd8ff;font-weight:600}
.ditem{border:1px solid #17415e;background:rgba(10,40,62,.5)}
.ditem:hover,.ditem.sel{border-color:#57d0ff;background:rgba(20,70,100,.6)}
.dtype{color:#5fb6e0}
.node.group{padding:5px 9px;border:1px dashed #4aa9d8;color:#9fe4ff;background:rgba(8,30,48,.8)}
.node.agent{padding:7px 9px;border:1px solid #2f7ba6;background:#0c2b42;box-shadow:0 0 0 3px rgba(10,31,51,.9)}
.node.agent:hover,.node.agent.active{border-color:#7fe3ff;box-shadow:0 0 14px rgba(90,210,255,.5)}
.node.agent.rev{border-color:#ffcf5f;color:#ffe6a8}
.edge{stroke:#4aa9d8}
#legend .dot.rev{background:#ffcf5f}
#panel{background:#0a2136;border-left:1px solid #2f7ba6;color:#cdeeff}
.p-prompt button{border:1px solid #2f7ba6;background:#0c2b42;color:#bfe6ff}
#p-name{color:#8fe4ff}
""")

# 2. EDITORIAL — newspaper serif, ink on cream, ruled columns.
T("editorial", "Editorial · The Dispatch Ledger", "THE DISPATCH LEDGER", "rows",
  "jornal impresso: serifada, tinta sobre creme, fios e capitulares, grafo em faixas",
r"""
body{font-family:Georgia,"Times New Roman",serif;color:#20180f;background:#f4efe3}
#sidebar{background:#efe8d8;border-right:2px solid #20180f}
.side-head{border-bottom:3px double #20180f}
#brand{font-weight:700;font-variant:small-caps;letter-spacing:.06em;text-align:center}
#tagline{text-align:center;font-style:italic}
.ditem{border-bottom:1px solid #c9bfa6}
.ditem:hover,.ditem.sel{background:#e6dcc2}
.dtype{font-style:italic;font-variant:small-caps;color:#7a5a2a;letter-spacing:.02em}
.dgoal{font-size:14px}
#stage-title{font-variant:small-caps;letter-spacing:.05em}
.node.group{font-variant:small-caps;font-weight:700;border-bottom:2px solid #20180f;padding:2px 6px}
.node.agent{padding:6px 10px;background:#fbf7ec;border:1px solid #20180f;box-shadow:3px 3px 0 #d8cdb0}
.node.agent:hover,.node.agent.active{background:#fff;box-shadow:3px 3px 0 #b59a63}
.node.agent.rev{border-width:2px;background:#f6ecd6}
.node .n-role{font-style:italic;text-transform:none;opacity:.75}
.edge{stroke:#5a4a30;stroke-dasharray:1 3}
#legend .dot.rev{background:#7a5a2a}
#panel{background:#f8f3e7;border-left:3px double #20180f;color:#20180f}
#p-name{font-variant:small-caps}
.p-prompt button{border:1px solid #20180f;background:#efe8d8;color:#20180f}
#p-prompt-body{border-top:1px solid #c9bfa6;padding-top:10px}
#tt{background:#20180f;color:#f4efe3;border-radius:0}
""")

# 3. TERMINAL — green phosphor CRT, monospace, scanlines.
T("terminal", "Terminal · dispatch.sh", "dispatch@orchestrator:~$", "timeline",
  "CRT fosforo verde: monospace, scanlines, nos como prompts, grafo em eixo temporal",
r"""
body{font-family:"IBM Plex Mono",ui-monospace,monospace;color:#4bff9f;background:#020806}
body::after{content:"";position:fixed;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 1px,transparent 1px 3px);z-index:30;opacity:.5}
#sidebar{background:#04120c;border-right:1px solid #0e3d28}
#brand{color:#7dffbf;text-shadow:0 0 8px rgba(75,255,159,.6)}
.ditem{border:1px solid #0e3d28}
.ditem::before{content:"> "}
.ditem:hover,.ditem.sel{background:#062818;border-color:#4bff9f}
.dtype{color:#2fd685}
.node.group{border:1px solid #2fd685;padding:3px 7px;background:#04140d}
.node.group::before{content:"["}.node.group::after{content:"]"}
.node.agent{padding:5px 9px;border:1px solid #12603f;background:#03130c;text-shadow:0 0 6px rgba(75,255,159,.5)}
.node.agent:hover,.node.agent.active{border-color:#7dffbf;box-shadow:0 0 12px rgba(75,255,159,.4)}
.node.agent.rev{color:#ffe26b;border-color:#8a6a10;text-shadow:0 0 6px rgba(255,226,107,.5)}
.node .n-role::before{content:"#"}
.edge{stroke:#2fd685;stroke-dasharray:2 2}
#legend .dot.rev{background:#ffe26b}
#panel{background:#04120c;border-left:1px solid #2fd685;color:#8dffc4}
#p-name{color:#7dffbf}
.p-prompt button{border:1px solid #12603f;background:#03130c;color:#4bff9f}
#p-prompt-body::before{content:"$ cat initial_prompt\A";white-space:pre;opacity:.5}
#tt{background:#03130c;color:#4bff9f;border:1px solid #2fd685;border-radius:0}
""")

# 4. NEO-BRUTALIST — thick black borders, raw color blocks, hard shadows.
T("brutalist", "Brutalist · DISPATCHES", "DISPATCHES//", "scatter",
  "neo-brutalista: bordas pretas grossas, blocos crus, sombras duras, nos espalhados",
r"""
body{font-family:"Arial Black",Haettenschweiler,Arial,sans-serif;color:#111;background:#f7e733}
#sidebar{background:#ff5da2;border-right:5px solid #111}
#brand{font-weight:900;text-transform:uppercase}
.ditem{border:3px solid #111;background:#fff;box-shadow:5px 5px 0 #111}
.ditem:hover,.ditem.sel{background:#7cf6ff;transform:translate(-1px,-1px);box-shadow:7px 7px 0 #111}
.dtype{background:#111;color:#f7e733;padding:2px 5px;font-weight:900}
#main{background:#f7e733}
.node.group{background:#111;color:#fff;padding:5px 10px;border:3px solid #111;font-weight:900;text-transform:uppercase}
.node.agent{background:#fff;border:4px solid #111;padding:7px 11px;box-shadow:6px 6px 0 #111;font-weight:700}
.node.agent:hover,.node.agent.active{background:#7cf6ff;box-shadow:8px 8px 0 #111}
.node.agent.rev{background:#ff5da2}
.edge{stroke:#111;stroke-width:3px}
#legend .dot.rev{background:#ff5da2;border:2px solid #111}
#panel{background:#7cf6ff;border-left:6px solid #111;color:#111}
#p-name{font-weight:900;text-transform:uppercase}
.p-role{background:#111;color:#7cf6ff;display:inline-block;padding:3px 7px}
.p-prompt button{border:3px solid #111;background:#f7e733;color:#111;font-weight:900;box-shadow:4px 4px 0 #111}
#tt{background:#111;color:#f7e733;border-radius:0;border:2px solid #f7e733}
""")

# 5. GLASS — glassmorphic frosted panels over a gradient aurora, radial graph.
T("glass", "Glass · Dispatch Atlas", "Dispatch Atlas", "radial",
  "glassmorphism: paineis foscos, gradiente aurora, desfoque, grafo radial",
r"""
body{font-family:"Inter",system-ui,sans-serif;color:#eaf0ff;background:#171a3a;
  background-image:radial-gradient(60% 60% at 15% 10%,#5b3ea8 0,transparent 60%),radial-gradient(50% 50% at 90% 20%,#1f7a8c 0,transparent 55%),radial-gradient(70% 70% at 60% 100%,#a83e7a 0,transparent 60%)}
#sidebar{background:rgba(255,255,255,.06);backdrop-filter:blur(14px);border-right:1px solid rgba(255,255,255,.14)}
#brand{font-weight:600}
.ditem{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:12px;backdrop-filter:blur(6px)}
.ditem:hover,.ditem.sel{background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.4)}
.dtype{color:#b9c6ff}
.node.group{padding:5px 12px;border-radius:20px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);backdrop-filter:blur(6px)}
.node.agent{padding:9px 12px;border-radius:16px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);backdrop-filter:blur(10px);box-shadow:0 8px 30px rgba(0,0,0,.25)}
.node.agent:hover,.node.agent.active{background:rgba(255,255,255,.26);border-color:#fff}
.node.agent.rev{border-color:#ffd27f;box-shadow:0 0 22px rgba(255,210,127,.35)}
.edge{stroke:rgba(255,255,255,.55);stroke-width:1.4px}
#legend .dot.rev{background:#ffd27f}
#panel{background:rgba(30,32,66,.72);backdrop-filter:blur(22px);border-left:1px solid rgba(255,255,255,.2);color:#eaf0ff}
.p-prompt button{border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.08);color:#eaf0ff;border-radius:12px}
#tt{background:rgba(20,22,48,.9);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.2)}
""")

# 6. ORBITAL — deep space, concentric rings per group, glowing bodies.
T("orbital", "Orbital · Dispatch System", "ORBITAL", "orbit",
  "sistema orbital: espaco profundo, grupos em aneis concentricos, corpos luminosos",
r"""
body{font-family:"Space Grotesk","Inter",system-ui,sans-serif;color:#dfe6ff;background:#05060f;
  background-image:radial-gradient(1px 1px at 20% 30%,#fff 50%,transparent),radial-gradient(1px 1px at 70% 60%,#9fb 50%,transparent),radial-gradient(1px 1px at 40% 80%,#bcf 50%,transparent),radial-gradient(1px 1px at 85% 25%,#fff 50%,transparent);background-size:auto}
#sidebar{background:rgba(8,10,26,.8);border-right:1px solid #1b2350}
#brand{letter-spacing:.28em;color:#9fb4ff}
.ditem{border:1px solid #1b2350;border-radius:10px;background:rgba(14,18,44,.6)}
.ditem:hover,.ditem.sel{border-color:#6f8bff;background:rgba(28,36,86,.7)}
.dtype{color:#8ea2ff}
#stage-wrap::before{content:"";position:absolute;left:50%;top:50%;width:6px;height:6px;border-radius:50%;transform:translate(-50%,-50%);background:#fff;box-shadow:0 0 24px 8px rgba(150,180,255,.6)}
.node.group{padding:3px 9px;border-radius:14px;border:1px solid #4a5aa8;background:rgba(10,14,36,.85);color:#aeb9ff}
.node.agent{width:auto;padding:8px 11px;border-radius:50px;background:radial-gradient(circle at 35% 30%,#3b4da0,#141a44);border:1px solid #5a6cc0;box-shadow:0 0 16px rgba(90,120,255,.35)}
.node.agent:hover,.node.agent.active{box-shadow:0 0 26px rgba(140,170,255,.7);border-color:#cdd7ff}
.node.agent.rev{background:radial-gradient(circle at 35% 30%,#a06a1e,#3a2708);border-color:#e6b24e;box-shadow:0 0 20px rgba(230,178,78,.5)}
.edge{stroke:#5a6cc0;stroke-width:1.2px;opacity:.6}
#legend .dot.rev{background:#e6b24e}
#panel{background:rgba(8,10,26,.9);border-left:1px solid #4a5aa8;color:#dfe6ff}
#p-name{color:#aeb9ff}
.p-prompt button{border:1px solid #4a5aa8;background:rgba(14,18,44,.8);color:#dfe6ff;border-radius:10px}
#tt{background:#0a0e24;border:1px solid #4a5aa8}
""")

# 7. SWISS — international typographic style, red/black on white, strict grid.
T("swiss", "Swiss · Dispatch Grid", "DISPATCH / GRID", "rows",
  "estilo suico: Helvetica, vermelho-preto-branco, grade rigida, faixas horizontais",
r"""
body{font-family:"Helvetica Neue",Arial,sans-serif;color:#111;background:#fff}
#sidebar{background:#fff;border-right:1px solid #111}
.side-head{border-bottom:4px solid #e2231a}
#brand{font-weight:700;letter-spacing:-.01em}
.ditem{border-bottom:1px solid #d6d6d6;border-radius:0}
.ditem:hover,.ditem.sel{background:#111;color:#fff}
.ditem:hover .dtype,.ditem.sel .dtype{color:#ff6b60}
.dtype{color:#e2231a;font-weight:700}
#stage-title{font-weight:700}
.node.group{border-left:4px solid #e2231a;padding:2px 8px;font-weight:700;background:#fff}
.node.agent{padding:7px 11px;border:1px solid #111;background:#fff;font-weight:500}
.node.agent:hover,.node.agent.active{background:#111;color:#fff}
.node.agent.rev{border-left:4px solid #e2231a}
.node .n-role{color:#e2231a;font-weight:700}
.node.agent:hover .n-role{color:#ff6b60}
.edge{stroke:#111;stroke-width:1.2px}
#legend .dot.rev{background:#e2231a}
#panel{background:#fff;border-left:1px solid #111;color:#111}
.p-role{color:#e2231a;font-weight:700}
#p-name{font-weight:700;letter-spacing:-.01em}
.p-prompt button{border:1px solid #111;background:#fff;color:#111;font-weight:700;border-radius:0}
#tt{background:#e2231a;border-radius:0}
""")

# 8. MISSION-CONTROL — dark ops console, amber+teal, telemetry vibe, radial.
T("mission", "Mission Control · Dispatch Ops", "MISSION CONTROL", "radial",
  "console de operacoes: escuro, ambar+teal, telemetria, grafo radial de estacao",
r"""
body{font-family:"Roboto Mono","IBM Plex Mono",monospace;color:#c9d6d3;background:#0b1114}
#sidebar{background:#0e161a;border-right:1px solid #1c2c33}
#brand{color:#37d6c4;letter-spacing:.16em}
#tagline{color:#8aa0a0}
.ditem{border:1px solid #1c2c33;background:#0c1418}
.ditem:hover,.ditem.sel{border-color:#37d6c4;background:#10221f}
.dtype{color:#f0a93b}
.node.group{padding:4px 9px;border:1px solid #2a4046;background:#0c1a1e;color:#7fe4d8;letter-spacing:.05em}
.node.agent{padding:6px 10px;border:1px solid #2a4046;background:#0d191d;box-shadow:inset 0 0 0 1px rgba(55,214,196,.12)}
.node.agent:hover,.node.agent.active{border-color:#37d6c4;box-shadow:0 0 14px rgba(55,214,196,.4)}
.node.agent.rev{border-color:#f0a93b;color:#ffce7a;box-shadow:0 0 14px rgba(240,169,59,.3)}
.node .n-role{color:#f0a93b}
.edge{stroke:#37d6c4;opacity:.6}
#legend .dot.rev{background:#f0a93b}
#panel{background:#0e161a;border-left:1px solid #2a4046;color:#c9d6d3}
#p-name{color:#7fe4d8}
.p-role{color:#f0a93b}
.p-meta dt{color:#5f7a7a}
.p-prompt button{border:1px solid #2a4046;background:#0c1a1e;color:#c9d6d3}
#tt{background:#06100f;border:1px solid #37d6c4}
""")

# 9. SKETCH — hand-drawn notebook, rough borders, graph-paper, marker nodes.
T("sketch", "Sketch · Dispatch Notebook", "dispatch notebook", "scatter",
  "caderno desenhado a mao: papel quadriculado, bordas irregulares, nos rabiscados",
r"""
body{font-family:"Comic Sans MS","Segoe Print","Bradley Hand",cursive;color:#2b2b2b;background:#fcfbf3;
  background-image:linear-gradient(#e4ecf5 1px,transparent 1px),linear-gradient(90deg,#e4ecf5 1px,transparent 1px);background-size:26px 26px}
#sidebar{background:rgba(252,251,243,.9);border-right:2px solid #2b2b2b}
#brand{font-weight:700}
.ditem{border:2px solid #2b2b2b;border-radius:14px 8px 16px 6px;background:#fff}
.ditem:hover,.ditem.sel{background:#fff6c9;transform:rotate(-.4deg)}
.dtype{color:#c0392b}
.node.group{padding:3px 10px;border:2px solid #2b2b2b;border-radius:20px 8px 22px 9px;background:#fff;font-weight:700}
.node.agent{padding:7px 12px;border:2px solid #2b2b2b;border-radius:14px 20px 10px 18px;background:#fff;box-shadow:2px 3px 0 rgba(43,43,43,.25)}
.node.agent:hover,.node.agent.active{background:#d7f0ff;transform:rotate(.6deg)}
.node.agent.rev{background:#ffe0b3;border-style:dashed}
.edge{stroke:#2b2b2b;stroke-width:2px;stroke-linecap:round;stroke-dasharray:1 5}
#legend .dot.rev{background:#e08a1e}
#panel{background:#fffdf2;border-left:2px solid #2b2b2b;color:#2b2b2b}
#p-name{font-weight:700}
.p-role{color:#c0392b}
.p-prompt button{border:2px solid #2b2b2b;background:#fff6c9;color:#2b2b2b;border-radius:10px 16px 8px 14px}
#tt{background:#2b2b2b;border-radius:10px 4px 12px 4px}
""")

# 10. MONO-MINIMAL — quiet monochrome, hairlines, generous whitespace, columns.
T("mono", "Mono · Dispatch", "dispatch", "columns",
  "monocromatico minimo: linhas finas, muito espaco, tipografia quieta, colunas",
r"""
body{font-family:"Inter",system-ui,sans-serif;color:#1b1b1b;background:#fafafa;font-weight:400}
#sidebar{background:#fafafa;border-right:1px solid #e6e6e6}
#brand{font-weight:500;letter-spacing:.02em;text-transform:lowercase}
#tagline{opacity:.5}
.ditem{border-bottom:1px solid #ededed}
.ditem:hover,.ditem.sel{background:#f0f0f0}
.dtype{color:#999;font-weight:500}
.dgoal{font-weight:400}
.node.group{padding:2px 8px;color:#999;font-weight:500;border-bottom:1px solid #cfcfcf}
.node.agent{padding:7px 12px;border:1px solid #d8d8d8;background:#fff}
.node.agent:hover,.node.agent.active{border-color:#1b1b1b}
.node.agent.rev{border-left:3px solid #1b1b1b}
.node .n-role{color:#aaa}
.edge{stroke:#c2c2c2;stroke-width:1px}
#legend .dot.rev{background:#1b1b1b}
#panel{background:#fff;border-left:1px solid #e6e6e6;color:#1b1b1b}
#p-name{font-weight:500}
.p-role{color:#999}
.p-prompt button{border:1px solid #d8d8d8;background:#fafafa;color:#1b1b1b}
#tt{background:#1b1b1b}
""")

# --------------------------------------------------------------------------- #
def build():
    os.makedirs(VARIANTS, exist_ok=True)
    for t in THEMES:
        html = PAGE.format(
            title=t["title"], layout=t["layout"], brand=t["brand"],
            bodyclass="v-" + t["vid"], base=BASE_CSS, theme=t["css"],
            vid=t["vid"], body=BODY, engine=ENGINE,
        )
        with open(os.path.join(VARIANTS, t["vid"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)

    # index.html — gallery linking all 10
    cards = ""
    for i, t in enumerate(THEMES, 1):
        cards += (
            '<a class="card" href="variants/{vid}.html">'
            '<span class="num">{n:02d}</span>'
            '<span class="ct">{title}</span>'
            '<span class="cd">{one}</span>'
            '<span class="cg">geometria: {lay}</span></a>\n'
        ).format(vid=t["vid"], n=i, title=t["title"].split(" · ")[0],
                 one=t["oneline"], lay=t["layout"])
    idx = """<!doctype html><html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>UI Experimentation · 10 variantes</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;font-family:"Inter",system-ui,sans-serif;background:#0d0f16;color:#e8ecf5;padding:44px}}
h1{{margin:0 0 6px;font-size:24px}}p.sub{{margin:0 0 30px;opacity:.6;font-size:14px;max-width:720px;line-height:1.5}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.card{{display:flex;flex-direction:column;gap:7px;padding:18px;border:1px solid #262b3a;border-radius:14px;text-decoration:none;color:inherit;background:#12151f;transition:.12s}}
.card:hover{{border-color:#5f7bff;transform:translateY(-2px);background:#161a27}}
.num{{font-size:11px;opacity:.4;letter-spacing:.1em}}
.ct{{font-size:16px;font-weight:600}}.cd{{font-size:12.5px;opacity:.72;line-height:1.45}}
.cg{{font-size:11px;opacity:.45;margin-top:4px}}
footer{{margin-top:34px;font-size:12px;opacity:.5;line-height:1.6;max-width:760px}}
code{{background:#1c2130;padding:1px 5px;border-radius:4px}}
</style></head><body>
<h1>UI Experimentation &mdash; 10 variantes</h1>
<p class="sub">Cada variante e um visualizador standalone de tela unica: lista os dispatches
<em>com estrutura de grafo</em>, mostra o grafo agentes&harr;revisores ao clicar num dispatch, e
revela os dados do agente (prompt, angulo, papel, modelo, orcamento) ao clicar num no.
Mesmo comportamento (CONST-FE: FE-1/2/3/5/6) em todas; linguagem visual distinta em cada.</p>
<div class="grid">
{cards}</div>
<footer>Dados: <code>data/dispatches.json</code> (extraidos por <code>extract.py</code> de
<code>telemetry/agents/subagents-dispatch.yaml</code> &mdash; apenas dispatches estruturados).
Abra servido (<code>python -m http.server</code>) ou por duplo-clique (fallback <code>data/dispatches.js</code>).</footer>
</body></html>""".format(cards=cards)
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx)
    print("wrote", len(THEMES), "variants + index.html")
    for t in THEMES:
        print("  {:<10} {:<9} {}".format(t["vid"], t["layout"], t["oneline"]))


if __name__ == "__main__":
    build()
