"""Auditoria financeira reproduzível — Taranis Black / ONE G11.

Dependências: apenas a biblioteca padrão Python.
Origem: CSV derivados das três abas do XLSX oficial, sem alteração da fonte.
A IA é usada para interpretar os resultados, nunca para inventar valores.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[2]
SOURCE_NAME = "05_Financas_Orcado_vs_Realizado.xlsx"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def money(value: str | int | Decimal) -> Decimal:
    return Decimal(str(value))


def fmt_brl(value: str | int | Decimal) -> str:
    number = money(value)
    us = f"{number:,.2f}"
    return "R$ " + us.replace(",", "*").replace(".", ",").replace("*", ".")


def pct(value: Decimal) -> str:
    return f"{value * 100:.2f}%".replace(".", ",")


def build_audit(data_dir: Path) -> dict:
    dre_rows = read_rows(data_dir / "dre_trimestral.csv")
    products = read_rows(data_dir / "receita_por_linha.csv")
    bottlenecks = read_rows(data_dir / "gargalos_operacionais.csv")
    manifest = json.loads((data_dir / "source_manifest.json").read_text(encoding="utf-8"))

    dre = {r["account"]: r for r in dre_rows}
    prod = {r["product"]: r for r in products}
    if len(dre) != len(dre_rows) or len(prod) != len(products):
        raise ValueError("Existem descrições de contas/produtos duplicadas nos CSVs.")

    required = [
        "TOTAL RECEITA BRUTA",
        "RECEITA LÍQUIDA OPERACIONAL",
        "LUCRO BRUTO OPERACIONAL",
        "EBITDA (RESULTADO OPERACIONAL ANTES DE JUROS/IMP.)",
        "LUCRO LÍQUIDO DO EXERCÍCIO",
        "Despesas com Fretes e Logística de Entrega CD",
        "Reentregas e Multas por Divergência de Pedido",
        "Provisão para Devedores Duvidosos (Inadimplência B2B)",
    ]
    missing = [name for name in required if name not in dre]
    if missing:
        raise ValueError(f"Contas obrigatórias ausentes na DRE: {missing}")

    def amount(account: str, field: str) -> Decimal:
        return money(dre[account][field])

    checks: list[dict] = []
    for row in dre_rows:
        for kind in ("budget", "actual"):
            calculated = sum((money(row[f"q{q}_{kind}"]) for q in (1, 2, 3, 4)), Decimal(0))
            reported = money(row[f"annual_{kind}"])
            checks.append({
                "id": f"SUM-{row['source_row']}-{kind.upper()}",
                "type": "quarter_sum",
                "account": row["account"],
                "source": f"{SOURCE_NAME} / {row['source_sheet']} / linha {row['source_row']}",
                "status": "PASS" if calculated == reported else "FAIL",
                "expected_annual": str(calculated),
                "reported_annual": str(reported),
            })

    product_total = next((p for p in products if p["product"] == "TOTAL TARANIS BLACK"), None)
    if product_total is None:
        raise ValueError("Total consolidado dos produtos não encontrado.")
    product_items = [p for p in products if p is not product_total]

    for kind in ("budget", "actual"):
        calculated = sum((money(p[f"annual_{kind}"]) for p in product_items), Decimal(0))
        declared = money(product_total[f"annual_{kind}"])
        checks.append({
            "id": f"PROD-{kind.upper()}", "type": "product_sum",
            "status": "PASS" if calculated == declared else "FAIL",
            "calculated": str(calculated), "reported": str(declared),
            "source": f"{SOURCE_NAME} / Receita_por_Linha_Produto / linhas 2 a 6",
        })

    # Conciliação de subtotal: positivos e despesas com sinais negativos.
    identities = [
        ("net_revenue", "RECEITA LÍQUIDA OPERACIONAL", [
            "TOTAL RECEITA BRUTA",
            "Impostos Incidentes (ICMS, PIS, COFINS)",
            "Cancelamentos e Devoluções por Atraso Logístico",
        ]),
        ("gross_profit", "LUCRO BRUTO OPERACIONAL", [
            "RECEITA LÍQUIDA OPERACIONAL",
            "Matéria-prima, Mesh e Componentes de Alumínio",
            "Mão de Obra Fabril e Montagem Direta",
        ]),
        ("ebitda", "EBITDA (RESULTADO OPERACIONAL ANTES DE JUROS/IMP.)", [
            "LUCRO BRUTO OPERACIONAL",
            "Despesas Comerciais e Vendas (Comissões e SDRs)",
            "Despesas com Fretes e Logística de Entrega CD",
            "Reentregas e Multas por Divergência de Pedido",
            "Despesas Administrativas e Sistemas Legados",
            "Provisão para Devedores Duvidosos (Inadimplência B2B)",
            "Marketing Institucional e Geração de Demanda",
        ]),
        ("net_income", "LUCRO LÍQUIDO DO EXERCÍCIO", [
            "EBITDA (RESULTADO OPERACIONAL ANTES DE JUROS/IMP.)",
            "Despesas Financeiras Líquidas e Juros",
            "IRPJ e CSLL Provisionados",
        ]),
    ]
    for key, target, parts in identities:
        for kind in ("budget", "actual"):
            calculated = sum((amount(part, f"annual_{kind}") for part in parts), Decimal(0))
            declared = amount(target, f"annual_{kind}")
            checks.append({
                "id": f"IDENT-{key}-{kind}", "type": "accounting_identity",
                "status": "PASS" if declared == calculated else "FAIL",
                "expected": str(calculated), "reported": str(declared),
                "source": f"{SOURCE_NAME} / DRE_Trimestral_Orcado_Real / totais anuais",
            })

    dre_budget = amount("TOTAL RECEITA BRUTA", "annual_budget")
    dre_actual = amount("TOTAL RECEITA BRUTA", "annual_actual")
    product_budget = money(product_total["annual_budget"])
    product_actual = money(product_total["annual_actual"])
    ebitda_budget = amount("EBITDA (RESULTADO OPERACIONAL ANTES DE JUROS/IMP.)", "annual_budget")
    ebitda_actual = amount("EBITDA (RESULTADO OPERACIONAL ANTES DE JUROS/IMP.)", "annual_actual")
    net_budget = amount("LUCRO LÍQUIDO DO EXERCÍCIO", "annual_budget")
    net_actual = amount("LUCRO LÍQUIDO DO EXERCÍCIO", "annual_actual")

    gaps = []
    for label, kind, d, p in [
        ("orçada", "budget", dre_budget, product_budget),
        ("realizada", "actual", dre_actual, product_actual),
    ]:
        gaps.append({"comparison":label, "dre":str(d), "products":str(p),
                     "difference_dre_minus_products":str(d-p), "source":SOURCE_NAME})

    share_discrepancies = []
    for product in product_items:
        declared = money(product["reported_share_pct"].replace("%", ""))
        calculated = (money(product["annual_actual"]) / product_actual) * 100
        diff_pp = calculated - declared
        share_discrepancies.append({
            "product": product["product"], "declared_share_pct":str(declared),
            "calculated_share_pct":str(calculated.quantize(Decimal("0.01"))),
            "deviation_pp":str(diff_pp.quantize(Decimal("0.01"))),
            "status": "REVIEW" if abs(diff_pp) > Decimal("0.5") else "OK",
            "source": f"{SOURCE_NAME} / Receita_por_Linha_Produto / linha {product['source_row']}",
        })

    expense_items = [
        "Despesas com Fretes e Logística de Entrega CD",
        "Reentregas e Multas por Divergência de Pedido",
        "Provisão para Devedores Duvidosos (Inadimplência B2B)",
    ]
    expense_overruns = [{
        "account": name,
        "budget_cost": str(-amount(name,"annual_budget")),
        "actual_cost": str(-amount(name,"annual_actual")),
        "unfavorable_variance": str(amount(name,"annual_budget")-amount(name,"annual_actual")),
        "source": f"{SOURCE_NAME} / DRE_Trimestral_Orcado_Real / linha {dre[name]['source_row']}",
    } for name in expense_items]

    issues = [
        {"id":"DQ-001", "severity":"high", "title":"Receita bruta anual não reconcilia entre abas",
         "evidence":"A DRE difere do total por linhas de produto no orçado e no realizado.",
         "action":"Confirmar critérios de escopo, canais, período e regras de consolidação. Não somar nem substituir bases sem validação."},
        {"id":"DQ-002", "severity":"medium", "title":"Participações por produto não correspondem integralmente aos valores realizados",
         "evidence":"Os percentuais informados somam 100%, mas diferem dos percentuais calculados a partir dos valores reais por produto.",
         "action":"Definir a base do percentual informado e sinalizar divergências maiores que 0,5 ponto percentual."},
        {"id":"DQ-003", "severity":"medium", "title":"Impactos operacionais estimados podem sobrepor despesas da DRE",
         "evidence":"Gargalos_Operacionais_Custos apresenta impactos estimados, enquanto a DRE apresenta despesas contabilizadas.",
         "action":"Não somar diretamente as estimativas de impacto aos desvios contábeis; solicitar rastreio e conciliação."},
        {"id":"DQ-004", "severity":"medium", "title":"Histórico insuficiente para afirmar precisão preditiva",
         "evidence":"A DRE disponibilizada tem quatro observações trimestrais.",
         "action":"Usar cenários com premissas explícitas; não anunciar previsão estatisticamente validada."},
    ]
    fail_count = sum(c["status"]=="FAIL" for c in checks)
    data = {
        "project":"Challenge Taranis Black — ONE G11 / Rota 4",
        "source_manifest":manifest,
        "summary": {
            "automated_checks":len(checks), "passed":len(checks)-fail_count,
            "failed":fail_count, "issues_for_review":len(issues),
            "dre_revenue_budget":str(dre_budget), "dre_revenue_actual":str(dre_actual),
            "products_revenue_budget":str(product_budget), "products_revenue_actual":str(product_actual),
            "ebitda_budget":str(ebitda_budget), "ebitda_actual":str(ebitda_actual),
            "ebitda_gap":str(ebitda_actual-ebitda_budget),
            "ebitda_variance_pct":str((ebitda_actual-ebitda_budget)/ebitda_budget*100),
            "net_profit_budget":str(net_budget), "net_profit_actual":str(net_actual),
            "net_profit_variance_pct":str((net_actual-net_budget)/net_budget*100),
            "bottleneck_count":len(bottlenecks),
        },
        "cross_sheet_reconciliation":gaps,
        "product_share_recalculation":share_discrepancies,
        "expense_overruns":expense_overruns,
        "checks":checks,
        "issues":issues,
        "bottlenecks":bottlenecks,
    }
    return data


def markdown_report(result: dict) -> str:
    s=result["summary"]
    gaps=result["cross_sheet_reconciliation"]
    costs=result["expense_overruns"]
    rows=[
        "# Auditoria financeira inicial — Taranis Black",
        "",
        "**Fonte:** `05_Financas_Orcado_vs_Realizado.xlsx` (Mock Data Kit da Alura).",
        "**Natureza:** cenário sintético. **Escopo:** quatro trimestres disponíveis; valores anuais em BRL.",
        "",
        "## Resumo executivo",
        "",
        f"- Receita bruta realizada (DRE): **{fmt_brl(s['dre_revenue_actual'])}**.",
        f"- EBITDA: **{fmt_brl(s['ebitda_actual'])}** frente a {fmt_brl(s['ebitda_budget'])} orçados ({pct(money(s['ebitda_variance_pct'])/100)}).",
        f"- Lucro líquido: **{fmt_brl(s['net_profit_actual'])}** frente a {fmt_brl(s['net_profit_budget'])} orçados ({pct(money(s['net_profit_variance_pct'])/100)}).",
        f"- Verificações automatizadas: **{s['passed']}/{s['automated_checks']}** aprovadas; **{s['failed']}** falhas de cálculos internos.",
        "",
        "## Conciliação de receitas — atenção prioritária",
        "",
        "| Referência | DRE | Linhas de produto | Diferença (DRE − produtos) |",
        "|---|---:|---:|---:|",
    ]
    for g in gaps:
        rows.append(f"| Receita {g['comparison']} | {fmt_brl(g['dre'])} | {fmt_brl(g['products'])} | **{fmt_brl(g['difference_dre_minus_products'])}** |")
    rows += [
        "",
        "A divergência **não é um prejuízo apurado**: pode refletir escopo, classificação ou inconsistência na base. A causa permanece não determinada.",
        "",
        "## Desvios desfavoráveis em despesas operacionais",
        "",
        "| Conta da DRE | Orçado | Realizado | Excesso |",
        "|---|---:|---:|---:|",
    ]
    for cost in costs:
        rows.append(f"| {cost['account']} | {fmt_brl(cost['budget_cost'])} | {fmt_brl(cost['actual_cost'])} | **{fmt_brl(cost['unfavorable_variance'])}** |")
    rows += ["", "Os valores acima são desvios contábeis, **não** economias já realizadas. Estimativas de impacto dos gargalos não devem ser somadas sem conciliação.",
             "", "## Participação por produto — conferência", "", "| Linha | Informado | Calculado com valores realizados | Divergência (p.p.) | Situação |", "|---|---:|---:|---:|---|"]
    for p in result["product_share_recalculation"]:
        rows.append(f"| {p['product']} | {p['declared_share_pct']}% | {p['calculated_share_pct']}% | {p['deviation_pp']} | {p['status']} |")
    rows += ["", "## Registro de qualidade de dados", ""]
    for issue in result["issues"]:
        rows.append(f"### {issue['id']} — {issue['title']}")
        rows.extend([f"**Risco:** {issue['severity']}  ", f"**Evidência:** {issue['evidence']}  ", f"**Tratamento proposto:** {issue['action']}", ""])
    rows += [
        "## Critérios de conclusão desta etapa", "",
        f"- {'[x]' if s['failed']==0 else '[ ]'} Totais anuais conciliados com os trimestres em cada linha da DRE.",
        f"- {'[x]' if s['failed']==0 else '[ ]'} Identidades contábeis anuais verificadas.",
        "- [ ] Divergências entre abas explicadas por fonte autorizada (pendência aberta).",
        "- [x] Hipóteses, estimativas e fatos identificados separadamente.",
        "",
        "## Próximo passo", "",
        "Construir o AI Canvas e a matriz Esforço × Impacto a partir dos gargalos confirmados, preservando a revisão humana para crédito e faturamento.",
        "",
    ]
    return "\n".join(rows)


def main() -> None:
    parser=argparse.ArgumentParser(description="Auditoria de finanças do Challenge Taranis Black")
    parser.add_argument("--data-dir",type=Path,default=PROJECT_ROOT/"data/derived")
    parser.add_argument("--output-dir",type=Path,default=PROJECT_ROOT/"reports")
    parser.add_argument("--source-xlsx",type=Path,default=None,help="Opcional: verifica SHA-256 do XLSX original sem modificá-lo")
    args=parser.parse_args()
    result=build_audit(args.data_dir)
    if args.source_xlsx:
        expected=result["source_manifest"]["original_sha256"]
        observed=hashlib.sha256(args.source_xlsx.read_bytes()).hexdigest()
        if observed!=expected:
            parser.error(f"SHA-256 da fonte não corresponde ao manifesto: esperado {expected}, obtido {observed}")
        print("SHA-256 da planilha de origem: CONFERIDO")
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/"audit_result.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    (args.output_dir/"auditoria_financeira_inicial.md").write_text(markdown_report(result),encoding="utf-8")
    s=result["summary"]
    print(f"Verificações internas: {s['passed']}/{s['automated_checks']} PASS; {s['failed']} FAIL")
    print(f"Receita realizada: DRE {fmt_brl(s['dre_revenue_actual'])}; produtos {fmt_brl(s['products_revenue_actual'])}")
    print(f"EBITDA: {fmt_brl(s['ebitda_actual'])} ({pct(money(s['ebitda_variance_pct'])/100)} vs. orçado)")
    print(f"Pendências interpretativas/documentais: {s['issues_for_review']}")
    print(f"Relatórios: {args.output_dir}")
    if s["failed"]:
        raise SystemExit(1)


if __name__=="__main__":
    main()
