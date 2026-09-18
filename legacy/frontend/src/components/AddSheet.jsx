import React, { useMemo, useState } from 'react'
import { BUCKETS, BUCKET_NAMES, allocateIncome } from '../lib/allocate'
import { money, moneyExact, todayISO } from '../lib/format'

const EXPENSE_CATEGORIES = [
  'Fuel',
  'Repair / Parts',
  'Insurance',
  'Loan Payment',
  'Permits & Fees',
  'Food',
  'Lodging',
  'Other',
]

export default function AddSheet({ store, onClose }) {
  const [tab, setTab] = useState('income')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  const [date, setDate] = useState(todayISO())
  const [amount, setAmount] = useState('')
  const [payee, setPayee] = useState('')
  const [notes, setNotes] = useState('')

  const [bucketKey, setBucketKey] = useState('personal')
  const [category, setCategory] = useState('Fuel')
  const [truckId, setTruckId] = useState('')
  const [odometer, setOdometer] = useState('')

  const [from, setFrom] = useState('capital')
  const [to, setTo] = useState('future_truck')

  // Live preview of the waterfall, so you see exactly where the money lands
  // before anything is written.
  const preview = useMemo(() => {
    if (tab !== 'income') return null
    return allocateIncome({
      amount: Number(amount),
      settings: store.settings,
      repairBalance: store.balances.truck_repair || 0,
    })
  }, [tab, amount, store.settings, store.balances])

  async function submit(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      if (tab === 'income') {
        await store.addIncome({ date, amount: Number(amount), payee, notes })
      } else if (tab === 'expense') {
        await store.addExpense({
          date,
          amount: Number(amount),
          bucket_key: bucketKey,
          category,
          payee,
          notes,
          truck_id: truckId || null,
          odometer,
        })
      } else {
        await store.addTransfer({ date, amount: Number(amount), from, to, notes })
      }
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="sheet-backdrop" onClick={onClose}>
      <form className="sheet" onClick={(e) => e.stopPropagation()} onSubmit={submit}>
        <div className="sheet-grip" />

        <div className="tabs">
          {['income', 'expense', 'transfer'].map((t) => (
            <button
              key={t}
              type="button"
              className={`tab ${tab === t ? 'active' : ''}`}
              onClick={() => {
                setTab(t)
                setError(null)
              }}
            >
              {t[0].toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="sheet-body">
          <label className="field">
            <span>Amount</span>
            <input
              type="number"
              inputMode="decimal"
              step="0.01"
              min="0"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.00"
              autoFocus
              required
            />
          </label>

          <label className="field">
            <span>Date</span>
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
          </label>

          {tab === 'income' && (
            <>
              <label className="field">
                <span>Paid by</span>
                <input
                  value={payee}
                  onChange={(e) => setPayee(e.target.value)}
                  placeholder="Dispatch company, broker…"
                />
              </label>

              {preview?.lines.length > 0 && (
                <div className="preview">
                  <div className="preview-title">
                    {money(preview.gross)} splits into
                  </div>
                  {preview.lines.map((line) => (
                    <div className="preview-row" key={line.bucket_key}>
                      <span>{BUCKET_NAMES[line.bucket_key]}</span>
                      <strong>{moneyExact(line.amount)}</strong>
                    </div>
                  ))}
                  <div className="preview-note">
                    Adjust the percentages in Settings to change this split.
                  </div>
                </div>
              )}
            </>
          )}

          {tab === 'expense' && (
            <>
              <label className="field">
                <span>Paid from</span>
                <select value={bucketKey} onChange={(e) => setBucketKey(e.target.value)}>
                  {BUCKETS.map((b) => (
                    <option key={b.key} value={b.key}>
                      {b.name} — {money(store.balances[b.key] || 0)}
                    </option>
                  ))}
                </select>
              </label>

              <label className="field">
                <span>Category</span>
                <select value={category} onChange={(e) => setCategory(e.target.value)}>
                  {EXPENSE_CATEGORIES.map((c) => (
                    <option key={c}>{c}</option>
                  ))}
                </select>
              </label>

              <label className="field">
                <span>Paid to</span>
                <input
                  value={payee}
                  onChange={(e) => setPayee(e.target.value)}
                  placeholder="Shop, vendor, bank…"
                />
              </label>

              {store.trucks.length > 0 && (
                <div className="field-row">
                  <label className="field">
                    <span>Truck</span>
                    <select value={truckId} onChange={(e) => setTruckId(e.target.value)}>
                      <option value="">None</option>
                      {store.trucks.map((t) => (
                        <option key={t.id} value={t.id}>
                          {t.name}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className="field">
                    <span>Odometer</span>
                    <input
                      type="number"
                      inputMode="numeric"
                      value={odometer}
                      onChange={(e) => setOdometer(e.target.value)}
                      placeholder="miles"
                    />
                  </label>
                </div>
              )}
            </>
          )}

          {tab === 'transfer' && (
            <div className="field-row">
              <label className="field">
                <span>From</span>
                <select value={from} onChange={(e) => setFrom(e.target.value)}>
                  {BUCKETS.map((b) => (
                    <option key={b.key} value={b.key}>
                      {b.name}
                    </option>
                  ))}
                </select>
              </label>
              <label className="field">
                <span>To</span>
                <select value={to} onChange={(e) => setTo(e.target.value)}>
                  {BUCKETS.map((b) => (
                    <option key={b.key} value={b.key}>
                      {b.name}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          )}

          <label className="field">
            <span>Note</span>
            <input
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Optional"
            />
          </label>

          {error && <p className="banner error">{error}</p>}
        </div>

        <div className="sheet-actions">
          <button type="button" className="btn ghost" onClick={onClose}>
            Cancel
          </button>
          <button className="btn primary" disabled={busy}>
            {busy ? 'Saving…' : 'Save'}
          </button>
        </div>
      </form>
    </div>
  )
}
