"""Run: python3 -m unittest discover -s performance/k6/analyze -v"""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from analyze import (ROOT, build_analysis, evaluate, load_config, load_samples,
                     metric, normalize_metrics, resource_intervals, status, summarize)
from reporting import chart, render


def passing_summary(config):
    metrics = {}
    for rule in config['rules']:
        phases = config['assess_phases'] if rule['scope']=='phase' else [None]
        for phase in phases:
            for endpoint in rule['endpoints']:
                tags = ([f'phase:{phase}'] if phase else []) + ([f'endpoint:{endpoint}'] if endpoint else [])
                key = rule['metric'] + ('{'+','.join(tags)+'}' if tags else '')
                field = 'value' if rule['stat']=='rate' else rule['stat']
                value = rule['limit'] + {'<':-.001, '>':1, '>=':0, '<=':0, '==':0}[rule['op']]
                metrics.setdefault(key,{})[field] = value
    return {'metrics':metrics}


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.run = Path(self.temp.name)/'run'
        self.run.mkdir()
        self.config = load_config('stress')

    def write(self, name, data):
        (self.run/name).write_text(json.dumps(data),encoding='utf-8')

    def result(self, test_type='stress'):
        return build_analysis(self.run,load_config(test_type))

    def test_stress_skips_diagnostic_and_failed_operations_at_limit_fail(self):
        summary = passing_summary(self.config)
        summary['metrics']['business_requests_skipped'] = {'count':999}
        self.write('summary.json',summary)
        self.assertEqual(self.result()['status'],'PASS')
        summary['metrics']['business_operations_failed{phase:hold_200}']['value'] = .01
        self.write('summary.json',summary)
        self.assertEqual(self.result()['status'],'FAIL')

    def test_baseline_does_not_require_steady_login(self):
        self.write('summary.json',passing_summary(load_config('baseline')))
        result = self.result('baseline')
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['counts'],{'pass':25,'fail':0,'missing':0})
        self.assertEqual(result['completeness'],'UNKNOWN')
        self.assertEqual(result['phases'][0]['duration_basis'],'nominal')
        self.assertEqual(result['phases'][0]['seconds'],300)

    def test_baseline_global_login_and_skips_still_fail(self):
        config = load_config('baseline')
        summary = passing_summary(config)
        summary['metrics']['http_req_duration{endpoint:login}']['p(95)'] = 500
        summary['metrics']['business_requests_skipped']['count'] = 1
        self.write('summary.json',summary)
        self.assertEqual(self.result('baseline')['counts']['fail'],2)

    def test_spike_phase_skips_still_fail(self):
        config = load_config('spike')
        summary = passing_summary(config)
        summary['metrics']['business_requests_skipped{phase:hold_1500}']['count'] = 1
        self.write('summary.json',summary)
        result = self.result('spike')
        self.assertEqual(result['counts'],{'pass':62,'fail':1,'missing':0})
        self.assertEqual(result['phases'][1]['status'],'FAIL')

    def test_endpoint_threshold_boundaries_and_missing_data(self):
        summary = passing_summary(self.config)
        key = 'http_req_duration{phase:hold_200,endpoint:login}'
        summary['metrics'][key]['p(95)'] = 500
        normalized = normalize_metrics(summary)
        self.assertEqual(status(evaluate(normalized,self.config)),'FAIL')
        del summary['metrics'][key]
        self.assertEqual(status(evaluate(normalize_metrics(summary),self.config)),'INCOMPLETE')
        summary['metrics']['checks{phase:hold_200}']['value'] = .99
        self.assertIs(next(c['passed'] for c in evaluate(normalize_metrics(summary),self.config)
                           if c['metric']=='checks' and c['phase']=='hold_200' and c['endpoint'] is None),True)

    def test_known_failure_is_not_hidden_by_missing_data(self):
        self.assertEqual(status([{'passed':False},{'passed':None}]),'FAIL')
        self.assertEqual(status([{'passed':True},{'passed':None}]),'INCOMPLETE')
        self.assertEqual(status([]),'INCOMPLETE')

    def test_modern_values_and_reordered_tags(self):
        summary = passing_summary(self.config)
        key = 'http_req_duration{phase:hold_200,endpoint:login}'
        value = summary['metrics'].pop(key)
        summary['metrics']['http_req_duration{endpoint:login,phase:hold_200}'] = value
        summary['metrics'] = {k:{'values':{('rate' if f=='value' else f):v for f,v in x.items()}} for k,x in summary['metrics'].items()}
        self.assertEqual(status(evaluate(normalize_metrics(summary),self.config)),'PASS')
        self.assertEqual(metric(normalize_metrics(summary),'http_req_duration','hold_200','login')['p(95)'],499.999)

    def test_interrupted_run_has_separate_completeness(self):
        self.write('summary.json',passing_summary(load_config('baseline')))
        self.write('measurement-timeline.json',{'before_start_ms':0,'k6_start_ms':1000,
                   'scenario_start_ms':1000,'k6_end_ms':121000,'after_end_ms':122000,'interrupted':True})
        result = self.result('baseline')
        self.assertEqual(result['completeness'],'PARTIAL')
        self.assertEqual(result['phases'][0]['seconds'],60)
        self.assertEqual(result['status'],'INCOMPLETE')
        self.assertEqual(result['phases'][0]['status'],'INCOMPLETE')

    def test_empty_inputs_and_bad_json_do_not_reuse_results(self):
        result = self.result()
        self.assertEqual(result['status'],'INCOMPLETE')
        self.assertEqual(result['counts']['missing'],400)
        self.assertFalse(result['samples'])
        (self.run/'summary.json').write_text('{broken')
        with self.assertRaisesRegex(ValueError,'JSON không hợp lệ'):
            self.result()

    def test_validation_rejects_configuration_and_timeline_errors(self):
        config = copy.deepcopy(self.config)
        config['rules'][0]['op'] = '!='
        self.write('profiles.json',{'stress':config})
        with self.assertRaises(ValueError):
            load_config('stress',self.run/'profiles.json')
        self.write('measurement-timeline.json',{'scenario_start_ms':2000,'k6_end_ms':1000})
        with self.assertRaisesRegex(ValueError,'đúng thứ tự'):
            self.result()

    def test_interval_boundaries_and_missing_samples(self):
        intervals = resource_intervals({'before_start_ms':0,'k6_start_ms':1000,
            'scenario_start_ms':2000,'k6_end_ms':4000,'after_end_ms':5000},
            [{'phase':'steady','target':50,'seconds':2}])
        self.assertEqual(intervals[0][1],('during_test',2000,4000,None))
        row = summarize([(1999,0,10),(2000,10,20),(3999,30,40),(4000,100,100)],intervals[0][1])
        self.assertEqual(row['samples'],2)
        self.assertEqual(row['cpu_avg_pct'],20)
        self.assertIsNone(summarize([],intervals[0][1])['cpu_avg_pct'])

    def test_malformed_telemetry_counted_and_nonfinite_rejected(self):
        (self.run/'node-cpu-ram.jsonl').write_text('\n'.join([
            'invalid','[]','{"type":"sample","ts":1,"cpu_pct":NaN,"rss":2}',
            '{"type":"metadata"}',
            '{"type":"sample","ts":1,"cpu_pct":0,"rss":1048576}']))
        rows, ignored = load_samples(self.run)
        self.assertEqual(rows,[(1,0,1)])
        self.assertEqual(ignored,3)

    def test_svg_has_gaps_and_escaped_labels(self):
        svg = chart('CPU < &', [0,1/60,10/60], [1,2,3])
        ET.fromstring(svg)
        self.assertEqual(svg.count('<polyline'),2)
        ET.fromstring(chart('p95',[0,1,2],[1,None,3],['a','b','c']))

    def test_cli_default_and_custom_outputs_and_input_immutability(self):
        self.write('summary.json',passing_summary(load_config('baseline')))
        source = self.run/'summary.json'
        digest = hashlib.sha256(source.read_bytes()).digest()
        command = [sys.executable,str(Path(__file__).with_name('analyze.py')),str(self.run),'--type','baseline']
        subprocess.run(command,check=True,capture_output=True)
        md = self.run/'analysis/report.md'
        first = md.read_text()
        self.assertIn('N/A',first)
        self.assertIn('nominal',first)
        subprocess.run(command,check=True,capture_output=True)
        self.assertEqual(first,md.read_text())
        self.assertEqual(digest,hashlib.sha256(source.read_bytes()).digest())
        out = Path(self.temp.name)/'custom'
        subprocess.run([*command,'--report-dir',str(out)],check=True,capture_output=True)
        self.assertTrue((out/'02-baseline-test-report.md').exists())
        self.assertTrue((out/'baseline_report.html').exists())
        self.assertFalse((out/'stress_report.html').exists())
        web = (out/'baseline_report.html').read_text()
        for link in re.findall(r'href="([^"]+)"',web):
            self.assertTrue((out/link).exists(),link)

    def test_invalid_source_and_config_leave_existing_report_intact(self):
        (self.run/'summary.json').write_text('[]')
        out = Path(self.temp.name)/'reports';out.mkdir()
        report = out/'stress_report.html';report.write_text('old report')
        command = [sys.executable,str(Path(__file__).with_name('analyze.py')),str(self.run),
                   '--type','stress','--report-dir',str(out)]
        result = subprocess.run(command,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertNotIn('Traceback',result.stderr)
        self.assertEqual(report.read_text(),'old report')

    def test_runner_calls_moved_analyzer_without_telemetry_and_preserves_exit_code(self):
        runner_root = Path(self.temp.name)/'k6'
        runner_root.mkdir()
        shutil.copy(ROOT/'run-stress.sh',runner_root/'run-stress.sh')
        shutil.copytree(ROOT/'analyze',runner_root/'analyze',ignore=shutil.ignore_patterns('__pycache__'))
        bin_dir = Path(self.temp.name)/'bin'
        bin_dir.mkdir()
        fake_k6 = bin_dir/'k6'
        fake_k6.write_text('''#!/usr/bin/env bash
for arg in "$@"; do
  case "$arg" in
    --summary-export=*) printf '{"metrics":{}}' > "${arg#*=}" ;;
  esac
done
exit "${MOCK_K6_EXIT:-0}"
''')
        fake_k6.chmod(0o755)
        # Real wall clocks can step backwards by milliseconds on the test host.
        fake_date = bin_dir/'date'
        fake_date.write_text('''#!/usr/bin/env python3
import os, sys
from pathlib import Path
if sys.argv[1] == '+%s%3N':
    state = Path(os.environ['MOCK_DATE_STATE'])
    value = int(state.read_text()) + 1000 if state.exists() else 1000
    state.write_text(str(value))
    print(value)
else:
    print('20261102-000000')
''')
        fake_date.chmod(0o755)
        for exit_code in (0,99):
            with self.subTest(exit_code=exit_code):
                env = {**os.environ,'TELEMETRY':'0','MOCK_K6_EXIT':str(exit_code),
                       'MOCK_DATE_STATE':str(Path(self.temp.name)/'clock'),
                       'PATH':str(bin_dir)+os.pathsep+os.environ['PATH']}
                process = subprocess.run(['bash',str(runner_root/'run-stress.sh')],env=env,
                                         capture_output=True,text=True,timeout=10)
                self.assertEqual(process.returncode,exit_code,process.stderr)
                report = runner_root/'reports/03-stress-test-report.md'
                self.assertTrue(report.exists(), process.stdout + process.stderr)
                self.assertIn('INCOMPLETE',report.read_text())
                self.assertNotIn('Không tổng hợp được',process.stderr)

    @unittest.skipUnless(shutil.which('node'),'Node.js not installed')
    def test_config_thresholds_match_actual_k6_scripts(self):
        # Evaluate JS initialization only. SharedArray fixture callbacks and load functions never run.
        code = r'''
const fs = require('node:fs'), vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0,'utf8'));
const context = {__ENV:{}, Counter:class {}, Rate:class {}, SharedArray:class {constructor(){return []}},
 http:{expectedStatuses(){}, setResponseCallback(){}}, exec:{}};
vm.createContext(context);
for (let source of input.sources) {
 source = source.replace(/^import .*;$/gm,'').replace(/export default function \(\)/g,'function iterationForTest()')
  .replace(/^export default .*;$/gm,'').replace(/export /g,'');
 vm.runInContext(source,context);
}
process.stdout.write(vm.runInContext('JSON.stringify({thresholds:options.thresholds,stages:options.stages || Object.values(options.scenarios)[0].stages})',context));
'''
        for test_type in ('baseline','spike','stress'):
            with self.subTest(test_type=test_type):
                paths = [ROOT/f'{test_type}.js']
                if test_type=='stress':
                    paths = [ROOT/'lib/metrics.js',ROOT/'lib/stress-test-profiles.js',*paths]
                result = subprocess.run(['node','-e',code],input=json.dumps({'sources':[p.read_text() for p in paths]}),
                                        text=True,capture_output=True,check=True)
                actual = json.loads(result.stdout)
                js = {key:rules for key,rules in actual['thresholds'].items() if rules}
                config = load_config(test_type)
                def seconds(duration):
                    parts = re.findall(r'([0-9.]+)(ms|s|m|h)',duration)
                    return sum(float(n)*{'ms':.001,'s':1,'m':60,'h':3600}[unit] for n,unit in parts)
                self.assertEqual([(seconds(s['duration']),s['target']) for s in actual['stages']],
                                 [(s['seconds'],s['target']) for s in config['profile']])
                expected = {}
                for c in evaluate({},config):
                    tags = ([f'phase:{c["phase"]}'] if c['phase'] else []) + ([f'endpoint:{c["endpoint"]}'] if c['endpoint'] else [])
                    key = c['metric']+('{'+','.join(tags)+'}' if tags else '')
                    expected[key] = [f'{c["stat"]}{c["op"]}{c["limit"]:g}']
                self.assertEqual(js,expected)


if __name__ == '__main__':
    unittest.main()
