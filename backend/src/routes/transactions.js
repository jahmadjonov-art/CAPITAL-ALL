const express = require('express');
const db = require('../db');

const router = express.Router();

router.get('/', (req, res) => {
  const rows = db.prepare('SELECT * FROM transactions ORDER BY date DESC LIMIT 100').all();
  res.json(rows);
});

router.post('/', (req, res) => {
  const { date, amount, type, bucket, category, payee, notes, truck_id, odometer } = req.body;
  const stmt = db.prepare('INSERT INTO transactions (date, amount, type, bucket, category, payee, notes, truck_id, odometer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
  const info = stmt.run(date, amount, type, bucket, category, payee, notes, truck_id || null, odometer || null);
  const tx = db.prepare('SELECT * FROM transactions WHERE id = ?').get(info.lastInsertRowid);
  res.json(tx);
});

module.exports = router;
