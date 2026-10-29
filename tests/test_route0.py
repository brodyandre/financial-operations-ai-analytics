"""Testes independentes da documentação incremental da Rota 0."""
import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROTA = ROOT / "docs" / "rota0"


class RouteZeroTests(unittest.TestCase):
    def test_three_use_cases(self):
        with (ROTA / "02_REGISTRO_OPORTUNIDADES.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual({x["id"] for x in rows}, {"C01", "C02", "C03"})

    def test_human_oversight_for_all_use_cases(self):
        with (ROTA / "02_REGISTRO_OPORTUNIDADES.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(all(x["supervisao_humana"].strip() for x in rows))

    def test_no_unsubstantiated_predictive_claim(self):
        text = (ROTA / "01_AI_CANVAS_TARANIS_BLACK.md").read_text(encoding="utf-8")
        self.assertIn("não sustenta treinamento", text)
        self.assertIn("não implementado", text)


if __name__ == "__main__":
    unittest.main()
