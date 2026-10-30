"""Verify captured end-to-end runs; never fabricate model output."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CapturedEvidenceTests(unittest.TestCase):
    def load_execution(self, name):
        text = (ROOT / "evidence" / name).read_text()
        pos = text.index("\n{") + 1
        return json.JSONDecoder().raw_decode(text[pos:])[0]

    def test_three_real_n8n_runs_completed(self):
        for name in [
            "final-batch-run.txt",
            "final-outage-run.txt",
            "final-duplicate-run.txt",
        ]:
            with self.subTest(name=name):
                r = self.load_execution(name)
                self.assertEqual(r["status"], "success")
                self.assertTrue(r["finished"])

    def test_captured_routes_match_expected(self):
        expected = {
            "SUP-001": ("exception", 4),
            "SUP-002": ("logged", 0),
            "SUP-003": ("exception", None),
            "SUP-004": ("manual_review", None),
            "SUP-005": ("manual_review", -2),
            "SUP-006": ("exception", 1),
            "FAILURE-001": ("manual_review", None),
        }
        records = json.loads((ROOT / "evidence/live-results.json").read_text())[
            "results"
        ]
        self.assertEqual(len(records), 7)
        for r in records:
            self.assertEqual((r["route"], r["delay_days"]), expected[r["message_id"]])
        fail = next(r for r in records if r["message_id"] == "FAILURE-001")
        self.assertIn("llm_unavailable", fail["issues"])

    def test_duplicate_replay_audited(self):
        audit = json.loads((ROOT / "evidence/final-audit.json").read_text())["attempts"]
        self.assertEqual(len(audit), 13)
        self.assertEqual(sum(a["event"] == "duplicate_skipped" for a in audit), 6)


if __name__ == "__main__":
    unittest.main()
