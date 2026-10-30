"""Correção localizada da apresentação de fontes DQ-001; mantém motor e dados."""
from __future__ import annotations

import ast
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "taranis_black" / "investigation_ui.py"

OLD = '''        st.dataframe(pd.DataFrame([
            {"Referência": "DRE", "Valor anual": pt_brl(case["dre_brl"]), "Fonte": case["sources"][0]},
            {"Referência": "Produtos", "Valor anual": pt_brl(case["products_brl"]), "Fonte": case["sources"][1]},
            {"Referência": "Diferença (DRE − produtos)", "Valor anual": pt_brl(case["difference_brl"]), "Fonte": "Cálculo determinístico"},
        ]), hide_index=True, width="stretch")'''
NEW = '''        st.caption("Fontes exibidas por extenso, sem rolagem horizontal.")
        evidence_rows = (
            ("DRE", case["dre_brl"], case["sources"][0]),
            ("Produtos", case["products_brl"], case["sources"][1]),
            ("Diferença (DRE − produtos)", case["difference_brl"], "Cálculo determinístico"),
        )
        for reference, value, source in evidence_rows:
            with st.container(border=True):
                st.markdown(f"**{reference}** · **{pt_brl(value)}**")
                st.markdown("**Fonte documental**")
                st.write(source)'''


def main() -> None:
    if not TARGET.is_file():
        raise SystemExit(f"BLOQUEADO: arquivo de interface ausente: {TARGET}")
    current = TARGET.read_text(encoding="utf-8")
    if NEW in current and OLD not in current:
        print("OK: fontes completas já habilitadas; nenhuma alteração necessária.")
        return
    if current.count(OLD) != 1:
        raise SystemExit("BLOQUEADO: trecho original não encontrado exatamente uma vez. Nenhum arquivo alterado.")
    updated = current.replace(OLD, NEW, 1)
    try:
        ast.parse(updated, filename=str(TARGET))
    except SyntaxError as exc:
        raise SystemExit(f"BLOQUEADO: nova interface não compila: {exc}") from exc
    backup_dir = Path(tempfile.mkdtemp(prefix="taranis_dq001_evidence_ui_backup_"))
    backup_file = backup_dir / "investigation_ui.py"
    shutil.copy2(TARGET, backup_file)
    TARGET.write_text(updated, encoding="utf-8")
    print("OK: evidências DQ-001 usam cartões com fontes completas.")
    print(f"Backup preservado: {backup_file}")
    print("Motor de auditoria e dados financeiros não foram alterados.")


if __name__ == "__main__":
    main()
