import React, { useMemo, useState } from 'react'
import { BUCKETS, BUCKET_NAMES } from '../lib/allocate'
import { moneyExact, prettyDate } from '../lib/format'

export default function Transactions({ store }) {
  const [filter, setFilter] = useState('all')
  const [pendingDelete, setPendingDelete] = useState(null)

  const rows = useMemo(() => {
    if (filter === 'all') return store.transactions
    return store.transactions.filter((tx) => tx.bucket_key === filter)
  }, [store.transactions, filter])

  // Income splits and transfers write several rows at once; showing them under
  // one date heading keeps the ledger readable.
  const byDate = useMemo(() => {
    const groups = new Map()
    for (const tx of rows) {
      if (!groups.has(tx.date)) groups.set(tx.date, [])
      groups.get(tx.date).push(tx)
    }
    return [...groups.entries()]
  }, [rows])

  async function confirmDelete(tx) {
    await store.deleteTransaction(tx)
    setPendingDelete(null)
  }

  return (
    <div className="view">
      <h2 className="view-title">Transactions</h2>

      <div className="chips">
        <button
          className={`chip ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        {BUCKETS.map((b) => (
          <button
            key={b.key}
            className={`chip ${filter === b.key ? 'active' : ''}`}
            onClick={() => setFilter(b.key)}
          >
            {b.name.split(' / ')[0]}
          </button>
        ))}
      </div>

      {rows.length === 0 ? (
        <p className="empty">No transactions here yet.</p>
      ) : (
        byDate.map(([date, items]) => (
          <div key={date} className="day-group">
            <div className="day-label">{prettyDate(date)}</div>
            {items.map((tx) => (
              <div className="tx" key={tx.id}>
                <div className="tx-main">
                  <div className="tx-title">{tx.category || tx.payee || 'Entry'}</div>
                  <div className="tx-meta">
                    {BUCKET_NAMES[tx.bucket_key] || tx.bucket_key}
                    {tx.payee && tx.category ? ` · ${tx.payee}` : ''}
                    {tx.notes ? ` · ${tx.notes}` : ''}
                  </div>
                </div>
                <div className={`tx-amount ${Number(tx.amount) < 0 ? 'neg' : 'pos'}`}>
                  {moneyExact(tx.amount)}
                </div>
                <button
                  className="tx-del"
                  onClick={() => setPendingDelete(tx)}
                  aria-label="Delete transaction"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        ))
      )}

      {pendingDelete && (
        <div className="sheet-backdrop" onClick={() => setPendingDelete(null)}>
          <div className="confirm" onClick={(e) => e.stopPropagation()}>
            <h3>Delete this entry?</h3>
            <p>
              {pendingDelete.group_id
                ? 'This was part of a split. Every line from that same entry will be removed together, so your balances stay correct.'
                : 'This removes one line from the ledger.'}
            </p>
            <div className="sheet-actions">
              <button className="btn ghost" onClick={() => setPendingDelete(null)}>
                Keep it
              </button>
              <button className="btn danger" onClick={() => confirmDelete(pendingDelete)}>
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
