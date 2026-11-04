"""Exercise the four independent runners without a backend or a real load test."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
KINDS = ('baseline', 'stress', 'spike', 'soak')

FAKE_K6 = r'''#!/usr/bin/env python3
import json, os, pathlib, signal, sys, time
args = sys.argv[1:]
kind = pathlib.Path(args[-1]).stem
for arg in args:
    if arg.startswith('json='):
        pathlib.Path(arg[5:]).write_text('{}\n')
    if arg.startswith('--summary-export='):
        pathlib.Path(arg.split('=', 1)[1]).write_text('{}\n')
assert os.environ['K6_WEB_DASHBOARD'] == 'true'
assert os.environ['K6_WEB_DASHBOARD_OPEN'] == 'false'
assert os.environ['K6_WEB_DASHBOARD_PORT'] == '0'
pathlib.Path(os.environ['K6_WEB_DASHBOARD_EXPORT']).write_text('<html>dashboard</html>')
marker = {'start_ms': 123456, 'profile': [{'seconds': 60, 'target': 50, 'phase': 'steady'}]}
print('level=info msg=' + json.dumps(kind.upper() + '_TIMELINE ' + json.dumps(marker)), flush=True)
if os.environ.get('TELEMETRY_FILE') and os.environ['TELEMETRY'] != '0':
    with open(os.environ['TELEMETRY_FILE'], 'a') as f:
        f.write('{"window":"load"}\n')
if os.environ.get('WAIT_FOR_SIGNAL') == '1':
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    signal.signal(signal.SIGINT, lambda *_: sys.exit(130))
    pathlib.Path(os.environ['READY_FILE']).touch()
    while True:
        time.sleep(.01)
sys.exit(int(os.environ.get('FAKE_EXIT', '0')))
'''
FAKE_SLEEP = r'''#!/usr/bin/env python3
import json, os, sys
with open(os.environ['SLEEP_CALLS'], 'a') as f:
    f.write(sys.argv[1] + '\n')
with open(os.environ['TELEMETRY_FILE'], 'a') as f:
    f.write(json.dumps({'window': sys.argv[1]}) + '\n')
'''


class RunnerTests(unittest.TestCase):
    def exercise(self, kind, code=0, telemetry=False, missing=False, interrupt=False):
        with tempfile.TemporaryDirectory(prefix='k6-runner-test-') as directory:
            temp = Path(directory)
            script = temp / f'run-{kind}.sh'
            shutil.copy2(ROOT / script.name, script)
            binary = temp / 'bin'
            binary.mkdir()
            for name, source in [('k6', FAKE_K6), ('sleep', FAKE_SLEEP)]:
                path = binary / name
                path.write_text(source)
                path.chmod(0o755)
            source = temp / 'telemetry.jsonl'
            source.write_text('{"window":"old"}\n')
            env = dict(os.environ, PATH=f'{binary}:{os.environ["PATH"]}',
                       TELEMETRY='1' if telemetry or missing else '0',
                       TELEMETRY_FILE=str(temp / 'missing.jsonl' if missing else source),
                       SLEEP_CALLS=str(temp / 'sleep-calls'), FAKE_EXIT=str(code),
                       WAIT_FOR_SIGNAL='1' if interrupt else '0', READY_FILE=str(temp / 'ready'))
            # Run outside the script directory to verify path handling.
            process = subprocess.Popen(['bash', str(script)], cwd='/tmp', env=env,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            try:
                if interrupt:
                    deadline = time.monotonic() + 5
                    while not (temp / 'ready').exists():
                        if process.poll() is not None or time.monotonic() > deadline:
                            self.fail('Mock k6 did not become ready')
                        time.sleep(.01)
                    process.send_signal(signal.SIGTERM)
                output, _ = process.communicate(timeout=10)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate()
            self.assertEqual(process.returncode, 143 if interrupt else code, output)
            self.assertNotIn('analyze', output)
            runs = list((temp / 'output').iterdir())
            self.assertEqual(len(runs), 1)
            run = runs[0]
            self.assertTrue(run.name.startswith(kind + '-'))
            for name in ('summary.json', 'metrics.json', 'k6.log',
                         'measurement-timeline.json', f'{kind}_report.html'):
                self.assertTrue((run / name).is_file(), name)
            timeline = json.loads((run / 'measurement-timeline.json').read_text())
            self.assertEqual(timeline['interrupted'], interrupt)
            self.assertEqual(timeline['scenario_start_ms'], 123456)
            self.assertEqual(timeline['profile'][0]['phase'], 'steady')
            # These are wall-clock timestamps; clock adjustments can reorder them.
            for key in ('before_start_ms', 'k6_start_ms', 'k6_end_ms', 'after_end_ms'):
                self.assertIsInstance(timeline[key], int)
                self.assertGreater(timeline[key], 0)
            if telemetry:
                rows = [json.loads(line) for line in (run / 'node-cpu-ram.jsonl').read_text().splitlines()]
                self.assertEqual([row['window'] for row in rows],
                                 ['30', 'load'] if interrupt else ['30', 'load', '60'])
                self.assertEqual((temp / 'sleep-calls').read_text().splitlines(),
                                 ['30'] if interrupt else ['30', '60'])
            else:
                self.assertFalse((run / 'node-cpu-ram.jsonl').exists())
                self.assertFalse((temp / 'sleep-calls').exists())
            if missing:
                self.assertIn('Không tìm thấy file CPU/RAM', output)

    def test_success_without_telemetry(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                self.exercise(kind)

    def test_threshold_failure_with_telemetry(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                self.exercise(kind, code=99, telemetry=True)

    def test_missing_telemetry_still_runs(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                self.exercise(kind, missing=True)

    def test_termination_saves_artifacts(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                self.exercise(kind, telemetry=True, interrupt=True)

    def test_no_analyzer_invocation(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                self.assertNotIn('analyze', (ROOT / f'run-{kind}.sh').read_text())


if __name__ == '__main__':
    unittest.main()
