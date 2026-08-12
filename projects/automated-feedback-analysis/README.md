# Automated Customer Feedback Analysis

An automated pipeline that collects customer feedback, analyzes it with AI, and turns
it into structured, real-time insight — with no manual steps.

Built for the scenario of a **Customer Success Manager** at a small online business who
needs to collect, analyze, and act on feedback fast enough to keep customers happy and
catch problems before they escalate.

## Overview (one-paragraph description)

A Google Form collects a satisfaction rating and a free-text comment. A Make scenario
then sends the comment to **Gemini 2.5 Flash**, which returns a sentiment classification
(Positive, Neutral, or Negative) and a one-sentence summary in a strict JSON format. A
JSON-parsing step extracts those fields, **Google Sheets** logs every response with a
timestamp, and a filter emails an instant alert whenever feedback is negative — so
unhappy customers are caught the same day instead of days later. The whole pipeline runs
hands-off from a single form submission, turning unstructured feedback into a clean,
analyzable log and a real-time early-warning system.

## Tools

- **Google Forms** — collects feedback
- **Make** — automates the flow
- **Gemini 2.5 Flash** — classifies sentiment and summarizes the message
- **Google Sheets** — stores the structured data
- **Gmail (via Make)** — sends the negative-feedback alert

## How the automation works

This workflow runs entirely on its own — one form submission is all it takes, and the
insight files itself with no manual steps.

When a customer submits the **Google Form** (a satisfaction rating plus a free-text
comment), that submission triggers a **Make scenario**. Make passes the comment to
**Gemini 2.5 Flash**, which reads the message and returns two things in a strict JSON
format: a **sentiment** label (Positive, Neutral, or Negative) and a **one-sentence
summary**. A **JSON parsing** step then pulls those two fields out of the AI's response.
Next, **Google Sheets** adds a new row containing the timestamp, satisfaction rating,
original feedback, sentiment, and summary — a clean, analyzable log. Finally, a
**filter** checks the sentiment: if it's Negative, Make sends an **email alert** with the
summary and a link to the sheet.

The one part that took real work was the AI output. The initial prompt returned the right
information but kept wrapping it in a Markdown code block and occasionally added a
sentence before it — which broke the parser. I rewrote the prompt to force *only* raw
JSON (no fences, no extra text), added a fallback for empty feedback, and lowered the
model temperature to `0.2` so the classifications stay consistent. After that, every
response parsed cleanly.

### Workflow diagram

```
  Google Form  ──(new response)──►  Make scenario (auto-triggered)
                                          │
                                          ▼
                                  Gemini 2.5 Flash
                                (sentiment + summary → JSON)
                                          │
                                          ▼
                                    Parse JSON
                                (extract 2 fields)
                                          │
                                          ▼
                                  Google Sheets
                    (row: timestamp · satisfaction · feedback ·
                              sentiment · summary)
                                          │
                              ┌───────────┴───────────┐
                      sentiment = Negative?     everything else
                              │                        │
                              ▼                      (done)
                        Email alert to me
                    (summary + link to sheet)
```

## Repository contents

| File | What it is |
| --- | --- |
| [`Automated-Feedback-Analysis-Jason-Teixeira.pptx`](Automated-Feedback-Analysis-Jason-Teixeira.pptx) | The 10-slide presentation (PowerPoint — imports into Google Slides). |
| [`presentation.html`](presentation.html) | The same deck as a web page (open in a browser). |
| [`PRESENTATION.md`](PRESENTATION.md) | The full slide content + a spoken demo script. |
| [`prompt.txt`](prompt.txt) | The exact Gemini prompt used in the Make module. |
| [`test-data.csv`](test-data.csv) | The 7 test responses and their expected AI output. |
| [`assets/`](assets/) | Screenshots (workflow canvas, sheet, alert email). |

## Insights from the test run

Across 7 test submissions the split was **3 Positive · 2 Neutral · 2 Negative**. The
useful part wasn't the split — it was the pattern in the negatives: both unhappy customers
were describing the same class of problem, **billing and account reliability** (a
double-charge with no reply, and repeated forced logouts). That's a concrete,
prioritizable signal, not just "people are unhappy."

## What I'd improve with more time and tools

- **Route alerts to Slack**, not just email — post negatives into a `#customer-alerts`
  channel so the whole team sees them, with a reaction to mark who's handling each one.
- **Add a topic tag** — extend the prompt so the AI also returns a category (billing,
  shipping, bug, praise), turning the sheet from something you read into something you can
  filter and trend.
- **Fallback logic** — if Gemini ever returns malformed JSON, catch it and write
  "needs review" instead of letting the scenario error out.
- **A live dashboard** — a Looker Studio chart on top of the sheet showing sentiment over
  time, so trends are visible at a glance.
- **Priority scoring** — flag responses that are both "Very unsatisfied" and Negative as
  high-priority, so the loudest alarms rise to the top.

## Submission links

> Replace the placeholders below with your own links after building the scenario.

- **Make scenario blueprint:** `TODO — export via ⋯ → Export blueprint, upload to Drive, share "anyone with link can view", paste URL here`
- **Google Sheet (test data):** `TODO — share "anyone with link can view", paste URL here`
- **Google Slides (if used):** `TODO — paste URL here`

---

Author: **Jason Teixeira** · TripleTen AI Automation program
