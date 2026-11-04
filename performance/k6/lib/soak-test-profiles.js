// Reduced soak from docs/Tool_Survey_Proposal.md: 30 VUs for 15 minutes.
// Ramp stages add two minutes to the steady measurement window.
export const profile = [
  { duration: '60s', seconds: 60, target: 30, phase: 'ramp_up' },
  { duration: '15m', seconds: 900, target: 30, phase: 'steady' },
  { duration: '60s', seconds: 60, target: 0, phase: 'ramp_down' },
];

export function phaseAt(elapsedMs) {
  let end = 0;
  for (const stage of profile) {
    end += stage.seconds * 1000;
    if (elapsedMs < end) return stage.phase;
  }
  return 'graceful_stop';
}
