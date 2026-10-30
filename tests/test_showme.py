"""Regressão da investigação e do experimento Show Me Project."""
from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from taranis_black.dashboard import load_data
from taranis_black.dq_experiment import detects_gap, run_experiment
from taranis_black.investigation import investigation_brief, investigation_snapshot, review_record


class ShowMeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()

    def test_realized_gap_from_source(self):
        s = investigation_snapshot(self.data)
        self.assertEqual(s["dre_brl"], Decimal("48500000"))
        self.assertEqual(s["products_brl"], Decimal("47400000"))
        self.assertEqual(s["difference_brl"], Decimal("1100000"))

    def test_budget_gap_from_source(self):
        self.assertEqual(investigation_snapshot(self.data, "orçada")["difference_brl"], Decimal("600000"))

    def test_source_evidence(self):
        s = investigation_snapshot(self.data)
        self.assertEqual(len(s["source_sha256"]), 64)
        self.assertIn("DRE_Trimestral", s["sources"][0])
        self.assertIn("Receita_por_Linha", s["sources"][1])
        self.assertFalse(s["cause_confirmed"])

    def test_unknown_base_rejected(self):
        with self.assertRaises(ValueError):
            investigation_snapshot(self.data, "semanal")

    def test_detects_inconsistent_snapshot(self):
        data = dict(self.data)
        audit = dict(data["audit"])
        audit["cross_sheet_reconciliation"] = [dict(x) for x in audit["cross_sheet_reconciliation"]]
        audit["cross_sheet_reconciliation"][1]["difference_dre_minus_products"] = "0"
        data["audit"] = audit
        with self.assertRaises(ValueError):
            investigation_snapshot(data)

    def test_prompt_is_explicitly_investigative(self):
        p = investigation_brief(investigation_snapshot(self.data))
        self.assertIn("CAUSA NÃO CONFIRMADA", p)
        self.assertIn("Hipóteses a INVESTIGAR", p)
        self.assertIn("ChatGPT", p)
        self.assertIn("48.500.000,00", p)
        self.assertIn("47.400.000,00", p)
        self.assertIn("1.100.000,00", p)

    def test_rejects_false_claim_of_confirmed_cause(self):
        s = investigation_snapshot(self.data)
        s["cause_confirmed"] = True
        with self.assertRaises(ValueError):
            investigation_brief(s)

    def test_human_review_remains_pending(self):
        record = review_record(investigation_snapshot(self.data), "Solicitar evidências adicionais", "Controladoria", "Verificar escopo")
        self.assertEqual(record["status"], "PENDENTE_DE_RECONCILIACAO")
        self.assertFalse(record["cause_confirmed"])
        self.assertFalse(record["accounting_adjustment_authorized"])
        self.assertFalse(record["real_world_deployment"])
        self.assertEqual(record["review_note"], "Verificar escopo")

    def test_rejects_unsafe_decisions_and_areas(self):
        s = investigation_snapshot(self.data)
        with self.assertRaises(ValueError):
            review_record(s, "Aprovar lançamento", "Controladoria")
        with self.assertRaises(ValueError):
            review_record(s, "Solicitar evidências adicionais", "ERP")

    def test_limits_review_notes(self):
        with self.assertRaises(ValueError):
            review_record(investigation_snapshot(self.data), "Solicitar evidências adicionais", "Controladoria", "a" * 501)

    def test_20_labeled_synthetic_cases(self):
        r = run_experiment()
        self.assertEqual(r["case_count"], 20)
        self.assertEqual(r["true_positives"], 12)
        self.assertEqual(r["true_negatives"], 8)
        self.assertEqual((r["false_positives"], r["false_negatives"]), (0, 0))

    def test_threshold_boundary(self):
        base = Decimal("48500000.00")
        self.assertFalse(detects_gap(base, base - Decimal("0.01")))
        self.assertTrue(detects_gap(base, base - Decimal("0.02")))
        self.assertTrue(detects_gap(base, base + Decimal("0.02")))

    def test_invalid_numeric_values_rejected(self):
        with self.assertRaises(ValueError):
            detects_gap(Decimal("NaN"), Decimal(1))
        with self.assertRaises(ValueError):
            detects_gap(Decimal(2), Decimal(1), Decimal("-0.01"))

    def test_experiment_does_not_claim_external_accuracy(self):
        r = run_experiment()
        self.assertIn("não demonstra precisão em produção", r["limit"])
        self.assertIn("sintético", r["data_scope"])


if __name__ == "__main__":
    unittest.main()
