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
request = {
    "model": "qwen2.5:3b",
    "stream": False,
    "format": schema,
    "options": {"temperature": 0, "num_ctx": 4096, "num_predict": 500, "num_thread": 4},
    "messages": [{"role": "system", "content": prompt}],
}
prepare = (
    "const request="
    + json.dumps(request)
    + "; return $input.all().map((item,i)=>({json:{source:item.json,request:{...request,messages:[...request.messages,{role:'user',content:JSON.stringify(item.json)}]}},pairedItem:{item:i}}));"
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
prepareRecord = "return $input.all().map((item,i)=>({json:{source:$('Prepare AI Request').itemMatching(i).json.source,ai:item.json.message ? item.json.message.content : {error:'llm_unavailable'}},pairedItem:{item:i}}));"
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
connections = {}
for a, b in zip(nodes, nodes[1:]):
    connections[a["name"]] = {
        "main": [[{"node": b["name"], "type": "main", "index": 0}]]
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
    "Built 7-node n8n workflow with local LLM, validation, routing and durable logging."
)
