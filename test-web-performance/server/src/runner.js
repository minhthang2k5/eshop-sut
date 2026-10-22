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
  const checks = metrics.checks?.values?.rate;
  const failedRequests = metrics.http_req_failed?.values?.rate;
  const pass = result.exitCode === 0 && !result.timedOut && (checks === undefined || checks === 1) && (failedRequests === undefined || failedRequests === 0);
  return {
    pass,
    exitCode: result.exitCode,
    checksRate: checks ?? null,
    failedRequestRate: failedRequests ?? null,
    p95Ms: metrics.http_req_duration?.values?.['p(95)'] ?? null,
    message: pass ? 'k6 smoke pass: script hoàn tất, không có request/check thất bại.' : `k6 smoke fail (exit ${result.exitCode}).`,
    log: result.log
  };
}
