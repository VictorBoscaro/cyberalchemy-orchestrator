---
artifact_kind: program-resolution-draft
status: provisional-awaiting-07-08
date: 2026-08-13
scope: milestone-1-d1-route
decision_authority: human
evidence_snapshot:
  included:
    - 01-runtime-diagnosis.md
    - 02-contract-analysis.md
    - 03-test-precedent-scout.md
    - 04-epistemic-replan.md
    - 05-runtime-extension-scope.md
    - 06-replan-compliance.md
    - ../../04-integrated-program.md
    - ../../../../research/milestone-1/01-repository-inventory/research-initial-definitions.md
  pending:
    - 07
    - 08
---

# Resolução provisória do programa D1

## Estado da decisão

**BLOCK provisório até incorporar 07/08 e obter decisão humana.** Este rascunho compara as três
rotas; não autoriza alteração de capability, runtime, record ou lançamento. No snapshot desta
análise, `07` e `08` ainda não existiam nesta pasta. Seus resultados são evidência posterior e não
foram inferidos.

## Pergunta bloqueadora

Qual é a menor mudança formal que permite executar o inventário observacional de D1 com claims
compatíveis com a evidência, sem transformar o Milestone 1 numa implementação de infraestrutura?

Há dois blockers independentes:

1. **Semântico:** a `research` atual exige uma matriz de candidates/owner/witness/soundness/verdict,
   enquanto D1 coleta ocorrências e está proibido de fabricar candidates ou verdicts
   (`04-epistemic-replan.md`).
2. **Operacional:** o runtime atual rejeita qualquer `connections` não vazio e, sem conexões, lança
   apenas assentos turn-zero com manifests vazios (`01-runtime-diagnosis.md`,
   `03-test-precedent-scout.md`).

Resolver o blocker semântico é suficiente para a sequência connectionless de seis dispatches
descrita em `06-replan-compliance.md`, sob uma claim deliberadamente menor. Resolver o blocker
operacional com equivalência ao D1a exige fan-in e feedback, não apenas aceitar `connections`.

## Critérios

Escala: 1 = desfavorável; 5 = favorável. Os escores são julgamentos provisórios apoiados pelos
artefatos acima, não medições.

| rota | menor expansão | fidelidade epistemológica | rastreabilidade | tempo até evidência | reversibilidade | consequência imediata |
|---|---:|---:|---:|---:|---:|---|
| **A — capability descritiva própria** | 3 | 5 | 4 | 3 | 4 | Separa coleta observacional de adjudicação, mas nenhuma capability instalada possui hoje esse trabalho; exige criar/registrar/validar um novo contrato e redesenhar os records. |
| **B — extensão formal e aditiva de `research`** | **5** | 4 | 4 | **5** | **5** | Adiciona um modo observacional explícito, preserva o modo de verdict existente e libera o programa connectionless de `06` sem alegar handoff governado. |
| **C — runtime DAG** | 1 | **5** | **5** | 1 | 2 | Pode provar effective input e topologia, mas D1a requer R1–R4: output host-observed, mapping, fan-in e feedback; estimativa atual é 20–30 arquivos e 3–4 incrementos. |

### A — outra capability descritiva

**Benefício.** Dá fronteira semântica limpa a inventários observacionais: ocorrência, ausência,
ambiguidade e nível de evidência não precisam ser convertidos em candidates ou GO/KILL.

**Custo/risco.** Não foi encontrado owner instalado adequado. `architecture-pattern-inventory`
possui mapeamento de arquitetura e exige que o agente principal sintetize; `inventory` mantém uma
camada compilada de conhecimento. Reutilizá-las mudaria o objeto e/ou o contrato do trabalho.
Criar uma capability nova implica nome, applicability, outputs, acceptance, routing, lifecycle,
fixtures e manutenção próprios antes de produzir evidência D1.

**Quando escolher.** Se 07/08 demonstrarem que inventário descritivo é uma classe recorrente,
irredutível e útil além de D1, ou que adicioná-lo a `research` produz uma união semântica incoerente.

### B — alterar/estender formalmente `research`

**Benefício.** É a menor expansão que resolve o blocker real de D1. A própria capability já admite
`n = 1`, `findings.md` como único output e pesquisa read-only; o conflito está na obrigatoriedade
universal da matriz de verdicts. Uma extensão aditiva pode declarar dois regimes, sem relaxar o
existente:

- **observational inventory:** ocorrência/controle/ausência/ambiguidade/nível de evidência; sem
  novelty verdict, GO/KILL ou skeptic gates fictícios;
- **candidate adjudication:** mantém owner, witness, soundness, GO/KILL, precedent-first e os
  collapse-tests atuais.

O regime deve ser escolhido explicitamente antes do dispatch; objetivos que misturem os dois
devem separar estágios. Isso permite usar `06-replan-compliance.md`: E1–E4 coletam, S1 sintetiza
bytes embutidos no prompt e A1 audita, sempre sob a claim reduzida registrada ali.

**Custo/risco.** Uma edição informal do arquivo gerado seria inválida. A mudança precisa ocorrer no
owner canônico da capability, ser regenerada nas superfícies aplicáveis, receber fixtures de ambos
os regimes e preservar compatibilidade do modo de adjudicação. O risco central é transformar
`research` numa capability genérica demais; applicability e collapse-tests entre regimes precisam
impedir isso.

**Quando escolher.** Agora, se 07/08 não trouxerem evidência de que o regime observacional possui
owner diferente ou quebra invariantes load-bearing de `research`.

### C — implementar runtime DAG

**Benefício.** É a rota de maior rastreabilidade operacional: produtor, bytes aceitos, mapping,
manifest, readiness, launch e feedback podem se tornar observáveis e reexecutáveis.

**Custo/risco.** Não é um patch de compiler. O mínimo útil ao record D1a atravessa R1–R4, inclui
migration, autoridade de launch, recovery, fan-in e semântica ainda aberta de feedback. O programa
integrado também declara que o Milestone 1 não autoriza construir runtime, e
`05-runtime-extension-scope.md` recomenda um milestone próprio. Implementá-lo agora atrasa a
primeira evidência sobre lentes e mistura a investigação do fenômeno com a infraestrutura usada
para observá-lo.

**Quando escolher.** Somente se a decisão humana elevar effective-input binding e causalidade da
topologia a requisito da investigação. Nesse caso, abrir RT-H1/RT-H2/RT-H3 como programa separado;
D1a não fica pronto após apenas o piloto sequencial 1→1.

## Recomendação provisória

**Preferir B; manter A como fallback semântico e C como roadmap separado.** B tem a menor expansão,
chega mais rápido à evidência interna e é reversível porque pode ser aditiva. Ela não torna a
sequência de `06` equivalente ao D1a: a claim aceitável continua limitada a dispatches fechados,
bytes embutidos em prompts confirmados e outputs citados, sem prova de consumo causal ou handoff
intradispatch.

A recomendação cai em favor de A se 07/08 mostrarem que o inventário observacional tem ciclo de
vida, consumidores ou critérios de aceitação incompatíveis com `research`. Ela cai em favor de C
somente se trouxerem evidência de que a pergunta do milestone não pode ser respondida honestamente
sem binding efetivo — algo que 01–06 não demonstram.

## Condições mínimas antes de prosseguir

1. Incorporar 07/08 citando seus resultados reais; não tratar ausência atual como parecer.
2. Submeter ao gate humano a escolha A/B/C, com opção de pedir mais contexto.
3. Se B for escolhida, produzir primeiro uma proposta de alteração do contrato canônico e seus
   collapse-tests; não editar a superfície gerada nem lançar D1 no mesmo ato.
4. Revalidar o programa stageado de `06` contra a capability ratificada e preparar records novos;
   não reutilizar o D1a conectado.
5. Manter C fechada salvo decisão explícita de abrir milestone de runtime independente.

