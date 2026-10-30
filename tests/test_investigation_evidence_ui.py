"""Proteção de regressão contra truncamento da tabela de evidências DQ-001."""
from __future__ import annotations

import ast
import unittest
from pathlib import Path


class InvestigationEvidenceDisplayTests(unittest.TestCase):
    def test_evidence_sources_are_outside_dataframes(self) -> None:
        target = Path(__file__).resolve().parents[1] / "src" / "taranis_black" / "investigation_ui.py"
        source = target.read_text(encoding="utf-8")
        ast.parse(source, filename=str(target))
        self.assertIn("    with tabs[0]:", source)
        evidence = source.split("    with tabs[0]:", 1)[1].split("    with tabs[1]:", 1)[0]
        self.assertNotIn("st.dataframe(", evidence)
        self.assertIn("with st.container(border=True):", evidence)
        self.assertIn("st.write(source)", evidence)
        self.assertIn('case["sources"][0]', evidence)
        self.assertIn('case["sources"][1]', evidence)
        self.assertIn('"Cálculo determinístico"', evidence)


if __name__ == "__main__":
    unittest.main()
