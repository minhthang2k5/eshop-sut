import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRemoteJWKSet, jwtVerify } from 'jose';

const ISSUER = 'https://auth.openai.com';
const AUTHORIZE_URL = 'https://auth.openai.com/api/accounts/authorize';
const TOKEN_URL = 'https://auth.openai.com/api/accounts/oauth/token';
const JWKS = createRemoteJWKSet(new URL('https://auth.openai.com/.well-known/jwks.json'));
const RESOURCE = 'https://api.openai.com/v1';
const SCOPES = 'openid profile email offline_access resource.invoke chatgpt.tokens.use.direct';
const DYNAMIC_CLIENT_ID = 'dynamic_agent_client';
const pending = new Map();

function b64url(bytes) { return Buffer.from(bytes).toString('base64url'); }
function now() { return Date.now(); }
function scopesFrom(value) { return String(value || '').split(/\s+/).filter(Boolean); }
async function readJson(file, fallback = null) {
  try { return JSON.parse(await fs.readFile(file, 'utf8')); } catch (error) { if (error.code === 'ENOENT') return fallback; throw error; }
}
async function writePrivateJson(file, value) {
  const temporary = `${file}.${crypto.randomUUID()}.tmp`;
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(temporary, JSON.stringify(value, null, 2), { mode: 0o600 });
  await fs.rename(temporary, file);
}

export function createChatGPTAuth({ authRoot, port, frontendOrigin }) {
  const hostFile = path.join(authRoot, 'host.json');
  const profileFile = path.join(authRoot, 'profile.json');
  const redirectUri = `http://127.0.0.1:${port}/auth/callback`;
  async function hostId() {
    const stored = await readJson(hostFile);
    if (stored?.id) return stored.id;
    const id = `urn:uuid:${crypto.randomUUID()}`;
    await writePrivateJson(hostFile, { id, createdAt: new Date().toISOString() });
    return id;
  }
  async function profile() { return readJson(profileFile); }
  function publicProfile(value) {
    if (!value) return { signedIn: false, planEnabled: false };
    const scopes = scopesFrom(value.scope);
    return { signedIn: true, planEnabled: scopes.includes('chatgpt.tokens.use.direct'), email: value.identity?.email || null, name: value.identity?.name || null, expiresAt: value.expiresAt, model: value.lastModel || null };
  }
  async function start() {
    const saved = await profile();
    const state = b64url(crypto.randomBytes(32));
    const nonce = b64url(crypto.randomBytes(32));
    const verifier = b64url(crypto.randomBytes(64));
    const challenge = b64url(crypto.createHash('sha256').update(verifier).digest());
    const existingClient = saved?.clientId || null;
    pending.set(state, { nonce, verifier, clientId: existingClient || DYNAMIC_CLIENT_ID, isInitial: !existingClient, createdAt: now() });
    for (const [key, item] of pending) if (now() - item.createdAt > 10 * 60_000) pending.delete(key);
    const query = new URLSearchParams({ response_type: 'code', client_id: existingClient || DYNAMIC_CLIENT_ID, redirect_uri: redirectUri, scope: SCOPES, resource: RESOURCE, state, nonce, code_challenge: challenge, code_challenge_method: 'S256' });
    if (existingClient && saved?.idToken) query.set('id_token_hint', saved.idToken);
    if (!existingClient) { query.set('agent_name_hint', 'Eshop k6 Script Audit'); query.set('ext_agent_host_id', await hostId()); }
    return `${AUTHORIZE_URL}?${query}`;
  }
  async function exchangeCallback(params) {
    const state = String(params.state || '');
    const item = pending.get(state);
    pending.delete(state);
    if (!item || now() - item.createdAt > 10 * 60_000) throw new Error('Phiên đăng nhập đã hết hạn. Hãy thử lại.');
    if (params.error) throw new Error('Bạn đã không hoàn tất cấp quyền ChatGPT.');
    if (!params.code) throw new Error('ChatGPT không trả authorization code.');
    const issuedClientId = item.isInitial ? String(params.client_id || '') : item.clientId;
    if (!issuedClientId || issuedClientId === DYNAMIC_CLIENT_ID) throw new Error('ChatGPT chưa cấp client ID cho ứng dụng local này.');
    const body = new URLSearchParams({ grant_type: 'authorization_code', client_id: issuedClientId, code: String(params.code), code_verifier: item.verifier, redirect_uri: redirectUri, resource: RESOURCE });
    const response = await fetch(TOKEN_URL, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
    if (!response.ok) throw new Error(`Không thể đổi mã đăng nhập (${response.status}).`);
    const tokens = await response.json();
    if (!tokens.id_token) throw new Error('ChatGPT không trả ID token để xác thực danh tính.');
    const { payload } = await jwtVerify(tokens.id_token, JWKS, { issuer: ISSUER, audience: issuedClientId, requiredClaims: ['sub', 'exp', 'iat'], clockTolerance: 5 });
    if (payload.nonce !== item.nonce) throw new Error('Nonce đăng nhập không khớp.');
    const scope = tokens.scope || SCOPES;
    const value = { clientId: issuedClientId, identity: { sub: payload.sub, email: typeof payload.email === 'string' ? payload.email : null, name: typeof payload.name === 'string' ? payload.name : null }, accessToken: tokens.access_token, refreshToken: tokens.refresh_token, idToken: tokens.id_token, scope, expiresAt: now() + Number(tokens.expires_in || 3600) * 1000, savedAt: new Date().toISOString() };
    await writePrivateJson(profileFile, value);
    return publicProfile(value);
  }
  async function tokenForPlan() {
    let saved = await profile();
    if (!saved) throw new Error('Hãy Continue with ChatGPT trước.');
    if (!scopesFrom(saved.scope).includes('chatgpt.tokens.use.direct')) throw new Error('Tài khoản chưa cấp quyền dùng ChatGPT plan cho AI review.');
    if (saved.accessToken && saved.expiresAt > now() + 60_000) return { accessToken: saved.accessToken, profile: saved };
    if (!saved.refreshToken) throw new Error('Phiên ChatGPT đã hết hạn; hãy đăng nhập lại.');
    const body = new URLSearchParams({ grant_type: 'refresh_token', client_id: saved.clientId, refresh_token: saved.refreshToken, resource: RESOURCE });
    const response = await fetch(TOKEN_URL, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
    if (!response.ok) throw new Error('Không thể làm mới phiên ChatGPT; hãy đăng nhập lại.');
    const tokens = await response.json();
    saved = { ...saved, accessToken: tokens.access_token, refreshToken: tokens.refresh_token || saved.refreshToken, idToken: tokens.id_token || saved.idToken, scope: tokens.scope || saved.scope, expiresAt: now() + Number(tokens.expires_in || 3600) * 1000, savedAt: new Date().toISOString() };
    await writePrivateJson(profileFile, saved);
    return { accessToken: saved.accessToken, profile: saved };
  }
  async function availableModels(accessToken) {
    const response = await fetch(`${RESOURCE}/models`, { headers: { Authorization: `Bearer ${accessToken}` } });
    if (!response.ok) throw new Error(`Không lấy được model ChatGPT (${response.status}).`);
    const payload = await response.json();
    return (payload.models || []).filter((model) => model.visibility === 'list' && model.slug);
  }
  async function markModel(model) { const saved = await profile(); if (saved) await writePrivateJson(profileFile, { ...saved, lastModel: model }); }
  function callbackRedirect(success) { return `${frontendOrigin}/?aiAuth=${success ? 'success' : 'failed'}`; }
  return { publicStatus: async () => publicProfile(await profile()), start, exchangeCallback, tokenForPlan, availableModels, markModel, callbackRedirect };
}
