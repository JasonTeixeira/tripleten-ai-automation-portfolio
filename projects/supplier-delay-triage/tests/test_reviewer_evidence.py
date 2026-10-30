"""Validate the new actual n8n runs without assuming deterministic LLM text."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "evidence/reviewer-fix"


def execution(name):
    text = (PROOF / name).read_text()
    return json.JSONDecoder().raw_decode(text[text.index("\n{") + 1 :])[0]


class ReviewerExecutionTests(unittest.TestCase):
    def test_normal_run_routes_every_item_to_its_validated_outcome(self):
        run = execution("normal-run.txt")
        self.assertEqual(run["status"], "success")
        data = run["data"]["resultData"]["runData"]
        ports = data["Route Delivery Outcomes"][0]["data"]["main"]
        self.assertEqual(sum(map(len, ports)), 6)
        self.assertEqual(len(ports[3]), 0)
        for index, route in enumerate(["exception", "logged", "manual_review"]):
            self.assertGreater(len(ports[index]), 0)
            self.assertTrue(
                all(item["json"]["route"] == route for item in ports[index])
            )
        receipts = data["Validate Route And Record"][0]["data"]["main"][0]
        self.assertTrue(all(item["json"]["created"] for item in receipts))

    def test_outage_reaches_native_manual_review_branch(self):
        run = execution("outage-run.txt")
        self.assertEqual(run["status"], "success")
        data = run["data"]["resultData"]["runData"]
        ports = data["Route Delivery Outcomes"][0]["data"]["main"]
        self.assertEqual(list(map(len, ports)), [0, 0, 1, 0])
        review = data["Manual Review"][0]["data"]["main"][0][0]["json"]
        self.assertIn("llm_unavailable", review["issues"])

    def test_duplicate_run_preserves_seven_rows_and_audits_six_skips(self):
        run = execution("duplicate-run.txt")
        self.assertEqual(run["status"], "success")
        receipts = run["data"]["resultData"]["runData"]["Validate Route And Record"][0][
            "data"
        ]["main"][0]
        self.assertEqual(len(receipts), 6)
        self.assertTrue(all(not item["json"]["created"] for item in receipts))
        rows = json.loads((PROOF / "stored-results.json").read_text())["results"]
        audit = json.loads((PROOF / "audit.json").read_text())["attempts"]
        self.assertEqual(len(rows), 7)
        self.assertEqual(len(audit), 13)
        self.assertEqual(sum(item["event"] == "duplicate_skipped" for item in audit), 6)

    def test_new_run_preserves_all_36_core_source_fields(self):
        expected = json.loads((ROOT / "samples/expected-extractions.json").read_text())
        rows = json.loads((PROOF / "normal-results.json").read_text())["results"]
        checked = 0
        for row in rows:
            ai = row["ai_json"]
            if isinstance(ai, str):
                ai = json.loads(ai)
            for field, value in expected[row["message_id"]].items():
                with self.subTest(message_id=row["message_id"], field=field):
                    self.assertEqual(ai[field], value)
                checked += 1
        self.assertEqual(checked, 36)


if __name__ == "__main__":
    unittest.main()
