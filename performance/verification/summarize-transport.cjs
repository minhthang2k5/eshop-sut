'use strict';
// Stream raw metrics after load has stopped; never count multiple metrics per request.
const fs=require('node:fs');
const path=require('node:path');
const readline=require('node:readline');
const evidence=path.resolve(__dirname,'../../submission/evidence/assignee-b');
async function main() {
  const rows=[];
  for(const entry of fs.readdirSync(evidence,{withFileTypes:true})) {
    if(!entry.isDirectory())continue;
    const meta=JSON.parse(fs.readFileSync(path.join(evidence,entry.name,'metadata.json'),'utf8'));
    if(!meta.endUtc)continue;
    const counts={}; let requests=0;
    for await(const line of readline.createInterface({input:fs.createReadStream(meta.rawMetrics),crlfDelay:Infinity})) {
      const p=JSON.parse(line);
      if(p.type!=='Point'||p.metric!=='http_reqs')continue;
      const t=p.data.tags; const key=JSON.stringify({phase:t.phase||'smoke',endpoint:t.endpoint||t.name,status:t.status,errorCode:t.error_code||null,error:t.error||null});
      counts[key]=(counts[key]||0)+p.data.value; requests+=p.data.value;
    }
    const summary=JSON.parse(fs.readFileSync(path.join(evidence,entry.name,'summary.json'),'utf8'));
    const count=(summary.metrics.http_reqs.values||summary.metrics.http_reqs).count;
    if(count!==requests)throw Error(`Raw count mismatch ${entry.name}`);
    rows.push({id:entry.name,requests,groups:Object.entries(counts).map(([k,count])=>({...JSON.parse(k),count}))});
  }
  fs.writeFileSync(path.join(evidence,'transport-summary.json'),JSON.stringify(rows,null,2)+'\n');
  for(const r of rows) {
    const errors=r.groups.filter(g=>g.status!=='200');
    const byCode={};for(const e of errors)byCode[e.errorCode]=(byCode[e.errorCode]||0)+e.count;
    console.log(JSON.stringify({id:r.id,requests:r.requests,errorCount:errors.reduce((n,g)=>n+g.count,0),byCode,examples:[...new Set(errors.map(g=>g.error))]}));
  }
}
main().catch(e=>{console.error(e);process.exitCode=1;});
