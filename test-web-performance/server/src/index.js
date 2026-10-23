import 'dotenv/config';
import crypto from 'node:crypto';
import express from 'express';
import cors from 'cors';
import multer from 'multer';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { rubric } from './rubric.js';
import { scanSource, validateScriptSafety } from './rules.js';
import { runSmoke, smokeEvidence } from './runner.js';
import { createScorecard } from './markdown.js';
import { createPlanModelReview } from './model-review.js';
import { createD7Guidance } from './d7-guidance.js';
import { createChatGPTAuth } from './chatgpt-auth.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const dataRoot = path.join(root, 'data');
const uploadsRoot = path.join(dataRoot, 'uploads');
const auditsRoot = path.join(dataRoot, 'audits');
const authRoot = path.join(dataRoot, 'chatgpt-auth');
const baseUrl = process.env.SUT_BASE_URL || 'http://localhost:3000';
const port = Number(process.env.PORT || 4000);
const frontendOrigin = process.env.FRONTEND_ORIGIN || 'http://localhost:5175';
const app = express();
const upload = multer({ dest: uploadsRoot, limits: { fileSize: 2 * 1024 * 1024, files: 3 } });

await Promise.all([fs.mkdir(uploadsRoot, { recursive: true }), fs.mkdir(auditsRoot, { recursive: true }), fs.mkdir(authRoot, { recursive: true })]);
const chatgptAuth = createChatGPTAuth({ authRoot, port, frontendOrigin });
app.use(cors({ origin: [frontendOrigin], methods: ['GET', 'POST', 'PATCH'] }));
app.use(express.json({ limit: '100kb' }));

function newId() { return `AUD-${new Date().toISOString().slice(0, 10).replaceAll('-', '')}-${crypto.randomBytes(3).toString('hex').toUpperCase()}`; }
function allowedBaseUrl(value) { return value === baseUrl; }
function fileByField(files, field) {
  // multer.fields() trả về object: { har: [file], chatgptScript: [file], ... }.
  // Giữ hỗ trợ mảng để hàm vẫn đúng nếu middleware sau này đổi sang upload.array().
  if (Array.isArray(files)) return files.find((file) => file.fieldname === field);
  return files?.[field]?.[0];
}
async function readAudit(id) {
  const audit = JSON.parse(await fs.readFile(path.join(auditsRoot, id, 'audit.json'), 'utf8'));
  audit.scripts = audit.scripts.map((script, index) => ({ ...script, label: `Script ${index + 1}` }));
  return audit;
}
async function saveAudit(audit) { const directory = path.join(auditsRoot, audit.id); await fs.mkdir(directory, { recursive: true }); await fs.writeFile(path.join(directory, 'audit.json'), JSON.stringify(audit, null, 2)); return directory; }
function redactionWarnings(har) {
  const raw = JSON.stringify(har);
  const warnings = [];
  if (/Bearer\s+(?!<redacted>|REDACTED|\*{3})[A-Za-z0-9._-]{12,}/i.test(raw)) warnings.push('Bearer token');
  if (/"password"\s*:\s*"(?!<redacted>|REDACTED|\*{3})[^"\s]{4,}"/i.test(raw)) warnings.push('password value');
  if (/eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{8,}/.test(raw)) warnings.push('JWT value');
  return warnings;
}
function normalizeCriteria(source, smoke) {
  const staticCriteria = scanSource(source);
  const runtime = { criterionId: 10, pass: smoke.pass, message: smoke.message, suggestion: smoke.pass ? 'Không cần sửa smoke run.' : 'Mở k6 log, sửa lỗi source/request rồi chạy audit lại.' };
  return [...staticCriteria, runtime].map((item) => {
    const rubricItem = rubric.criteria.find((criterion) => criterion.id === item.criterionId);
    return { ...item, title: rubricItem.title, autoScore: item.pass ? 1 : 0, finalScore: item.pass ? 1 : 0, overrideReason: '' };
  });
}

app.get('/api/health', (_req, res) => res.json({ ok: true, baseUrl, rubric: { id: rubric.id, version: rubric.version } }));
app.get('/api/rubric', (_req, res) => res.json(rubric));
app.get('/api/auth/chatgpt/status', async (_req, res, next) => { try { res.json(await chatgptAuth.publicStatus()); } catch (error) { next(error); } });
app.post('/api/auth/chatgpt/start', async (_req, res, next) => { try { res.json({ authorizationUrl: await chatgptAuth.start() }); } catch (error) { next(error); } });
app.post('/api/auth/chatgpt/logout', async (_req, res, next) => { try { res.json(await chatgptAuth.logout()); } catch (error) { next(error); } });
app.get('/auth/callback', async (req, res) => {
  try {
    await chatgptAuth.exchangeCallback(req.query);
    res.redirect(chatgptAuth.callbackRedirect(true));
  } catch (error) {
    console.warn(`ChatGPT sign-in failed: ${error.message}`);
    res.redirect(chatgptAuth.callbackRedirect(false));
  }
});

app.post('/api/audits', upload.fields([{ name: 'har', maxCount: 1 }, { name: 'chatgptScript', maxCount: 1 }, { name: 'claudeScript', maxCount: 1 }]), async (req, res, next) => {
  try {
    const harFile = fileByField(req.files, 'har');
    const chatgptFile = fileByField(req.files, 'chatgptScript');
    const claudeFile = fileByField(req.files, 'claudeScript');
    if (!harFile || !chatgptFile || !claudeFile) return res.status(400).json({ error: 'Cần đủ HAR, Script 1 và Script 2.' });
    if (!harFile.originalname.endsWith('.har') || !chatgptFile.originalname.endsWith('.js') || !claudeFile.originalname.endsWith('.js')) return res.status(400).json({ error: 'HAR phải có đuôi .har và hai script phải có đuôi .js.' });
    const requestedBaseUrl = req.body.baseUrl || baseUrl;
    if (!allowedBaseUrl(requestedBaseUrl)) return res.status(400).json({ error: `Chỉ được phép smoke SUT đã cấu hình: ${baseUrl}` });
    let har;
    try { har = JSON.parse(await fs.readFile(harFile.path, 'utf8')); } catch { return res.status(400).json({ error: 'HAR không phải JSON hợp lệ.' }); }
    const redaction = redactionWarnings(har);
    if (redaction.length) return res.status(400).json({ error: `HAR có vẻ chưa redacted: phát hiện key nhạy cảm ${redaction.join(', ')}.` });
    const id = newId();
    const auditDirectory = path.join(auditsRoot, id);
    await fs.mkdir(auditDirectory, { recursive: true });
    const rawScripts = [
      { label: 'Script 1', field: chatgptFile, storageName: 'chatgpt_script.js' },
      { label: 'Script 2', field: claudeFile, storageName: 'claude_script.js' }
    ];
    const scripts = [];
    for (const item of rawScripts) {
      const source = await fs.readFile(item.field.path, 'utf8');
      const issue = validateScriptSafety(source, requestedBaseUrl);
      if (issue) return res.status(400).json({ error: `${item.label}: ${issue}` });
      const scriptPath = path.join(auditDirectory, item.storageName);
      await fs.copyFile(item.field.path, scriptPath);
      const scriptOutput = path.join(auditDirectory, item.storageName.replace('.js', '-smoke'));
      await fs.mkdir(scriptOutput, { recursive: true });
      const result = await runSmoke({ scriptPath, baseUrl: requestedBaseUrl, outputDir: scriptOutput });
      const smoke = smokeEvidence(result);
      scripts.push({ label: item.label, originalName: item.field.originalname, fileName: item.storageName, criteria: normalizeCriteria(source, smoke), smoke, _source: source });
    }
    await fs.copyFile(harFile.path, path.join(auditDirectory, 'session-redacted.har'));
    for (const script of scripts) delete script._source;
    const audit = { id, createdAt: new Date().toISOString(), reviewer: req.body.reviewer?.trim() || 'Thành viên C', note: req.body.note?.trim() || '', baseUrl: requestedBaseUrl, rubric: { id: rubric.id, version: rubric.version, maxScore: rubric.maxScore }, har: { originalName: harFile.originalname }, scripts, d7Guidance: { status: 'ready', message: 'Chưa có đề xuất D7. Chạy Luna để phân tích và tạo bảng threshold/correlation.' }, modelReview: { status: 'skipped', message: 'AI review đang được bỏ qua. Điểm và evidence hiện tại đã do rule engine + k6 quyết định.' } };
    for (const script of audit.scripts) script.finalScore = script.criteria.reduce((sum, item) => sum + item.finalScore, 0);
    await saveAudit(audit);
    res.status(201).json(audit);
  } catch (error) { next(error); }
});

app.get('/api/audits/:id', async (req, res, next) => { try { res.json(await readAudit(req.params.id)); } catch { next(); } });
app.patch('/api/audits/:id/scores', async (req, res, next) => {
  try {
    const audit = await readAudit(req.params.id);
    const changes = Array.isArray(req.body.changes) ? req.body.changes : [];
    for (const change of changes) {
      const script = audit.scripts.find((item) => item.fileName === change.fileName);
      const criterion = script?.criteria.find((item) => item.criterionId === Number(change.criterionId));
      if (criterion && (change.finalScore === 0 || change.finalScore === 1)) { criterion.finalScore = change.finalScore; criterion.overrideReason = String(change.reason || '').slice(0, 500); }
    }
    for (const script of audit.scripts) script.finalScore = script.criteria.reduce((sum, item) => sum + item.finalScore, 0);
    await saveAudit(audit);
    res.json(audit);
  } catch (error) { next(error); }
});
app.patch('/api/audits/:id/model-review', async (req, res, next) => {
  try {
    const audit = await readAudit(req.params.id);
    if (req.body?.action !== 'skip') return res.status(400).json({ error: 'Chỉ hỗ trợ thao tác bỏ qua AI review.' });
    audit.modelReview = { status: 'skipped', message: 'Bạn đã chọn bỏ qua AI review. Điểm và evidence vẫn do rule engine + k6 quyết định.' };
    await saveAudit(audit);
    res.json(audit);
  } catch (error) { next(error); }
});
app.post('/api/audits/:id/model-review', async (req, res, next) => {
  try {
    const audit = await readAudit(req.params.id);
    const { accessToken } = await chatgptAuth.tokenForPlan();
    const available = await chatgptAuth.availableModels(accessToken);
    const requested = typeof req.body?.model === 'string' ? req.body.model : 'gpt-5.6-luna';
    const reasoningEffort = 'medium';
    const selected = available.find((item) => item.slug === requested);
    if (!selected) return res.status(422).json({ error: `Tài khoản ChatGPT này không có model ${requested}. Không tự đổi sang model khác.` });
    const scripts = await Promise.all(audit.scripts.map(async (script) => ({ ...script, source: await fs.readFile(path.join(auditsRoot, audit.id, script.fileName), 'utf8') })));
    audit.modelReview = await createPlanModelReview({ accessToken, model: selected.slug, reasoningEffort, scripts, baseUrl: audit.baseUrl, rubric });
    await chatgptAuth.markModel(selected.slug);
    await saveAudit(audit);
    res.json(audit);
  } catch (error) {
    const status = /Continue with ChatGPT|chưa cấp quyền|hết hạn/.test(error.message) ? 401 : 502;
    res.status(status).json({ error: error.message || 'Không thể hoàn tất AI review.' });
  }
});
app.post('/api/audits/:id/d7-guidance', async (req, res, next) => {
  try {
    const audit = await readAudit(req.params.id);
    const { accessToken } = await chatgptAuth.tokenForPlan();
    const available = await chatgptAuth.availableModels(accessToken);
    const requested = typeof req.body?.model === 'string' ? req.body.model : 'gpt-5.6-luna';
    const reasoningEffort = 'medium';
    const selected = available.find((item) => item.slug === requested);
    if (!selected) return res.status(422).json({ error: `Tài khoản ChatGPT này không có model ${requested}. Không tự đổi sang model khác.` });
    const scripts = await Promise.all(audit.scripts.map(async (script) => ({ ...script, source: await fs.readFile(path.join(auditsRoot, audit.id, script.fileName), 'utf8') })));
    audit.d7Guidance = await createD7Guidance({ accessToken, model: selected.slug, reasoningEffort, scripts, baseUrl: audit.baseUrl });
    await chatgptAuth.markModel(selected.slug);
    await saveAudit(audit);
    res.json(audit);
  } catch (error) {
    const status = /Continue with ChatGPT|chưa cấp quyền|hết hạn/.test(error.message) ? 401 : 502;
    res.status(status).json({ error: error.message || 'Không thể tạo gợi ý D7.' });
  }
});
app.get('/api/audits/:id/scorecard.md', async (req, res, next) => {
  try { const audit = await readAudit(req.params.id); res.type('text/markdown').attachment('rubric_scorecard.md').send(createScorecard(audit)); } catch (error) { next(error); }
});
app.use((error, _req, res, _next) => { console.error(error); res.status(error.code === 'LIMIT_FILE_SIZE' ? 413 : 500).json({ error: error.code === 'LIMIT_FILE_SIZE' ? 'Mỗi file tối đa 2 MB.' : 'Server không thể hoàn tất audit.' }); });
app.listen(port, () => console.log(`AI k6 audit API listening on http://localhost:${port}`));
