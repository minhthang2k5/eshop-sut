// Focused runtime branches with HTTP/clock stubs; no load or live database needed.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'baseline.js'), 'utf8').replace(/^import .*;$/gm, '').replace('export const options', 'const options').replace('export default function ()', 'function iteration()');
const accountCsv = fs.readFileSync(path.join(root, 'data/test_accounts.csv'), 'utf8');
function harness({accounts = accountCsv, random = .9, login = 'ok', protectedStatus = 200, badBody = false} = {}) {
  let now = 1000;
  const requests = [], sleeps = [], checks = [], skipped = [];
  const context = {
    __ENV: {BASE_URL: 'http://sut///'}, console: {log() {}},
    Date: {now: () => now}, Math: {random: () => random},
    exec: {vu: {idInTest: 1}, scenario: {startTime: 1000}},
    open: file => file.includes('accounts') ? accounts : fs.readFileSync(path.join(root, file), 'utf8'),
    SharedArray: class {constructor(_, callback) {return callback();}},
    Counter: class {add(value, tags) {skipped.push({value,tags});}},
    sleep: value => sleeps.push(value),
    check(response, rules, tags) {const valid = Object.values(rules).every(fn => fn(response)); checks.push({valid,tags}); return valid;},
    http: {
      expectedStatuses() {}, setResponseCallback() {},
      post(url, payload, params) {
        requests.push({url,params,payload:JSON.parse(payload)});
        if (url.endsWith('/login')) {
          now = 62000; // login crosses ramp_up -> steady
          return {status: login === 'timeout' ? 0 : 200, json() {
            if (login === 'json') throw Error('invalid JSON');
            return login === 'empty' ? {token:''} : {token:'token'};
          }};
        }
        return {status: protectedStatus, json: () => badBody ? {} : url.endsWith('/cart') ? {message:'Added to cart'} : {orderId:1}};
      },
      get(url, params) {
        requests.push({url,params});
        const product = {id:1,name:'iPhone 15 Pro Max',price:30000000};
        return {status:200,json: () => badBody ? (url.includes('?') ? [null] : {}) : url.includes('?') ? [product] : product};
      },
    },
  };
  vm.createContext(context); vm.runInContext(source, context);
  return {run: () => vm.runInContext('iteration()', context), requests,sleeps,checks,skipped,context};
}
for (const login of ['json','empty','timeout']) {
  const h = harness({login}); h.run();
  assert.equal(h.requests.length,1); assert.equal(h.skipped[0].value,1);
  assert.equal(h.checks[0].valid,false); assert.equal(h.sleeps.length,1);
}
const h = harness({protectedStatus:401}); h.run(); h.run();
assert.equal(h.requests.filter(r => r.url.endsWith('/login')).length,2);
assert.equal(h.requests[0].params.tags.phase,'ramp_up');
assert.equal(h.requests[1].params.tags.phase,'steady');
assert.equal(h.requests[1].url,'http://sut/api/cart');
assert.equal(h.skipped[0].tags.phase,'steady');
assert.equal(h.requests.length,4); // no write retry within an iteration
for (const random of [.1,.6,.9,.99]) {
  const h = harness({random}); h.run();
  assert.ok(h.checks.every(c => c.valid)); assert.equal(h.sleeps.length,1);
}
for (const random of [.1,.6,.9,.99]) {
  const h = harness({random, badBody:true}); h.run();
  assert.equal(h.checks.at(-1).valid,false); assert.equal(h.sleeps.length,1);
}
const cached = harness(); cached.run(); cached.run();
assert.equal(cached.requests.filter(r => r.url.endsWith('/login')).length,1);
const last = harness(); last.context.exec.vu.idInTest = 50; last.run();
assert.equal(last.requests[0].payload.email, accountCsv.split('\n')[50].split(',')[0]);
assert.throws(() => harness({accounts:accountCsv.split('\n').slice(0,50).join('\n')}), /at least 50/);
assert.throws(() => harness({accounts:accountCsv + accountCsv.split('\n')[1]+'\n'}), /duplicate/);
const quoted = accountCsv.replace(/^(.*)$/m, '\uFEFF$1').replace(/,([^,\n]+),user/, ',"Name, with ""quote""",user');
harness({accounts:quoted}).run();
console.log('Baseline runtime: fixture, 4 endpoints, login failures, pacing, 401 and phase boundary OK');
