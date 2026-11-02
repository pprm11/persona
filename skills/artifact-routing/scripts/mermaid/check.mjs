// Parse every mermaid block of the given files with the real mermaid parser.
// Usage: node check.mjs FILE.md|FILE.html ...
// Reads ```mermaid fences (Markdown) and <pre class="mermaid"> blocks (HTML, text HTML-unescaped).
// A file with no block prints a warning; a file that mentions mermaid but yields no block fails (exit 1).
import { JSDOM } from 'jsdom';
import fs from 'fs';
const dom = new JSDOM('<!doctype html><body></body>');
globalThis.window = dom.window; globalThis.document = dom.window.document;
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });
globalThis.DOMParser = dom.window.DOMParser; globalThis.Element = dom.window.Element;
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false });

const FENCE = /```mermaid\n([\s\S]*?)```/g;
const PRE = /<pre\b[^>]*\bclass\s*=\s*(?:"[^"]*\bmermaid\b[^"]*"|'[^']*\bmermaid\b[^']*')[^>]*>([\s\S]*?)<\/pre\s*>/gi;

function unescapeHtml(s) {
  const named = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: '\u00a0' };
  return s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === '#') {
      const code = e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(code) ? String.fromCodePoint(code) : m;
    }
    return Object.prototype.hasOwnProperty.call(named, e.toLowerCase()) ? named[e.toLowerCase()] : m;
  });
}

export function blocksOf(file, raw) {
  const text = raw.split('\r\n').join('\n');
  const fences = [...text.matchAll(FENCE)].map(m => m[1]);
  const pres = [...text.matchAll(PRE)].map(m => unescapeHtml(m[1]).replace(/^\n+|\n+$/g, '') + '\n');
  if (/\.(md|markdown)$/i.test(file)) return fences;
  if (/\.html?$/i.test(file)) return pres;
  return pres.concat(fences);
}

const files = process.argv.slice(2);
if (!files.length) { console.error('Usage: node check.mjs FILE.md|FILE.html ...'); process.exit(2); }
let exit = 0;
for (const file of files) {
  const raw = fs.readFileSync(file, 'utf8');
  const blocks = blocksOf(file, raw);
  if (!blocks.length) {
    console.warn(`warning: no mermaid blocks found in ${file}`);
    if (/mermaid/i.test(raw)) { console.error(`error: ${file} mentions mermaid but no block matched (expected <pre class="mermaid"> or a \`\`\`mermaid fence)`); exit = 1; }
    continue;
  }
  let ok = 0; const bad = [];
  for (const [i, b] of blocks.entries()) { try { await mermaid.parse(b); ok++; } catch (e) { bad.push(i + 1); } }
  console.log(`${file}: ${ok}/${blocks.length} parse OK`, bad.length ? 'failed: ' + bad.join(',') : '');
  if (bad.length) exit = 1;
}
process.exit(exit);
