#!/usr/bin/env python3
"""Render Node CPU/RSS JSONL files as standalone, offline HTML reports."""
import argparse
import html
import json
import math
from pathlib import Path
import re
import sys


TEMPLATE = r'''<!doctype html>
<html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
body{font:16px system-ui;margin:32px auto;padding:0 20px;max-width:1200px;color:#172337;background:#f5f7fb}section{background:white;border:1px solid #dce3ed;border-radius:12px;padding:20px;margin:20px 0}svg{width:100%;height:auto}text{font:12px system-ui;fill:#536176}#tip{position:fixed;background:#172337;color:white;padding:8px;border-radius:6px;pointer-events:none;display:none;white-space:pre-line}
</style>
<h1>CPU và RAM backend</h1>
<section><h2>CPU (%)</h2><svg id="cpu" viewBox="0 0 1100 300" role="img" aria-label="CPU theo thời gian"></svg></section>
<section><h2>RAM RSS (MiB)</h2><svg id="ram" viewBox="0 0 1100 300" role="img" aria-label="RAM theo thời gian"></svg></section><div id="tip"></div>
<script>
const rows=__DATA__, timeline=__TIMELINE__;
const fmt=n=>n.toLocaleString(undefined,{maximumFractionDigits:2});
const start=rows[0][0], end=rows[rows.length-1][0], span=Math.max(end-start,1);
function draw(id,col,color){
 const svg=document.getElementById(id), ns='http://www.w3.org/2000/svg';
 function el(tag,attrs,text){const e=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;svg.append(e);return e;}
 let peak=0;for(const r of rows)peak=Math.max(peak,r[col]);const ymax=Math.max(peak*1.1,1);
 const x=t=>70+(t-start)/span*1000,y=v=>250-v/ymax*220;
 for(let i=0;i<=4;i++){const v=ymax*i/4;el('line',{x1:70,x2:1070,y1:y(v),y2:y(v),stroke:'#e3e8ef'});el('text',{x:60,y:y(v)+4,'text-anchor':'end'},fmt(v));}
 for(let i=0;i<=4;i++){const t=start+span*i/4;el('text',{x:x(t),y:280,'text-anchor':'middle'},new Date(t).toLocaleTimeString());}
 // Fixed offsets from the first and last samples, independent of k6 timeline.
 for(const [t,c,label,labelY] of [[start+30000,'#15803d','Hết 30s đầu',14],[end-60000,'#dc2626','Bắt đầu 60s cuối',29]]){
  if(t<start||t>end)continue;
  el('line',{x1:x(t),x2:x(t),y1:35,y2:250,stroke:c,'stroke-width':2,'stroke-dasharray':'5 4'});
  el('text',{x:Math.max(140,Math.min(1000,x(t))),y:labelY,'text-anchor':'middle',style:`fill:${c};font-weight:600`},label);
 }
 el('polyline',{points:rows.map(r=>`${x(r[0])},${y(r[col])}`).join(' '),fill:'none',stroke:color,'stroke-width':2});
 if(rows.length===1)el('circle',{cx:x(start),cy:y(rows[0][col]),r:4,fill:color});
 const cursor=el('line',{x1:70,x2:70,y1:20,y2:250,stroke:'#8996aa',visibility:'hidden'});
 svg.addEventListener('pointermove',e=>{const rect=svg.getBoundingClientRect(),t=start+((e.clientX-rect.left)/rect.width*1100-70)/1000*span;let lo=0,hi=rows.length-1;while(lo<hi){const mid=(lo+hi)>>1;if(rows[mid][0]<t)lo=mid+1;else hi=mid;}if(lo>0&&Math.abs(rows[lo-1][0]-t)<Math.abs(rows[lo][0]-t))lo--;const r=rows[lo];cursor.setAttribute('x1',x(r[0]));cursor.setAttribute('x2',x(r[0]));cursor.setAttribute('visibility','visible');const tip=document.getElementById('tip');tip.textContent=`${new Date(r[0]).toLocaleString()}\nCPU: ${fmt(r[1])}%\nRAM: ${fmt(r[2])} MiB`;tip.style.display='block';tip.style.left=Math.max(0,Math.min(e.clientX+12,innerWidth-tip.offsetWidth-8))+'px';tip.style.top=Math.max(0,Math.min(e.clientY+12,innerHeight-tip.offsetHeight-8))+'px';});
 svg.addEventListener('pointerleave',()=>{cursor.setAttribute('visibility','hidden');document.getElementById('tip').style.display='none';});
}
draw('cpu',1,'#2563eb');draw('ram',2,'#9333ea');
</script></html>'''


def read_samples(path):
    rows, skipped = [], 0
    with path.open(encoding='utf-8') as source:
        for line in source:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError('expected object')
                if row.get('type') == 'meta':
                    continue
                if row.get('type') != 'sample':
                    raise ValueError('unknown record type')
                values = [row[k] for k in ('ts', 'cpu_pct', 'rss')]
                if any(isinstance(v, bool) or not isinstance(v, (int, float))
                       or not math.isfinite(v) or v < 0 for v in values):
                    raise ValueError('invalid measurement')
                rows.append([values[0], values[1], values[2] / (1024 ** 2)])
            except (ValueError, KeyError, TypeError):
                skipped += 1
    if skipped:
        print(f'Cảnh báo: {path}: bỏ qua {skipped} dòng không hợp lệ.', file=sys.stderr)
    if not rows:
        raise ValueError(f'{path}: không có mẫu CPU/RAM hợp lệ')
    rows.sort(key=lambda row: row[0])
    return rows, skipped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path, help='Telemetry JSONL input files')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent.parent / 'output' / 'telemetry')
    parser.add_argument('--source-name', help='Original telemetry filename (single input only)')
    parser.add_argument('--timeline', type=Path, help='Optional measurement-timeline.json')
    args = parser.parse_args()
    if args.source_name and len(args.files) != 1:
        parser.error('--source-name requires exactly one input')
    timeline = {}
    if args.timeline:
        try:
            timeline = json.loads(args.timeline.read_text(encoding='utf-8'))
            if not isinstance(timeline, dict):
                raise ValueError('timeline must be an object')
        except (OSError, ValueError) as error:
            print(f'Cảnh báo: không đọc được timeline: {error}', file=sys.stderr)
            timeline = {}
    failed = False
    for path in args.files:
        try:
            rows, _ = read_samples(path)
            name = Path(args.source_name or path.name).stem
            title = html.escape(name)
            # Escape '<' so embedded data cannot terminate the script element.
            data = json.dumps(rows, allow_nan=False).replace('<', '\\u003c')
            clock = json.dumps(timeline, allow_nan=False).replace('<', '\\u003c')
            replacements = {'__TITLE__': title,
                            '__DATA__': data, '__TIMELINE__': clock}
            report = re.sub('|'.join(replacements), lambda match: replacements[match[0]], TEMPLATE)
            args.output_dir.mkdir(parents=True, exist_ok=True)
            target = args.output_dir / f'{name}.html'
            temporary = target.with_suffix('.html.tmp')
            temporary.write_text(report, encoding='utf-8')
            temporary.replace(target)
            print(f'CPU/RAM HTML: {target}')
        except (OSError, ValueError) as error:
            print(f'Lỗi: {error}', file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
