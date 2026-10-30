import unittest
import threading
import tempfile
import os
import json
import urllib.request
import urllib.error
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ledger import Handler, ThreadingHTTPServer
from test_workflow import SOURCE, AI


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.old = os.environ.get("LEDGER_DB")
        os.environ["LEDGER_DB"] = cls.tmp.name + "/api.db"
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.url = "http://127.0.0.1:" + str(cls.server.server_port)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.tmp.cleanup()
        if cls.old is None:
            os.environ.pop("LEDGER_DB", None)
        else:
            os.environ["LEDGER_DB"] = cls.old

    def get(self, path):
        return urllib.request.urlopen(self.url + path)

    def post(self, path, data):
        request = urllib.request.Request(
            self.url + path,
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            return urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            return e

    def test_evidence_views(self):
        self.post(
            "/record",
            {"source": {**SOURCE, "message_id": "SUP-001"}, "ai": json.dumps(AI)},
        )
        for name in ["input", "output", "ai", "quality"]:
            self.assertEqual(self.get("/evidence/" + name).status, 200)
        self.assertEqual(len(json.load(self.get("/intake/failure"))["messages"]), 1)

    def test_health(self):
        self.assertEqual(json.load(self.get("/health"))["status"], "ok")

    def test_intake(self):
        self.assertEqual(len(json.load(self.get("/intake"))["messages"]), 6)

    def test_record_and_read(self):
        self.assertEqual(
            json.load(self.post("/record", {"source": SOURCE, "ai": AI}))["route"],
            "exception",
        )
        rows = json.load(self.get("/results"))["results"]
        self.assertIn(SOURCE["message_id"], [r["message_id"] for r in rows])
        self.assertIn("attempts", json.load(self.get("/audit")))
        self.assertIn("message_id", self.get("/results.csv").read().decode())

    def test_malformed_payload(self):
        self.assertEqual(self.post("/record", {}).code, 400)

    def test_invalid_input(self):
        self.assertEqual(self.post("/record", {"source": {}, "ai": {}}).code, 400)

    def test_large_payload(self):
        self.assertEqual(self.post("/record", {"body": "x" * 100001}).code, 413)

    def test_unknown_post(self):
        self.assertEqual(self.post("/wrong", {}).code, 404)

    def test_unknown_get(self):
        with self.assertRaises(urllib.error.HTTPError) as c:
            self.get("/wrong")
        self.assertEqual(c.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
