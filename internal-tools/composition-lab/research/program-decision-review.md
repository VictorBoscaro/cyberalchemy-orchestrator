---
artifact_kind: decision-oriented-document-review
target: internal-tools/composition-lab/research-program.md
status: complete
date: 2026-08-13
authority: review-only
---

# Review do programa de pesquisa orientado a decisão

## Veredito

**FIX.** O documento já é um bom núcleo de orientação: um mantenedor entende rapidamente o problema
geral, por que ele importa, o estado desigual da evidência, os principais desconhecidos e por que
lentes são somente o Caso 1. Nenhuma afirmação factual verificada exige bloqueio. Antes de tratá-lo
como a referência decisória curta do laboratório, porém, são necessárias duas correções substantivas
e duas clarificações pequenas.

## O que está funcionando

- **Problema e relevância:** a distinção entre composição e agregação, sequência, configuração,
  integração ou coordenação aparece cedo e é ligada a riscos concretos de produto e atribuição causal.
- **Estado epistêmico:** evidência externa aceita, ausência de findings internos aceitos e ausência de
  autorização arquitetural estão separados sem ambiguidade.
- **Conhecidos e desconhecidos:** o texto não promove recorrências condicionadas a universais e
  preserva questões sobre identidade, ordem, perda, recuperação e novidade do todo.
- **Lentes como Caso 1:** o documento afirma explicitamente que o caso inicia a investigação e não é
  sinônimo nem modelo geral de composição. Isso é coerente com o README.
- **Autoridade da evidência:** a síntese externa citada tem verificação final `PASS / KEEP`; o programa
  distingue corretamente findings de review e não transforma o review em fonte.
- **Densidade:** há pequena repetição inevitável com o README, mas os papéis são distinguíveis: o
  README apresenta o laboratório; o programa preserva estado, implicações e direção da pesquisa.

## Mudanças necessárias

### 1. Tornar explícitos os gates de decisão — MAJOR

A seção “Decisões deferidas e consequências” descreve bem por que **não decidir agora**, mas não
permite responder de forma direta **o que o projeto terá de decidir quando houver evidência**. As
alternativas estão distribuídas entre a pergunta geral e os riscos prematuros; também não aparecem
as consequências específicas de escolher errado depois.

Mudança mínima: substituir ou preceder a lista atual por quatro gates nomeados, mantendo-os
deferidos:

1. se “composição” será um modelo comum, uma família tipada ou termos separados;
2. o que uma representação precisa tornar explícito — partes, operação, admissibilidade, ambiente,
   estágio, preservação/perda e falha;
3. quais alegações sobre o todo exigem prova, execução, observação ou julgamento;
4. onde reside a autoridade para admitir, executar, avaliar e revisar uma composição, inclusive se
   uma ferramenta externa deve coordenar essas funções.

Para cada gate, acrescentar uma consequência curta da escolha errada. Exemplos: falsa
interoperabilidade entre fenômenos incompatíveis; schema que apaga causalidade ou perda; avaliação
que confunde formação com execução; orquestrador que centraliza autoridade que pertence ao domínio
ou ao usuário. Não escolher alternativas ainda; apenas tornar a futura decisão e seu custo legíveis.

### 2. Declarar um próximo passo singular e verificável — MAJOR

“Próxima evidência necessária” lista duas frentes amplas e depois uma comparação, mas não informa
qual ação é o próximo passo do programa, qual delas é caminho crítico ou qual condição permite
avançar. Um mantenedor não consegue sair do documento sabendo o que deve acontecer agora.

Mudança mínima: abrir a seção com uma frase como: “O próximo gate é obter e aprovar o primeiro lote
de findings internos comparáveis; a ampliação externa pode ocorrer em paralelo, mas não substitui
esse gate.” Em seguida, definir a condição de saída em uma linha: corpus identificado (incluindo
`domainspec-v2`), casos e negativos preservados, classificação não predeterminada pelo vocabulário
externo e review independente `KEEP`. Se a pesquisa interna estiver operacionalmente bloqueada, o
estado atual deve nomear esse bloqueio em vez de apenas dizer que a evidência não foi aceita.

### 3. Resolver a regra conflitante de entrada no documento progressivo — MINOR

O README diz que findings internos e externos “são comparados antes de entrar no documento
progressivo”. O programa, que se declara esse núcleo progressivo, já incorpora findings externos
antes de existirem findings internos aceitos. As duas práticas podem ser compatíveis, mas a regra
atual não explica como.

Mudança mínima: esclarecer em um dos dois arquivos que findings aceitos de uma única linha podem
entrar como resultados **limitados àquela linha**, enquanto afirmações cruzadas ou gerais só entram
após comparação interna–externa. Se a intenção era realmente impedir qualquer entrada antecipada,
então a seção externa do programa deve permanecer apenas como link de estado, não como síntese.

### 4. Distinguir os dois status editoriais — MINOR

O README do internal tool está `proposed`, enquanto o programa está `active`. Isso pode ser legítimo
— ferramenta proposta, programa de pesquisa ativo —, mas não está declarado e pode parecer deriva
de autoridade.

Mudança mínima: adicionar ao “Estado atual” uma frase dizendo que `active` qualifica a pesquisa, não
ratifica o internal tool, sua teoria, interface ou autoridade.

## Checagem orientada ao leitor

| Pergunta do mantenedor | Estado atual |
|---|---|
| Qual é o problema geral? | Claro |
| Por que importa para o projeto? | Claro |
| O que sabemos agora? | Claro e adequadamente limitado |
| O que não sabemos? | Claro |
| O que precisa ser decidido? | Parcial; decisões não estão estruturadas como gates |
| Qual o custo de decidir errado? | Parcial; cobre prematuridade, não cada escolha futura |
| Qual é o próximo passo? | Ambíguo entre duas frentes; falta condição de saída |
| Lentes são apenas Caso 1? | Inequívoco |

## Disposição

**FIX**, sem bloqueio de pesquisa. Após as quatro mudanças mínimas, o documento pode ser revisto de
forma estreita apenas quanto a gates, próximo passo e coerência de status/processo; não é necessária
nova pesquisa para resolver este parecer.

---

## Re-review estreito — 2026-08-13

### Verificações

- **Quatro gates e consequências:** `Unidade conceitual`, `Representação`, `Evidência sobre o todo`
  e `Autoridade` agora nomeiam decisões futuras distintas. Cada gate declara uma consequência
  concreta de escolha errada, e nenhum é apresentado como resolvido.
- **Próximo passo singular:** o programa identifica obter e aprovar o primeiro lote de findings
  internos comparáveis como próximo gate. A pesquisa externa é explicitamente paralela e não o
  substitui.
- **Condição de saída:** o critério exige cobertura nominal do corpus, incluindo `domainspec-v2`,
  preservação de positivos, negativos e incertezas, independência classificatória do vocabulário
  externo e review independente `KEEP`. É verificável sem antecipar o resultado da pesquisa.
- **Coerência README/programa:** a disciplina de atualização esclarece que findings aceitos de uma
  única linha podem entrar apenas como resultados limitados àquela linha; afirmações cruzadas ou
  gerais continuam dependendo da comparação interna–externa. Isso torna explícita a interpretação
  que faltava à regra mais curta do README.
- **`proposed` versus `active`:** o estado atual distingue inequivocamente o internal tool proposto
  do programa de pesquisa ativo e nega ratificação implícita de teoria, interface ou autoridade.
- **Clareza e concisão:** as adições são proporcionais ao problema. Os gates substituem abstrações
  distribuídas por decisões legíveis, e o próximo passo pode ser encontrado sem reconstruir o plano
  a partir de várias seções.

### Findings sobreviventes

Nenhum finding MAJOR ou MINOR sobrevive dentro do escopo desta re-verificação. A menção ao bloqueio
operacional informa o estado do caminho crítico sem converter este documento em relatório de
execução.

### Disposição final

**PASS / KEEP.** Os quatro change requests do review original foram resolvidos. O programa está apto
a funcionar como referência decisória curta do Composition Lab, preservando seus limites de
autoridade e a condição de lentes como somente o Caso 1.
