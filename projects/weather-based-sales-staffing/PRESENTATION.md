# Presentation copy aligned to the supplied template

Author: Jason Teixeira. This file contains draft copy, not a completed slide deck.
Keep the supplied template's design. Delete the instructions slide and unused
assets before submitting. Add actual screenshots after live testing. Do not turn
the sample email files into images that appear to prove inbox delivery.

## Title

**Automation of Weather-Based Sales and Staffing Decisions**

Bayside Brews & Scoops, Miami, Florida

Jason Teixeira

Speaker notes: The goal is to give Emily a useful morning starting point before
the kiosk gets busy. Weather informs the suggestions, and she keeps the final say.

## Problem

**Morning preparation depends on a manual weather check**

Emily checks Miami's weather before deciding what to prepare and whether to
adjust coverage. Heat can shift attention toward cold drinks and gelato. Rain
or coastal wind may change beach traffic. Checking everything manually adds
another task to opening the kiosk.

Speaker notes: These are planning assumptions from the project brief. I would
need the kiosk's sales history to measure how strongly weather affects demand.

## Solution

**A daily plan in Emily's inbox**

At 7 AM Miami time, Zapier retrieves current conditions from OpenWeather.
Gemini suggests product priorities, a staffing adjustment if needed, and two
short customer messages. Validation checks the response before Gmail sends it.

Speaker notes: The provided endpoint returns current conditions. I keep that
distinction clear instead of presenting a morning observation as an afternoon
forecast. The live schedule and delivery still need verification.

## Workflow diagram

**The morning workflow**

Show the diagram from README.md or the actual Zap canvas. Include the weather
validation and AI-output validation steps. Put the optional weather filter after
the daily email.

Speaker notes: The core apps follow the assignment. The one combined validation and formatting Code step help
prevent missing or malformed data from reaching Emily. The filter adds a second
email only when the weather meets our alert rule.

## Workflow in action

**Weather, prompt, and received email**

Use at least three readable screenshots:

1. A successful Postman or Webhook response, with API key hidden.
2. The Gemini prompt and generated JSON.
3. The received daily email with matching weather values.

Split this slide into two if the screenshots would be too small. Include the full
prompt in an appendix or link to `prompt.txt` in the repository.

Speaker notes: Once tested, explain the observed values and trace them across the
screenshots. Until then, this is an evidence collection plan, not a test result.

## Benefits

**A clearer starting point for the manager**

- Emily receives one summary instead of assembling it across separate apps.
- Product advice connects directly to the weather observation.
- Both promo messages are ready for review and stay under 120 characters.
- Staffing advice leaves the final decision with the person running the kiosk.

Speaker notes: The intended benefit is simpler morning preparation. I have not
measured time savings, sales increases, or reduced waste.

## Optional extras

**Heat, rain, and storm alerts**

The alert rule checks temperature above 91°F, or a description containing
“storm” or “rain.” Code calculates the result so a different AI wording cannot
change whether the rule triggers. The regular morning plan still goes out first.

Speaker notes: The rule follows the rubric, including light rain. It is an
operational flag rather than an official severe-weather warning. Add a real
received alert screenshot after a clearly labeled synthetic trigger test.

## Challenges & improvements

**What still needs a stronger signal**

The morning observation cannot predict the whole day. A useful next step is to
add the remaining same-day forecast intervals, then compare recommendations
with actual sales and stock. I would also give alerts an independent route so
a failed AI step cannot block them.

Speaker notes: Local tests cover alert boundaries, malformed responses, missing
data, and promo length. They do not prove live API access or inbox delivery.
Update this reflection with the actual build experience after live testing.

## Optional repository slide

**Project files and testing**

Repository: https://github.com/JasonTeixeira/tripleten-ai-automation-portfolio

Project folder: `projects/weather-based-sales-staffing/`

The repository contains the exact prompt, request, setup guide, validation
source, and local test commands. Add a direct project-folder link only after
publishing the folder to the submitted branch. Add the final Google Slides URL
to SUBMISSION.md after preparing the deck.
