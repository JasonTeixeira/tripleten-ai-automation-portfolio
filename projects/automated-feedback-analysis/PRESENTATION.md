# Presentation — slide content & spoken script

Full text for each slide (paste into Google Slides / PowerPoint), plus the spoken
script for a recorded demo. Open [`presentation.html`](presentation.html) for the
visual version.

---

### Slide 1 — Title
**Automated Customer Feedback Analysis**
Raw customer feedback in, structured real-time insight out. Nothing slips through,
and unhappy customers get caught the same day.
Tools: Google Forms · Make · Gemini 2.5 Flash · Google Sheets
Prepared by Jason Teixeira · Customer Success Manager (project scenario)

**Say:** "Hi, I'm Jason. For this project I played the role of a Customer Success
Manager and built an automated pipeline that reads customer feedback, scores it, and
files it, completely hands-off."

### Slide 2 — The problem
Feedback lands in a form and just sits there. Reading it by hand doesn't scale, two
people will grade the same message differently, and the angry responses are exactly the
ones you can't afford to miss for days.

**Say:** "The problem: feedback lands in a form and just sits there. Reading it by hand
doesn't scale, people grade the same message differently, and the responses that matter
most, the angry ones, are the ones you can't afford to sit on."

### Slide 3 — What I built
One form in, structured insight out, no manual steps. Collect (form) → Analyze (Gemini)
→ Store (Sheets) → Alert (email on negative).

**Say:** "Here's what I built. A customer fills out one short form. Behind the scenes an
AI model returns a sentiment label and a one-line summary, that lands in a spreadsheet
automatically, and if it's negative I get an email."

### Slide 4 — How it works (workflow diagram)
Google Forms (trigger) → Gemini 2.5 Flash (classify + summarize) → Parse JSON → Google
Sheets (add row) → Filtered email (only if Negative).
📸 *Screenshot: the full Make scenario canvas.*

**Say:** "This is the workflow in Make. Google Forms triggers it, Gemini analyzes the
message, a JSON step pulls out the two fields, Google Sheets stores the row, and a
filtered email fires only on negative feedback. No manual steps anywhere."

### Slide 5 — The AI part & prompt engineering
The starter prompt returned code-fenced text that broke the parser. I rewrote it to
demand raw JSON only, added an empty-feedback fallback, and set temperature to 0.2.
(See `prompt.txt`.)

**Say:** "The trickiest part was the AI output. The starter prompt kept wrapping its
answer in a code block, and sometimes added a sentence first, which broke the parser. I
rewrote it to demand only raw JSON, added a fallback for empty feedback, and set the
temperature low so ratings stay consistent. After that it parsed every time."

### Slide 6 — The output
Clean data in Sheets: Timestamp · Satisfaction · Feedback · Sentiment · Summary.
📸 *Screenshot: your real Google Sheet.*

**Say:** "Here's the output. One clean row per response, with sentiment and a summary.
This is my real sheet from the seven test submissions."

### Slide 7 — Insights
3 Positive · 2 Neutral · 2 Negative. Both negatives were about billing + account
reliability, which is a concrete thing to go fix.

**Say:** "The interesting insight wasn't the split. Both negatives were about the same
thing: billing and account reliability. So instead of 'people are unhappy' I get 'fix
the billing response time and the logout bug first.'"

### Slide 8 — Email alerts (optional)
Filter `sentiment = Negative` → email with summary + link to sheet.
📸 *Screenshot (optional): the alert email in your inbox.*

**Say:** "I also added the optional alert. Any negative response emails me instantly
with the summary and a link to the sheet. That turns a passive log into an early-warning
system."

### Slide 9 — What I'd improve
Slack alerts · topic tags · fallback logic for bad output · a live dashboard · priority
scoring for very-unsatisfied negatives.

**Say:** "With more time I'd route alerts into a Slack channel, have the AI tag a topic
category so I could trend it, add fallback logic for malformed output, and put a live
dashboard on top."

### Slide 10 — Links
Make blueprint: https://drive.google.com/file/d/1mFRXlwrmPMcy_1W7vSgARE3hg_QLvR9J/view?usp=sharing
Google Sheet: https://docs.google.com/spreadsheets/d/1L-kVnd12jnnij_LtLvnCo6Gdk9jjtZIxbvY9c5mPjNQ/edit?usp=sharing

**Say:** "And here are the links to my Make blueprint and the live sheet. Thanks for
reviewing."
