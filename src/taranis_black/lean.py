"""Rota 4: consistência estrutural de SIPOC, AS-IS, Ishikawa e baselines.

Os artefatos são consultivos: nenhuma automação ou melhoria foi implantada.
Somente biblioteca padrão. Os arquivos CSV derivados têm referência à aba/linha.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "lean_route4_2026.json"
GAPS_CSV = ROOT / "data" / "derived" / "gargalos_operacionais.csv"
DOCS_DIR = ROOT / "docs" / "rota4"
REPORTS_DIR = ROOT / "reports"
EXPECTED_6M = {"Metodo", "Maquina", "Mao de obra", "Material", "Medicao", "Meio ambiente"}


def load_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_gaps_csv(path: Path = GAPS_CSV) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as fp:
        return list(csv.DictReader(fp))


def validate_config(config: dict, gaps: list[dict]) -> None:
    if config.get("status") != "proposta_consultiva_nao_implantada":
        raise ValueError("status não pode alegar implementação")
    if config.get("data_scope") != "somente_dados_sinteticos_alura":
        raise ValueError("escopo deve ser exclusivamente sintético")
    if not str(config.get("source_process", "")).endswith(".docx"):
        raise ValueError("documento de origem operacional ausente")
    if not str(config.get("source_finance", "")).endswith(".xlsx"):
        raise ValueError("planilha financeira de origem ausente")

    steps = config.get("process_stages")
    if not isinstance(steps, list) or len(steps) != 5:
        raise ValueError("processo AS-IS deve ter cinco passos")
    if [step.get("id") for step in steps] != [f"P{i:02d}" for i in range(1, 6)]:
        raise ValueError("IDs ou ordem do AS-IS inconsistentes")
    for step in steps:
        if any(not str(step.get(key, "")).strip() for key in ("name", "activity", "bottleneck", "source")):
            raise ValueError("passo sem atividade, gargalo ou fonte")

    sipoc = config.get("sipoc")
    if not isinstance(sipoc, list) or len(sipoc) != 5:
        raise ValueError("SIPOC deve conter 5 linhas")
    for row in sipoc:
        if any(not str(row.get(key, "")).strip() for key in ("supplier", "input", "process", "output", "customer")):
            raise ValueError("SIPOC possui célula vazia")

    ishikawa = config.get("ishikawa")
    if not isinstance(ishikawa, dict) or set(ishikawa) != EXPECTED_6M:
        raise ValueError("Ishikawa deve conter os seis grupos 6M")
    for group, causes in ishikawa.items():
        if not isinstance(causes, list) or len(causes) < 3 or any(not str(c).strip() for c in causes):
            raise ValueError(f"causas insuficientes em {group}")

    checks = config.get("kpi_source_expectations")
    if not isinstance(checks, list) or len(checks) != 5:
        raise ValueError("esperados cinco KPIs de gargalos")
    if len(gaps) != 5:
        raise ValueError("CSV de gargalos deve conter cinco linhas")
    by_name = {row["metric"]: row for row in gaps}
    if len(by_name) != 5:
        raise ValueError("KPIs CSV repetidos")
    for check in checks:
        row = by_name.get(check["metric"])
        if row is None:
            raise ValueError("KPI de origem não encontrado")
        for field in ("target", "actual", "source_row"):
            if row.get(field) != check.get(field):
                raise ValueError(f"KPI não coincide com fonte: {check['metric']} / {field}")
        if row.get("source_sheet") != "Gargalos_Operacionais_Custos":
            raise ValueError("proveniência da aba de gargalos inconsistente")

    guardrails = config.get("guardrails", {})
    if guardrails.get("human_approval_required") is not True:
        raise ValueError("revisão humana obrigatória")
    for key in ("automatic_credit_approval", "erp_integration_claimed", "financial_benefit_realized_claimed", "predictive_model_claimed"):
        if guardrails.get(key) is not False:
            raise ValueError(f"alegação ou automação não autorizada: {key}")


def build_result(config: dict, gaps: list[dict]) -> dict:
    validate_config(config, gaps)
    return {
        "project": config["project"],
        "status": "PROPOSTA CONSULTIVA NÃO IMPLANTADA",
        "as_is_steps": len(config["process_stages"]),
        "sipoc_rows": len(config["sipoc"]),
        "ishikawa_groups": sorted(config["ishikawa"]),
        "ishikawa_causes": sum(len(v) for v in config["ishikawa"].values()),
        "baseline_metrics": [
            {key: row[key] for key in ("metric", "target", "actual", "source_sheet", "source_row")}
            for row in gaps
        ],
        "safeguards": config["guardrails"],
        "caveats": [
            "Tempos e custos vêm do cenário simulado; não houve medição de melhoria pós-intervenção.",
            "Ciclo do pedido (>5 dias úteis) difere do tempo de fechamento contábil (7 versus 2 dias úteis).",
            "Diferença de R$ 1,1 mi entre receitas DRE e produtos permanece sem conciliação.",
            "R$ 960 mil relatados em fretes extras não equivalem automaticamente ao desvio total de R$ 1,36 mi da DRE.",
            "ERP legado descrito sem API. Nenhuma integração ou decisão de crédito automática é demonstrada.",
        ],
    }


def render_report(result: dict) -> str:
    lines = [
        "# Rota 4 — Etapa 1 | Diagnóstico Lean validado estruturalmente", "",
        f"**Status:** {result['status']}. Não é comprovação de implantação ou resultados obtidos.", "",
        f"- Passos do AS-IS: **{result['as_is_steps']}**",
        f"- Linhas da matriz SIPOC: **{result['sipoc_rows']}**",
        f"- Categorias de Ishikawa: **{len(result['ishikawa_groups'])}**",
        f"- Causas registradas nos 6M: **{result['ishikawa_causes']}**", "",
        "## Baselines sintéticos", "",
        "| Métrica | Meta | Atual | Fonte (linha) |", "|---|---|---|---|",
    ]
    for row in result["baseline_metrics"]:
        lines.append(f"| {row['metric']} | {row['target']} | {row['actual']} | {row['source_sheet']} ({row['source_row']}) |")
    lines.extend(["", "## Ressalvas e limites", ""])
    lines.extend(f"- {item}" for item in result["caveats"])
    return "\n".join(lines) + "\n"


def main() -> int:
    config = load_config()
    gaps = read_gaps_csv()
    result = build_result(config, gaps)
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / "rota4_etapa1_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS_DIR / "rota4_etapa1_resumo.md").write_text(
        render_report(result), encoding="utf-8"
    )
    print(f"Rota 4 Etapa 1: {result['as_is_steps']} passos AS-IS; {result['sipoc_rows']} linhas SIPOC; "
          f"{len(result['ishikawa_groups'])} grupos 6M; {result['ishikawa_causes']} causas")
    print(f"Rota 4 Etapa 1: {len(result['baseline_metrics'])} baselines; proposta não implantada")
    print(f"Relatórios: {REPORTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
