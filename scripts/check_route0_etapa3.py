#!/usr/bin/env python3
"""Valida entregáveis da Rota 0 Etapa 3, sem dependências externas."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.governance import build_result, load_config, main, validate_config  # noqa: E402


def run() -> int:
    cfg = load_config()
    validate_config(cfg)
    main()
    result = build_result(cfg)
    docs = ROOT / "docs" / "rota0"
    content = {p: (docs / p).read_text(encoding="utf-8") for p in (
        "10_POLITICA_USO_IA_LGPD.md", "11_RISCOS_CONTROLES_VIES.md",
        "12_COMITE_AUDITORIA_RACI.md", "13_RESUMO_EXECUTIVO_ETAPA3.md",
        "14_COMO_VALIDAR_ETAPA3.md",
    )}
    policy = content["10_POLITICA_USO_IA_LGPD.md"]
    risks = content["11_RISCOS_CONTROLES_VIES.md"]
    committee = content["12_COMITE_AUDITORIA_RACI.md"]
    summary = content["13_RESUMO_EXECUTIVO_ETAPA3.md"]
    checks = [
        ("Proposta permanece não aprovada", result["status"] == "PROPOSTA_NAO_APROVADA"),
        ("Dados apenas sintéticos", result["synthetic_data_only"]),
        ("12 controles definidos", result["controls_defined"] == 12),
        ("8 riscos com donos e gates", result["risk_items"] == 8),
        ("Política permite e proíbe usos", "Uso permitido" in policy and "Uso proibido" in policy),
        ("LGPD e hipótese legal registradas", "hipótese legal" in policy and "LGPD" in policy),
        ("Revisão humana e alçadas", "revisão humana" in policy.lower() and "alçadas" in policy.lower()),
        ("Critérios de notificação e ANPD", "três dias úteis" in policy and "ANPD" in policy),
        ("Retenção e tratamento de incidentes", "retenção" in policy.lower() and "incidentes" in policy.lower()),
        ("Mitigação de vieses documentada", "mitigar vieses" in risks.lower()),
        ("Predição C03 bloqueada", "C03 bloqueado" in risks and "C03" in policy),
        ("Comitê proposto e RACI", "RACI" in committee and "proposto" in committee),
        ("Resumo executivo sem alegar implantação", "não representam governança implantada" in summary),
        ("Relatórios de auditoria gerados", (ROOT / "reports" / "rota0_etapa3_result.json").is_file() and (ROOT / "reports" / "rota0_etapa3_resumo.md").is_file()),
    ]
    nfailed = 0
    for title, ok in checks:
        print(("PASS" if ok else "FAIL") + ": " + title)
        nfailed += not ok
    print(f"Rota 0 Etapa 3: {len(checks)-nfailed}/{len(checks)} PASS")
    return 1 if nfailed else 0


if __name__ == "__main__":
    raise SystemExit(run())
