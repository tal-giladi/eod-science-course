// Validate every $...$ / $$...$$ segment in the course with KaTeX (same tokenizer as index.html).
// Usage: npm i katex@0.16.9 (anywhere on NODE_PATH) ; node scripts/check_math.js
const katex = require('katex'), fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const files = [];
(function walk(d) {
  for (const f of fs.readdirSync(d)) {
    if (['.git', 'research', 'node_modules', '.claude'].includes(f)) continue;
    const p = path.join(d, f), st = fs.statSync(p);
    if (st.isDirectory()) walk(p); else if (p.endsWith('.md')) files.push(p);
  }
})(root);
const TOKEN = /(```[\s\S]*?```|~~~[\s\S]*?~~~)|(`[^`\n]*`)|(\$\$[\s\S]+?\$\$)|(\$(?!\s)[^$\n]+?(?<![\s\\])\$)/g;
let errs = 0, n = 0;
for (const f of files) {
  const t = fs.readFileSync(f, 'utf8'); let m;
  while ((m = TOKEN.exec(t))) {
    if (m[1] || m[2]) continue;
    const disp = !!m[3], src = disp ? m[3].slice(2, -2) : m[4].slice(1, -1); n++;
    try { katex.renderToString(src, { displayMode: disp, throwOnError: true, strict: false }); }
    catch (e) { errs++; console.log(path.relative(root, f) + ': ' + e.message.split('\n')[0].slice(0, 120) + ' | ' + src.slice(0, 90).replace(/\n/g, ' ')); }
  }
}
console.log('math segments', n, 'errors', errs);
process.exit(errs ? 1 : 0);
