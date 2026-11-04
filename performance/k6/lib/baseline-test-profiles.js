// Shared timeline for the executor and request-start phase tags.
export const profile = [
  { phase: 'ramp_up', duration: '60s', seconds: 60, target: 50 },
  { phase: 'steady', duration: '300s', seconds: 300, target: 50 },
  { phase: 'ramp_down', duration: '60s', seconds: 60, target: 0 },
];

export function phaseAt(elapsedMs) {
  let end = 0;
  for (const stage of profile) {
    end += stage.seconds * 1000;
    if (elapsedMs < end) return stage.phase;
  }
  return 'graceful_stop';
}
