"""Supplier exception validation, durable audit log and local intake API."""

import csv
import io
import json
import os
import re
import sqlite3
from datetime import date, datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(source, raw):
    issues = []
    ai = raw
    if not isinstance(source, dict):
        source = {}
    if not all(
        isinstance(source.get(k), str) and 0 < len(source[k]) <= limit
        for k, limit in [("message_id", 100), ("subject", 500), ("body", 20000)]
    ):
        issues.append("invalid_input")
    if issues:
        return {
            "route": "manual_review",
            "priority": "review",
            "delay_days": None,
            "issues": issues,
            "ai": {},
        }
    if isinstance(ai, str):
        try:
            ai = json.loads(ai)
        except (ValueError, TypeError):
            ai = {}
            issues.append("invalid_ai_json")
    if not isinstance(ai, dict):
        ai = {}
        issues.append("invalid_ai_json")
    if "error" in ai:
        issues.append("llm_unavailable")
    required = {
        "purchase_order",
        "supplier",
        "event_type",
        "promised_date",
        "revised_date",
        "quantity",
        "summary",
        "evidence_quote",
        "confidence",
    }
    if not required.issubset(ai):
        issues.append("missing_fields")
    text = source.get("subject", "") + "\n" + source.get("body", "")
    po = ai.get("purchase_order")
    quote = ai.get("evidence_quote")
    event = ai.get("event_type")
    if (
        not isinstance(po, str)
        or not re.fullmatch(r"PO-\d{4,8}", po)
        or po not in re.findall(r"(?<![\w-])PO-\d{4,8}(?![\w-])", text)
    ):
        issues.append("ungrounded_purchase_order")
    if not isinstance(quote, str) or len(quote) < 8 or quote not in text:
        issues.append("ungrounded_quote")
    if not isinstance(ai.get("supplier"), str) or not 1 <= len(ai["supplier"]) <= 150:
        issues.append("invalid_supplier")
    elif ai["supplier"] not in text:
        issues.append("ungrounded_supplier")
    if event not in ["delay", "on_track", "short_shipment", "unclear"]:
        issues.append("invalid_event_type")
    if event == "unclear":
        issues.append("ambiguous_message")
    c = ai.get("confidence")
    if type(c) not in [int, float] or not 0 <= c <= 1:
        issues.append("invalid_confidence")
    elif c < 0.85:
        issues.append("low_confidence")
    q = ai.get("quantity")
    if q is not None and (type(q) is not int or not 0 <= q <= 10000000):
        issues.append("invalid_quantity")
    if not isinstance(ai.get("summary"), str) or not 1 <= len(ai["summary"]) <= 500:
        issues.append("invalid_summary")
    dates = {}
    for key in ["promised_date", "revised_date"]:
        val = ai.get(key)
        if val is not None:
            try:
                if not isinstance(val, str) or not re.fullmatch(
                    r"\d{4}-\d{2}-\d{2}", val
                ):
                    raise ValueError()
                dates[key] = date.fromisoformat(val)
                if val not in text:
                    issues.append("ungrounded_date")
            except ValueError:
                issues.append("invalid_date")
    delay = None
    if event in ["delay", "on_track"]:
        if len(dates) != 2:
            issues.append("missing_dates")
        else:
            delay = (dates["revised_date"] - dates["promised_date"]).days
            if event == "delay" and delay <= 0:
                issues.append("inconsistent_delay")
            if event == "on_track" and delay > 0:
                issues.append("inconsistent_on_track")
    route = (
        "manual_review"
        if issues
        else "exception"
        if event in ["delay", "short_shipment"]
        else "logged"
    )
    return {
        "route": route,
        "priority": "review"
        if issues
        else "high"
        if delay is not None and delay >= 3
        else "normal",
        "delay_days": delay,
        "issues": sorted(set(issues)),
        "ai": ai,
    }


def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute(
        "CREATE TABLE IF NOT EXISTS results (message_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, subject TEXT NOT NULL, route TEXT NOT NULL, priority TEXT NOT NULL, delay_days INTEGER, issues TEXT NOT NULL, source_json TEXT NOT NULL, ai_json TEXT NOT NULL)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY, message_id TEXT, created_at TEXT, event TEXT)"
    )
    db.commit()
    return db


def save_result(db, source, raw, result):
    mid = source["message_id"]
    now = datetime.now(timezone.utc).isoformat()
    with db:
        cur = db.execute(
            "INSERT OR IGNORE INTO results VALUES (?,?,?,?,?,?,?,?,?)",
            (
                mid,
                now,
                source["subject"],
                result["route"],
                result["priority"],
                result["delay_days"],
                json.dumps(result["issues"]),
                json.dumps(source),
                json.dumps(raw),
            ),
        )
        created = cur.rowcount == 1
        db.execute(
            "INSERT INTO attempts(message_id,created_at,event) VALUES (?,?,?)",
            (mid, now, "created" if created else "duplicate_skipped"),
        )
    existing = dict(
        db.execute(
            "SELECT message_id,route,priority,delay_days,issues FROM results WHERE message_id=?",
            (mid,),
        ).fetchone()
    )
    existing["issues"] = json.loads(existing["issues"])
    return {**existing, "created": created}


def export_csv(db):
    output = io.StringIO()
    writer = csv.writer(output)
    extracted = [
        "purchase_order",
        "supplier",
        "event_type",
        "promised_date",
        "revised_date",
        "quantity",
        "confidence",
        "summary",
        "evidence_quote",
    ]
    base = ["message_id", "subject", "route", "priority", "delay_days", "issues"]
    writer.writerow(base + extracted)
    for row in db.execute("SELECT * FROM results ORDER BY message_id"):
        ai = json.loads(row["ai_json"])
        if isinstance(ai, str):
            try:
                ai = json.loads(ai)
            except ValueError:
                ai = {}
        if not isinstance(ai, dict):
            ai = {}
        values = [row[k] for k in base] + [ai.get(k) for k in extracted]
        writer.writerow(
            [
                "'" + v
                if isinstance(v, str) and v.lstrip().startswith(("=", "+", "-", "@"))
                else v
                for v in values
            ]
        )
    return output.getvalue()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send(self, status, data, ctype="application/json"):
        body = (
            json.dumps(data, indent=2) if ctype == "application/json" else data
        ).encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self.send(200, {"status": "ok", "project": "Supplier Delay Triage"})
        if self.path == "/intake/failure":
            messages = json.loads((ROOT / "samples/messages.json").read_text())
            messages[0]["message_id"] = "FAILURE-001"
            return self.send(200, {"messages": [messages[0]]})
        if self.path == "/intake":
            return self.send(
                200,
                {"messages": json.loads((ROOT / "samples/messages.json").read_text())},
            )
        db = connect(os.environ.get("LEDGER_DB", str(ROOT / "evidence/ledger.sqlite")))
        try:
            if self.path.startswith("/evidence/"):
                rows = [
                    dict(r)
                    for r in db.execute("SELECT * FROM results ORDER BY message_id")
                ]
                kind = self.path.split("/")[-1]
                if kind == "input":
                    return self.send(
                        200, json.loads((ROOT / "samples/messages.json").read_text())[0]
                    )
                if kind == "output":
                    return self.send(
                        200,
                        {
                            "results": [
                                {
                                    k: r[k]
                                    for k in [
                                        "message_id",
                                        "route",
                                        "priority",
                                        "delay_days",
                                    ]
                                }
                                for r in rows
                            ]
                        },
                    )
                if kind == "ai":
                    return self.send(
                        200,
                        {
                            "message_id": r["message_id"],
                            "ai_result": json.loads(json.loads(r["ai_json"])),
                        }
                        if (
                            r := next(
                                (r for r in rows if r["message_id"] == "SUP-001"), None
                            )
                        )
                        else {"status": "pending"},
                    )
                if kind == "quality":
                    return self.send(
                        200,
                        {
                            "manual_review": [
                                {
                                    "message_id": r["message_id"],
                                    "issues": json.loads(r["issues"]),
                                }
                                for r in rows
                                if r["route"] == "manual_review"
                            ]
                        },
                    )
            if self.path == "/results":
                rows = [
                    dict(r)
                    for r in db.execute("SELECT * FROM results ORDER BY message_id")
                ]
                for r in rows:
                    for k in ["issues", "source_json", "ai_json"]:
                        r[k] = json.loads(r[k])
                return self.send(200, {"results": rows})
            if self.path == "/audit":
                return self.send(
                    200,
                    {
                        "attempts": [
                            dict(r)
                            for r in db.execute("SELECT * FROM attempts ORDER BY id")
                        ]
                    },
                )
            if self.path == "/results.csv":
                return self.send(200, export_csv(db), "text/csv; charset=utf-8")
            self.send(404, {"error": "not_found"})
        finally:
            db.close()

    def do_POST(self):
        if self.path != "/record":
            return self.send(404, {"error": "not_found"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if not 0 < n <= 100000:
                return self.send(413, {"error": "invalid_payload_size"})
            body = json.loads(self.rfile.read(n))
            source = body["source"]
            raw = body["ai"]
            result = validate(source, raw)
            if "invalid_input" in result["issues"]:
                return self.send(400, {"error": "invalid_input"})
            db = connect(
                os.environ.get("LEDGER_DB", str(ROOT / "evidence/ledger.sqlite"))
            )
            try:
                receipt = save_result(db, source, raw, result)
            finally:
                db.close()
            self.send(200, receipt)
        except (ValueError, KeyError, TypeError):
            self.send(400, {"error": "invalid_payload"})
        except sqlite3.Error:
            self.send(503, {"error": "storage_unavailable"})


if __name__ == "__main__":
    ThreadingHTTPServer(
        (
            os.environ.get("LEDGER_HOST", "127.0.0.1"),
            int(os.environ.get("LEDGER_PORT", "8091")),
        ),
        Handler,
    ).serve_forever()
