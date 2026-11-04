#!/usr/bin/env node
// Single-line CSV parser matching seed.js. Run again whenever fixtures change.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
function read(name, header) {
  const text = fs.readFileSync(path.join(__dirname, name), 'utf8');
  const lines = text.replace(/^\uFEFF/, '').trim().split(/\r?\n/);
  if (lines.shift() !== header) throw new Error('Invalid header: ' + name);
  const rows = lines.map(line => {
    const fields = []; const re = /(?:^|,)(?:"((?:[^"]|"")*)"|([^",\r\n]*))(?=,|$)/gy;
    let m, end = 0;
    while ((m = re.exec(line))) { fields.push(m[1] === undefined ? m[2] : m[1].replace(/""/g, '"')); end = re.lastIndex; if (end === line.length) break; }
    if (end !== line.length || fields.length !== header.split(',').length) throw new Error('Invalid row: ' + name);
    return fields;
  });
  return { rows, hash: crypto.createHash('sha256').update(text).digest('hex') };
}
const a = read('test_accounts.csv', 'email,password,name,role');
const p = read('test_products.csv', 'product_id,name,price,description,image_url,category_id,search_keyword');
const products = p.rows.map(([id, name, price]) => ({ id: Number(id), name, price: Number(price) }));
const keywords = ["iPhone", "Samsung", "MacBook", "AirPods", "iPad", "Apple Watch", "Sony", "Keychron", "Logitech", "Dell", "Asus", "Xiaomi"];
const manifest = {
  datasetId: `test-data-${a.hash.slice(0,12)}-${p.hash.slice(0,12)}`,
  sourceHashes: { accounts: a.hash, products: p.hash }, accountCount: a.rows.length,
  products,
  keywords: keywords.map(keyword => ({ keyword, expectedIds: products.filter(p => p.name.toLowerCase().includes(keyword.toLowerCase())).map(p => p.id).sort((a,b) => a-b) })),
};
fs.writeFileSync(path.join(__dirname, 'test-data-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`Built manifest ${manifest.datasetId}`);
