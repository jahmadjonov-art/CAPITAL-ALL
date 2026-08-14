const express = require('express');
const db = require('../db');

const router = express.Router();

router.get('/', (req, res) => {
  const row = db.prepare('SELECT * FROM settings WHERE id = 1').get();
  res.json(row);
});

router.post('/', (req, res) => {
  const s = req.body;
  db.prepare(`UPDATE settings SET
    manager_salary_cap = ?,
    min_capital_pct = ?,
    repair_target = ?,
    tax_pct = ?,
    current_truck_loan = ?,
    future_truck_target = ?
    WHERE id = 1`).run(s.manager_salary_cap, s.min_capital_pct, s.repair_target, s.tax_pct, s.current_truck_loan, s.future_truck_target);
  res.json({ ok: true });
});

module.exports = router;
