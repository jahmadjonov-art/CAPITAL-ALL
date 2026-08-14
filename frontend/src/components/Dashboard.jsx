import React from 'react'
import { BUCKETS } from '../lib/allocate'
import { money, prettyDate } from '../lib/format'

function Stat({ label, value, tone }) {
  return (
    <div className={`stat ${tone || ''}`}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  )
}

function BucketRow({ bucket, balance, target }) {
  const pct = target > 0 ? Math.min(100, (balance / target) * 100) : null
  return (
    <div className="bucket">
      <div className="bucket-head">
        <span className="bucket-name">{bucket.name}</span>
        <span className="bucket-amount">{money(balance)}</span>
      </div>
      {pct !== null && (
        <>
          <div className="meter">
            <div
              className={`meter-fill ${pct >= 100 ? 'full' : ''}`}
              style={{ width: `${Math.max(pct, 1.5)}%` }}
            />
          </div>
          <div className="bucket-sub">
            {pct >= 100 ? 'Target reached' : `${Math.round(pct)}% of ${money(target)} target`}
          </div>
        </>
      )}
    </div>
  )
}

export default function Dashboard({ balances, summary, settings, transactions }) {
  const targets = {
    truck_repair: Number(settings.repair_target),
    future_truck: Number(settings.future_truck_target),
  }
  const recent = transactions.slice(0, 8)

  return (
    <div className="view">
      <h2 className="view-title">This month</h2>
      <div className="stat-grid">
        <Stat label="Income allocated" value={money(summary.income)} tone="up" />
        <Stat label="Spent" value={money(summary.spend)} tone="down" />
        <Stat label="Salary paid" value={money(summary.salaryPaid)} />
        <Stat label="Salary left in cap" value={money(summary.salaryRemaining)} />
      </div>

      <h2 className="view-title">Buckets</h2>
      <div className="bucket-list">
        {BUCKETS.map((b) => (
          <BucketRow key={b.key} bucket={b} balance={balances[b.key] || 0} target={targets[b.key]} />
        ))}
      </div>

      <h2 className="view-title">Recent activity</h2>
      {recent.length === 0 ? (
        <p className="empty">
          Nothing logged yet. Tap <strong>+</strong> to record your first income event.
        </p>
      ) : (
        <div className="tx-list">
          {recent.map((tx) => (
            <div className="tx" key={tx.id}>
              <div className="tx-main">
                <div className="tx-title">{tx.category || tx.payee || tx.bucket_key}</div>
                <div className="tx-meta">
                  {prettyDate(tx.date)} · {BUCKETS.find((b) => b.key === tx.bucket_key)?.name}
                </div>
              </div>
              <div className={`tx-amount ${Number(tx.amount) < 0 ? 'neg' : 'pos'}`}>
                {money(tx.amount)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
