"""Rota 0 Etapa 3: validações estruturais da proposta de governança (não de conformidade legal)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs" / "governance_controls_2026.json"
EXPECTED_CASES = {"C01", "C02", "C03"}
REQUIRED_THEMES = {
    "inventory", "lawful_basis", "prohibited_automation", "human_oversight",
    "provenance", "security", "bias_and_validation", "retention",
    "incident_response", "third_party", "data_subject_rights", "audit_and_change",
}


def load_config(path: Path = CONFIG) -> dict:
    """Lê o registro da proposta; não faz chamadas externas."""
    return json.loads(path.read_text(encoding="utf-8"))


def risk_level(score: int) -> str:
    """Bandas ilustrativas definidas para o case, não uma taxonomia oficial."""
    if not isinstance(score, int) or isinstance(score, bool) or not 1 <= score <= 25:
        raise ValueError("risk score deve ser inteiro entre 1 e 25")
    if score <= 5:
        return "baixo"
    if score <= 11:
        return "moderado"
    if score <= 19:
        return "alto"
    return "crítico"


def validate_config(cfg: dict) -> None:
    """Verifica consistência, bloqueios e cobertura de riscos da proposta."""
    if cfg.get("policy_status") != "draft_for_review_not_approved":
        raise ValueError("status de política deve indicar rascunho não aprovado")
    if cfg.get("approved_for_production") is not False:
        raise ValueError("nenhuma aprovação de produção pode ser alegada")
    if cfg.get("data_scope") != "synthetic_mock_data_only":
        raise ValueError("escopo de dados deve ser estritamente sintético")
    if set(cfg.get("use_cases", [])) != EXPECTED_CASES or len(cfg["use_cases"]) != 3:
        raise ValueError("esperados C01, C02, C03 sem duplicações")

    controls = cfg.get("controls")
    if not isinstance(controls, list) or len(controls) < len(REQUIRED_THEMES):
        raise ValueError("registro de controles incompleto")
    ids = [item.get("id") for item in controls]
    if len(ids) != len(set(ids)) or any(not isinstance(x, str) or not x.startswith("G-") for x in ids):
        raise ValueError("IDs de controles inválidos ou repetidos")
    themes = [item.get("theme") for item in controls]
    if len(themes) != len(set(themes)) or not REQUIRED_THEMES.issubset(themes):
        raise ValueError("temas mínimos ausentes ou duplicados")
    case_coverage = set()
    for item in controls:
        for field in ("owner", "requirement", "evidence"):
            minimum = 5 if field == "owner" else 15
            if not isinstance(item.get(field), str) or len(item[field].strip()) < minimum:
                raise ValueError(f"controle {item.get('id')}: {field} insuficiente")
        cases = item.get("cases")
        if not isinstance(cases, list) or not cases or not set(cases).issubset(EXPECTED_CASES):
            raise ValueError("aplicabilidade do controle inválida")
        if item.get("review_required") is not True:
            raise ValueError("revisão humana não pode ser desativada nos controles")
        case_coverage.update(cases)
    if case_coverage != EXPECTED_CASES:
        raise ValueError("falta cobertura por caso")
    for item in controls:
        if item["theme"] == "prohibited_automation" and not {"C01", "C02"}.issubset(item["cases"]):
            raise ValueError("automação de crédito e conciliação devem ter gate")

    risks = cfg.get("risks")
    if not isinstance(risks, list) or len(risks) < 6:
        raise ValueError("inventário de risco insuficiente")
    risk_ids = [risk.get("id") for risk in risks]
    if len(set(risk_ids)) != len(risk_ids) or any(not isinstance(x, str) or not x.startswith("R-") for x in risk_ids):
        raise ValueError("IDs de riscos inválidos ou duplicados")
    for risk in risks:
        cases = risk.get("cases")
        if not isinstance(cases, list) or not cases or not set(cases).issubset(EXPECTED_CASES):
            raise ValueError("caso de risco inválido")
        for key in ("probability", "impact"):
            val = risk.get(key)
            if not isinstance(val, int) or isinstance(val, bool) or not 1 <= val <= 5:
                raise ValueError(f"{key} deve ser 1 a 5")
        for field in ("name", "mitigation", "owner", "decision_gate"):
            if not isinstance(risk.get(field), str) or len(risk[field].strip()) < 10:
                raise ValueError(f"risco {risk.get('id')}: campo {field} incompleto")
    predicted = [risk for risk in risks if "C03" in risk["cases"]]
    if not any("bloqueado" in risk["decision_gate"].lower() for risk in predicted):
        raise ValueError("C03 exige bloqueio explícito por dados")

    committee = cfg.get("committee")
    if not isinstance(committee, dict):
        raise ValueError("comitê não definido")
    if len(committee.get("members_by_role", [])) < 5 or len(committee.get("production_approval_requires", [])) < 5:
        raise ValueError("comitê sem papéis ou sem gates de aprovação suficientes")
    if not committee.get("cadence"):
        raise ValueError("comitê sem cadência")


def build_result(cfg: dict) -> dict:
    validate_config(cfg)
    risks = sorted(
        (
            {
                "id": risk["id"],
                "name": risk["name"],
                "score": risk["probability"] * risk["impact"],
                "level": risk_level(risk["probability"] * risk["impact"]),
                "owner": risk["owner"],
                "gate": risk["decision_gate"],
            }
            for risk in cfg["risks"]
        ),
        key=lambda x: (-x["score"], x["id"]),
    )
    return {
        "status": "PROPOSTA_NAO_APROVADA",
        "production_approved": False,
        "synthetic_data_only": True,
        "controls_defined": len(cfg["controls"]),
        "risk_items": len(cfg["risks"]),
        "committee_proposed": True,
        "risk_register": risks,
        "limitations": [
            "Verificação automatizada é estrutural; não demonstra implantação nem conformidade legal.",
            "C03 bloqueado por insuficiência de histórico granular rotulado.",
            "Uso de dados pessoais reais depende de avaliação específica e aprovação competente.",
        ],
    }


def render_report(result: dict) -> str:
    lines = [
        "# Rota 0 — Etapa 3 | Resultado da validação estrutural",
        "",
        "**Status:** PROPOSTA NÃO APROVADA; não representa política vigente ou conformidade jurídica.",
        "",
        f"- Controles propostos: **{result['controls_defined']}**",
        f"- Riscos avaliados consultivamente: **{result['risk_items']}**",
        "- Comitê e rito de auditoria: **propostos; não constituídos**.",
        "- Escopo: **somente dados sintéticos do Mock Data Kit**.",
        "",
        "| Risco | Nota inerente | Nível | Dono proposto |",
        "|---|---:|---|---|",
    ]
    for r in result["risk_register"]:
        lines.append(f"| {r['id']} | {r['score']} | {r['level']} | {r['owner']} |")
    lines += ["", "## Limitações", ""]
    lines += [f"- {item}" for item in result["limitations"]]
    return "\n".join(lines) + "\n"


def main() -> int:
    cfg = load_config()
    result = build_result(cfg)
    output = ROOT / "reports"
    output.mkdir(parents=True, exist_ok=True)
    (output / "rota0_etapa3_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "rota0_etapa3_resumo.md").write_text(render_report(result), encoding="utf-8")
    print(f"Rota 0 Etapa 3: {result['controls_defined']} controles; {result['risk_items']} riscos; proposta não aprovada")
    print(f"Relatórios: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
