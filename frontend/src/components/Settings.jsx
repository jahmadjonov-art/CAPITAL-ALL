import React, { useEffect, useState } from 'react'
import { supabase } from '../supabaseClient'
import { allocateIncome } from '../lib/allocate'
import { money, moneyExact } from '../lib/format'

const FIELDS = [
  { key: 'tax_pct', label: 'Tax withholding', suffix: '%', hint: 'Taken off the top of every income event.' },
  { key: 'repair_pct', label: 'Repair reserve', suffix: '%', hint: 'Of gross income, until the reserve hits its target.' },
  { key: 'repair_target', label: 'Repair reserve target', prefix: '$', hint: 'Funding stops once the reserve reaches this.' },
  { key: 'min_capital_pct', label: 'Minimum to capital', suffix: '%', hint: 'The floor your capital fund always gets.' },
  { key: 'manager_salary_cap', label: 'Manager salary cap', prefix: '$', hint: 'Most you pay yourself from one income event.' },
  { key: 'future_truck_target', label: 'Future truck goal', prefix: '$', hint: 'Savings target for the next truck.' },
]

// A worked example beats six abstract percentages — this shows what the current
// settings would actually do to a typical load payment.
const SAMPLE = 10000

export default function Settings({ store, session }) {
  const [draft, setDraft] = useState(store.settings)
  const [busy, setBusy] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => setDraft(store.settings), [store.settings])

  const preview = allocateIncome({
    amount: SAMPLE,
    settings: draft,
    repairBalance: store.balances.truck_repair || 0,
  })

  async function save(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await store.saveSettings(draft)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="view">
      <h2 className="view-title">Allocation rules</h2>

      <form onSubmit={save}>
        <div className="panel">
          {FIELDS.map((f) => (
            <label className="field setting" key={f.key}>
              <span>
                {f.label}
                <em>{f.hint}</em>
              </span>
              <div className="input-affix">
                {f.prefix && <i>{f.prefix}</i>}
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={draft[f.key] ?? ''}
                  onChange={(e) => setDraft({ ...draft, [f.key]: e.target.value })}
                />
                {f.suffix && <i>{f.suffix}</i>}
              </div>
            </label>
          ))}
        </div>

        <div className="preview">
          <div className="preview-title">A {money(SAMPLE)} load would split into</div>
          {preview.lines.map((line) => (
            <div className="preview-row" key={line.bucket_key}>
              <span>{line.category}</span>
              <strong>{moneyExact(line.amount)}</strong>
            </div>
          ))}
        </div>

        {error && <p className="banner error">{error}</p>}

        <button className="btn primary block" disabled={busy}>
          {busy ? 'Saving…' : saved ? 'Saved' : 'Save rules'}
        </button>
      </form>

      <h2 className="view-title">Account</h2>
      <div className="panel">
        <div className="panel-sub">Signed in as {session?.user?.email}</div>
        <button className="btn ghost block" onClick={() => supabase.auth.signOut()}>
          Sign out
        </button>
      </div>
    </div>
  )
}
