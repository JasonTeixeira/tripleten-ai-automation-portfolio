# Presenter notes

1. **Supplier Delay Triage.** My capstone automates the repetitive work of reading supplier delivery updates and maintaining an exception register. It is a new process, separate from my earlier coursework.

2. **Business problem.** Supplier messages use different wording, but operations staff need the same facts every time. Repeated reading and copying makes it easy to miss a revised arrival date or a partial shipment.

3. **Manual and automated process.** AI reads and extracts the message. Code handles date calculations, validation, routing, and duplicate protection. A person still decides how to follow up with the supplier or change an order.

4. **Workflow diagram.** The input API supplies email records. n8n fetches and splits the batch, prepares the custom request, and calls the local LLM. The ledger API validates the response and writes structured results to SQLite. The workflow connects separate automation, LLM, and data services.

5. **Input.** This fictional supplier update contains an order number, an original delivery date, a revised date, and a quantity. I used six realistic examples to cover both normal and problematic situations. This prototype does not access a real mailbox.

6. **Custom prompt.** I instructed the model to act as an operations analyst, treat email content as data, preserve unknown or conflicting facts, and return only the required JSON fields. The complete prompt is included with the project.

7. **AI result.** The model extracted the order and dates from the message. The validator independently calculated a four-day delay and assigned high priority. Confidence is logged, but it is not an accuracy guarantee.

8. **Batch results.** Three records became exceptions, one was logged as routine, and two needed manual review. The negative delay in the fifth example is intentional test data: an earlier revised date contradicts the message’s claim that the order is delayed.

9. **Structured output.** Each record has a stable ID, route, priority, and calculated delay. The CSV also includes the extracted business fields. The source and raw model response remain available so a reviewer can trace the result.

10. **Quality control.** I tested both problematic content and service failure. Missing dates and contradictory dates go to review. A separate workflow calls an unavailable LLM endpoint and still creates a review record. A duplicate replay adds audit events without adding duplicate result rows.

11. **Testing.** All six samples matched their expected final route. The outage and duplicate tests also passed, as did 34 automated checks. The 94% code coverage figure applies to the ledger code; it does not measure model accuracy.

12. **Business value.** These numbers are an illustration. Forty weekly messages at four minutes each would require 160 minutes. If automation reduces human handling to one minute per message, the estimate is 120 minutes saved per week. A real pilot must validate that assumption.

13. **Reflection.** AI helped turn varied language into consistent fields. The most useful safeguard was checking facts outside the model: it assigned high confidence to contradictory dates, but code caught the conflict. Future work includes inbox integration, purchase-order checks, and better evaluation of whether evidence quotes support a classification. The model’s license also needs review before commercial use.

14. **Submission.** The package includes the editable deck, PDF, workflow files, prompt, inputs, outputs, source code, tests, and raw evidence. The local prototype is complete and tested. Live inbox integration and a scheduled production pilot are future work.


## Reviewer implementation appendix

Slides 1–14 preserve the original demonstration, including its original 34-test results. Slide 15 introduces the revision, which has 42 passing tests and eleven nodes. The fresh editor run and the earlier CLI revision are distinct runs.

16. **Complete n8n workflow.** Actual successful editor run. All 11 nodes connect, with 3 exception, 1 routine and 2 review items.
17. **API intake configuration.** GET /intake supplies six fictional email records, including subject and body.
18. **One email per workflow item.** Split Out maps the messages array into six individual supplier email records.
19. **Custom AI system prompt.** The actual Prepare AI Request node defines extraction rules and treats email text as untrusted data.
20. **Email content mapped into the LLM request.** Each email becomes JSON.stringify(item.json). The request includes the model, JSON Schema and system prompt.
21. **Ollama HTTP configuration.** POST /api/chat sends $json.request to Qwen2.5 3B and returns the actual structured response.
22. **AI response and source mapping.** The Code node pairs the source record with message.content. The validator parses and checks that JSON.
23. **Validation and SQLite write request.** POST /record sends $json. The separate ledger service validates and stores the result before returning its route.
24. **Mapped payload for SQLite storage.** The HTTP body maps the complete $json source and AI payload into /record. The response confirms created: true.
25. **Exception condition and execution.** Native Switch compares $json.route with exception. Its Exception output contains three actual records.
26. **Routine Log condition and execution.** Native Switch compares $json.route with logged. Its Routine Log output contains SUP-002.
27. **Manual Review condition and execution.** Native Switch compares $json.route with manual_review. Missing or conflicting dates produce two review items.
28. **SQLite service configuration.** The ledger container sets LEDGER_DB to /data/ledger-review.sqlite. SQLite storage runs in this service.
29. **SQLite persisted CLI-run records.** Read-only SQL from the earlier CLI revision shows 2 exceptions, 1 routine log and 3 review records.
30. **Controlled LLM outage execution.** The actual editor run continues through the failed LLM call and routes one item to Manual Review.
31. **Controlled outage configuration and error.** The test deliberately calls closed port 1. Continue-on-error passes the failure to validation.
32. **Stored outage review result.** FAILURE-001 reaches Manual Review with llm_unavailable. The workflow completes and stores the record.
