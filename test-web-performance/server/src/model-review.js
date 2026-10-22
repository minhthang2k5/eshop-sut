function evidenceForModel({ scripts, baseUrl, rubric }) {
  return {
    baseUrl,
    rubric: { id: rubric.id, version: rubric.version, criteria: rubric.criteria.map(({ id, title, hint }) => ({ id, title, hint })) },
    scripts: scripts.map(({ label, fileName, criteria, smoke, source }) => ({ label, fileName, source: source.slice(0, 20_000), criteria, smoke: { ...smoke, log: (smoke.log || '').slice(-2_000) } }))
  };
}

function describeFailure(status, body) {
  let detail = '';
  try { const parsed = JSON.parse(body); detail = parsed.error?.message || parsed.detail || ''; } catch { /* HTTP status is enough. */ }
  return `ChatGPT không thể hoàn tất review (${status})${detail ? `: ${String(detail).slice(0, 180)}` : '.'}`;
}

function networkMessage(error) {
  const code = error?.cause?.code || error?.code;
  if (code === 'ENOTFOUND') return 'Backend không phân giải được api.openai.com (DNS/proxy). Hãy kiểm tra Internet hoặc cấu hình proxy của mạng.';
  if (code === 'ECONNREFUSED' || code === 'ECONNRESET' || code === 'ETIMEDOUT') return `Backend không kết nối được OpenAI (${code}). Hãy kiểm tra firewall, VPN hoặc proxy.`;
  return `Backend không kết nối được OpenAI${code ? ` (${code})` : ''}.`;
}

async function requestWithRetry(url, options) {
  let lastError;
  for (let attempt = 0; attempt < 2; attempt += 1) {
    try { return await fetch(url, options); } catch (error) {
      lastError = error;
      if (attempt === 0) await new Promise((resolve) => setTimeout(resolve, 700));
    }
  }
  throw new Error(networkMessage(lastError));
}

export async function createPlanModelReview({ accessToken, model, reasoningEffort, scripts, baseUrl, rubric }) {
  const response = await requestWithRetry('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: { Authorization: `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      reasoning: { effort: reasoningEffort },
      store: false,
      stream: true,
      instructions: 'Bạn là reviewer hỗ trợ cho bài audit k6. Trả lời bằng tiếng Việt, ngắn gọn và dựa DUY NHẤT trên evidence được cung cấp. Không tự chấm điểm, không thay đổi bất kỳ điểm nào. Nêu: (1) tóm tắt chất lượng mỗi script, (2) 1-3 rủi ro hoặc cải thiện cụ thể có thể kiểm tra được, (3) điều gì evidence hiện tại chưa chứng minh. Không đưa secrets, không suy đoán về HAR.',
      input: [{
        role: 'user',
        content: `Audit evidence JSON:\n${JSON.stringify(evidenceForModel({ scripts, baseUrl, rubric }))}`
      }]
    })
  });
  if (!response.ok) throw new Error(describeFailure(response.status, await response.text()));
  if (!response.body) throw new Error('ChatGPT không mở được luồng phản hồi.');

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let text = '';
  let completed = false;
  let failure = '';
  const handleEvent = (block) => {
    const data = block.split('\n').filter((line) => line.startsWith('data:')).map((line) => line.slice(5).trim()).join('\n');
    if (!data || data === '[DONE]') return;
    let event;
    try { event = JSON.parse(data); } catch { return; }
    if (event.type === 'response.output_text.delta') text += event.delta || '';
    if (event.type === 'response.completed') completed = true;
    if (event.type === 'response.failed') failure = event.response?.error?.message || 'ChatGPT đánh dấu review thất bại.';
  };
  while (true) {
    const { done, value } = await reader.read();
    buffer += decoder.decode(value || new Uint8Array(), { stream: !done }).replaceAll('\r\n', '\n');
    const blocks = buffer.split('\n\n');
    buffer = blocks.pop() || '';
    blocks.forEach(handleEvent);
    if (done) break;
  }
  if (buffer.trim()) handleEvent(buffer);
  if (failure) throw new Error(failure);
  if (!completed) throw new Error('Luồng ChatGPT kết thúc trước khi xác nhận hoàn tất.');
  return { status: 'complete', model, reasoningEffort, text: text.trim() || 'ChatGPT đã hoàn tất nhưng không trả nội dung.' };
}
