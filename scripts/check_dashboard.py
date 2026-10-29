"""Pré-flight estrito para o dashboard, sem instalar dependências gráficas."""
from __future__ import annotations
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.dashboard import load_data, reconciliation, simulate_triage, summary_for_period


def main() -> None:
    data = load_data()
    metrics = summary_for_period(data)
    rec = reconciliation(data)
    checks = [
        ("48 identidades financeiras preservadas", data["audit"]["summary"]["passed"] == 48),
        ("Sem falhas contábeis", data["audit"]["summary"]["failed"] == 0),
        ("4 exceções documentadas", len(data["audit"]["issues"]) == 4),
        ("Receita anual DRE", metrics["revenue"]["actual"] == 48_500_000),
        ("EBITDA anual DRE", metrics["ebitda"]["actual"] == 5_770_000),
        ("Lucro líquido anual", metrics["net_income"]["actual"] == 3_108_600),
        ("Diferença real não ocultada", rec["realizada"]["difference"] == 1_100_000),
        ("Diferença orçada não ocultada", rec["orçada"]["difference"] == 600_000),
        ("Operações do kit", len(data["operations"]) == 5),
        ("Ranking Rota 0 presente", len(data["ranking"]["scores"]) == 3),
        ("Simulação é hipotética", "HIPÓTESE" in simulate_triage()["label"]),
        ("Dashboard compila", compile((ROOT / "dashboard" / "app.py").read_text(encoding="utf-8"), "dashboard/app.py", "exec") is not None),
        ("CSS disponível", (ROOT / "dashboard" / "theme.css").is_file()),
        ("Instruções de execução presentes", (ROOT / "docs" / "rota4" / "07_DASHBOARD_GUIA.md").is_file()),
    ]
    failures = [label for label, ok in checks if not ok]
    for label, ok in checks:
        print(("PASS" if ok else "FAIL") + ": " + label)
    print(f"Dashboard / Fase 2: {len(checks) - len(failures)}/{len(checks)} PASS")
    if failures:
        raise SystemExit(1)
    print("Nota: este pré-flight NÃO substitui abrir a interface no navegador e conferir os gráficos.")


if __name__ == "__main__":
    main()
