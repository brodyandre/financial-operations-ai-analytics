"""Testes de regressão com dados sintéticos oficiais derivados."""
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.audit import build_audit, fmt_brl  # noqa: E402


class FinancialAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=build_audit(ROOT/"data/derived")

    def test_quarter_totals_and_accounting_identities(self):
        self.assertEqual(self.result["summary"]["failed"],0)
        self.assertGreaterEqual(self.result["summary"]["automated_checks"],45)

    def test_dre_and_product_reconciliation(self):
        gaps=self.result["cross_sheet_reconciliation"]
        self.assertEqual(Decimal(gaps[0]["difference_dre_minus_products"]),Decimal(600000))
        self.assertEqual(Decimal(gaps[1]["difference_dre_minus_products"]),Decimal(1100000))

    def test_ebitda_and_net_profit(self):
        s=self.result["summary"]
        self.assertEqual(Decimal(s["ebitda_actual"]),Decimal(5770000))
        self.assertEqual(Decimal(s["ebitda_gap"]),Decimal(-4078000))
        self.assertEqual(Decimal(s["net_profit_actual"]),Decimal(3108600))

    def test_cost_overruns(self):
        overruns={r["account"]:Decimal(r["unfavorable_variance"]) for r in self.result["expense_overruns"]}
        self.assertEqual(overruns["Despesas com Fretes e Logística de Entrega CD"],Decimal(1360000))
        self.assertEqual(overruns["Reentregas e Multas por Divergência de Pedido"],Decimal(515000))
        self.assertEqual(overruns["Provisão para Devedores Duvidosos (Inadimplência B2B)"],Decimal(670000))

    def test_product_share_discrepancy_flagged(self):
        flags=self.result["product_share_recalculation"]
        self.assertTrue(any(x["status"]=="REVIEW" for x in flags))

    def test_currency_pt_br(self):
        self.assertEqual(fmt_brl(1100000),"R$ 1.100.000,00")


if __name__=="__main__":
    unittest.main()
