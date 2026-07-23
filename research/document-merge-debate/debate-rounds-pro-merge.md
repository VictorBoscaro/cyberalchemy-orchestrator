# Debate — registro do defensor inicial da junção

## Rodada 1 — steelman da rejeição e reteste da tese

Tese oposta lida integralmente: `document-unification-debate/reject-unification.md` (269 linhas,
versão presente em 2026-07-22).

### Argumentos mais fortes da rejeição

1. **Gates não equivalentes.** O critério de ACP cobre ownership da compilação, protocolo ativo,
   higiene de julgamento e autoridade do `DispatchSpec` (ACP, linhas 735–751); o de BC cobre
   candidate/receipt/accepted, release gates, `RoutingState`, change set isolado e capabilities (BC,
   linhas 626–642). Um gate editorial único seria \(G_A\land G_B\), embora o corpus não demonstre
   \(G_A\leftrightarrow G_B\). Isso bloquearia promoção parcial sem ganho lógico demonstrado.
2. **Há mudanças locais reais nos dois sentidos.** Role `researcher`, trust anchor e `JudgmentRound`
   podem mudar ACP sem mudar o wire contract (ACP, linhas 165–189, 253–258 e 330–367); threshold
   inline/artifact, integridade de blobs e retenção podem mudar BC sem mudar a semântica de protocolo
   (BC, linhas 553–568). Portanto, a hipótese universal de co-mudança é falsa.
3. **O mapping central ainda não existe.** ACP tipa atividades como `produce`, `evaluate`, `decide` e
   `approve` (ACP, linhas 303–328), enquanto BC expõe `submit_work`/`submit_review` e coloca decisão
   humana no command plane (BC, linhas 385–474). Antes de definir a função de compilação, proximidade
   lexical não prova identidade operacional.
4. **Proveniência de review é assimétrica.** BC possui review clean-room e registro de remediação
   (BCR, linhas 3–46); no material lido não existe equivalente dentro do diretório de ACP. A junção
   imediata pode apagar quais claims passaram por quais lentes.
5. **Existe alternativa menos acoplada.** Um index, glossário, matriz de correspondência, version pins
   e gate de compatibilidade cruzada podem tornar drift detectável sem compartilhar lifecycle
   editorial. BC já declara relação de aprofundamento e retroalimentação sem identidade documental
   (BC, linhas 28–39).

### Reteste honesto da defesa original

A defesa original mostrou corretamente que existe um conjunto não vazio de invariantes de interface
\(X\): versão exata de review, mudança de topologia/confirmacão e roteamento de correção são tratados
pelos dois textos (ACP, linhas 369–398, 410–412 e 599–609; BC, linhas 345–371, 423–429 e 517–532).
Também mostrou que provar apenas \(P\setminus X\) e \(B\setminus X\) não prova \(X\).

O salto não demonstrado foi concluir que a única autoridade adequada para \(X\) precisa ser o mesmo
documento que contém todo \(P\) e todo \(B\). Uma especificação de interface versionada pode ser dona
de \(X\) e ser pinada por ambos. Isso satisfaz a necessidade lógica sem implicar gate único.

A condição econômica proposta na defesa era:

\[
k(D+S+V-N)>R.
\]

O corpus prova que drift, sincronização e verificação cruzada têm custo não nulo, mas não quantifica
\(D,S,V,N,R\). A tese oposta acrescenta evidência qualitativa de \(N\): mudanças locais existem nos
dois sentidos e gates podem avançar separadamente. Logo, a desigualdade **não está provada**. Isso não
é uma refutação matemática da possibilidade de junção; é suficiente para retirar a recomendação
incondicional “juntar agora”, pois o ônus da mudança recai sobre quem propõe a consolidação.

A defesa também propôs manter documentos separados se menos de 20% dos invariantes de BC tivessem
dependência semântica em ACP. O corpus não contém essa classificação. O limiar foi declarado sugestão
experimental, não fato, portanto não foi cruzado; porém sua ausência impede usá-lo como suporte à
junção.

### Posição revisada após a rodada 1

Não há base suficiente para uma fusão editorial imediata. A conclusão racional provisória é:

- manter ACP e BC separados, com seus gates próprios;
- criar uma camada de integração pequena e canônica para os invariantes \(X\), sem copiar os detalhes
  internos dos dois documentos;
- exigir pins bidirecionais e compatibilidade cruzada antes de promover qualquer claim de interface;
- preservar proveniência de reviews por claim/seção;
- executar a medição de co-mudança, localizabilidade e findings antes de reconsiderar consolidação.

Foi enviado ao autor da tese oposta pedido de concordância sobre essa direção e uma pergunta crítica:
qual deve ser o estatuto do artefato integrador para que ele não se torne uma terceira verdade.

## Rodada 2 — estatuto da interface e acordo

O agente inicialmente contrário aceitou a direção e propôs que o integrador seja normativo apenas
para a função parcial versionada \(f:A\rightharpoonup B\) e para os invariantes cruzados \(X\). ACP
continua canônico para intenção/semântica; BC, para publicação/materialização/routing/consumo. Termo
sem mapping, pin divergente ou probe ausente falha fechado. Essa resposta resolve a objeção da
“terceira verdade”: o integrador não possui autoridade para redefinir nenhum domínio local.

Foi então redigido `document-unification-debate/common-agreement.md`. Na revisão cruzada, o outro
agente identificou que a primeira função de gates deixava casos sobrepostos quando \(a(m)\) e
\(b(m)\) eram verdadeiros mas \(x(m)\) era falso por prova de independência. Ele corrigiu a partição:

\[
G(m)=
\begin{cases}
G_A(m), & a(m)\land\neg b(m)\land\neg x(m)\\
G_B(m), & b(m)\land\neg a(m)\land\neg x(m)\\
G_A(m)\land G_B(m), & a(m)\land b(m)\land\neg x(m)\\
G_A(m)\land G_B(m)\land G_X(m), & x(m).
\end{cases}
\]

A correção foi aceita porque torna os casos explícitos e evita que duas alterações locais agrupadas
escapem de um dos gates, sem acionar desnecessariamente o gate de interface.

Ambos leram integralmente e aceitaram explicitamente a mesma versão final do acordo, SHA-256
`6515958162F9685AA411DC52A335B5001468F2EA0CC8DA51F9041A23A16F862D`. A decisão atual é não fundir;
a questão de uma junção futura fica condicionada a mappings completos e evidência mensurada de
densidade de \(X\), co-mudança, drift, navegação/review e proveniência.
