import { rubric } from './rubric.js';
import { analyzeSource } from './source-analysis.js';

function lineFor(source, matcher) {
  const index = source.search(matcher);
  return index < 0 ? null : source.slice(0, index).split('\n').length;
}

function evidence(pass, message, source, matcher, suggestion) {
  const line = lineFor(source, matcher);
  return { pass, message, suggestion, line: line ?? undefined };
}

function criterion(id, source, analysis) {
  switch (id) {
    case 1: {
      const required = analysis.endpointsValid;
      const forbidden = [/\/api\/auth\//, /\/api\/orders\b/].filter((pattern) => pattern.test(source));
      return evidence(required && forbidden.length === 0,
        forbidden.length ? 'Có endpoint không thuộc spec (ví dụ /api/auth/login hoặc /api/orders).' : required ? 'Dùng đúng nhóm endpoint EShop.' : 'Thiếu ít nhất một endpoint của flow.',
        source, /\/api\//, 'Dùng POST /api/login, GET /api/products, GET /api/products/:id và POST /api/checkout.');
    }
    case 2: {
      const login = analysis.methodsValid;
      const checkout = analysis.methodsValid;
      const json = analysis.methodsValid;
      return evidence(login && checkout && json, login && checkout && json ? 'Login và checkout có JSON body bắt buộc.' : 'Thiếu POST/body JSON hoặc trường bắt buộc.', source, /http\.post/, 'Dùng http.post(..., JSON.stringify({...}), { headers: { "Content-Type": "application/json" } }).');
    }
    case 3: {
      return evidence(analysis.flowValid, analysis.flowValid ? 'Có guard dừng flow khi thiếu token lấy từ login.' : 'Chưa xác nhận guard dừng flow khi login thiếu token.', source, /\/api\/login/, 'Chỉ gọi checkout trong nhánh token hợp lệ sau login.');
    }
    case 4: {
      const extracts = analysis.correlation;
      const bearer = analysis.correlation;
      return evidence(extracts && bearer, extracts && bearer ? 'Trích xuất token và truyền Authorization Bearer.' : 'Không thấy correlation token hoặc Bearer header đúng.', source, /token|Authorization/, 'Lấy loginRes.json("token") rồi đặt Authorization: `Bearer ${token}` khi checkout.');
    }
    case 5: {
      const valid = analysis.thinkTimeValid;
      return evidence(valid, valid ? 'Có think-time random đúng khoảng cho search/detail/checkout.' : 'Chưa xác nhận think-time random đúng khoảng cho cả ba nhánh.', source, /sleep\s*\(/, 'Dùng random 1–3s cho search, 2–5s cho detail, 3–6s cho checkout.');
    }
    case 6: {
      const randomBranch = analysis.workload;
      return evidence(randomBranch, randomBranch ? 'Có nhánh random với ngưỡng 55% và 80%.' : 'Không nhận diện được phân phối 55%/25%/20%.', source, /Math\.random|0\.55/, 'Dùng r < 0.55 cho search, r < 0.80 cho detail, còn lại checkout.');
    }
    case 7: {
      const keywords = ['iPhone', 'Samsung', 'MacBook', 'AirPods', 'Keychron'].every((keyword) => source.includes(keyword));
      const randomId = analysis.parameterization;
      return evidence(keywords && randomId, keywords && randomId ? 'Keyword và product ID được parameterize.' : 'Thiếu tập keyword chuẩn hoặc product ID random 1–5.', source, /iPhone|Math\.floor/, 'Khai báo mảng 5 keyword và dùng Math.floor(Math.random() * 5) + 1 cho product ID.');
    }
    case 8: {
      const status = analysis.checksValid;
      const token = analysis.checksValid;
      const orderId = analysis.checksValid;
      return evidence(status && token && orderId, status && token && orderId ? 'Có check status, token và orderId.' : 'Thiếu check status 200, token hoặc orderId.', source, /check\s*\(/, 'Thêm check cho login status/token, response product và checkout status/orderId.');
    }
    case 9: {
      const p95 = analysis.thresholdsValid;
      const checks = analysis.thresholdsValid;
      return evidence(p95 && checks, p95 && checks ? 'Có ngưỡng p95 và check rate SLO.' : 'Thiếu p95<500 hoặc checks rate>=0.99.', source, /thresholds|p\(95\)/, "Thêm thresholds: { http_req_duration: ['p(95)<500'], checks: ['rate>=0.99'] }.");
    }
    default:
      return evidence(false, 'Đang chờ kết quả k6 smoke.', source, /export\s+default/, 'Chạy smoke test để chấm tiêu chí này.');
  }
}

export function scanSource(source) {
  let analysis;
  try { analysis = analyzeSource(source); }
  catch (error) { return rubric.criteria.slice(0, 9).map((item) => ({ criterionId: item.id, pass: false, message: `Không phân tích được JavaScript: ${error.message}`, suggestion: 'Sửa cú pháp trước khi chấm lại.', line: error.loc?.line })); }
  return rubric.criteria.slice(0, 9).map((item) => {
    const result = criterion(item.id, analysis.code, analysis);
    return { criterionId: item.id, ...result, reviewRequired: !result.pass, message: !result.pass ? `${result.message} Cần đối chiếu source trước khi kết luận sai.` : result.message };
  });
}

export function validateScriptSafety(source, baseUrl) {
  const imports = [...source.matchAll(/from\s+['"]([^'"]+)['"]/g)].map((m) => m[1]);
  const invalidImport = imports.find((value) => value !== 'k6' && !value.startsWith('k6/'));
  if (invalidImport) return `Import không cho phép: ${invalidImport}. Chỉ chấp nhận module k6.`;
  const urls = [...source.matchAll(/https?:\/\/[^'"`\s)]+/g)].map((m) => m[0]);
  const foreignUrl = urls.find((url) => !url.startsWith(baseUrl));
  if (foreignUrl) return `URL ngoài SUT không được phép: ${foreignUrl}`;
  return null;
}
