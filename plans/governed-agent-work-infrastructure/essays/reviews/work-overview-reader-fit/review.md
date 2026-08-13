# Review — `work-and-knowledge-system-overview.md`

## Coverage

| attacker | lens | findings raised | zero-findings defence (if any) |
|---|---|---:|---|
| Drucker, Peter | reader fit, need-driven narrative, editorial economy, terminology timing e composições retrospectivas | 3 | — |

O documento completo foi atacado como uma única experiência de leitura, da apresentação do objetivo às leituras complementares. A revisão testou todas as lentes declaradas: adequação a um leitor inteligente, prático e sem familiaridade prévia; progressão movida por perguntas; custo editorial; momento de introdução dos termos; e se as composições finais reutilizam partes já compreendidas. Não foram identificadas falhas verificáveis de economia editorial ou de timing terminológico além das que participam diretamente dos achados abaixo; queixas apenas preferenciais foram descartadas.

## `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| 1 | `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md:78` | “Considere uma pessoa responsável por mudar o comportamento de um produto de software. Ela conhece o resultado desejado e algumas restrições, mas ainda não sabe tudo o que precisa ser feito.” Em seguida, o sistema “apresenta uma proposta inspecionável” e, diante de uma decisão fora dos limites, “ela volta para quem tem autoridade” (linhas 81–90). O suposto exemplo não fornece um resultado, uma restrição, uma divisão, uma decisão ou uma evidência concretos; ele repete o modelo abstrato em forma narrativa. Isso priva o leitor prático do caso que deveria tornar o restante intuitivo. | MAJOR | Substituir o cenário genérico por um caso curto e concreto que mostre pedido, proposta de divisão, limite de autoridade, uma intervenção real e as evidências entregues no final. |
| 2 | `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md:106` | A seção promete: “Um segundo olhar: as partes que apareceram no percurso” e diz que “Alguns nomes agora permitem distinguir partes” (linhas 106–109). Porém, apenas dentro da terceira composição surgem “uma revisão, [...] uma decisão de aceitação e [...] o escopo no qual essa aceitação vale”, seguidos das primeiras definições de “conhecimento” e “proveniência” (linhas 174–180). A síntese deixa de ser retrospectiva justamente no componente de conhecimento: introduz peças e regras novas enquanto deveria mostrar como peças já compreendidas se combinam. | MAJOR | Apresentar revisão, aceitação, escopo, conhecimento e proveniência como partes locais no “segundo olhar”; deixar a seção de composição apenas relacioná-las e explicar o efeito emergente. |
| 3 | `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md:111` | “A descrição aprovada do que deve acontecer é um **dispatch**. Ela registra o resultado procurado, a forma proposta para o trabalho, os limites aplicáveis e as decisões já tomadas.” Depois, “Um objetivo, uma divisão proposta, um dispatch aprovado, participantes, papéis, autoridade e limites formam” o trabalho delimitado (linhas 145–150). Resultado/divisão/limites aparecem primeiro como conteúdo do dispatch e depois como partes paralelas a ele. A composição central fica ontologicamente ambígua: o leitor não sabe se está vendo campos de um registro, objetos ligados ou duplicação explicativa. | MAJOR | Escolher e declarar uma relação: ou o dispatch contém objetivo, divisão e limites, ou referencia objetos próprios; então listar a composição sem duplicar os mesmos elementos em dois níveis. |

**Verdict:** FIX

## Change requests

1. **MAJOR** — Tornar “Como seria usar o sistema” um caso concreto, com entrada, divisão proposta, limite, intervenção e saída verificável.
2. **MAJOR** — Introduzir localmente as peças do conhecimento antes de reuni-las em “Continuidade do conhecimento”.
3. **MAJOR** — Desambiguar a relação entre dispatch e objetivo, divisão e limites na composição “Trabalho delimitado”.

`exit_reason: verified_change_requests_delivered`  
`agents_spawned: 0`
