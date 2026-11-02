#!/usr/bin/env python3
"""Analyze saved k6 baseline, stress and spike runs; Python standard library only."""
import argparse
import csv
import json
import math
import operator
from pathlib import Path
import re

from reporting import render

ROOT = Path(__file__).resolve().parent.parent
OPERATORS = {'<': operator.lt, '>': operator.gt, '>=': operator.ge, '<=': operator.le, '==': operator.eq}
RESOURCE_COLUMNS = ['period', 'target_vus', 'duration_s', 'samples', 'cpu_avg_pct',
                    'cpu_max_pct', 'ram_avg_mib', 'ram_max_mib', 'ram_first_mib', 'ram_last_mib']


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def read_json(path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as error:
        raise ValueError(f'{path}: JSON không hợp lệ: {error}') from error


def validate_profile(stages):
    if not isinstance(stages, list) or not stages:
        raise ValueError('profile phải là danh sách phase không rỗng')
    names = set()
    for stage in stages:
        if (not isinstance(stage, dict) or not isinstance(stage.get('phase'), str)
                or not stage['phase'] or stage['phase'] in names
                or not number(stage.get('seconds')) or stage['seconds'] < 0
                or not number(stage.get('target')) or stage['target'] < 0):
            raise ValueError('Phase phải có tên duy nhất, seconds và target không âm')
        names.add(stage['phase'])


def load_config(test_type, path=None):
    configs = read_json(path or Path(__file__).with_name('profiles.json'))
    if not isinstance(configs, dict) or not isinstance(configs.get(test_type), dict):
        raise ValueError(f'Không có cấu hình cho {test_type}')
    config = configs[test_type]
    validate_profile(config.get('profile'))
    phases = {s['phase']: s for s in config['profile']}
    selected = config.get('assess_phases')
    if (not isinstance(selected, list) or not selected
            or any(not isinstance(p, str) for p in selected) or len(set(selected)) != len(selected)
            or any(p not in phases or phases[p]['seconds'] <= 0 for p in selected)):
        raise ValueError('assess_phases phải chứa các phase có thời lượng dương trong profile')
    for key in ('title', 'description', 'markdown_name', 'html_name'):
        if not isinstance(config.get(key), str) or not config[key]:
            raise ValueError(f'Cấu hình thiếu {key}')
    for key in ('markdown_name', 'html_name'):
        if Path(config[key]).name != config[key]:
            raise ValueError('Tên báo cáo không được chứa đường dẫn')
    if not isinstance(config.get('rules'), list) or not config['rules']:
        raise ValueError('rules phải là danh sách không rỗng')
    for rule in config['rules']:
        if (not isinstance(rule, dict) or not isinstance(rule.get('metric'), str)
                or not rule['metric'] or rule.get('stat') not in ('p(95)', 'rate', 'count')
                or not isinstance(rule.get('op'), str) or rule['op'] not in OPERATORS
                or not number(rule.get('limit'))
                or rule.get('scope') not in ('phase', 'global')
                or not isinstance(rule.get('endpoints'), list) or not rule['endpoints']
                or any(e is not None and not isinstance(e, str) for e in rule['endpoints'])):
            raise ValueError(f'Threshold không hợp lệ: {rule}')
    config['type'] = test_type
    return config


def normalize_metrics(summary):
    if not isinstance(summary, dict) or not isinstance(summary.get('metrics', {}), dict):
        raise ValueError('summary phải có metrics dạng object')
    metrics = {}
    for key, entry in summary.get('metrics', {}).items():
        if not isinstance(entry, dict):
            raise ValueError(f'Metric {key} không phải object')
        name, _, selector = key.partition('{')
        tags = {}
        if selector:
            if not selector.endswith('}'):
                raise ValueError(f'Tag metric không hợp lệ: {key}')
            for tag in selector[:-1].split(','):
                tag_name, colon, value = tag.partition(':')
                if not colon or not tag_name or tag_name in tags:
                    raise ValueError(f'Tag metric không hợp lệ: {key}')
                tags[tag_name] = value
        values = entry.get('values', entry)
        if not isinstance(values, dict):
            raise ValueError(f'Metric values {key} không phải object')
        normalized_key = (name, tuple(sorted(tags.items())))
        if normalized_key in metrics:
            raise ValueError(f'Metric trùng tag sau chuẩn hóa: {key}')
        metrics[normalized_key] = values
    return metrics


def metric(metrics, name, phase=None, endpoint=None):
    tags = {}
    if phase is not None:
        tags['phase'] = phase
    if endpoint is not None:
        tags['endpoint'] = endpoint
    return metrics.get((name, tuple(sorted(tags.items()))), {})


def statistic(values, stat):
    value = values.get('rate', values.get('value')) if stat == 'rate' else values.get(stat)
    return value if number(value) else None


def evaluate(metrics, config):
    conditions = []
    for rule in config['rules']:
        phases = config['assess_phases'] if rule['scope'] == 'phase' else [None]
        for phase in phases:
            for endpoint in rule['endpoints']:
                value = statistic(metric(metrics, rule['metric'], phase, endpoint), rule['stat'])
                passed = OPERATORS[rule['op']](value, rule['limit']) if value is not None else None
                conditions.append({**rule, 'phase': phase, 'endpoint': endpoint,
                                   'value': value, 'passed': passed})
    return conditions


def status(conditions):
    """A known violation remains FAIL even when other evidence is missing."""
    results = [c['passed'] for c in conditions]
    if False in results:
        return 'FAIL'
    if not results or None in results:
        return 'INCOMPLETE'
    return 'PASS'


def load_timeline(run):
    timeline = read_json(run / 'measurement-timeline.json', {})
    if not isinstance(timeline, dict):
        raise ValueError('measurement-timeline.json phải là object')
    # Legacy stress runner records the scenario origin and actual stages in the log.
    if 'profile' not in timeline or 'scenario_start_ms' not in timeline:
        log = run / 'k6.log'
        if log.exists():
            with log.open(encoding='utf-8', errors='replace') as stream:
                for line in stream:
                    if 'STRESS_TIMELINE ' not in line:
                        continue
                    try:
                        marker, _ = json.JSONDecoder().raw_decode(line.replace('\\"', '"').split('STRESS_TIMELINE ', 1)[1])
                        timeline.setdefault('scenario_start_ms', marker['start_ms'])
                        timeline.setdefault('profile', marker['profile'])
                        break
                    except (ValueError, KeyError, TypeError):
                        continue
    if 'profile' in timeline:
        validate_profile(timeline['profile'])
    if 'interrupted' in timeline and not isinstance(timeline['interrupted'], bool):
        raise ValueError('timeline.interrupted phải là boolean')
    keys = ['before_start_ms', 'k6_start_ms', 'scenario_start_ms', 'k6_end_ms', 'after_end_ms']
    times = [timeline[k] for k in keys if k in timeline]
    if any(not number(v) or v < 0 for v in times) or times != sorted(times):
        raise ValueError('Mốc timeline phải hữu hạn, không âm và đúng thứ tự')
    return timeline


def load_samples(run):
    rows, ignored = [], 0
    path = run / 'node-cpu-ram.jsonl'
    if path.exists():
        with path.open(encoding='utf-8') as stream:
            for line in stream:
                try:
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise ValueError('sample is not an object')
                    if row.get('type') != 'sample':
                        continue
                    if not all(number(row.get(k)) and row[k] >= 0 for k in ('ts', 'cpu_pct', 'rss')):
                        raise ValueError('invalid sample')
                    rows.append((row['ts'], row['cpu_pct'], row['rss'] / 2**20))
                except (ValueError, KeyError):
                    ignored += 1
    return sorted(rows), ignored


def resource_intervals(timeline, profile):
    periods, phases = [], []
    start, end = timeline.get('scenario_start_ms'), timeline.get('k6_end_ms')
    launch, before, after = (timeline.get(k) for k in ('k6_start_ms', 'before_start_ms', 'after_end_ms'))
    if before is not None and launch is not None:
        periods.append(('before_test', before, launch, None))
    if start is not None and end is not None:
        periods.append(('during_test', start, end, None))
        if launch is not None and start > launch:
            phases.append(('setup', launch, start, None))
        elapsed = start
        for stage in profile:
            following = elapsed + stage['seconds']*1000
            if following > elapsed:
                phases.append((stage['phase'], min(elapsed, end), min(following, end), stage['target']))
            elapsed = following
        if end > elapsed:
            phases.append(('graceful_stop', elapsed, end, None))
    if end is not None and after is not None:
        periods.append(('after_test', end, after, None))
    return periods, phases


def summarize(samples, interval):
    name, start, end, target = interval
    rows = [r for r in samples if start <= r[0] < end]
    record = dict.fromkeys(RESOURCE_COLUMNS)
    record.update(period=name, target_vus=target, duration_s=(end-start)/1000, samples=len(rows))
    if rows:
        cpu, ram = [r[1] for r in rows], [r[2] for r in rows]
        record.update(cpu_avg_pct=sum(cpu)/len(cpu), cpu_max_pct=max(cpu),
                      ram_avg_mib=sum(ram)/len(ram), ram_max_mib=max(ram),
                      ram_first_mib=ram[0], ram_last_mib=ram[-1])
    return record


def build_analysis(run, config):
    summary = read_json(run / 'summary.json', {})
    metrics = normalize_metrics(summary)
    timeline = load_timeline(run)
    profile = timeline.get('profile', config['profile'])
    samples, ignored = load_samples(run)
    samples = [r for r in samples if timeline.get('before_start_ms', -math.inf) <= r[0] < timeline.get('after_end_ms', math.inf)]
    periods, intervals = resource_intervals(timeline, profile)
    period_stats = [summarize(samples, interval) for interval in periods]
    phase_stats = [summarize(samples, interval) for interval in intervals]
    actual = {name: (end-start)/1000 for name, start, end, _ in intervals}
    observed_time = 'scenario_start_ms' in timeline and 'k6_end_ms' in timeline
    conditions = evaluate(metrics, config)
    stage_by_name = {s['phase']: s for s in profile}
    warnings = []
    phase_rows = []
    for name in config['assess_phases']:
        stage = stage_by_name.get(name)
        seconds = actual.get(name) if observed_time else stage['seconds'] if stage else None
        subset = [c for c in conditions if c['phase'] == name]
        duration_ok = stage is not None and (not observed_time or actual.get(name, 0) >= stage['seconds'])
        if not duration_ok:
            warnings.append(f'{name}: thiếu cửa sổ đầy đủ hoặc không thuộc profile của run.')
        phase_status = status(subset)
        if phase_status == 'PASS' and not duration_ok:
            phase_status = 'INCOMPLETE'
        n = metric(metrics, 'http_reqs', name).get('count')
        latency = metric(metrics, 'http_req_duration', name)
        phase_rows.append(dict(phase=name, target=stage['target'] if stage else None,
                               seconds=seconds, duration_basis='observed' if observed_time else 'nominal',
                               requests=n, rps=n/seconds if number(n) and seconds else None,
                               p50=latency.get('med'), p95=latency.get('p(95)'), p99=latency.get('p(99)'),
                               error=statistic(metric(metrics,'http_req_failed',name),'rate'),
                               checks=statistic(metric(metrics,'checks',name),'rate'),
                               skipped=metric(metrics,'business_requests_skipped',name).get('count'),
                               status=phase_status))
    elapsed = (timeline['k6_end_ms']-timeline['scenario_start_ms'])/1000 if observed_time else None
    planned = sum(s['seconds'] for s in profile)
    if timeline.get('interrupted') or (elapsed is not None and elapsed < planned):
        completeness = 'PARTIAL'
    elif elapsed is not None:
        completeness = 'COMPLETE'
    else:
        completeness = 'UNKNOWN'
    overall = status(conditions)
    if overall == 'PASS' and (completeness == 'PARTIAL' or any(r['status'] == 'INCOMPLETE' for r in phase_rows)):
        overall = 'INCOMPLETE'
    if not observed_time:
        warnings.append('Không có đủ mốc scenario/k6: thời lượng phase và RPS dùng lịch danh định; chưa xác nhận thời lượng thực tế.')
    if timeline.get('profile') and timeline['profile'] != config['profile']:
        # Ignore optional k6 fields such as duration when comparing actual stage semantics.
        semantic = lambda stages: [(s['phase'],s['seconds'],s['target']) for s in stages]
        if semantic(profile) != semantic(config['profile']):
            warnings.append('Profile run khác cấu hình hiện tại; dùng profile run để tính thời lượng, không giả định hai workload tương đương.')
    if not metrics:
        warnings.append('Thiếu summary k6 hoặc không có metric; không thể xác nhận đạt SLO.')
    if not samples:
        warnings.append('Không có mẫu CPU/RAM; không diễn giải tài nguyên là 0.')
    if ignored:
        warnings.append(f'Đã bỏ qua {ignored} dòng telemetry không hợp lệ.')
    if samples and 'scenario_start_ms' not in timeline:
        warnings.append('Không có mốc scenario; chỉ xuất mẫu tài nguyên, không gán phase hoặc vẽ theo mốc tự suy đoán.')
    if completeness == 'PARTIAL':
        warnings.append('Lần đo bị ngắt hoặc chưa đủ lịch tải; các vi phạm quan sát được vẫn là FAIL.')
    overview = []
    for label, name, stat, scale in [
        ('HTTP requests','http_reqs','count',1), ('Throughput (requests/s)','http_reqs','rate_total',1),
        ('HTTP lỗi (%)','http_req_failed','rate',100), ('Checks đạt (%)','checks','rate',100),
        ('Iterations hoàn tất','iterations','count',1),
        ('Nghiệp vụ skipped','business_requests_skipped','count',1),
        ('Iteration nghiệp vụ bắt đầu','business_iterations_started','count',1),
        ('Iteration nghiệp vụ hoàn tất','business_iterations_completed','count',1),
        ('HTTP nghiệp vụ đã gửi','business_requests_sent','count',1),
        ('Request nghiệp vụ lỗi (gồm login chặn thao tác)','business_requests_failed','count',1),
        ('Thao tác nghiệp vụ thất bại (%)','business_operations_failed','rate',100)]:
        values = metric(metrics,name)
        value = values.get('rate') if stat == 'rate_total' else statistic(values,stat)
        if number(value):
            overview.append([label, value*scale, 0 if stat=='count' else 3])
    for key in ('avg','med','p(95)','p(99)','max'):
        overview.append([f'Latency {key} (ms)', metric(metrics,'http_req_duration').get(key), 3])
    notes = make_notes(config, phase_rows, period_stats)
    return dict(run=run, config=config, timeline=timeline, profile=profile, samples=samples,
                period_stats=period_stats, phase_stats=phase_stats, conditions=conditions,
                phases=phase_rows, overview=overview, status=overall, completeness=completeness,
                counts={k:sum(c['passed'] is v for c in conditions) for k,v in [('pass',True),('fail',False),('missing',None)]},
                warnings=warnings, notes=notes)


def make_notes(config, phases, period_stats):
    notes = []
    if config['type'] == 'stress':
        holds = [r for r in phases if r['phase'].startswith('hold_')]
        passed = [r for r in holds if r['status']=='PASS']
        first_fail = next((r['phase'] for r in holds if r['status']=='FAIL'), 'chưa ghi nhận')
        prefix = []
        for row in holds:
            if row['status'] != 'PASS': break
            prefix.append(row['target'])
        notes += [f'{len(passed)}/{len(holds)} bậc hold PASS. Bậc FAIL đầu tiên: {first_fail}.',
                  f'Vùng PASS liên tục từ bậc đầu: {prefix[0]}–{prefix[-1]} VU.' if prefix else 'Chưa xác lập vùng PASS liên tục từ bậc đầu.']
    elif config['type'] == 'baseline':
        notes += ['Steady: '+next((r['status'] for r in phases if r['phase']=='steady'),'INCOMPLETE')+'. Login toàn bài được đánh giá riêng; login steady không bắt buộc có mẫu.']
    else:
        notes += ['Trước và trong spike: '+', '.join(f'{r["phase"]} {r["status"]}' for r in phases if not r['phase'].startswith('recovery_'))+'.']
    recovery = [r for r in phases if r['phase'].startswith('recovery_')]
    if recovery:
        notes += ['Recovery: '+', '.join(f'{r["phase"]} {r["status"]}' for r in recovery)+'. Percentile của cửa sổ không xác định chính xác giây phục hồi.']
    periods = {r['period']:r for r in period_stats}
    if 'during_test' in periods:
        row = periods['during_test']
        notes += [f'Trong tải: {row["samples"]} mẫu / {row["duration_s"]:.2f}s. TB tài nguyên là trung bình mẫu, không có trọng số thời gian; khoảng thiếu mẫu có thể bỏ sót đỉnh.']
    before, after = periods.get('before_test'), periods.get('after_test')
    if before and after and before['samples'] and after['samples']:
        notes += [f'Sau tải: CPU TB {after["cpu_avg_pct"]:.2f}%; RSS TB {after["ram_avg_mib"]:.2f} MiB, chênh trước tải {after["ram_avg_mib"]-before["ram_avg_mib"]:+.2f} MiB.']
    notes += ['Kết quả một lượt đo không chứng minh sức tải ổn định; CPU/RAM riêng lẻ không đủ kết luận nguyên nhân nghẽn hoặc memory leak.']
    return notes


def save_csv(path, columns, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Run directory or node-cpu-ram.jsonl')
    parser.add_argument('--type', required=True, choices=['stress','spike','baseline'], dest='test_type')
    parser.add_argument('--report-dir', type=Path, help='Explicit destination; uses test-specific report names')
    args = parser.parse_args()
    run = args.source if args.source.is_dir() else args.source.parent
    if not run.is_dir() or (not args.source.is_dir() and args.source.name != 'node-cpu-ram.jsonl'):
        parser.error('source phải là thư mục run hoặc đường dẫn node-cpu-ram.jsonl')
    try:
        config = load_config(args.test_type)
        result = build_analysis(run.resolve(),config)
        output = (args.report_dir or run/'analysis').resolve()
        # Construct both reports before touching their destinations.
        documents = render(result,output,custom_names=args.report_dir is not None)
        output.mkdir(parents=True,exist_ok=True)
        save_csv(output/'node-cpu-ram.csv',['timestamp_ms','cpu_percent_one_core','ram_mib'],result['samples'])
        for name, rows in [('cpu-ram-before-during-after.csv',result['period_stats']),('cpu-ram-phases.csv',result['phase_stats'])]:
            save_csv(output/name,RESOURCE_COLUMNS,[[r[k] for k in RESOURCE_COLUMNS] for r in rows])
        for name, content in documents.items():
            target = output/name
            temporary = target.with_suffix(target.suffix+'.tmp')
            temporary.write_text(content,encoding='utf-8')
            temporary.replace(target)
            print(f'Báo cáo: {target}')
        print(f'SLO {result["status"]}; lần đo {result["completeness"]}; điều kiện: {result["counts"]}')
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
