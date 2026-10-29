"""Modelo consultivo transparente para Rota 0 / etapa 2.

Somente biblioteca padrão; pesos/notas são hipóteses. Não modifica dados-fonte.
"""
from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs" / "prioritization_2026.json"


def dec(value: str | int | float | Decimal) -> Decimal:
    # No input calculations rely on floating-point arithmetic.
    return Decimal(str(value))


def round_two(number: Decimal) -> str:
    return str(number.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def load_config(path: Path = CONFIG) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_config(cfg: dict) -> None:
    assert cfg["schema_version"] == "1.0"
    for dimension in ("impact", "effort"):
        weights = cfg["criteria"][dimension]
        assert sum((dec(x) for x in weights.values()), Decimal(0)) == 1, f"pesos {dimension}"
        assert all(dec(x) > 0 for x in weights.values())
    items = cfg["use_cases"]
    assert {c["id"] for c in items} == {"C01", "C02", "C03"}
    for item in items:
        for dimension in ("impact", "effort"):
            assert set(item[dimension]) == set(cfg["criteria"][dimension]), item["id"]
            assert all(isinstance(value, int) and 1 <= value <= 5 for value in item[dimension].values())
        assert item["reason"] and item["decision"] and item["data_gate"]
    s = cfg["roi_sensitivity"]
    assert s["use_case_id"] == "C01"
    assert s["monthly_order_volumes"] and all(type(v) is int and v > 0 for v in s["monthly_order_volumes"])
    assert dec(s["baseline_minutes_per_order"]) == 40
    assert 0 < dec(s["fraction_of_triage_time_reduced"]) < 1
    assert all(dec(s[key]) >= 0 for key in ("illustrative_loaded_hourly_cost_brl", "illustrative_upfront_cost_brl", "illustrative_monthly_maintenance_brl"))
    assert type(s["months"]) is int and s["months"] > 0


def weighted_score(scores: dict, weights: dict) -> Decimal:
    return sum((dec(scores[key]) * dec(weights[key]) for key in weights), Decimal(0))


def rank_cases(cfg: dict) -> list[dict]:
    validate_config(cfg)
    thresholds = cfg["quadrant_rules"]
    ranking = []
    for row in cfg["use_cases"]:
        impact = weighted_score(row["impact"], cfg["criteria"]["impact"])
        effort = weighted_score(row["effort"], cfg["criteria"]["effort"])
        if row["data_gate"].startswith("blocked_"):
            quadrant = "BLOQUEADO: insuficiência de dados"
        elif impact >= dec(thresholds["high_impact_at_least"]) and effort <= dec(thresholds["low_effort_at_most"]):
            quadrant = "ALTO IMPACTO / BAIXO ESFORÇO (MVP)"
        elif impact >= dec(thresholds["high_impact_at_least"]):
            quadrant = "ALTO IMPACTO / MAIOR ESFORÇO"
        else:
            quadrant = "AVALIAR CONDIÇÕES"
        ranking.append({
            "id": row["id"], "title": row["title"],
            "impact_score": round_two(impact), "effort_score": round_two(effort),
            "quadrant": quadrant, "data_gate": row["data_gate"],
            "reason": row["reason"], "decision": row["decision"],
        })
    # Ordinal scores serve as discussion support, not as an economic ROI proxy.
    ranking.sort(key=lambda r: (r["data_gate"].startswith("blocked_"), -dec(r["impact_score"]), dec(r["effort_score"])))
    # Explicitly identify executive rollout order rather than interpreting ranking as an automatic decision.
    return ranking


def sensitivity_cases(cfg: dict) -> dict:
    validate_config(cfg)
    s = cfg["roi_sensitivity"]
    baseline = dec(s["baseline_minutes_per_order"])
    fraction = dec(s["fraction_of_triage_time_reduced"])
    loaded_cost = dec(s["illustrative_loaded_hourly_cost_brl"])
    upfront = dec(s["illustrative_upfront_cost_brl"])
    monthly = dec(s["illustrative_monthly_maintenance_brl"])
    months = dec(s["months"])
    annual_cost = upfront + monthly * months
    saved_minutes_per_order = baseline * fraction
    rows = []
    for monthly_volume in s["monthly_order_volumes"]:
        hours_per_month = dec(monthly_volume) * saved_minutes_per_order / dec(60)
        illustrative_annual_capacity_brl = hours_per_month * loaded_cost * months
        net = illustrative_annual_capacity_brl - annual_cost
        roi = (net / annual_cost * dec(100)) if annual_cost else None
        rows.append({
            "orders_per_month_assumed": monthly_volume,
            "minutes_released_per_order_assumed": round_two(saved_minutes_per_order),
            "hours_released_per_month_assumed": round_two(hours_per_month),
            "illustrative_annual_capacity_value_brl": round_two(illustrative_annual_capacity_brl),
            "illustrative_annual_cost_brl": round_two(annual_cost),
            "illustrative_net_balance_brl": round_two(net),
            "illustrative_roi_percent_if_value_realized": round_two(roi) if roi is not None else None,
        })
    monthly_value_per_one_order = saved_minutes_per_order / dec(60) * loaded_cost * months
    breakeven_volume = annual_cost / monthly_value_per_one_order if monthly_value_per_one_order > 0 else None
    return {
        "scenario_kind": "hipótese didática; não é resultado realizado nem caso econômico aprovado",
        "input_label": s["label"],
        "annual_cost_brl": round_two(annual_cost),
        "breakeven_orders_per_month_if_value_realized": round_two(breakeven_volume) if breakeven_volume is not None else None,
        "scenarios": rows,
        "caveats": s["caveats"],
    }


def build_result(cfg: dict) -> dict:
    ranking = rank_cases(cfg)
    return {
        "assessment_date": cfg["assessment_date"],
        "scope": cfg["evaluation_scope"],
        "assessment_kind": cfg["assessment_kind"],
        "notes": ["Primeiro piloto executivo: C02; segundo após aprovação: C01; C03 não é executável com os dados atuais.",
                  "Não tratar notas subjetivas como prova de ROI, causalidade ou impacto realizado.",
                  "IA no C02 atual é apoio consultivo do ChatGPT; cálculos são determinísticos."],
        "scores": ranking,
        "roi_sensitivity": sensitivity_cases(cfg),
    }


def render_report(result: dict) -> str:
    lines = [
        "# Rota 0 — Etapa 2 | Resultado reproduzível de priorização",
        "", "**Status:** julgamento consultivo para validação humana; não homologado pela Taranis Black.",
        "**Escopo:** protótipo offline, não integração em produção.", "",
        "## Matriz esforço × impacto", "",
        "| Caso | Impacto (1–5) | Esforço (1–5) | Quadrante | Gate de dados |",
        "|---|---:|---:|---|---|",
    ]
    for item in sorted(result["scores"], key=lambda r:r["id"]):
        lines.append(f'| {item["id"]} | {item["impact_score"]} | {item["effort_score"]} | {item["quadrant"]} | {item["data_gate"]} |')
    lines += ["", "**Recomendação:** C02 → C01 (condicional) → C03 (bloqueado até haver histórico).", "", "## Cenários ilustrativos do C01", "",
              "| Pedidos/mês (hipótese) | Horas/mês liberadas (hipótese) | Valor anual de capacidade | Custo anual | ROI teórico se monetizado |",
              "|---:|---:|---:|---:|---:|"]
    for r in result["roi_sensitivity"]["scenarios"]:
        lines.append(f'| {r["orders_per_month_assumed"]} | {r["hours_released_per_month_assumed"]} | R$ {r["illustrative_annual_capacity_value_brl"]} | R$ {r["illustrative_annual_cost_brl"]} | {r["illustrative_roi_percent_if_value_realized"]}% |')
    lines += ["", "**Cuidado:** horas liberadas não são automaticamente economia financeira; o cálculo só teria validade como ROI depois de validar volumes, taxas, custos, adoção e realização econômica com o Financeiro.",
              "A diferença DRE versus produtos de R$ 1,1 milhão é uma pendência contábil, **não** benefício financeiro.",
              "", "## Fontes e metodologia", "",
              "- Fontes: Mock Data Kit da Alura, planilha `05_Financas_Orcado_vs_Realizado.xlsx` e `06_Descritivo_Processo_Operacional_SIPOC.docx`.",
              "- Notas e pesos: `configs/prioritization_2026.json` (hipóteses consultivas explícitas).",
              "- Fórmulas e cálculos: `src/taranis_black/prioritization.py`; valores calculados, sem LLM no cálculo.",
              "- Privilégios e aprovação em produção: política e revisão humana a definir na Rota 0/Etapa 3.", ""]
    return "\n".join(lines)


def main() -> None:
    cfg = load_config()
    result = build_result(cfg)
    reports = ROOT / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "rota0_etapa2_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (reports / "rota0_etapa2_resumo.md").write_text(render_report(result), encoding="utf-8")
    print("Rota 0 / Etapa 2: relatórios gerados em reports/")
    for item in sorted(result["scores"], key=lambda r:r["id"]):
        print(f'{item["id"]}: impacto={item["impact_score"]}; esforço={item["effort_score"]}; {item["quadrant"]}')
    print("ORDEM PROPOSTA: C02 -> C01 (condicional) -> C03 (bloqueado)")


if __name__ == "__main__":
    main()
