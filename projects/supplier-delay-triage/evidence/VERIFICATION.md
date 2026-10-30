# Final verification — October 30, 2026

## Executed checks

| Check | Result | Evidence |
|---|---|---|
| Workflow generation | PASS; two importable seven-node workflows | build.txt, workflows/*.json |
| Python compile / shell syntax / Compose config | PASS | `python3 -m compileall -q src tests`; `bash -n run-demo.sh`; `docker compose config --quiet` |
| Ruff lint and formatting | PASS | lint.txt; `ruff format --check src tests` |
| Automated tests | 34 passed, 0 failures | tests.txt |
| Ledger line coverage | 94% (186 executable statements) | coverage.txt |
| Real n8n six-email batch | success, finished=true; 6 expected routes | final-batch-run.txt, live-results.json |
| Controlled LLM outage | success; FAILURE-001 routed to review with llm_unavailable | final-outage-run.txt |
| Duplicate replay | success; 6 duplicate_skipped events, 7 unique records | final-duplicate-run.txt, final-audit.json |
| Smaller CPU runtime | actual LLM returned READY; complete n8n workflow also passed | cpu-runtime-smoke.json, cpu-workflow-smoke.txt |
| Secret-pattern scan in authored project files | No matches | secret-scan.txt |
| Independent code review | Both material findings fixed and rechecked | REVIEW.md |
| Editable PowerPoint | 14 slides; package, geometry, font and reimport checks passed; no findings or warnings | presentation-validation-final.json |
| PDF export | 14 pages; all pages contain text; cover, diagram, result table, error log, test results and closing slide checked after export | PDF deliverable and native slide renders |

Test output:

```text
Ran 34 tests in 0.592s
OK
TOTAL 186 statements, 12 missed, 94% coverage
All checks passed!
```

## What the evidence proves

The normal batch made actual calls through n8n to a real Qwen2.5 3B model served by Ollama and wrote results to the SQLite-backed API. It produced three exceptions, one routine record and two review records. The deliberately failed LLM endpoint created a seventh, separately identified review record. The first duplicate replay produced six audit skips. Those three runs and their 13-event audit snapshot are preserved separately. An additional full n8n replay then validated the smaller CPU runtime; the live audit therefore has six more duplicate-skip events than the earlier snapshot.

The 6/6 result is agreement with expected routing on six fictional fixtures. It is not a general model-accuracy benchmark. The confidence values are model self-assessments. Quote checks test source presence rather than semantic relevance. Business time savings are illustrative assumptions, not a timed operational study.

## Review and scope limits

The folder is a new standalone project, not a Git repository. Existing portfolio files were read without modification; no push, publication, account change, paid plan, cloud upload, or course submission occurred. Authenticated inbox intake, real customer data, commercial model licensing and production deployment remain future work. PowerPoint and Google Slides native-app compatibility were not directly tested; first-party PPTX import and LibreOffice PDF conversion were tested.

The n8n image emits a missing Python task-runner notice; this workflow uses JavaScript preparation nodes and completed successfully. Security review covered input limits, JSON validation, exact PO tokens, parameterized SQLite writes, CSV formula escaping, prompt/data boundaries and loopback-only host exposure. Container CVE scanning was not performed. This is a local educational demo, not a production security certification.

The Docker VM was already capacity-constrained during setup. App and model data use host bind mounts. The final Ollama CPU image is approximately 234 MB; it copies official pinned runtime binaries and omits unused GPU libraries. The initial vendor download is larger. Only this task’s redundant model volume and vendor image tag were removed; no existing project resources, general caches, snapshots, settings or schedules were pruned.

## Public repository handoff

The statements above record the local build and test phase. The owner subsequently explicitly authorized publishing the audited project, slides and evidence to the public TripleTen portfolio. This GitHub handoff publishes static project files; it does not activate an external workflow or submit coursework. The public audited ZIP redacts execution-resume tokens and regenerates its internal checksums; test records and business results remain unchanged.

For Git readability, extracted execution text logs have trailing whitespace removed and the CSV uses LF line endings. Record values and execution results are unchanged. The included audited ZIP keeps the original record formatting, with execution-resume token values redacted.

Publication security review redacted all four completed n8n `resumeToken` values from the public execution logs and downloadable ZIP. The original local archive remains private. No other credentials were found by the publication review.

## Reviewer screenshot revision verification

The revised importable workflows contain eleven nodes, including a native Switch and three visible branches. The current suite passes 42 tests with 94% ledger line coverage. Ruff, formatting, Python compilation, shell syntax and Compose validation pass. Actual editor captures show a fresh 3/1/2 normal execution and an independent successful controlled outage. Earlier revised CLI evidence 2/1/3 and duplicate prevention remain separate. See reviewer-fix/ for raw screenshots, separate snapshots, run logs, current test output and presentation validation. The 32-slide revised PPTX and PDF replace the original deck as the resubmission artifact. No course upload is performed by this repository update.
