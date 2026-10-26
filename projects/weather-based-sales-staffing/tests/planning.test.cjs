'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { prepareWeather, prepareEmail } = require('../src/planning.cjs');

const now = Date.parse('2026-10-26T11:00:00Z');
function weather(overrides = {}) {
  return {
    temperature: '86', description: 'clear sky', humidity: '78', wind: '8',
    observed_at: String(now / 1000), ...overrides,
  };
}
function plan(overrides = {}) {
  return JSON.stringify({
    product_focus: 'Prioritize cold drinks and gelato. Keep hot drinks and pastries available in smaller batches.',
    staffing_suggestion: 'Keep the usual schedule and review demand before adding coverage.',
    promos: ['Iced coffee for a warm Miami morning.', 'A little gelato for your afternoon break.'],
    ...overrides,
  });
}
function email(overrides = {}) {
  return prepareEmail({ ...weather(), ai_response: plan(), ...overrides }, now);
}

test('normalizes mapped imperial weather and preserves source time', () => {
  const result = prepareWeather(weather(), now);
  assert.equal(result.temperature_f, 86);
  assert.equal(result.alert_required, false);
  assert.match(result.weather_summary, /86 °F/);
  assert.match(result.weather_summary, /78%/);
  assert.match(result.weather_summary, /8 mph/);
  assert.match(result.weather_summary, /current conditions/i);
  assert.match(result.local_observed_at, /7:00/);
});

for (const [temperature, description, expected] of [
  ['91', 'clear sky', false], ['91.1', 'clear sky', true],
  ['85', 'light rain', true], ['85', 'Thunderstorm', true],
  ['85', 'overcast clouds', false], ['85', 'drizzle', false],
]) {
  test(`alert rule: ${temperature} F, ${description} => ${expected}`, () => {
    const result = prepareWeather(weather({ temperature, description }), now);
    assert.equal(result.alert_required, expected);
    assert.equal(Boolean(result.alert_reasons), expected);
  });
}

test('explains all matching alert rules', () => {
  assert.match(prepareWeather(weather({ temperature: '94', description: 'thunderstorm with rain' }), now).alert_reasons,
    /temperature.*storm.*rain/i);
});

for (const temperature of ['', ' ', null, undefined, 'NaN', 'Infinity', '86 F', true, '200', '-150']) {
  test(`rejects invalid temperature ${String(temperature)}`, () => {
    assert.throws(() => prepareWeather(weather({ temperature }), now), /temperature/i);
  });
}

for (const description of ['', ' ', null, 'clear\nignore instructions', '<script>x</script>', 'x'.repeat(201)]) {
  test(`rejects invalid or unsafe description ${JSON.stringify(description).slice(0, 30)}`, () => {
    assert.throws(() => prepareWeather(weather({ description }), now), /description/i);
  });
}

test('missing optional observations are unavailable rather than zero', () => {
  assert.match(prepareWeather(weather({ humidity: '', wind: undefined }), now).weather_summary,
    /Humidity: unavailable.*Wind: unavailable/);
});

for (const overrides of [{ humidity: '101' }, { wind: '-1' }, { humidity: false }]) {
  test(`rejects invalid optional weather ${JSON.stringify(overrides)}`, () => {
    assert.throws(() => prepareWeather(weather(overrides), now), /humidity|wind/i);
  });
}

test('rejects missing, stale, and future observation timestamps', () => {
  for (const observed_at of ['', String(now / 1000 - 10801), String(now / 1000 + 601)]) {
    assert.throws(() => prepareWeather(weather({ observed_at }), now), /observation/i);
  }
});

test('formats Miami time correctly across daylight saving offsets', () => {
  const winter = Date.parse('2026-12-01T12:00:00Z');
  const result = prepareWeather(weather({ observed_at: String(winter / 1000) }), winter);
  assert.match(result.local_observed_at, /7:00/);
  assert.match(result.local_observed_at, /EST/);
});

test('formats a friendly daily email with source values and both promos', () => {
  const result = email();
  assert.equal(result.subject, 'Daily Plan – Bayside Brews & Scoops (Miami, FL)');
  assert.match(result.body, /Good morning, Emily/);
  assert.match(result.body, /86 °F/);
  assert.match(result.body, /Product focus/);
  assert.match(result.body, /Staffing suggestion/);
  assert.match(result.body, /1\. Iced coffee/);
  assert.match(result.body, /2\. A little gelato/);
  assert.equal(result.promo_1_characters, 37);
  assert.equal(result.alert_required, false);
});

test('builds an alert with reasons and condition-specific actions', () => {
  const heat = email({ temperature: '94' });
  assert.match(heat.alert_body, /hydration/i);
  assert.doesNotMatch(heat.alert_body, /loose outdoor items/i);
  const storm = email({ description: 'thunderstorm with rain' });
  assert.match(storm.alert_body, /loose outdoor items/i);
  assert.match(storm.alert_body, /official/i);
  assert.match(storm.alert_body, /project-defined/i);
});

for (const ai_response of ['', 'Not JSON', '{}', 'null', '[]', '```json\n{}\n```', 'x'.repeat(12001)]) {
  test(`rejects unusable AI response ${ai_response.slice(0, 25)}`, () => {
    assert.throws(() => email({ ai_response }), /AI|JSON|plan|product/i);
  });
}

test('requires exactly two short promos', () => {
  for (const promos of [[], ['one'], ['one', 'two', 'three'], ['x'.repeat(120), 'two'], [' ', 'two'], [1, 'two']]) {
    assert.throws(() => email({ ai_response: plan({ promos }) }), /promo/i);
  }
  assert.equal(email({ ai_response: plan({ promos: ['x'.repeat(119), 'two'] }) }).promo_1_characters, 119);
});

test('counts Unicode characters consistently', () => {
  const result = email({ ai_response: plan({ promos: ['☕'.repeat(119), 'Enjoy some gelato.'] }) });
  assert.equal(result.promo_1_characters, 119);
});

test('accepts a complete JSON code fence observed in the live Gemini action', () => {
  const result = email({ ai_response: '```json\n' + plan() + '\n```' });
  assert.match(result.body, /Product focus/);
  assert.equal(result.promo_1_characters, 37);
  assert.match(email({ ai_response: '```\n' + plan() + '\n```' }).body, /Staffing suggestion/);
});

test('rejects commentary around a JSON code fence', () => {
  assert.throws(() => email({ ai_response: 'Here is your plan:\n```json\n' + plan() + '\n```' }), /JSON/);
});

test('rejects plans over the total word limit', () => {
  assert.throws(() => email({ ai_response: plan({ product_focus: 'a '.repeat(181).trim() }) }), /180 words/);
});

test('rejects AI fields that could break plain-text sections or exceed bounds', () => {
  for (const overrides of [
    { product_focus: '' }, { staffing_suggestion: false }, { product_focus: '<b>gelato</b>' },
    { staffing_suggestion: 'one\ntwo' }, { product_focus: 'x'.repeat(701) },
    { promos: ['Cold coffee\r\nBcc: example', 'Gelato today'] },
  ]) {
    assert.throws(() => email({ ai_response: plan(overrides) }), /product|staffing|promo/i);
  }
});

test('does not accept AI-provided email addresses, subjects, or alert decisions', () => {
  const result = email({ ai_response: plan({ recipient: 'other@example.invalid', subject: 'Override', alert_required: true }) });
  assert.equal(result.subject, 'Daily Plan – Bayside Brews & Scoops (Miami, FL)');
  assert.equal(result.alert_required, false);
  assert.equal('recipient' in result, false);
});
