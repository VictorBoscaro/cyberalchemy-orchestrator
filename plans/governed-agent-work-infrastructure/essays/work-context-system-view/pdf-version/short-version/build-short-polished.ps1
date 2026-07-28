$ErrorActionPreference = "Stop"

$root = "C:\Users\victo\cyberalchemy-orchestrator"
$source = Join-Path $root "plans\governed-agent-work-infrastructure\essays\work-context-system-view\pdf-version\work-context-system-view-polished-diagrams.html"
$output = Join-Path $root "plans\governed-agent-work-infrastructure\essays\work-context-system-view\pdf-version\short-version\work-context-system-view-short-polished-diagrams.html"

$html = [IO.File]::ReadAllText($source, [Text.Encoding]::UTF8)

$extraCss = @'

/* Short edition: quieter marginal signals and compact explanatory figures. */
@page {
  @top-left-corner {
    background:
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) left 8mm top 8mm / 7mm .4pt no-repeat,
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) left 8mm top 8mm / .4pt 7mm no-repeat;
  }
  @top-right-corner {
    background:
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) right 8mm top 8mm / 7mm .4pt no-repeat,
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) right 8mm top 8mm / .4pt 7mm no-repeat;
  }
  @bottom-left-corner {
    background:
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) left 8mm bottom 8mm / 7mm .4pt no-repeat,
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) left 8mm bottom 8mm / .4pt 6mm no-repeat;
  }
  @bottom-right-corner {
    background:
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) right 8mm bottom 8mm / 7mm .4pt no-repeat,
      linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) right 8mm bottom 8mm / .4pt 6mm no-repeat;
  }
  @top-center { background: none; }
  @bottom-center { background: none; }
  @left-middle { background: none; }
  @right-middle { background: none; }
}

.flow-explanation {
  margin: 1mm 0 3mm;
  color: #51433b;
  font-size: 9.25pt;
}

.intention-map {
  position: relative;
  margin: 3.5mm 0 5.5mm;
  padding: 6mm 5mm 4.5mm;
  border-top: .7pt solid rgba(123,33,20,.46);
  border-bottom: .7pt solid rgba(123,33,20,.34);
  break-inside: avoid-page;
}

.intention-map::before {
  content: "";
  position: absolute;
  top: 17.2mm;
  left: 11mm;
  right: 11mm;
  height: .7pt;
  background: linear-gradient(90deg, #8b2d1c, #b87f64 44%, #302720);
}

.intention-map__stages {
  position: relative;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 2.5mm;
}

.intention-stage {
  position: relative;
  min-width: 0;
  padding-top: 9mm;
  text-align: center;
}

.intention-stage::before {
  content: "";
  position: absolute;
  top: 5.2mm;
  left: 50%;
  width: 3.2mm;
  height: 3.2mm;
  border: 1.2pt solid #842718;
  border-radius: 50%;
  background: #f4eadc;
  transform: translateX(-50%);
}

.intention-stage:nth-child(3)::before {
  background: #211b17;
  border-color: #211b17;
}

.intention-stage b {
  display: block;
  margin-bottom: 1.2mm;
  color: #792315;
  font: 700 8.1pt/1.15 Arial, sans-serif;
  letter-spacing: .55pt;
  text-transform: uppercase;
}

.intention-stage span {
  display: block;
  margin: .7mm 0;
  color: #2e241e;
  font: 7.5pt/1.24 Arial, sans-serif;
}

.intention-stage em {
  color: #7b5c4d;
  font-style: normal;
}

.revision-loop {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.5mm;
  margin-top: 3.5mm;
  color: #6f3d30;
  font: 7.5pt/1.2 Arial, sans-serif;
  letter-spacing: .18pt;
}

.revision-loop::before,
.revision-loop::after {
  content: "";
  width: 17mm;
  height: 3.5mm;
  border-top: .7pt dashed #b56750;
  border-radius: 50%;
}

.context-hierarchy {
  margin: 3.5mm 0 5mm;
  padding: 3mm 2mm 2.5mm;
  border-top: .7pt solid rgba(123,33,20,.46);
  border-bottom: .7pt solid rgba(123,33,20,.34);
  break-inside: avoid-page;
}

.context-hierarchy svg {
  display: block;
  width: 100%;
  height: 61mm;
}

.context-hierarchy .context-node {
  fill: rgba(255,250,242,.72);
  stroke: #9d806b;
  stroke-width: 1.05;
}

.context-hierarchy .context-node--selected {
  fill: #241d19;
  stroke: #241d19;
}

.context-hierarchy .context-node--accent {
  fill: #f3dfcf;
  stroke: #9b321f;
  stroke-width: 1.15;
}

.context-hierarchy .context-line {
  fill: none;
  stroke: #9b6e5b;
  stroke-width: 1.15;
}

.context-hierarchy .context-return {
  fill: none;
  stroke: #b43f27;
  stroke-width: 1.05;
  stroke-dasharray: 4 4;
}

.context-hierarchy .context-kicker {
  fill: #8a4a38;
  font: 700 7px Arial, sans-serif;
  letter-spacing: .85px;
}

.context-hierarchy .context-title {
  fill: #261d18;
  font: 700 10px Georgia, serif;
}

.context-hierarchy .context-copy {
  fill: #665249;
  font: 7.5px Arial, sans-serif;
}

.context-hierarchy .context-inverse {
  fill: #fff8ed;
}

.context-hierarchy figcaption {
  margin: 2mm 1mm 0;
  color: #69564a;
  font: 7.6pt/1.35 Arial, sans-serif;
}

.context-field {
  margin: 3mm 0 6mm;
  padding: 4.5mm;
  border: .7pt solid #ad927d;
  background: rgba(255,250,242,.45);
  break-inside: avoid-page;
}

.context-field__center {
  width: 43mm;
  margin: 0 auto 3.5mm;
  padding: 2.5mm 3mm;
  border-radius: 20mm;
  background: #211b17;
  color: #fff7ea;
  font: 700 8.2pt/1.2 Arial, sans-serif;
  text-align: center;
  letter-spacing: .35pt;
  text-transform: uppercase;
}

.context-field__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2mm;
}

.context-field__grid div {
  min-height: 17mm;
  padding: 2.5mm;
  border-top: 1.2pt solid #a53b26;
  background: rgba(244,234,220,.7);
  color: #2c221d;
  font: 7.6pt/1.28 Arial, sans-serif;
}

.context-field__grid b {
  display: block;
  margin-bottom: .8mm;
  color: #792315;
  font-size: 7.2pt;
  letter-spacing: .3pt;
  text-transform: uppercase;
}

.short-status {
  margin: 4mm 0 6mm;
  padding: 3.5mm 4mm;
  border-left: 2.2pt solid #b43f27;
  background: rgba(255,250,241,.48);
  color: #47372f;
  font: 8.2pt/1.42 Arial, sans-serif;
}

.section3-page {
  break-before: page;
  margin-top: 0;
  padding-top: 3mm;
}

.section3-page + p {
  margin-bottom: 3.5mm;
  color: #51433b;
  font-size: 9pt;
}

.inspection-test {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3mm;
  margin: 6mm 0 0;
  padding-top: 4mm;
  border-top: .7pt solid rgba(123,33,20,.45);
  break-inside: avoid-page;
}

.inspection-test div {
  padding-right: 2mm;
  color: #352922;
  font: 8pt/1.38 Arial, sans-serif;
}

.inspection-test b {
  display: block;
  margin-bottom: 1.3mm;
  color: #7b2114;
  font-size: 7.4pt;
  letter-spacing: .45pt;
  text-transform: uppercase;
}

.infrastructure-opening,
.infrastructure-diagram-page {
  break-before: page;
  margin-top: 0;
  padding-top: 3mm;
}

.infrastructure-lede {
  max-width: 151mm;
  color: #3d3029;
  font-size: 9.35pt;
  line-height: 1.48;
}

.infra-thesis {
  display: grid;
  grid-template-columns: 43mm 1fr;
  gap: 7mm;
  margin: 6mm 0 7mm;
  padding: 5mm 0;
  border-top: .8pt solid rgba(123,33,20,.52);
  border-bottom: .8pt solid rgba(123,33,20,.32);
  break-inside: avoid-page;
}

.infra-thesis strong {
  color: #792315;
  font: 700 8pt/1.25 Arial, sans-serif;
  letter-spacing: .55pt;
  text-transform: uppercase;
}

.infra-thesis p {
  margin: 0;
  color: #2f251f;
  font-size: 9pt;
  line-height: 1.46;
}

.plane-reading {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3mm 5mm;
  margin: 5mm 0 0;
  break-inside: avoid-page;
}

.plane-reading article {
  min-height: 29mm;
  padding: 3.5mm 3.5mm 3mm;
  border-top: 1.25pt solid #9e3b29;
  background: rgba(246,238,226,.54);
}

.plane-reading small {
  display: block;
  margin-bottom: 1mm;
  color: #8a5c49;
  font: 700 6.9pt/1.15 Arial, sans-serif;
  letter-spacing: .45pt;
  text-transform: uppercase;
}

.plane-reading h3 {
  margin: 0 0 1.2mm;
  color: #27201c;
  font-size: 10pt;
}

.plane-reading p {
  margin: 0;
  color: #493a32;
  font-size: 8pt;
  line-height: 1.38;
}

.infra-figure {
  margin: 3mm 0 4mm;
  padding: 3mm 2.5mm 2.5mm;
  border-top: .7pt solid rgba(123,33,20,.45);
  border-bottom: .7pt solid rgba(123,33,20,.28);
  break-inside: avoid-page;
}

.infra-figure svg {
  display: block;
  width: 100%;
  height: auto;
}

.infra-figure .boundary {
  fill: rgba(255,250,241,.18);
  stroke: #6d5d52;
  stroke-width: 1.25;
}

.infra-figure .plane {
  stroke-width: 1;
}

.infra-figure .decision-plane {
  fill: rgba(145,172,188,.11);
  stroke: #6e8999;
}

.infra-figure .mediation-plane {
  fill: rgba(191,128,72,.09);
  stroke: #a86a34;
}

.infra-figure .knowledge-plane {
  fill: rgba(80,139,111,.08);
  stroke: #4f8469;
}

.infra-figure .service {
  fill: #fffaf1;
  stroke-width: 1.15;
}

.infra-figure .service-decision { stroke: #587b90; }
.infra-figure .service-run { stroke: #9c632f; }
.infra-figure .service-knowledge { stroke: #4d8067; }
.infra-figure .service-gate { fill: #f7f0fb; stroke: #8763a3; }
.infra-figure .service-open { fill: #fff4f1; stroke: #a7473b; stroke-dasharray: 4 3; }

.infra-figure .label {
  fill: #29221e;
  font: 700 10px Arial, sans-serif;
}

.infra-figure .copy {
  fill: #625248;
  font: 8px Arial, sans-serif;
}

.infra-figure .cap {
  fill: #724033;
  font: 700 8px Arial, sans-serif;
  letter-spacing: 1px;
}

.infra-figure .flow {
  fill: none;
  stroke: #745448;
  stroke-width: 1.35;
}

.infra-figure .evidence-flow {
  fill: none;
  stroke: #4d8067;
  stroke-width: 1.15;
}

.infra-figure .reference-flow {
  fill: none;
  stroke: #8763a3;
  stroke-width: 1;
  stroke-dasharray: 4 3;
}

.infra-legend {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4mm;
  margin-top: 4mm;
  break-inside: avoid-page;
}

.infra-legend div {
  color: #44362f;
  font: 7.8pt/1.4 Arial, sans-serif;
}

.infra-legend b {
  display: block;
  margin-bottom: 1mm;
  color: #792315;
  font-size: 7.1pt;
  letter-spacing: .45pt;
  text-transform: uppercase;
}

.infra-note {
  margin: 4.5mm 0 0;
  padding: 3.5mm 4mm;
  border-left: 2pt solid #a7473b;
  background: rgba(255,246,240,.48);
  color: #49372f;
  font: 8pt/1.42 Arial, sans-serif;
}

.infra-runline {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 2mm;
  margin: 7mm 0 4mm;
  padding: 4mm 0;
  border-top: .7pt solid rgba(123,33,20,.45);
  border-bottom: .7pt solid rgba(123,33,20,.3);
  break-inside: avoid-page;
}

.infra-runline div {
  position: relative;
  padding: 0 2mm;
  color: #493a32;
  font: 7.4pt/1.34 Arial, sans-serif;
}

.infra-runline div:not(:last-child)::after {
  content: "→";
  position: absolute;
  top: 3.5mm;
  right: -1.8mm;
  color: #a66a55;
}

.infra-runline b {
  display: block;
  margin-bottom: 1mm;
  color: #792315;
  font-size: 6.9pt;
  letter-spacing: .4pt;
  text-transform: uppercase;
}

.infra-reading-note {
  margin: 0;
  color: #54443a;
  font-size: 8.4pt;
  line-height: 1.43;
}

.infra-preserves {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4mm;
  margin-top: 6mm;
  padding-top: 4mm;
  border-top: .7pt solid rgba(123,33,20,.38);
  break-inside: avoid-page;
}

.infra-preserves div {
  color: #493a32;
  font: 7.8pt/1.4 Arial, sans-serif;
}

.infra-preserves b {
  display: block;
  margin-bottom: 1mm;
  color: #792315;
  font-size: 7pt;
  letter-spacing: .4pt;
  text-transform: uppercase;
}

.part3-short,
.part4-short {
  break-before: page;
  margin-top: 0;
  padding-top: 3mm;
}

.part3-lede,
.part4-lede {
  color: #45362e;
  font-size: 9.4pt;
  line-height: 1.5;
}

.recover-grid {
  margin: 5mm 0 6mm;
  border-top: .7pt solid rgba(123,33,20,.46);
  break-inside: avoid-page;
}

.recover-row {
  display: grid;
  grid-template-columns: 34mm 1fr;
  gap: 6mm;
  padding: 3.4mm 0;
  border-bottom: .55pt solid rgba(111,83,65,.34);
}

.recover-row b {
  color: #792315;
  font: 700 7.5pt/1.25 Arial, sans-serif;
  letter-spacing: .5pt;
  text-transform: uppercase;
}

.recover-row span {
  color: #30251f;
  font-size: 8.8pt;
  line-height: 1.42;
}

.gentle-claim {
  margin: 5mm 0 6mm;
  padding: 4mm 5mm;
  border-left: 2.4pt solid #b43f27;
  background: rgba(255,250,241,.5);
  color: #3d3029;
  font-size: 9pt;
  line-height: 1.48;
}

.system-qualities {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 3mm;
  padding-top: 4mm;
  border-top: .7pt solid rgba(123,33,20,.4);
  break-inside: avoid-page;
}

.system-qualities div {
  color: #4d3d34;
  font: 7.7pt/1.38 Arial, sans-serif;
}

.system-qualities b {
  display: block;
  margin-bottom: 1mm;
  color: #792315;
  font-size: 7pt;
  letter-spacing: .4pt;
  text-transform: uppercase;
}

.part4-short + .part4-lede {
  margin-bottom: 3mm;
}

.part4-short ~ .infra-figure {
  margin-top: 4mm;
}

.part4-caption {
  margin: 2.5mm 0 4mm;
  color: #625046;
  font: 7.8pt/1.38 Arial, sans-serif;
}

.part4-reading {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4mm;
  padding-top: 4mm;
  border-top: .7pt solid rgba(123,33,20,.38);
  break-inside: avoid-page;
}

.part4-reading div {
  color: #493a32;
  font: 7.7pt/1.4 Arial, sans-serif;
}

.part4-reading b {
  display: block;
  margin-bottom: 1mm;
  color: #792315;
  font-size: 7pt;
  letter-spacing: .4pt;
  text-transform: uppercase;
}
'@

$html = $html.Replace("</style>", $extraCss + "`r`n</style>")

$perceptionScopeParagraph = @'
<p>The system does not need to model human perception itself. It needs to preserve the attributable
transition from a situated perception to a declared and revisable objective.</p>
'@

if (-not $html.Contains($perceptionScopeParagraph)) {
  throw "Perception-scope paragraph was not found exactly."
}
$html = $html.Replace($perceptionScopeParagraph, "")

$oldFlow = @'
<pre><code class="language-text">perception
-&gt; objective
-&gt; monolithic intention
-&gt; differentiated intentions
&lt;-&gt; composed and revisable objective
-&gt; possible route
-&gt; Plan, workstream, or another decomposable form
-&gt; steps
-&gt; detailed work
-&gt; tasks
-&gt; attempts
-&gt; effects and artifacts
</code></pre>
'@

$newFlow = @'
<p class="flow-explanation">As an intention is differentiated, work acquires a hierarchy of contexts. Each lower context makes one portion of the objective more concrete without becoming detached from the broader purpose that explains it.</p>
<figure class="context-hierarchy" aria-label="A hierarchy of contexts from objective to effects and artifacts">
  <svg viewBox="0 0 760 286" role="img" aria-labelledby="context-hierarchy-title context-hierarchy-desc">
    <title id="context-hierarchy-title">A hierarchy of work contexts</title>
    <desc id="context-hierarchy-desc">A composed objective differentiates into several intentions. One selected intention becomes a route, then a bounded form of work, detailed work, tasks, attempts, effects, and artifacts. Meaning descends while evidence and learning return upward.</desc>
    <defs>
      <marker id="context-return-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#b43f27"/></marker>
    </defs>

    <text class="context-kicker" x="8" y="24">BROADER CONTEXT</text>
    <text class="context-kicker" x="8" y="270">LOCAL CONTEXT</text>
    <path class="context-line" d="M28 34V250"/>

    <rect class="context-node context-node--accent" x="270" y="8" width="220" height="36" rx="18"/>
    <text class="context-kicker" x="292" y="23">COMPOSED AND REVISABLE</text>
    <text class="context-title" x="292" y="36">objective</text>

    <path class="context-line" d="M380 44V58M142 58H618M142 58V70M380 58V70M618 58V70"/>
    <rect class="context-node" x="70" y="70" width="144" height="38" rx="8"/>
    <text class="context-kicker" x="86" y="86">INTENTION A</text>
    <text class="context-copy" x="86" y="99">one differentiated concern</text>
    <rect class="context-node context-node--selected" x="308" y="70" width="144" height="38" rx="8"/>
    <text class="context-kicker context-inverse" x="324" y="86">SELECTED INTENTION</text>
    <text class="context-copy context-inverse" x="324" y="99">the branch being developed</text>
    <rect class="context-node" x="546" y="70" width="144" height="38" rx="8"/>
    <text class="context-kicker" x="562" y="86">INTENTION C</text>
    <text class="context-copy" x="562" y="99">another possible concern</text>

    <path class="context-line" d="M380 108V124"/>
    <rect class="context-node context-node--accent" x="296" y="124" width="168" height="34" rx="8"/>
    <text class="context-kicker" x="312" y="139">POSSIBLE ROUTE</text>
    <text class="context-copy" x="312" y="151">a direction toward the objective</text>

    <path class="context-line" d="M380 158V174"/>
    <rect class="context-node" x="262" y="174" width="236" height="34" rx="8"/>
    <text class="context-kicker" x="278" y="189">BOUNDED FORM OF WORK</text>
    <text class="context-copy" x="278" y="201">Plan, workstream, section, or directly bounded task</text>

    <path class="context-line" d="M380 208V221M196 221H564M196 221V232M380 221V232M564 221V232"/>
    <rect class="context-node" x="128" y="232" width="136" height="38" rx="8"/>
    <text class="context-kicker" x="144" y="248">DETAILED WORK</text>
    <text class="context-copy" x="144" y="261">steps and tasks</text>
    <rect class="context-node" x="312" y="232" width="136" height="38" rx="8"/>
    <text class="context-kicker" x="328" y="248">ATTEMPTS</text>
    <text class="context-copy" x="328" y="261">concrete acts</text>
    <rect class="context-node context-node--accent" x="496" y="232" width="136" height="38" rx="8"/>
    <text class="context-kicker" x="512" y="248">REALIZATION</text>
    <text class="context-copy" x="512" y="261">effects and artifacts</text>

    <path class="context-return" d="M650 251C724 238 726 50 506 26" marker-end="url(#context-return-arrow)"/>
    <text class="context-copy" x="655" y="150" transform="rotate(-90 655 150)">evidence and learning revise higher contexts</text>
  </svg>
  <figcaption>Context narrows downward: purpose and constraints remain inherited as work becomes executable. Evidence travels upward: attempts and effects can clarify, challenge, or revise any context above them.</figcaption>
</figure>
'@

if (-not $html.Contains($oldFlow)) {
  throw "Original intention sequence was not found exactly."
}
$html = $html.Replace($oldFlow, $newFlow)

$oldConnections = @'
<p>A local piece of work should remain connected to:</p>
<ul>
<li>the objective from which it ultimately emerged;</li>
<li>the interpretations, assumptions, and evidence that shaped that objective;</li>
<li>the Plans, discoveries, specifications, and decisions that refined it;</li>
<li>the authority that permitted a person, agent, or tool to act;</li>
<li>the attempts, effects, and artifacts through which the work became concrete; and</li>
<li>the evidence used to judge whether the result advanced anything larger.</li>
</ul>
'@

$newConnections = @'
<p>A local piece of work is explained by a field of relationships, not by one parent link. The same six connections from the longer essay can be read as distinct questions around the local act:</p>
<figure class="context-field" aria-label="The relationships that explain a local piece of work">
  <div class="context-field__center">local piece of work</div>
  <div class="context-field__grid">
    <div><b>Purpose</b>the objective from which it ultimately emerged</div>
    <div><b>Interpretation</b>the assumptions and evidence that shaped that objective</div>
    <div><b>Refinement</b>the Plans, discoveries, specifications, and decisions that refined it</div>
    <div><b>Authority</b>what permitted a person, agent, or tool to act</div>
    <div><b>Realization</b>the attempts, effects, and artifacts through which the work became concrete</div>
    <div><b>Judgment</b>the evidence used to judge whether the result advanced anything larger</div>
  </div>
</figure>
'@

if (-not $html.Contains($oldConnections)) {
  throw "Original section 3 connection list was not found exactly."
}
$html = $html.Replace($oldConnections, $newConnections)

$firstTable = $html.IndexOf("<table>", $html.IndexOf("<h3>Proposal: why familiar framings may be partial</h3>", [StringComparison]::Ordinal), [StringComparison]::Ordinal)
if ($firstTable -lt 0) {
  throw "Section 3 framing table not found."
}
$tableLead = @'
<h3 class="section3-page">Four useful components, none sufficient alone</h3>
<p>Each familiar system preserves one necessary part of the route. The comparison below does not reject those systems; it shows why work-context infrastructure must connect their contributions without treating any one of them as the whole.</p>
'@
$html = $html.Insert($firstTable, $tableLead)

$readingMapPattern = '(?s)<h3>Reading map</h3>\s*<ul>.*?</ul>\s*(?=<h3>Proposal:)'
$html = [regex]::Replace($html, $readingMapPattern, @'
<div class="short-status"><strong>Short-edition scope.</strong> This version follows the core problem from intention to distributed work, identifies the paths that must remain independently inspectable, and closes with a compact conceptual infrastructure for preserving them.</div>
'@)

$inspectionClose = @'
<div class="inspection-test" aria-label="How to inspect the five paths">
  <div><b>Inspect, do not infer</b>A strong purpose link does not prove authority, assignment, causation, or realization. Each path must answer its own question.</div>
  <div><b>Keep gaps visible</b>Missing, conflicted, and superseded links are information. The system should expose them instead of completing the story by proximity.</div>
  <div><b>Test both directions</b>From a local effect, recover why and under whose authority it exists. From an objective, recover what work and evidence make it real.</div>
</div>
'@

$fivePathsEndPattern = '(?s)(<figure class="concept-figure five-paths".*?</figure>)\s*(?=<h2>4\. Moving from the part to the whole</h2>)'
$html = [regex]::Replace($html, $fivePathsEndPattern, ('$1' + $inspectionClose))

$section4 = $html.IndexOf("<h2>4. Moving from the part to the whole</h2>", [StringComparison]::Ordinal)
if ($section4 -lt 0) {
  throw "Section 4 boundary not found."
}

$part4 = @'
<h2 class="infrastructure-opening">4. Infrastructure that preserves the paths</h2>
<p class="infrastructure-lede">The preceding sections describe a continuity problem: local work becomes easier to execute as it becomes harder to relate back to purpose, authority, and evidence. The infrastructure below is one conceptual response. It separates the decisions that shape a run from the machinery that executes it, the mediation that protects independent work, and the durable knowledge needed to reconstruct what happened.</p>
<p class="infrastructure-lede">This is not a deployment diagram. The boxes name responsibilities that must remain distinguishable even when several are implemented by one component. The boundaries matter because collapsing them makes hidden substitutions possible: a runtime may change an approved plan, a transport may rewrite an agent's judgment, or a record may preserve outputs without preserving their lineage.</p>

<div class="infra-thesis">
  <strong>Architectural claim</strong>
  <p>A governed run is not merely a sequence of agent calls. It is a confirmed work shape executed without silent reinterpretation, mediated without hidden authorship, and recorded through identities and versioned references that make the result inspectable later.</p>
</div>

<div class="plane-reading" aria-label="How to read the four infrastructure planes">
  <article><small>01 - Decide</small><h3>Decision plane</h3><p>Classifies the question, selects a versioned protocol, and compiles a concrete work shape. Its output is a proposal for what may run, not execution itself.</p></article>
  <article><small>02 - Run</small><h3>Execution plane</h3><p>Resolves approved bindings and invokes the work that was confirmed. It should not quietly redesign the topology while running it.</p></article>
  <article><small>03 - Mediate</small><h3>Mediation plane</h3><p>Fabric remains present during agent work. It addresses, seals, holds, releases, and delivers contributions while preserving their authorship and independence.</p></article>
  <article><small>04 - Remember</small><h3>Knowledge plane</h3><p>Identity, versioned prompts, and an append-only record provide the stable references through which purpose, action, and evidence can be traced.</p></article>
</div>

<div class="infra-runline" aria-label="One governed run">
  <div><b>01 - Question</b>declare objective and boundary</div>
  <div><b>02 - Decide</b>classify, route, and compile</div>
  <div><b>03 - Confirm</b>approve shape and authorize digest</div>
  <div><b>04 - Execute</b>mediate independent work</div>
  <div><b>05 - Record</b>preserve evidence and revise</div>
</div>
<p class="infra-reading-note">The sequence is intentionally narrow. Context is not copied into one giant prompt; it remains addressable through stable identities, typed relations, versioned instructions, and evidence emitted at each handoff.</p>

<h3 class="infrastructure-diagram-page">A conceptual system boundary</h3>
<p class="infrastructure-lede">A human question enters the decision plane. The resulting shape is confirmed before execution; agent work is mediated through Fabric; and events flow into the durable record. Supporting identities and prompt versions remain addressable throughout the run.</p>

<figure class="infra-figure" aria-label="Conceptual infrastructure for governed agent work">
  <svg viewBox="0 0 760 500" role="img" aria-labelledby="infra-title infra-desc">
    <title id="infra-title">Conceptual system boundary for governed agent work</title>
    <desc id="infra-desc">A question moves through Classifier, Protocol, Compiler, human confirmation, and Execution. Fabric mediates agent workers. Identity, Prompts, and Record support durable reference and evidence. Authority ownership remains open.</desc>
    <defs>
      <marker id="infra-arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#745448"/></marker>
      <marker id="infra-evidence" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#4d8067"/></marker>
      <marker id="infra-reference" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#8763a3"/></marker>
    </defs>

    <rect class="boundary" x="108" y="18" width="540" height="458" rx="13"/>
    <text class="cap" x="128" y="42">PROPOSED SYSTEM BOUNDARY - CONCEPTUAL</text>

    <rect class="service service-decision" x="8" y="80" width="86" height="74" rx="10"/>
    <text class="cap" x="22" y="101">HUMAN</text>
    <text class="label" x="22" y="123">Question</text>
    <text class="copy" x="22" y="140">objective + boundary</text>

    <rect class="plane decision-plane" x="128" y="64" width="318" height="124" rx="11"/>
    <text class="cap" x="146" y="86">DECISION PLANE - WHAT MAY RUN</text>
    <rect class="service service-decision" x="146" y="103" width="84" height="57" rx="8"/>
    <text class="label" x="158" y="126">Classifier</text>
    <text class="copy" x="158" y="143">question to kind</text>
    <rect class="service service-decision" x="246" y="103" width="84" height="57" rx="8"/>
    <text class="label" x="259" y="126">Protocol</text>
    <text class="copy" x="259" y="143">versioned shape</text>
    <rect class="service service-decision" x="346" y="103" width="84" height="57" rx="8"/>
    <text class="label" x="358" y="126">Compiler</text>
    <text class="copy" x="358" y="143">bound plan</text>

    <rect class="service service-gate" x="462" y="84" width="82" height="84" rx="9"/>
    <text class="cap" x="476" y="105">HUMAN GATE</text>
    <text class="label" x="476" y="128">Confirm</text>
    <text class="copy" x="476" y="145">shape + digest</text>

    <rect class="service service-run" x="560" y="73" width="70" height="104" rx="10"/>
    <text class="cap" x="571" y="95">EXECUTION</text>
    <text class="label" x="571" y="121">Run</text>
    <text class="copy" x="571" y="139">resolve</text>
    <text class="copy" x="571" y="151">collect</text>

    <rect class="plane mediation-plane" x="128" y="214" width="502" height="98" rx="11"/>
    <text class="cap" x="146" y="236">MEDIATION PLANE - PRESENT THROUGHOUT AGENT WORK</text>
    <rect class="service service-run" x="146" y="251" width="466" height="42" rx="8"/>
    <text class="label" x="160" y="270">Fabric</text>
    <text class="copy" x="211" y="270">address - seal - hold - release - deliver unchanged - record</text>
    <text class="copy" x="160" y="284">transports and enforces; never authors or rewrites judgment</text>

    <rect class="service service-run" x="664" y="215" width="86" height="97" rx="10"/>
    <text class="cap" x="677" y="237">AGENT WORKERS</text>
    <text class="label" x="677" y="262">independent A</text>
    <text class="label" x="677" y="281">independent B</text>
    <text class="copy" x="677" y="299">aggregation point</text>

    <rect class="plane knowledge-plane" x="128" y="340" width="502" height="112" rx="11"/>
    <text class="cap" x="146" y="362">KNOWLEDGE PLANE - STABLE REFERENCE AND DURABLE FACT</text>
    <rect class="service service-knowledge" x="146" y="380" width="126" height="52" rx="8"/>
    <text class="label" x="160" y="403">Identity</text>
    <text class="copy" x="160" y="419">typed relations</text>
    <rect class="service service-knowledge" x="288" y="380" width="126" height="52" rx="8"/>
    <text class="label" x="302" y="403">Prompts</text>
    <text class="copy" x="302" y="419">versioned bindings</text>
    <rect class="service service-knowledge" x="430" y="373" width="182" height="66" rx="8"/>
    <text class="label" x="445" y="397">Record</text>
    <text class="copy" x="445" y="414">append-only events + lineage</text>
    <text class="copy" x="445" y="428">only durable-fact ingress</text>

    <rect class="service service-open" x="8" y="358" width="86" height="76" rx="10"/>
    <text class="cap" x="21" y="380">OPEN OBLIGATION</text>
    <text class="label" x="21" y="402">Authority</text>
    <text class="copy" x="21" y="419">owner unresolved</text>

    <path class="flow" d="M94 117H142" marker-end="url(#infra-arrow)"/>
    <path class="flow" d="M230 132H242M330 132H342M430 132H458M544 132H556" marker-end="url(#infra-arrow)"/>
    <path class="flow" d="M595 177V210" marker-end="url(#infra-arrow)"/>
    <path class="flow" d="M612 272H660" marker-end="url(#infra-arrow)"/>
    <path class="flow" d="M664 286H616" marker-end="url(#infra-arrow)"/>
    <path class="evidence-flow" d="M595 293V335H522V369" marker-end="url(#infra-evidence)"/>
    <path class="evidence-flow" d="M379 293V326H522V369" marker-end="url(#infra-evidence)"/>
    <path class="reference-flow" d="M208 380V326H188V164" marker-end="url(#infra-reference)"/>
    <path class="reference-flow" d="M351 380V326H595V181" marker-end="url(#infra-reference)"/>
    <path class="flow" d="M94 396H124" stroke-dasharray="4 3"/>
  </svg>
</figure>

<div class="infra-legend" aria-label="Infrastructure interpretation">
  <div><b>Control</b>The upper route decides, confirms, and executes one explicit work shape. Confirmation is meaningful only if execution consumes the same version and digest.</div>
  <div><b>Content</b>Agent messages and judgments pass through Fabric. Mediation may enforce timing and delivery rules, but it must not become an invisible co-author.</div>
  <div><b>Evidence</b>Events enter Record as durable facts linked to stable identities and versions. Corrections append; they do not erase the path that produced them.</div>
</div>

<div class="infra-note"><strong>Still unresolved:</strong> authority is a first-class obligation, but its owning service is not yet fixed. The diagram keeps that gap outside the system boundary so the architecture does not imply a certainty it has not earned.</div>

<div class="infra-preserves" aria-label="What the infrastructure must preserve">
  <div><b>Same confirmed shape</b>The executable digest must be the shape the human inspected and authorized. Any changed route becomes a new version.</div>
  <div><b>Visible authorship</b>Infrastructure may transport, validate, and sequence contributions, but it must not silently become their author.</div>
  <div><b>Durable revision</b>New facts and corrections append to the record, keeping the context they supersede available for inspection.</div>
</div>
'@

$html = $html.Substring(0, $section4) + $part4 + "</main></body></html>`r`n"

# Final short-edition composition: Parts 1-2 remain above; Parts 3-4 are intentionally
# lighter, user-facing, and constrained to one page each.
$section3Start = $html.IndexOf("<h2>3. The problem the system must solve</h2>", [StringComparison]::Ordinal)
if ($section3Start -lt 0) {
  throw "Section 3 boundary not found for the final short composition."
}

$diagramMatch = [regex]::Match($part4, '(?s)<figure class="infra-figure".*?</figure>')
if (-not $diagramMatch.Success) {
  throw "Compact infrastructure diagram could not be recovered."
}

$shortTail = @'
<h2 class="part3-short">3. What continuity would make possible</h2>
<p class="part3-lede">As work becomes divided, its meaning is distributed across many places. A project contains tasks; a specification carries traces of research and discussion; a decision rests on assumptions that may no longer be visible. The practical promise of work-context infrastructure is modest: to let a person recover those relationships when they matter.</p>
<p class="part3-lede">Instead of treating each document, task, or artifact as an isolated object, the system would help it remain part of a larger and revisable story.</p>

<div class="recover-grid" aria-label="What a person could understand through preserved work context">
  <div class="recover-row"><b>From a project</b><span>see which tasks, attempts, and results gradually composed it.</span></div>
  <div class="recover-row"><b>From a specification</b><span>recover the research, questions, and interpretations that refined what it came to say.</span></div>
  <div class="recover-row"><b>From a decision</b><span>understand the assumptions, alternatives, evidence, and authority behind it.</span></div>
  <div class="recover-row"><b>From an artifact</b><span>trace the work that produced it and the objective it was meant to advance.</span></div>
  <div class="recover-row"><b>From an objective</b><span>follow the work outward and notice what remains incomplete, uncertain, or no longer aligned.</span></div>
</div>

<div class="gentle-claim">The aim is not to produce a perfect account of work. It is to make forgetting less automatic: to preserve enough continuity that people can revisit why something exists, how it changed, and whether it still belongs to the purpose that first gave it meaning.</div>

<div class="system-qualities" aria-label="Qualities that support continuity">
  <div><b>Connected</b>Work can point beyond itself toward the contexts that explain it.</div>
  <div><b>Attributable</b>Ideas, judgments, and actions retain a visible source.</div>
  <div><b>Revisable</b>Later learning can change earlier understanding without erasing its history.</div>
  <div><b>Honest about gaps</b>Missing or conflicting context remains visible rather than being guessed.</div>
</div>

<h2 class="part4-short">4. One possible shape for the infrastructure</h2>
<p class="part4-lede">The diagram offers one possible arrangement, not a finished architecture. Its purpose is to show a few useful separations: deciding what work should happen, carrying it out, mediating contributions, and preserving what can later be known about the run.</p>
<p class="part4-lede">A human question enters at the top. Work is shaped and confirmed before execution, contributions pass through a shared fabric, and identities, instructions, and recorded events keep the result connected to its history.</p>

__DIAGRAM__

<p class="part4-caption">The boundaries are conceptual. Several responsibilities may initially live in one component. What matters is that a system can distinguish a proposed route from its execution, an agent's contribution from its transport, and a current conclusion from the record through which it became credible. Authority remains deliberately open.</p>

<div class="part4-reading" aria-label="A light reading of the infrastructure">
  <div><b>Shape before action</b>The work can be inspected before people or agents begin carrying it out.</div>
  <div><b>Preserve the voice</b>Mediation helps contributions move without quietly rewriting who said what.</div>
  <div><b>Remember change</b>The record keeps later revision connected to the path that made revision possible.</div>
</div>
'@

$shortTail = $shortTail.Replace("__DIAGRAM__", $diagramMatch.Value)
$html = $html.Substring(0, $section3Start) + $shortTail + "</main></body></html>`r`n"

[IO.File]::WriteAllText($output, $html, [Text.UTF8Encoding]::new($false))
Write-Output $output
