import { useEffect, useMemo, useState } from 'react';

const api = async (url, options) => {
  const response = await fetch(url, options);
  const data = response.headers.get('content-type')?.includes('application/json') ? await response.json() : await response.text();
  if (!response.ok) throw new Error(data.error || 'Yêu cầu không thành công.');
  return data;
};

function Score({ value }) { return <span className={value ? 'score pass' : 'score fail'}>{value ? '1' : '0'}</span>; }

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
        <div><p className="eyebrow">01 · Nộp artifacts</p><h2>Tạo một audit mới</h2><p>Đưa vào HAR đã redacted cùng hai script để hệ thống chạy rule và k6 smoke test.</p></div>
        <span className="step-status">Bắt đầu tại đây</span>
      </div>
      <fieldset className="artifact-fieldset">
        <legend>Files bắt buộc</legend>
        <div className="file-grid">
          {fileInput('har', 'HAR đã redacted', '.har,application/json', 'HAR: login → search → detail → checkout')}
          {fileInput('chatgptScript', 'ChatGPT raw script', '.js,text/javascript', 'File .js do ChatGPT sinh ra')}
          {fileInput('claudeScript', 'Claude raw script', '.js,text/javascript', 'File .js do Claude sinh ra')}
        </div>
      </fieldset>
      <div className="form-grid">
        <label>Người chấm<input value={reviewer} onChange={(event) => setReviewer(event.target.value)} /></label>
        <label>Ghi chú<textarea value={note} onChange={(event) => setNote(event.target.value)} placeholder="Bối cảnh hoặc lưu ý cho lần audit này (tùy chọn)" /></label>
      </div>
      <div className="submit-row">
        <div>
          <p className="safety">Smoke run: 1 VU × 1 iteration tại SUT local.</p>
          <p className="ai-note">AI review là tùy chọn sau khi audit xong. Không cần đăng nhập để có điểm rubric và evidence.</p>
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

function AIReview({ audit, onAudit, auth, refreshAuth }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function continueWithChatGPT() {
    setError('');
    try { window.location.assign((await api('/api/auth/chatgpt/start', { method: 'POST' })).authorizationUrl); } catch (err) { setError(err.message); }
  }

  async function startModelReview() {
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
      <div><p className="eyebrow">03 · Tùy chọn</p><h3 id="ai-review-heading">AI review</h3></div>
      <span className="optional-badge">Không ảnh hưởng điểm</span>
    </div>
    <p className="panel-intro">Rule engine và k6 quyết định điểm. AI chỉ đọc source, rubric và evidence để giải thích hoặc nêu rủi ro cần kiểm tra thêm.</p>
    <div className={`ai-result ${review.status === 'complete' ? 'is-complete' : ''}`}>
      {review.status === 'complete' ? <><p className="connected">Đã review bằng {review.model} · reasoning {review.reasoningEffort || 'medium'}.</p><MarkdownReview text={review.text} /></> : <p>{review.message || 'Chưa có AI review.'}</p>}
    </div>
    <div className="ai-connection">
      {auth?.signedIn && auth.planEnabled ? <p className="connected">Đã kết nối ChatGPT{auth.email ? `: ${auth.email}` : ''}. AI review sẽ dùng quyền ChatGPT plan bạn đã cấp.</p> : <p className="muted">Chưa kết nối ChatGPT. Bạn vẫn có thể chấm, lưu điểm và tải scorecard bình thường.</p>}
      <div className="ai-actions">
        {auth?.planEnabled ? <button className="primary-action" onClick={startModelReview} disabled={loading}>{loading ? 'Đang review…' : 'Review bằng Luna 5.6 · medium'}</button> : <button className="primary-action" onClick={continueWithChatGPT} disabled={loading}>Continue with ChatGPT</button>}
        <button className="secondary" onClick={skip} disabled={loading}>Bỏ qua AI review</button>
      </div>
    </div>
    {error && <p className="error inline-alert" role="alert">{error}</p>}
  </section>;
}

function D7Guidance({ audit, onAudit, auth, refreshAuth }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const guidance = audit.d7Guidance || {};
  const complete = guidance.status === 'complete' && guidance.schemaVersion === 2;
  const scriptLabel = (fileName) => audit.scripts.find((script) => script.fileName === fileName)?.label || fileName;
  const confidence = (value) => <span className={`confidence confidence-${value}`}>Tin cậy {({ low: 'thấp', medium: 'vừa', high: 'cao' })[value] || value}</span>;

  async function continueWithChatGPT() {
    setError('');
    try { window.location.assign((await api('/api/auth/chatgpt/start', { method: 'POST' })).authorizationUrl); } catch (err) { setError(err.message); }
  }

  async function generate() {
    setLoading(true); setError('');
    try { onAudit(await api(`/api/audits/${audit.id}/d7-guidance`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ model: 'gpt-5.6-luna', reasoningEffort: 'medium' }) })); await refreshAuth(); } catch (err) { setError(err.message); } finally { setLoading(false); }
  }

  return <section className="d7-guidance" aria-labelledby="d7-heading">
    <div className="panel-heading">
      <div><p className="eyebrow">D7 · Luna performance guidance</p><h3 id="d7-heading">Đề xuất threshold & correlation</h3></div>
      <span className="optional-badge">Backup · không ảnh hưởng điểm</span>
    </div>
    <p className="panel-intro">Luna phân tích source và evidence k6 của từng script, tự đề xuất giá trị và cách xử lý dữ liệu động. Web chuyển kết quả của Luna thành hai bảng dưới đây.</p>
    {complete ? <>
      <div className="d7-result is-complete" role="status"><p className="connected">Đề xuất từ {guidance.model} · reasoning {guidance.reasoningEffort || 'medium'} · {new Date(guidance.generatedAt).toLocaleString('vi-VN')}</p><p>{guidance.summary}</p></div>
      <section className="d7-output" aria-labelledby="threshold-heading">
        <h4 id="threshold-heading">01 · Threshold Luna đề xuất</h4>
        <p className="muted">Ngưỡng khởi điểm cần được kiểm chứng bằng load test. Smoke chỉ chạy 1 VU × 1 iteration.</p>
        <div className="table-wrap"><table className="d7-table"><caption>Threshold đề xuất bởi Luna theo từng script</caption><thead><tr><th>Script / Metric</th><th>Ngưỡng đề xuất</th><th>Lý do & evidence</th><th>Cách kiểm chứng</th></tr></thead><tbody>{guidance.thresholds.map((row, index) => <tr key={index}><td><strong>{scriptLabel(row.script)}</strong><code>{row.metric}</code></td><td>{row.expression ? <code className="threshold-value">{row.expression}</code> : <span className="muted">Chưa đủ dữ liệu để đề xuất số</span>}{confidence(row.confidence)}</td><td><p>{row.reason}</p><span className="d7-evidence">Evidence: {row.evidence}</span></td><td>{row.validation}</td></tr>)}</tbody></table></div>
      </section>
      <section className="d7-output" aria-labelledby="correlation-heading">
        <h4 id="correlation-heading">02 · Correlation Luna đề xuất</h4>
        {guidance.correlations.length ? <div className="table-wrap"><table className="d7-table"><caption>Phân tích extract và inject dữ liệu động bởi Luna</caption><thead><tr><th>Script / Biến động</th><th>Nguồn → Đích</th><th>Hiện trạng & evidence</th><th>Đề xuất xử lý</th></tr></thead><tbody>{guidance.correlations.map((row, index) => <tr key={index}><td><strong>{scriptLabel(row.script)}</strong><code>{row.variable}</code>{confidence(row.confidence)}</td><td><span className="d7-direction">Lấy từ</span>{row.extractFrom}<span className="d7-direction">Gửi vào</span>{row.injectInto}</td><td><p>{row.finding}</p><span className="d7-evidence">Evidence: {row.evidence}</span></td><td>{row.suggestion}</td></tr>)}</tbody></table></div> : <p className="muted">Luna không tìm thấy correlation cần đề xuất. Xem giới hạn evidence bên dưới.</p>}
      </section>
      {guidance.limitations.length > 0 && <aside className="d7-limitations"><h4>Giới hạn evidence do Luna ghi nhận</h4><ul>{guidance.limitations.map((item, index) => <li key={index}>{item}</li>)}</ul></aside>}
    </> : <div className="d7-result" role="status"><p>{guidance.standard ? 'Kết quả D7 cũ dùng template cố định. Bấm tạo đề xuất để Luna phân tích lại và lập bảng mới.' : 'Chưa có đề xuất D7. Bấm nút bên dưới để Luna phân tích hai script.'}</p></div>}
    <div className="ai-connection">
      {auth?.signedIn && auth.planEnabled ? <p className="connected">Đã kết nối ChatGPT{auth.email ? `: ${auth.email}` : ''}. Luna 5.6 · medium sẽ phân tích source và smoke evidence.</p> : <p className="muted">Kết nối ChatGPT để Luna tạo bảng đề xuất D7.</p>}
      <div className="ai-actions">
        {auth?.planEnabled ? <button className="primary-action" onClick={generate} disabled={loading}>{loading ? 'Luna đang phân tích…' : 'Tạo gợi ý D7 bằng Luna'}</button> : <button className="primary-action" onClick={continueWithChatGPT} disabled={loading}>Continue with ChatGPT</button>}
      </div>
    </div>
    {error && <p className="error inline-alert" role="alert">{error}</p>}
  </section>;
}

function AuditDashboard({ audit, onAudit, auth, refreshAuth }) {
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
      <div className="summary-grid">{audit.scripts.map((script) => <article className={`summary ${script.smoke.pass ? 'summary-pass' : 'summary-fail'}`} key={script.fileName}><div><p>{script.label}</p><strong>{script.finalScore}<small>/10</small></strong></div><span className={script.smoke.pass ? 'run pass-text' : 'run fail-text'}><i aria-hidden="true" />{script.smoke.pass ? 'Smoke pass' : 'Smoke fail'}</span></article>)}</div>
    </section>
    <section className="scoring-panel" aria-labelledby="scoring-heading">
      <div className="panel-heading"><div><p className="eyebrow">02 · Evidence</p><h3 id="scoring-heading">Bảng chấm 10 tiêu chí</h3></div><p className="table-hint"><span className="score pass">1</span> đạt <span className="score fail">0</span> chưa đạt</p></div>
      <div className="table-wrap"><table><caption>Evidence rule engine theo từng tiêu chí và script</caption><thead><tr><th scope="col">#</th><th scope="col">Tiêu chí</th>{audit.scripts.map((script) => <th scope="col" key={script.fileName}>{script.label}</th>)}</tr></thead><tbody>{audit.scripts[0].criteria.map((row, index) => <tr key={row.criterionId}><td className="criterion-number">{row.criterionId}</td><td className="criterion-title"><strong>{row.title}</strong></td>{audit.scripts.map((script) => { const item = script.criteria[index]; return <td key={script.fileName} className="result-cell"><button className="score-button" onClick={() => toggle(script, item)} aria-label={`Chỉnh điểm ${script.label} tiêu chí ${item.criterionId}`} title="Bấm để duyệt lại điểm"><Score value={item.finalScore} /></button>{item.finalScore !== item.autoScore && <small className="human">Đã duyệt thủ công</small>}<strong>{item.message}</strong>{item.line && <span className="line">Source line {item.line}</span>}<span>{item.suggestion}</span></td>; })}</tr>)}</tbody></table></div>
    </section>
    <section className="smoke" aria-labelledby="smoke-heading"><div className="panel-heading"><div><p className="eyebrow">Runtime evidence</p><h3 id="smoke-heading">k6 smoke logs</h3></div><p className="table-hint">Mở từng dòng để xem log.</p></div>{audit.scripts.map((script) => <details key={script.fileName}><summary><span><strong>{script.label}</strong><small>{script.smoke.message}</small></span><span className={script.smoke.pass ? 'run pass-text' : 'run fail-text'}>{script.smoke.pass ? 'Pass' : 'Fail'} · exit {script.smoke.exitCode} · p95 {script.smoke.p95Ms?.toFixed?.(2) ?? 'n/a'} ms</span></summary><pre>{script.smoke.log || 'Không có log.'}</pre></details>)}</section>
    <D7Guidance audit={audit} onAudit={onAudit} auth={auth} refreshAuth={refreshAuth} />
    <AIReview audit={audit} onAudit={onAudit} auth={auth} refreshAuth={refreshAuth} />
    <div className="actions"><div><strong>{changes.length ? `${changes.length} thay đổi chưa lưu` : 'Chưa có thay đổi điểm'}</strong><span>Điểm đã duyệt chỉ được ghi nhận khi bạn lưu.</span></div><div className="action-buttons"><button className="primary-action" onClick={save} disabled={saving || !changes.length}>{saving ? 'Đang lưu…' : 'Lưu điểm đã duyệt'}</button><button className="secondary" onClick={() => onAudit(null)}>Audit mới</button></div></div>
    {active && <div className="review" role="region" aria-label="Ghi lý do chỉnh điểm"><div><p className="eyebrow">Duyệt thủ công</p><p><strong>Ghi lý do chỉnh điểm — tiêu chí {active.criterionId}</strong></p></div><textarea value={reason} onChange={(event) => setReason(event.target.value)} placeholder="Ví dụ: script dùng tên biến khác nhưng vẫn correlation token đúng." /><button className="primary-action" onClick={() => { const clone = structuredClone(audit); const item = clone.scripts.find((script) => script.fileName === editing.fileName).criteria.find((row) => row.criterionId === editing.criterionId); item.overrideReason = reason; onAudit(clone); setEditing(null); setReason(''); }}>Xác nhận lý do</button></div>}
  </section>;
}

export default function App() {
  const [audit, setAudit] = useState(null);
  const [rubric, setRubric] = useState(null);
  const [auth, setAuth] = useState(null);
  const [authNotice, setAuthNotice] = useState('');
  const refreshAuth = () => api('/api/auth/chatgpt/status').then(setAuth).catch(() => setAuth(null));

  useEffect(() => { api('/api/rubric').then(setRubric).catch(() => {}); refreshAuth(); }, []);
  useEffect(() => {
    const result = new URLSearchParams(window.location.search).get('aiAuth');
    if (!result) return;
    setAuthNotice(result === 'success' ? 'Đã kết nối ChatGPT. Bạn có thể thêm AI review cho audit.' : 'Không thể kết nối ChatGPT hoặc bạn đã hủy cấp quyền. Audit vẫn dùng bình thường.');
    window.history.replaceState({}, '', window.location.pathname);
    refreshAuth();
  }, []);

  return <main className="app-shell">
    <header className="hero">
      <div className="brand-mark" aria-hidden="true">k6</div>
      <div><p className="eyebrow">ESHOP · PERFORMANCE SCRIPT AUDIT</p><h1>Kiểm chứng script AI bằng evidence có thể xem lại.</h1><p className="hero-copy">Rule cố định, k6 smoke test và quyết định của người chấm — tách bạch để kết quả dễ tin cậy.</p><div className="hero-meta">{rubric && <span className="badge">{rubric.criteria.length} tiêu chí · tối đa {rubric.maxScore} điểm</span>}<span className="local-badge">Local SUT only</span></div>{authNotice && <p className="auth-notice" role="status">{authNotice}</p>}</div>
    </header>
    {audit ? <AuditDashboard audit={audit} onAudit={setAudit} auth={auth} refreshAuth={refreshAuth} /> : <UploadForm onAudit={setAudit} />}
  </main>;
}
