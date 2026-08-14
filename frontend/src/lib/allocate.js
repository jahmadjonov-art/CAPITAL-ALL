// The allocation waterfall — the one piece of real logic in this app.
//
// This used to live in a Supabase Edge Function. It does not need to: it is
// arithmetic over a handful of numbers, so it runs in the browser where you
// can see the split before you commit it.

export const BUCKETS = [
  { key: 'capital', name: 'Truck / Capital Fund', sort: 1 },
  { key: 'truck_repair', name: 'Truck Repair Reserve', sort: 2 },
  { key: 'tax_reserve', name: 'Tax Reserve', sort: 3 },
  { key: 'personal', name: 'Personal / Manager Salary', sort: 4 },
  { key: 'future_truck', name: 'Future Truck', sort: 5 },
]

export const BUCKET_NAMES = Object.fromEntries(BUCKETS.map((b) => [b.key, b.name]))

export const DEFAULT_SETTINGS = {
  tax_pct: 20,
  repair_pct: 10,
  repair_target: 30000,
  min_capital_pct: 50,
  manager_salary_cap: 4000,
  future_truck_target: 50000,
}

const round2 = (n) => Math.round((Number(n) || 0) * 100) / 100

/**
 * Split one gross income event across the buckets, in priority order.
 *
 *   1. Taxes come off the top — that money was never yours.
 *   2. The repair reserve is topped up, but only until it reaches its target.
 *   3. Capital takes its guaranteed floor percentage.
 *   4. You pay yourself whatever is left, up to the salary cap.
 *   5. Any surplus above the cap falls back into capital.
 *
 * Every step draws from a running remainder that is clamped at zero, so an
 * aggressive settings combination (say 60% tax + 60% capital) can starve the
 * later buckets but can never allocate more than came in. The returned lines
 * always sum to exactly the gross amount.
 *
 * @param {object}  args
 * @param {number}  args.amount        gross income for this event
 * @param {object}  args.settings      the user's allocation knobs
 * @param {number}  args.repairBalance current truck-repair reserve balance
 * @returns {{lines: Array, gross: number, allocated: number}}
 */
export function allocateIncome({ amount, settings, repairBalance = 0 }) {
  const gross = round2(amount)
  const s = { ...DEFAULT_SETTINGS, ...(settings || {}) }

  if (!(gross > 0)) return { lines: [], gross: 0, allocated: 0 }

  let remaining = gross

  // Draw `want` from the remainder, never more than is actually left.
  const draw = (want) => {
    const taken = Math.max(0, Math.min(round2(want), remaining))
    remaining = round2(remaining - taken)
    return taken
  }

  const lines = []
  const push = (bucket_key, value, category, notes) => {
    if (value > 0) lines.push({ bucket_key, amount: value, category, notes })
  }

  const tax = draw((gross * Number(s.tax_pct)) / 100)
  push('tax_reserve', tax, 'Tax Reserve', `${s.tax_pct}% of gross withheld for taxes`)

  // Only fund repairs up to the gap between the reserve and its target — once
  // the truck fund is full, that money is better off as capital.
  const repairGap = Math.max(0, round2(Number(s.repair_target) - Number(repairBalance)))
  const repair = draw(Math.min((gross * Number(s.repair_pct)) / 100, repairGap))
  push(
    'truck_repair',
    repair,
    'Repair Reserve',
    repairGap <= 0
      ? 'Repair reserve already at target'
      : `${s.repair_pct}% of gross, capped at the remaining gap to target`
  )

  const capitalFloor = draw((gross * Number(s.min_capital_pct)) / 100)

  const salary = draw(Math.min(Number(s.manager_salary_cap), remaining))
  push('personal', salary, 'Manager Salary', `Paid to you, capped at ${s.manager_salary_cap}`)

  // Anything still left is above your salary cap, so it compounds as capital.
  const surplus = draw(remaining)
  const capitalTotal = round2(capitalFloor + surplus)
  push(
    'capital',
    capitalTotal,
    'Capital Allocation',
    surplus > 0
      ? `${s.min_capital_pct}% floor plus ${surplus.toFixed(2)} surplus over the salary cap`
      : `${s.min_capital_pct}% floor`
  )

  return {
    lines,
    gross,
    allocated: round2(lines.reduce((sum, l) => sum + l.amount, 0)),
  }
}
