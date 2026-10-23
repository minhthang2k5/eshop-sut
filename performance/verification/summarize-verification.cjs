'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const evidence = path.resolve(__dirname, '../../submission/evidence/assignee-b');
function metric(summary, name) {
  const m = summary.metrics[name];
  return m && (m.values || m);
}
function stats(s, filter, seconds) {
  const suffix = filter ? `{${filter}}` : '';
  const count = metric(s, 'http_reqs'+suffix)?.count;
  const d = metric(s, 'http_req_duration'+suffix);
  const failed = metric(s, 'http_req_failed'+suffix);
  const checks = metric(s, 'checks'+suffix);
  if (!Number.isFinite(count) || !d || !failed) return null;
  return { count, p50:d.med, p95:d['p(95)'], p99:d['p(99)'], errorPct:100*failed.value,
    checksPct:checks ? 100*checks.value : null, rps: seconds ? count/seconds : null,
    slo: { latency:d['p(95)']<500, httpErrors:failed.value<0.01, checks:checks ? checks.value>=0.99 : null, hasSamples:count>0 } };
}
function analyze(s, test) {
  const phases = test==='baseline' ? { steady:300 } : test==='spike' ? { hold_50:30, hold_1500:60, recovery_1:60 } : {};
  const result = { all:stats(s,'',null), login:stats(s,'endpoint:login',null), phases:{}, thresholds:[] };
  for (const [phase,seconds] of Object.entries(phases)) {
    const skipped = metric(s, test==='baseline' ? 'business_requests_skipped' : `business_requests_skipped{phase:${phase}}`)?.count;
    result.phases[phase] = { seconds, total:stats(s,`phase:${phase}`,seconds), skipped, byEndpoint:{} };
    for (const endpoint of ['search','detail','cart','checkout','login']) {
      result.phases[phase].byEndpoint[endpoint] = stats(s,`phase:${phase},endpoint:${endpoint}`,seconds);
    }
    const p = result.phases[phase];
    p.businessCount = ['search','detail','cart','checkout'].reduce((n,k)=>n+(p.byEndpoint[k]?.count||0),0);
    p.businessRps = p.businessCount/seconds;
    if (p.total && !p.byEndpoint.login) {
      // Stress/spike do not export phase+login submetrics. Only five endpoints exist.
      p.byEndpoint.login = { count:p.total.count-p.businessCount, inferredFromTotalMinusBusiness:true, p50:null,p95:null,p99:null,errorPct:null };
    }
    if (p.total && (p.byEndpoint.login.count<0 || p.businessCount+p.byEndpoint.login.count!==p.total.count)) throw Error(`Count mismatch in ${phase}`);
  }
  // Legacy export booleans mean threshold violated; newer export may expose {ok}.
  for (const [name,m] of Object.entries(s.metrics)) {
    for (const [condition,t] of Object.entries(m.thresholds || {})) {
      result.thresholds.push({ metric:name, condition, passed:typeof t==='boolean' ? !t : t.ok===true });
    }
  }
  result.thresholdPass = result.thresholds.every(t=>t.passed);
  return result;
}
if (require.main===module) {
  const runs = [];
  for (const entry of fs.readdirSync(evidence,{withFileTypes:true})) {
    if (!entry.isDirectory()) continue;
    const dir = path.join(evidence,entry.name);
    if (!fs.existsSync(path.join(dir,'summary.json'))) continue;
    const meta = JSON.parse(fs.readFileSync(path.join(dir,'metadata.json'),'utf8'));
    if (!meta.endUtc) continue;
    runs.push({ id:meta.id, variant:meta.variant, test:meta.test, exit:meta.exit, startUtc:meta.startUtc, endUtc:meta.endUtc,
      ...analyze(JSON.parse(fs.readFileSync(path.join(dir,'summary.json'),'utf8')),meta.test) });
  }
  const refs = {
    baseline_original:'baseline-20261022-110446-eGLTX1', baseline_tuned:'baseline-20261023-084311-TSxg2P',
    spike_original:'spike-20261022-190641-UgVeF4', spike_tuned:'spike-20261023-085706-BOOKoc',
  };
  const reference = {};
  for (const [key,id] of Object.entries(refs)) reference[key]={id,...analyze(JSON.parse(fs.readFileSync(path.resolve(__dirname,'../k6/output',id,'summary.json'),'utf8')),key.split('_')[0])};
  fs.writeFileSync(path.join(evidence,'verification-summary.json'),JSON.stringify({runs,reference},null,2)+'\n');
  const files = [];
  function walk(dir) { for (const e of fs.readdirSync(dir,{withFileTypes:true})) { const p=path.join(dir,e.name); if(e.isDirectory())walk(p);else if(e.name!=='SHA256SUMS.txt') files.push(p); } }
  walk(evidence);
  fs.writeFileSync(path.join(evidence,'SHA256SUMS.txt'),files.sort().map(f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')+'  '+path.relative(evidence,f).replace(/\\/g,'/')).join('\n')+'\n');
  console.log(JSON.stringify(runs.map(r=>({id:r.id,pass:r.thresholdPass,all:r.all,phases:r.phases})),null,2));
}
module.exports={metric,stats,analyze};
