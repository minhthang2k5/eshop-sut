import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { scanSource } from './rules.js';
import { smokeEvidence } from './runner.js';

const sample = (name) => fs.readFile(new URL(`../../samples/${name}`, import.meta.url), 'utf8');
const criterion = (source, id) => scanSource(source).find((row) => row.criterionId === id);

for (const name of ['chatgpt_script_good.js', 'gemini_script_real.js', 'claude_scipt_real.js']) {
  test(`recognizes valid source patterns: ${name}`, async () => {
    assert.deepEqual(scanSource(await sample(name)).map((row) => row.pass), Array(9).fill(true));
  });
}

test('intentional error sample stays rejected and comments cannot satisfy rules', async () => {
  const bad = await sample('claude_script_with_errors.js');
  assert.equal(criterion(bad, 4).pass, false);
  assert.equal(criterion(`${bad}\n/* Math.random(); 0.55 0.80 token orderId status === 200 */`, 6).pass, false);
  assert.equal(criterion(`${bad}\n/* check(response, { token: r => true, orderId: r => true }) */`, 8).pass, false);
});

test('rejects real regressions instead of accepting names and literal hints', async () => {
  const source = await sample('gemini_script_real.js');
  const mutations = [
    [source.replace('/api/checkout', '/api/orders'), 1],
    [source.replace('http.post(`${BASE_URL}/api/checkout`', 'http.get(`${BASE_URL}/api/checkout`'), 2],
    [source.replace('total_amount: 30000000', 'wrong_field: 30000000'), 2],
    [source.replace("'Authorization':", "'token':"), 4],
    [source.replace('const token = loginJson.token;', "const token = 'hardcoded';"), 4],
    [source.replace('const token = loginJson.token;', 'const token = loginJson.accessToken;'), 4],
    [source.replace('rand < 0.80', 'rand < 0.90'), 6],
    [source.replace('getRandomInt(1, 5)', 'getRandomInt(1, 8)'), 7],
    [source.replace('getRandomInt(1, 5)', '1'), 7],
    [source.replace('getRandomElement(SEARCH_KEYWORDS)', "'iPhone'"), 7],
    [source.replace('sleep(getRandomFloat(1, 3))', 'sleep(2)'), 5],
    [source.replace('sleep(getRandomFloat(2, 5))', 'sleep(getRandomFloat(2, 9))'), 5],
    [source.replace("'checkout orderId exists': () => checkoutJson !== null && checkoutJson.orderId !== undefined && checkoutJson.orderId !== null,", ''), 8],
    [source.replace('if (!loginSuccess || !loginJson || !loginJson.token)', 'if (loginSuccess && loginJson && loginJson.token)'), 3],
    [source.replace("http_req_duration: ['p(95)<500']", "unused_metric: ['p(95)<500']"), 9]
  ];
  for (const [mutant, id] of mutations) assert.equal(criterion(mutant, id).pass, false, `criterion ${id}`);
});

test('unknown patterns and syntax errors are explained for manual review', () => {
  assert.equal(criterion('export default function () {}', 4).reviewRequired, true);
  assert.match(criterion('export default function (', 1).message, /JavaScript/);
});

function flat() {
  return { exitCode: 0, timedOut: false, log: '', summary: { metrics: {
    checks: { value: 1, passes: 3, fails: 0 },
    http_req_failed: { value: 0 },
    http_req_duration: { 'p(95)': 85 },
    http_reqs: { count: 2 }
  } } };
}

test('reads flat summary-export metrics including p95', () => {
  const evidence = smokeEvidence(flat());
  assert.equal(evidence.pass, true);
  assert.equal(evidence.checksRate, 1);
  assert.equal(evidence.failedRequestRate, 0);
  assert.equal(evidence.p95Ms, 85);
  assert.equal(evidence.requestCount, 2);
});

test('reads nested handleSummary metrics', () => {
  const result = flat();
  result.summary.metrics = { checks: { values: { rate: 1, passes: 3, fails: 0 } }, http_req_failed: { values: { rate: 0 } }, http_req_duration: { values: { 'p(95)': 70 } }, http_reqs: { values: { count: 2 } } };
  assert.equal(smokeEvidence(result).pass, true);
  assert.equal(smokeEvidence(result).p95Ms, 70);
});

test('exit zero does not hide check/HTTP failures', () => {
  for (const mutate of [
    (r) => { r.summary.metrics.checks = { value: 0, passes: 0, fails: 2 }; },
    (r) => { r.summary.metrics.http_req_failed.value = 1; }
  ]) { const result = flat(); mutate(result); assert.equal(smokeEvidence(result).pass, false); }
});

test('fails closed on missing metrics, no work, timeouts, exits and exceptions', () => {
  for (const mutate of [
    (r) => { r.summary = null; },
    (r) => { delete r.summary.metrics.checks; },
    (r) => { r.summary.metrics.http_reqs.count = 0; },
    (r) => { r.summary.metrics.checks = { value: 1, passes: 0, fails: 0 }; },
    (r) => { r.timedOut = true; },
    (r) => { r.exitCode = 99; },
    (r) => { r.log = 'ERRO[0000] TypeError: runtime exception'; }
  ]) { const result = flat(); mutate(result); assert.equal(smokeEvidence(result).pass, false); }
});
