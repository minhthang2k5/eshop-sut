'use strict';
const fs = require('node:fs');
const path = require('node:path');

// CPU and resident RAM of this Node process, sampled once per second.
function start({ label = 'backend' } = {}) {
  if (process.env.TELEMETRY === '0') return null;
  let fd, timer;
  const stop = () => {
    clearInterval(timer);
    if (fd !== undefined) { fs.closeSync(fd); fd = undefined; }
  };
  try {
    const directory = path.resolve(process.env.TELEMETRY_DIR || path.join(__dirname, '../output/telemetry'));
    const file = process.env.TELEMETRY_FILE || path.join(directory, `server-${label}-${process.pid}-${Date.now()}.jsonl`);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fd = fs.openSync(file, 'a');
    const write = row => fs.writeSync(fd, JSON.stringify({ ts: Date.now(), pid: process.pid, ...row }) + '\n');
    write({ type: 'meta', label });
    let cpu = process.cpuUsage(), time = process.hrtime.bigint();
    timer = setInterval(() => {
      try {
        const nextCpu = process.cpuUsage(), nextTime = process.hrtime.bigint();
        const elapsedUs = Number(nextTime - time) / 1000;
        write({ type: 'sample', cpu_pct: ((nextCpu.user - cpu.user) + (nextCpu.system - cpu.system)) / elapsedUs * 100,
          rss: process.memoryUsage.rss() });
        cpu = nextCpu; time = nextTime;
      } catch (error) { console.error(`Telemetry stopped: ${error.message}`); stop(); }
    }, 1000);
    timer.unref();
    process.once('exit', stop);
    console.log(`CPU/RAM: ${file}`);
    return { file, stop };
  } catch (error) {
    console.error(`Telemetry unavailable: ${error.message}`);
    stop();
    return null;
  }
}
module.exports = { start };
