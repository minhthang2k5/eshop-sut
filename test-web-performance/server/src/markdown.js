import { rubric } from './rubric.js';

function escapeCell(value = '') { return String(value).replaceAll('|', '\\|').replaceAll('\n', '<br>'); }

export function createScorecard(audit) {
  const lines = [
    `# AI k6 Script Audit — ${audit.id}`,
    '',
    `- Date: ${audit.createdAt}`,
    `- Reviewer: ${audit.reviewer || 'Thành viên C'}`,
    `- Rubric: ${rubric.id} v${rubric.version}`,
    `- HAR: ${audit.har.originalName} (redacted by submitter)`,
    `- Smoke profile: 1 VU × 1 iteration, base URL ${audit.baseUrl}`,
    ''
  ];
  for (const script of audit.scripts) {
    lines.push(`## ${script.label} — ${script.finalScore}/10`, '', '| # | Tiêu chí | Điểm | Evidence | Cách sửa |', '| --- | --- | :---: | --- | --- |');
    for (const item of script.criteria) {
      const humanNote = item.overrideReason ? ` Human review: ${item.overrideReason}` : '';
      lines.push(`| ${item.criterionId} | ${escapeCell(item.title)} | ${item.finalScore} | ${escapeCell(item.message)}${humanNote} | ${escapeCell(item.suggestion)} |`);
    }
    lines.push('', '### Smoke evidence', '', `- ${script.smoke.message}`, `- Exit code: ${script.smoke.exitCode}; checks: ${script.smoke.checksRate ?? 'n/a'}; failed requests: ${script.smoke.failedRequestRate ?? 'n/a'}; p95: ${script.smoke.p95Ms ?? 'n/a'} ms`, '');
  }
  const d7 = audit.d7Guidance;
  if (d7?.status === 'complete' && d7.schemaVersion === 2) {
    lines.push('## D7 — Threshold & correlation do Luna đề xuất', '', `- Model: ${d7.model}; reasoning: ${d7.reasoningEffort}; tạo lúc: ${d7.generatedAt}`, '- Ngưỡng khởi điểm từ smoke 1 VU × 1 iteration; cần load test để kiểm chứng.', '', d7.summary, '', '### Threshold đề xuất', '', '| Script | Metric | Expression | Lý do | Evidence | Tin cậy | Kiểm chứng |', '| --- | --- | --- | --- | --- | --- | --- |');
    for (const row of d7.thresholds) lines.push(`| ${[row.script, row.metric, row.expression ?? 'Chưa đủ dữ liệu', row.reason, row.evidence, row.confidence, row.validation].map(escapeCell).join(' | ')} |`);
    lines.push('', '### Correlation đề xuất', '', '| Script | Biến | Nguồn | Đích | Hiện trạng | Đề xuất | Evidence | Tin cậy |', '| --- | --- | --- | --- | --- | --- | --- | --- |');
    for (const row of d7.correlations) lines.push(`| ${[row.script, row.variable, row.extractFrom, row.injectInto, row.finding, row.suggestion, row.evidence, row.confidence].map(escapeCell).join(' | ')} |`);
    lines.push('', '### Giới hạn evidence', '', ...d7.limitations.map((item) => `- ${item}`));
    lines.push('');
  }
  lines.push('## Ghi chú', '', audit.note || 'Không có ghi chú bổ sung.', '');
  return lines.join('\n');
}
