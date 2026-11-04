import http from 'k6/http';
import { preflight } from './lib/data.js';
import { profile, phaseAt } from './lib/soak-test-profiles.js';
import { thresholdsFor } from './lib/metrics.js';
import { createIteration } from './lib/normal-day-workload.js';

export const options = {
  scenarios: {
    soak: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: profile.map(({ duration, target }) => ({ duration, target })),
      gracefulRampDown: '30s',
      gracefulStop: '30s',
    },
  },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  thresholds: thresholdsFor(profile),
};

// This SUT returns 200 for every successful endpoint in this test.
http.setResponseCallback(http.expectedStatuses(200));

export function setup() {
  preflight();
}

export default createIteration({ profile, phaseAt, timelineLabel: 'SOAK_TIMELINE' });
