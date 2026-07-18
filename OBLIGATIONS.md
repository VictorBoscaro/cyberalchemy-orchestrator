# OBLIGATIONS — alvos falsificáveis (candidato)

*O que teria de ser provado para o vault deixar de ser metáfora. Cada obrigação é enunciada
com precisão + carrega seu collapse-test. Nenhuma está descarregada. Não-revisado.*

---

## OBL-E3 — A linguagem de orquestração é uma categoria? *(o teste que decide tudo)*

**Claim a descarregar.** Existe uma categoria `ORCH` onde:
- **objetos** = grupos de dispatch;
- **morfismos** = `connections` tipadas (`sequential` / `zig-zag` / `feedback`);
- **composição** = concatenação de pipeline;
- **identidade** = grupo pass-through.

**Sub-obrigações (todas precisam valer):**
1. **Associatividade.** `(h∘g)∘f = h∘(g∘f)` para conexões encadeadas.
2. **Leis de identidade.** pass-through é unidade à esquerda e à direita.
3. **Resíduo = mesmo objeto.** O resíduo de uma síntese (o que um `synthesizer`/merge perde)
   é o **mesmo** objeto que `FunctorialResidueStructure`
   (`lean-formalization/FunctorialResidueStructure.lean:97`), via um funtor de `ORCH`-sínteses
   para a estrutura de resíduo — **não** só um resíduo count-shaped.

**Risco nomeado (não escondido).** `zig-zag` e `feedback` são *loops*, não claramente
morfismos. Palpite honesto: só o fragmento `sequential` é categoria de cara; `zig-zag`/`feedback`
provavelmente são estrutura extra (2-células? uma bicategoria? um sistema de fatoração?) e
**não** morfismos de 1-nível. Se for isso, o claim se restringe ao fragmento sequential.

**Collapse-test (duplo).**
- (a) Se `zig-zag`/`feedback` não compõem associativamente, `ORCH` é categoria só no
  fragmento `sequential` (um DAG) — e o paralelo CT é **decoração** para essas arestas.
- (b) Se o resíduo-de-síntese for demonstravelmente count-shaped (não alcança
  `FunctorialResidueStructure`), a sub-obrigação 3 colapsa a **analogia**, e o "mesmo resíduo"
  cai a zero contribuição.

**Onde vive.** Lean, no repo `domainspec-lean-formalization`. Custo: sessão dedicada, não
inline. Depende de: nada externo — é descarregável já, se e quando valer o investimento.

**Status.** OPEN. É o primeiro alvo real; até descarregá-lo (ou bater o collapse-test), tudo
no vault é candidato tipado, não resultado.
