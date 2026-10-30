import unittest
import sys
import tempfile
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
try:
    from ledger import validate, save_result, connect, export_csv
except ImportError:
    validate = save_result = connect = export_csv = None

SOURCE = {
    "message_id": "T01",
    "subject": "PO-1042 update",
    "body": "Harbor Packaging: PO-1042 was due 2026-11-02, now arriving 2026-11-06. Quantity 400.",
}
AI = {
    "purchase_order": "PO-1042",
    "supplier": "Harbor Packaging",
    "event_type": "delay",
    "promised_date": "2026-11-02",
    "revised_date": "2026-11-06",
    "quantity": 400,
    "summary": "Packaging arrives four days late.",
    "evidence_quote": "now arriving 2026-11-06",
    "confidence": 0.95,
}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(
            validate, "validation and database implementation required"
        )

    def test_valid_delay(self):
        r = validate(SOURCE, AI)
        self.assertEqual(r["route"], "exception")
        self.assertEqual(r["delay_days"], 4)
        self.assertEqual(r["priority"], "high")

    def test_po_substring_rejected(self):
        source = {
            **SOURCE,
            "subject": "PO-10420 update",
            "body": SOURCE["body"].replace("PO-1042", "PO-10420"),
        }
        self.assertIn("ungrounded_purchase_order", validate(source, AI)["issues"])

    def test_required_nullable_fields_present(self):
        ai = {
            k: v
            for k, v in AI.items()
            if k not in ["quantity", "promised_date", "revised_date"]
        }
        self.assertIn(
            "missing_fields",
            validate(SOURCE, {**ai, "event_type": "short_shipment"})["issues"],
        )

    def test_invalid_input_types(self):
        self.assertIn("invalid_input", validate({**SOURCE, "subject": 7}, AI)["issues"])

    def test_on_time(self):
        r = validate(
            SOURCE, {**AI, "event_type": "on_track", "revised_date": "2026-11-02"}
        )
        self.assertEqual(r["route"], "logged")

    def test_missing_date_review(self):
        self.assertIn(
            "missing_dates", validate(SOURCE, {**AI, "revised_date": None})["issues"]
        )

    def test_invalid_date(self):
        self.assertIn(
            "invalid_date",
            validate(SOURCE, {**AI, "revised_date": "2026-02-30"})["issues"],
        )

    def test_unknown_po(self):
        self.assertIn(
            "ungrounded_purchase_order",
            validate(SOURCE, {**AI, "purchase_order": "PO-9999"})["issues"],
        )

    def test_unsupported_evidence(self):
        self.assertIn(
            "ungrounded_quote",
            validate(SOURCE, {**AI, "evidence_quote": "bankruptcy"})["issues"],
        )

    def test_low_confidence(self):
        self.assertEqual(
            validate(SOURCE, {**AI, "confidence": 0.6})["route"], "manual_review"
        )

    def test_boolean_confidence(self):
        self.assertIn(
            "invalid_confidence", validate(SOURCE, {**AI, "confidence": True})["issues"]
        )

    def test_bad_quantity(self):
        self.assertIn(
            "invalid_quantity", validate(SOURCE, {**AI, "quantity": -4})["issues"]
        )

    def test_unknown_event(self):
        self.assertEqual(
            validate(SOURCE, {**AI, "event_type": "pay_supplier"})["route"],
            "manual_review",
        )

    def test_ambiguous(self):
        self.assertEqual(
            validate(SOURCE, {**AI, "event_type": "unclear"})["route"], "manual_review"
        )

    def test_reversed_delay(self):
        self.assertIn(
            "inconsistent_delay",
            validate(SOURCE, {**AI, "revised_date": "2026-11-01"})["issues"],
        )

    def test_missing_response(self):
        self.assertIn("invalid_ai_json", validate(SOURCE, "broken json")["issues"])

    def test_llm_error(self):
        self.assertIn(
            "llm_unavailable", validate(SOURCE, {"error": "timeout"})["issues"]
        )

    def test_empty_input(self):
        self.assertIn("invalid_input", validate({}, AI)["issues"])

    def test_overlong_input(self):
        self.assertIn(
            "invalid_input", validate({**SOURCE, "body": "x" * 20001}, AI)["issues"]
        )

    def test_invalid_summary(self):
        self.assertIn(
            "invalid_summary", validate(SOURCE, {**AI, "summary": ""})["issues"]
        )

    def test_duplicate_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            db = connect(pathlib.Path(d) / "test.db")
            r = validate(SOURCE, AI)
            self.assertTrue(save_result(db, SOURCE, AI, r)["created"])
            self.assertFalse(save_result(db, SOURCE, AI, r)["created"])
            self.assertEqual(
                db.execute("select count(*) from results").fetchone()[0], 1
            )

    def test_csv_formula_safety(self):
        with tempfile.TemporaryDirectory() as d:
            db = connect(pathlib.Path(d) / "test.db")
            s = {**SOURCE, "subject": '=HYPERLINK("bad")'}
            save_result(db, s, AI, validate(s, AI))
            self.assertIn("'=HYPERLINK", export_csv(db))


if __name__ == "__main__":
    unittest.main()
