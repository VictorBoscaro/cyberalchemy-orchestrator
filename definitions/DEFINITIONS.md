# DEFINITIONS — vocabulário normativo (v0.1, candidato)

*Não-revisado. Claim ≤ proof: nada aqui é resultado provado; onde a âncora é fraca
(nível-memória, Lean não-commitado, ou síntese nossa) isso está rotulado inline.*
*Adota o protocolo de definições de `Arcanum/definitions/DEFINITIONS.md` — fonte única de
verdade: cada termo é definido normativamente em exatamente UM lugar; as fronteiras não colidem.*

---

### DEF-ORCH-001

- **ID:** DEF-ORCH-001
- **Status:** candidato
- **Termo + Aliases:** **resíduo** (*residue*, "o que se perde na tradução")
- **Voz científica/formal:** O objeto categórico que mede o que um morfismo/tradução deixa de
  preservar, tipado contra `FunctorialResidueStructure` — a ação de separação como ação
  funtorial, não como conjunto de perdas. Tem duas faces decompostas como soma: **sombra ⊕
  estrutura** (face escalar object-level ⊕ face morphism-level).
- **Interpretação operacional:** Quando um agente/verbo transforma um artefato de conhecimento
  (schema → instância, merge, coarsening), o resíduo é *o objeto* que carrega a distinção
  sobrevivente — não o relatório textual da perda, mas a coisa contra a qual "vencer a
  contagem" é sequer definível.
- **Voz coloquial:** É o que a tradução perdeu, guardado como uma coisa em vez de um lamento.
- **Fronteira:** EXCLUI a **sombra** (DEF-ORCH-003): o resíduo é o objeto de duas faces; a
  sombra é *apenas uma* delas (a escalar). Um resíduo cuja única face não-trivial é a sombra
  está *count-capped* e não bate a contagem. Resíduo ≠ o verbo que o gera (DEF-ORCH-005).
- **Tipo categórico + âncora:** `structure FunctorialResidueStructure` —
  `lean-formalization/FunctorialResidueStructure.lean:97`; ação `separation_is_functor_action` — `:513`.
- **Relacionadas:** DEF-ORCH-002, DEF-ORCH-003, DEF-ORCH-005.

---

### DEF-ORCH-002

- **ID:** DEF-ORCH-002
- **Status:** candidato
- **Termo + Aliases:** **separação** (*separation*, "distinguir")
- **Voz científica/formal:** O primitivo: distinguir dois objetos. Precede a contagem — sem
  sinal individuante não há o que contar; indiscernível = idêntico. Formalmente, o critério
  que separa uma ação que apenas *tampa* a contagem (`CountCapped`) de uma que a *bate* (`BeatsCount`).
- **Interpretação operacional:** Antes de o orquestrador contar, agrupar ou pontuar qualquer
  coisa, algum mapa precisou distinguir dois artefatos. Separação é essa operação anterior; a
  contagem é derivada dela, nunca o contrário.
- **Voz coloquial:** Primeiro você distingue duas coisas; só depois faz sentido contá-las.
- **Fronteira:** EXCLUI a contagem e a sombra: separação é *anterior* — é a condição da
  contagem, não um caso dela. RÓTULO (fraco): a lição "separation IS count" (dentro de CIC) é
  nível-memória — `separation-is-count-two-routes-closed` — e **não tem declaração Lean**;
  trata-se de um teto observado, não de um teorema aqui.
- **Tipo categórico + âncora:** `CountCapped` — `lean-formalization/BeatsCountCriterion.lean:111`;
  `BeatsCount` — `:118`; `not_countCapped_of_beatsCount` — `:140`.
- **Relacionadas:** DEF-ORCH-001, DEF-ORCH-003.

---

### DEF-ORCH-003

- **ID:** DEF-ORCH-003
- **Status:** candidato
- **Termo + Aliases:** **sombra** (*shadow*, contagem/entropia/magnitude)
- **Voz científica/formal:** A face escalar, object-level, do resíduo: um funtor para uma
  categoria *thin*. Separa mas não reconstrói (lossy). Casos: entropia = log-cardinalidade;
  magnitude; qualquer leitura numérica invariante.
- **Interpretação operacional:** Métricas do orquestrador — número de nós, entropia de uma
  partição, tamanho de um merge. Úteis para ordenar, inúteis para inverter: dada a sombra, não
  se recupera o objeto.
- **Voz coloquial:** É o número que resume o objeto e joga fora o objeto.
- **Fronteira:** EXCLUI a face morphism-level do resíduo (DEF-ORCH-001): sobre uma categoria
  thin, nenhuma leitura morphism-level bate a contagem — o colapso é estrutural. A sombra é
  *uma* face; nunca as duas.
- **Tipo categórico + âncora:** entropia = log-cardinalidade,
  `entropy_nondecreasing_under_temporal_coarsening` — `lean-formalization/SecondLawDiscrete.lean:288`;
  colapso thin `thin_codomain_noise_hom_subsingleton` — `ThinCodomainCollapse.lean:98`;
  `thin_hom_readout_not_beatsCount` — `BeatsCountCriterion.lean:196`. RÓTULO (fraco):
  magnitude-como-sombra é memória + Lean não-commitado.
- **Relacionadas:** DEF-ORCH-001, DEF-ORCH-002.

---

### DEF-ORCH-004

- **ID:** DEF-ORCH-004
- **Status:** candidato
- **Termo + Aliases:** **sonda** (*probe/recon*, mapa-teste)
- **Voz científica/formal:** A interrogação ativa de um objeto por mapas-teste `A → X` que
  *nós* escolhemos (Yoneda). A família completa desses mapas reconstrói o objeto: o mergulho
  de Yoneda é fully faithful.
- **Interpretação operacional:** O orquestrador conhece um artefato não por inspeção interna,
  mas pelo conjunto de perguntas `A → X` que consegue endereçar a ele; a totalidade das
  respostas *é* o artefato.
- **Voz coloquial:** Você conhece a coisa pelo conjunto completo de perguntas que consegue fazer a ela.
- **Fronteira:** DESAMBIGUAÇÃO obrigatória: **sonda-recon** (Yoneda, ESTE termo — reconstrução
  por mapas-teste) ≠ **probe-experimento** (falsificação Popperiana, NÃO é este termo, vive em
  `experiment/SKILL.md`). EXCLUI o **verbo** (DEF-ORCH-005): a sonda *lê* o objeto sem
  transformá-lo; o verbo *age* sobre ele.
- **Tipo categórico + âncora:** `y` — `lean-formalization/YonedaAsTranslation.lean:41`;
  `Faithful` — `:45`; `Full` — `:50`; `schema_residue_vanishes` — `:58`; identidade
  functor-of-points (este sentido) `Probe.lean:8-13` (é um `example`, thin). RÓTULO (fraco): a
  dualidade sonda-ativa / sinal-passivo é síntese nossa, **não** é claim do repo.
- **Relacionadas:** DEF-ORCH-001, DEF-ORCH-005.

---

### DEF-ORCH-005

- **ID:** DEF-ORCH-005
- **Status:** candidato
- **Termo + Aliases:** **verbo** (*verb/action*, ação sobre objeto)
- **Voz científica/formal:** Uma ação sobre um objeto = um morfismo **mais** a condição sob a
  qual ele preserva a simetria do objeto. Dentro da condição, é preservador (iso/Aut); fora
  dela, gera resíduo. Morfismo ≠ simetria: só isomorfismos/Aut preservam distinções.
- **Interpretação operacional:** Cada verbo do orquestrador (merge, refine, forget, translate)
  é um morfismo com uma zona de segurança declarada; aplicá-lo fora dessa zona produz resíduo
  — e é *aí* que há informação a formalizar.
- **Voz coloquial:** Uma ação que, quando sai da faixa onde é reversível, começa a perder coisas.
- **Fronteira:** EXCLUI o **resíduo** (DEF-ORCH-001): o verbo é a *causa* (o morfismo aplicado),
  o resíduo é o *efeito* (o objeto perdido). EXCLUI a **sonda** (DEF-ORCH-004): sonda lê, verbo
  transforma. RÓTULO (fraco): a caracterização "verbo = morfismo + condição de preservação" é
  nível-memória (`symmetry-invertible-lever-is-enrichment`), **sem declaração Lean**.
- **Tipo categórico + âncora:** memória `symmetry-invertible-lever-is-enrichment` (morfismo ≠
  simetria; só iso/Aut preserva). Nenhuma decl Lean dedicada — rótulo fraco assumido.
- **Relacionadas:** DEF-ORCH-001, DEF-ORCH-004.

---

## Tabela de fronteiras

Para cada termo, o UM traço que o separa mais nitidamente do vizinho mais próximo
(demonstra que as fronteiras não colidem):

| Termo | Traço separador mais nítido (vs. vizinho) |
|---|---|
| **resíduo** (001) | Tem DUAS faces (sombra ⊕ estrutura); vizinho *sombra* tem só uma. É o *efeito* de um verbo, não o verbo. |
| **separação** (002) | É *anterior* à contagem — condição, não caso; vizinho *sombra* é já uma leitura numérica derivada. |
| **sombra** (003) | Funtor para categoria *thin*, lossy, não reconstrói; vizinha *sonda* (Yoneda completa) reconstrói. |
| **sonda** (004) | *Lê* o objeto sem transformá-lo (Yoneda FF); vizinho *verbo* *age* e pode gerar resíduo. |
| **verbo** (005) | É o morfismo aplicado + condição de simetria (a *causa*); vizinho *resíduo* é o objeto perdido (o *efeito*). |
