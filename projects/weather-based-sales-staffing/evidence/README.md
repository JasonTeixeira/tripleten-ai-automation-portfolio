# Evidence record

See [LIVE_PROGRESS.md](LIVE_PROGRESS.md) for inputs, timestamps, test limits, and
remaining work. Screenshots are actual service UI, not mockups.

| Evidence | Result |
|---|---|
| Direct OpenWeather/Gemini calls | HTTP200 with real Miami weather and validated AI output |
| Schedule/Webhooks/Gemini/Code editor tests | Passed |
| Received daily email | Verified, 06-received-daily-email.jpg |
| Normal filter | Correctly stopped; 07-alert-filter-false.jpg |
| Simulated severe-weather filter | Correctly continued; 08-alert-filter-true-simulated.jpg |
| Simulated alert email | Send succeeded, INBOX returned, received message visible in Gmail search; 09-alert-send-success-simulated.jpg |
| Postman | Not run; importable collection supplied |
| Recurring schedule | Not activated or observed |
| Presentation exports | Complete; 17-slide PDF and editable PowerPoint in ../presentation/ |
| Final native Google Slides | 17 slides converted and reviewed; Anyone with link → Viewer; 10-google-slides-viewer-access.png |
| Original Google template | Separate unfinished draft; use the final link in ../SUBMISSION.md |

Local tests cover91°F/91.1°F boundaries, rain, storms, invalid mappings, stale
observations, malformed AI, and promo lengths. They do not prove cloud delivery.
Both generated scripts are exercised locally; the installed Zap uses only the
combined plan validator after Gemini. The weather-only script is optional.

Public evidence excludes credentials and unrelated inbox content. The recipient
shown in project screenshots is the owner's confirmed business test inbox.
