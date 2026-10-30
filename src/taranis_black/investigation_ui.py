"""Componente Streamlit isolado; não altera lógica financeira ou fontes."""
from __future__ import annotations

import json

from .dashboard import pt_brl
from .dq_experiment import run_experiment
from .investigation import (
    VALID_ACTIONS,
    VALID_AREAS,
    investigation_brief,
    investigation_snapshot,
    review_record,
)


def render_investigation(data: dict) -> None:
    import pandas as pd
    import streamlit as st

    st.subheader("Investigação financeira · DQ-001")
    st.caption("Caso de uso C02 · auditoria determinística + interpretação consultiva com ChatGPT + revisão humana")
    st.warning("Exceção não reconciliada. A diferença não comprova perda financeira, fraude ou receita recuperável.")

    base = st.segmented_control(
        "Visão anual de receita", options=["realizada", "orçada"], default="realizada",
        format_func=lambda x: "Realizada" if x == "realizada" else "Orçada",
        key="dq001_base",
    )
    if base is None:
        base = "realizada"
    case = investigation_snapshot(data, base)
    cols = st.columns(3)
    cols[0].metric("DRE", pt_brl(case["dre_brl"], compact=True))
    cols[1].metric("Receita por produtos", pt_brl(case["products_brl"], compact=True))
    cols[2].metric("Diferença a investigar", pt_brl(case["difference_brl"], compact=True))

    tabs = st.tabs(["Evidências", "ChatGPT assistido", "Encaminhamento humano", "Experimento controlado"])
    with tabs[0]:
        st.markdown("**Rastro do dado: origem → conferência → exceção**")
        st.caption("Fontes exibidas por extenso, sem rolagem horizontal.")
        evidence_rows = (
            ("DRE", case["dre_brl"], case["sources"][0]),
            ("Produtos", case["products_brl"], case["sources"][1]),
            ("Diferença (DRE − produtos)", case["difference_brl"], "Cálculo determinístico"),
        )
        for reference, value, source in evidence_rows:
            with st.container(border=True):
                st.markdown(f"**{reference}** · **{pt_brl(value)}**")
                st.markdown("**Fonte documental**")
                st.write(source)
        st.markdown("**Próximos testes de hipótese — nenhum foi confirmado**")
        st.markdown("1. Conferir **escopo e canais** contemplados em cada aba.\n2. Comparar o **período de competência** usado nas consolidações.\n3. Examinar **regras de classificação e exclusões** de receita.")
        st.caption(f"SHA-256 da planilha de origem: `{case['source_sha256']}`")
        st.caption("A rastreabilidade é documental; não temos acesso a lançamentos ou transações de ERP.")
    with tabs[1]:
        st.markdown("**Briefing pronto para análise externa no ChatGPT**")
        st.info("Copie o texto abaixo para uma conversa com ChatGPT. Esta aplicação não chama uma API e não valida automaticamente a resposta do modelo.")
        prompt = investigation_brief(case)
        st.code(prompt, language="text")
        st.caption("Revise qualquer resposta contra as duas abas de origem. Hipóteses não são evidências; nenhuma causa deve ser marcada como resolvida.")
    with tabs[2]:
        st.markdown("**Registro de encaminhamento demonstrativo**")
        st.caption("O formulário registra apenas uma ação de investigação. Não aprova conciliação ou lançamento e não grava dados no servidor.")
        with st.form("dq001_review_form"):
            action = st.selectbox("Ação recomendada", sorted(VALID_ACTIONS))
            area = st.selectbox("Área proposta para analisar", sorted(VALID_AREAS))
            note = st.text_area("Nota de acompanhamento (opcional; sem dados pessoais)", max_chars=500)
            submitted = st.form_submit_button("Preparar registro para revisão", type="primary")
        if submitted:
            st.session_state["dq001_record"] = review_record(case, action, area, note)
        record = st.session_state.get("dq001_record")
        if record and record.get("base") == base:
            st.success("Registro de encaminhamento preparado localmente — pendência permanece aberta.")
            st.json(record)
            st.download_button("Exportar registro JSON", data=json.dumps(record, indent=2, ensure_ascii=False), file_name="DQ-001-encaminhamento-demonstrativo.json", mime="application/json")
        elif record:
            st.info("Altere o formulário ou volte à base utilizada para gerar o registro anterior.")
    with tabs[3]:
        result = run_experiment()
        st.markdown("**Teste laboratorial de detecção de diferenças conhecidas**")
        cols = st.columns(4)
        cols[0].metric("Cenários sintéticos", result["case_count"])
        cols[1].metric("Classificados corretamente", result["true_positives"] + result["true_negatives"])
        cols[2].metric("Falsos positivos", result["false_positives"])
        cols[3].metric("Falsos negativos", result["false_negatives"])
        st.caption(f"Tolerância R$ {result['tolerance_brl']}. {result['limit']}")
        st.dataframe(pd.DataFrame(result["cases"]), hide_index=True, width="stretch")
        st.download_button("Exportar resultado sintético", data=json.dumps(result, ensure_ascii=False, indent=2), file_name="DQ-001-experimento-sintetico.json", mime="application/json")
        st.caption("Não é medição de economia, produtividade, acurácia de IA ou desempenho em produção.")
