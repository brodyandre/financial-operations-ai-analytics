"""Regressão da matriz, gates de dados e cenários econômicos hipotéticos."""
import copy
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.prioritization import (  # noqa: E402
    build_result, load_config, render_report, sensitivity_cases, validate_config,
    weighted_score,
)


class RouteZeroStageTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = load_config()
        cls.result = build_result(cls.cfg)
        cls.scores = {item["id"]: item for item in cls.result["scores"]}
        cls.scenarios = {
            x["orders_per_month_assumed"]: x
            for x in cls.result["roi_sensitivity"]["scenarios"]
        }

    def test_weights_are_normalized(self):
        validate_config(self.cfg)
        for name in ("impact", "effort"):
            self.assertEqual(sum(Decimal(str(x)) for x in self.cfg["criteria"][name].values()), Decimal(1))

    def test_reject_invalid_weights(self):
        bad = copy.deepcopy(self.cfg)
        bad["criteria"]["impact"]["financial_relevance"] = 0.45
        with self.assertRaises(AssertionError):
            validate_config(bad)

    def test_reject_invalid_score(self):
        bad = copy.deepcopy(self.cfg)
        bad["use_cases"][0]["impact"]["service_level"] = 7
        with self.assertRaises(AssertionError):
            validate_config(bad)

    def test_impact_weighted_formula(self):
        score = weighted_score(
            {"financial_relevance": 5, "service_level": 4, "cross_functional_reach": 4},
            self.cfg["criteria"]["impact"],
        )
        self.assertEqual(score, Decimal("4.40"))

    def test_c02_is_quick_win_in_demo_only(self):
        self.assertEqual(self.scores["C02"]["impact_score"], "4.40")
        self.assertEqual(self.scores["C02"]["effort_score"], "2.00")
        self.assertIn("MVP", self.scores["C02"]["quadrant"])
        self.assertEqual(self.result["scores"][0]["id"], "C02")

    def test_c01_is_conditional(self):
        self.assertEqual(self.scores["C01"]["impact_score"], "4.35")
        self.assertEqual(self.scores["C01"]["effort_score"], "3.35")
        self.assertEqual(self.scores["C01"]["data_gate"], "conditional")

    def test_c03_is_blocked(self):
        self.assertEqual(self.scores["C03"]["impact_score"], "3.75")
        self.assertEqual(self.scores["C03"]["effort_score"], "4.70")
        self.assertIn("BLOQUEADO", self.scores["C03"]["quadrant"])

    def test_scenario_100_orders(self):
        self.assertEqual(self.scenarios[100]["hours_released_per_month_assumed"], "16.67")
        self.assertEqual(self.scenarios[100]["illustrative_annual_capacity_value_brl"], "12000.00")
        self.assertEqual(self.scenarios[100]["illustrative_roi_percent_if_value_realized"], "-35.48")

    def test_scenario_200_orders(self):
        self.assertEqual(self.scenarios[200]["illustrative_roi_percent_if_value_realized"], "29.03")
        self.assertEqual(self.scenarios[200]["illustrative_net_balance_brl"], "5400.00")

    def test_scenario_400_orders(self):
        self.assertEqual(self.scenarios[400]["illustrative_roi_percent_if_value_realized"], "158.06")
        self.assertEqual(self.scenarios[400]["illustrative_annual_capacity_value_brl"], "48000.00")

    def test_break_even_is_illustrative(self):
        self.assertEqual(self.result["roi_sensitivity"]["breakeven_orders_per_month_if_value_realized"], "155.00")
        self.assertIn("hipótese", self.result["roi_sensitivity"]["scenario_kind"])

    def test_report_does_not_claim_realised_roi(self):
        text = render_report(self.result)
        self.assertIn("não são automaticamente economia financeira", text)
        self.assertIn("R$ 1,1 milhão", text)
        self.assertIn("diferença", text)


if __name__ == "__main__":
    unittest.main()
