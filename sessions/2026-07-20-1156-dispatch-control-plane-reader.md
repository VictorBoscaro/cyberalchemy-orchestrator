---
tags: [agents, orchestration, control-plane, ledger, ui]
node_type: discovery
is_session: true
layer: architecture
nature: technical
status: active
created: 2026-07-20
timestamp: 2026-07-20T11:56:29-03:00
expires: 2026-09-18
conversation_id: b232d909-3a3e-48be-afd9-78a4b0ad7e7d
decisions_made: true
contradictions_found: true
specs_updated: [.claude/skills/close-session/SKILL.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "É a primeira fatia executável do orquestrador do PLAN.md — leitor rodando contra 693 dispatches reais e dez variantes de UI validadas — mas ainda não fecha, faltando a escolha humana e a Fase 2."
---

# Dispatch control plane — Fase 1 (o leitor)

## Summary

A sessão começou como uma pergunta sobre conectar o trabalho de agentes deste repo a
um servidor com UI em tempo real, e virou a construção da primeira fatia executável do
"orquestrador de agentes" do `PLAN.md`. O desenho convergiu para uma UI de control
plane que renderiza a dispatch sheet, serve de gate humano e observa as execuções ao
vivo — explicitamente **não** um editor de agentes, já que quem compõe os subagentes é
o Claude e o humano confirma. A leitura de `register-dispatch` revelou que o schema de
composição **já existe** (v0.6.0, com edges tipados), então nenhum schema novo foi
inventado; ela também expôs o problema de ordem: o ledger só é escrito após o confirm
humano, logo uma UI que lê só o ledger nunca pode *ser* o gate. A peça faltante foi
nomeada: um artefato pré-confirm em `telemetry/agents/pending/<id>.json`, a única
superfície editável, deixando o ledger append-only intocado. A Fase 1 foi construída:
servidor FastAPI com SSE que auto-descobre repos e parseia os ledgers, mais dez
variantes de UI sobre um único contrato. Dados reais forçaram duas correções de
desenho — o leitor precisa ser **leniente** onde o appender é estrito (em modo estrito
o repo `domainspec` retornava zero dispatches), e campos calculados pelo leitor
precisam de prefixo `_` porque `status` é chave real das rows pré-v0.5.2 e estava sendo
sobrescrita. Os testes construídos validam o que esta sessão produziu — parser (smoke
contra 693 dispatches reais) e uma suíte Playwright rodando o mesmo contrato contra as
dez variantes — e não geram evidência sobre specs pré-existentes; três dos bugs
encontrados estavam no próprio arcabouço de teste, não nas UIs. Uma auditoria de enums
sobre os ledgers reais achou dez `exit_reason` fora do vocabulário v0.6.0, dois deles
datados de 2026-07-18 e portanto não-históricos. As dez variantes passam 24/24 e
aguardam a escolha do humano.

## Contradictions

- questions `.claude/skills/register-dispatch/SKILL.md` — a auditoria achou dez
  `exit_reason` fora do vocabulário fechado v0.6.0; dois deles são o valor literal
  `"success"`, datados de 2026-07-18 e portanto não-grandfathered. Como
  `append-dispatch.cjs` rejeita esse valor com exit 2, aquelas close rows não podem ter
  passado pelo appender documentado, o que sugere um caminho de escrita paralelo que a
  skill não prevê.
- contradicts `.claude/skills/register-dispatch/SKILL.md` — a skill diz que registrar um
  `dispatch_type` RESERVED "signals an upstream violation", mas `code` aparece 26 vezes
  e `suggestion` 1 vez nos ledgers reais, e um hook PreToolUse pede registro a cada
  dispatch de Agent. Não é dúvida: as contagens são fechadas, e a regra escrita e a
  prática instalada se refutam.

## Open questions

- Um artefato pré-confirm editável preserva a disciplina append-only ou apenas
  **desloca** a escrita para fora do alcance da validação? A fixture de demonstração
  enuncia a pergunta; a sessão não a respondeu.
- O fan-out de dez variantes revelou opções de desenho genuínas, ou dez vestimentas do
  mesmo layout? O contrato fixou estrutura e testids com rigor suficiente para que a
  variação possa ser só de pele — não foi medido.

## Next steps

1. Escolher a variante; apagar as nove restantes de `implementations/static/ui/` e
   remover a fixture `telemetry/agents/pending/2026-07-19-exemplo-ui-control-plane.json`.
2. Rastrear como as duas close rows de 2026-07-18 entraram no ledger de
   `domainspec-lean-formalization` sem passar pelo appender.
3. Construir a Fase 2: `POST /confirm` no servidor mais a espera via `Monitor`, mantendo
   a cadeia check-tension → register-dispatch intacta.

## Recommendation

O keystone é (2), o furo no caminho de escrita — não (1), que é barato e independente.
O fato que licencia isso é uma auditoria que rodou, não um palpite: a primeira aresta de
Contradictions acima já registra duas close rows que o appender teria rejeitado. A
próxima sessão deveria atacar (2) antes de (3), porque o gate que a UI existe para impor
herda qualquer furo que tenha deixado aquelas rows entrarem. A primeira Open question
acima é a forma abstrata do mesmo risco e deve ser decidida junto, não depois.

## Files touched

- implementations/README.md
- implementations/UI-CONTRACT.md
- implementations/config.example.json
- implementations/requirements.txt
- implementations/server/__init__.py
- implementations/server/config.py
- implementations/server/ledger.py
- implementations/server/main.py
- implementations/static/index.html
- implementations/static/ui/aurora/index.html
- implementations/static/ui/blueprint/index.html
- implementations/static/ui/brutalist/index.html
- implementations/static/ui/cyberpunk/index.html
- implementations/static/ui/grimoire/index.html
- implementations/static/ui/linear/index.html
- implementations/static/ui/mission-control/index.html
- implementations/static/ui/radar/index.html
- implementations/static/ui/swiss/index.html
- implementations/static/ui/terminal/index.html
- implementations/tests/audit_enums.py
- implementations/tests/test_ledger.py
- implementations/tests/test_ui.py
- telemetry/agents/pending/2026-07-19-exemplo-ui-control-plane.json
- .claude/skills/close-session/SKILL.md
