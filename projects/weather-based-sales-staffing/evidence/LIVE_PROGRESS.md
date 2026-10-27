# Live setup progress — October 26, 2026

Editor step tests and inbox delivery are proven below. Publishing was attempted
after restoration, but Zapier showed “Upgrade to Pro to publish this Zap.” The
account is on Free, which allows two-step Zaps. No subscription was started.
No scheduled 7 AM run has been observed.

| Check | Observed result | Evidence |
|---|---|---|
| OpenWeather direct API | HTTP 200; Miami 79.92°F, broken clouds | live-openweather-response.json |
| Gemini direct API | HTTP 200; gemini-2.5-flash; validated promos 83/98 characters | live-gemini-result.json; live-api-validation.json |
| Schedule1 | Every day, 7 AM, weekends yes, America/New_York; editor test passed | Saved Zap draft |
| Webhooks2 | HTTP success, Miami 79.75°F, broken clouds; humidity72%, wind18.41mph | 02-zapier-openweather-success.jpg |
| Gemini3 | Send Prompt succeeded with mapped real fields; STOP; two promos | 03-zapier-gemini-input.jpg; 04-zapier-gemini-success.jpg; zapier-gemini-response.txt |
| Code4 | Cloud validation passed; promos84/97 characters; alert false | 05-zapier-validation-success.jpg |
| Gmail5 | Sent to owner's confirmed inbox; received October26 at7:40PM EDT | 06-received-daily-email.jpg; received-daily-email.txt |
| Filter6 negative | Real normal-weather alert_required false stopped filter | 07-alert-filter-false.jpg |
| Filter6 positive | Synthetic94°F with thunderstorm/rain produced true and passed | 08-alert-filter-true-simulated.jpg |
| Gmail7 positive | Labeled simulated alert sent at7:58PM EDT; Gmail returned INBOX/SENT; search showed received message | 09-alert-send-success-simulated.jpg |
| Restoration | Code4 temperature and description restored to Webhooks tokens; retest returned false; Gmail7 subject/body restored to Code4 tokens only | Observed editor fields and cloud retest |
| Publication | Blocked by Free plan; Pro required for this multistep workflow | 10-publish-plan-blocker.jpg |
| Presentation | Renamed, author added, Problem edited; other template placeholders remain | presentation-cover-draft.jpg |

## What these tests establish

The real daily email used the same saved OpenWeather response and Gemini output
through the mapped validation and Gmail actions. These were individual editor
tests, not a single observed scheduled execution. Source weather was observed at
6:16:54PM EDT; the daily editor email arrived at7:40PM EDT. Its footer describes
the configured schedule, not the test-send time.

The optional alert test temporarily replaced only Code4 temperature/description
with synthetic94°F and thunderstorm/rain. The AI response remained the normal
weather response and was not used as storm advice. Gmail5 was not sent during
this simulation. Gmail7's deterministic alert body included heat/storm adjustments,
and both subject/body identified the simulation. Production mappings were then
restored and the validator returned alert_required false. The final Gmail7 body
is empty under normal conditions, which is expected behind Filter6.

Direct API and later Zapier tests are separate observations, explaining the small
temperature difference. `templates/` and live-api-email-preview.txt are local
examples, not evidence of delivery. No secrets are saved in this evidence set.

## Still outstanding

- Complete and visually review the presentation; remove instructions/sample slides.
- Capture an opened alert email screenshot (inbox search receipt already observed).
- Complete the plan decision, run a final normal workflow check, and publish/activate it.
- Publish dialog was given the name Bayside Brews & Scoops — Daily Weather Plan.
- Observe the first scheduled run near7AM Miami time.
- Run the imported Postman collection before claiming a Postman-specific test.

Browser control became unresponsive during final editing. The last verified
state was the same saved draft with live mappings restored, all seven step tests
passed, and production Gmail7 subject/body mappings cleaned of simulation text.
After refreshing, publication reached the explicit plan blocker. No publish
success or activation was observed. The Zap and presentation tabs were reopened
and preserved for continuation.

## Links

- Zap draft: https://zapier.com/editor/384798430/draft
- Presentation draft: https://docs.google.com/presentation/d/1oSvomOtgMT6Z-msUzkPApBAOdD0wG976CkDw2cGDn7U/edit
