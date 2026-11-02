"""Render a precomputed analysis as Markdown, standalone HTML and inline SVG."""
import html
import math
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def fmt(value, digits=3):
    return f'{value:,.{digits}f}' if number(value) else 'N/A'


def table(headers, rows, web=False):
    if web:
        cells = lambda row, tag: '<tr>' + ''.join(f'<{tag}>{html.escape(str(v))}</{tag}>' for v in row) + '</tr>'
        return '<div class="scroll"><table><thead>' + cells(headers, 'th') + '</thead><tbody>' + ''.join(cells(r, 'td') for r in rows) + '</tbody></table></div>'
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '|' + '|'.join(['---']*len(headers)) + '|'] + ['| ' + ' | '.join(str(v).replace('|', '&#124;').replace('\n', ' ') for v in r) + ' |' for r in rows])


def chart(title, xs, ys, labels=None, threshold=None, color='#2563eb', markers=()):
    valid = [v for v in ys if number(v)]
    if not valid or not xs:
        return f'<p>{html.escape(title)}: không có dữ liệu.</p>'
    ymax = max(valid + [threshold or 0])*1.12 or 1
    lo, hi = min(xs), max(xs)
    X = lambda v: 80 + (v-lo)/(hi-lo or 1)*1060
    Y = lambda v: 240 - v/ymax*180
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" role="img" aria-label="{html.escape(title)}"><title>{html.escape(title)}</title><text x="20" y="25" font-size="18">{html.escape(title)}</text>']
    for i in range(5):
        v = ymax*i/4
        parts.append(f'<path d="M80 {Y(v):.2f}H1140" stroke="#ddd"/><text x="5" y="{Y(v)+4:.2f}" font-size="12">{v:.1f}</text>')
    if threshold is not None:
        parts.append(f'<path d="M80 {Y(threshold):.2f}H1140" stroke="#dc2626" stroke-dasharray="5 4"/><text x="900" y="{Y(threshold)-5:.2f}" font-size="12">SLO {threshold:g} ms</text>')
    for x, label, level in markers:
        if not lo <= x <= hi:
            continue
        parts.append(f'<path d="M{X(x):.2f} 60V240" stroke="#64748b" stroke-dasharray="4 4"/><text x="{X(x):.2f}" y="{40+level*14}" text-anchor="end" font-size="11">{html.escape(label)}</text>')
    segments = [[]]
    for i, (x, y) in enumerate(zip(xs, ys)):
        if not number(y):
            segments.append([])
            continue
        if labels is None and i and x-xs[i-1] > 2/60:
            segments.append([])
        segments[-1].append(f'{X(x):.2f},{Y(y):.2f}')
        parts.append(f'<circle cx="{X(x):.2f}" cy="{Y(y):.2f}" r="{3 if labels else 1}" fill="{color}"><title>{html.escape(labels[i]) if labels else f"{x:.3f} phút"}: {y:.3f}</title></circle>')
    for segment in segments:
        if segment:
            parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="1.5" points="{" ".join(segment)}"/>')
    ticks = list(zip(xs, labels)) if labels else [(lo+(hi-lo)*i/8, f'{lo+(hi-lo)*i/8:.1f}') for i in range(9)]
    for x, label in ticks:
        parts.append(f'<text x="{X(x):.2f}" y="266" text-anchor="middle" font-size="11">{html.escape(label)}</text>')
    parts.append(f'<text x="600" y="304" text-anchor="middle" font-size="13">{"VU target theo phase; R = recovery" if labels else "Phút từ lúc scenario bắt đầu"}</text></svg>')
    return '\n'.join(parts)


def render(result, destination, custom_names=False):
    """Return file contents only; all statistics and SLO decisions come from analyze.py."""
    config = result['config']
    title = config['title'] + ' Test Report — EShop'
    markdown_name = config['markdown_name'] if custom_names else 'report.md'
    html_name = config['html_name'] if custom_names else 'report.html'
    run, timeline = result['run'], result['timeline']
    relative = Path(os.path.relpath(run, destination)).as_posix()
    root_relative = Path(os.path.relpath(ROOT, destination)).as_posix()

    def local_time(key):
        value = timeline.get(key)
        return datetime.fromtimestamp(value/1000, timezone(timedelta(hours=7))).isoformat(timespec='milliseconds') if value is not None else 'Chưa ghi nhận'

    info = [['Run ID',run.name],['Loại test',config['type']],
            ['Scenario bắt đầu (UTC+7)',local_time('scenario_start_ms')],
            ['k6 kết thúc (UTC+7)',local_time('k6_end_ms')],
            ['Độ đầy đủ lần đo',result['completeness']],
            ['Môi trường / phiên bản','Không được lưu trong dữ liệu đầu vào; chưa xác nhận']]
    overview = [[label,fmt(value,digits)] for label,value,digits in result['overview']]
    counts = result['counts']
    overview += [['Threshold đạt / không đạt / thiếu dữ liệu',f'{counts["pass"]} / {counts["fail"]} / {counts["missing"]}'],
                 ['SLO trên dữ liệu quan sát',result['status']]]
    criteria = (f'Đánh giá theo cấu hình {config["type"]} trong analyze/profiles.json, không dùng cờ threshold của summary. '
                + config['description'] + ' INCOMPLETE nghĩa là thiếu bằng chứng để xác nhận đạt. '
                'COMPLETE/PARTIAL/UNKNOWN mô tả độ đầy đủ lịch tải, độc lập với vi phạm SLO đã quan sát.')
    rule_rows = []
    for rule in config['rules']:
        rule_rows.append([rule['metric'],f'{rule["stat"]} {rule["op"]} {rule["limit"]:g}',
                          'các phase đánh giá' if rule['scope']=='phase' else 'toàn bài',
                          ', '.join(e or 'tổng' for e in rule['endpoints'])])
    phase_note = ('RPS = request / thời lượng phase: dùng cửa sổ quan sát khi có timeline, nếu thiếu thì dùng thời lượng danh định và ghi rõ trong bảng. '
                  'VU là mục tiêu profile, không phải VU thực đo. Không cộng hoặc lấy trung bình percentile của các phase. '
                  'Thứ tự phase theo cấu hình; bảng profile bên dưới ghi lịch của run nếu có, nếu không thì dùng cấu hình.')
    phase_headers = ['Phase','VU target','Giây','Cơ sở thời lượng','Requests','RPS','p50 ms','p95 ms','p99 ms','HTTP lỗi %','Checks %','Skipped','SLO']
    phase_rows = []
    for row in result['phases']:
        phase_rows.append([row['phase'],fmt(row['target'],0),fmt(row['seconds'],2),row['duration_basis'],
                           fmt(row['requests'],0),fmt(row['rps']),fmt(row['p50']),fmt(row['p95']),fmt(row['p99']),
                           fmt(row['error']*100 if number(row['error']) else None),
                           fmt(row['checks']*100 if number(row['checks']) else None),fmt(row['skipped'],0),row['status']])
    # Show global conditions as well as failed/missing phase conditions, explaining phase FAIL.
    condition_rows = []
    for c in result['conditions']:
        if c['phase'] is None or c['passed'] is not True:
            condition_rows.append([c['phase'] or 'toàn bài',c['endpoint'] or 'tổng',c['metric'],
                                   f'{c["stat"]} {c["op"]} {c["limit"]:g}',fmt(c['value']),
                                   'PASS' if c['passed'] is True else 'FAIL' if c['passed'] is False else 'INCOMPLETE'])
    condition_headers = ['Phase','Endpoint','Metric','Điều kiện','Giá trị','Kết quả']
    cpu_headers = ['Giai đoạn','VU target','Giây','Mẫu','CPU TB %','CPU max %','RAM TB MiB','RAM max MiB','RAM đầu MiB','RAM cuối MiB']
    cpu_keys = ['period','target_vus','duration_s','samples','cpu_avg_pct','cpu_max_pct','ram_avg_mib','ram_max_mib','ram_first_mib','ram_last_mib']

    def resource_rows(stats):
        return [[r[k] if k=='period' else fmt(r[k],0 if k in ('target_vus','samples') else 2) for k in cpu_keys] for r in stats]

    resources = [('Trước / trong / sau tải',resource_rows(result['period_stats'])),
                 ('Từng phase',resource_rows(result['phase_stats']))]
    labels = [str(r['target']) if r['target'] is not None else r['phase'] for r in result['phases']]
    labels = ['R'+label if row['phase'].startswith('recovery_') else label for row,label in zip(result['phases'],labels)]
    xs = list(range(len(labels)))
    figures = [chart('VU target theo phase đánh giá',xs,[r['target'] for r in result['phases']],labels),
               chart('Latency p95 (ms) theo phase',xs,[r['p95'] for r in result['phases']],labels,
                     threshold=next((r['limit'] for r in config['rules'] if r['metric']=='http_req_duration' and r['stat']=='p(95)'),None),color='#7c3aed')]
    samples = result['samples']
    if samples and 'scenario_start_ms' in timeline:
        start = timeline['scenario_start_ms']
        markers = [(0,'Bắt đầu',0)]
        elapsed = 0
        for stage in result['profile']:
            if stage['phase'].startswith('recovery_'):
                markers.append((elapsed/60,'Recovery',0))
            elapsed += stage['seconds']
        if 'k6_end_ms' in timeline:
            markers.append(((timeline['k6_end_ms']-start)/60000,'Kết thúc k6',1))
        xs = [(r[0]-start)/60000 for r in samples]
        for index,caption,color in [(1,'CPU Node.js (%)','#2563eb'),(2,'RAM Node.js — RSS (MiB)','#059669')]:
            figures.append(chart(caption,xs,[r[index] for r in samples],color=color,markers=markers))
    else:
        figures.append('<p>Chưa đủ dữ liệu CPU/RAM hoặc mốc scenario để vẽ theo thời gian.</p>')
    cpu_note = ('CPU 100% = một core; RAM = RSS (MiB). TB là trung bình mẫu. '
                'Cửa sổ [bắt đầu, kết thúc); trong tải gồm recovery và grace, setup tách riêng. '
                'Biểu đồ giữ toàn bộ mẫu và ngắt nét khi khoảng cách vượt 2s. N/A là thiếu dữ liệu, không phải 0.')
    profile_rows = [[s['phase'],fmt(s['seconds'],2),fmt(s['target'],0)] for s in result['profile']]
    profile_headers = ['Phase','Giây danh định','VU target']
    source_names = [name for name in ['summary.json','measurement-timeline.json','node-cpu-ram.jsonl','k6.log'] if (run/name).exists()]
    source_links = [(name,f'{relative}/{name}') for name in source_names]
    source_links += [(name,name) for name in ['node-cpu-ram.csv','cpu-ram-phases.csv','cpu-ram-before-during-after.csv']]
    source_links += [('profiles.json',f'{root_relative}/analyze/profiles.json')]
    notes = result['warnings'] + result['notes']
    md = ['# '+title,'','Báo cáo tự động từ dữ liệu đã lưu. '+f'[Biểu đồ HTML]({html_name}).',
          '', '## 1. Thông tin lần đo','',table(['Trường','Giá trị'],info),
          '', '## 2. Tiêu chí đánh giá','',criteria,'',table(['Metric','Ngưỡng','Phạm vi','Endpoint'],rule_rows),
          '', '## 3. Profile và cách chạy','',table(profile_headers,profile_rows),'',
          f'[Script {config["type"]}]({root_relative}/{config["type"]}.js) · [Hướng dẫn analyzer]({root_relative}/analyze/README.md).',
          '', '## 4. Nguồn dữ liệu','', ' · '.join(f'[{label}]({url})' for label,url in source_links),
          '', '## 5. Cách đọc kết quả','',phase_note,
          '', '## 6. Kết quả đo','', '### 6.1 Tổng quan','',table(['Chỉ số','Kết quả'],overview),
          '', '### 6.2 Theo phase','',table(phase_headers,phase_rows),
          '', 'Điều kiện toàn bài và các điều kiện phase không đạt/thiếu dữ liệu:','',table(condition_headers,condition_rows),
          '', '### 6.3 CPU và RAM Node.js','',cpu_note]
    for caption,rows in resources:
        md += ['','#### '+caption,'',table(cpu_headers,rows)]
    md += ['','### 6.4 Nhận xét và kết luận','',*['- '+n for n in notes],'']
    web = ['<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
           '<title>'+html.escape(title)+'</title><style>body{font:16px system-ui;max-width:1200px;margin:32px auto;padding:0 20px;color:#172033}p{line-height:1.6}svg{width:100%;height:auto;background:#f8fafc;margin:12px 0}.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid #ddd;padding:8px;text-align:right}th:first-child,td:first-child{text-align:left}</style></head><body>',
           '<h1>'+html.escape(title)+'</h1>',table(['Trường','Giá trị'],info,True),
           '<h2>Tiêu chí đánh giá</h2><p>'+html.escape(criteria)+'</p>',table(['Metric','Ngưỡng','Phạm vi','Endpoint'],rule_rows,True),
           '<h2>Profile</h2>',table(profile_headers,profile_rows,True),
           '<h2>Tổng quan</h2>',table(['Chỉ số','Kết quả'],overview,True),
           '<h2>Tải và latency</h2><p>'+html.escape(phase_note)+'</p>',*figures[:2],table(phase_headers,phase_rows,True),
           '<h3>Điều kiện toàn bài và các điều kiện phase không đạt/thiếu dữ liệu</h3>',table(condition_headers,condition_rows,True),
           '<h2>CPU và RAM</h2><p>'+cpu_note+'</p>',*figures[2:]]
    for caption,rows in resources:
        web += ['<h3>'+caption+'</h3>',table(cpu_headers,rows,True)]
    web += ['<h2>Nhận xét</h2>',*['<p>'+html.escape(n)+'</p>' for n in notes],
            f'<p><a href="{html.escape(markdown_name)}">Báo cáo Markdown</a> · '+ ' · '.join(f'<a href="{html.escape(url,quote=True)}">{html.escape(label)}</a>' for label,url in source_links)+'</p></body></html>']
    return {markdown_name:'\n'.join(md),html_name:'\n'.join(web)}
