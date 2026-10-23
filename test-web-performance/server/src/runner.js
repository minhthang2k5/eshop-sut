import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';

const k6Binary = process.env.K6_BINARY || 'k6';

export async function runSmoke({ scriptPath, baseUrl, outputDir }) {
  const summaryPath = path.join(outputDir, 'summary.json');
  const args = ['run', '--vus', '1', '--iterations', '1', '--summary-export', summaryPath, scriptPath];
  const startedAt = new Date().toISOString();
  const result = await new Promise((resolve) => {
    const child = spawn(k6Binary, args, {
      cwd: outputDir,
      env: { ...process.env, BASE_URL: baseUrl },
      windowsHide: true
    });
    let stdout = '';
    let stderr = '';
    let timedOut = false;
    const timeout = setTimeout(() => { timedOut = true; child.kill(); }, 45_000);
    child.stdout.on('data', (chunk) => { stdout += chunk.toString(); });
    child.stderr.on('data', (chunk) => { stderr += chunk.toString(); });
    child.on('error', (error) => {
      clearTimeout(timeout);
      resolve({ exitCode: -1, stdout, stderr: `${stderr}\n${error.message}`, timedOut: false });
    });
    child.on('close', (exitCode) => {
      clearTimeout(timeout);
      resolve({ exitCode: exitCode ?? -1, stdout, stderr, timedOut });
    });
  });
  let summary = null;
  try { summary = JSON.parse(await fs.readFile(summaryPath, 'utf8')); } catch { /* k6 may fail before writing a summary */ }
  const log = `${result.stdout}\n${result.stderr}`.trim().slice(-8000);
  await fs.writeFile(path.join(outputDir, 'k6.log'), log);
  return { ...result, startedAt, summary, log };
}

export function smokeEvidence(result) {
  const metrics = result.summary?.metrics || {};
  const number = (...values) => values.find((value) => typeof value === 'number' && Number.isFinite(value)) ?? null;
  // --summary-export uses flat metric fields; handleSummary uses nested values.
  const checks = number(metrics.checks?.values?.rate, metrics.checks?.value);
  const failedRequests = number(metrics.http_req_failed?.values?.rate, metrics.http_req_failed?.value);
  const p95 = number(metrics.http_req_duration?.values?.['p(95)'], metrics.http_req_duration?.['p(95)']);
  const requests = number(metrics.http_reqs?.values?.count, metrics.http_reqs?.count);
  const checkMetric = metrics.checks?.values || metrics.checks;
  const checkCount = checkMetric && typeof checkMetric.passes === 'number' && typeof checkMetric.fails === 'number' ? checkMetric.passes + checkMetric.fails : null;
  const runtimeError = /(?:level=error|ERRO)[^\n]*(?:TypeError|ReferenceError|SyntaxError|GoError|Uncaught)/i.test(result.log || '');
  const reasons = [];
  if (result.exitCode !== 0) reasons.push(`exit ${result.exitCode}`);
  if (result.timedOut) reasons.push('quá thời gian chạy');
  if (runtimeError) reasons.push('exception trong script');
  if (!(requests > 0)) reasons.push('không có request được xác nhận');
  if (checks === null || failedRequests === null || p95 === null) reasons.push('thiếu metric cần thiết trong summary');
  if (!(checkCount > 0)) reasons.push('không xác nhận được check đã thực thi');
  if (checks !== null && checks !== 1) reasons.push('có check thất bại');
  if (failedRequests !== null && failedRequests !== 0) reasons.push('có request thất bại');
  const pass = reasons.length === 0;
  return {
    pass,
    exitCode: result.exitCode,
    checksRate: checks,
    failedRequestRate: failedRequests,
    p95Ms: p95,
    requestCount: requests,
    message: pass ? 'k6 smoke pass trên nhánh đã chạy; chưa chứng minh mọi nhánh nghiệp vụ.' : `k6 smoke chưa đạt: ${reasons.join('; ')}.`,
    log: result.log
  };
}
