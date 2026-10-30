"""Proteção estática contra regressão de texto truncado na tela de qualidade."""
from __future__ import annotations

import ast
import unittest
from pathlib import Path


class QualityExceptionsUIRegressionTests(unittest.TestCase):
    def test_full_issue_action_is_written_outside_dataframe(self) -> None:
        app = Path(__file__).resolve().parents[1] / "dashboard" / "app.py"
        module = ast.parse(app.read_text(encoding="utf-8"), filename=str(app))
        fn = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == "quality")
        loops = [n for n in ast.walk(fn) if isinstance(n, ast.For) and ast.unparse(n.iter) == "audit['issues']"]
        self.assertEqual(len(loops), 1, "Exceções devem ter exibição própria, fora da tabela")
        calls = [n for n in ast.walk(loops[0]) if isinstance(n, ast.Call)]
        self.assertTrue(any(ast.unparse(c.func) == "st.write" and c.args and ast.unparse(c.args[0]) == "issue['action']" for c in calls), "O texto integral de 'Próxima verificação' deve ser mostrado")
        self.assertTrue(any(ast.unparse(c.func) == "st.write" and c.args and ast.unparse(c.args[0]) == "issue['title']" for c in calls), "O texto integral de 'Problema' deve ser mostrado")


if __name__ == "__main__":
    unittest.main()
