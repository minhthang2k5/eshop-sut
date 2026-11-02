#!/usr/bin/env python3
"""Run k6 and save Node CPU/RAM before, during and after stress."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
BEFORE_SECONDS = 30
AFTER_SECONDS = 60


def find_source():
    if os.environ.get('TELEMETRY_FILE'):
        return Path(os.environ['TELEMETRY_FILE'])
    directory = Path(os.environ.get('TELEMETRY_DIR', HERE.parent / 'output/telemetry'))
    for file in sorted(directory.glob('server-*.jsonl'), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            with file.open() as stream:
                meta = json.loads(stream.readline())
            os.kill(meta['pid'], 0)
            return file
        except (OSError, ValueError, KeyError):
            continue
    return None


def main():
    output = Path(sys.argv[1])
    source = find_source() if os.environ.get('TELEMETRY', '1') != '0' else None
    offset = source.stat().st_size if source else 0
    print(f'Stress output: {output}', flush=True)
    if not source and os.environ.get('TELEMETRY', '1') != '0':
        print('Không tìm thấy file CPU/RAM của backend; vẫn chạy k6.', flush=True)
    child = None
    interrupted = threading.Event()
    now = lambda: time.time_ns() // 1_000_000
    timeline = {'before_start_ms': now()}

    def interrupt(signum, _):
        interrupted.set()
        if child is not None and child.poll() is None:
            child.send_signal(signum)
    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, interrupt)
    code = 130
    try:
        if source:
            print(f'Thu CPU/RAM trước tải: {BEFORE_SECONDS}s...', flush=True)
            interrupted.wait(BEFORE_SECONDS)
        if not interrupted.is_set():
            timeline['k6_start_ms'] = now()
            child = subprocess.Popen(['k6', 'run', '--out', f'json={output / "metrics.json"}',
                f'--summary-export={output / "summary.json"}', str(HERE.parent / 'stress.js')],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
            if interrupted.is_set():
                child.terminate()
            with (output / 'k6.log').open('wb') as log:
                for line in child.stdout:
                    log.write(line)
                    # k6 quotes JSON inside its console log message.
                    text = line.decode(errors='replace').replace('\\"', '"')
                    if 'STRESS_TIMELINE ' in text:
                        try:
                            marker, _ = json.JSONDecoder().raw_decode(text.split('STRESS_TIMELINE ', 1)[1])
                            timeline['scenario_start_ms'] = marker['start_ms']
                            timeline['profile'] = marker['profile']
                        except (ValueError, KeyError):
                            pass
                    try:
                        sys.stdout.buffer.write(line); sys.stdout.buffer.flush()
                    except BrokenPipeError:
                        pass
            code = child.wait()
            timeline['k6_end_ms'] = now()
            if source and not interrupted.is_set():
                print(f'Thu CPU/RAM sau tải: {AFTER_SECONDS}s; giữ backend đang chạy...', flush=True)
                interrupted.wait(AFTER_SECONDS)
    finally:
        if child is not None and child.poll() is None:
            child.terminate()
            try: child.wait(timeout=5)
            except subprocess.TimeoutExpired: child.kill(); child.wait()
        timeline['after_end_ms'] = now()
        timeline['interrupted'] = interrupted.is_set()
        (output / 'measurement-timeline.json').write_text(json.dumps(timeline, indent=2) + '\n')
    if source:
        try:
            with source.open('rb') as stream, (output / 'node-cpu-ram.jsonl').open('wb') as dest:
                stream.seek(offset)
                for line in stream:
                    if line.endswith(b'\n'): dest.write(line)
            subprocess.run([sys.executable, str(HERE / 'analyze.py'), str(output / 'node-cpu-ram.jsonl')], check=True)
        except (OSError, subprocess.SubprocessError) as error:
            print(f'Không tạo được kết quả CPU/RAM: {error}', file=sys.stderr)
    print(f'Kết quả: {output}')
    if interrupted.is_set() and code == 0:
        return 130
    return code if code >= 0 else 128 - code


if __name__ == '__main__':
    sys.exit(main())
