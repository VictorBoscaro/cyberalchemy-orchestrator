#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOTOR ECONOMICO — JBP FOODSToGo x RappiAds 2025
================================================
Fonte unica de verdade (SSOT) do business case.

TODOS os numeros deste caso sao DERIVADOS deste modelo. Nenhum PDF ou slide
pode citar um numero que nao saia daqui. Rode `python motor.py` para regenerar
`model.json` (consumido pela camada de conteudo/design).

NATUREZA DOS DADOS
------------------
Os dados de pricelist, features e historico de vendas NAO foram fornecidos no
briefing (o Excel "Pricelist e Projecao" nao veio anexado). Portanto foram
MODELADOS SINTETICAMENTE com ordens de grandeza plausiveis para CPG de
alimentos em q-commerce (Rappi Brasil). Toda premissa esta marcada e isolada
na secao PREMISSAS para que possa ser substituida pelos numeros reais sem
mexer na logica.

CADEIA LOGICA DO CASO
---------------------
Investimento (tier) -> alocado por estrategia -> gera GMV incremental via ROAS
(com saturacao) -> GMV incremental x margem de contribuicao = margem de
contribuicao incremental -> RETORNO LIQUIDO DE MARGEM = margem de contribuicao
incremental - investimento -> ROMI = retorno liquido de margem / investimento.

ATENCAO A NOMENCLATURA (correcao importante para o CFO)
-------------------------------------------------------
O que este modelo calcula NAO e "lucro liquido". E o retorno de MARKETING sobre
a MARGEM DE CONTRIBUICAO incremental. Fica ANTES de custos fixos, opex, impostos
e logistica. A metrica correta e ROMI (Return on Marketing Investment), nao ROI
de fundo de DRE, e nao deve ser apresentada como lucro liquido da empresa.
"""

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

# =====================================================================
# 1. PREMISSAS (todas explicitas, todas substituiveis por dado real)
# =====================================================================

MOEDA = "USD"

# --- 1.1 Historico de vendas organicas na Rappi (sinteticas) ----------
# GMV mensal organico de FOODSToGo na Rappi nos ultimos 12 meses (USD).
# Padrao: sazonalidade com picos em datas de "encontro/pre-evento"
# (jun=festa junina, out, dez=festas). Base media ~ 250k/mes.
HISTORICO_GMV_MENSAL = {
    "2024-01": 210_000, "2024-02": 225_000, "2024-03": 240_000,
    "2024-04": 235_000, "2024-05": 250_000, "2024-06": 305_000,  # festa junina
    "2024-07": 260_000, "2024-08": 255_000, "2024-09": 270_000,
    "2024-10": 310_000, "2024-11": 300_000, "2024-12": 380_000,  # festas de fim de ano
}
# Ticket medio e margem
TICKET_MEDIO = 18.0                 # USD por pedido
MARGEM_CONTRIBUICAO = 0.38          # 38% — margem de contribuicao CPG alimentos
#   (margem sobre a venda que "sobra" para cobrir midia e gerar lucro)

# --- 1.2 Catalogo de features RappiAds (Pricelist sintetico) ----------
# Preco MAXIMO a negociar (teto) por feature, base anual, e metrica de eficiencia.
# roas_base = retorno em GMV por USD investido, ANTES de saturacao/cenario.
FEATURES = [
    # nome,                  funil,        preco_teto_anual, roas_base, papel
    ("Banner Home",          "topo",        140_000, 2.6, "alcance"),
    ("Banner Categoria",     "meio",         90_000, 3.2, "alcance"),
    ("Push Segmentado",      "meio",         70_000, 4.1, "momentos"),
    ("Sponsored Products",   "fundo",       160_000, 5.2, "performance"),
    ("Cupom Cofinanciado",   "fundo",       120_000, 4.6, "performance"),
    ("Brand Page / Loja",    "topo",         80_000, 2.9, "alcance"),
    ("Ativacao de Momento",  "fundo",       130_000, 5.6, "momentos"),  # bursts em datas
    ("Video / Rich Media",   "topo",         60_000, 2.4, "alcance"),
]

# --- 1.3 Estrategias: mix de alocacao do investimento -----------------
# Cada estrategia distribui 100% do investimento entre os PAPEIS das features.
# (alcance / meio-funil implicito / performance / momentos)
ESTRATEGIAS = {
    "Alcance": {
        "tese": "Construir presenca de marca no topo do funil; barato por impressao, "
                "reach amplo, conversao difusa. Menor risco, ROI mais lento.",
        "mix":  {"alcance": 0.65, "momentos": 0.10, "performance": 0.25},
    },
    "Performance": {
        "tese": "Capturar intencao no fundo do funil; venda direta rapida, "
                "reach mais estreito, ROI mais rapido.",
        "mix":  {"alcance": 0.15, "momentos": 0.20, "performance": 0.65},
    },
    "Momentos": {
        "tese": "Concentrar investimento nas janelas de pico do territorio da marca "
                "(fim de semana, festas, pre-evento). Maior eficiencia por USD.",
        "mix":  {"alcance": 0.20, "momentos": 0.55, "performance": 0.25},
    },
    "Blend Recomendado": {
        "tese": "Ancorado em Momentos + Performance com base de Alcance para "
                "sustentar a marca. Equilibra ROI e construcao de territorio.",
        "mix":  {"alcance": 0.25, "momentos": 0.40, "performance": 0.35},
    },
}

# roas medio por PAPEL (derivado das features daquele papel)
def _roas_por_papel():
    acc, cnt = {}, {}
    for _, _, _, roas, papel in FEATURES:
        acc[papel] = acc.get(papel, 0) + roas
        cnt[papel] = cnt.get(papel, 0) + 1
    return {p: acc[p] / cnt[p] for p in acc}

ROAS_PAPEL = _roas_por_papel()  # {'alcance':..., 'momentos':..., 'performance':...}

# --- 1.4 Cenarios: multiplicador sobre o ROAS (incerteza) -------------
CENARIOS = {
    "Conservador": 0.75,   # execucao/eficiencia abaixo do esperado
    "Base":        1.00,   # premissa central
    "Otimista":    1.25,   # execucao e sazonalidade a favor
}

# --- 1.5 Tiers de investimento (700k como teto; ancoragem) ------------
TIERS = {
    "Enxuto":     400_000,
    "Alvo (JBP)": 700_000,
    "Ampliado": 1_000_000,
}

# --- 1.6 Saturacao (retornos decrescentes) ----------------------------
# ROAS efetivo cai conforme o investimento sobe alem de um ponto de referencia.
# Modelado como fator = (ref / spend) ^ elasticidade, limitado a [0.7, 1.15].
SPEND_REFERENCIA = 700_000
ELASTICIDADE_SATURACAO = 0.18

def fator_saturacao(spend: float) -> float:
    f = (SPEND_REFERENCIA / spend) ** ELASTICIDADE_SATURACAO
    return max(0.7, min(1.15, f))

# =====================================================================
# 2. MOTOR DE CALCULO
# =====================================================================

@dataclass
class Resultado:
    estrategia: str
    tier: str
    cenario: str
    investimento: float
    roas_efetivo: float
    gmv_incremental: float
    margem_contrib_incremental: float
    retorno_liquido_margem: float  # margem de contrib. incremental - investimento (NAO e lucro liquido)
    romi: float                    # retorno_liquido_margem / investimento (Return on Marketing Investment)
    pedidos_incrementais: int

def roas_estrategia(mix: dict) -> float:
    """ROAS ponderado pela alocacao da estrategia."""
    return sum(peso * ROAS_PAPEL[papel] for papel, peso in mix.items())

def calcular(estrategia: str, tier: str, cenario: str) -> Resultado:
    invest = TIERS[tier]
    mix = ESTRATEGIAS[estrategia]["mix"]
    roas_bruto = roas_estrategia(mix)
    roas_ef = roas_bruto * CENARIOS[cenario] * fator_saturacao(invest)
    gmv_inc = invest * roas_ef
    margem_inc = gmv_inc * MARGEM_CONTRIBUICAO
    retorno_liq = margem_inc - invest      # NAO e lucro liquido: antes de opex/fixos/impostos
    romi = retorno_liq / invest            # Return on Marketing Investment (base margem de contrib.)
    pedidos = int(gmv_inc / TICKET_MEDIO)
    return Resultado(
        estrategia, tier, cenario,
        round(invest, 2), round(roas_ef, 3), round(gmv_inc, 2),
        round(margem_inc, 2), round(retorno_liq, 2), round(romi, 4), pedidos,
    )

# =====================================================================
# 3. EXECUCAO — gera todas as combinacoes e emite JSON
# =====================================================================

def gerar_modelo() -> dict:
    hist_total = sum(HISTORICO_GMV_MENSAL.values())
    resultados = []
    for est in ESTRATEGIAS:
        for tier in TIERS:
            for cen in CENARIOS:
                resultados.append(asdict(calcular(est, tier, cen)))

    # tabela-resumo: Blend Recomendado no tier Alvo (700k), 3 cenarios
    resumo_recomendado = [
        asdict(calcular("Blend Recomendado", "Alvo (JBP)", c)) for c in CENARIOS
    ]

    return {
        "moeda": MOEDA,
        "premissas": {
            "ticket_medio": TICKET_MEDIO,
            "margem_contribuicao": MARGEM_CONTRIBUICAO,
            "spend_referencia": SPEND_REFERENCIA,
            "elasticidade_saturacao": ELASTICIDADE_SATURACAO,
            "roas_por_papel": {k: round(v, 3) for k, v in ROAS_PAPEL.items()},
        },
        "nomenclatura": {
            "metrica_retorno": "ROMI (Return on Marketing Investment)",
            "base": "margem de contribuicao incremental",
            "aviso": ("retorno_liquido_margem = margem de contribuicao incremental - "
                      "investimento em midia. NAO e lucro liquido: fica antes de "
                      "custos fixos, opex, impostos e logistica."),
        },
        "historico_gmv_mensal": HISTORICO_GMV_MENSAL,
        "historico_gmv_total_12m": hist_total,
        "features": [
            {"nome": n, "funil": f, "preco_teto_anual": p,
             "roas_base": r, "papel": pap}
            for (n, f, p, r, pap) in FEATURES
        ],
        "estrategias": {
            k: {"tese": v["tese"], "mix": v["mix"],
                "roas_ponderado": round(roas_estrategia(v["mix"]), 3)}
            for k, v in ESTRATEGIAS.items()
        },
        "cenarios": CENARIOS,
        "tiers": TIERS,
        "resultados": resultados,
        "resumo_recomendado_700k": resumo_recomendado,
    }

def main():
    modelo = gerar_modelo()
    out = Path(__file__).parent / "model.json"
    out.write_text(json.dumps(modelo, indent=2, ensure_ascii=False), encoding="utf-8")

    # print legivel do resumo-chave
    print(f"Historico GMV organico 12m: {modelo['historico_gmv_total_12m']:,} {MOEDA}")
    print(f"ROAS por papel: {modelo['premissas']['roas_por_papel']}")
    print("\nBLEND RECOMENDADO @ 700k (Alvo JBP):")
    print(f"{'Cenario':<14}{'ROAS':>7}{'GMV inc.':>14}{'Marg.contrib.':>14}{'Ret.liq.marg.':>15}{'ROMI':>9}")
    for r in modelo["resumo_recomendado_700k"]:
        print(f"{r['cenario']:<14}{r['roas_efetivo']:>7}"
              f"{r['gmv_incremental']:>14,.0f}{r['margem_contrib_incremental']:>14,.0f}"
              f"{r['retorno_liquido_margem']:>15,.0f}{r['romi']*100:>8.1f}%")
    print(f"\nmodel.json escrito em: {out}")

if __name__ == "__main__":
    main()
