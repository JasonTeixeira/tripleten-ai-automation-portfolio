import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
prompt = (root / "prompt.txt").read_text()
schema = {
    "type": "object",
    "properties": {
        "purchase_order": {"type": ["string", "null"]},
        "supplier": {"type": ["string", "null"]},
        "event_type": {
            "type": "string",
            "enum": ["delay", "on_track", "short_shipment", "unclear"],
        },
        "promised_date": {"type": ["string", "null"]},
        "revised_date": {"type": ["string", "null"]},
        "quantity": {"type": ["integer", "null"]},
        "summary": {"type": "string"},
        "evidence_quote": {"type": "string"},
        "confidence": {"type": "number"},
    },
    "required": [
        "purchase_order",
        "supplier",
        "event_type",
        "promised_date",
        "revised_date",
        "quantity",
        "summary",
        "evidence_quote",
        "confidence",
    ],
    "additionalProperties": False,
}
nodes = []


def add(name, kind, params, x, version=1, **extra):
    nodes.append(
        {
            "id": name.lower().replace(" ", "-"),
            "name": name,
            "type": "n8n-nodes-base." + kind,
            "typeVersion": version,
            "position": [x, 300],
            "parameters": params,
            **extra,
        }
    )


add("Run Supplier Batch", "manualTrigger", {}, 0)
add(
    "Fetch Supplier Emails",
    "httpRequest",
    {"url": "http://ledger:8091/intake", "options": {}},
    250,
    4.2,
)
add(
    "One Email Per Item",
    "splitOut",
    {"fieldToSplitOut": "messages", "options": {}},
    500,
    1,
)
prepare = (
    "const systemPrompt = "
    + json.dumps(prompt.split("\n"), indent=2)
    + '.join("\\n");\n\n'
    + "const outputSchema = "
    + json.dumps(schema, indent=2)
    + ";\n\n"
    + """return $input.all().map((item, index) => ({
  json: {
    source: item.json,
    request: {
      model: "qwen2.5:3b",
      stream: false,
      format: outputSchema,
      options: { temperature: 0, num_ctx: 4096, num_predict: 500, num_thread: 4 },
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: JSON.stringify(item.json) }
      ]
    }
  },
  pairedItem: { item: index }
}));"""
)
add("Prepare AI Request", "code", {"jsCode": prepare}, 650, 2)
body = "={{ $json.request }}"
add(
    "Extract With Local LLM",
    "httpRequest",
    {
        "method": "POST",
        "url": "http://ollama:11434/api/chat",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": body,
        "options": {
            "timeout": 240000,
            "batching": {"batch": {"batchSize": 1, "batchInterval": 100}},
        },
    },
    750,
    4.2,
    onError="continueRegularOutput",
)
prepareRecord = """return $input.all().map((item, index) => ({
  json: {
    source: $("Prepare AI Request").itemMatching(index).json.source,
    ai: item.json.message
      ? item.json.message.content
      : { error: "llm_unavailable" }
  },
  pairedItem: { item: index }
}));"""
add("Prepare Ledger Record", "code", {"jsCode": prepareRecord}, 900, 2)
record = "={{ $json }}"
add(
    "Validate Route And Record",
    "httpRequest",
    {
        "method": "POST",
        "url": "http://ledger:8091/record",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": record,
        "options": {"timeout": 15000},
    },
    1000,
    4.2,
    retryOnFail=True,
    maxTries=3,
    waitBetweenTries=1000,
)
# Expose backend-validated outcomes directly on the n8n canvas.
routing_rules = []
for value, label in [
    ("exception", "Exception"),
    ("logged", "Routine Log"),
    ("manual_review", "Manual Review"),
]:
    routing_rules.append(
        {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                    "version": 2,
                },
                "conditions": [
                    {
                        "id": "route-" + value,
                        "leftValue": "={{ $json.route }}",
                        "rightValue": value,
                        "operator": {"type": "string", "operation": "equals"},
                    }
                ],
                "combinator": "and",
            },
            "renameOutput": True,
            "outputKey": label,
        }
    )
add(
    "Route Delivery Outcomes",
    "switch",
    {
        "rules": {"values": routing_rules},
        "options": {"fallbackOutput": "extra"},
    },
    1820,
    3.3,
)
for label, y in [("Exception", 100), ("Routine Log", 300), ("Manual Review", 500)]:
    add(label, "noOp", {}, 2080)
    nodes[-1]["position"][1] = y
for index, node in enumerate(nodes[:8]):
    node["position"] = [index * 260, 300]
connections = {}
for a, b in zip(nodes[:8], nodes[1:8]):
    connections[a["name"]] = {
        "main": [[{"node": b["name"], "type": "main", "index": 0}]]
    }
connections["Route Delivery Outcomes"] = {
    "main": [
        [{"node": name, "type": "main", "index": 0}]
        for name in ["Exception", "Routine Log", "Manual Review", "Manual Review"]
    ]
}
workflow = {
    "id": "supplierDelayCapstone2026",
    "name": "Supplier Delay Triage | TripleTen Final | Jason Teixeira",
    "nodes": nodes,
    "connections": connections,
    "active": False,
    "settings": {"executionOrder": "v1"},
    "pinData": {},
    "tags": [],
}
(root / "workflows/supplier-delay-triage.json").write_text(
    json.dumps(workflow, indent=2)
)
(root / "samples/output-schema.json").write_text(json.dumps(schema, indent=2))
failure = json.loads(json.dumps(workflow))
failure["id"] = "supplierFailureCapstone2026"
failure["name"] = "Controlled LLM outage | TripleTen Final"
for node in failure["nodes"]:
    if node["name"] == "Fetch Supplier Emails":
        node["parameters"]["url"] = "http://ledger:8091/intake/failure"
    if node["name"] == "Extract With Local LLM":
        node["parameters"]["url"] = "http://ollama:1/api/chat"
        node["parameters"]["options"] = {"timeout": 5000}
(root / "workflows/controlled-llm-outage.json").write_text(
    json.dumps(failure, indent=2)
)
print(
    "Built 11-node n8n workflow with visible routes, local LLM, validation, routing and durable logging."
)
