# Creating a Chatbot with Zapier — Project Submission

**Name:** Jason Teixeira
**Sprint:** AI Tools and Prompt Engineering
**Scenario:** Hotel assistant · **Built with:** Zapier Chatbots

### 🔗 Public link to the live chatbot
**https://triple-peaks-hotel-assistant-9fe415.zapier.app/**
*Access: Anyone with the link can view.*

📄 A combined, ready-to-print version of this submission is also available here:
[`Jason_Teixeira_Chatbot_with_Zapier.pdf`](Jason_Teixeira_Chatbot_with_Zapier.pdf)

---

## 1. Chatbot scenario chosen
I built the **Hotel Assistant** scenario: a chatbot named **Triple Peaks Hotel Assistant**
that answers common guest questions — check-in/check-out times, Wi-Fi, parking, amenities,
booking changes, and pet policy — using the provided **Triple Peaks Hotel Knowledge Base**
PDF as its sole knowledge source. Its purpose is to give guests fast, accurate, professional
answers around the clock and to hand off cleanly to the front desk for anything outside its
scope.

**How it was configured**
- **Knowledge source:** the Triple Peaks Hotel FAQ PDF was uploaded and indexed; the chatbot
  is set to answer *only* from this source.
- **Directive (system prompt):** sets a professional, concise, conversational hospitality
  tone and requires every answer to come from the knowledge base (no invented details).
- **Fallback:** a custom message for out-of-knowledge questions — the hotel's official
  fallback pointing guests to the front desk at (123) 456-7890 or help@triplepeakshotel.com.

---

## 2. Setup screenshots (knowledge base + directive)

**Knowledge source uploaded** — Triple Peaks Hotel Knowledge Base PDF indexed, with the
custom fallback configured (respond with a custom message when no answer is found):

![Knowledge source uploaded](screenshots/01-knowledge-source-uploaded.png)

**Directive (system prompt) and welcome/greeting message:**

![Directive and greeting](screenshots/02-instructions-directive-greeting.png)

**Published — public link with access set to "Anyone with the link can view":**

![Published public link](screenshots/09-published-public-link.png)

---

## 3. Five tested conversations
All answers are drawn directly from the uploaded knowledge base.

**Q1 — What time is check-in and check-out?**
> Check-in is at 3:00 PM, and check-out is at 11:00 AM. Early check-in and late check-out may be available upon request, subject to availability.

![Q1 check-in check-out](screenshots/03-q1-checkin-checkout.png)

**Q2 — Do you offer free Wi-Fi?**
> Yes — complimentary high-speed Wi-Fi is available in all guest rooms and public areas.

![Q2 wifi](screenshots/04-q2-wifi.png)

**Q3 — Is parking available at the hotel?**
> Yes. Self-parking is $15 per day, and valet parking is $25 per day. Spaces are limited and available on a first-come, first-served basis.

![Q3 parking](screenshots/05-q3-parking.png)

**Q4 — How can I modify or cancel my reservation?**
> You can modify or cancel your reservation through the confirmation email link, the hotel website, or by calling the front desk at (123) 456-7890. Free cancellation is available up to 24 hours before check-in; later cancellations or no-shows incur a one-night charge.

![Q4 booking modify](screenshots/06-q4-booking-modify.png)

**Q5 — Are pets allowed at the hotel?**
> Yes! Dogs and cats are welcome — up to 2 pets per room, each weighing up to 50 lbs. The pet fee is $30 per stay, and pets must be leashed in public areas.

![Q5 pets](screenshots/07-q5-pets.png)

---

## 4. Fallback demonstration (question outside the knowledge base)

**Question asked:** *"Can you book me a flight to Denver?"*
> I'm sorry, I don't have information on that. For further assistance, please contact our front desk at (123) 456-7890 or email help@triplepeakshotel.com.

![Fallback out of scope](screenshots/08-fallback-out-of-scope.png)

---

## 5. Live chatbot — public link

**https://triple-peaks-hotel-assistant-9fe415.zapier.app/**

Verified working in a logged-out public session (what a reviewer sees):

![Live public page](screenshots/10-live-public-page.png)

Live verification with a brand-new question (breakfast hours), answered correctly from the PDF:

![Live verification breakfast](screenshots/11-live-verification-breakfast.png)

---

## Submission checklist — coverage
| Required item | Where it is |
| --- | --- |
| Short explanation of scenario chosen | Section 1 |
| Setup screenshots (uploaded knowledge base + directive) | Section 2 |
| Screenshots of ≥5 different conversations | Section 3 (5 Q&A) + Section 4 (fallback) |
| Public link to live chatbot | Top of page + Section 5 |
