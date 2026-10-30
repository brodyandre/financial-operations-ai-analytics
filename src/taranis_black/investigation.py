"""Investigação consultiva DQ-001 sobre valores auditados do cenário sintético.

Nunca resolve automaticamente divergências, altera fontes ou aprova lançamentos.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any

from .dashboard import pt_brl, reconciliation

VALID_BASES = {"realizada", "orçada"}
VALID_ACTIONS = {
    "Solicitar evidências adicionais",
    "Encaminhar à Controladoria",
    "Manter pendente e monitorar",
}
VALID_AREAS = {"Controladoria", "Financeiro", "TI e Dados"}


def investigation_snapshot(data: dict[str, Any], base: str = "realizada") -> dict[str, Any]:
    """Evidências do DQ-001; valores calculados na auditoria existente."""
    if base not in VALID_BASES:
        raise ValueError("Base desconhecida; use realizada ou orçada.")
    comparison = reconciliation(data)[base]
    audit = data["audit"]
    issue = next((x for x in audit["issues"] if x["id"] == "DQ-001"), None)
    if issue is None:
        raise ValueError("Achado DQ-001 ausente da auditoria.")
    if comparison["dre"] - comparison["products"] != comparison["difference"]:
        raise ValueError("Diferença inconsistente; investigação bloqueada.")
    if audit["summary"]["failed"] != 0:
        raise ValueError("A auditoria da fonte possui falhas; investigação bloqueada.")
    manifest = audit["source_manifest"]
    return {
        "case_id": "DQ-001",
        "base": base,
        "dre_brl": comparison["dre"],
        "products_brl": comparison["products"],
        "difference_brl": comparison["difference"],
        "severity": issue["severity"],
        "title": issue["title"],
        "evidence_description": issue["evidence"],
        "recommended_action": issue["action"],
        "sources": [
            f"{manifest['original_file']} / DRE_Trimestral_Orcado_Real / TOTAL RECEITA BRUTA / anual {base}",
            f"{manifest['original_file']} / Receita_por_Linha_Produto / TOTAL / anual {base}",
        ],
        "source_sha256": manifest["original_sha256"],
        "status": "PENDENTE_DE_RECONCILIACAO",
        "cause_confirmed": False,
        "scope": "Dados sintéticos da Alura, sem conexão a ERP",
    }


def investigation_brief(snapshot: dict[str, Any]) -> str:
    """Briefing para copiar no ChatGPT, sem PII nem instrução de atuar no ERP."""
    if snapshot.get("case_id") != "DQ-001" or snapshot.get("cause_confirmed") is not False:
        raise ValueError("Briefing exige DQ-001 sem causa confirmada.")
    return "\n".join([
        "Atue como consultor de controladoria da Taranis Black (empresa SIMULADA).",
        "Considere apenas as evidências abaixo; não use dados externos nem invente causas.",
        "Nunca trate a diferença como perda, fraude ou receita recuperável.",
        "Não autorize alteração contábil, concessão de crédito ou integração ao ERP.",
        "Caso: DQ-001 — divergência entre duas visões de receita anual.",
        f"Base: {snapshot['base']}.",
        f"DRE: {pt_brl(snapshot['dre_brl'])}.",
        f"Receita por produto: {pt_brl(snapshot['products_brl'])}.",
        f"Diferença DRE − produtos: {pt_brl(snapshot['difference_brl'])}.",
        "Situação: PENDENTE DE CONCILIAÇÃO; CAUSA NÃO CONFIRMADA.",
        "Fontes informadas no Mock Data Kit:",
        *(f"- {source}" for source in snapshot["sources"]),
        f"SHA-256 do XLSX de origem: {snapshot['source_sha256']}.",
        "Hipóteses a INVESTIGAR (não são fatos): escopo/canais; período de competência; regras de classificação.",
        "Responda em português brasileiro, nas seções:",
        "1. Fatos observáveis e evidências (cite as abas de origem).",
        "2. Hipóteses não comprovadas e quais dados faltam para testá-las.",
        "3. Três verificações concretas, com prioridade e área responsável proposta.",
        "4. Riscos de uma decisão prematura e necessidade de aprovação humana.",
        "5. Limitações: dados sintéticos, sem causa confirmada, sem resultado financeiro realizado.",
        "Não afirme que o ChatGPT executou conciliação, alterou dados ou foi integrado ao dashboard.",
    ])


def review_record(snapshot: dict[str, Any], action: str, area: str, note: str = "") -> dict[str, Any]:
    """Registro para download *manual*; NÃO aprova a causa nem persiste no servidor."""
    if snapshot.get("case_id") != "DQ-001" or snapshot.get("cause_confirmed") is not False:
        raise ValueError("Registro só permitido para DQ-001 sem causa confirmada.")
    if action not in VALID_ACTIONS:
        raise ValueError("Ação deve ser uma das opções de acompanhamento disponíveis.")
    if area not in VALID_AREAS:
        raise ValueError("Área responsável inválida.")
    if len(note) > 500:
        raise ValueError("Nota superior a 500 caracteres.")
    return {
        "schema_version": "1.0",
        "case_id": "DQ-001",
        "base": snapshot["base"],
        "status": "PENDENTE_DE_RECONCILIACAO",
        "review_scope": "ENCAMINHAMENTO_DA_INVESTIGACAO",
        "action_requested": action,
        "area_proposed": area,
        "review_note": note.strip(),
        "source_sha256": snapshot["source_sha256"],
        "difference_brl": str(snapshot["difference_brl"]),
        "cause_confirmed": False,
        "accounting_adjustment_authorized": False,
        "real_world_deployment": False,
        "disclaimer": "Registro demonstrativo e local: não comprova decisão/aprovação real.",
    }
