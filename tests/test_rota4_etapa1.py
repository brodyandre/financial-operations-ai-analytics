"""Teste de consistência documental, proveniência e limites de uso da Rota 4."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.lean import (  # noqa: E402
    build_result, load_config, read_gaps_csv, render_report, validate_config,
)


class LeanRoute4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = load_config()
        cls.gaps = read_gaps_csv()

    def test_valid_baseline(self):
        validate_config(self.cfg, self.gaps)

    def test_as_is_has_five_consecutive_steps(self):
        result = build_result(self.cfg, self.gaps)
        self.assertEqual(result["as_is_steps"], 5)
        self.assertEqual([row["id"] for row in self.cfg["process_stages"]], ["P01", "P02", "P03", "P04", "P05"])

    def test_missing_step_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["process_stages"].pop()
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_duplicate_step_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["process_stages"][1]["id"] = "P01"
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_sipoc_five_complete_rows(self):
        self.assertEqual(build_result(self.cfg, self.gaps)["sipoc_rows"], 5)

    def test_missing_sipoc_cell_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["sipoc"][0]["output"] = ""
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_ishikawa_six_m(self):
        result = build_result(self.cfg, self.gaps)
        self.assertEqual(len(result["ishikawa_groups"]), 6)
        self.assertEqual(result["ishikawa_causes"], 18)

    def test_missing_m_rejected(self):
        bad = copy.deepcopy(self.cfg)
        del bad["ishikawa"]["Maquina"]
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_baseline_csv_matches_config(self):
        self.assertEqual(len(build_result(self.cfg, self.gaps)["baseline_metrics"]), 5)

    def test_tampered_baseline_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["kpi_source_expectations"][1]["actual"] = "4 horas"
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_unproven_erp_integration_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["guardrails"]["erp_integration_claimed"] = True
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_autonomous_credit_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["guardrails"]["automatic_credit_approval"] = True
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_unproven_savings_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["guardrails"]["financial_benefit_realized_claimed"] = True
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_unsafe_real_data_scope_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["data_scope"] = "real_customers"
        with self.assertRaises(ValueError):
            validate_config(bad, self.gaps)

    def test_report_marks_non_implementation_and_differences(self):
        txt = render_report(build_result(self.cfg, self.gaps))
        self.assertIn("NÃO IMPLANTADA", txt)
        self.assertIn("R$ 1,1 mi", txt)
        self.assertIn("R$ 960 mil", txt)
        self.assertIn("R$ 1,36 mi", txt)


if __name__ == "__main__":
    unittest.main()
