# MAPPING — paralelos construto ⟷ tipo CT (ledger vivo)

> Estatuto: brainstorm/candidato, **não-revisado**. Claim ≤ proof: cada linha é um
> **paralelo candidato a tipar**, não um resultado. Onde a âncora é fraca (memória / Lean
> não-commitado / síntese nossa) está rotulado. Fonte-única do mapping (protocolo §3 do PLAN):
> a tabela vive **aqui**; PLAN §4 aponta, não duplica.
>
> **Regra herdada.** Todo construto da linguagem-de-agentes → seu tipo em CT + âncora num
> arquivo real. A base operacional é a skill `domainspec-subagents-strategy`
> (`domainspec/.claude/skills/domainspec-subagents-strategy/SKILL.md`) + constituição
> `subagents-strategy-constitution-proposal.md` (v0.6.3). Criado 2026-07-19.

---

## 1. Tabela-semente (herdada de PLAN §4)

| Construto | Tipo CT candidato | Âncora | Força |
|---|---|---|---|
| sonda/probe (recon) | elemento generalizado / functor-of-points (Yoneda) | `YonedaAsTranslation.y`, `Probe.lean` | candidato forte |
| probe (experiment) | falsificação Popperiana | `experiment/SKILL.md` | rima nominal (≠ Yoneda) |
| zig-zag | identidades triangulares / `EqvGen` ida-e-volta | `P1Positive.CommaConnected`, `probe_zigzag_nf.lean` | candidato forte |
| sequential | composição `∘` | `connections` | estrutural |
| dispatch | diagrama tipado `J → Cat` | schema v0.6.x | candidato |
| feedback / robot-talks | ? (2-célula / (co)limite de perspectivas) | — | aberto → ver §2 |
| residue de uma síntese | `FunctorialResidueStructure` / unit de Lan não-iso | `FunctorialResidueStructure.lean` | estrutural |

## 2. Paralelos derivados da skill `subagents-strategy` (sessão 2026-07-19)

| Construto | Semântica literal na skill | Tipo CT candidato | Força / o que resolve |
|---|---|---|---|
| **concat vs. synthesis** (P7) | `robot_talks:true → sintetiza`; senão `concat`; "aggregation is **derived**, never a field"; "a bare concat is never the final deliverable" | **concat = coproduto** (thin, count-shaped) vs. **synthesis = pushout/colimit** (identifica sobreposições na tensão; **gera resíduo**) | **forte.** Liga direto a `FunctorialResidueStructure` (DEF-ORCH-001); meio caminho da sub-obrigação 3 de OBL-E3 |
| **feedback edge** | "`feedback` edges **never count as dependencies**"; conditional; back-edge p/ puxar material | **NÃO 1-morfismo** — 2-célula / estrutura extra (fora do 1-esqueleto) | **evidência positiva** p/ o risco de OBLIGATIONS. Move P-CT: feedback = 2-cell, não morfismo |
| **check-tension / anti-bias axes** (P5) | par n≥2 tensionado; eixo ∈ {methodology, source-corpus, attack-vector, temporal-prior}; 2 agentes verificam | **família separadora de sondas** (jointly-faithful); cada eixo = direção de probe ortogonal; o gate = enriquecer `C` não-thin | **forte.** Dá à sonda (DEF-ORCH-004) forma *plural*; amarra F4 + F6 (eixo = separador/anomalia) |
| **meta + lineage** (P13) | `meta:true` = dispatch *sobre* dispatching; `parent_dispatch_id`; cadeia finita/acíclica | **endofunctor / free monad**; linhagem = árvore bem-fundada (operad de dispatches) | **forte.** Tese A6 ("framework as its own instance") mecanizada num campo do registro |
| **final_approver** (P12) | auditor dedicado, nunca membro de grupo (no self-approval); recebe o `working_folder` inteiro | **cone terminal / limite** do diagrama; auditor = ápice fora do diagrama | candidato |
| **exit_reason** | vocabulário fechado `resolved\|loop_ceiling_reached\|dissent_irreconcilable\|user_abort\|error` | mapa classificante p/ objeto **thin** finito = a **sombra** do run | candidato — liga DEF-ORCH-003 (leitura escalar, lossy; o resíduo real é o artefato) |
| **dependency scheduling / READY** (P4) | READY quando toda aresta `sequential`/`zig-zag` que entra produziu; todos READY lançam concorrentes; ordem declarada é só tiebreak | diagrama `J → Cat`; escala = ordem topológica do **poset** de dependências | reforça `dispatch = J → Cat` da §1 |
| **collapse-detection** (P14) | synthesizer downstream de robot-talks **precisa** das posições **inicial E final** | guardar o **morfismo**, não só o objeto = *beats count* (não decategorificar) | candidato — instância viva de F1/F3 |

## 3. Estatuto e collapse-tests

- **concat/synthesis (o achado central).** *Collapse:* se a síntese for, na prática, um merge
  count-shaped, cai no mesmo collapse-test (b) de OBL-E3 — vira analogia, não pushout.
- **feedback = 2-cell.** *Collapse:* se `feedback` compuser associativamente como aresta de
  1-nível, volta a ser morfismo e o risco de OBLIGATIONS se dissolve (improvável dado
  "never counts as a dependency").
- **sonda-plural.** *Collapse:* se os 4 eixos não forem jointly-faithful (algum objeto
  indistinguível por toda a família), a família não reconstrói e o paralelo Yoneda-FF enfraquece.
- **meta/A6.** *Collapse:* se a linhagem admitir ciclo, deixa de ser árvore bem-fundada / free
  monad — mas a constituição exige finita e acíclica.

## 4. Pendências que estas linhas tocam

- **P-CT** (PLAN): feedback/robot-talks — **encaminhado** por §2 (feedback = 2-cell; synthesis
  = colimit). Falta tipar em Lean.
- **OBL-E3 sub-3** (resíduo-de-síntese = mesmo objeto): a linha concat/synthesis é a rota
  concreta de descarga — tipar `synthesize` como pushout cujo unit não-iso É `FunctorialResidueStructure`.
