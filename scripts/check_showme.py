"""Validação integrada Show Me Project, sem API externa e sem Streamlit instalado."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.dashboard import load_data
from taranis_black.dq_experiment import run_experiment
from taranis_black.investigation import investigation_brief, investigation_snapshot, review_record


def main() -> None:
    data = load_data()
    real = investigation_snapshot(data)
    budget = investigation_snapshot(data, "orçada")
    experiment = run_experiment()
    prompt = investigation_brief(real)
    record = review_record(real, "Solicitar evidências adicionais", "Controladoria")
    app_path = ROOT / "dashboard" / "app.py"
    app = app_path.read_text(encoding="utf-8")
    checks = [
        ("Receita DRE realizada", real["dre_brl"] == 48_500_000),
        ("Receita de produtos realizada", real["products_brl"] == 47_400_000),
        ("DQ-001 realizada R$ 1,1 milhão", real["difference_brl"] == 1_100_000),
        ("DQ-001 orçada R$ 600 mil", budget["difference_brl"] == 600_000),
        ("Causa não confirmada", real["cause_confirmed"] is False),
        ("Fontes em abas distintas", len(real["sources"]) == 2 and all("/" in s for s in real["sources"])),
        ("Integridade da fonte", len(real["source_sha256"]) == 64),
        ("Prompt distingue hipótese de evidência", "Hipóteses a INVESTIGAR" in prompt and "CAUSA NÃO CONFIRMADA" in prompt),
        ("Prompt proíbe ações ERP", "Não autorize alteração contábil" in prompt),
        ("Revisão sem aprovação contábil", record["accounting_adjustment_authorized"] is False),
        ("Casos sintéticos suficientes", experiment["case_count"] == 20),
        ("Detecção sob condições controladas", experiment["true_positives"] == 12 and experiment["true_negatives"] == 8),
        ("Sem falsa alegação de precisão produtiva", "não demonstra precisão em produção" in experiment["limit"]),
        ("Menu DQ-001 integrado", 'elif section == "Investigação DQ-001":' in app),
        ("Dashboard permanece compilável", compile(app, str(app_path), "exec") is not None),
    ]
    for name, passed in checks:
        print(("PASS" if passed else "FAIL") + ": " + name)
    print(f"Show Me Ready: {sum(ok for _,ok in checks)}/{len(checks)} PASS")
    if not all(ok for _, ok in checks):
        raise SystemExit(1)
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "showme_experimento_sintetico.json").write_text(
        json.dumps(experiment, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Relatório do experimento: {reports / 'showme_experimento_sintetico.json'}")


if __name__ == "__main__":
    main()
