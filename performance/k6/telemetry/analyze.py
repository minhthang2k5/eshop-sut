#!/usr/bin/env python3
"""Node CPU/RAM tables by stress phase and before/during/after."""
import csv
import json
import os
from pathlib import Path
import sys

COLUMNS = ['period', 'target_vus', 'duration_s', 'samples', 'cpu_avg_pct', 'cpu_max_pct',
           'ram_avg_mib', 'ram_max_mib', 'ram_first_mib', 'ram_last_mib']


def intervals(timeline):
    before = timeline['before_start_ms']
    launch = timeline.get('k6_start_ms', timeline['after_end_ms'])
    start = timeline.get('scenario_start_ms', launch)
    end = timeline.get('k6_end_ms', launch)
    finish = timeline['after_end_ms']
    periods = [('before_stress', before, launch, ''), ('during_stress', start, end, ''),
               ('after_stress', end, finish, '')]
    phases = []
    if 'k6_start_ms' in timeline and start > launch:
        phases.append(('setup', launch, start, ''))
    elapsed = start
    for stage in timeline.get('profile', []):
        next_time = elapsed + stage['seconds'] * 1000
        if next_time > elapsed:
            # Clip the last phase if k6 was stopped early; do not report unrun phases as measured.
            phases.append((stage['phase'], min(elapsed, end), min(next_time, end), stage['target']))
        elapsed = next_time
    if timeline.get('profile') and end > elapsed:
        phases.append(('graceful_stop', elapsed, end, ''))
    return periods, phases


def summarize(rows, interval):
    name, start, end, target = interval
    samples = [r for r in rows if start <= r[0] < end]
    values = {'period': name, 'target_vus': target, 'duration_s': max(0, end-start) / 1000, 'samples': len(samples)}
    if samples:
        cpu, ram = [r[1] for r in samples], [r[2] for r in samples]
        values.update(cpu_avg_pct=sum(cpu)/len(cpu), cpu_max_pct=max(cpu),
                      ram_avg_mib=sum(ram)/len(ram), ram_max_mib=max(ram),
                      ram_first_mib=ram[0], ram_last_mib=ram[-1])
    return {key: values.get(key, '') for key in COLUMNS}


def save_table(path, records):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(records)


def markdown_table(records):
    lines = ['| Giai đoạn | VU target | Giây | Mẫu | CPU TB (%) | CPU max (%) | RAM TB (MiB) | RAM max (MiB) | RAM đầu (MiB) | RAM cuối (MiB) |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    def cell(value):
        return f'{value:.2f}' if isinstance(value, float) else str(value) if value != '' else '—'
    lines += ['| ' + ' | '.join(cell(record[key]) for key in COLUMNS) + ' |' for record in records]
    return lines


def update_report(source, lines, report_path=None):
    report_path = report_path or Path(__file__).resolve().parent.parent / 'reports/03-stress-test-report.md'
    start_marker = '<!-- CPU_RAM_RESULTS_START -->'
    end_marker = '<!-- CPU_RAM_RESULTS_END -->'
    text = report_path.read_text()
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    relative = Path(os.path.relpath(source.parent.resolve(), report_path.parent.resolve())).as_posix()
    content = [f'Lượt đo: [{source.parent.name}]({relative}/). Các bảng bên dưới được cập nhật từ lượt chạy gần nhất.', ''] + lines
    report_path.write_text(text[:start] + '\n\n' + '\n'.join(content) + '\n\n' + text[end:])
    print(f'Bảng CPU/RAM: {report_path}')


def main():
    source = Path(sys.argv[1])
    rows = []
    with source.open() as stream:
        for line in stream:
            try:
                row = json.loads(line)
                if row.get('type') == 'sample':
                    rows.append((row['ts'], row['cpu_pct'], row['rss'] / 2**20))
            except (ValueError, KeyError):
                continue
    rows.sort(key=lambda row: row[0])
    timeline_file = source.with_name('measurement-timeline.json')
    timeline = json.loads(timeline_file.read_text()) if timeline_file.exists() else None
    periods, phases = intervals(timeline) if timeline else ([], [])
    if timeline:
        rows = [row for row in rows if timeline['before_start_ms'] <= row[0] < timeline['after_end_ms']]
        period_stats = [summarize(rows, interval) for interval in periods]
        phase_stats = [summarize(rows, interval) for interval in phases]
        save_table(source.with_name('cpu-ram-before-during-after.csv'), period_stats)
        save_table(source.with_name('cpu-ram-phases.csv'), phase_stats)
        report = ['#### Trước / trong / sau stress', ''] + markdown_table(period_stats)
        report += ['', '#### Từng phase', ''] + markdown_table(phase_stats)
        report += ['', 'CPU 100% = một core; RAM là RSS. TB là trung bình các mẫu. RAM đầu/cuối là mẫu đầu/cuối trong cửa sổ.',
                   'Trong stress tính từ scenario bắt đầu đến khi k6 kết thúc, gồm recovery và grace cuối. Setup nằm riêng, không gộp vào trước tải.',
                   'Phase theo lịch target; iteration cũ có thể còn hoàn tất sau khi hạ tải. Mẫu thuộc cửa sổ [bắt đầu, kết thúc).',
                   'Ô — nghĩa là thiếu mẫu; phase có 0 giây nghĩa là chưa quan sát trong lần chạy này.']
        if 'scenario_start_ms' not in timeline:
            report += ['Chưa có mốc scenario: không xác định được từng phase; khoảng trong stress chỉ là thời gian tiến trình k6.']
        if timeline.get('interrupted'):
            report += ['Lần đo bị ngắt: các cửa sổ có thể chưa đủ thời gian dự kiến.']
        before, _, after = period_stats
        if before['samples'] and after['samples']:
            report += ['', f"Chênh lệch sau − trước: CPU TB {after['cpu_avg_pct']-before['cpu_avg_pct']:+.2f} điểm phần trăm; RAM TB {after['ram_avg_mib']-before['ram_avg_mib']:+.2f} MiB."]
        update_report(source, report)
    if not rows:
        print('Chưa có mẫu CPU/RAM.')
        return
    with source.with_name('node-cpu-ram.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['timestamp_ms', 'cpu_percent_one_core', 'ram_mib'])
        writer.writerows(rows)


if __name__ == '__main__':
    main()
