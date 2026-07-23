# Steelman da tese pró-junção e resposta — rodada 1

## Objeto lido

Leitura integral de
`docs/features/agents-communication-infra/discovery/document-merge-debate/defesa-juncao.md`
(337 linhas), confrontada com
`docs/features/agents-communication-infra/discovery/document-unification-debate/reject-unification.md`.

## Steelman: os argumentos pró-junção mais fortes

1. **BC é especialização declarada de ACP, não apenas tema vizinho.** BC diz que ACP cobre o fluxo
   completo e que ele próprio aprofunda a fronteira de assignment, input, submission, artifact,
   routing e consumo (`BC:28–39`). ACP já exige contratos de submission/review e a fronteira
   bus–journal nos seus resultados (`ACP:369–398`, `ACP:599–609`, `ACP:689–702`). Portanto, existe
   sobreposição intencional de deliverable.
2. **Há invariantes cruzados que testes locais não provam.** Se \(P\) são invariantes de protocolo,
   \(B\) os de bus e \(X\) os de interface, então provar
   \(\bigwedge(P\setminus X)\land\bigwedge(B\setminus X)\) não prova \(\bigwedge X\). O
   contraexemplo mais forte é um review aceito e corretamente roteado pelo bus que agrega duas
   posições sem a `JudgmentRound` selada obrigatória: os invariantes locais de receipt/routing podem
   passar e a higiene global falhar (`ACP:347–367`; `BC:96–109`).
3. **As taxonomias ainda não têm mapping total.** ACP usa Activity, Contribution, Artifact e
   GroupResult; BC introduz WorkAssignment, WorkPublicationCandidate, WorkSubmission,
   ReviewSubmission e ChangeSetArtifact (`ACP:303–328`, `ACP:369–383`; `BC:41–60`, `BC:534–551`).
   Duas formulações sem autoridade de interface permitem drift e adjudicação tardia.
4. **O review de BC demonstra que detalhes locais afetam garantias globais.** Os oito findings
   clean-room incluíram release prematuro, plano/estado confundidos, consumo ausente e lifecycle
   colapsado (`BCR:17–41`). As remediações concretizam ownership, inputs exatos, invalidação e
   separação entre evidência e resultado oficial de ACP (`ACP:281–301`, `ACP:347–383`,
   `ACP:586–597`; `BC:96–109`, `BC:172–194`, `BC:395–419`, `BC:517–532`).
5. **Uma junção modular não implica monólito runtime.** A tese oposta preserva explicitamente as
   fronteiras entre Work Bus, command plane, handoff, projection e knowledge futuro
   (`BC:373–474`) e propõe seções/owners internos distintos, não uma concatenação bruta.

Esses pontos provam a necessidade de uma autoridade e de probes ponta a ponta para \(X\). Eles são
mais fortes que uma justificativa editorial por redução do número de arquivos.

## Teste da minha tese contra minhas condições de falsificação

Minha tese original dizia que eu aceitaria junção se houvesse escopo/lifecycle único, equivalência dos
gates, mapping completo, co-mudança dominante e preservação de provenance. A tese oposta não apresenta
essas provas:

- reconhece que os níveis arquitetura/domínio e aplicação/orquestração são diferentes e que o risco
  de um arquivo com mais de mil linhas precisa de experimento (`defesa-juncao.md:231–257`);
- admite que \(N\), custo adicional de navegação/review, e \(R\), custo da refatoração, não foram
  medidos (`defesa-juncao.md:200–229`);
- propõe como teste futuro medir dependências, vocabulário, review cego, owners/ciclos e a suficiência
  de matriz de rastreabilidade (`defesa-juncao.md:285–304`);
- não refuta os contraexemplos de mudança local: roles/trust anchor podem mudar só em ACP
  (`ACP:165–189`, `ACP:253–258`), enquanto blob integrity/retention podem mudar só em BC
  (`BC:553–568`).

Portanto, as condições para fundir **agora** não foram satisfeitas. Porém, o argumento de \(X\) refuta
uma versão fraca da minha alternativa: uma página-index meramente informativa não basta para impedir
que ambos os documentos passem localmente enquanto uma interface global falha.

## Revisão da posição

Aceito a seguinte convergência:

1. não fundir ACP e BC agora;
2. preservar gates locais independentes \(G_A\) e \(G_B\);
3. criar um terceiro artefato cuja autoridade seja **normativa apenas sobre compatibilidade de
   interface \(X\)**;
4. exigir um gate cruzado \(G_X\) somente para alterações/promotions que toquem \(X\), sem transformar
   toda promoção em \(G_A\land G_B\);
5. reconsiderar consolidação após mappings e probes mensuráveis.

O gate correto passa a ser, para uma mudança \(m\):

\[
G(m)=
\begin{cases}
G_A(m), & a(m)\land\neg x(m)\\
G_B(m), & b(m)\land\neg x(m)\\
G_A(m)\land G_B(m)\land G_X(m), & x(m)
\end{cases}
\]

onde \(x(m)\) significa que a mudança altera um invariante/mapping cruzado. Isso preserva promoção
local e fecha a lacuna lógica dos invariantes de interface.

## Estatuto exato do artefato integrador

Para não virar uma terceira verdade concorrente, o artefato deve seguir estas restrições:

- **Autoridade positiva limitada:** é a única autoridade para mappings e invariantes que mencionem
  termos dos dois lados; não é autoridade sobre semântica interna de ACP nem implementação interna de
  BC.
- **Sem duplicação normativa:** não reexplica conceitos locais. Cada célula aponta para seção + versão
  ou digest do documento owner.
- **Schema por linha:** `interface_id`, `protocol_owner_ref`, `bus_owner_ref`, `mapping_kind`,
  `cross_invariant`, `protocol_version`, `bus_version`, `status`, `compatibility`, `probe_ref` e
  `decision_ref`.
- **Fail closed:** termo sem mapping, versão divergente ou probe obrigatório ausente resulta em
  `compatibility: unresolved|stale|failed`, nunca equivalência inferida.
- **Regra de conflito:** ACP é canônico para intenção/semântica de trabalho; BC é canônico para
  publicação/materialização/routing/consumo. Se uma claim não puder ser fatorada nessa precedência,
  ela é genuinamente \(X\) e permanece `unresolved` até decisão conjunta registrada no próprio
  artefato.
- **Lifecycle:** qualquer mudança em uma linha de \(X\) exige revisão pelos dois domínios e execução
  do probe cruzado; mudanças locais que preservem as refs/digests não exigem reabrir o outro gate.
- **Estado inicial:** proposal/draft. Só se torna normativo para \(X\) após revisão independente e
  aceitação explícita por ambos os lados; até lá, não autoriza promoção.

Esse artefato não é uma terceira verdade porque não possui liberdade para redefinir A ou B: ele é a
função parcial versionada \(f:A\rightharpoonup B\) e o conjunto de predicados \(X\). As duas fontes
continuam donas dos seus domínios; a interface passa a ter exatamente um owner.

## Ponto enviado para a próxima rodada

A direção comum é racionalmente defensável se o agente pró-junção aceitar: (i) não fusão imediata,
(ii) autoridade estreita do artefato integrador, (iii) fail-closed, e (iv) gates locais preservados,
com \(G_X\) acionado apenas por mudança cruzada. A discordância remanescente deixa de ser “um ou dois
arquivos” e passa a ser experimental: quando a densidade de \(X\), o custo de drift e o custo de
navegação justificariam consolidação posterior.
