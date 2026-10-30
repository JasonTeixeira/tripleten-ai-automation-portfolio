# Revised TripleTen capstone submission

**Supplier Delay Triage · Jason Teixeira**

1. Open the [revised 32-slide PDF](presentation/Supplier-Delay-Triage-Jason-Teixeira-Reviewer-Revision-Final.pdf). Slides 16–32 show actual implementation screenshots, each on its own slide.
2. Use the [editable PowerPoint](presentation/Supplier-Delay-Triage-Jason-Teixeira-Reviewer-Revision-Final.pptx) if required. Speaker notes are embedded.
3. Read [REVIEWER-RESPONSE.md](REVIEWER-RESPONSE.md) for a ready-to-paste response and a requirement-to-slide index.
4. Submit the revised presentation and [updated package](submission/TripleTen-Final-Project-Jason-Teixeira-Reviewer-Revision.zip) through TripleTen. The course upload remains your final step.

The fresh editor run produced 3 exceptions, 1 routine log and 2 manual reviews. The separate controlled outage produced one stored review record. Earlier original and revised CLI evidence remains clearly labeled. The current suite passes 42 tests with 94% ledger coverage.

This is a manually triggered local prototype using fictional supplier records fetched through an API. It connects real n8n, Ollama and SQLite services. Business savings remain illustrative assumptions. To rerun with Docker Desktop, run `bash run-demo.sh`. Cached models, n8n owner credentials and private runtime files are excluded from the package.
