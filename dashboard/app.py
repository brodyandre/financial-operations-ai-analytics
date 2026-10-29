"""Financial Operations Intelligence — protótipo local da Taranis Black.

Executar, a partir da raiz do repositório:
    python -m streamlit run dashboard/app.py
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from taranis_black.dashboard import (
    EBITDA,
    NET_INCOME,
    PERIODS,
    REVENUE,
    expense_overruns,
    load_data,
    prompt_for_chatgpt,
    pt_brl,
    pt_percent,
    quarterly_series,
    reconciliation,
    simulate_triage,
    summary_for_period,
)

# Design tokens específicos da demo (não alteram dados nem testes financeiros).
INK = "#0B1220"
BG = "#0B1220"
ACTUAL_COLOR = "#43E0C4"
BUDGET_COLOR = "#FFC857"
PINK = "#F394A8"
AMBER = "#FFCA85"
TEXT = "#E6F0FA"
MUTED = "#C1D1E1"

st.set_page_config(
    page_title="Financial Operations Intelligence | Taranis Black",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"<style>{(Path(__file__).parent / 'theme.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner="Preparando indicadores financeiros…")
def get_data() -> dict:
    return load_data()


def chart_style(fig: go.Figure, title: str, height: int = 370) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=17, color=TEXT)),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=MUTED, size=12),
        margin=dict(l=10, r=18, t=55, b=24),
        height=height,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12, x=1, xanchor="right", font=dict(size=11)),
        xaxis=dict(showgrid=False, linecolor="#35435A"),
        yaxis=dict(gridcolor="#334A65", zerolinecolor="#35435A", tickformat=".2s"),
    )
    return fig


def bar_comparison(data: dict, account: str, title: str) -> go.Figure:
    series = quarterly_series(data, account)
    x = [r["quarter"] for r in series]
    fig = go.Figure()
    fig.add_bar(name="Orçado", x=x, y=[float(r["budget"] / 1_000_000) for r in series], marker_color=BUDGET_COLOR)
    fig.add_bar(name="Realizado", x=x, y=[float(r["actual"] / 1_000_000) for r in series], marker_color=ACTUAL_COLOR)
    chart_style(fig, title)
    fig.update_layout(barmode="group", yaxis_title="R$ milhões", yaxis_tickformat=".2f")
    return fig


def expense_chart(costs: list[dict]) -> go.Figure:
    labels = ["Fretes", "Reentregas", "Inadimplência (PDD)"]
    fig = go.Figure()
    fig.add_bar(name="Orçado", x=labels, y=[float(r["budget"] / 1_000_000) for r in costs], marker_color=BUDGET_COLOR)
    fig.add_bar(name="Realizado", x=labels, y=[float(r["actual"] / 1_000_000) for r in costs], marker_color=ACTUAL_COLOR)
    chart_style(fig, "Despesas críticas · orçado x realizado", height=340)
    fig.update_layout(barmode="group", yaxis_title="R$ milhões", yaxis_tickformat=".2f")
    return fig


def stat_cards(metrics: dict) -> None:
    cols = st.columns(3, gap="medium")
    captions = (("revenue", "Receita bruta", "DRE"), ("ebitda", "EBITDA", "Operacional"), ("net_income", "Lucro líquido", "Resultado final"))
    for col, (key, title, category) in zip(cols, captions):
        m = metrics[key]
        with col:
            with st.container(border=True):
                st.caption(category.upper())
                st.metric(title, pt_brl(m["actual"], compact=True), delta=pt_percent(m["variance_pct"]), help="Variação percentual do realizado em relação ao orçado (DRE).")
                st.caption(f"Orçado: {pt_brl(m['budget'], compact=True)}")


def label_section(title: str, subtitle: str = "") -> None:
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)


def executive(data: dict, period: str) -> None:
    stats = summary_for_period(data, period)
    label_section("Visão executiva", "Números do Mock Data Kit, auditados e sem projeção estatística.")
    stat_cards(stats)
    col1, col2 = st.columns([1.25, 1], gap="large")
    with col1:
        st.plotly_chart(bar_comparison(data, REVENUE, "Receita bruta · evolução trimestral"), width="stretch", config={"displayModeBar": False})
    with col2:
        st.plotly_chart(bar_comparison(data, EBITDA, "EBITDA · evolução trimestral"), width="stretch", config={"displayModeBar": False})
    a, b = st.columns(2, gap="large")
    with a:
        with st.container(border=True):
            st.markdown("**Exceção prioritária · DQ-001**")
            st.metric("DRE menos produtos · realizado anual", pt_brl(reconciliation(data)["realizada"]["difference"], compact=True))
            st.caption("Diferença de conciliação sem causa confirmada. Não representa receita perdida ou economia.")
    with b:
        with st.container(border=True):
            st.markdown("**Piloto proposto · C02**")
            st.markdown("Conciliação financeira e qualidade de dados")
            st.caption("Rotinas determinísticas validadas; ChatGPT participa somente na análise consultiva. Revisão humana obrigatória.")
    st.caption("Fonte: 05_Financas_Orcado_vs_Realizado.xlsx / DRE_Trimestral_Orcado_Real, linhas 5 e 21. A seleção de período altera os KPIs superiores; os gráficos mostram T1–T4.")


def finance(data: dict, period: str) -> None:
    label_section("Análise financeira", "Comparação contábil, com despesas negativas normalizadas apenas para visualização.")
    stats = summary_for_period(data, period)
    rows = []
    for key, label in (("revenue", "Receita bruta"), ("ebitda", "EBITDA"), ("net_income", "Lucro líquido")):
        r = stats[key]
        rows.append({"Conta": label, "Orçado (R$)": float(r["budget"]), "Realizado (R$)": float(r["actual"]), "Diferença (R$)": float(r["difference"]), "Variação": pt_percent(r["variance_pct"])})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", column_config={
        "Orçado (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
        "Realizado (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
        "Diferença (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
    })
    st.plotly_chart(bar_comparison(data, NET_INCOME, "Lucro líquido · variação trimestral"), width="stretch", config={"displayModeBar": False})
    st.divider()
    label_section("Pressões de custo", "Valores anuais da DRE. Não adicionar aos impactos operacionais estimados: possível dupla contagem.")
    costs = expense_overruns(data)
    st.plotly_chart(expense_chart(costs), width="stretch", config={"displayModeBar": False})
    st.dataframe(pd.DataFrame([{"Conta": r["account"], "Orçado": pt_brl(r["budget"]), "Realizado": pt_brl(r["actual"]), "Desvio desfavorável": pt_brl(r["overrun"]), "Origem": r["source"]} for r in costs]), hide_index=True, width="stretch")


def quality(data: dict) -> None:
    label_section("Qualidade e reconciliação", "Os testes verificam identidades e totais internos; divergências entre fontes continuam abertas.")
    a, b, c = st.columns(3)
    audit = data["audit"]
    a.metric("Verificações de consistência", f"{audit['summary']['passed']}/{audit['summary']['automated_checks']}")
    b.metric("Achados documentais", str(audit["summary"]["issues_for_review"]))
    c.metric("Causa de DQ-001", "Não confirmada")
    comparisons = reconciliation(data)
    st.dataframe(pd.DataFrame([{"Base": label.capitalize(), "DRE": pt_brl(v["dre"]), "Produtos": pt_brl(v["products"]), "Diferença": pt_brl(v["difference"])} for label, v in comparisons.items()]), hide_index=True, width="stretch")
    st.warning("A diferença de R$ 1,1 mi no realizado e R$ 600 mil no orçado não deve ser corrigida ou considerada perda até reconciliação de escopo e critérios.")
    st.markdown("**Registro de exceções para análise humana**")
    st.dataframe(pd.DataFrame([{"ID": r["id"], "Prioridade": r["severity"], "Problema": r["title"], "Próxima verificação": r["action"]} for r in audit["issues"]]), hide_index=True, width="stretch")
    with st.expander("Percentuais declarados x calculados por linha de produto"):
        st.dataframe(pd.DataFrame([{"Produto": r["product"], "Declarado (%)": float(r["declared_share_pct"]), "Calculado (%)": float(r["calculated_share_pct"]), "Diferença (p.p.)": float(r["deviation_pp"]), "Status": r["status"]} for r in audit["product_share_recalculation"]]), hide_index=True, width="stretch")
    st.caption("Fontes: planilha 05 da Alura, abas DRE_Trimestral_Orcado_Real e Receita_por_Linha_Produto. A matriz de achados usa audit.py e não modifica as fontes.")


def operations(data: dict) -> None:
    label_section("Operações & diagnóstico Lean", "Gargalos declarados no cenário. Sem medições de melhoria realizadas pelo protótipo.")
    st.dataframe(pd.DataFrame([{"Indicador": r["metric"], "Meta": r["target"], "Atual": r["actual"], "Desvio": r["gap"], "Impacto anual informado": r["estimated_annual_impact"]} for r in data["operations"]]), hide_index=True, width="stretch")
    st.info("Impactos operacionais são estimativas descritas na fonte. Podem se sobrepor a despesas contabilizadas; não os agregamos a um total de economia potencial.")
    st.markdown("**Prioridade do roadmap (julgamento consultivo, não aprovação executiva)**")
    ranks = sorted(data["ranking"]["scores"], key=lambda x: x["id"])
    st.dataframe(pd.DataFrame([{"Caso": r["id"], "Proposta": r["title"], "Impacto / 5": r["impact_score"], "Esforço / 5": r["effort_score"], "Decisão": r["decision"]} for r in ranks]), hide_index=True, width="stretch")
    st.markdown("**Fluxo operacional**")
    st.markdown("Proposta comercial → Triagem manual → Homologação de crédito → Faturamento → Expedição. O desenho TO-BE está documentado em `docs/rota4/02_FLUXOS_AS_IS_TO_BE.md`, com revisão humana nas alçadas de crédito.")
    st.caption("Fontes: Gargalos_Operacionais_Custos e documento 06 de processos. AS-IS, SIPOC e Ishikawa: docs/rota4/. C03 preditivo está bloqueado por ausência de histórico granular.")


def scenarios(data: dict, period: str) -> None:
    label_section("Cenários & apoio com ChatGPT", "Simulação ilustrativa do C01. Nenhuma mudança operacional foi implantada.")
    st.info("O piloto demonstrado é C02 (conciliação financeira). O simulador abaixo é uma hipótese estratégica do C01, não ROI realizado.")
    a, b, c = st.columns(3)
    orders = a.slider("Pedidos por mês (hipótese)", 0, 600, 200, step=10)
    reduction = b.slider("Redução de triagem (%)", 0, 100, 25, step=5)
    rate = c.number_input("Custo-hora ilustrativo (R$)", min_value=0.0, max_value=1000.0, value=60.0, step=5.0)
    with st.expander("Premissas econômicas editáveis", expanded=False):
        upfront = st.number_input("Custo inicial hipotético (R$)", min_value=0.0, value=15000.0, step=1000.0)
        maintenance = st.number_input("Manutenção mensal hipotética (R$)", min_value=0.0, value=300.0, step=50.0)
    result = simulate_triage(orders, reduction, rate, upfront, maintenance)
    s1, s2, s3 = st.columns(3)
    s1.metric("Capacidade liberada / mês", f"{float(result['hours_released_per_month']):.1f} h")
    s2.metric("Valor anual teórico", pt_brl(result["capacity_value_brl"], compact=True))
    s3.metric("ROI se monetizado", pt_percent(result["roi_pct_if_monetized"]))
    st.caption(f"Custo anual total ilustrativo: {pt_brl(result['cost_brl'])}; saldo teórico: {pt_brl(result['balance_brl'])}. Capacidade liberada não significa economia. Base de triagem: 40 min por pedido; horizonte: 12 meses.")
    st.divider()
    label_section("Briefing para análise assistida com ChatGPT", "Texto preparado com valores auditados. Copie manualmente e revise a resposta antes de utilizá-la.")
    st.code(prompt_for_chatgpt(data, period), language=None)
    st.caption("O dashboard não contém API do ChatGPT e não executa inferência de modelo em tempo real. O uso de ChatGPT é externo e consultivo; não enviar dados pessoais ou confidenciais.")


try:
    data = get_data()
except (OSError, ValueError, KeyError) as exc:
    st.error(f"O dashboard foi bloqueado por falha de integridade ou leitura: {exc}")
    st.stop()

with st.sidebar:
    st.markdown("### ◈ TARANIS BLACK")
    st.caption("FINANCIAL OPERATIONS INTELLIGENCE")
    st.divider()
    section = st.radio("Navegação", ["Visão executiva", "Análise financeira", "Qualidade de dados", "Operações", "Cenários & ChatGPT"], label_visibility="collapsed")
    st.divider()
    period_label = st.selectbox("Período dos indicadores", list(PERIODS))
    st.caption("A reconciliação de produtos é anual, independentemente do período selecionado.")
    st.divider()
    st.markdown("**Integridade da fonte**")
    st.success("48/48 verificações financeiras")
    st.caption("4 pendências interpretativas em aberto")
    st.caption("Alura ONE G11 • Rota 4 • 2026")

period = PERIODS[period_label]
st.markdown('<div class="eyebrow">ALURA ONE G11 <span> / </span> TARANIS BLACK <span> / </span> DEMO OFFLINE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="hero-tag">C02 · PILOTO PRIORITÁRIO</div><h1>Financial Operations<br/><span>Intelligence.</span></h1><p>Decisões apoiadas por indicadores auditáveis, reconciliação e governança de IA.</p></div>', unsafe_allow_html=True)
st.caption("Cenário sintético · Dados locais · Não implantado em produção · Revisão humana requerida")

if section == "Visão executiva":
    executive(data, period)
elif section == "Análise financeira":
    finance(data, period)
elif section == "Qualidade de dados":
    quality(data)
elif section == "Operações":
    operations(data)
else:
    scenarios(data, period)

st.divider()
st.caption("FONTE: Mock Data Kit Alura | MOTOR: Python determinístico | ANÁLISE: ChatGPT consultivo | INTEGRAÇÃO ERP: inexistente")
