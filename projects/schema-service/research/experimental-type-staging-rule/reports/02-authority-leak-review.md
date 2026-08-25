# Revisão adversarial — vazamento de autoridade no staging experimental

## Veredito

**A hipótese sobrevive apenas se “confinado ao diretório” for uma regra de custódia, não o mecanismo de autoridade.** O próprio modelo do Schema Service diz que caminho e digest não bastam como identidade durável e que a disposição física permanece aberta ([README.md, linhas 33–36](../../../README.md#L33-L36); [README.md, linhas 61–62](../../../README.md#L61-L62)). Portanto, localização não pode decidir se uma definição é normativa. O collapse-test falha sempre que uma referência experimental tiver a mesma forma resolvível de `schema` que uma referência publicada, ou quando um resolver normativo puder descobrir o candidato por varredura, índice, fallback ou fechamento de dependências sem consultar um registro de publicação autorizado.

As definições iniciais reconhecem precisamente os vazios que tornam esse colapso possível: namespace experimental ainda indecidido, ausência de contrato de resolução e promoção não especificada ([research-initial-definitions.md, linhas 67–73](../research-initial-definitions.md#L67-L73)). Assim, o confinamento proposto ainda não é uma regra suficiente; é uma intenção que precisa dos guardrails abaixo.

## Ataques que sobrevivem

### 1. Localização pode ser confundida com autoridade

**Severidade: crítica.** A regra desejada limita uso ao escopo declarado do experimento ([research-initial-definitions.md, linhas 35–45](../research-initial-definitions.md#L35-L45)), mas não define como um consumidor prova esse escopo. Um resolver que aceite “arquivo encontrado no caminho esperado” transforma convenção de diretório em publicação implícita, contradizendo a regra de que publicação é operação autorizada do registry ([README.md, linhas 137–140](../../../README.md#L137-L140)). Cópia, symlink, indexação ampla ou mudança de raiz poderiam então alterar a autoridade sem alterar o conteúdo.

**Mudança requerida:** nenhum resolver normativo pode aceitar caminho, presença em catálogo local ou digest como prova de publicação. Ele deve resolver exclusivamente uma identidade revision-exact presente em registro de publicação autorizado; o resolver experimental deve ser uma operação distinta e explicitamente parametrizada pelo experimento.

### 2. A mesma forma de referência permite interpretação normativa acidental

**Severidade: crítica.** O envelope normativo requer `schema` resolvível e revision-exact ([README.md, linhas 333–345](../../../README.md#L333-L345)), enquanto o lifecycle ainda deixa aberto se uma instância pode referenciar schema não publicado para validação local ([README.md, linhas 142–144](../../../README.md#L142-L144)). Se a fixture experimental preencher `schema: document/analysis@0`, um consumidor externo não consegue distinguir candidato de norma somente pela referência. O namespace experimental também está explicitamente em aberto ([research-initial-definitions.md, linhas 67–70](../research-initial-definitions.md#L67-L70)).

**Mudança requerida:** uma fixture experimental não pode colocar o candidato no campo normativo `schema`. Deve usar uma referência inequivocamente experimental contendo, no mínimo, `experiment_ref` e uma identidade revision-exact do candidato. Qualquer consumidor sem capacidade experimental explícita deve rejeitá-la, nunca fazer fallback silencioso nem tentar o registry pelo nome proposto.

### 3. `TypeId`, revisão candidata e revisão publicada podem colidir

**Severidade: maior.** O modelo separa identidade semântica de tipo e `SchemaId` revision-exact, mas ainda não decidiu o contrato estável de `Type` ([README.md, linhas 56–60](../../../README.md#L56-L60); [README.md, linhas 96–100](../../../README.md#L96-L100)). Reutilizar antecipadamente um futuro `TypeId` ou `SchemaId` no candidato cria duas autoridades concorrentes quando outro experimento ou o registry publicar o mesmo nome.

**Mudança requerida:** o candidato recebe uma identidade própria, escopada ao experimento e distinta tanto do `proposed_type_id` quanto de qualquer `SchemaId` normativo. A promoção deve verificar colisões e produzir um mapeamento explícito candidato → publicação; igualdade de rótulo ou digest não implica igualdade de identidade ou autoridade.

### 4. Promoção pode reescrever o passado por mudança de resolução

**Severidade: crítica.** A premissa exige que promoção não altere execuções observadas ([research-initial-definitions.md, linhas 41–43](../research-initial-definitions.md#L41-L43)), e o modelo estabelece que nova revisão não muda o significado de `SchemaId` existente ([README.md, linhas 59–60](../../../README.md#L59-L60)). Porém, se referências antigas forem resolvidas por nome e passarem a encontrar uma publicação posterior, a mesma fixture muda de “experimental” para “normativa” retroativamente.

**Mudança requerida:** cada execução fixa o digest do manifesto do experimento, a revisão candidata exata e o modo `experimental`. Promoção cria um registro de publicação e uma nova referência normativa; não edita a referência, o relatório ou o manifesto da execução anterior. Reclassificação de instância exige nova revisão, como já determina a rota de novidade ([README.md, linhas 181–193](../../../README.md#L181-L193)).

### 5. Dependências e artefatos derivados podem exportar autoridade

**Severidade: maior.** O effective schema é um fechamento resolvido de bases e capacidades ([README.md, linhas 146–156](../../../README.md#L146-L156)). Sem uma barreira de modo, um schema publicado pode importar um candidato, ou um resultado de validação local pode circular sem indicar que seu contrato era experimental. O modelo exige que relatórios identifiquem schema exato e versão do validador para não parecerem verdade corrente ([README.md, linhas 374–379](../../../README.md#L374-L379)), mas isso sozinho não distingue autoridade experimental.

**Mudança requerida:** o fechamento normativo deve rejeitar toda dependência experimental. O fechamento experimental pode importar revisões publicadas e candidatos do mesmo experimento, mas seu resultado e todo relatório derivado permanecem marcados como experimentais, com `experiment_ref` e revisão candidata exata. Um artefato derivado não pode remover essa marca e continuar alegando conformance.

### 6. Candidatos órfãos continuam encontráveis sem dono ou destino

**Severidade: maior.** Não há regra de expiração, abandono ou supersessão ([research-initial-definitions.md, linhas 71–75](../research-initial-definitions.md#L71-L75)). Um experimento encerrado pode deixar definições encontráveis indefinidamente; isso amplia a chance de uso externo e torna ambíguo se o candidato ainda pode receber evidência ou promoção.

**Mudança requerida:** o manifesto do experimento deve possuir dono e estado explícito. `abandoned` e `superseded` tornam o candidato inelegível para novas resoluções e promoção direta, preservando-o apenas para reproduzir execuções já fixadas. A ausência do manifesto ou do dono é erro fechado, não estado implícito.

## Menor conjunto de guardrails

1. **Duas capacidades de resolução.** O resolver normativo consulta somente registros de publicação autorizados. A resolução experimental exige chamada explícita, `experiment_ref` autorizado e raiz/catálogo declarado; nenhuma busca global ou fallback entre modos.
2. **Duas classes de referência.** `schema` permanece reservado a `SchemaId` publicado. O candidato usa referência experimental estruturada com `experiment_ref`, `candidate_revision_id` e digest; rótulos propostos não são resolvíveis.
3. **Três identidades não colapsadas.** Manter separados `candidate_revision_id`, `proposed_type_id` e o `SchemaId` produzido na publicação. Promoção registra o mapeamento e rejeita colisões; não renomeia o passado.
4. **Imutabilidade observável.** Cada execução fixa digest do manifesto, candidato exato, validador e modo experimental. Alteração cria nova revisão candidata; promoção cria nova referência normativa e nova revisão de manifest para qualquer instância adotante.
5. **Fechamento de autoridade.** Schema normativo não pode depender de candidato. Resultado experimental herda a inelegibilidade de qualquer dependência experimental e carrega essa proveniência em toda saída de validação.
6. **Lifecycle mínimo e erro fechado.** `active`, `superseded`, `abandoned` e `promoted` bastam para staging. Apenas `active` resolve para novas execuções; `promoted` não converte referências antigas; estados terminais continuam disponíveis somente para replay revision-exact. Manifesto ausente, escopo divergente ou referência ambígua falham.

Esses seis guardrails são o mínimo porque cada um fecha uma via diferente do collapse-test: descoberta, sintaxe da referência, colisão de identidade, mutação temporal, propagação por dependência e orfandade. O precedente local sustenta apenas parte desse desenho: ele separa o lote por `candidate_batch_not_registry` e marca cada item `resolution_eligible: false` ([seed-registry-candidates-v01.json, linhas 2–8](../../../../../docs/features/agent-provenance-telemetry/contracts/fixtures/seed-registry-candidates-v01.json#L2-L8)); também condiciona resolução canônica à conjunção `accepted` + `resolution_eligible` ([seed-registry-gate.md, linhas 19–32](../../../../../docs/features/agent-provenance-telemetry/research/seed-registry-gate.md#L19-L32)). Esse precedente, contudo, está marcado como superseded e conformance-only ([seed-registry-gate.md, linhas 1–17](../../../../../docs/features/agent-provenance-telemetry/research/seed-registry-gate.md#L1-L17); [seed-registry-gate.md, linhas 34–44](../../../../../docs/features/agent-provenance-telemetry/research/seed-registry-gate.md#L34-L44)); ele apoia negação explícita de elegibilidade, não autoriza copiar seu lifecycle.

## Decisões que devem permanecer abertas

- A serialização final de `TypeId` e `SchemaId`, já declarada em aberto ([README.md, linhas 118–135](../../../README.md#L118-L135)). O staging só precisa impedir colisão e ambiguidade; não deve congelar o registry definitivo.
- O caminho e nome canônicos do catálogo experimental. A pesquisa precisa de uma raiz declarada por experimento, mas o modelo mantém o arranjo físico aberto ([README.md, linhas 33–36](../../../README.md#L33-L36)); logo, fixar agora uma taxonomia global acoplaria identidade à localização.
- Os critérios probatórios de promoção e a autoridade humana/organizacional concreta. O modelo já exige dono, autoridade e registro imutável na publicação ([README.md, linhas 137–140](../../../README.md#L137-L140)), mas o gate de evidência permanece pergunta explícita ([README.md, linhas 453–457](../../../README.md#L453-L457)).
- A operação física de promoção — copiar, empacotar ou reautorizar — desde que preserve o digest candidato, crie identidade/publicação normativa explícita e não reescreva execuções.
- Expiração automática e prazos. O guardrail necessário é estado terminal e erro fechado; duração e política de retenção exigem evidência operacional ainda inexistente.
- Extensões específicas para skills e folders. A própria pesquisa admite que a regra ainda não foi demonstrada nessas famílias ([research-initial-definitions.md, linhas 73–75](../research-initial-definitions.md#L73-L75)), e o modelo alerta que snapshots variam para folders, skills compostas e ferramentas remotas ([README.md, linhas 244–251](../../../README.md#L244-L251)). O núcleo de autoridade pode ser comum sem antecipar suas mecânicas de representação.

## Collapse-test operacional

Para qualquer candidato, execute a prova negativa: entregue sua referência e seus artefatos derivados a um consumidor que possui apenas capacidade normativa. O resultado aceitável é rejeição explícita por referência experimental/ausência de publicação. Se ele resolver pelo nome, caminho, digest, índice, fallback, dependência ou estado posterior de promoção, a regra falhou. Em seguida, um consumidor experimental autorizado deve conseguir reproduzir a execução somente com o `experiment_ref`, manifesto e revisão candidata fixados, sem consultar “a versão mais recente”.
