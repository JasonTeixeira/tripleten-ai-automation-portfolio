# Automated Customer Feedback Analysis

An automated pipeline that collects customer feedback, runs it through AI, and turns it
into structured insight in real time. No manual steps anywhere.

The scenario: I'm a Customer Success Manager at a small online business. Feedback comes
in faster than anyone can read it, and the angry messages are the ones you can't afford
to sit on for days.

## Overview

A Google Form collects a satisfaction rating and a free-text comment. When a response
comes in, a Make scenario sends the comment to **Gemini 2.5 Flash**, which returns a
sentiment label (Positive, Neutral, or Negative) plus a one-sentence summary in a strict
JSON format. A JSON parsing step pulls out those two fields, **Google Sheets** logs the
full response with a timestamp, and if the sentiment is Negative, a filter fires off an
email alert so the unhappy customer gets caught the same day instead of whenever someone
next opens the spreadsheet. One form submission is all it takes.

## Tools

- **Google Forms** — collects feedback
- **Make** — automates the flow
- **Gemini 2.5 Flash** — classifies sentiment and summarizes the message
- **Google Sheets** — stores the structured data
- **Gmail (via Make)** — sends the negative-feedback alert

## How the automation works

A customer submits the Google Form (a satisfaction rating and a free-text comment).
That submission triggers the Make scenario. Make hands the comment to Gemini 2.5 Flash,
which reads it and returns two things in strict JSON: a sentiment label and a
one-sentence summary. A JSON parsing step extracts both fields. Google Sheets then adds
a new row with the timestamp, satisfaction rating, original feedback, sentiment, and
summary. Last step is a filter that checks the sentiment: if it's Negative, Make sends
me an email with the summary and a link to the sheet.

The part that took real work was the AI output. The starter prompt returned the right
information but kept wrapping it in a Markdown code block, and every so often it added a
sentence before the JSON. Both of those broke the parser. I rewrote the prompt to demand
raw JSON only, with nothing before or after it, added a fallback for empty feedback, and
dropped the model temperature to `0.2`. One more issue showed up in testing: a borderline
comment ("packaging was excessive") flip-flopped between Neutral and Negative across
runs. Adding explicit classification rules to the prompt fixed it — mild gripes stay
Neutral, and Negative is reserved for real problems that need action. After that, every
response parsed cleanly and classified the same way on every run.

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

Across 7 test submissions the split came out **3 Positive · 2 Neutral · 2 Negative**.
The split itself isn't the interesting part. What stood out is that both negatives
described the same class of problem: billing and account reliability (a double-charge
with no reply, and repeated forced logouts). That's something a team can actually
prioritize, not just a vague "some customers are unhappy."

## What I'd improve with more time and tools

- **Slack alerts** — post negatives into a `#customer-alerts` channel instead of just
  email, so the whole team sees them and someone can claim each one with a reaction.
- **Topic tags** — extend the prompt so the AI also returns a category (billing,
  shipping, bug, praise). The sheet goes from something you read to something you can
  filter and trend.
- **Fallback logic** — if Gemini ever returns malformed JSON, catch it and log the row
  as "needs review" rather than letting the scenario error out.
- **A live dashboard** — a Looker Studio chart on top of the sheet showing sentiment
  over time.
- **Priority scoring** — anything that's both "Very unsatisfied" and Negative gets
  flagged high-priority, so the loudest alarms rise to the top.

## Submission links

- **Make scenario blueprint (Drive, view-only):** https://drive.google.com/file/d/1mFRXlwrmPMcy_1W7vSgARE3hg_QLvR9J/view?usp=sharing (also in [`assets/blueprint.json`](assets/blueprint.json))
- **Google Sheet (live test data, view-only):** https://docs.google.com/spreadsheets/d/1L-kVnd12jnnij_LtLvnCo6Gdk9jjtZIxbvY9c5mPjNQ/edit?usp=sharing
- **Google Slides:** https://docs.google.com/presentation/d/1m3MkKktEcnunVZ3gSGPlA_2q3-LNyqh0MEEzUg_8koM/edit?usp=sharing

---

Author: **Jason Teixeira** · TripleTen AI Automation program
