#!/usr/bin/env node
'use strict';

// Run AFTER starting the backend: its startup recreates all database tables.
// Usage: node data/seed.js [database-path] (from performance/k6)
// The optional path is useful for seeding a separate test database.
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const backendRequire = createRequire(path.resolve(__dirname, '../../../backend/package.json'));
const sqlite3 = backendRequire('sqlite3');

const accountsCsvPath = path.join(__dirname, 'test_accounts.csv');
const productsCsvPath = path.join(__dirname, 'test_product.csv');
const dbPath = path.resolve(process.argv[2] || path.join(__dirname, '../../../backend/database.sqlite'));

// Handle quoted fields, escaped quotes, BOM, CRLF and a missing final newline.
function parseCsv(text, expectedFields, label) {
  const rows = [];
  const pattern = /(?:^|,)(?:"((?:[^"]|"")*)"|([^",\r\n]*))(?=,|$)/gy;
  for (const [index, line] of text.replace(/^\uFEFF/, '').split(/\r?\n/).entries()) {
    if (!line.trim()) continue;
    const fields = [];
    pattern.lastIndex = 0;
    let match;
    let end = 0;
    while ((match = pattern.exec(line)) !== null) {
      fields.push(match[1] === undefined ? match[2] : match[1].replace(/""/g, '"'));
      end = pattern.lastIndex;
      if (end === line.length) break;
    }
    if (end !== line.length || fields.length !== expectedFields) {
      throw new Error(`Invalid ${label} CSV row ${index + 1}: expected ${expectedFields} single-line fields.`);
    }
    rows.push(fields);
  }
  return rows;
}

function readAccounts() {
  const [header, ...rows] = parseCsv(fs.readFileSync(accountsCsvPath, 'utf8'), 4, 'account');
  if (!header || header.join(',') !== 'email,password,name,role') {
    throw new Error('CSV header must be email,password,name,role.');
  }
  if (!rows.length) throw new Error('CSV contains no accounts.');
  const emails = new Set();
  return rows.map(([email, password, name, role], index) => {
    if (![email, password, name, role].every(value => value.trim()) ||
        !['user', 'admin'].includes(role) || emails.has(email)) {
      throw new Error(`Invalid or duplicate account at CSV record ${index + 2}.`);
    }
    emails.add(email);
    return { email, password, name, role };
  });
}

function readProducts() {
  const [header, ...rows] = parseCsv(fs.readFileSync(productsCsvPath, 'utf8'), 7, 'product');
  const expectedHeader = 'product_id,name,price,description,image_url,category_id,search_keyword';
  if (!header || header.join(',') !== expectedHeader) {
    throw new Error(`Product CSV header must be ${expectedHeader}.`);
  }
  if (!rows.length) throw new Error('Product CSV contains no products.');
  const ids = new Set();
  return rows.map(([productId, name, price, description, imageUrl, categoryId, searchKeyword], index) => {
    const id = Number(productId);
    const amount = Number(price);
    const category = Number(categoryId);
    if (![productId, name, price, description, imageUrl, categoryId, searchKeyword].every(value => value.trim()) ||
        !Number.isSafeInteger(id) || id <= 0 || ids.has(id) ||
        !Number.isSafeInteger(amount) || amount <= 0 ||
        !Number.isSafeInteger(category) || category <= 0) {
      throw new Error(`Invalid or duplicate product at CSV record ${index + 2}.`);
    }
    ids.add(id);
    return { id, name, price: amount, description, imageUrl, categoryId: category };
  });
}

function run(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function (error) {
      if (error) reject(error);
      else resolve(this.changes);
    });
  });
}

async function main() {
  if (process.argv.length > 3) throw new Error('Usage: node seed.js [database-path]');
  const accounts = readAccounts();
  const products = readProducts();
  // OPEN_READWRITE avoids silently creating an empty database at a wrong path.
  const db = await new Promise((resolve, reject) => {
    const connection = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE, error => {
      if (error) reject(error);
      else resolve(connection);
    });
  });
  db.configure('busyTimeout', 5000);
  let transaction = false;
  let inserted = 0;
  let updated = 0;
  let productsInserted = 0;
  let productsUpdated = 0;
  try {
    await run(db, 'BEGIN IMMEDIATE');
    transaction = true;
    for (const { email, password, name, role } of accounts) {
      // email has no UNIQUE constraint in this SUT; do not use ON CONFLICT.
      const changes = await run(db, `UPDATE users
        SET name = ?, password = ?, role = ?, login_attempts = 0,
            locked_until = NULL, reset_token = NULL
        WHERE email = ?`, [name, password, role, email]);
      if (changes > 1) throw new Error('Database contains duplicate emails for a CSV account.');
      if (changes === 1) {
        updated++;
      } else {
        // Preserve plaintext passwords to match the SUT login implementation.
        await run(db, 'INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
          [name, email, password, role]);
        inserted++;
      }
    }
    for (const { id, name, price, description, imageUrl, categoryId } of products) {
      const changes = await run(db, `UPDATE products
        SET name = ?, price = ?, description = ?, imageUrl = ?, category_id = ?
        WHERE id = ?`, [name, price, description, imageUrl, categoryId, id]);
      if (changes > 1) throw new Error(`Database contains duplicate product ID ${id}.`);
      if (changes === 1) {
        productsUpdated++;
      } else {
        await run(db, `INSERT INTO products (id, name, price, description, imageUrl, category_id)
          VALUES (?, ?, ?, ?, ?, ?)`, [id, name, price, description, imageUrl, categoryId]);
        productsInserted++;
      }
    }
    await run(db, 'COMMIT');
    transaction = false;
  } catch (error) {
    if (transaction) await run(db, 'ROLLBACK');
    throw error;
  } finally {
    await new Promise((resolve, reject) => db.close(error => error ? reject(error) : resolve()));
  }
  console.log(`Seeded ${accounts.length} accounts: ${inserted} inserted, ${updated} updated; ${productsInserted} products inserted, ${productsUpdated} updated.\nDatabase: ${dbPath}`);
}

main().catch(error => {
  console.error(`Seed failed: ${error.message}`);
  process.exitCode = 1;
});
