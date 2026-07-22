---
tags: [agents-communication-infra, discovery, protocols, research, review, workers]
node_type: discovery
is_session: false
layer: [application, orchestration]
nature: [research, design]
status: draft
version: 0.1.0
last_updated: 2026-07-22
---

# Agents Communication Protocols — Discovery

## Objetivo

Este discovery deve definir como agentes pesquisam, discutem, sintetizam, executam tarefas,
revisam artefatos, solicitam correções e aprovam um resultado usando a infraestrutura de
comunicação entre agentes.

O problema não é apenas transportar mensagens. Precisamos preservar a independência das avaliações,
registrar versões e discussões sem sobrescrever evidência, limitar ciclos de correção e garantir que
cada aprovação se refira à versão exata que foi analisada.

O discovery também deve decidir se esses protocolos pertencem integralmente a
`agents-communication-infra` ou se a infraestrutura deve cuidar apenas de transporte e persistência,
enquanto uma feature separada governa pesquisa, execução e revisão.

## Contexto

O repositório já possui skills para pesquisa, revisão, estratégia de subagentes, registro de
dispatches, criação de SPEC e implementação. Também possui uma proposta de barramento, journal,
artefatos imutáveis, receipts e geração determinística de testes. Essas superfícies ainda não formam
um protocolo único e explícito para o ciclo completo de trabalho.

As conversas que motivaram este discovery indicam, entre outras, as seguintes necessidades:

- relatórios individuais de pesquisa são imutáveis;
- discussões geram novos relatórios, também registrados;
- uma síntese possui um escritor responsável e outro agente que a revisa;
- workers podem receber uma ou mais tarefas coerentes;
- a tarefa aponta para trechos autoritativos da SPEC, em vez de copiar critérios inventados pelo pai;
- o escopo de escrita é declarado por caminhos e permite criação de arquivos;
- cada worker possui revisão local com ciclos limitados;
- feedback de revisão é publicado pelo barramento e persistido pelo journal;
- a revisão final pode reabrir um worker, um grupo ou toda a integração;
- nenhuma aprovação é produzida automaticamente quando o limite de ciclos é atingido.

## Hipótese de superfície única para skills e agentes

Este discovery deve testar uma superfície única: o usuário invoca uma skill ou agente existente,
e a estratégia de subagentes transforma essa invocação em um dispatch governado. O usuário não
deveria precisar operar separadamente uma skill, um registro de protocolos e o runtime.

A hipótese de integração é um **Skill Execution Profile** versionado. Ele não seria um novo
registro de protocolos em paralelo. Seria uma compilação registrada que liga uma versão exata da
skill ou agente, junto com os digests de agentes e dependências que ela referencia, ao vocabulário
existente de `recipe_ref` e `DispatchSpec`. O perfil declararia como instruções já existentes são
mapeadas para grupos, seats, entradas, permissões, comunicação e ciclos; o `DispatchSpec`
confirmado continuaria sendo a autoridade executável de cada run.

Esta é uma hipótese de discovery, não um schema ratificado. Recipes arbitrárias e workflows que
alteram arquivos continuam fora do escopo da SPEC atual de `agents-communication-infra`; sua
promoção exige evidência, mudança de governança e atualização das autoridades aplicáveis.

### Ownership e precedência propostos

A skill permanece dona da intenção de domínio, dos entregáveis, das fontes autoritativas e do que
significa trabalho de qualidade. O perfil possui somente a compilação dessas instruções para:

- bundles coerentes de trabalho e suas dependências;
- roles e quantidades de workers e reviewers;
- mapeamento de entradas para cada agente;
- capabilities, ferramentas, permissões e ownership de caminhos;
- mensagens, visibilidade, review, rework e integração.

Cada mapeamento do perfil deve apontar para sua origem na skill ou em outra autoridade exata e
declarar uma de quatro disposições: `preserved`, `compiled`, `superseded` ou `unsupported`. Uma
instrução material marcada como `unsupported` bloqueia o dispatch. `superseded` exige autoridade
explícita e não pode ser inferido pelo orquestrador. Depois da confirmação, os bytes e digests do
`DispatchSpec`, e não o perfil reutilizável, governam aquela execução.

O perfil deve possuir um manifesto de dependências, não apenas o digest de `SKILL.md`. Mudanças em
agentes referenciados, templates, skills auxiliares, taxonomias, contratos ou recipes podem tornar
o perfil incompatível ou stale. O discovery deve definir quais mudanças permitem revalidação e
quais exigem uma nova proposta e confirmação.

### Onboarding quando o perfil não existe ou está stale

Na ausência de perfil compatível, a superfície poderia invocar **um único helper read-only e não
confiável** para propor a compilação. O helper não executa a skill, não registra a própria proposta,
não amplia permissões e não introduz comandos confiáveis. Antes de qualquer efeito, o usuário vê:

1. as interpretações e os pontos não suportados;
2. o perfil reutilizável proposto;
3. o dispatch concreto, incluindo agentes, bundles, caminhos, dependências e limites;
4. a escolha entre usar a proposta somente uma vez ou registrar aquele digest exato.

Decompor automaticamente qualquer skill continua sendo uma hipótese não provada. A proposta do
helper é material para confirmação humana, não prova de compatibilidade.

### Identidade e contrato de cada agente

O perfil e sua compilação devem preservar, sem colapsar, as camadas de identidade já existentes ou
planejadas:

- `agent_ref`: definição executável e versionada do agente;
- `agent_name`: persona opcional, nullable e não única; nunca identidade de execução;
- `role`: vocabulário fechado hoje em `explorer`, `synthesizer`, `skeptic`, `writer`, `auditor`,
  `planner` e `coder`; extensibilidade futura deve ser testada antes de ser promovida;
- `angle`: posição no eixo de anti-bias, preservando seu significado atual e obrigatoriedade em
  grupos com `n >= 2`;
- IDs distintos de seat, instância e attempt, sem deduzi-los de role ou persona;
- modelo, budget de tokens e outros recursos, prompt inicial, ferramentas/capabilities e
  permissões efetivas.

O perfil pode declarar defaults e constraints. O dispatch concreto resolve os valores exatos para
cada seat antes da confirmação. Um perfil não pode apagar diferenças relevantes entre o agente
executável, a persona escolhida e a identidade autenticada da tentativa.

### Decomposição e distribuição de trabalho

`worker_count` declara capacidade, mas não define sozinho o significado da distribuição. O perfil
deve escolher ou permitir um modo explícito, por exemplo `partitioned` ou `independent_replicas`.
No modo `partitioned`, o orquestrador analisa a invocação antes da confirmação, forma bundles
coerentes com um ou mais arquivos, declara dependências e atribui ownership exclusivo de cada
caminho. Um agente pode ser dono de vários arquivos relacionados; nenhum caminho pode ter dois
escritores concorrentes.

A proposta deve mostrar a atribuição exata. O orquestrador pode usar menos workers que o limite
pedido quando não houver paralelismo útil e não pode fragmentar trabalho artificialmente apenas para
ocupar seats. Sob o P5 atual, writers particionados sem tensão entre si devem compilar como grupos
singleton conectados por dependências, e não como um único grupo com `n > 1`.

O runtime deve impedir que um agente filho criado durante a execução escape do grafo confirmado.
Spawn aninhado deve ser desabilitado ou interceptado e transformado em solicitação ao orquestrador;
a helper rule atual não pode funcionar como bypass de ownership, permissão ou confirmação.

Transferência de ownership deve ser explícita. Arquivos compartilhados ou mudanças de integração
precisam de uma única autoridade de materialização/integração. Toda edição de integração deve
produzir uma nova versão e invalidar os pareceres cujo subject foi alterado.

### Input contracts, submissões e review

O `input_contract` proposto não valida se o artefato de domínio está correto. Ele verifica, antes de
invocar um agente, se estão presentes as entradas exatas que a skill exige: objetivo, referências e
versões autoritativas, outputs upstream, caminhos-alvo, permissões e formato esperado de retorno.
Esses requisitos são derivados da skill e rastreados pelo perfil; a infraestrutura apenas valida o
contrato compilado.

O retorno de um worker deve compilar para a `Contribution` tipada existente e para um `Artifact`
imutável que manifeste, no mínimo, os caminhos, hashes e base snapshot submetidos. Imutabilidade
aqui significa que a submissão histórica não é sobrescrita; o arquivo de trabalho pode ser corrigido,
mas a correção cria outro manifesto. Reviewers avaliam uma submissão exata, e seus pareceres ficam
vinculados ao respectivo manifesto e versão.

`reviewer_count` é independente de `worker_count`. Uma implementação com três writers pode ter um,
três ou outro número confirmado de reviewers. Reviewers em um grupo com `n >= 2` permanecem
selados até publicar suas posições iniciais e precisam ser tensionados conforme P5; suas diferenças
não podem ser justificadas apenas pela partição dos arquivos. O `GroupResult` de review é evidência
para a decisão. Sob P12, o `final_approver` continua separado e não pode ser membro do grupo de
trabalho. Atingir o limite de rework encerra como não resolvido; nunca aprova automaticamente.

### Recipes reutilizáveis, não um protocolo por skill

O alvo é um conjunto pequeno de patterns reutilizáveis entre skills, por exemplo autoria
particionada seguida de review independente, ou pesquisa independente seguida de síntese. O perfil
seleciona e parametriza uma recipe existente; uma skill não recebe automaticamente um protocolo
exclusivo. Se uma skill exigir uma interação que a álgebra atual não expressa, isso é evidência para
avaliar uma nova recipe ou primitive, não autoriza um branch ad hoc no kernel.

Todo planejamento contextual deve acontecer antes da confirmação. Descobrir depois um novo
artefato, ampliar caminhos, trocar uma autoridade ou alterar materialmente bundles, agents,
permissões ou policies suspende a execução e exige uma proposta emendada e nova confirmação.

### Exemplo candidato: `domainspec-spec-feature`

Uma invocação poderia pedir três agentes de implementação que produzam coletivamente o pacote:

- writer 1: `SPEC.md`, `domain.md` e `rules.md`;
- writer 2: `events.md`, `states.md` e `workflows.md`;
- writer 3: `architecture.md`, `interfaces.md` e os demais aspectos coerentes identificados;
- uma autoridade explícita integra `glossary.md`, links e ajustes transversais quando esses arquivos
  dependerem do pacote completo;
- reviewers independentes avaliam os manifests exatos e o pacote integrado; o `final_approver`
  toma a decisão final conforme P12.

Cada caminho tem um writer por vez, embora cada writer possua vários arquivos. O orquestrador
decide a divisão concreta por coerência, dependências, isolamento de escrita e carga; o usuário vê
essa divisão antes de confirmar.

A skill atual, porém, manda escrever um documento por vez, revisá-lo imediatamente e reutilizar o
mesmo helper no re-check. Portanto, o exemplo acima não é uma execução fiel da skill atual sem
mudanças: o perfil teria de marcar a orquestração embutida como explicitamente `superseded`, ao
mesmo tempo que preserva sua semântica de domínio e seus critérios de qualidade. Isso requer
alteração da skill/governança e promoção do workflow mutante antes de se tornar comportamento live.

## Perguntas principais

1. Qual feature é dona dos protocolos de pesquisa, síntese, trabalho e revisão?
2. Qual é o conteúdo mínimo de uma atribuição de trabalho?
3. Como uma tarefa referencia partes da SPEC sem reinterpretar seus critérios?
4. Como caminhos autorizam criação e alteração sem permitir escrita fora do escopo?
5. Exclusão e movimentação exigem uma autorização separada?
6. Quando um worker pode receber várias tarefas e quando elas precisam ser separadas?
7. Como dividir a criação de uma SPEC entre agentes sem gerar divergência entre seus arquivos?
8. Como relatórios individuais, discussões, sínteses e revisões são versionados e relacionados?
9. Qual informação deve ser fornecida por um agente e qual deve ser registrada automaticamente?
10. Qual é o parecer mínimo que um revisor precisa publicar?
11. Como funcionam os ciclos escritor–revisor, worker–revisor e integração–revisores finais?
12. Como alterações invalidam aprovações anteriores e determinam o alcance da nova revisão?
13. Como revisores finais solicitam trabalho a grupos específicos sem se tornarem orquestradores?
14. Quais mensagens são apenas transporte e quais fatos precisam ser persistidos no journal?
15. O que acontece quando um ciclo não converge dentro do limite?
16. Qual é a forma mínima do `Skill Execution Profile` e como cada mapeamento preserva sua origem?
17. Como detectar staleness quando mudam skill, agente, template, recipe ou outra dependência?
18. Quais recipes atendem várias skills sem criar branches por skill no kernel?
19. Como o orquestrador propõe bundles e assignments reproduzíveis sem inventar requisitos?
20. Quais mudanças tardias são materiais e obrigam uma nova confirmação?

## Pesquisas necessárias

### 1. Inventário do funcionamento atual

Levantar o comportamento real das skills e dos registros existentes:

- [research](../../../../../.claude/skills/research/SKILL.md);
- [review](../../../../../.claude/skills/review/SKILL.md);
- [domainspec-subagents-strategy](../../../../../.claude/skills/domainspec-subagents-strategy/SKILL.md);
- [register-dispatch](../../../../../.claude/skills/register-dispatch/SKILL.md);
- skills e agentes de discovery, SPEC e implementação;
- registros reais em `telemetry/agents/`;
- [test-derivation-engine](../../../../../tools/test-derivation-engine/README.md).

A pesquisa deve distinguir regras efetivamente aplicadas, regras apenas documentadas e convenções
que hoje dependem do agente pai.

### 2. Independência, discussão e decisão coletiva

Pesquisar evidência sobre:

- julgamento independente antes da interação;
- feedback controlado e métodos semelhantes ao Delphi;
- risco de conformidade, cascata informacional e groupthink;
- discussão depois do registro das posições iniciais;
- nova decisão privada depois da discussão;
- unanimidade, objeção bloqueante e tratamento de dissenso;
- limites de ciclos como controle de custo, não como aprovação automática.

O resultado deve recomendar quando agentes podem conversar e quais posições precisam permanecer
registradas antes e depois da conversa.

### 3. Protocolo de pesquisa e síntese

Comparar pelo menos estes modos:

1. pesquisadores independentes sem discussão, seguidos por um sintetizador;
2. pesquisadores registram seus relatórios, discutem e publicam um relatório complementar;
3. dois sintetizadores produzem versões independentes antes de um deles integrar;
4. um sintetizador escreve e outro executa um ciclo de revisão da síntese.

A pesquisa deve avaliar qualidade, preservação de dissenso, custo, número de ciclos, facilidade de
auditoria e risco de o sintetizador omitir evidências.

### 4. Granularidade das atribuições de trabalho

Investigar como decompor trabalho sem usar nem tarefas pequenas demais nem pedidos abertos como
“implemente todo o `architecture.md`”. Devem ser avaliados:

- uma tarefa por worker;
- várias tarefas relacionadas por worker;
- uma capability ou fatia vertical por worker;
- um arquivo por agente na criação de SPEC;
- conjuntos de arquivos relacionados com um responsável único;
- planejamento obrigatório antes de executar uma arquitetura ampla.

O objetivo é propor critérios de coesão e revisabilidade, sem fazer o agente pai inventar requisitos
que deveriam vir da SPEC.

### 5. Escopo de escrita por caminhos

Pesquisar e testar um contrato de escrita baseado em caminhos, incluindo:

- criação e alteração dentro de raízes autorizadas;
- autorização separada para excluir ou mover;
- contenção por caminho absoluto resolvido;
- traversal e symlinks;
- caminhos sobrepostos entre workers;
- ownership de arquivos compartilhados;
- comportamento quando uma implementação precisa sair do escopo inicialmente concedido.

### 6. Contrato mínimo de revisão

Determinar o menor payload de revisão que continue auditável. A hipótese inicial é que o revisor
forneça apenas:

- referência e hash do artefato analisado;
- parecer `aprovado` ou `precisa de correção`;
- problema e evidência;
- indicação de que o problema impede ou não a aprovação.

Identidade, modelo/provider, tarefa, ciclo, horário, prompt, arquivos alterados, testes executados e
estado do finding devem ser avaliados como metadados capturados automaticamente, não campos que o
revisor precisa preencher manualmente.

### 7. Versionamento, discussão e invalidação

Definir como representar:

- relatório original e relatório complementar da discussão;
- posição inicial e posição final de cada participante;
- versões sucessivas da síntese ou implementação;
- parecer aplicável a uma versão exata;
- correção que fecha, refuta ou mantém um problema;
- mudança local que invalida apenas um parecer;
- mudança transversal que reabre vários grupos;
- risco aceito somente por autoridade autorizada.

### 8. Barramento, journal e roteamento

Pesquisar o contrato entre transporte e autoridade:

- o barramento entrega atribuições, findings e solicitações de correção;
- o journal persiste submissões, versões, discussões, pareceres, reaberturas e aprovações;
- agentes não escrevem diretamente o estado oficial da tarefa;
- mensagens repetidas são idempotentes;
- visibilidade é limitada ao worker, revisores, sintetizador e agente pai apropriados;
- o revisor final emite uma solicitação estruturada, enquanto o orquestrador valida e agenda o
  trabalho.

### 9. Ciclos locais e revisão final

Comparar limites separados para:

- escritor e revisor da síntese;
- worker e revisor local;
- integração e revisores finais.

A pesquisa deve definir convergência, escalonamento, troca de reviewer, reaproveitamento do mesmo
reviewer e efeito de atingir o limite. A hipótese inicial é que o limite encerre o fluxo como não
resolvido e nunca reduza o critério de aprovação.

### 10. Experimentos de validação

Antes da promoção para SPEC, executar probes pequenos e reproduzíveis:

- pesquisa com e sem discussão posterior;
- um versus dois sintetizadores;
- criação coordenada de uma SPEC com ownership por arquivo ou por conjunto coerente;
- dois workers tentando escrever em caminhos sobrepostos;
- reviewer avaliando uma versão que muda depois do parecer;
- revisão final reabrindo somente um grupo e depois vários grupos;
- repetição de mensagens e recuperação após interrupção;
- término do limite de ciclos com objeção ainda aberta.

Adicionar probes focados na superfície única e no perfil candidato:

- compilar duas skills diferentes para a mesma recipe reutilizável, sem branch por skill no kernel;
- gerar um perfil para uma skill não registrada e medir correções humanas, omissões materiais e
  falsos `preserved`/`compiled`;
- alterar separadamente `SKILL.md`, agente referenciado, template e recipe, verificando se o perfil
  correto fica stale;
- comparar uma autoria DomainSpec sequencial fiel à skill atual com uma proposta particionada em
  três bundles, medindo consistência transversal, rework, custo e tempo;
- confirmar que writers particionados viram grupos singleton sob P5 e que reviewers tensionados
  permanecem selados até suas posições iniciais;
- tentar spawn de child agent, escrita sobreposta, transferência implícita de ownership e ampliação
  tardia de paths, verificando bloqueio ou retorno ao gate;
- modificar um arquivo durante integração e demonstrar invalidação somente dos reviews aplicáveis;
- atingir o loop ceiling com finding aberto e demonstrar que `GroupResult` não vira aprovação.

## Resultados esperados do discovery

O discovery deve produzir recomendações, não código. Seu resultado precisa incluir:

- decisão de ownership entre infraestrutura de comunicação e protocolo de trabalho;
- vocabulário mínimo;
- contratos mínimos de atribuição, submissão, discussão, revisão e rework;
- diagramas dos fluxos de pesquisa e workers;
- regras de versionamento e invalidação;
- política de caminhos autorizados;
- política de ciclos e escalonamento;
- fronteira entre barramento e journal;
- experimentos necessários antes da SPEC;
- mapa dos documentos, skills e componentes que precisariam mudar.
- proposta do `Skill Execution Profile`, incluindo manifesto de dependências, staleness e matriz de
  rastreabilidade `preserved | compiled | superseded | unsupported`;
- catálogo mínimo de recipes reutilizáveis e lacunas da álgebra atual;
- contrato de onboarding read-only para skills sem perfil e evidência sobre a viabilidade de
  decomposição automática;
- regras propostas para bundles, ownership, integração, spawn aninhado e mudanças tardias;
- resultado do piloto `domainspec-spec-feature`, incluindo as mudanças de skill e governança
  necessárias antes de qualquer promoção.

## Fora de escopo neste momento

- alterar a SPEC existente;
- implementar o runtime ou o barramento;
- mudar as skills atuais;
- escolher valores definitivos para todos os limites de ciclo;
- criar schemas finais de eventos ou banco de dados;
- assumir que consenso implica correção;
- assumir que modelos ou providers diferentes garantem independência.

## Critério para avançar

O discovery poderá ser promovido somente depois de revisão independente que confirme:

- cobertura dos fluxos de pesquisa e execução;
- separação clara entre transporte e autoridade;
- ausência de campos sem necessidade demonstrada;
- ausência de decisões inventadas pelo agente pai;
- tratamento explícito de versão, rework, invalidação e não convergência;
- recomendação clara sobre a feature responsável pelo protocolo.
