// Post-build script: generates public/_headers with auto-computed CSP hashes
// for inline <script> and <style> tags.
// Run after `hugo --minify` to ensure hashes match the minified output.
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

const scriptHashes = new Set();
const styleHashes = new Set();
const scriptRegex = /<script>([\s\S]*?)<\/script>/g;
const styleRegex = /<style>([\s\S]*?)<\/style>/g;

for (const file of findHtmlFiles(PUBLIC_DIR)) {
  const html = fs.readFileSync(file, 'utf8');
  let match;

  // Collect inline <script> hashes (skip empty scripts)
  while ((match = scriptRegex.exec(html)) !== null) {
    const content = match[1];
    if (content.trim().length === 0) continue;
    const hash = crypto.createHash('sha256').update(content, 'utf8').digest('base64');
    scriptHashes.add("'sha256-" + hash + "'");
  }

  // Collect inline <style> hashes (skip empty styles)
  while ((match = styleRegex.exec(html)) !== null) {
    const content = match[1];
    if (content.trim().length === 0) continue;
    const hash = crypto.createHash('sha256').update(content, 'utf8').digest('base64');
    styleHashes.add("'sha256-" + hash + "'");
  }
}

const scriptHashList = [...scriptHashes].sort().join(' ');
const styleHashList = [...styleHashes].sort().join(' ');

// Read template, replace placeholders, write output
const template = fs.readFileSync(TEMPLATE, 'utf8');
if (!template.includes('{{SCRIPT_HASHES}}')) {
  console.error('ERROR: _headers.template is missing {{SCRIPT_HASHES}} placeholder');
  process.exit(1);
}
if (!template.includes('{{STYLE_HASHES}}')) {
  console.error('ERROR: _headers.template is missing {{STYLE_HASHES}} placeholder');
  process.exit(1);
}

const output = template
  .replace('{{SCRIPT_HASHES}}', scriptHashList)
  .replace('{{STYLE_HASHES}}', styleHashList);
fs.writeFileSync(OUTPUT, output, 'utf8');

console.log('Generated public/_headers with ' + scriptHashes.size + ' script hashes and ' + styleHashes.size + ' style hashes');
