# Supplier Delay Triage

**Jason Teixeira — TripleTen AI Automation Final Project**

I built an AI workflow for an operations team that repeatedly reads supplier emails and updates a delivery tracker. The workflow identifies delayed deliveries, partial shipments, and on-time confirmations, then records structured results for staff to review.

The manual process requires opening each email, finding the purchase-order number, copying delivery dates and quantities, calculating lateness, flagging uncertain updates, and checking duplicates. These tasks are repetitive and inconsistent messages make copying errors more likely.

My workflow uses **n8n** to fetch email records from an **intake API**, split the batch, and call **Ollama running Qwen2.5 3B**. I wrote a custom prompt asking the LLM to extract the purchase order, supplier, event type, dates, quantity, summary, exact source quote, and confidence. The LLM returns JSON using a required schema.

A separate **Operations Ledger API** validates the output, calculates the delay, assigns a route, and writes the result to **SQLite**. The results can also be exported as CSV. Deterministic checks catch missing fields, unsupported order numbers, invalid dates, conflicting delivery information, and low confidence. Failed AI calls create manual-review records. Message IDs prevent duplicate rows and every write attempt is audited.

The real n8n workflow was tested on six realistic fictional supplier messages. The final routes matched all six expectations: three exceptions, one routine log, and two manual reviews. A separate test deliberately made the LLM unavailable and successfully recorded the failure for review. Replaying the batch skipped six duplicate records. The included automated suite passed 34 tests with 94% line coverage of the validation/ledger code.

One important result was that the model gave a contradictory date pair 0.95 confidence. The date validator caught the contradiction. This showed why confidence scores alone are insufficient. Exact quote matching also checks whether a quote exists, not whether it supports the classification; stronger semantic evaluation is a next step.

Business value is estimated rather than measured: at 40 messages per week, reducing human handling from four minutes to one minute per message would save about 120 minutes per week. A pilot would need to measure actual handling time and error rates.

The presentation includes the process map, an editable workflow diagram, input and output screenshots, the actual AI result, review/error logs, test results, and reflection. Supporting files include importable n8n workflows, the full prompt, sample data, runnable services, and execution evidence.

This is a tested local prototype using a manual batch trigger and fixture emails served through an API. Future work includes authenticated inbox intake, purchase-order system checks, better evidence-quality evaluation, and a monitored pilot. Model licensing must be reviewed before commercial deployment.
