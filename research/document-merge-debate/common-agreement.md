# Acordo comum — relação entre `agents-communication-protocols` e `bus-contracts`

## Participantes e decisão

Participantes:

- posição inicial pró-junção: `/root/defende_juncao`;
- posição inicial contra a junção: `/root/rejeita_juncao`.

**Decisão comum:** não fundir os dois discoveries agora. Manter ACP como owner da intenção e da
semântica do ciclo de trabalho e BC como owner dos contratos de publicação, materialização, routing e
consumo. Criar, como trabalho posterior sujeito a review, um artefato integrador pequeno e versionado,
normativo **somente** para mappings e invariantes cruzados \(X\). Preservar gates locais e aplicar um
gate cruzado apenas quando uma mudança tocar \(X\).

Este não é um falso consenso entre “juntar” e “não juntar”. A recomendação operacional presente é
inequivocamente **não juntar agora**. A posição pró-junção retirou sua recomendação imediata porque a
evidência demonstra a necessidade de autoridade para a interface, mas não demonstra que essa
autoridade deva conter os dois domínios completos nem compartilhar um único gate editorial.

## Fundamentos aceitos por ambos

1. **Existe acoplamento semântico real.** BC se declara aprofundamento da fronteira de assignment,
   input, submission, artifact, routing e consumo dentro do problema mais amplo de ACP (BC, linhas
   28–39). ACP já exige contratos de input/submission/review e pesquisa da fronteira bus–journal (ACP,
   linhas 369–398 e 599–609).
2. **Testes apenas locais são insuficientes para invariantes cruzados.** Um review pode satisfazer
   receipt e routing de BC e ainda violar a `JudgmentRound` selada obrigatória de ACP (BC, linhas
   96–109; ACP, linhas 347–367). Logo, a interface requer owner e probes próprios.
3. **Os domínios não co-mudam universalmente.** Role/trust anchor/julgamento podem mudar ACP sem mudar
   BC (ACP, linhas 165–189, 253–258 e 330–367); threshold inline/artifact, integridade de blobs e
   retenção podem mudar BC sem mudar ACP (BC, linhas 553–568). Portanto, um gate único para toda
   mudança seria acoplamento não justificado.
4. **Os gates atuais não são equivalentes.** ACP exige decisões de ownership, profiles, recipes,
   independência e autoridade do `DispatchSpec` (ACP, linhas 735–751). BC exige recovery de
   candidate/receipt, release gates, evolução de `RoutingState`, changesets isolados e matriz de
   capabilities (BC, linhas 626–642). O corpus não prova \(G_A\leftrightarrow G_B\).
5. **A taxonomia cruzada ainda está incompleta.** ACP propõe Activity, Contribution, Artifact,
   GroupResult e operações de decisão (ACP, linhas 303–367 e 369–398); BC propõe WorkAssignment,
   WorkSubmission, ReviewSubmission e operações `submit_*`, deixando decisão humana no command plane
   (BC, linhas 385–474 e 534–551). Essa lacuna precisa ficar visível e fail-closed.
6. **A proveniência de review deve ser preservada.** BC possui review clean-room/remediation próprio
   (BCR, linhas 3–46), sem artefato equivalente encontrado no diretório de ACP lido. Qualquer
   integração deve vincular review a claim/seção/versão, sem atribuir cobertura retroativa.

## Modelo de gates acordado

Para uma mudança \(m\), sejam:

- \(a(m)\): altera conteúdo pertencente a ACP;
- \(b(m)\): altera conteúdo pertencente a BC;
- \(x(m)\): altera mapping ou invariante cruzado;
- \(G_A,G_B,G_X\): gates local de ACP, local de BC e de interface.

O princípio é:

\[
G(m)=
\begin{cases}
G_A(m), & a(m)\land\neg b(m)\land\neg x(m)\\
G_B(m), & b(m)\land\neg a(m)\land\neg x(m)\\
G_A(m)\land G_B(m), & a(m)\land b(m)\land\neg x(m)\\
G_A(m)\land G_B(m)\land G_X(m), & x(m).
\end{cases}
\]

Se uma mudança tocar materialmente os dois domínios, ela é classificada como \(x(m)\), salvo prova de
que são alterações locais independentes. Classificação ambígua falha fechada e exige adjudicação; não
é normalizada silenciosamente para “local”.

## Estatuto do futuro artefato integrador

O integrador evita ser uma terceira fonte concorrente pelas seguintes restrições:

- **autoridade estreita:** é owner apenas da função parcial versionada
  \(f:A\rightharpoonup B\) e dos predicados \(X\); ACP e BC continuam owners dos conceitos locais;
- **sem duplicação normativa:** não reexplica definições internas; referencia seção e versão/digest de
  cada owner;
- **linha tipada:** cada entrada contém ao menos `interface_id`, `protocol_owner_ref`, `bus_owner_ref`,
  `mapping_kind`, `cross_invariant`, versões/digests, `status`, `compatibility`, `probe_ref` e
  `decision_ref`;
- **fail-closed:** termo sem mapping, pin divergente ou probe obrigatório ausente resulta em
  `unresolved`, `stale` ou `failed`, nunca compatibilidade inferida;
- **precedência fatorada:** ACP decide intenção/semântica de trabalho; BC decide
  publicação/materialização/routing/consumo; claim que não possa ser fatorada é genuinamente \(X\) e
  requer decisão conjunta;
- **lifecycle próprio e limitado:** mudanças em \(X\) exigem review dos dois domínios e probe cruzado;
  mudança local que preserva pins e invariantes não reabre o outro gate;
- **estado inicial draft:** só se torna normativo para \(X\) depois de review independente e aceitação
  explícita dos dois owners; antes disso, não autoriza promoção.

A criação desse integrador não está sendo fingida como concluída neste acordo. Este texto decide o
seu estatuto; schema final, população da matriz, owners humanos e probes ainda exigem trabalho e
review.

## Condições para reconsiderar junção posterior

A junção editorial só deve voltar à pauta depois de existir evidência sobre:

1. mapping completo e estável das taxonomias e superfícies de autoridade;
2. densidade de \(X\) e histórico de co-mudança material entre ACP e BC;
3. custo observado de drift/sincronização versus custo de navegação e review de um artefato maior;
4. desempenho de leitores/revisores em experimento cego comparando documentos separados + integrador
   com um protótipo consolidado;
5. owner e lifecycle de revisão/promoção aprovados para eventual artefato único;
6. preservação verificável da proveniência de reviews por seção e claim;
7. demonstração de que consolidação não transforma todo avanço em \(G_A\land G_B\) sem necessidade.

Não se adota agora um limiar numérico arbitrário. Métricas e thresholds devem ser registrados antes
do experimento para evitar escolha oportunista após observar os resultados.

## Divergência residual registrada

Não resta divergência sobre a ação atual. Resta uma hipótese empírica aberta: após implantação da
interface versionada, a densidade/custo de \(X\) pode revelar que consolidação futura é mais barata, ou
que a separação modular é estável e suficiente. Ambos aceitam que essa questão seja decidida por
evidência, não pela posição inicial de cada participante.

## Aceitação explícita do mesmo texto

- `/root/defende_juncao`: **ACEITO**, sujeito à confirmação de que o arquivo revisado permanece
  byte-a-byte/semanticamente igual ao texto que revisei após a rodada final.
- `/root/rejeita_juncao`: **ACEITO** após leitura integral e correção da partição de casos em
  `G(m)`; o caso de alterações locais independentes nos dois domínios exige (G_A\land G_B), sem
  acionar (G_X).
