# FRAMINGS — ledger de enquadramentos (sessão 2026-07-18)

> Estatuto: brainstorm/candidato, **não-revisado**. Cada entrada é hipótese, não resultado.
> Distinto das definições normativas (§3 do PLAN) e de resultados Lean — **nada aqui está
> provado**. Âncoras verificadas por sonda 2026-07-18; onde a âncora é fraca (memória /
> Lean não-commitado / síntese própria), está **rotulado**.

---

## F1 — Resíduo = sombra ⊕ estrutura

- **Forma tipada:** O resíduo decompõe-se em duas faces — a *sombra* (invariante escalar
  object-level: contagem/entropia/magnitude) e a *estrutura* (objeto categórico:
  morfismos/tipos/regras). A estrutura domina estritamente a sombra quando o codomínio não é thin.
- **Âncora:** `FunctorialResidueStructure.lean:97` `structure FunctorialResidueStructure`,
  `:513` `separation_is_functor_action`; entropia = log-cardinalidade em
  `SecondLawDiscrete.lean:288` `entropy_nondecreasing_under_temporal_coarsening`.
- **Collapse-test:** Se a estrutura fosse recuperável da sombra, as faces colapsam numa —
  mas decategorificar é irreversível (parede do "beats count").

## F2 — Bateria de sombras + teto

- **Forma tipada:** Cada métrica escalar é um funtor para uma categoria thin — uma direção
  de projeção distinta (contagem < entropia < magnitude no quanto veem). Projeção separa
  mas não reconstrói; ascender = trocar o codomínio `C` por um não-thin, não clarear a sombra.
- **Âncora:** `FunctorialResidueStructure.lean:162` `ofAntitoneSet` (§2, `C = (Set O, ⊆)` =
  instância thin degenerada, "a parede"); colapso thin em `ThinCodomainCollapse.lean:98`
  `thin_codomain_noise_hom_subsingleton` e `BeatsCountCriterion.lean:196`
  `thin_hom_readout_not_beatsCount`.
  — *Âncora fraca:* magnitude-como-sombra = memória `magnitude-owns-four-base-invariant` +
  Lean **não-commitado** (`MagnitudeEnriched.lean`), não teorema commitado.
- **Collapse-test:** A bateria só é não-vazia se sombras diferentes **discordam** em algum
  par. Se toda métrica ordenasse igual, colapsa a um funtor — mas count e magnitude discordam.

## F3 — Contagem pressupõe separação

- **Forma tipada:** O fundo da escada não é a contagem, é a separação/individuação: sem
  sinal individuante não há contagem (indiscernível = idêntico). Dois níveis de sinal —
  individuante (habilita contar, object-level) vs relacional (habilita ver morfismos, beats count).
- **Âncora:** `BeatsCountCriterion.lean:111` `CountCapped`, `:118` `BeatsCount`, `:140`
  `not_countCapped_of_beatsCount`.
  — *Âncora fraca:* "separation IS count" **não tem decl Lean** — é lição memory-level
  (`separation-is-count-two-routes-closed`, quatro rotas closed-negative). Instância física
  (partículas idênticas QM não-contáveis como indivíduos) é ilustração, não teorema do repo.
- **Collapse-test:** Se contagem pudesse existir sem separação prévia, a precedência cai e
  F3 vira circular.

## F4 — Dualidade sonda-ativa / sinal-passivo

- **Forma tipada:** O resíduo emite sinais indiretos (sombras recebidas involuntariamente,
  lossy) **e** admite sondas ativas — mapas-teste `A → X` que escolhemos (Yoneda). A família
  completa de sondas reconstrói (Yoneda fully faithful); uma sombra passiva única não.
  Ativo/passivo = escolher a tela vs estar preso à projeção = o lever thin/não-thin.
- **Âncora:** covariante (sonda-para-dentro) `YonedaAsTranslation.lean:41` `y`, `:45`
  `Faithful`, `:50` `Full`, `:58` `schema_residue_vanishes`; functor-of-points `Probe.lean:8-13`
  (é um `example`, não lemma nomeado — thin); contravariante (observar-para-fora)
  `files/new/YonedaBridge.lean:65` `coyonedaUnit`.
  — *Rótulo:* o **split** covariante/contravariante é real no repo; a **dualidade** que os
  pareia (sonda ⟷ observável) é **síntese desta sessão**, não um claim existente do repo.
- **Collapse-test:** Se probing por todos os representáveis não fosse fiel, a face ativa não
  teria vantagem — mas Yoneda FF garante que tem.

## F5 — Regra-do-verbo

- **Forma tipada:** Um verbo (`implements`/`validates`/`refines`/…) é um morfismo **mais** a
  condição sob a qual preserva a simetria do objeto; fora dessa condição, gera resíduo —
  tornando o resíduo mensurável por-verbo.
- **Âncora:** memória `symmetry-invertible-lever-is-enrichment` (morfismo ≠ simetria; só
  iso/Aut preserva). — *Âncora fraca:* memory-level, sem decl Lean dedicada.
- **Collapse-test:** Se todo verbo preservasse simetria, não haveria resíduo por-verbo —
  mas o morfismo geral não é iso.

## F6 — O ponto de Yoneda como alvo, a anomalia como motor (a dinâmica)

- **Forma tipada:** O **ponto de Yoneda** (fully faithful, resíduo 0, individuação total) é
  o alvo — o conhecimento cristalino. Em domínios com self-modeling operativo é **inatingível
  por construção** (o resíduo é estrutural). Você *sabe* que não chegou porque recebe um
  **sinal discriminante**: uma falha-de-FF detectada (duas coisas que o modelo identificara
  revelam-se distintas sob uma sonda nova = um separador que a lente atual é cega a). Caçar
  essa anomalia → mandar sonda ativa ali → enriquecer `C` → encolher o resíduo. Isso é o
  **processo científico**.
- **Âncora:** ponto de Yoneda = `YonedaAsTranslation.lean:58` `schema_residue_vanishes`
  (resíduo some sse `Full ∧ Faithful`); a anomalia = `BeatsCountCriterion.lean:118`
  `BeatsCount` (separador invisível à resolução atual). — *Âncora fraca:* a inatingibilidade
  em domínios ricos é o gradiente A3 (BACKLOG / memória), não teorema Lean.
- **Collapse-test:** Cai se, em domínios ricos, o ponto de Yoneda for atingível (motor para);
  ou se toda "anomalia" for sempre re-expressível na resolução atual (sinal sem separador
  novo) — aí não há estrutura a extrair, só ruído.
- **Status (2026-07-20):** parcialmente deflacionado pelo debate das 3 sondas — a face
  *inatingível* sobrevive (o lema de persistência concorda: resíduo positivo em todo nível
  finito), mas o enquadramento "ponto de Yoneda = alvo que se *atinge*" cai: `y` é FF de graça
  e o endpoint resíduo-0 é vacuoso (`Knowledge.total`). O conteúdo é a **trajetória ordenada de
  enriquecimento** — ver F7 e memória `yoneda-ascension-thesis-verdict`.

## F7 — Duas espécies de sonda = os dois eixos independentes, com ordem de apresentação

- **Forma tipada:** A sonda tem duas espécies, uma por eixo *independente* de descoberta:
  **sonda-de-reconhecimento** (acha *quais objetos/tipos existem* — eixo `¬EssSurj →
  NewObjects`) e **sonda-de-ligação** (estabelece *as relações* entre objetos já achados —
  eixo `¬Full → NewRelations`, os mapas-teste de Yoneda). Os eixos são independentes, mas a
  **ordem recon→ligação não é arbitrária**: é uma **dependência de formação-de-tipo** — uma
  ligação vive em `Hom(A,B)`, cujo tipo é mal-formado enquanto `A,B` não existem. Logo a
  estrutura é um **poset graduado** (estratificação bem-fundada objeto→relação; o nome "Reedy"
  é analogia, não a estrutura homônima), não uma escada linear nem uma necessidade lógica. A
  leitura raso→profundo ("buscar por cima, depois pesquisa profunda") é o **eixo-β de
  resolução** (sub-família grossa que ainda não separa → enriquecer até separar), que compõe
  com o eixo objeto→relação.
- **Âncora:** eixos = `distilled-knowledge/knowledge-evolution-typing.md` em
  `domainspec-lean-formalization` (`¬EssSurj→NewObjects` ⊥ `¬Full→NewRelations`); família de
  ligações reconstrói = `ProbeTypology.lean:38` `representables_separate`, `:49`
  `representables_isSeparating`. — *Rótulo (fraco):* as "duas espécies operacionais = os dois
  rungs", o poset de Reedy e o eixo-β são **síntese** (debate 2026-07-20), **sem decl Lean** —
  a testemunha de convergência graduada (sub-família falha → adicionar sonda restaura FF) é
  **obrigação aberta**.
- **Collapse-test:** Cai se as espécies não forem independentes (uma sonda que é recon *e*
  ligação ao mesmo tempo desfaz o produto de eixos), ou se a ordem não for forçada pela
  tipagem de `Hom` (um objeto universal que deixe linkar antes de achar).

---

## Fio comum

F1–F5 são a **anatomia estática**; F6 é a **dinâmica**; **F7 refina a sonda ativa de F4 nos
dois eixos independentes de descoberta (objeto ⊥ relação) e ordena-os por apresentação
(recon→ligação)**. Todas circulam o mesmo lever —
**thin vs não-thin, a escolha de `C`**. A sombra escalar (F1) e cada métrica (F2) são os
codomínios thin onde a estrutura se perde; F3 mostra que até a contagem, o piso desse regime,
já pressupõe um sinal individuante que ela não fabrica; F4 nomeia a saída — trocar a projeção
passiva pela família ativa de sondas (Yoneda FF) é *escolher um `C` não-thin*; F5 localiza
onde o resíduo aparece nesse `C` mais rico (o defeito de simetria por-verbo); e F6 põe tudo
em movimento: o trabalho é **subir `C` rumo ao ponto de Yoneda inatingível, movido pelos
sinais discriminantes**. A aposta comum, e o único ponto onde todas caem juntas: que ascender
significa sempre **enriquecer o codomínio, nunca clarear a sombra**.
