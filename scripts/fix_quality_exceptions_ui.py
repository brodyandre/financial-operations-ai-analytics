"""Correção localizada: exibir textos integrais de achados em Qualidade de dados.

Não altera dados, cálculos, nem a seção Investigação DQ-001.
Executar da raiz do repositório: python scripts/fix_quality_exceptions_ui.py
"""
from __future__ import annotations

import ast
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "dashboard" / "app.py"

OLD = '''    st.markdown("**Registro de exceções para análise humana**")
    st.dataframe(pd.DataFrame([{"ID": r["id"], "Prioridade": r["severity"], "Problema": r["title"], "Próxima verificação": r["action"]} for r in audit["issues"]]), hide_index=True, width="stretch")
'''
NEW = '''    st.markdown("**Registro de exceções para análise humana**")
    st.caption("Achados completos, sem corte de texto ou rolagem horizontal.")
    priority_labels = {"high": "Alta", "medium": "Média", "low": "Baixa"}
    for issue in audit["issues"]:
        with st.container(border=True):
            priority = priority_labels.get(str(issue["severity"]).lower(), str(issue["severity"]))
            st.caption(f"{issue['id']} · Prioridade: {priority}")
            st.markdown("**Problema**")
            st.write(issue["title"])
            st.markdown("**Próxima verificação**")
            st.write(issue["action"])
'''


def main() -> None:
    if not APP.is_file():
        raise SystemExit(f"BLOQUEADO: arquivo não encontrado: {APP}")
    current = APP.read_text(encoding="utf-8")
    if NEW in current and OLD not in current:
        print("OK: correção já está aplicada; nenhuma alteração necessária.")
        return
    if current.count(OLD) != 1:
        raise SystemExit("BLOQUEADO: trecho esperado da tabela não foi encontrado exatamente uma vez. Nenhum arquivo alterado.")
    modified = current.replace(OLD, NEW, 1)
    try:
        ast.parse(modified, filename=str(APP))
    except SyntaxError as exc:
        raise SystemExit(f"BLOQUEADO: a alteração não compila: {exc}") from exc
    backup_dir = Path(tempfile.mkdtemp(prefix="taranis_quality_ui_backup_"))
    backup_path = backup_dir / "app.py"
    shutil.copy2(APP, backup_path)
    APP.write_text(modified, encoding="utf-8")
    print("OK: Qualidade de dados agora exibe cada exceção em cartão com texto integral.")
    print(f"Backup preservado: {backup_path}")
    print("As fontes, as auditorias, os gráficos e a Investigação DQ-001 não foram modificados.")


if __name__ == "__main__":
    main()
