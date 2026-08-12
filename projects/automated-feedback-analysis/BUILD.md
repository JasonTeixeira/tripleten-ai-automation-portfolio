# Build guide — do this once (~15 min)

Everything else in this folder is ready. These are the only steps that must happen
in your own accounts, because they produce the real proof a reviewer checks.

## Step 1 — Google Form (2 min)
1. Go to **forms.google.com** → **Blank form**.
2. Question 1 → **Multiple choice**, title:
   *"How satisfied are you with our product or service?"*
   Options: `Very satisfied` · `Satisfied` · `Neutral` · `Unsatisfied` · `Very unsatisfied`
3. Question 2 → **Paragraph**, title:
   *"Please describe your experience or share any feedback in your own words."*
4. **Send** → copy the link → submit the **7 responses in `test-data.csv`**.

## Step 2 — Make scenario (8 min)
Go to **make.com** → **Create a new scenario**. Add these 5 modules, left to right,
connecting each to the next:

1. **Google Forms → Watch Responses** — connect your Google account, choose your form.
   *(This is the trigger.)*
2. **Google Gemini AI → Create a Completion**
   - Model: `gemini-2.5-flash`
   - Prompt: paste the contents of **`prompt.txt`**, and map the Q2 (paragraph) field
     into the `{{feedback}}` spot.
   - Temperature: `0.2`
3. **JSON → Parse JSON**
   - JSON string: the **text/result** output from the Gemini module.
   - Data structure: two fields — `sentiment` (text), `summary` (text).
4. **Google Sheets → Add a Row**
   - Create/select a sheet with columns:
     `Timestamp · Satisfaction · Feedback · Sentiment · Summary`
   - Map: Timestamp = `{{now}}`, Satisfaction = Q1, Feedback = Q2,
     Sentiment = `{{sentiment}}`, Summary = `{{summary}}`.
5. **Router / Filter → Gmail (or Email) → Send an Email**
   - Filter: `sentiment` **Equal to** `Negative`.
   - To: your email. Subject: `⚠️ Negative feedback just came in`.
     Body: `{{summary}}` + a link to the sheet.

Click **Run once**, submit one test form, and watch the data flow through. Then toggle
scheduling **ON** (bottom-left) so it runs automatically.

## Step 3 — Screenshots (2 min)
Save these into `assets/`:
- `workflow.png` — the whole Make canvas with all 5 modules connected
- `sheet.png` — the Google Sheet with the columns filled in
- `alert-email.png` — (optional) the alert email in your inbox

## Step 4 — Export + links (3 min)
1. In Make: scenario **⋯ (More) → Export blueprint** → downloads a `.json`.
   Put it in `assets/blueprint.json` (or upload to Drive).
2. Share the **Make blueprint** (Drive file) and the **Google Sheet** as
   *"Anyone with the link can view."*
3. Paste both links into `README.md` (Submission links section) **and** on the last
   slide of the deck.

## Step 5 — Commit
```bash
cd ~/code/active/tripleten-ai-automation-portfolio
git add -A
git commit -m "Add blueprint, sheet link, and screenshots"
git push
```

Done — that completes every rubric row.
