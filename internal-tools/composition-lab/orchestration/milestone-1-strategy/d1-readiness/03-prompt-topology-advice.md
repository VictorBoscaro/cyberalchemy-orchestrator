---
artifact_kind: d1-prompt-topology-advice
status: proposed
date: 2026-08-13
scope: D1-repository-lens-inventory
---

# Parecer sobre prompts e topologia de D1

## Recomendação

D1 deve ser um research bifásico. A primeira fase extrai fatos literais sem receber o codebook de
“lente” ou “composição”. A segunda classifica uma tabela bruta já congelada. O conjunto mínimo que
cobre as superfícies reais do repositório é de **quatro explorers de extração e dois explorers de
classificação independentes**. Menos de quatro extratores funde superfícies com regimes de prova
diferentes; um único classificador transforma julgamento contestável em fato.

Topologia recomendada:

```text
4 extractors independentes
        ↓
collector único → raw inventory congelado + manifest/hash
        ↓
2 classifiers independentes, cegos um ao outro
        ↓
writer único preserva acordo, desacordo e unclassified
        ↔
skeptics tardios: non-vacuity + definitional-soundness
        ↓
coverage/provenance auditor
        ↓
final approver dedicado
```

O collector não interpreta. Os classificadores não procuram novos casos. O writer não resolve
divergência apagando a linha bruta. Feedback volta ao extrator somente por evidência ausente ou
citação inválida; volta aos classificadores somente por aplicação inconsistente do codebook.

## Fase 1 — perspectivas e prompts de extração

Todos os prompts devem abrir com o binding exigido pelo host. Depois do binding, cada seat recebe a
mesma proibição: **não definir lente/composição; não decidir se um caso é composição; não usar as
categorias L/C/E, a lista de operações candidata nem a unidade observacional do programa integrado;
registrar ausência e ambiguidade como dados**.

### Explorer A — registros de dispatch e configuração

**Corpus:** `telemetry/agents/subagents-dispatch.yaml`, proposals/manifests ativos sob
`.codex/workflow-inputs/**` e `.codex/dispatch-proposals/**`, e arquivos diretamente referenciados
por esses registros.

**Prompt funcional:**

> Faça um censo reproduzível das unidades de trabalho registradas. Para cada identidade de
> ocorrência, transcreva campos literais que expressem alvo, diferenças entre assentos, role,
> angle, initial_prompt, anti_bias, grupos, connections, loops, informação disponível, approver,
> working folder, estado e outputs referenciados. Ligue proposal, manifest, open e close que sejam
> o mesmo evento; não conte representações como eventos distintos. Não determine se há lente ou
> composição. Cite path:line, registre versão/data e marque campos ausentes ou incompatíveis.

**Retorno esperado:** tabela de ocorrências configuradas; mapa de equivalência entre registros;
contagens mecânicas por campo/schema; lista de referências quebradas e drift.

### Explorer B — execuções e artefatos preservados

**Corpus:** working folders apontados pelo Explorer A; `**/robot-talks/**/{dialogue,findings,reports}*`;
`**/review.md`; research outputs, handoffs e versões explicitamente ligados a uma ocorrência.

**Prompt funcional:**

> Extraia somente traços preservados do que aconteceu: entradas vistas, ordem, mensagens ou
> handoffs, outputs por assento, versões before/after, desafios e respostas, concatenação,
> seleção, síntese, divergência e resíduo preservado. Não infira interação a partir do plano, nem
> efeito a partir de close/resolved. Relacione cada traço à occurrence ID recebida ou marque
> `identity-unresolved`. Cite path:line e registre outputs mencionados mas ausentes.

**Retorno esperado:** tabela de traços de execução; encadeamentos entre outputs; ausências;
ocorrências sem output verificável; possíveis duplicatas sem decisão conceitual.

### Explorer C — normas, skills, specs e probes

**Corpus:** skills ativas em `.agents/skills/**/SKILL.md` e equivalentes realmente vinculadas pelo
repositório; `docs/features/agent-provenance-telemetry/**`; specs/probes citadas por esses materiais.

**Prompt funcional:**

> Extraia prescrições e mecanismos literalmente descritos para diferenciar perspectivas ou
> relacionar contribuições. Registre entradas, passos, ordem, independência, reveal, feedback,
> outputs e critérios declarados. Separe regra ativa, proposta, preregistro, resultado e exemplo.
> Não trate mecanismo prescrito como execução nem generalize termos locais. Cite path:line e anote
> status, data e relação explícita com registros ou outputs, quando existir.

**Retorno esperado:** catálogo de mecanismos prescritos/propostos; vínculos demonstráveis a
instâncias; versões conflitantes; termos locais sem normalização.

### Explorer D — busca negativa, drift e casos fronteiriços

**Corpus:** as mesmas famílias de A–C, orientadas por busca de ausência, equivalência e falha; closes
incompletos, propostas não executadas, outputs órfãos e versões históricas incluídos.

**Prompt funcional:**

> Procure deliberadamente casos em que multiplicidade nominal não corresponde a diferença
> observável, em que trabalho é dividido por fonte/arquivo, em que retornos só são reunidos, em que
> proposta não foi executada, em que close não preserva interação, ou em que versões/schema tornam
> a leitura incerta. Também registre casos inesperados que não caibam nessas buscas. Não classifique
> como não-composição: descreva literalmente a estrutura e a evidência disponível. Cite path:line,
> occurrence ID quando resolvível e a razão factual da seleção.

**Retorno esperado:** conjunto negativo/fronteiriço; outliers; riscos de dupla contagem,
sobrevivência e retroatividade; candidatos `unclassified`.

## Corpus: inclusão e exclusão

### Incluir

- censo integral das entradas open/close do ledger e suas identidades resolvidas;
- proposals/manifests e outputs diretamente ligados às ocorrências do censo;
- todas as ocorrências raras encontradas de reveal/reavaliação e probes observacionais;
- Robot-Talks, reviews, research e dispatches legados com diferenças inscritas em role/angle/prompt;
- casos incompletos, órfãos e não executados, porque a ausência é parte do regime de evidência;
- versões históricas necessárias para interpretar o registro na regra vigente à época.

### Excluir da unidade de contagem, sem apagar do manifest

- hits lexicais isolados de `lens/lente`, usados apenas como pista de busca;
- caches, dependências, builds, arquivos gerados e documentação externa vendorizada;
- duplicatas `.claude`/`.codex` sem provenance que demonstre prática distinta;
- proposal, manifest, ledger, report e close como ocorrências separadas quando representam o mesmo
  evento;
- pesquisa externa e taxonomias externas;
- artefatos não ligados ao trabalho de agentes, salvo como controle lexical explicitamente marcado.

Um item excluído permanece no log de busca com motivo. “Não encontrado no corpus congelado” nunca
vira “não existe no repositório”.

## Amostragem

O ledger recebe censo integral. A inspeção profunda usa amostra determinística de máxima variação,
mas os estratos devem ser definidos por **família material de artefato/mecanismo**, não por uma
teoria de composição: review; Robot-Talks; workflows com versões/reveal; research; probes/specs;
legados baseados em role/angle/prompt; casos incompletos.

- Inspecionar todos os casos raros de reveal/reavaliação e probes.
- Nos grupos numerosos, selecionar inicialmente três casos por função determinística publicada,
  variando data, tipo, topologia registrada e estado de fechamento.
- Publicar antes da leitura profunda a lista ordenada de candidatos, a chave de ordenação e a regra
  de seleção; qualquer substituição recebe justificativa.
- Expandir em blocos de dois. Parar quando duas inclusões consecutivas não acrescentarem novo campo
  literal, nova forma material de relação ou novo modo de ausência/falha.
- Nomear o resultado apenas “estabilidade descritiva desta amostra”; não “saturação da composição”
  nem cobertura do fenômeno.
- Todo outlier que contradiga a estrutura descritiva entra independentemente da regra de parada.

## Controles negativos pré-especificados

Cada controle deve ter pelo menos uma testemunha concreta ou ser registrado como `not observed`:

1. agentes divididos somente por arquivos/fontes;
2. instruções com nomes diferentes mas pedido de julgamento equivalente;
3. agente único usando “lens” em prosa;
4. múltiplos retornos apenas concatenados;
5. proposta nunca executada;
6. close sem output capaz de mostrar relação entre contribuições;
7. o mesmo evento materializado em proposal, manifest, ledger e report, para testar deduplicação;
8. mecanismo prescrito numa skill sem instância ligada demonstrável.

Os controles testam o protocolo de inclusão, não provam uma definição de não-composição.

## Fase 2 — classificação tardia

Somente depois do raw inventory e manifest serem congelados, dois classifiers recebem todas as
linhas brutas e um codebook provisório. Eles trabalham cegos um ao outro e retornam, por occurrence
ID: classificação, nível máximo de evidência, citação, confiança e justificativa. Categorias
permitidas: `mention`, `work-partition`, `declared-plurality`, `observed-candidate`, `ambiguous`,
`negative-control`, `unclassified`; níveis independentes: `prescribed`, `instantiated`, `executed`,
`effect-observed`, `unknown`.

Prompt comum:

> Classifique somente a partir da linha bruta e das citações congeladas. Não procure novas
> evidências, não corrija o raw inventory e não escolha a categoria mais forte quando faltarem
> dados. Para `effect-observed`, exija delta atribuível, controle/contrafactual ou avaliação
> independente; frequência, configuração e close não bastam. Registre todas as categorias
> plausíveis quando houver ambiguidade e escreva a observação mínima que resolveria o desacordo.

O writer publica a matriz classifier A × classifier B. Acordo não valida a categoria; desacordo não
é erro a ser apagado. Casos disputados permanecem localizáveis e podem motivar Robot-Talks.

## Skeptic gates: agora ou depois

Os três gates da skill não cabem simetricamente na extração.

- **Precedent:** o gate formal deve ficar para a pesquisa posterior de vocabulário/modelos, quando
  houver candidato capaz de carregar claim de ownership ou novidade. D1 não faz claim de novidade.
  Agora é necessário apenas um check interno de provenance/owner para deduplicar e datar práticas;
  isso cabe ao auditor, não deve autorizar taxonomia externa nem verdict de candidato.
- **Non-vacuity:** cabe em D1, mas somente depois da classificação e da primeira síntese. Ataca cada
  categoria descritiva exigindo uma linha concreta. Categoria sem witness recebe `KILL/no-witness`;
  a linha bruta não é removida.
- **Definitional-soundness:** também cabe somente depois da classificação. Testa se uma distinção
  proposta faz trabalho além de role, prompt, partição, concatenação ou outro nome já usado no
  corpus. Colapso recebe `KILL/tautological`, preservado como negativo tipado.

Se a governança exigir literalmente três skeptics em D1, o primeiro deve ser chamado
`internal-ownership/provenance` e ter escopo explicitamente limitado; não deve ser apresentado como
precedent externo completo. Encontrar owner nunca é KILL.

## Retornos agregados esperados

`research.md` preserva verbatim os quatro retornos de extração, o raw inventory congelado, os dois
retornos de classificação e os ataques dos skeptics. `findings.md`, escrito por um único owner,
contém:

- manifest path/hash e protocolo reproduzível;
- regra de identidade/deduplicação e contagens estruturais;
- tabela bruta referenciável e tabela classificada ligada por occurrence ID;
- matriz de acordo/desacordo dos classifiers;
- controles positivos, negativos, ambiguidades e `unclassified`;
- mapa separado de prescrição, instanciação, execução e efeito;
- matriz de gates com negativos tipados;
- limites, ausências e recomendação evidenciada para o próximo dispatch.

Toda claim load-bearing cita o trecho correspondente de `research.md` e o source `path:line`.

## Gates de passagem

D1 avança somente quando:

1. o corpus, busca, lista ordenada, função de amostragem e hashes permitem reprodução;
2. cada item tem occurrence ID estável e representações duplicadas estão ligadas, não contadas;
3. nenhuma linha bruta contém classificação conceitual inserida pelo extrator;
4. todos os itens classificados conservam a linha bruta e as duas decisões independentes;
5. cada família material tem caso, controle/contracaso ou lacuna explícita;
6. prescrições, instâncias, execuções e efeitos são campos independentes;
7. nenhuma claim de execução vem só de plano e nenhuma claim de efeito vem de configuração,
   frequência ou fechamento;
8. divergências, ausências, perdas e `unclassified` sobrevivem ao writer;
9. non-vacuity e definitional-soundness deixam matriz rederivável, incluindo KILLs tipados;
10. o auditor confirma citações, cobertura, hashes, deduplicação e drift; o approver dedicado aceita.

Falha de citação, identidade ou cobertura volta ao seat responsável por no máximo dois loops. Falha
conceitual não volta ao extrator para “achar” testemunha: a categoria morre. Se todas as categorias
candidatas morrerem, o resultado negativo é válido e D1 fecha `resolved`, mas o programa para para
decisão humana antes de Robot-Talks.

## Decisão para o owner do dispatch

Adotar a forma bifásica e retirar dos prompts de extração todo vocabulário que antecipe a teoria.
Manter quatro superfícies independentes porque configuração, execução, norma e contracaso possuem
regimes de prova diferentes. Adiar precedent externo; executar em D1 apenas provenance interno,
non-vacuity e collapse tardios. Essa é a menor forma que torna o inventário auditável sem fazê-lo
encontrar apenas o modelo que já recebeu.
