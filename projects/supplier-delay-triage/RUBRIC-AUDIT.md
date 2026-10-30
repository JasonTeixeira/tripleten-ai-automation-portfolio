# Final project requirement audit

## Overall conclusion

The supplied technical and presentation checklist is covered by observable local evidence. This supports submitting the capstone for grading; it does not guarantee a grade. Two final handoff items remain: confirm the connection to the student's work/studies/community without inventing a client or job history, and perform the course upload in the accepted submission format.

| Requirement | Evidence | Assessment |
|---|---|---|
| New idea, distinct from earlier sprints | Supplier delivery triage; earlier projects were customer support, hotel chatbot, feedback, invoices and weather planning | Covered |
| Repetitive real business process and clear value | Manual steps, target operations role, potential planning impact; estimated handling-time benefit disclosed as an assumption | Covered as a studied business process; personal/community connection awaiting confirmation |
| An approved automation platform | Actual n8n 2.45.7 import and completed execution logs | Covered |
| At least two different services | n8n calls the intake/ledger API and Ollama LLM service; durable SQLite output | Covered; cloud SaaS services are not specifically required in the supplied brief |
| External input | HTTP API supplies six realistic fictional email records | Covered; sample data and API fetches are expressly allowed |
| Custom LLM prompt | prompt.txt; required JSON Schema; real Qwen2.5 3B responses | Covered |
| Structured output | SQLite database, CSV with extracted business fields, JSON results | Covered; the brief explicitly accepts database entries |
| Quality control | Input/field validation, source grounding, date checks, confidence logging, review routing, outage handling and duplicate protection | Covered |
| Sample-data testing | Six actual n8n/LLM cases; 6/6 expected routes; 36/36 checked core extraction fields | Covered for this small test set |
| Error handling/confidence evidence | Actual controlled outage, review log screenshot, logged confidence, six duplicate skips | Covered |
| Workflow diagram | Editable diagram on slide 4 | Covered |
| Input and output screenshots | Slides 5 and 9; original screenshots and CSV/database supplied | Covered |
| AI results and error-log screenshots | Slides 7 and 10 | Covered |
| Reflection | Process, importance, AI contribution and improvements in slides 2–3 and 13; presenter notes | Covered |
| Professional presentation | 32-slide revised editable PPTX and PDF; package/layout checks and visual review | Covered; PDF checked, native PowerPoint/Google Slides app not directly tested |
| Accessible submission | ZIP contains code, importable workflows, data, results, prompt, evidence and both deck formats | Public GitHub project files and revised package; course upload remains a separate step |

## Accuracy check added during this audit

A retrospective comparison checked six fields for each of the six original supplier fixtures: purchase order, supplier, event type, promised date, revised date and quantity. All **36/36** matched the source-derived expected values. See `samples/expected-extractions.json` and `evidence/field-accuracy.json`.

This is a small controlled demonstration. It does not prove general model accuracy. Summary quality, semantic relevance of evidence quotes and confidence calibration were not counted in the 36 checks. The model supplied an irrelevant quote for the short-shipment classification and high confidence for a contradictory date pair; these limitations are disclosed. The date contradiction is routed to manual review rather than accepted as a valid delay.

## What is not required by the supplied brief

A paid subscription, a live Gmail connection, a public deployment, a production schedule and commercial usage are not listed requirements. The project does not claim any of them. Additional services are separate from n8n, so this is not a one-tool filter/formula workflow.

## Final handoff checklist

- Confirm a truthful sentence explaining why this process relates to your work, studies or community. Do not invent employment, a client, or measured savings.
- Read the PDF and presenter notes and confirm you can explain the workflow and its limitations.
- Upload the presentation and supporting workflow package using TripleTen's accepted method. If a share link is used, verify that the reviewer can open it.
- A top grade remains the instructor's decision; no score is promised.

## Instructor-required implementation evidence

The revised deck adds actual readable n8n screenshots on slides 16–32, mapped individually in REVIEWER-RESPONSE.md. It shows every requested configuration, source/AI mapping, three route conditions and outputs, SQLite service/output, and successful plus controlled-outage execution. The current importable workflows contain 11 nodes. Tests now total 42 passing, with 94% ledger coverage. Original 34-test evidence is historical. Fresh editor results 3/1/2 and earlier revised CLI results 2/1/3 are separately preserved and labeled.
