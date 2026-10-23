import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createChatGPTAuth } from './chatgpt-auth.js';

async function fixture(t) {
  const authRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'script-audit-auth-test-'));
  t.after(() => fs.rm(authRoot, { recursive: true, force: true }));
  const file = path.join(authRoot, 'profile.json');
  await fs.writeFile(file, JSON.stringify({ scope: 'chatgpt.tokens.use.direct', accessToken: 'fake-access', refreshToken: 'fake-refresh', clientId: 'test', expiresAt: 0 }));
  await fs.writeFile(path.join(authRoot, 'host.json'), JSON.stringify({ id: 'test-host' }));
  return { file, authRoot, auth: createChatGPTAuth({ authRoot, port: 4000, frontendOrigin: 'http://localhost:5175' }) };
}

test('logout disconnects the app, preserves host identity, and can be repeated', async (t) => {
  const { auth, file, authRoot } = await fixture(t);
  assert.equal((await auth.publicStatus()).signedIn, true);
  assert.deepEqual(await auth.logout(), { signedIn: false, planEnabled: false });
  await assert.rejects(fs.readFile(file), { code: 'ENOENT' });
  assert.equal(JSON.parse(await fs.readFile(path.join(authRoot, 'host.json'))).id, 'test-host');
  await auth.logout();
  await assert.rejects(auth.tokenForPlan(), /Continue with ChatGPT/);
});

test('an in-flight token refresh cannot restore a logged-out profile', async (t) => {
  const { auth, file } = await fixture(t);
  let release;
  let started;
  const fetching = new Promise((resolve) => { started = resolve; });
  t.mock.method(globalThis, 'fetch', async () => {
    started();
    return new Promise((resolve) => { release = () => resolve(new Response(JSON.stringify({ access_token: 'refreshed', expires_in: 3600 }))); });
  });
  const refreshing = auth.tokenForPlan();
  const rejection = assert.rejects(refreshing, /đăng xuất/);
  await fetching;
  await auth.logout();
  release();
  await rejection;
  await auth.markModel('test');
  await assert.rejects(fs.readFile(file), { code: 'ENOENT' });
});
