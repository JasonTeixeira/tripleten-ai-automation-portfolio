'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { prepareEmail } = require('../src/planning.cjs');
const now = Date.parse('2026-10-26T11:00:00Z');
const input = {
  temperature: '86', description: 'scattered clouds', humidity: '78', wind: '8',
  observed_at: String(now / 1000),
  ai_response: JSON.stringify({
    product_focus: 'Put cold drinks and gelato first for this warm, humid morning. Keep hot drinks available and prepare pastries in smaller batches.',
    staffing_suggestion: 'Keep the usual schedule. Review the afternoon forecast and early sales before asking one extra person to cover a busier period.',
    promos: ['Warm morning? Make it an iced coffee kind of day.', 'A little scoop of happiness from Bayside Brews & Scoops.'],
  }),
};
const daily = prepareEmail(input, now);
const alert = prepareEmail({ ...input, temperature: '94', description: 'thunderstorm with rain' }, now);
const root = path.resolve(__dirname, '..');
fs.writeFileSync(path.join(root, 'templates/sample-daily-email.txt'),
  `SIMULATED EXAMPLE: hand-authored plan and synthetic weather. No API call or email delivery.\n\nSubject: ${daily.subject}\n\n${daily.body}\n`);
fs.writeFileSync(path.join(root, 'templates/sample-alert-email.txt'),
  `SIMULATED EXAMPLE: synthetic heat and storm scenario. No email delivery.\n\nSubject: ${alert.alert_subject}\n\n${alert.alert_body}\n`);
console.log('Created two clearly labeled local email examples. Nothing sent.');
