"""Experimento sintético reprodutível para uma regra de conciliação de receita.

Os rótulos são definidos manualmente; não se trata de treinamento ou validação
estatística para dados reais. Fonte financeira oficial NÃO é alterada.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any

TOLERANCE = Decimal("0.01")
BASE = Decimal("48500000.00")

# Casos com rótulos deliberadamente predefinidos, incluindo diferenças negativas.
SYNTHETIC_CASES: tuple[tuple[str, str, bool], ...] = (
    ("S01", "0", False), ("S02", "0.001", False),
    ("S03", "-0.001", False), ("S04", "0.005", False),
    ("S05", "-0.005", False), ("S06", "0.009", False),
    ("S07", "-0.009", False), ("S08", "0.01", False),
    ("S09", "0.02", True), ("S10", "-0.02", True),
    ("S11", "0.03", True), ("S12", "-0.03", True),
    ("S13", "1.00", True), ("S14", "-1.00", True),
    ("S15", "125", True), ("S16", "-500", True),
    ("S17", "1500", True), ("S18", "-5000", True),
    ("S19", "600000", True), ("S20", "1100000", True),
)


def detects_gap(dre: Decimal, products: Decimal, tolerance: Decimal = TOLERANCE) -> bool:
    if any(not x.is_finite() for x in (dre, products, tolerance)) or tolerance < 0:
        raise ValueError("Valores devem ser finitos e tolerância não negativa.")
    return abs(dre - products) > tolerance


def run_experiment() -> dict[str, Any]:
    results = []
    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for case_id, difference_str, expected in SYNTHETIC_CASES:
        difference = Decimal(difference_str)
        observed = detects_gap(BASE, BASE - difference)
        key = "tp" if observed and expected else "fp" if observed else "fn" if expected else "tn"
        counts[key] += 1
        results.append({
            "id": case_id,
            "injected_gap_brl": str(difference),
            "expected_flag": expected,
            "detected_flag": observed,
            "result": key.upper(),
        })
    tp, fp, tn, fn = (counts[x] for x in ("tp", "fp", "tn", "fn"))
    return {
        "experiment": "DQ-001 synthetic exception detection",
        "case_count": len(results),
        "tolerance_brl": str(TOLERANCE),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "precision": tp / (tp + fp) if (tp + fp) else None,
        "recall": tp / (tp + fn) if (tp + fn) else None,
        "cases": results,
        "limit": "20 casos construídos e rotulados para exercitar a regra; não demonstra precisão em produção.",
        "data_scope": "100% sintético; valores reais e CSVs oficiais não modificados",
    }
