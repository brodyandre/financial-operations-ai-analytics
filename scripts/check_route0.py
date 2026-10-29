#!/usr/bin/env python3
"""Validação documental simples da Rota 0/Etapa 1 (somente biblioteca padrão)."""
import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "docs" / "rota0" / "02_REGISTRO_OPORTUNIDADES.csv"
CANVAS = ROOT / "docs" / "rota0" / "01_AI_CANVAS_TARANIS_BLACK.md"
DRE = ROOT / "data" / "derived" / "dre_trimestral.csv"
PRODUCTS = ROOT / "data" / "derived" / "receita_por_linha.csv"
GAPS = ROOT / "data" / "derived" / "gargalos_operacionais.csv"


def validate():
    checks = []
    with CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    checks.append(("3 casos", len(rows) == 3))
    checks.append(("IDs distintos", {r["id"] for r in rows} == {"C01", "C02", "C03"}))
    checks.append(("3 classificações", all(k in " ".join(r["tipo_principal"] for r in rows) for k in ["Generativa", "Tradicional", "Preditiva"])))
    checks.append(("Fontes identificadas", all(r["baseline_fonte"].strip() for r in rows)))
    checks.append(("Revisão humana", all(r["supervisao_humana"].strip() for r in rows)))
    txt = CANVAS.read_text(encoding="utf-8")
    checks.append(("Canvas contempla 3 casos", all(f"### {cid}" in txt for cid in ["C01", "C02", "C03"])))
    checks.append(("Limitação preditiva explícita", "não sustenta treinamento" in txt))
    with DRE.open(encoding="utf-8-sig", newline="") as f:
        dre = list(csv.DictReader(f))
    with PRODUCTS.open(encoding="utf-8-sig", newline="") as f:
        products = list(csv.DictReader(f))
    with GAPS.open(encoding="utf-8-sig", newline="") as f:
        gaps = list(csv.DictReader(f))
    revenue_dre = next(r for r in dre if r["account"] == "TOTAL RECEITA BRUTA")
    revenue_prod = next(r for r in products if r["product"] == "TOTAL TARANIS BLACK")
    checks.append(("Divergência DRE x produtos confirmada", Decimal(revenue_dre["annual_actual"]) - Decimal(revenue_prod["annual_actual"]) == Decimal("1100000")))
    checks.append(("Gargalos disponíveis", len(gaps) == 5))
    checks.append(("Não alegar implantação de C03", "não incluída na versão funcional" in txt))
    failures = 0
    for label, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}: {label}")
        failures += not ok
    print(f"Rota 0 Etapa 1: {len(checks)-failures}/{len(checks)} PASS")
    return failures


if __name__ == "__main__":
    raise SystemExit(1 if validate() else 0)
