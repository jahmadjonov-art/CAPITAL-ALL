const express = require('express');
const db = require('../db');

const router = express.Router();

router.get('/', (req, res) => {
  const rows = db.prepare('SELECT * FROM trucks ORDER BY id DESC').all();
  res.json(rows);
});

router.post('/', (req, res) => {
  const { name, year, make, model, vin, mileage, purchase_price, purchase_date, loan_balance } = req.body;
  const stmt = db.prepare('INSERT INTO trucks (name, year, make, model, vin, mileage, purchase_price, purchase_date, loan_balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
  const info = stmt.run(name, year, make, model, vin, mileage || null, purchase_price || 0, purchase_date || null, loan_balance || 0);
  const truck = db.prepare('SELECT * FROM trucks WHERE id = ?').get(info.lastInsertRowid);
  res.json(truck);
});

module.exports = router;
