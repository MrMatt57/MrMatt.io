// Post-build script: generates public/_headers with auto-computed CSP script hashes.
// Run after `hugo --minify` to ensure hashes match the minified inline scripts.
//
// Usage: node scripts/generate-headers.js

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const TEMPLATE = path.join(__dirname, '..', '_headers.template');
const OUTPUT = path.join(PUBLIC_DIR, '_headers');

function findHtmlFiles(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...findHtmlFiles(full));
    } else if (entry.name.endsWith('.html')) {
      results.push(full);
    }
  }
  return results;
}

// Collect all unique inline <script> hashes (skip JSON-LD and empty scripts)
const hashes = new Set();
const scriptRegex = /<script>([\s\S]*?)<\/script>/g;

for (const file of findHtmlFiles(PUBLIC_DIR)) {
  const html = fs.readFileSync(file, 'utf8');
  let match;
  while ((match = scriptRegex.exec(html)) !== null) {
    const content = match[1];
    if (content.trim().length === 0) continue;
    const hash = crypto.createHash('sha256').update(content, 'utf8').digest('base64');
    hashes.add("'sha256-" + hash + "'");
  }
}

const hashList = [...hashes].sort().join(' ');

// Read template, replace placeholder, write output
const template = fs.readFileSync(TEMPLATE, 'utf8');
if (!template.includes('{{SCRIPT_HASHES}}')) {
  console.error('ERROR: _headers.template is missing {{SCRIPT_HASHES}} placeholder');
  process.exit(1);
}

const output = template.replace('{{SCRIPT_HASHES}}', hashList);
fs.writeFileSync(OUTPUT, output, 'utf8');

console.log('Generated public/_headers with ' + hashes.size + ' script hashes');
