import { SharedArray } from 'k6/data';
import http from 'k6/http';
import { sha256 } from 'k6/crypto';

// Search keyword percentages. Keys must match the manifest; total must be 100.
export const keywordWeights = {
  "iPhone": 25,
  "Samsung": 20,
  "MacBook": 15,
  "AirPods": 7,
  "iPad": 6,
  "Apple Watch": 6,
  "Sony": 6,
  "Keychron": 3,
  "Logitech": 3,
  "Dell": 3,
  "Asus": 3,
  "Xiaomi": 3
};

export const baseUrl = (__ENV.BASE_URL || 'http://localhost:3000').replace(/\/+$/, '');
// Same single-line CSV contract as seed.js: quoted commas and escaped quotes supported.
function csv(text, expected) {
  const pattern = /(?:^|,)(?:"((?:[^"]|"")*)"|([^",\r\n]*))(?=,|$)/gy;
  const rows = text.replace(/^\uFEFF/, '').split(/\r?\n/).filter(line => line.trim()).map((line, index) => {
    const fields = [];
    pattern.lastIndex = 0;
    let match, end = 0;
    while ((match = pattern.exec(line)) !== null) {
      fields.push(match[1] === undefined ? match[2] : match[1].replace(/""/g, '"'));
      end = pattern.lastIndex;
      if (end === line.length) break;
    }
    if (end !== line.length || fields.length !== expected.split(',').length) throw new Error(`Invalid CSV row ${index + 1}`);
    return fields;
  });
  if (!rows.length || rows.shift().join(',') !== expected) throw new Error('Invalid CSV header');
  return rows;
}
export const accounts = new SharedArray('stress accounts', () => {
  const seen = new Set();
  const source = open('../data/test_accounts.csv');
  const metadata = JSON.parse(open('../data/test-data-manifest.json'));
  if (sha256(source, 'hex') !== metadata.sourceHashes.accounts) throw new Error('Stale account manifest: run data/build-manifest.cjs');
  const rows = csv(source, 'email,password,name,role');
  return rows.map(([email, password, name, role]) => {
    if (![email, password, name, role].every(v => v.trim()) || email !== email.trim() || role !== 'user' || seen.has(email)) throw new Error('Invalid/duplicate account');
    seen.add(email);
    return { email, password };
  });
});
export const manifest = JSON.parse(open('../data/test-data-manifest.json'));
export const products = new SharedArray('stress products', () => {
  const source = open('../data/test_products.csv');
  if (sha256(source, 'hex') !== manifest.sourceHashes.products) throw new Error('Stale product manifest: run data/build-manifest.cjs');
  const rows = csv(source, 'product_id,name,price,description,image_url,category_id,search_keyword');
  const items = rows.map(([id, name, price]) => ({ id: Number(id), name, price: Number(price) }));
  if (items.length < 100 || items.length > 500 || new Set(items.map(p => p.id)).size !== items.length || items.some(p => !Number.isSafeInteger(p.id) || p.id <= 0 || !p.name.trim() || !Number.isFinite(p.price) || p.price <= 0)) throw new Error('Invalid products');
  if (JSON.stringify(items) !== JSON.stringify(manifest.products) || manifest.accountCount !== accounts.length) throw new Error('Stale manifest: run data/build-manifest.cjs');
  return items;
});
if (!manifest.datasetId || manifest.keywords.length < 10 || manifest.keywords.length > 15 || new Set(manifest.keywords.map(k => k.keyword)).size !== manifest.keywords.length) throw new Error('Invalid manifest');
for (const k of manifest.keywords) {
  const expected = manifest.products.filter(p => p.name.toLowerCase().includes(k.keyword.toLowerCase())).map(p => p.id).sort((a,b) => a-b);
  if (!expected.length || JSON.stringify(expected) !== JSON.stringify(k.expectedIds)) throw new Error('Invalid keyword expected IDs');
}
const weights = Object.values(keywordWeights);
if (weights.length !== manifest.keywords.length ||
    manifest.keywords.some(k => !Object.prototype.hasOwnProperty.call(keywordWeights, k.keyword)) ||
    weights.some(weight => !Number.isFinite(weight) || weight <= 0) ||
    weights.reduce((sum, weight) => sum + weight, 0) !== 100) {
  throw new Error('Invalid keyword weights: match manifest keywords and total 100');
}
export function keyword() {
  let r = Math.random() * 100;
  for (const k of manifest.keywords) {
    r -= keywordWeights[k.keyword];
    if (r < 0) return k;
  }
  return manifest.keywords[manifest.keywords.length - 1];
}
export function json(response) { try { return response.json(); } catch (_) { return null; } }
export function matchesIds(body, ids) {
  return Array.isArray(body) && body.length === ids.length && JSON.stringify(body.map(p => p.id).sort((a,b) => a-b)) === JSON.stringify(ids);
}
// Read-only and outside the stress scenario. Preflight metrics have a separate phase.
export function preflight() {
  const params = { timeout: '10s', tags: { phase: 'preflight', endpoint: 'preflight', name: 'GET catalogue preflight' } };
  const response = http.get(`${baseUrl}/api/products`, params);
  const body = json(response);
  if (response.status !== 200 || !Array.isArray(body) || !manifest.products.every(p => body.some(row => row.id === p.id && row.name === p.name && Number(row.price) === p.price))) throw new Error('Preflight: server catalogue does not match fixture; seed backend first');
  for (const k of manifest.keywords) {
    const res = http.get(`${baseUrl}/api/products?search=${encodeURIComponent(k.keyword)}`, params);
    if (res.status !== 200 || !matchesIds(json(res), k.expectedIds)) throw new Error(`Preflight: search mismatch for ${k.keyword}`);
  }
  console.log(`Stress dataset=${manifest.datasetId}, accounts=${accounts.length}, products=${products.length}; login per protected iteration`);
}