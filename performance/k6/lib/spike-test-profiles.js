// Abrupt spike to 1,000 VUs, then observe recovery at the normal load.
export const profile = [
  { duration: '30s', seconds: 30, target: 50, phase: 'hold_50' },
  { duration: '0s', seconds: 0, target: 1000, phase: 'burst' },
  { duration: '60s', seconds: 60, target: 1000, phase: 'hold_1000' },
  { duration: '0s', seconds: 0, target: 50, phase: 'unload' },
  { duration: '60s', seconds: 60, target: 50, phase: 'recovery_1' },
];

export function phaseAt(elapsedMs) {
  let end = 0;
  for (const stage of profile) {
    end += stage.seconds * 1000;
    if (elapsedMs < end) return stage.phase;
  }
  return 'graceful_stop';
}
