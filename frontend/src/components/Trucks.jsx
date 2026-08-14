import React, { useState } from 'react'
import { money } from '../lib/format'

const BLANK = {
  name: '',
  year: '',
  make: '',
  model: '',
  vin: '',
  mileage: '',
  purchase_price: '',
  purchase_date: '',
  loan_balance: '',
}

export default function Trucks({ store }) {
  const [editing, setEditing] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  async function save(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await store.saveTruck(editing)
      setEditing(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="view">
      <div className="view-head">
        <h2 className="view-title">Trucks</h2>
        <button className="btn small" onClick={() => setEditing({ ...BLANK })}>
          Add truck
        </button>
      </div>

      {store.trucks.length === 0 && <p className="empty">No trucks yet.</p>}

      {store.trucks.map((t) => (
        <div className="panel" key={t.id}>
          <div className="panel-head">
            <div>
              <div className="panel-title">{t.name}</div>
              <div className="panel-sub">
                {[t.year, t.make, t.model].filter(Boolean).join(' ') || 'No details'}
              </div>
            </div>
            <button className="btn small ghost" onClick={() => setEditing(t)}>
              Edit
            </button>
          </div>
          <div className="kv-grid">
            <div>
              <span>Mileage</span>
              <strong>{t.mileage ? t.mileage.toLocaleString() : '—'}</strong>
            </div>
            <div>
              <span>Loan balance</span>
              <strong>{money(t.loan_balance)}</strong>
            </div>
            <div>
              <span>Purchase price</span>
              <strong>{money(t.purchase_price)}</strong>
            </div>
            <div>
              <span>VIN</span>
              <strong className="mono">{t.vin || '—'}</strong>
            </div>
          </div>
        </div>
      ))}

      {editing && (
        <div className="sheet-backdrop" onClick={() => setEditing(null)}>
          <form className="sheet" onClick={(e) => e.stopPropagation()} onSubmit={save}>
            <div className="sheet-grip" />
            <div className="sheet-body">
              <h3 className="sheet-title">{editing.id ? 'Edit truck' : 'Add truck'}</h3>

              <label className="field">
                <span>Name</span>
                <input
                  value={editing.name}
                  onChange={(e) => setEditing({ ...editing, name: e.target.value })}
                  placeholder="Unit 1"
                  required
                />
              </label>

              <div className="field-row">
                <label className="field">
                  <span>Year</span>
                  <input
                    type="number"
                    value={editing.year ?? ''}
                    onChange={(e) => setEditing({ ...editing, year: e.target.value })}
                  />
                </label>
                <label className="field">
                  <span>Make</span>
                  <input
                    value={editing.make ?? ''}
                    onChange={(e) => setEditing({ ...editing, make: e.target.value })}
                  />
                </label>
              </div>

              <div className="field-row">
                <label className="field">
                  <span>Model</span>
                  <input
                    value={editing.model ?? ''}
                    onChange={(e) => setEditing({ ...editing, model: e.target.value })}
                  />
                </label>
                <label className="field">
                  <span>Mileage</span>
                  <input
                    type="number"
                    value={editing.mileage ?? ''}
                    onChange={(e) => setEditing({ ...editing, mileage: e.target.value })}
                  />
                </label>
              </div>

              <label className="field">
                <span>VIN</span>
                <input
                  value={editing.vin ?? ''}
                  onChange={(e) => setEditing({ ...editing, vin: e.target.value })}
                />
              </label>

              <div className="field-row">
                <label className="field">
                  <span>Purchase price</span>
                  <input
                    type="number"
                    step="0.01"
                    value={editing.purchase_price ?? ''}
                    onChange={(e) => setEditing({ ...editing, purchase_price: e.target.value })}
                  />
                </label>
                <label className="field">
                  <span>Purchase date</span>
                  <input
                    type="date"
                    value={editing.purchase_date ?? ''}
                    onChange={(e) => setEditing({ ...editing, purchase_date: e.target.value })}
                  />
                </label>
              </div>

              <label className="field">
                <span>Loan balance</span>
                <input
                  type="number"
                  step="0.01"
                  value={editing.loan_balance ?? ''}
                  onChange={(e) => setEditing({ ...editing, loan_balance: e.target.value })}
                />
              </label>

              {error && <p className="banner error">{error}</p>}
            </div>

            <div className="sheet-actions">
              {editing.id && (
                <button
                  type="button"
                  className="btn danger ghost"
                  onClick={async () => {
                    await store.deleteTruck(editing.id)
                    setEditing(null)
                  }}
                >
                  Delete
                </button>
              )}
              <button type="button" className="btn ghost" onClick={() => setEditing(null)}>
                Cancel
              </button>
              <button className="btn primary" disabled={busy}>
                {busy ? 'Saving…' : 'Save'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
