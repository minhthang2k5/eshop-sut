// Read-only summary; excludes login from action metrics. CSV is parsed with quoted fields.
const fs = require('node:fs');
const input = process.argv[2];
if (!input) throw new Error('Usage: node summarize.cjs path/to/baseline.jtl');
function csv(text) {
  const rows = []; let row = [], field = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (quoted && text[i + 1] === '"') { field += '"'; i++; }
      else quoted = !quoted;
    } else if (c === ',' && !quoted) { row.push(field); field = ''; }
    else if (c === '\n' && !quoted) {
      row.push(field.replace(/\r$/, '')); rows.push(row); row = []; field = '';
    } else field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  if (quoted) throw new Error('Unterminated quoted CSV field');
  return rows;
}
const [header, ...lines] = csv(fs.readFileSync(input, 'utf8'));
const samples = lines.filter(r => r.length === header.length).map(r => Object.fromEntries(header.map((h, i) => [h, r[i]])));
if (!samples.length) throw new Error('No samples');
const actionLabels = ['search', 'detail', 'checkout'];
const actions = samples.filter(r => actionLabels.includes(r.label));
function metrics(rows) {
  if (!rows.length) return { count: 0 };
  const elapsed = rows.map(r => Number(r.elapsed)).sort((a, b) => a - b);
  const percentile = p => elapsed[Math.ceil(p * elapsed.length) - 1];
  const errors = rows.filter(r => r.success !== 'true').length;
  const span = (Math.max(...rows.map(r => Number(r.timeStamp) + Number(r.elapsed))) - Math.min(...rows.map(r => Number(r.timeStamp)))) / 1000;
  return { count: rows.length, errors, errorPct: Number((100 * errors / rows.length).toFixed(4)), p50: percentile(.5), p95: percentile(.95), p99: percentile(.99), throughputPerSecond: Number((rows.length / span).toFixed(3)), observedSpanSeconds: Number(span.toFixed(3)) };
}
const summary = { percentileMethod: 'nearest rank on elapsed milliseconds, all samples including failures', all: metrics(samples), actions: metrics(actions), byLabel: Object.fromEntries(['login', ...actionLabels].map(label => [label, { ...metrics(samples.filter(r => r.label === label)), ...(actionLabels.includes(label) ? { actionSharePct: Number((100 * samples.filter(r => r.label === label).length / actions.length).toFixed(3)) } : {}) }])) };
summary.slo = { p95Below500ms: summary.actions.p95 < 500, errorsBelow1pct: summary.actions.errorPct < 1 };
console.log(JSON.stringify(summary, null, 2));
