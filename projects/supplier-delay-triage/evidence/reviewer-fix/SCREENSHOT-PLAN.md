# Actual implementation screenshot plan

Every screenshot must come from the running n8n editor or actual database service. No recreated n8n screens, simulated executions, or placeholder configuration images.

| Capture | Actual screen | What the reviewer can verify |
|---|---|---|
| Complete workflow | n8n canvas, executed state | All 11 connected nodes, native Switch and three labeled outcomes |
| Intake | Fetch Supplier Emails parameters/output | GET ledger /intake and incoming messages array |
| One email per item | Split Out parameters/output | messages field split to six individual records |
| Custom prompt | Prepare AI Request expanded Code editor | Full system instructions in readable source |
| Email mapping | Prepare AI Request code / generated request | user message receives JSON.stringify(item.json) |
| Ollama request | Extract With Local LLM parameters/output | POST /api/chat, request mapping, real structured response |
| Response mapping | Prepare Ledger Record parameters/output | Source item pairing, AI content, explicit unavailable-model fallback |
| Validation and storage | Validate Route And Record parameters/output | POST /record, source/AI JSON payload, persisted receipt |
| Route conditions | Route Delivery Outcomes parameters | exact comparisons for exception, logged and manual_review plus fallback |
| Exception execution | Exception branch output | Current exception records actually routed |
| Routine execution | Routine Log branch output | On-time message actually routed |
| Review execution | Manual Review branch output | Validation reasons and uncertain/conflicting messages |
| SQLite configuration | Docker Desktop ledger Inspect | Actual LEDGER_DB path /data/ledger-review.sqlite |
| SQLite records | Docker Desktop ledger Exec | Read-only SQL query and stored rows |
| Outage execution | Controlled outage workflow execution | llm_unavailable review item and completed run |

Each configuration gets its own slide, with one large readable screenshot and a plain caption. Preserve the original 14-slide submission as historical evidence. Label the fresh revision run separately because a conservative quote check sends SUP-003 to manual review in this run.
