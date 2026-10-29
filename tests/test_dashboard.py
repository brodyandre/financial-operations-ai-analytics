"""Regressão do dashboard: valores contábeis, hipóteses e qualidade dos dados.

Não requer Streamlit/Plotly para rodar na CI existente.
"""
import unittest
from decimal import Decimal
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.dashboard import (
    EBITDA, NET_INCOME, REVENUE, account_value, expense_overruns,
    load_data, pt_brl, prompt_for_chatgpt, quarterly_series,
    reconciliation, simulate_triage, summary_for_period,
)


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()

    def test_auditoria_preservada(self):
        s = self.data["audit"]["summary"]
        self.assertEqual((s["passed"], s["failed"]), (48, 0))
        self.assertEqual(s["issues_for_review"], 4)

    def test_receita_dre(self):
        m = summary_for_period(self.data)
        self.assertEqual(m["revenue"]["actual"], Decimal("48500000"))
        self.assertEqual(m["revenue"]["budget"], Decimal("48600000"))

    def test_ebitda_realizado(self):
        m = summary_for_period(self.data)
        self.assertEqual(m["ebitda"]["actual"], Decimal("5770000"))
        self.assertLess(m["ebitda"]["variance_pct"], 0)

    def test_lucro_liquido(self):
        self.assertEqual(summary_for_period(self.data)["net_income"]["actual"], Decimal("3108600"))

    def test_quarters_sum_to_annual(self):
        for account in (REVENUE, EBITDA, NET_INCOME):
            q = quarterly_series(self.data, account)
            self.assertEqual(sum((r["actual"] for r in q), Decimal(0)), account_value(self.data, account, "annual", "actual"))
            self.assertEqual(sum((r["budget"] for r in q), Decimal(0)), account_value(self.data, account, "annual", "budget"))

    def test_reconciliation_remains_open(self):
        r = reconciliation(self.data)
        self.assertEqual(r["realizada"]["difference"], Decimal("1100000"))
        self.assertEqual(r["orçada"]["difference"], Decimal("600000"))

    def test_expense_overruns_are_not_savings(self):
        costs = expense_overruns(self.data)
        self.assertEqual([x["overrun"] for x in costs], [Decimal("1360000"), Decimal("515000"), Decimal("670000")])

    def test_simulation_200_orders_illustrative_roi(self):
        r = simulate_triage()
        self.assertEqual(r["hours_released_per_month"], Decimal("100") / 3)
        self.assertEqual(r["capacity_value_brl"], Decimal("24000"))
        self.assertEqual(r["cost_brl"], Decimal("18600"))
        self.assertAlmostEqual(float(r["roi_pct_if_monetized"]), 29.0322580645)
        self.assertIn("HIPÓTESE", r["label"])

    def test_simulation_zero_cost_undefined_roi(self):
        self.assertIsNone(simulate_triage(0, 0, 0, 0, 0)["roi_pct_if_monetized"])

    def test_simulation_rejects_invalid_inputs(self):
        cases = [dict(monthly_orders=-1), dict(monthly_orders=1.5), dict(reduction_pct=101), dict(reduction_pct=-1), dict(hourly_cost=-2), dict(upfront_cost=-3)]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    simulate_triage(**kwargs)

    def test_display_brazilian_format(self):
        self.assertEqual(pt_brl(Decimal("48500000"), compact=True), "R$ 48,50 mi")
        self.assertEqual(pt_brl(Decimal("-1500.20")), "R$ -1.500,20")

    def test_prompt_avoids_false_claims(self):
        text = prompt_for_chatgpt(self.data)
        self.assertIn("SEM CAUSA CONFIRMADA", text)
        self.assertIn("Não invente", text)
        self.assertIn("determinística", text)
        self.assertIn("quatro achados", text)


if __name__ == "__main__":
    unittest.main()
