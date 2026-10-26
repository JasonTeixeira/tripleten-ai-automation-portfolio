'use strict';
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'src/planning.cjs'), 'utf8')
  .replace('module.exports = { prepareWeather, prepareEmail };', '');
for (const [name, fn] of [['01-validate-weather.js.txt', 'prepareWeather'], ['02-validate-plan-and-format-email.js.txt', 'prepareEmail']]) {
  const generated = `${source}\nreturn ${fn}(inputData);\n`;
  // Compile the exact code to paste into Code by Zapier, including its return.
  new Function('inputData', generated);
  fs.writeFileSync(path.join(root, 'zapier', name), generated);
}
console.log('Built and syntax-checked both Code by Zapier scripts.');
