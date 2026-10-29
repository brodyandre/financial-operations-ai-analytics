#!/usr/bin/env python3
"""Gera os artefatos e valida requisitos mínimos da Etapa 2; biblioteca padrão."""
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.prioritization import build_result, load_config, main, validate_config  # noqa: E402


def run() -> int:
    cfg = load_config()
    main()  # Gera os relatórios somente no diretório reports/.
    result = build_result(cfg)
    scores = {item["id"]: item for item in result["scores"]}
    scenario = {x["orders_per_month_assumed"]: x for x in result["roi_sensitivity"]["scenarios"]}
    docs = ROOT / "docs" / "rota0"
    checks = [
        ("Configuração válida", _is_valid(cfg)),
        ("3 oportunidades", set(scores) == {"C01", "C02", "C03"}),
        ("C02 alto impacto", Decimal(scores["C02"]["impact_score"]) >= Decimal(4)),
        ("C02 baixo esforço no MVP", Decimal(scores["C02"]["effort_score"]) <= Decimal(3)),
        ("C01 requer piloto condicional", scores["C01"]["data_gate"] == "conditional"),
        ("C03 bloqueado por dados", scores["C03"]["data_gate"].startswith("blocked_")),
        ("Recomendação C02 primeiro", result["scores"][0]["id"] == "C02"),
        ("Baseline de triagem 40 min", cfg["roi_sensitivity"]["baseline_minutes_per_order"] == 40),
        ("Cenário 100 pedidos: R$ 12 mil teóricos", scenario[100]["illustrative_annual_capacity_value_brl"] == "12000.00"),
        ("Cenário 200 pedidos: ROI 29,03% hipotético", scenario[200]["illustrative_roi_percent_if_value_realized"] == "29.03"),
        ("Ponto de equilíbrio: 155 pedidos/mês hipotéticos", result["roi_sensitivity"]["breakeven_orders_per_month_if_value_realized"] == "155.00"),
        ("KPIs documentados", "K-10" in (docs / "06_DICIONARIO_KPIS.md").read_text(encoding="utf-8")),
        ("Adoção e supervisão documentadas", "interromper a automação" in (docs / "08_GESTAO_MUDANCA.md").read_text(encoding="utf-8")),
    ]
    failed = 0
    for label, ok in checks:
        print(f'{"PASS" if ok else "FAIL"}: {label}')
        failed += not ok
    print(f'Rota 0 Etapa 2: {len(checks)-failed}/{len(checks)} PASS')
    return failed


def _is_valid(cfg):
    try:
        validate_config(cfg)
        return True
    except (AssertionError, KeyError, ValueError, TypeError):
        return False


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
