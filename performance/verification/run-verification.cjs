'use strict';
// Run an unmodified A script against an isolated copy of the selected SUT.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const net = require('node:net');
const crypto = require('node:crypto');
const { spawn, spawnSync } = require('node:child_process');
const { createRequire } = require('node:module');
const root = path.resolve(__dirname, '../..');
const backendRequire = createRequire(path.join(root, 'backend/package.json'));
const sqlite = backendRequire('sqlite3');
const [variant, test] = process.argv.slice(2);
if (!['original','tuned'].includes(variant) || !['smoke','baseline','spike'].includes(test)) {
  throw Error('Usage: node run-verification.cjs original|tuned smoke|baseline|spike');
}
const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const id = `${test}-${variant}-${stamp}`;
const out = path.join(__dirname, 'local-runs', id);
const evidence = path.join(root, 'submission/evidence/assignee-b', id);
const sut = path.join(out, 'sut');
const source = path.join(root, variant === 'original' ? 'backend' : 'tuned-backend');
const dbFile = path.join(sut, variant === 'original' ? 'database.sqlite' : 'database_tuned.sqlite');
const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const write = (file, value) => fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
function command(cmd, args) {
  const r = spawnSync(cmd, args, { cwd: root, encoding: 'utf8', windowsHide: true });
  if (r.error || r.status !== 0) throw r.error || Error(r.stderr || `${cmd}: ${r.status}`);
  return r.stdout.trim();
}
function query(db, sql) { return new Promise((resolve,reject) => db.all(sql, (e,rows) => e ? reject(e) : resolve(rows))); }
async function inspect() {
  const db = await new Promise((resolve,reject) => { const d = new sqlite.Database(dbFile, sqlite.OPEN_READWRITE, e => e ? reject(e) : resolve(d)); });
  try {
    return {
      version: await query(db, 'SELECT sqlite_version() AS version'),
      journal: await query(db, 'PRAGMA journal_mode'),
      indexes: await query(db, "SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='products'"),
      queryPlan: await query(db, "EXPLAIN QUERY PLAN SELECT * FROM products WHERE name LIKE '%iPhone%'"),
      counts: await query(db, 'SELECT (SELECT COUNT(*) FROM users) AS users, (SELECT COUNT(*) FROM products) AS products, (SELECT COUNT(*) FROM orders) AS orders'),
    };
  } finally { await new Promise((resolve,reject) => db.close(e => e ? reject(e) : resolve())); }
}
async function portFree() {
  await new Promise((resolve,reject) => {
    const probe = net.createServer();
    probe.once('error', () => reject(Error('Port 3000 occupied; stop the existing SUT yourself before retrying.')));
    probe.listen(3000, '127.0.0.1', () => probe.close(resolve));
  });
}
async function main() {
  await portFree();
  fs.mkdirSync(sut, { recursive: true });
  fs.mkdirSync(evidence, { recursive: true });
  for (const f of ['server.js','database.js','package.json','package-lock.json']) fs.copyFileSync(path.join(source,f),path.join(sut,f));
  fs.cpSync(path.join(source,'test-data'), path.join(sut,'test-data'), { recursive: true });
  const hashes = {};
  for (const f of ['server.js','database.js','package.json','package-lock.json']) hashes[path.relative(root,path.join(source,f))] = hash(path.join(source,f));
  for (const f of [`performance/k6/${test}.js`, 'performance/k6/data/test_accounts.csv', 'performance/k6/data/seed.js']) hashes[f] = hash(path.join(root,f));
  const sourceDbHashes = {};
  for (const f of ['backend/database.sqlite','tuned-backend/database_tuned.sqlite']) sourceDbHashes[f] = hash(path.join(root,f));
  const metadata = {
    id, variant, test, actor: 'Codex executed in assignee B workspace; not a human cross-run sign-off',
    startUtc: new Date().toISOString(), timezone: 'Asia/Bangkok', commit: command('git',['rev-parse','HEAD']),
    dirtyStatus: command('git',['status','--short']), hashes, sourceDbHashes,
    node: process.version, k6: command('k6',['version']), os: { platform: os.platform(), release: os.release(), arch: os.arch(), cpu: os.cpus()[0].model, logicalCpu: os.cpus().length, totalMemory: os.totalmem(), freeMemory: os.freemem() },
    baseUrl: 'http://localhost:3000', copiedSut: sut, rawMetrics: path.join(out,'metrics.json'),
    dependencies: 'Resolved from existing backend/node_modules via NODE_PATH; original package-lock hashes recorded',
  };
  const serverLog = fs.openSync(path.join(out,'server.log'),'a');
  const server = spawn(process.execPath, [path.join(sut,'server.js')], { cwd: sut, windowsHide: true, env: { ...process.env, NODE_PATH: path.join(root,'backend/node_modules') }, stdio: ['ignore',serverLog,serverLog] });
  let serverError;
  server.on('error', e => { serverError=e; });
  try {
    let ready = false;
    for (let i=0;i<150;i++) {
      if (serverError) throw serverError;
      if (server.exitCode !== null) throw Error(`SUT exited ${server.exitCode}`);
      const log = fs.readFileSync(path.join(out,'server.log'),'utf8');
      if (log.includes('Server is running') && log.includes('Database initialized') && (! (variant === 'tuned') || log.includes('idx_products_name ON products(name)'))) {
        try { const s = await inspect(); if (s.counts[0].products===5 && (variant!=='tuned' || s.indexes.some(r=>r.name==='idx_products_name'))) {ready=true;break;} } catch (_) { /* asynchronous seed not finished */ }
      }
      await new Promise(r=>setTimeout(r,200));
    }
    if (!ready) throw Error('SUT seed/readiness timed out');
    command(process.execPath, ['performance/k6/data/seed.js', dbFile]);
    metadata.before = await inspect();
    if (metadata.before.counts[0].orders !== 0) throw Error('Expected clean orders');
    if (variant==='tuned' && metadata.before.journal[0].journal_mode !== 'wal') throw Error('Tuned WAL missing');
    write(path.join(evidence,'metadata.json'),metadata);
    console.log(`START ${id}: seeded isolated SUT, journal=${metadata.before.journal[0].journal_mode}`);
    const args = ['run','--out',`json=${path.join(out,'metrics.json')}`,'--summary-export',path.join(evidence,'summary.json'),path.join(root,`performance/k6/${test}.js`)];
    const env = { ...process.env, BASE_URL: metadata.baseUrl, K6_NO_COLOR: 'true', K6_WEB_DASHBOARD: test==='baseline'?'true':'false', K6_WEB_DASHBOARD_OPEN:'false', K6_WEB_DASHBOARD_PORT:'0', K6_WEB_DASHBOARD_EXPORT:path.join(out,'baseline_report.html') };
    const log = fs.createWriteStream(path.join(evidence,'k6.log'));
    const result = await new Promise((resolve,reject) => {
      const child = spawn('k6',args,{cwd:root,env,windowsHide:true});
      child.stdout.pipe(log,{end:false}); child.stderr.pipe(log,{end:false});
      child.once('error',reject); child.once('close',(code,signal)=>resolve({code,signal}));
    });
    await new Promise(r=>log.end(r));
    metadata.exit = result;
    metadata.after = await inspect();
    metadata.endUtc = new Date().toISOString();
    metadata.sourceDbUnchanged = Object.entries(sourceDbHashes).every(([f,h])=>hash(path.join(root,f))===h);
    write(path.join(evidence,'metadata.json'),metadata);
    fs.copyFileSync(path.join(out,'server.log'),path.join(evidence,'server.log'));
    console.log(`END ${id}: k6 exit=${result.code}; source DB unchanged=${metadata.sourceDbUnchanged}`);
    if (![0,99].includes(result.code)) throw Error(`k6 infrastructure error: ${result.code}`);
    if (!metadata.sourceDbUnchanged) throw Error('Source DB changed during run');
  } finally {
    if (server.exitCode===null) {
      await new Promise(resolve => { server.once('exit',resolve); server.kill(); });
    }
    fs.closeSync(serverLog);
  }
}
main().catch(e=>{console.error(e);process.exitCode=1;});
