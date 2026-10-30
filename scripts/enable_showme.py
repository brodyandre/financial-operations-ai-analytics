"""Adiciona a seção DQ-001 ao dashboard SEM substituir o arquivo do usuário.

Uso: python scripts/enable_showme.py
Interrompe se não reconhecer a estrutura existente; salva backup em /tmp.
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "dashboard" / "app.py"
NAV_OLD = '["Visão executiva", "Análise financeira", "Qualidade de dados", "Operações", "Cenários & ChatGPT"]'
NAV_NEW = '["Visão executiva", "Análise financeira", "Qualidade de dados", "Investigação DQ-001", "Operações", "Cenários & ChatGPT"]'
ROUTE_OLD = 'elif section == "Operações":\n    operations(data)\nelse:\n    scenarios(data, period)'
ROUTE_NEW = ('elif section == "Investigação DQ-001":\n'
             '    from taranis_black.investigation_ui import render_investigation\n'
             '    render_investigation(data)\n'
             + ROUTE_OLD)


def patch(content: str) -> str:
    already_nav = NAV_NEW in content
    already_route = 'elif section == "Investigação DQ-001":' in content
    if already_nav and already_route:
        return content
    if already_nav != already_route:
        raise ValueError("Patch parcial: preservar app.py e investigar manualmente.")
    if content.count(NAV_OLD) != 1 or content.count(ROUTE_OLD) != 1:
        raise ValueError("Layout do dashboard diferente do esperado: patch abortado sem alterações.")
    new = content.replace(NAV_OLD, NAV_NEW, 1).replace(ROUTE_OLD, ROUTE_NEW, 1)
    compile(new, "dashboard/app.py", "exec")
    return new


def main() -> None:
    before = APP.read_text(encoding="utf-8")
    after = patch(before)
    if before == after:
        print("OK: investigação DQ-001 já integrada; nenhuma alteração realizada.")
        return
    backup_dir = Path(tempfile.mkdtemp(prefix="taranis_showme_backup_"))
    shutil.copy2(APP, backup_dir / "app.py")
    APP.write_text(after, encoding="utf-8")
    print("OK: menu Investigação DQ-001 habilitado em dashboard/app.py")
    print(f"Backup anterior: {backup_dir / 'app.py'}")
    print("Não houve alteração nos dados, gráficos, fontes ou cálculos da aplicação.")


if __name__ == "__main__":
    main()
