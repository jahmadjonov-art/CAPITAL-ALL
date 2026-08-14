const fs = require('fs');
const path = require('path');
const db = require('./src/db');

function run() {
  // Create tables
  db.exec(`
  PRAGMA foreign_keys = ON;
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
  );

  CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    manager_salary_cap REAL DEFAULT 4000,
    min_capital_pct REAL DEFAULT 50,
    repair_target REAL DEFAULT 30000,
    tax_pct REAL DEFAULT 20,
    current_truck_loan REAL DEFAULT 10000,
    future_truck_target REAL DEFAULT 50000
  );

  CREATE TABLE IF NOT EXISTS buckets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    balance REAL DEFAULT 0
  );

  CREATE TABLE IF NOT EXISTS trucks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year INTEGER,
    make TEXT,
    model TEXT,
    vin TEXT,
    mileage INTEGER,
    purchase_price REAL,
    purchase_date TEXT,
    loan_balance REAL
  );

  CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    amount REAL,
    type TEXT,
    bucket TEXT,
    category TEXT,
    payee TEXT,
    notes TEXT,
    truck_id INTEGER,
    odometer INTEGER
  );
  `);

  // Insert default settings row if missing
  const s = db.prepare('SELECT COUNT(*) as c FROM settings').get();
  if (!s.c) {
    db.prepare('INSERT INTO settings (id, manager_salary_cap, min_capital_pct, repair_target, tax_pct, current_truck_loan, future_truck_target) VALUES (1,?,?,?,?,?,?)').run(4000,50,30000,20,10000,50000);
  }

  // Insert default buckets
  const b = db.prepare('SELECT COUNT(*) as c FROM buckets').get();
  if (!b.c) {
    const buckets = ['Truck / Capital Fund','Truck Repair Reserve','Tax Reserve','Personal / Manager Salary','Current Truck Loan','Future Truck'];
    const stmt = db.prepare('INSERT INTO buckets (name, balance) VALUES (?,?)');
    for (const name of buckets) stmt.run(name, 0);
  }

  // Insert demo truck
  const t = db.prepare('SELECT COUNT(*) as c FROM trucks').get();
  if (!t.c) {
    db.prepare('INSERT INTO trucks (name, year, make, model, vin, mileage, purchase_price, purchase_date, loan_balance) VALUES (?,?,?,?,?,?,?,?,?)')
      .run('Demo Truck', 2018, 'Freightliner', 'Cascadia', 'VINDEMO123', 250000, 80000, '2023-05-01', 10000);
  }

  // Insert some demo transactions if none exist
  const tx = db.prepare('SELECT COUNT(*) as c FROM transactions').get();
  if (!tx.c) {
    const ins = db.prepare('INSERT INTO transactions (date, amount, type, bucket, category, payee, notes) VALUES (?,?,?,?,?,?,?)');
    ins.run('2026-08-01', 16000, 'income', 'Truck / Capital Fund', 'Load Income', 'Dispatch Co', 'Demo income');
    ins.run('2026-08-02', -120, 'expense', 'Personal / Manager Salary', 'Food', 'Grocery Store', 'Groceries');
    ins.run('2026-08-05', -400, 'expense', 'Truck Repair Reserve', 'Electrical / Parts', 'Mechanic', 'Alternator');
    ins.run('2026-08-06', -1500, 'expense', 'Current Truck Loan', 'Loan Payment', 'Bank', 'Monthly truck payment');
  }

  console.log('Seed complete.');
}

run();
