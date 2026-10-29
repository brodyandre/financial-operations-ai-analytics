"""Testes de contrato da proposta de governança; não constituem auditoria jurídica."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.governance import (  # noqa: E402
    build_result, load_config, render_report, risk_level, validate_config,
)


class RouteZeroStageThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = load_config()

    def test_draft_only_and_synthetic_scope(self):
        validate_config(self.cfg)
        self.assertFalse(self.cfg["approved_for_production"])
        self.assertEqual(self.cfg["data_scope"], "synthetic_mock_data_only")

    def test_tampered_approved_flag_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["approved_for_production"] = True
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_real_data_scope_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["data_scope"] = "real_customer_data"
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_duplicate_control_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["controls"][1]["id"] = bad["controls"][0]["id"]
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_missing_legal_basis_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["controls"] = [x for x in bad["controls"] if x["theme"] != "lawful_basis"]
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_case_id_not_authorized_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["risks"][0]["cases"] = ["C04"]
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_probability_out_of_bounds_rejected(self):
        bad = copy.deepcopy(self.cfg)
        bad["risks"][0]["probability"] = 7
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_human_review_cannot_be_disabled(self):
        bad = copy.deepcopy(self.cfg)
        bad["controls"][0]["review_required"] = False
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_blocked_predictive_case_required(self):
        bad = copy.deepcopy(self.cfg)
        for item in bad["risks"]:
            if "C03" in item["cases"]:
                item["decision_gate"] = "Coleta de dados sem bloqueio formal"
        with self.assertRaises(ValueError):
            validate_config(bad)

    def test_risk_scale_boundaries(self):
        self.assertEqual(risk_level(5), "baixo")
        self.assertEqual(risk_level(6), "moderado")
        self.assertEqual(risk_level(12), "alto")
        self.assertEqual(risk_level(20), "crítico")
        with self.assertRaises(ValueError):
            risk_level(26)

    def test_risk_result_ranks_critical_first(self):
        result = build_result(self.cfg)
        self.assertEqual(result["controls_defined"], 12)
        self.assertEqual(result["risk_items"], 8)
        self.assertEqual(result["risk_register"][0]["id"], "R-05")
        self.assertEqual(result["risk_register"][0]["score"], 20)

    def test_report_is_explicit_about_non_deployment(self):
        report = render_report(build_result(self.cfg))
        self.assertIn("PROPOSTA NÃO APROVADA", report)
        self.assertIn("não representa", report)
        self.assertIn("C03 bloqueado", report)


if __name__ == "__main__":
    unittest.main()
