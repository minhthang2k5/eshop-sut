import http from 'k6/http';
import { preflight } from './lib/data.js';
import { profile } from './lib/stress-test-profiles.js';
import { thresholdsFor } from './lib/metrics.js';
import { iteration } from './lib/workload.js';

http.setResponseCallback(http.expectedStatuses(200));

export const options = {
  scenarios: {
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: profile.map(({ duration, target }) => ({ duration, target })),
      gracefulRampDown: '60s',
      gracefulStop: '60s',
    },
  },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  thresholds: thresholdsFor(profile),
};

export function setup() {
  preflight();
}

export default iteration;