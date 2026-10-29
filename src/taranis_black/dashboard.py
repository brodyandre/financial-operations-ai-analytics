"""Camada de apresentação do dashboard, isolada do Streamlit e dos gráficos.

Todos os valores são derivados dos CSVs auditáveis e do motor já existente.
Sem chamadas a modelos de IA, APIs, ERP ou dados reais.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from .audit import PROJECT_ROOT, build_audit, money, read_rows
from .prioritization import build_result, load_config

DATA_DIR = PROJECT_ROOT / "data" / "derived"
REVENUE = "TOTAL RECEITA BRUTA"
EBITDA = "EBITDA (RESULTADO OPERACIONAL ANTES DE JUROS/IMP.)"
NET_INCOME = "LUCRO LÍQUIDO DO EXERCÍCIO"
MAIN_ACCOUNTS = (REVENUE, EBITDA, NET_INCOME)
PERIODS = {"Ano completo": "annual", "1º trimestre": "q1", "2º trimestre": "q2", "3º trimestre": "q3", "4º trimestre": "q4"}


def _as_decimal(value: str | int | Decimal | float) -> Decimal:
    return Decimal(str(value))


def load_data(data_dir: Path = DATA_DIR) -> dict:
    """Carrega, recompõe e valida os dados. Não utiliza relatórios pré-gerados."""
    audit = build_audit(data_dir)
    if audit["summary"]["failed"]:
        raise ValueError("Auditoria contábil reprovada: interrompendo o dashboard.")
    dre_rows = read_rows(data_dir / "dre_trimestral.csv")
    rows = {row["account"]: row for row in dre_rows}
    for account in MAIN_ACCOUNTS:
        if account not in rows:
            raise ValueError(f"Conta principal ausente: {account}")
    ranking = build_result(load_config())
    return {
        "audit": audit,
        "dre_rows": dre_rows,
        "dre_by_account": rows,
        "products": read_rows(data_dir / "receita_por_linha.csv"),
        "operations": read_rows(data_dir / "gargalos_operacionais.csv"),
        "ranking": ranking,
    }


def account_value(data: dict, name: str, period: str, kind: str) -> Decimal:
    if period not in PERIODS.values():
        raise ValueError(f"Período inválido: {period}")
    if kind not in ("budget", "actual"):
        raise ValueError(f"Tipo inválido: {kind}")
    return money(data["dre_by_account"][name][f"{period}_{kind}"])


def percentage_change(actual: Decimal, budget: Decimal) -> Decimal | None:
    return ((actual - budget) / budget * 100) if budget else None


def quarterly_series(data: dict, account: str) -> list[dict]:
    return [{
        "quarter": f"T{idx}",
        "budget": account_value(data, account, f"q{idx}", "budget"),
        "actual": account_value(data, account, f"q{idx}", "actual"),
    } for idx in (1, 2, 3, 4)]


def summary_for_period(data: dict, period: str = "annual") -> dict:
    result = {}
    for label, account in (("revenue", REVENUE), ("ebitda", EBITDA), ("net_income", NET_INCOME)):
        budget = account_value(data, account, period, "budget")
        actual = account_value(data, account, period, "actual")
        result[label] = {
            "budget": budget,
            "actual": actual,
            "difference": actual - budget,
            "variance_pct": percentage_change(actual, budget),
        }
    return result


def reconciliation(data: dict) -> dict:
    diffs = data["audit"]["cross_sheet_reconciliation"]
    return {row["comparison"]: {
        "dre": money(row["dre"]),
        "products": money(row["products"]),
        "difference": money(row["difference_dre_minus_products"]),
    } for row in diffs}


def expense_overruns(data: dict) -> list[dict]:
    return [{
        "account": row["account"],
        "budget": money(row["budget_cost"]),
        "actual": money(row["actual_cost"]),
        "overrun": money(row["unfavorable_variance"]),
        "source": row["source"],
    } for row in data["audit"]["expense_overruns"]]


def simulate_triage(
    monthly_orders: int = 200,
    reduction_pct: Decimal | float | int = Decimal("25"),
    hourly_cost: Decimal | float | int = Decimal("60"),
    upfront_cost: Decimal | float | int = Decimal("15000"),
    monthly_maintenance: Decimal | float | int = Decimal("300"),
    *,
    baseline_minutes: Decimal | float | int = Decimal("40"),
    months: int = 12,
) -> dict:
    """Cenário C01: valor teórico de capacidade, nunca economia observada."""
    if type(monthly_orders) is not int or not 0 <= monthly_orders <= 100_000:
        raise ValueError("Pedidos/mês devem ser inteiro entre 0 e 100000.")
    if type(months) is not int or not 1 <= months <= 60:
        raise ValueError("Meses fora do intervalo permitido.")
    pct = _as_decimal(reduction_pct)
    hourly = _as_decimal(hourly_cost)
    upfront = _as_decimal(upfront_cost)
    maintenance = _as_decimal(monthly_maintenance)
    baseline = _as_decimal(baseline_minutes)
    if not pct.is_finite() or not Decimal("0") <= pct <= Decimal("100"):
        raise ValueError("Redução deve ficar entre 0 e 100%.")
    if any(not v.is_finite() or v < 0 for v in (hourly, upfront, maintenance, baseline)):
        raise ValueError("Custos e tempos devem ser números não negativos e finitos.")
    hours = _as_decimal(monthly_orders) * baseline * (pct / 100) / 60
    annual_capacity_value = hours * hourly * months
    total_cost = upfront + maintenance * months
    net_illustrative = annual_capacity_value - total_cost
    theoretical_roi = (net_illustrative / total_cost * 100) if total_cost else None
    return {
        "orders_per_month_assumed": monthly_orders,
        "minutes_released_per_order": baseline * pct / 100,
        "hours_released_per_month": hours,
        "capacity_value_brl": annual_capacity_value,
        "cost_brl": total_cost,
        "balance_brl": net_illustrative,
        "roi_pct_if_monetized": theoretical_roi,
        "label": "HIPÓTESE DIDÁTICA, sem ganhos realizados nem validação operacional",
    }


def pt_brl(value: Decimal | str | int | float, compact: bool = False) -> str:
    number = _as_decimal(value)
    if compact:
        if abs(number) >= 1_000_000:
            return f"R$ {_pt_number(number / 1_000_000, 2)} mi"
        if abs(number) >= 1_000:
            return f"R$ {_pt_number(number / 1_000, 0)} mil"
    return "R$ " + _pt_number(number, 2)


def _pt_number(number: Decimal, places: int) -> str:
    quantized = number.quantize(Decimal("1").scaleb(-places), rounding=ROUND_HALF_UP)
    rendered = f"{quantized:,.{places}f}"
    return rendered.replace(",", "§").replace(".", ",").replace("§", ".")


def pt_percent(value: Decimal | None) -> str:
    return "N/D" if value is None else _pt_number(value, 2) + "%"


def prompt_for_chatgpt(data: dict, period: str = "annual") -> str:
    metrics = summary_for_period(data, period)
    rev = reconciliation(data)["realizada"]
    cost = expense_overruns(data)
    lines = [
        "Você é um consultor financeiro da Taranis Black (empresa fictícia).",
        "Analise SOMENTE os indicadores auditados abaixo, em português brasileiro.",
        "Não invente causas, resultados de implantação, economias ou integrações.",
        f"Período: {period}.",
    ]
    for key, title in (("revenue", "Receita bruta DRE"), ("ebitda", "EBITDA"), ("net_income", "Lucro líquido")):
        m = metrics[key]
        lines.append(f"- {title}: orçado {pt_brl(m['budget'])}; realizado {pt_brl(m['actual'])}; desvio {pt_percent(m['variance_pct'])}.")
    lines += [
        f"- Receita anual DRE vs produtos: {pt_brl(rev['dre'])} vs {pt_brl(rev['products'])}; diferença SEM CAUSA CONFIRMADA {pt_brl(rev['difference'])}.",
        "- Desvios anuais de despesas (não são economias): " + "; ".join(f"{x['account']} {pt_brl(x['overrun'])}" for x in cost),
        "- Há quatro achados documentais de qualidade de dados em aberto.",
        "- Indicadores operacionais são estimativas/valores do cenário; evite somar com a DRE por possível sobreposição.",
        "- C02 é conciliação financeira determinística no protótipo; IA auxilia análise, sem modelo treinado.",
        "Produza: 1) resumo executivo objetivo; 2) três prioridades verificáveis; 3) riscos e próximos passos de validação humana; 4) limitações das evidências.",
        "Não extrapole quatro trimestres como previsão estatisticamente validada.",
    ]
    return "\n".join(lines)
