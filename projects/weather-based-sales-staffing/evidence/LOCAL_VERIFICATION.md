# Local verification

Verified October 26, 2026 on Node.js v22.22.3. This report covers local helpers
and generated scripts, not the live external workflow.

| Gate | Result |
|---|---|
| `npm run build` | Passed: both generated Code by Zapier scripts compiled |
| `npm run check` | Passed: source/build/demo syntax checks |
| `npm test` | 47 passed, 0 failed, 0 skipped |
| `npm run test:coverage` | planning.cjs: 100% lines, 100% functions, 98.31% branches |
| `npm run demo` | Passed: two explicitly simulated local examples, no email sent |
| Runtime dependencies | None |
| `npm audit` | Passed: 0 vulnerabilities |
| Independent read-only code/security review | No blocking findings; corrected prompt word-limit mismatch |

TDD checkpoints on local branch `codex/weather-based-sales-staffing`:

- `b7c45ba`: tests executed against missing implementation, 43 failures.
- `99ad087`: implementation added, 44 tests passed, including an added word-limit check.
- Three generated-script integration tests subsequently brought the total to 47.

Security review checked invalid/missing inputs, bounded AI output, strict JSON,
plain-text rendering, fixed subjects, absence of AI-selected recipients, and
absence of embedded keys. No application server, credential store, database,
or network client is present in these helpers.

The generated scripts must still be tested in the actual Zapier runtime with
real mappings. Gemini can produce semantically weak advice despite passing
structural checks. Upstream failures suppress the downstream alert. No live
OpenWeather, Gemini, Gmail, scheduling, or inbox proof has been collected.
