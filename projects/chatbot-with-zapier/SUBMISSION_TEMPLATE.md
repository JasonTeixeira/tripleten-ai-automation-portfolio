# Creating a Chatbot with Zapier — Project Submission

**Name:** Jason Teixeira
**Sprint:** AI Tools and Prompt Engineering
**Live chatbot link:** https://triple-peaks-hotel-assistant-9fe415.zapier.app/
**Access:** Anyone with the link can view

---

## 1. Chatbot scenario chosen
I built the **Hotel Assistant** scenario: a chatbot named **Triple Peaks Hotel Assistant**
that answers common guest questions — check-in/check-out times, Wi-Fi, parking, amenities,
booking changes, and pet policy — using the provided **Triple Peaks Hotel Knowledge Base**
PDF as its sole knowledge source. Its purpose is to give guests fast, accurate, professional
answers and to hand off cleanly to the front desk for anything outside its scope.

**How it was configured**
- **Knowledge source:** Triple Peaks Hotel Knowledge Base PDF, uploaded and indexed in the
  Knowledge tab; the bot is set to answer only from this source.
- **Directive (system prompt):** instructs a professional, concise hospitality tone and
  requires every answer to come from the knowledge base (no invented details).
- **Fallback:** custom message for out-of-knowledge questions — the hotel's official
  fallback pointing to the front desk (123) 456-7890 / help@triplepeakshotel.com.

## 2. Setup screenshots
| Screenshot | File |
| --- | --- |
| Knowledge source uploaded + fallback configured | `screenshots/01-knowledge-source-uploaded.png` |
| Greeting + Directive (system prompt) | `screenshots/02-instructions-directive-greeting.png` |
| Published public link + access setting | `screenshots/09-published-public-link.png` |
| Live public chatbot page | `screenshots/10-live-public-page.png` |

## 3. Five tested conversations (all answered correctly from the PDF)
| # | Question asked | Chatbot answer (verbatim) | Screenshot |
| --- | --- | --- | --- |
| 1 | What time is check-in and check-out? | Check-in is at 3:00 PM, and check-out is at 11:00 AM. Early check-in and late check-out may be available upon request, subject to availability. | `screenshots/03-q1-checkin-checkout.png` |
| 2 | Do you offer free Wi-Fi? | Yes—complimentary high-speed Wi-Fi is available in all guest rooms and public areas. | `screenshots/04-q2-wifi.png` |
| 3 | Is parking available at the hotel? | Yes. Self-parking is $15 per day, and valet parking is $25 per day. Spaces are limited and available on a first-come, first-served basis. | `screenshots/05-q3-parking.png` |
| 4 | How can I modify or cancel my reservation? | You can modify or cancel your reservation through the confirmation email link, the hotel website, or by calling the front desk at (123) 456-7890. Free cancellation is available up to 24 hours before check-in; later cancellations or no-shows incur a one-night charge. | `screenshots/06-q4-booking-modify.png` |
| 5 | Are pets allowed at the hotel? | Yes! Dogs and cats are welcome—up to 2 pets per room, each weighing up to 50 lbs. The pet fee is $30 per stay, and pets must be leashed in public areas. | `screenshots/07-q5-pets.png` |

## 4. Fallback demonstration (question outside the knowledge base)
- **Question asked:** "Can you book me a flight to Denver?"
- **Chatbot response:** "I'm sorry, I don't have information on that. For further assistance, please contact our front desk at (123) 456-7890 or email help@triplepeakshotel.com."
- **Screenshot:** `screenshots/08-fallback-out-of-scope.png`

## 5. Public link
https://triple-peaks-hotel-assistant-9fe415.zapier.app/
