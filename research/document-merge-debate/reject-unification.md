# Tese contrária à junção de `agents-communication-protocols` e `bus-contracts`

## Conclusão executiva

Os dois discoveries **não devem ser fundidos em um único documento** neste estágio. Devem permanecer
documentos separados, ligados por referências normativas explícitas e por uma pequena matriz de
interfaces. A razão não é estética: os próprios textos declaram escopos, camadas, perguntas,
entregáveis e gates de promoção diferentes. A junção faria a evolução e a promoção da fronteira
estreita do Work Bus dependerem de decisões semânticas muito mais amplas que ainda estão abertas;
simetricamente, faria o discovery de protocolos carregar detalhes operacionais que ele explicitamente
atribui à infraestrutura existente.

Esta conclusão é sobre **unificação documental**, não sobre isolamento conceitual ou ausência de
integração. Os textos devem concordar na interface; não precisam compartilhar lifecycle editorial.

## Fontes, edição e significado das referências

Esta tese usa somente evidência interna verificável, sem depender de afirmações externas:

- `ACP` = `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`,
  versão `0.3.0`, `last_updated: 2026-07-22` (`ACP`, linhas 1–12).
- `BC` = `docs/features/agents-communication-infra/discovery/bus-contracts/README.md`, versão `0.3.0`,
  `last_updated: 2026-07-22` (`BC`, linhas 1–11).
- `BCR` = `docs/features/agents-communication-infra/discovery/bus-contracts/review/review.md`, review
  pós-remediação (`BCR`, linhas 1–17).

Uma citação `ACP:22–29`, por exemplo, significa as linhas 22 a 29 do arquivo `ACP` acima. Como ambos
os textos são drafts (`ACP:7`; `BC:7`), números de linha devem ser atualizados se os arquivos mudarem.

## Definição operacional de “junção”

Rejeito a seguinte operação: substituir os dois discoveries por um artefato editorial único, com um
único escopo, backlog de perguntas, conjunto de resultados e gate de promoção. Não rejeito:

1. referências cruzadas;
2. um glossário compartilhado;
3. uma tabela de correspondência entre entidades;
4. promoção posterior de contratos compatíveis para a SPEC;
5. uma página-index que apresente ambos como partes de uma mesma iniciativa.

Essa distinção é exigida pelo próprio `BC`: ele declara que aprofunda uma fronteira mais estreita do
discovery de protocolos, que seu resultado pode alterar aquele discovery e que só depois de revisão
independente contratos podem ser promovidos à SPEC (`BC:28–39`). Relação e retroalimentação já são
previstas sem identidade documental.

## Argumento 1 — os objetos de decisão são diferentes

**Premissa 1.** `ACP` procura definir o ciclo completo pelo qual agentes pesquisam, discutem,
sintetizam, executam, revisam, pedem correções e aprovam; além do transporte, ele trata independência,
versionamento, limites de correção e vinculação da aprovação à versão exata (`ACP:16–29`).

**Premissa 2.** `BC` cobre somente o Work Bus e operações de submissão/revisão; exclui Knowledge,
telemetria e controle, reservando Knowledge a outro discovery (`BC:15–26`). Ele se define ainda como
aprofundamento da fronteira estreita entre assignment, input materializado, submission, artifact,
roteamento e consumo (`BC:28–36`).

**Premissa 3.** `BC` exclui do próprio bus o command/control plane, handoff workflow, realtime
projection e uma extensão futura de knowledge (`BC:373–383`); explica que bloqueio, cancelamento,
reabertura e decisão humana entram no command service, não no texto de uma submissão (`BC:431–439`).
`ACP`, em contraste, precisa decidir gates, discussão, rework, revisão final e aprovação
(`ACP:38–49`, `ACP:437–485`).

**Inferência.** Um documento único teria de adotar simultaneamente os predicados “cobre o ciclo
completo” e “cobre somente a fronteira estreita Work Bus”. Isso só seria coerente se contivesse
subdocumentos com escopos próprios. Mas essa solução recria a separação defendida aqui, apenas dentro
de um arquivo maior.

**Conclusão.** A unidade lógica adequada é uma relação produtor/consumidor entre especificações, não
uma única especificação editorial.

## Argumento 2 — a precedência já define uma interface, não ownership compartilhado

`ACP` fixa uma separação explícita: a skill conserva intenção e qualidade de domínio; a recipe
digest-pinned é autoridade do grafo executável; o perfil fornece requisitos e bindings e nunca
sobrescreve a recipe; depois da confirmação, o `DispatchSpec` governa a execução (`ACP:70–99`). O
texto também diz que a mecânica runtime já pertence a `agents-communication-infra` e que o discovery
deve localizar a semântica de trabalho sem criar runtime paralelo (`ACP:22–29`).

`BC` opera justamente do lado infra dessa fronteira: o `RoutingPlan` é compilado no `DispatchSpec`,
contém topologia e release gates, enquanto instâncias, leases e rework vivem em `RoutingState` alterado
por comandos com CAS (`BC:345–366`). Além disso, skills podem ajudar, mas não substituir a SPEC,
assignment ou runtime policy (`BC:296–315`).

Portanto, os textos descrevem uma dependência orientada: semântica compilada → `DispatchSpec`/
`RoutingPlan` → mecanismos de publicação e consumo. Fundir os documentos apaga visualmente a fronteira
de autoridade que ambos tentam tornar verificável. A alternativa testável é manter duas autoridades
documentais e exigir um mapping explícito dos termos exportados/importados.

## Argumento 3 — os gates de promoção não são equivalentes

Defina:

- \(G_A\): gate de avanço de `ACP` satisfeito;
- \(G_B\): gate de promoção de `BC` satisfeito.

`ACP` requer, entre outras coisas, cobertura dos fluxos de pesquisa e execução, ownership de
compilação/registro, perfil obrigatório, separação de workers/reviewers/approval, classificação de
julgamentos, uma recipe por protocolo e autoridade única no `DispatchSpec` (`ACP:735–751`). `BC`
requer payload mínimo, reconstrução de inputs/outputs, convergência candidate/receipt/accepted,
release por classe de consumidor, evolução de `RoutingState`, change set isolado, schemas e matriz de
capabilities (`BC:626–642`). Logo, há obrigações exclusivas nos dois sentidos; em particular, provar a
atomicidade de publicação não resolve o ownership do compilador, e escolher esse ownership não prova
recovery sob crash.

Sob uma fusão com promoção única, o gate necessariamente seria

\[
G_{fusão}=G_A \land G_B.
\]

Assim, por eliminação da conjunção, \(G_{fusão}\Rightarrow G_A\) e
\(G_{fusão}\Rightarrow G_B\). A contrapositiva dá
\(\neg G_A\Rightarrow\neg G_{fusão}\) e \(\neg G_B\Rightarrow\neg G_{fusão}\): qualquer pendência
semântica ampla bloqueia a promoção do contrato estreito, e qualquer falha operacional bloqueia o
avanço da pesquisa semântica. Separados, é possível promover somente a parte cujo gate foi provado,
mantendo a outra draft, sem afirmar que a interface não importa.

Esse bloqueio não é hipotético no sentido documental: `ACP` lista 34 perguntas principais ainda em
aberto (`ACP:437–485`) e declara que decomposição automática de qualquer skill continua não provada
(`ACP:187–189`); `BC` lista 14 perguntas operacionais abertas (`BC:553–568`). Não há base nos textos
para afirmar \(G_A\leftrightarrow G_B\), condição que tornaria inofensiva uma promoção única.

## Argumento 4 — o acoplamento de mudança cresceria sem evidência de co-mudança total

Considere uma mudança \(m\) e dois predicados:

- \(a(m)\): a mudança altera semântica de protocolo;
- \(b(m)\): a mudança altera contrato do Work Bus.

Os próprios backlogs contêm testemunhas para três classes:

1. \(a(m)\land\neg b(m)\): escolher alias/extensão do role `researcher`, compilar julgamento selado
   ou decidir trust anchor da skill compiladora (`ACP:253–258`, `ACP:330–367`, `ACP:165–189`).
2. \(\neg a(m)\land b(m)\): definir threshold inline/artifact, integridade de blobs ou retenção de
   observation segments (`BC:553–568`).
3. \(a(m)\land b(m)\): mudar como profiles/assignments compilam para `RoutingPlan`, ou como uma
   submissão libera reviewers (`ACP:369–398`; `BC:96–109`, `BC:345–371`).

Logo, é falsa a hipótese de que toda mudança relevante exige editar ambos: as classes 1 e 2 são
contraexemplos extraídos dos próprios textos. Uma fusão força revisão de um artefato maior também para
mudanças locais; separação com interface explícita permite revisão local para classes 1/2 e revisão
coordenada para classe 3. A tese não afirma quantitativamente que o custo será sempre menor, apenas
que a equivalência de change sets necessária para justificar a fusão não existe.

## Argumento 5 — a diferença de maturidade epistêmica deve permanecer visível

`ACP` se autodeclara `status: draft`, `veracity: low` e `conviction: high` (`ACP:7–10`), chama o Skill
Execution Profile de hipótese, não schema ratificado (`ACP:51–68`), e mantém fora de escopo alterar a
SPEC ou criar schemas finais (`ACP:724–733`). `BC` também é draft (`BC:7`), chama seus schemas de
candidatos (`BC:199–204`) e veda promover imediatamente os nomes para a SPEC (`BC:617–624`).

Apesar dessa semelhança, a evidência de revisão não é simétrica: há um review específico de `BC` que
registra uma auditoria de remediação e oito gaps clean-room (`BCR:3–15`), com oito change requests e
verdict `FIX` (`BCR:19–41`), seguido de closure `resolved` (`BCR:43–46`). Nenhum review equivalente faz
parte do diretório de `ACP` lido para esta tese. Fundir os textos agora tornaria menos claro quais
claims passaram por qual lente e qual closure. Preservar os artefatos separados conserva a
proveniência das avaliações.

## Argumento 6 — as taxonomias ainda não fecham sem decisões adicionais

`ACP` propõe atividades com operações `produce | transform | investigate | evaluate | decide |
approve` e função epistêmica `evidence | proposal | judgment | decision`, que devem compilar para
entidades runtime existentes (`ACP:303–328`). Também exige `JudgmentRound` para qualquer agregação de
duas ou mais posições, com freeze, sealing, close, reveal e agregação (`ACP:330–367`).

`BC`, por outro lado, congela um `work_kind` único por run, atualmente apenas `research |
implementation`; review é fase/papel desse tipo e transição entre research e implementation exige
outro dispatch (`BC:476–515`). Suas operações agent-facing são `submit_work` e `submit_review`, com
capabilities/schemas disjuntos (`BC:385–425`, `BC:463–474`).

Não há contradição necessária se houver uma função de compilação bem definida. Mas o mapping ainda não
está especificado: por exemplo, `decide` e `approve` são operações de atividade em `ACP`, enquanto
decisão humana pertence ao command plane fora do Work Bus em `BC` (`BC:431–436`). Incorporar ambos
num documento antes de definir esse homomorfismo cria ambiguidade sobre se nomes semelhantes são
equivalentes, submetidos no bus ou realizados no control plane. A separação torna essa lacuna um
contrato de interface explícito e falseável.

## Argumento 7 — duplicação atual é coordenação deliberada, não prova de identidade

Há sobreposição real: ambos tratam versionamento, submissions/reviews exatos, routing, skill refs,
artifacts e invalidação. `ACP` pede que o bus entregue assignments/findings enquanto o journal persiste
versões, pareceres e aprovações (`ACP:599–609`); `BC` especifica candidate→receipt→accepted e release
gates (`BC:62–109`). `ACP` diz que o retorno compila para `Contribution` com `Artifact` imutável e pede
um submission manifest ainda não ratificado (`ACP:369–383`); `BC` aprofunda `WorkArtifact`,
`WorkPublicationCandidate`, `WorkSubmission` e `ChangeSetArtifact` (`BC:41–60`, `BC:534–551`).

Essa sobreposição é exatamente a forma esperada de uma interface: o consumidor semântico declara a
propriedade de que precisa; o contrato de infraestrutura especifica como realizá-la. A própria frase
de relação de `BC` confirma que ele “aprofunda a fronteira mais estreita” e pode retroalimentar o outro
discovery (`BC:28–39`). Portanto, encontrar o mesmo substantivo nos dois arquivos não demonstra que
todos os seus invariantes têm o mesmo owner.

## A alternativa concreta

Manter os dois arquivos e acrescentar, sem mover seus conteúdos:

1. uma matriz `claim/interface -> owner documental -> termo exportado -> termo consumido -> status ->
   evidência`, consistente com a matriz de autoridade que `ACP` já exige (`ACP:489–508`);
2. links bidirecionais nas seções de relacionamento;
3. uma tabela de mapping entre `activity`/`judgment`/`Contribution` de `ACP` e
   `WorkAssignment`/`OutputContract`/`WorkSubmission`/`ReviewSubmission` de `BC` (`ACP:303–328`,
   `ACP:369–398`; `BC:534–551`);
4. um gate de compatibilidade cruzada: nenhuma promoção de um documento pode contradizer a versão
   pinada da interface do outro, sem exigir que ambos sejam promovidos no mesmo commit.

Essa proposta satisfaz a necessidade de consistência sem impor \(G_A\land G_B\) como gate único.

## Tentativas de falsear esta tese

### F1 — “Os dois textos mudam sempre juntos”

**Predição da tese pró-fusão:** para toda mudança material \(m\), \(a(m)\leftrightarrow b(m)\).

**Teste:** classificar o backlog dos dois arquivos e procurar uma mudança exclusiva. Os exemplos de
roles/trust anchor em `ACP` (`ACP:253–258`, `ACP:165–189`) e de blob integrity/retention em `BC`
(`BC:553–568`) são contraexemplos. Portanto, a proposição universal é refutada na versão atual.

### F2 — “Os gates são na prática equivalentes”

**Predição pró-fusão:** \(G_A\leftrightarrow G_B\).

**Teste:** uma execução pode provar recovery candidate/receipt sob crash (`BC:570–580`) sem decidir
ownership da compilação ou trust anchor (`ACP:437–485`); inversamente, uma decisão documental de
ownership não prova integridade do blob ou atomicidade de promotion (`BC:553–568`). Há testemunhas
nos dois sentidos; equivalência não está demonstrada.

### F3 — “Separar produz contradições silenciosas”

Este é o ataque mais forte à minha posição. De fato, `ACP` ainda propõe `Contribution`/`Artifact`
(`ACP:377–383`) enquanto `BC` introduz uma taxonomia mais fina (`BC:534–551`), e os dois tratam de
routing em níveis diferentes (`ACP:599–609`; `BC:345–371`). Se mantidos sem versionamento cruzado,
podem divergir.

**Resultado:** o risco é confirmado, mas não refuta separação; refuta separação **sem contrato de
interface**. A matriz e o gate cruzado propostos acima tornam divergência detectável. A tese seria
refutada apenas se um experimento mostrasse que mappings/version pins não conseguem detectar
incompatibilidades que um arquivo único detectaria.

### F4 — “Um único arquivo melhora descobribilidade”

É plausível, mas não está medido nos materiais. Uma página-index com links resolve descobribilidade
sem fundir lifecycles. A tese deve ser revista se testes com leitores demonstrarem simultaneamente:
(i) falhas materiais de entendimento usando index + mappings, (ii) melhora com arquivo único e
(iii) custo de revisão/promoção não maior. Nenhum desses dados aparece nos dois discoveries.

## Condições que fariam a junção racional

Eu mudaria de posição se todas as condições abaixo fossem demonstradas:

1. escopo único reescrito sem a tensão “ciclo completo” versus “somente Work Bus”;
2. um único owner e um único lifecycle de revisão/promoção aprovados;
3. equivalência ou dependência obrigatória comprovada entre \(G_A\) e \(G_B\);
4. mapping completo e estável entre atividades/julgamentos e operações/capabilities do bus;
5. evidência de que a maioria dominante das mudanças materiais cruza a fronteira, tornando a
   separação mais custosa que a fusão;
6. preservação explícita da proveniência das reviews por seção/claim.

Na versão lida, os textos não satisfazem essas condições: mantêm perguntas e schemas candidatos,
gates distintos e fora-de-escopo diferentes (`ACP:437–485`, `ACP:724–751`; `BC:553–568`,
`BC:617–642`).

## Veredicto

**Rejeitar a junção agora.** Manter `agents-communication-protocols` como discovery da semântica e
governança do ciclo de trabalho; manter `bus-contracts` como discovery da fronteira operacional de
publicação, materialização, roteamento e consumo. Integrá-los por contrato versionado, matriz de
traceabilidade e revisão cruzada. Esse arranjo respeita o que os próprios textos declaram, evita um
gate conjuntivo artificial e transforma divergências em testes de interface em vez de escondê-las em
um documento monolítico.
