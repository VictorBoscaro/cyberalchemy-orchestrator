---
artifact_kind: external-research-execution-redesign
status: blocked-pending-honest-routing
date: 2026-08-13
---

# Plano externo em pequenos lotes

## Veredito

**BLOCK** para registrar, abrir ou lançar as unidades abaixo como dispatches `research`.
**READY** apenas para preparar tarefas nativas bounded/read-only, se esse mecanismo for confirmado
pelo owner. O dispatch conectado original continua semanticamente correto e operacionalmente
bloqueado; remover suas conexões falsificaria os handoffs.

## Correção produzida pela revisão

A primeira proposta tratava owner-maps isolados como `research` com um único
`skeptic/precedent`. Isso é inválido: o mesmo seat descobriria e julgaria candidatos, e o dispatch
fecharia sem witness, soundness, verdict, use-mode e resposta ao goal. Um auditor isolado tampouco
é `research`: sua posição vem de uma edge downstream. Portanto, coleta parcial não será chamada de
dispatch `research` nem produzirá sua matriz canônica.

## Mecanismo honesto proposto

Por domínio, executar somente após confirmação:

1. tarefa bounded de owner-map: 1 collector, 5.000 tokens, web REQUIRED, 5--7 âncoras;
2. tarefa bounded de witness probe: até 3 entradas congeladas, 3.500 tokens, web LIMITED;
3. tarefa bounded de collapse probe: mesmas entradas, 3.500 tokens, web LIMITED;
4. tarefa bounded de evidence-pack: 1 writer, 5.000 tokens, web DISABLED;
5. revisão bounded separada: 2.500 tokens, web DISABLED.

Cada etapa escreve em folder próprio e só consome artefatos aceitos anteriores por path e hash.
Nenhuma delas emite GO/KILL canônico. O primeiro `research` governado virá depois, contendo
exploração, três gates, writer e auditor e fechando `research.md`, `findings.md`, matriz completa e
resposta ao goal. Com o runtime atual, ele permanece BLOCK até haver handoffs governados.

Fontes: papers/livros originais, standards, specifications, publicações institucionais e docs
oficiais. Reviews/handbooks só navegam. Excluir dicionários como fundamento, resumos sem fonte,
vendor thought pieces e analogias. Registrar citações estáveis, queries e inclusão/exclusão; exigir
uma fonte de fronteira/falha. Sem web efetiva no seat, BLOCK, sem substituição por memória.

## Primeiro lote exato

### A — `e1-formal-structural-owner-map`

- mecanismo: tarefa nativa bounded/read-only; seat sugerida `Capucci, Matteo`; 5.000 tokens;
- folder: `internal-tools/composition-lab/research/external-composition-precedents/batches/e1-formal-structural-owner-map/`;
- pergunta: quais contas formais possuídas definem composição por plugging, substituição ou
  encadeamento, e quais leis de tipagem, identidade, associatividade, equivalência, fechamento ou
  decomposição a distinguem de justaposição/pareamento?
- corpus: category/monoidal theory, operads, compositional/process semantics e type/algebraic
  specification; 5--7 fontes primárias/autoridades, incluindo uma boundary/failure;
- admissão: owner exato + operação explícita + obrigação observável + vizinho distinguido;
- output: somente `owner-map.md`, com source/search log, limites de transferência e entradas; sem
  matriz/veredito.
- prompt: pesquise somente essas superfícies; use web e o corpus limitado; preserve owners,
  citações, operação, obrigação, vizinho, limite e decisões de seleção; exclua analogias; escreva
  apenas `owner-map.md`; não sintetize domínios nem inspecione o repositório.

### B — `e1-engineered-owner-map`

- mecanismo: tarefa nativa bounded/read-only; seat sugerida `Parnas, David`; 5.000 tokens;
- folder: `internal-tools/composition-lab/research/external-composition-precedents/batches/e1-engineered-owner-map/`;
- pergunta: quais modelos possuídos de componentes software/sistemas, workflow/dataflow e end-user
  composition definem composição por contratos, interfaces, closure ou substitution, e como a
  distinguem de integração, configuração e orquestração?
- corpus: 5--7 papers, standards, specs ou docs oficiais, incluindo boundary/failure;
- admissão/output: iguais a A;
- prompt: pesquise somente essas superfícies; preserve owner, citação, contrato/interface/operação,
  obrigação, vizinho, limite e selection log; exclua materiais não autorizados; escreva apenas
  `owner-map.md`; não sintetize.

O par é piloto por maximizar contraste entre um substrato formal e um engineered, ambos com
operações/obrigações relativamente explícitas. Isso testa o protocolo antes dos domínios
parts-wholes-systems e epistemic-social-creative; não lhes atribui prioridade teórica.

### C — revisão do lote

Após A e B aceitos, tarefa bounded/read-only com reviewer, 2.500 tokens, web DISABLED e inputs por
path/hash. Verifica método, proveniência, source logs e contrato, sem comparar findings ou criar
teoria. Output `audit.md`. PASS permite propor os outros dois owner-maps; FAIL exige correção.

## Gates

1. Confirmar o uso de tarefas nativas bounded como mecanismo, sem lifecycle de dispatch.
2. Congelar prompts, budgets, folders e escopo de escrita.
3. Verificar web efetiva antes de A/B.
4. Aceitar cada output e congelar path/hash antes de C.
5. Não executar probes, escalar domínios, comparar ou sintetizar antes de C.

## Estado factual

Advisor consultado; revisão independente resultou em BLOCK e suas críticas foram incorporadas.
Nenhuma web, pesquisa, record, registro, open, binding, launch ou close ocorreu.
