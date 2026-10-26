'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
execFileSync(process.execPath, [path.resolve(__dirname, '../scripts/build.cjs')]);
const run = (filename, input) => new Function('inputData', fs.readFileSync(path.resolve(__dirname, '../zapier', filename), 'utf8'))(input);
const weather = () => ({ temperature: '94', description: 'clear sky', observed_at: String(Date.now() / 1000) });
test('generated weather Code step returns fields Zapier can map', () => {
  assert.equal(run('01-validate-weather.js.txt', weather()).alert_required, true);
});
test('generated email Code step returns fixed subjects and a valid plan', () => {
  const result = run('02-validate-plan-and-format-email.js.txt', {
    ...weather(), ai_response: JSON.stringify({ product_focus: 'Focus on cold drinks and gelato, with hot drinks and pastries available.',
      staffing_suggestion: 'Keep the usual coverage and review early demand.', promos: ['Iced coffee today.', 'A scoop for your break.'] }),
  });
  assert.match(result.body, /94 °F/);
  assert.equal(result.alert_required, true);
});
test('generated email step rejects invalid AI before Gmail can run', () => {
  assert.throws(() => run('02-validate-plan-and-format-email.js.txt', { ...weather(), ai_response: '{}' }), /product focus/);
});
