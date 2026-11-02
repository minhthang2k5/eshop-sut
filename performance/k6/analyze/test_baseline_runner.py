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

class BaselineRunnerTests(unittest.TestCase):
    def test_exit_codes_timeline_reports_and_interrupt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy(ROOT / 'run-baseline.sh', root / 'run-baseline.sh')
            shutil.copytree(ROOT / 'analyze', root / 'analyze', ignore=shutil.ignore_patterns('__pycache__'))
            binary = root / 'bin'
            binary.mkdir()
            fake = binary / 'k6'
            fake.write_text('''#!/usr/bin/env python3
import json, os, signal, sys, time
for arg in sys.argv:
    if arg.startswith('--summary-export='):
        open(arg.split('=',1)[1], 'w').write('{"metrics":{}}')
print('level=info msg=' + json.dumps('BASELINE_TIMELINE ' + json.dumps({'start_ms':int(open(os.environ['MOCK_CLOCK']).read())+1,'profile':[
 {'phase':'ramp_up','seconds':60,'target':50},
 {'phase':'steady','seconds':300,'target':50},
 {'phase':'ramp_down','seconds':60,'target':0}]})), flush=True)
signal.signal(signal.SIGINT, lambda *_: sys.exit(130))
if os.environ['MOCK_EXIT'] == 'interrupt':
    time.sleep(20)
else:
    sys.exit(int(os.environ['MOCK_EXIT']))
''')
            fake.chmod(0o755)
            date = binary / 'date'
            date.write_text('''#!/usr/bin/env python3
import os, sys
from pathlib import Path
p = Path(os.environ['MOCK_CLOCK'])
if sys.argv[1] == '+%s%3N':
    n = int(p.read_text())+1000 if p.exists() else 1000
    p.write_text(str(n))
    print(n)
else:
    print('20261102-000000')
''')
            date.chmod(0o755)
            for outcome in ('0', '99', 'interrupt'):
                with self.subTest(outcome=outcome):
                    env = {**os.environ, 'TELEMETRY':'0', 'MOCK_EXIT':outcome, 'MOCK_CLOCK':str(root/'clock'),
                           'PATH':str(binary)+os.pathsep+os.environ['PATH']}
                    p = subprocess.Popen(['bash', str(root/'run-baseline.sh')], env=env,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         text=True, start_new_session=True)
                    if outcome == 'interrupt':
                        deadline = time.monotonic()+5
                        while time.monotonic() < deadline:
                            logs = list((root/'output').glob('*/k6.log'))
                            if any('BASELINE_TIMELINE' in log.read_text() and not (log.parent/'measurement-timeline.json').exists() for log in logs):
                                break
                            time.sleep(.02)
                        os.killpg(p.pid, signal.SIGINT)
                    stdout, stderr = p.communicate(timeout=10)
                    self.assertEqual(p.returncode, 130 if outcome == 'interrupt' else int(outcome), stderr)
                    run = Path(stdout.split('Baseline output: ',1)[1].splitlines()[0])
                    timeline = json.loads((run/'measurement-timeline.json').read_text())
                    self.assertIn('scenario_start_ms', timeline)
                    self.assertEqual(timeline['profile'][1]['seconds'], 300)
                    self.assertEqual(timeline['interrupted'], outcome == 'interrupt')
                    self.assertTrue((root/'reports/baseline_report.html').exists(), stdout+stderr)
                    self.assertIn('INCOMPLETE', (root/'reports/02-baseline-test-report.md').read_text())
                    self.assertFalse((run/'node-cpu-ram.jsonl').exists())
                    self.assertNotIn('Không tổng hợp được', stderr)

if __name__ == '__main__':
    unittest.main()
