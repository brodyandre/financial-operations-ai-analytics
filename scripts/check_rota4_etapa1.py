#!/usr/bin/env python3
"""Valida o pacote Lean/SIPOC/Ishikawa sem alterar dados-fonte nem outras fases."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.lean import build_result, load_config, main, read_gaps_csv  # noqa: E402


def run() -> int:
    main()
    result = build_result(load_config(), read_gaps_csv())
    d = ROOT / "docs" / "rota4"
    docs = {p: (d / p).read_text(encoding="utf-8") for p in (
        "01_DIAGNOSTICO_LEAN_EXECUTIVO.md",
        "02_FLUXOS_AS_IS_TO_BE.md",
        "03_MATRIZ_SIPOC.md",
        "04_ISHIKAWA_6M.md",
        "05_PLANO_MELHORIA_E_KPIS.md",
        "06_ROTEIRO_EVIDENCIAS_ETAPA1.md",
    )}
    checklist = [
        ("5 passos do AS-IS", result["as_is_steps"] == 5),
        ("5 registros SIPOC", result["sipoc_rows"] == 5),
        ("6 grupos Ishikawa", len(result["ishikawa_groups"]) == 6),
        ("18 ou mais causas documentadas", result["ishikawa_causes"] >= 18),
        ("5 baselines rastreáveis à planilha", len(result["baseline_metrics"]) == 5),
        ("AS-IS e TO-BE identificados", "AS-IS" in docs["02_FLUXOS_AS_IS_TO_BE.md"] and "TO-BE" in docs["02_FLUXOS_AS_IS_TO_BE.md"]),
        ("Fluxo AS-IS renderizável com Mermaid", "```mermaid" in docs["02_FLUXOS_AS_IS_TO_BE.md"]),
        ("SIPOC com entradas, saídas e clientes", all(s in docs["03_MATRIZ_SIPOC.md"] for s in ("Fornecedor", "Entrada", "Saída", "Cliente"))),
        ("Ishikawa com diagrama Mermaid", "```mermaid" in docs["04_ISHIKAWA_6M.md"]),
        ("Fechamento e ciclo de pedidos diferenciados", "indicadores diferentes" in docs["01_DIAGNOSTICO_LEAN_EXECUTIVO.md"]),
        ("Reconciliação de receita pendente explícita", "R$ 1,1 mi" in docs["01_DIAGNOSTICO_LEAN_EXECUTIVO.md"]),
        ("Evita dupla contagem de fretes", "dupla contagem" in docs["05_PLANO_MELHORIA_E_KPIS.md"]),
        ("Aprovação humana permanece obrigatória", result["safeguards"]["human_approval_required"]),
        ("Não alega ERP integrado nem ROI realizado", not result["safeguards"]["erp_integration_claimed"] and not result["safeguards"]["financial_benefit_realized_claimed"]),
        ("Relatório JSON produzido", (ROOT / "reports" / "rota4_etapa1_result.json").is_file()),
        ("Relatório MD produzido", (ROOT / "reports" / "rota4_etapa1_resumo.md").is_file()),
    ]
    failed = 0
    for label, ok in checklist:
        print(f"{'PASS' if ok else 'FAIL'}: {label}")
        failed += not ok
    print(f"Rota 4 Etapa 1: {len(checklist) - failed}/{len(checklist)} PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run())
