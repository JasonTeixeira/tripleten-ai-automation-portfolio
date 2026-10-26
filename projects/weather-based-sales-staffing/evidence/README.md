# Evidence record

## Local implementation proof

The Node test suite exercises validation and formatting, including the generated
scripts intended for Code by Zapier. It does not use live external accounts.
Run `npm run test:coverage` for the latest results. See `LOCAL_VERIFICATION.md`
for the recorded local gate results.

## Live proof still required

| Evidence | Status | Suggested screenshot |
|---|---|---|
| Postman success with Miami response and imperial query | Not run | 01-postman-redacted.png |
| Full Zap canvas with field mappings | Not built in a live account | 02-zap-workflow.png |
| Gemini prompt and actual output | Not run | 03-gemini-prompt-output.png |
| Daily email received in confirmed test inbox | Not sent | 04-received-daily-email.png |
| Clear sky at 91°F, regular email and no extra alert | Not run live | 05-boundary-no-alert.png |
| Synthetic 91.1°F, regular email and heat alert | Not run live | 06-heat-alert.png |
| Synthetic rain/storm alert received | Not run live | 07-storm-alert.png |
| Scheduled run near 7 AM Miami time | Not activated | 08-scheduled-run.png |

For each test, record time, input source, observed result, and screenshot filename.
Label edited/synthetic weather explicitly. Redact API keys, connection details,
and unrelated inbox content before putting evidence in a public repository.
No screenshots have been fabricated or supplied for these pending tests.
