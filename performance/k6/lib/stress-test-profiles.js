// One timeline drives both the executor and request-start classification.
export const profile = [];
for (const target of [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]) {
  profile.push({ duration: '30s', seconds: 30, target, phase: `ramp_${target}` });
  profile.push({ duration: '120s', seconds: 120, target, phase: `hold_${target}` });
}
profile.push({ duration: '0s', seconds: 0, target: 50, phase: 'unload' });
profile.push({ duration: '60s', seconds: 60, target: 50, phase: 'recovery_1' });
export function phaseAt(elapsedMs) {
  let end = 0;
  for (const stage of profile) {
    end += stage.seconds * 1000;
    if (elapsedMs < end) return stage.phase;
  }
  return 'graceful_stop';
}
