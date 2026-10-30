# Your finished TripleTen capstone

**Project:** Supplier Delay Triage · **Presenter:** Jason Teixeira

1. Open `presentation/Supplier-Delay-Triage-Jason-Teixeira-Final.pdf` to review the 14 slides.
2. Use the matching `.pptx` if you want to edit or import the deck into Google Slides. Speaker notes are embedded. A separate `PRESENTER-NOTES.md` is included.
3. Submit the presentation together with this project package, or attach the workflow JSON and supporting evidence as your course allows. `SUBMISSION.md` contains ready-to-paste project text.
4. To demonstrate the workflow again with Docker Desktop running, execute `bash run-demo.sh` from this folder. Initial setup downloads the model and vendor image. The runtime uses a smaller CPU image built from the official Ollama binaries.

The project has already run in real n8n with a real local LLM. The six-email test produced three exception records, one routine record, and two review records. A separate LLM outage produced a review record, and a duplicate replay skipped six writes. Raw run logs, AI results, the CSV, screenshots, and verification records are in `evidence/`.

**Scope:** a manually triggered local prototype with realistic fictional email inputs fetched through an API. It does not monitor a live mailbox. Estimated business savings are labeled as assumptions. Project files are published in this GitHub portfolio. The workflow is not cloud-hosted, and course submission has not been performed.

You do not need a paid Zapier account or a cloud LLM key. Docker Desktop and sufficient space for the initial vendor/model downloads are required to rerun it. Cached model and application data are excluded from the submission ZIP.
