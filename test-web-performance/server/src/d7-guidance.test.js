import test from 'node:test';
import assert from 'node:assert/strict';
import { createD7Guidance, parseD7Output } from './d7-guidance.js';
import { createScorecard } from './markdown.js';

const scripts = ['chatgpt_script.js', 'claude_script.js'].map((fileName) => ({ fileName, label: fileName, source: '// fixture', smoke: { pass: false, exitCode: 1, log: 'connection refused', p95Ms: null }, criteria: [] }));
const output = {
  summary: 'Cả hai smoke fail, chưa chứng minh correlation.',
  thresholds: scripts.map(({ fileName }, index) => ({ script: fileName, metric: 'http_req_duration', expression: index ? null : 'p(95)<750', reason: 'Ngưỡng khởi điểm tạm thời.', evidence: 'Smoke chưa kết nối được.', confidence: 'low', validation: 'Chạy baseline trên SUT hoạt động.' })),
  correlations: [{ script: scripts[0].fileName, variable: 'session', extractFrom: 'Login response', injectInto: 'Header', finding: 'Chưa xác nhận runtime.', suggestion: 'Guard parse response.', evidence: 'connection refused', confidence: 'low' }],
  limitations: ['1 VU × 1 iteration.']
};

test('accepts dynamic thresholds, nullable recommendations, and correlation fields', () => {
  assert.deepEqual(parseD7Output(JSON.stringify(output), scripts), output);
});

test('rejects invalid JSON, unknown scripts, missing fields and missing script coverage', () => {
  assert.throws(() => parseD7Output('not json', scripts));
  for (const mutate of [
    (data) => { data.thresholds[0].script = 'other.js'; },
    (data) => { delete data.correlations[0].injectInto; },
    (data) => { data.thresholds.pop(); },
    (data) => { data.thresholds[0].confidence = 'certain'; }
  ]) {
    const data = structuredClone(output);
    mutate(data);
    assert.throws(() => parseD7Output(JSON.stringify(data), scripts));
  }
});

test('streams Luna JSON into saved data and Markdown tables without changing scores', async (t) => {
  let request;
  t.mock.method(globalThis, 'fetch', async (_url, options) => {
    request = JSON.parse(options.body);
    const content = JSON.stringify(output);
    const events = [
      { type: 'response.output_text.delta', delta: content.slice(0, 80) },
      { type: 'response.output_text.delta', delta: content.slice(80) },
      { type: 'response.completed' }
    ].map((event) => `data: ${JSON.stringify(event)}\n\n`).join('');
    return new Response(events);
  });
  const before = structuredClone(scripts);
  const guidance = await createD7Guidance({ accessToken: 'mock', model: 'gpt-5.6-luna', reasoningEffort: 'medium', scripts, baseUrl: 'http://localhost:3000' });
  assert.equal(guidance.schemaVersion, 2);
  assert.equal(guidance.thresholds[0].expression, 'p(95)<750');
  assert.equal(guidance.standard, undefined);
  assert.ok(Array.isArray(request.input));
  assert.equal(request.reasoning.effort, 'medium');
  assert.deepEqual(scripts, before);
  const md = createScorecard({ id: 'TEST', har: { originalName: 'redacted.har' }, scripts, d7Guidance: guidance });
  assert.match(md, /p\(95\)<750/);
  assert.match(md, /Chưa đủ dữ liệu/);
  assert.match(md, /Guard parse response/);
});
