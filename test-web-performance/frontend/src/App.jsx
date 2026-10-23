import { useEffect, useMemo, useRef, useState } from 'react';

const api = async (url, options) => {
  const response = await fetch(url, options);
  const data = response.headers.get('content-type')?.includes('application/json') ? await response.json() : await response.text();
  if (!response.ok) throw new Error(data.error || 'Yêu cầu không thành công.');
  if (Array.isArray(data?.scripts)) data.scripts = data.scripts.map((script, index) => ({ ...script, label: `Script ${index + 1}` }));
  return data;
};

function Score({ value }) { return <span className={value ? 'score pass' : 'score fail'}>{value ? '1' : '0'}</span>; }

function AccountIcon({ exit = false }) {
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{exit ? <><path d="M9 5H5v14h4M14 8l4 4-4 4M9 12h9" /></> : <><circle cx="12" cy="8" r="3.5" /><path d="M5 21v-2a7 7 0 0 1 14 0v2" /></>}</svg>;
}

function SignInNotice({ onSignIn, onDismiss, busy }) {
  return <div className="sign-in-notice" role="alert">
    <p>Vui lòng đăng nhập bằng tài khoản ChatGPT Plus trở lên để sử dụng tính năng này.</p>
    <div className="ai-actions"><button className="primary-action" onClick={onSignIn} disabled={busy}><AccountIcon />{busy ? 'Đang kết nối…' : 'Đăng nhập ChatGPT'}</button><button className="secondary" onClick={onDismiss} disabled={busy}>Để sau</button></div>
  </div>;
}

function AccountMenu({ auth, busy, onSignIn, onSignOut }) {
  const menu = useRef(null);
  useEffect(() => {
    const close = (event) => {
      if (event.type === 'keydown' && event.key !== 'Escape') return;
      if (menu.current?.open && (event.type === 'keydown' || !menu.current.contains(event.target))) {
        menu.current.open = false;
        if (event.type === 'keydown') menu.current.querySelector('summary')?.focus();
      }
    };
    document.addEventListener('pointerdown', close);
    document.addEventListener('keydown', close);
    return () => { document.removeEventListener('pointerdown', close); document.removeEventListener('keydown', close); };
  }, []);
  return <nav className="topbar" aria-label="Tài khoản">
    <span className="app-wordmark">k6 <span>Script Audit</span></span>
    {auth?.signedIn ? <details className="account-menu" ref={menu}>
      <summary aria-label="Mở tài khoản ChatGPT"><span className="account-avatar"><AccountIcon /></span><span className="account-label">{auth.name || 'Tài khoản ChatGPT'}<small>{auth.planEnabled ? 'Đã kết nối' : 'Cần cấp quyền AI'}</small></span><span aria-hidden="true">⌄</span></summary>
      <div className="account-popover"><strong>ChatGPT</strong><p className="account-email">{auth.email || auth.name || 'Đã đăng nhập'}</p>{!auth.planEnabled && <button className="secondary" onClick={onSignIn} disabled={busy}>Kết nối lại</button>}<button className="account-logout" onClick={async () => { await onSignOut(); if (menu.current) menu.current.open = false; }} disabled={busy}><AccountIcon exit />{busy ? 'Đang xử lý…' : 'Đăng xuất'}</button><small>Ngắt kết nối ChatGPT khỏi ứng dụng này.</small></div>
    </details> : <button className="account-login secondary" onClick={onSignIn} disabled={busy}><AccountIcon />{busy ? 'Đang kết nối…' : 'Đăng nhập ChatGPT'}</button>}
  </nav>;
}

function MarkdownText({ text }) {
  const tokens = String(text).split(/(\*\*[^*]+\*\*|`[^`]+`)/g).filter(Boolean);
  return tokens.map((token, index) => {
    if (token.startsWith('**') && token.endsWith('**')) return <strong key={index}>{token.slice(2, -2)}</strong>;
    if (token.startsWith('`') && token.endsWith('`')) return <code key={index}>{token.slice(1, -1)}</code>;
    return token;
  });
}

function MarkdownReview({ text }) {
  const lines = String(text || '').replaceAll('\r\n', '\n').split('\n');
  const blocks = [];
  let index = 0;
  while (index < lines.length) {
    const line = lines[index].trim();
    if (!line) { index += 1; continue; }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) { blocks.push(<h4 key={`heading-${index}`}>{<MarkdownText text={heading[2]} />}</h4>); index += 1; continue; }
    if (/^---+$/.test(line)) { blocks.push(<hr key={`rule-${index}`} />); index += 1; continue; }
    if (/^[-*]\s+/.test(line)) {
      const items = [];
      while (index < lines.length && /^[-*]\s+/.test(lines[index].trim())) { items.push(lines[index].trim().replace(/^[-*]\s+/, '')); index += 1; }
      blocks.push(<ul key={`list-${index}`}>{items.map((item, itemIndex) => <li key={itemIndex}><MarkdownText text={item} /></li>)}</ul>);
      continue;
    }
    if (/^\d+\.\s+/.test(line)) {
      const items = [];
      while (index < lines.length && /^\d+\.\s+/.test(lines[index].trim())) { items.push(lines[index].trim().replace(/^\d+\.\s+/, '')); index += 1; }
      blocks.push(<ol key={`ordered-${index}`}>{items.map((item, itemIndex) => <li key={itemIndex}><MarkdownText text={item} /></li>)}</ol>);
      continue;
    }
    blocks.push(<p key={`paragraph-${index}`}><MarkdownText text={line} /></p>);
    index += 1;
  }
  return <div className="model-markdown">{blocks}</div>;
}

function UploadForm({ onAudit }) {
  const [files, setFiles] = useState({});
  const [reviewer, setReviewer] = useState('Thành viên C');
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function submit(event) {
    event.preventDefault();
    setError('');
    if (!files.har || !files.chatgptScript || !files.claudeScript) return setError('Hãy chọn đủ 3 file bắt buộc.');
    const body = new FormData();
    Object.entries(files).forEach(([key, value]) => body.append(key, value));
    body.append('reviewer', reviewer);
    body.append('note', note);
    setLoading(true);
    try { onAudit(await api('/api/audits', { method: 'POST', body })); } catch (err) { setError(err.message); } finally { setLoading(false); }
  }

  const fileInput = (key, label, accept, help) => <label className="file-field">
    <span className="file-label">{label}</span>
    <span className={`file-picker ${files[key] ? 'has-file' : ''}`}>
      <input type="file" accept={accept} onChange={(event) => setFiles((old) => ({ ...old, [key]: event.target.files[0] }))} />
      <span className="file-picker-action">Chọn file</span>
      <span className="file-picker-name">{files[key]?.name || help}</span>
    </span>
  </label>;

  return <div className="upload-layout">
    <form className="upload-card" onSubmit={submit}>
      <div className="section-heading">
        <div><p className="eyebrow">01 · Chọn đầu vào</p><h2>Đánh giá hai script</h2><p>Chọn HAR đã che dữ liệu nhạy cảm và hai file JavaScript.</p></div>
      </div>
      <fieldset className="artifact-fieldset">
        <legend>Files bắt buộc</legend>
        <div className="file-grid">
          {fileInput('har', 'HAR đã redacted', '.har,application/json', 'HAR: login → search → detail → checkout')}
          {fileInput('chatgptScript', 'Script 1', '.js,text/javascript', 'Chọn file k6 .js')}
          {fileInput('claudeScript', 'Script 2', '.js,text/javascript', 'Chọn file k6 .js')}
        </div>
      </fieldset>
      <div className="form-grid">
        <label>Người chấm<input value={reviewer} onChange={(event) => setReviewer(event.target.value)} /></label>
        <label>Ghi chú<textarea value={note} onChange={(event) => setNote(event.target.value)} placeholder="Bối cảnh hoặc lưu ý cho lần audit này (tùy chọn)" /></label>
      </div>
      <div className="submit-row">
        <div>
          <p className="safety">Smoke run: 1 VU × 1 iteration tại SUT local.</p>
          <p className="ai-note">Đăng nhập ChatGPT khi cần phân tích AI.</p>
        </div>
        <button className="primary-action" disabled={loading} type="submit">{loading ? 'Đang chạy k6 smoke…' : 'Chạy audit'}</button>
      </div>
      {error && <p className="error inline-alert" role="alert">{error}</p>}
    </form>
    <aside className="workflow-card" aria-label="Quy trình audit">
      <p className="eyebrow">Quy trình</p>
      <h2>Ba bước, một scorecard</h2>
      <ol className="workflow-list">
        <li><span>1</span><div><strong>Nộp artifacts</strong><p>HAR redacted và hai raw script.</p></div></li>
        <li><span>2</span><div><strong>Chạy evidence</strong><p>Rule cố định và k6 smoke kiểm chứng script.</p></div></li>
        <li><span>3</span><div><strong>Duyệt kết quả</strong><p>Chỉnh điểm khi cần rồi tải scorecard.</p></div></li>
      </ol>
      <div className="workflow-note"><strong>Không phải load test</strong><p>Smoke run chỉ xác nhận luồng script chạy cơ bản, không đo baseline, stress hoặc spike.</p></div>
    </aside>
  </div>;
}

function AIReview({ audit, onAudit, auth, refreshAuth, onSignIn, authBusy }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loginRequired, setLoginRequired] = useState(false);

  async function startModelReview() {
    if (!auth?.signedIn || !auth?.planEnabled) { setLoginRequired(true); return; }
    setLoginRequired(false);
    setLoading(true); setError('');
    try { onAudit(await api(`/api/audits/${audit.id}/model-review`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ model: 'gpt-5.6-luna', reasoningEffort: 'medium' }) })); await refreshAuth(); } catch (err) { setError(err.message); } finally { setLoading(false); }
  }

  async function skip() {
    setLoading(true); setError('');
    try { onAudit(await api(`/api/audits/${audit.id}/model-review`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action: 'skip' }) })); } catch (err) { setError(err.message); } finally { setLoading(false); }
  }

  const review = audit.modelReview || {};
  return <section className="model-review" aria-labelledby="ai-review-heading">
    <div className="panel-heading">
      <div><p className="eyebrow">03 · Phân tích AI</p><h3 id="ai-review-heading">Nhận xét script</h3></div>
    </div>
    <p className="panel-intro">Luna nhận xét chất lượng code và những điểm cần cải thiện dựa trên rubric, source và kết quả k6.</p>
    <div className={`ai-result ${review.status === 'complete' ? 'is-complete' : ''}`}>
      {review.status === 'complete' ? <><p className="connected">{review.model} · {review.reasoningEffort || 'medium'}</p><MarkdownReview text={review.text} /></> : <p>Chưa có nhận xét AI.</p>}
    </div>
    <div className="ai-connection">
      <div className="ai-actions">
        <button className="primary-action" onClick={startModelReview} disabled={loading || authBusy}>{loading ? 'Đang nhận xét…' : 'Nhận xét'}</button>
        <button className="secondary" onClick={skip} disabled={loading}>Bỏ qua AI review</button>
      </div>
    </div>
    {loginRequired && !auth?.planEnabled && <SignInNotice onSignIn={onSignIn} onDismiss={() => setLoginRequired(false)} busy={authBusy} />}
    {error && <p className="error inline-alert" role="alert">{error}</p>}
  </section>;
}

function D7Guidance({ audit, onAudit, auth, refreshAuth, onSignIn, authBusy }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loginRequired, setLoginRequired] = useState(false);
  const guidance = audit.d7Guidance || {};
  const complete = guidance.status === 'complete' && guidance.schemaVersion === 2;
  const scriptLabel = (fileName) => audit.scripts.find((script) => script.fileName === fileName)?.label || fileName;

  async function generate() {
    if (!auth?.signedIn || !auth?.planEnabled) { setLoginRequired(true); return; }
    setLoginRequired(false);
    setLoading(true); setError('');
    try { onAudit(await api(`/api/audits/${audit.id}/d7-guidance`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ model: 'gpt-5.6-luna', reasoningEffort: 'medium' }) })); await refreshAuth(); } catch (err) { setError(err.message); } finally { setLoading(false); }
  }

  return <section className="d7-guidance" aria-labelledby="d7-heading">
    <div className="panel-heading">
      <div><p className="eyebrow">04 · Gợi ý hiệu năng</p><h3 id="d7-heading">Threshold & correlation</h3></div>
    </div>
    <p className="panel-intro">Luna đề xuất ngưỡng hiệu năng và cách xử lý dữ liệu động cho từng script.</p>
    {complete ? <>
      <div className="d7-result is-complete" role="status"><p className="connected">Đề xuất từ {guidance.model} · reasoning {guidance.reasoningEffort || 'medium'} · {new Date(guidance.generatedAt).toLocaleString('vi-VN')}</p><p>{guidance.summary}</p></div>
      <section className="d7-output" aria-labelledby="threshold-heading">
        <h4 id="threshold-heading">01 · Threshold Luna đề xuất</h4>
        <p className="muted">Ngưỡng khởi điểm cần được kiểm chứng bằng load test. Smoke chỉ chạy 1 VU × 1 iteration.</p>
        <div className="table-wrap"><table className="d7-table"><caption>Threshold đề xuất bởi Luna theo từng script</caption><thead><tr><th>Script / Metric</th><th>Ngưỡng đề xuất</th><th>Lý do & evidence</th><th>Cách kiểm chứng</th></tr></thead><tbody>{guidance.thresholds.map((row, index) => <tr key={index}><td><strong>{scriptLabel(row.script)}</strong><code>{row.metric}</code></td><td>{row.expression ? <code className="threshold-value">{row.expression}</code> : <span className="muted">Chưa đủ dữ liệu để đề xuất số</span>}</td><td><p>{row.reason}</p><span className="d7-evidence">Evidence: {row.evidence}</span></td><td>{row.validation}</td></tr>)}</tbody></table></div>
      </section>
      <section className="d7-output" aria-labelledby="correlation-heading">
        <h4 id="correlation-heading">02 · Correlation Luna đề xuất</h4>
        {guidance.correlations.length ? <div className="table-wrap"><table className="d7-table"><caption>Phân tích extract và inject dữ liệu động bởi Luna</caption><thead><tr><th>Script / Biến động</th><th>Nguồn → Đích</th><th>Hiện trạng & evidence</th><th>Đề xuất xử lý</th></tr></thead><tbody>{guidance.correlations.map((row, index) => <tr key={index}><td><strong>{scriptLabel(row.script)}</strong><code>{row.variable}</code></td><td><span className="d7-direction">Lấy từ</span>{row.extractFrom}<span className="d7-direction">Gửi vào</span>{row.injectInto}</td><td><p>{row.finding}</p><span className="d7-evidence">Evidence: {row.evidence}</span></td><td>{row.suggestion}</td></tr>)}</tbody></table></div> : <p className="muted">Luna không tìm thấy correlation cần đề xuất. Xem giới hạn evidence bên dưới.</p>}
      </section>
      {guidance.limitations.length > 0 && <aside className="d7-limitations"><h4>Giới hạn evidence do Luna ghi nhận</h4><ul>{guidance.limitations.map((item, index) => <li key={index}>{item}</li>)}</ul></aside>}
    </> : <div className="d7-result" role="status"><p>{guidance.standard ? 'Tạo lại đề xuất để cập nhật bảng phân tích.' : 'Chưa có đề xuất. Chạy Luna để tạo bảng phân tích.'}</p></div>}
    <div className="ai-connection">
      <div className="ai-actions">
        <button className="primary-action" onClick={generate} disabled={loading || authBusy}>{loading ? 'Đang phân tích…' : 'Tạo đề xuất'}</button>
      </div>
    </div>
    {loginRequired && !auth?.planEnabled && <SignInNotice onSignIn={onSignIn} onDismiss={() => setLoginRequired(false)} busy={authBusy} />}
    {error && <p className="error inline-alert" role="alert">{error}</p>}
  </section>;
}

function AuditDashboard({ audit, onAudit, auth, refreshAuth, onSignIn, authBusy }) {
  const [editing, setEditing] = useState(null);
  const [reason, setReason] = useState('');
  const [saving, setSaving] = useState(false);
  const changes = useMemo(() => audit.scripts.flatMap((script) => script.criteria.filter((item) => item.finalScore !== item.autoScore || item.overrideReason).map((item) => ({ fileName: script.fileName, criterionId: item.criterionId, finalScore: item.finalScore, reason: item.overrideReason }))), [audit]);

  function toggle(script, criterion) {
    const clone = structuredClone(audit);
    const target = clone.scripts.find((item) => item.fileName === script.fileName).criteria.find((item) => item.criterionId === criterion.criterionId);
    target.finalScore = target.finalScore ? 0 : 1;
    target.overrideReason = '';
    clone.scripts.forEach((item) => { item.finalScore = item.criteria.reduce((sum, row) => sum + row.finalScore, 0); });
    onAudit(clone); setEditing({ fileName: script.fileName, criterionId: criterion.criterionId }); setReason(criterion.overrideReason || '');
  }

  async function save() {
    setSaving(true);
    try { onAudit(await api(`/api/audits/${audit.id}/scores`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ changes }) })); setEditing(null); } finally { setSaving(false); }
  }

  const active = editing && audit.scripts.find((script) => script.fileName === editing.fileName)?.criteria.find((item) => item.criterionId === editing.criterionId);
  return <section className="dashboard">
    <header className="audit-header">
      <div className="audit-identity"><p className="eyebrow">Audit hoàn tất</p><h2>Kết quả đã sẵn sàng để duyệt</h2><p><span>{audit.id}</span> · Rubric {audit.rubric.id} v{audit.rubric.version} · {new Date(audit.createdAt).toLocaleString('vi-VN')}</p><p>Reviewer: {audit.reviewer}</p></div>
      <a className="download" href={`/api/audits/${audit.id}/scorecard.md`}>Tải rubric_scorecard.md <span aria-hidden="true">↓</span></a>
    </header>
    <section className="overview-panel" aria-labelledby="overview-heading">
      <div className="panel-heading"><div><p className="eyebrow">01 · Tổng quan</p><h3 id="overview-heading">Điểm theo từng script</h3></div><p className="table-hint">Bấm vào điểm trong bảng để duyệt lại.</p></div>
      <div className="summary-grid">{audit.scripts.map((script) => <article className={`summary ${script.smoke.pass ? 'summary-pass' : 'summary-fail'}`} key={script.fileName}><div><p>{script.label}</p><span className="script-file">{script.originalName || script.fileName}</span><strong>{script.finalScore}<small>/10</small></strong></div><span className={script.smoke.pass ? 'run pass-text' : 'run fail-text'}><i aria-hidden="true" />{script.smoke.pass ? 'Smoke pass' : 'Smoke fail'}</span></article>)}</div>
    </section>
    <section className="scoring-panel" aria-labelledby="scoring-heading">
      <div className="panel-heading"><div><p className="eyebrow">02 · Evidence</p><h3 id="scoring-heading">Bảng chấm 10 tiêu chí</h3></div><p className="table-hint"><span className="score pass">1</span> đạt <span className="score fail">0</span> chưa đạt</p></div>
      <div className="table-wrap"><table><caption>Evidence rule engine theo từng tiêu chí và script</caption><thead><tr><th scope="col">#</th><th scope="col">Tiêu chí</th>{audit.scripts.map((script) => <th scope="col" key={script.fileName}>{script.label}</th>)}</tr></thead><tbody>{audit.scripts[0].criteria.map((row, index) => <tr key={row.criterionId}><td className="criterion-number">{row.criterionId}</td><td className="criterion-title"><strong>{row.title}</strong></td>{audit.scripts.map((script) => { const item = script.criteria[index]; return <td key={script.fileName} className="result-cell"><button className="score-button" onClick={() => toggle(script, item)} aria-label={`Chỉnh điểm ${script.label} tiêu chí ${item.criterionId}`} title="Bấm để duyệt lại điểm"><Score value={item.finalScore} /></button>{item.finalScore !== item.autoScore && <small className="human">Đã duyệt thủ công</small>}<strong>{item.message}</strong>{item.line && <span className="line">Source line {item.line}</span>}<span>{item.suggestion}</span></td>; })}</tr>)}</tbody></table></div>
    </section>
    <section className="smoke" aria-labelledby="smoke-heading"><div className="panel-heading"><div><p className="eyebrow">Runtime evidence</p><h3 id="smoke-heading">k6 smoke logs</h3></div><p className="table-hint">Mở từng dòng để xem log.</p></div>{audit.scripts.map((script) => <details key={script.fileName}><summary><span><strong>{script.label}</strong><small>{script.smoke.message}</small></span><span className={script.smoke.pass ? 'run pass-text' : 'run fail-text'}>{script.smoke.pass ? 'Pass' : 'Fail'} · exit {script.smoke.exitCode} · p95 {script.smoke.p95Ms?.toFixed?.(2) ?? 'n/a'} ms</span></summary><pre>{script.smoke.log || 'Không có log.'}</pre></details>)}</section>
    <AIReview audit={audit} onAudit={onAudit} auth={auth} refreshAuth={refreshAuth} onSignIn={onSignIn} authBusy={authBusy} />
    <D7Guidance audit={audit} onAudit={onAudit} auth={auth} refreshAuth={refreshAuth} onSignIn={onSignIn} authBusy={authBusy} />
    <div className="actions"><div><strong>{changes.length ? `${changes.length} thay đổi chưa lưu` : 'Chưa có thay đổi điểm'}</strong><span>Điểm đã duyệt chỉ được ghi nhận khi bạn lưu.</span></div><div className="action-buttons"><button className="primary-action" onClick={save} disabled={saving || !changes.length}>{saving ? 'Đang lưu…' : 'Lưu điểm đã duyệt'}</button><button className="secondary" onClick={() => onAudit(null)}>Audit mới</button></div></div>
    {active && <div className="review" role="region" aria-label="Ghi lý do chỉnh điểm"><div><p className="eyebrow">Duyệt thủ công</p><p><strong>Ghi lý do chỉnh điểm — tiêu chí {active.criterionId}</strong></p></div><textarea value={reason} onChange={(event) => setReason(event.target.value)} placeholder="Ví dụ: script dùng tên biến khác nhưng vẫn correlation token đúng." /><button className="primary-action" onClick={() => { const clone = structuredClone(audit); const item = clone.scripts.find((script) => script.fileName === editing.fileName).criteria.find((row) => row.criterionId === editing.criterionId); item.overrideReason = reason; onAudit(clone); setEditing(null); setReason(''); }}>Xác nhận lý do</button></div>}
  </section>;
}

export default function App() {
  const [audit, setAudit] = useState(null);
  const [rubric, setRubric] = useState(null);
  const [auth, setAuth] = useState(null);
  const [authNotice, setAuthNotice] = useState('');
  const [authBusy, setAuthBusy] = useState(true);
  const refreshAuth = () => api('/api/auth/chatgpt/status').then(setAuth).catch(() => setAuth(null)).finally(() => setAuthBusy(false));

  async function signIn() {
    setAuthBusy(true); setAuthNotice('');
    try {
      const { authorizationUrl } = await api('/api/auth/chatgpt/start', { method: 'POST' });
      // Restore this tab's audit (including score edits) after the OAuth redirect.
      try { if (audit) sessionStorage.setItem('script-audit-return', JSON.stringify(audit)); else sessionStorage.removeItem('script-audit-return'); } catch { /* Storage can be disabled in private browsing. */ }
      window.location.assign(authorizationUrl);
    } catch (error) { setAuthNotice(error.message); setAuthBusy(false); }
  }

  async function signOut() {
    setAuthBusy(true); setAuthNotice('');
    try { setAuth(await api('/api/auth/chatgpt/logout', { method: 'POST' })); setAuthNotice('Đã đăng xuất ChatGPT.'); }
    catch (error) { setAuthNotice(error.message); }
    finally { setAuthBusy(false); }
  }

  useEffect(() => { api('/api/rubric').then(setRubric).catch(() => {}); refreshAuth(); }, []);
  useEffect(() => {
    const result = new URLSearchParams(window.location.search).get('aiAuth');
    if (!result) return;
    setAuthNotice(result === 'success' ? 'Đã kết nối ChatGPT.' : 'Chưa kết nối được ChatGPT. Bạn có thể thử đăng nhập lại.');
    try {
      const saved = JSON.parse(sessionStorage.getItem('script-audit-return') || 'null');
      if (saved?.id && Array.isArray(saved.scripts)) setAudit({ ...saved, scripts: saved.scripts.map((script, index) => ({ ...script, label: `Script ${index + 1}` })) });
      sessionStorage.removeItem('script-audit-return');
    } catch { /* Keep the upload screen if a stored draft is unavailable. */ }
    window.history.replaceState({}, '', window.location.pathname);
    refreshAuth();
  }, []);

  return <main className="app-shell">
    <AccountMenu auth={auth} busy={authBusy} onSignIn={signIn} onSignOut={signOut} />
    {authNotice && <p className="auth-notice" role="status">{authNotice}</p>}
    <header className="hero">
      <div className="brand-mark" aria-hidden="true">k6</div>
      <div><p className="eyebrow">PERFORMANCE TESTING</p><h1>Đánh giá hai script k6.</h1><p className="hero-copy">Chạy smoke test, so sánh kết quả và nhận gợi ý từ Luna.</p><div className="hero-meta">{rubric && <span className="badge">{rubric.criteria.length} tiêu chí · {rubric.maxScore} điểm / script</span>}</div></div>
    </header>
    {audit ? <AuditDashboard audit={audit} onAudit={setAudit} auth={auth} refreshAuth={refreshAuth} onSignIn={signIn} authBusy={authBusy} /> : <UploadForm onAudit={setAudit} />}
  </main>;
}
