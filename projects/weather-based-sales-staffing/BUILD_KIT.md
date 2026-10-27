# Build the Bayside morning plan

This is the canonical setup for the tested helpers in this folder. It uses the
assignment's current-weather endpoint and the JSON contract in `prompt.txt`.

## Before starting

Confirm your Zapier plan/trial supports Webhooks and multi-step Zaps. Connect
OpenWeather, Google AI Studio (Gemini), and Gmail yourself through their supported
flows. Keep API keys private. Confirm your own test inbox before running Gmail.
The example address `emily.davis@retail.com` is not a test destination.

## 1. Schedule by Zapier

- Event: Every Day.
- Time: 7:00 AM.
- Weekends: Yes.
- Timezone Override (Optional): America/New_York, when this field is available.
  This override is present in the current editor and was set on the live draft.
  If your version lacks it, set the Zapier account timezone to America/New_York.

## 2. Test OpenWeather in Postman, then Zapier

Import `postman_collection.json`. Set `OPENWEATHER_API_KEY` as a private local
environment variable in Postman. Run the request and check HTTP 200, city Miami,
numeric `main.temp`, and a nonempty `weather[0].description`. Hide the API key in
screenshots and do not export the populated environment.

In Webhooks by Zapier select GET:

```text
URL: https://api.openweathermap.org/data/2.5/weather
q: Miami,FL,US
units: imperial
appid: enter your API key privately
```

If a new key returns 401, check the key and activation status. Do not continue
with sample weather pretending it came from a successful API call.

## 3. Google AI Studio (Gemini): Send Prompt

Paste `prompt.txt`, replacing each placeholder with its corresponding Webhooks
output token: temperature = main.temp, description = weather[0].description,
humidity = main.humidity, wind = wind.speed, observed_at = dt (Unix seconds).
Use gemini-2.5-flash, temperature 0.2 and maximum output tokens 2048.
These values were used in the successful live editor test.

Inspect the response for `product_focus`, `staffing_suggestion` and two `promos`.
The validator accepts raw JSON or one complete outer JSON code fence. It rejects
surrounding commentary. The generated weather-only helper `01-validate-weather.js.txt`
is an optional reusable helper and is not installed in this seven-step Zap.

## 4. Code by Zapier: validate the plan and format email

Run Javascript. Paste `zapier/02-validate-plan-and-format-email.js.txt` in full.
Map temperature (main.temp), description (weather[0].description), humidity
(main.humidity), wind (wind.speed), and observed_at (dt) from the Webhook, plus:

| Input Data key | Value |
|---|---|
| ai_response | Gemini's generated text response, not a whole response object |

The helper requires imperial units, rejects observations over three hours old or
over ten minutes in the future, and validates AI output before creating `subject`, `body`, `alert_subject`, and
`alert_body`. It also outputs a Boolean `alert_required` and both promo character
counts. Do not map AI text directly into Gmail around this check.

## 5. Gmail: regular plan

- Event: Send Email.
- To: your confirmed test inbox, entered directly.
- From name: Bayside Brews & Scoops.
- Subject: step 4 `subject`.
- Body type: Plain.
- Body: step 4 `body`.

Run this step only after confirming the recipient. Inspect the received email,
including weather values, headings, both promos, and observation time. A successful
Gmail action alone does not prove inbox receipt.

## 6. Filter by Zapier: optional alert

Continue only if step 4 `alert_required` **(Boolean) Is true**. This helper computes
the rubric's OR rule: temperature >91, description contains storm, or description
contains rain. Do not filter on AI-generated text or compare the Boolean to a
numeric temperature. Zapier's displayed field types should be confirmed in a test.

## 7. Gmail: alert

Same confirmed test inbox. Plain body. Map step 4 `alert_subject` and `alert_body`.
The daily email precedes this filter so normal days still get their plan.

## Testing and activation

1. Save redacted evidence of the real Postman, Webhook, Gemini, and inbox tests.
2. Use a draft copy with synthetic weather to test clear sky, 91, 91.1, rain, and
   storms. Keep observation timestamps current in synthetic cases.
3. Confirm the negative cases: malformed AI, a 120-character promo, and missing
   temperature stop before email. Do not weaken production checks to pass a test.
4. Restore real mappings and check both Gmail recipients before activation.
5. After activation, verify a scheduled run near 7 AM Miami time and inbox receipt.
6. Record what passed in `evidence/README.md`. Update the project status only after
   the evidence exists. Do not describe synthetic cases as live weather.

If an upstream step fails, review Zap history and perform the weather check
manually. Failure notification, automatic retries, deduplication, and independent
storm alerts are future enhancements. Do not enable recurring sends to someone
else's address without their authorization.
