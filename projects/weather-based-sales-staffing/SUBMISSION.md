# Submission links and readiness

**Author:** Jason Teixeira

**Existing repository:** https://github.com/JasonTeixeira/tripleten-ai-automation-portfolio

**Local project folder:** `projects/weather-based-sales-staffing/`

**Published branch:** `codex/weather-based-sales-staffing`.

**Project link:** https://github.com/JasonTeixeira/tripleten-ai-automation-portfolio/tree/codex/weather-based-sales-staffing/projects/weather-based-sales-staffing

This branch contains the reviewed build kit. The main branch does not yet include
this project. The live workflow and final presentation remain pending.

**Presentation template:** https://docs.google.com/presentation/d/1oSvomOtgMT6Z-msUzkPApBAOdD0wG976CkDw2cGDn7U/edit

**Presentation draft:** The linked Google deck is renamed and partially edited,
but remains incomplete. It is not yet a submission-ready presentation.

## Before submitting

- [ ] Confirm the recipient and connect Zapier, OpenWeather, Gemini, and Gmail.
- [ ] Build the Zap using BUILD_KIT.md and test with real OpenWeather data.
- [ ] Receive and inspect the test email.
- [ ] Test optional alert behavior, clearly labeling synthetic weather.
- [ ] Capture redacted screenshots and complete the evidence record.
- [ ] Update the presentation with actual findings and screenshots.
- [ ] Delete instructions and unused sample slides.
- [ ] Add the final deck URL and/or exported deck to this project folder.
- [x] Review the local diff, then publish the approved branch to the existing repository.
- [x] Verify the branch includes this folder through the GitHub repository API.
- [ ] Confirm the final submission link opens for the reviewer after all live evidence is added.

The project folder is available on the published branch. Do not submit the
project as fully working based on local helper tests alone.

## Live setup checkpoint — October 26, 2026

- GitHub authentication verified and the reviewed project branch published.
- Local build, syntax checks, 47 tests, and dependency audit passed again before publishing.
- Zapier sign-in and Gmail connection are now verified. The connected business
  inbox will be used for tests. No emails sent and no recurring Zap activated.
- Schedule and OpenWeather editor tests passed in the saved live Zap draft.
- Direct OpenWeather and Gemini API tests passed. The Gemini Zapier connection
  is awaiting completion in its open connection window.
- No direct Google Drive or Gmail connector is confirmed connected in this session.
- Actual weather and AI output are saved under `evidence/`, with direct API tests
  distinguished from Zapier tests. See `evidence/LIVE_PROGRESS.md`.
