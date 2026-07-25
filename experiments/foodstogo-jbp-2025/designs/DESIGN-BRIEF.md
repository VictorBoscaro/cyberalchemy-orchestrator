# BRIEF COMPARTILHADO — 5 designs do JBP FOODSToGo × RappiAds 2025

Todos os 5 agentes de design seguem ESTE brief. A identidade visual é o que muda entre eles.

## Regra de ouro
- **Fonte única de verdade do conteúdo:** `../content/conteudo-canonico.md`.
- **Fonte única dos números:** `../model/model.json`.
- Você **aplica design**. Você **NÃO** inventa, altera ou arredonda nenhum número, título de seção, nem a ordem das páginas.
- Idioma **pt-BR**. Autor/apresentador em toda peça: **Leonardo Stonoga**.

## Estrutura fixa de páginas (idêntica nos 5)
1. **CAPA**
2. **ABORDAGEM CFO** (eixo ROI/eficiência) — pode ocupar 1–2 páginas
3. **PÁGINA EM BRANCO**
4. **ABORDAGEM CMO** (eixo território/momentos) — 1–2 páginas
5. **PÁGINA EM BRANCO**
6. **ABORDAGEM CEO** (eixo crescimento) — 1–2 páginas
7. **PÁGINA EM BRANCO**
8. **APÊNDICE TÉCNICO** — 1–3 páginas

## Técnica de paginação (OBRIGATÓRIA — testada, funciona no headless Chrome)
```css
@page { size: A4; margin: 16mm; }
.page   { break-after: page; min-height: 244mm; }   /* cada página de conteúdo */
.blank  { break-after: page; min-height: 244mm; }   /* página em branco (div vazio) */
```
- Cada bloco de conteúdo de página = um elemento com classe `.page`.
- Cada página em branco = `<div class="blank"></div>` (vazio, sem texto).
- NÃO confie apenas em `page-break-after` sem `min-height`: divs pequenos colapsam e a página some.

## Render (HTML → PDF)
```
bash ../render.sh <seu.html> ../out/<seu-nome>.pdf
```
Depois valide a contagem de páginas (o PDF deve ter as 3 páginas em branco + conteúdo).

## Qualidade
- Tabelas legíveis; números alinhados; destaque visual para ROMI e para o "700k".
- Rodapé em todas as páginas de conteúdo: *"Leonardo Stonoga · RappiAds · JBP FOODSToGo 2025"*.
- Autossuficiente: CSS embutido no `<head>`, sem dependências externas de rede (fontes do sistema ou `@font-face` inline; sem CDN).
- Impressão fiel de cores: incluir `-webkit-print-color-adjust: exact; print-color-adjust: exact;` no `body`.
