# Reviewer revision status

## Completed locally

- Preserved the published original capstone and presentation.
- Added a real native n8n Switch with explicit route comparisons and a fail-safe extra output to Manual Review.
- Added visible Exception, Routine Log and Manual Review branch nodes. The workflow now has 11 nodes.
- Reformatted the real AI prompt and request/response mapping code for readable editor inspection.
- Ran the revised workflow against the real local LLM and a new isolated SQLite database. Switch counts: [2, 1, 3, 0].
- Ran a real controlled outage. Switch counts: [0, 0, 1, 0].
- Replayed the six messages. All six duplicate writes were skipped, leaving7 unique rows and13 audit events after the outage and replay.
- Passed42 automated tests and Ruff. Ledger code coverage remains94%.
- Independent reviewer reran42 tests, checked outputs and redaction, and found no routing correctness or security blocker.
- Captured actual Docker Desktop SQLite-path configuration, a read-only SQL query with six stored normal-run records, and the unchanged backend routing source.

## Required user step

Open http://localhost:5680/setup and complete the first local n8n owner account. The original project used n8n's CLI and has no existing editor owner login. New-password entry must be completed by the user under computer-use confirmation rules. No default password is placed in code or requested in chat.

## Still pending

- Actual n8n canvas, individual node parameter/mapping screens and execution screenshots.
- A readable revised presentation with those captures spread across separate slides.
- Updated submission ZIP, final public manifest and GitHub publication of the completed revision.

Do not resubmit the original14-slide deck as the completed screenshot revision. No fabricated or recreated n8n screenshots will be used.

## Evidence boundary

Original run:3 exceptions,1 routine log,2 reviews;34 tests. New revision run:2 exceptions,1 routine log,3 reviews;42 tests. In the new run, SUP-003's quote differs in capitalization from the source and correctly fails the exact-source check. The42-test suite verifies all36 core fields in that new six-message run separately from quote validity.
