#!/usr/bin/env node
// expand-config.js
// Usage: node expand-config.js input.json [output.json]
const fs = require('fs');
const path = require('path');

function expandEnv(obj) {
  if (typeof obj === 'string') {
    return obj.replace(/\$\{([A-Z0-9_]+)\}/g, (_, v) => process.env[v] || obj);
  } else if (Array.isArray(obj)) {
    return obj.map(expandEnv);
  } else if (typeof obj === 'object' && obj !== null) {
    const out = {};
    for (const k in obj) out[k] = expandEnv(obj[k]);
    return out;
  }
  return obj;
}

const input = process.argv[2];
const output = process.argv[3];
if (!input) {
  console.error('Usage: node expand-config.js input.json [output.json]');
  process.exit(1);
}
const raw = fs.readFileSync(input, 'utf8');
const expanded = expandEnv(JSON.parse(raw));
if (output) {
  fs.writeFileSync(output, JSON.stringify(expanded, null, 2));
  console.log('Expanded config written to', output);
} else {
  console.log(JSON.stringify(expanded, null, 2));
} 