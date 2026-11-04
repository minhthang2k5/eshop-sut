import { Counter, Rate } from 'k6/metrics';
export const endpoints = ['search', 'detail', 'cart', 'checkout'];
export const started = new Counter('business_iterations_started');
export const completed = new Counter('business_iterations_completed');
export const selected = new Counter('business_operations_selected');
export const sent = new Counter('business_requests_sent');
export const succeeded = new Counter('business_requests_succeeded');
export const requestsFailed = new Counter('business_requests_failed');
export const operationsSucceeded = new Counter('business_operations_succeeded');
export const failed = new Rate('business_operations_failed');
export const skipped = new Counter('business_requests_skipped');
export function thresholdsFor(profile) {
  const thresholds = {};
  for (const stage of profile.filter(s => s.phase === 'steady' || /^(hold_|recovery_)/.test(s.phase))) {
    for (const endpoint of [null, 'login', ...endpoints]) {
      const filter = `phase:${stage.phase}${endpoint ? `,endpoint:${endpoint}` : ''}`;
      thresholds[`http_req_duration{${filter}}`] = ['p(95)<500'];
      thresholds[`http_req_failed{${filter}}`] = ['rate<0.01'];
      thresholds[`checks{${filter}}`] = ['rate>=0.99'];
      thresholds[`http_reqs{${filter}}`] = ['count>0'];
    }
    thresholds[`business_operations_failed{phase:${stage.phase}}`] = ['rate<0.01'];
    // Skips remain diagnostic; failed login already counts in business_operations_failed.
  }
  return thresholds;
}
