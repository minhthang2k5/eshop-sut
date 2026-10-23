// Rasterize the inline SVG charts in the submitted HTML; never sends load.
// Needs Node.js + sharp. Run from any working directory: node render_figures.cjs
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('sharp');
const root = __dirname;
const colors = ['#a14d17', '#146bba'];
const esc = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
function svgs(file) {
  return fs.readFileSync(path.join(root, 'html', file), 'utf8').match(/<svg\b[\s\S]*?<\/svg>/g);
}
const tuned = svgs('tuned_baseline_report.html');
const tasks = [
 ['01-baseline-percentiles.png','Baseline · percentile tổng steady', [tuned[0]], true,
  ['baseline-20261022-110446-eGLTX1 → baseline-20261023-084311-TSxg2P', 'Nguồn: summary.json · phase:steady · 50 VUs × 300s · latency ms']],
 ['02-baseline-api.png','Baseline · p95 theo API trong steady', [tuned[1]], true,
  ['baseline-20261022-110446-eGLTX1 → baseline-20261023-084311-TSxg2P', 'Nguồn: summary.json · phase:steady · latency ms; các API đều dưới SLO 500 ms']],
 ['03-stress-before.png','Stress trước tune · p95 theo plateau/recovery', [svgs('stress_report.html')[1]], false,
  ['stress-20261022-181718-lx8F4c · mỗi plateau/recovery 60s', 'Nguồn: summary.json · R50 = recovery 50 VUs · đường nối các mẫu tổng hợp']],
 ['04-spike-before.png','Spike trước tune · p95 theo phase', [svgs('spike_report.html')[1]], false,
  ['spike-20261022-190641-UgVeF4 · nền 30s / đỉnh 60s / recovery 60s', 'Nguồn: summary.json · R50 = recovery 50 VUs · không phải chuỗi thời gian']],
 ['05-stress-comparison.png','Stress · so sánh trước và sau tune', [tuned[2],tuned[3],tuned[4]], true,
  ['stress-20261022-181718-lx8F4c → stress-20261023-090531-KgTWyh', 'Nguồn: summary.json · hold 60s/bậc · RPS = count/60 · tổng gồm Login', 'Trục latency log10 · các đường nối mẫu tổng hợp; recovery xem bảng báo cáo']],
 ['06-spike-comparison.png','Spike · so sánh trước và sau tune', [tuned[5],tuned[6],tuned[7]], true,
  ['spike-20261022-190641-UgVeF4 → spike-20261023-085706-BOOKoc', 'Nguồn: summary.json · nền 30s / đỉnh 60s / recovery 60s · tổng gồm Login', 'Trục latency log10 · RPS = count/thời lượng phase · không phải chuỗi thời gian']],
];
(async () => {
 for (const [name,title,charts,legend,notes] of tasks) {
  let y = legend ? 116 : 78;
  const chunks = [`<rect width="1200" height="100%" fill="white"/>`, `<text x="40" y="42" font-size="27" font-weight="bold">${esc(title)}</text>`];
  if (legend) {
   chunks.push(`<path d="M40 80H95" stroke="${colors[0]}" stroke-width="4" stroke-dasharray="8 4"/><text x="110" y="87" font-size="21">Trước tune</text><path d="M350 80H405" stroke="${colors[1]}" stroke-width="4"/><text x="420" y="87" font-size="21">Sau tune</text>`);
  }
  for (const chart of charts) {
   const titleMatch = chart.match(/aria-label="([^"]+)"/);
   if (charts.length>1) { chunks.push(`<text x="40" y="${y+23}" font-size="23" font-weight="bold">${esc(titleMatch[1])}</text>`); y+=48; }
   const [,w,h] = chart.match(/viewBox="0 0 (\d+) (\d+)"/);
   const height = Number(h)*1120/Number(w);
   let inner=chart.replace(/^<svg\b[^>]*>/,'').replace(/<\/svg>$/,'');
   chunks.push(`<g transform="translate(40 ${y}) scale(${1120/Number(w)})">${inner}</g>`);
   y+=height+24;
  }
  y+=14;
  for (const note of notes) { chunks.push(`<text x="40" y="${y}" font-size="18" fill="#34485e">${esc(note)}</text>`); y+=30; }
  const height=Math.ceil(y+15);
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="${height}" viewBox="0 0 1200 ${height}" font-family="DejaVu Sans, sans-serif" fill="#172c44">${chunks.join('')}</svg>`;
  await sharp(Buffer.from(svg)).resize({width:1800}).png().toFile(path.join(root,'figures',name));
  console.log(name);
 }
})().catch(e=>{console.error(e);process.exitCode=1});
