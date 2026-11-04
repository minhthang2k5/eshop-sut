import http from 'k6/http';
import { preflight } from './lib/data.js';
import { profile, phaseAt } from './lib/spike-test-profiles.js';
import { thresholdsFor } from './lib/metrics.js';
import { createIteration } from './lib/black-friday-workload.js';

http.setResponseCallback(http.expectedStatuses(200));

export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-vus',
      startVUs: 50,
      stages: profile.map(({ duration, target }) => ({ duration, target })),
      gracefulRampDown: '30s',
      gracefulStop: '30s',
    },
  },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  thresholds: thresholdsFor(profile),
};

export function setup() {
  preflight();
}

export default createIteration({ profile, phaseAt, timelineLabel: 'SPIKE_TIMELINE' });