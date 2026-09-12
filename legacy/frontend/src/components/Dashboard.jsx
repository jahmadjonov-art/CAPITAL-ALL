import React from 'react'
import { BUCKETS, BUCKET_NAMES } from '../lib/allocate'
import { money, moneyExact, prettyDate } from '../lib/format'

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

// The headline card: what the most recent payday did, in full. This is the
// answer to "I got paid, where does it go" without opening anything else.
function LastPaycheck({ paycheck }) {
  return (
    <div className="paycheck">
      <div className="paycheck-head">
        <div>
          <div className="paycheck-label">
            Last paycheck · {prettyDate(paycheck.date)}
            {paycheck.payee ? ` · ${paycheck.payee}` : ''}
          </div>
          <div className="paycheck-gross">{money(paycheck.gross)}</div>
        </div>
        <div className="paycheck-yours">
          <span>Your pay</span>
          <strong>{money(paycheck.salary)}</strong>
        </div>
      </div>
      <div className="paycheck-lines">
        {paycheck.lines.map((line) => (
          <div className="preview-row" key={line.bucket_key}>
            <span>{BUCKET_NAMES[line.bucket_key] || line.bucket_key}</span>
            <strong>{moneyExact(line.amount)}</strong>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function Dashboard({ balances, totals, lastPaycheck, settings, transactions }) {
  const targets = {
    truck_repair: Number(settings.repair_target),
    future_truck: Number(settings.future_truck_target),
  }
  const recent = transactions.slice(0, 8)

  return (
    <div className="view">
      {lastPaycheck ? (
        <>
          <h2 className="view-title">Latest</h2>
          <LastPaycheck paycheck={lastPaycheck} />
        </>
      ) : (
        <>
          <h2 className="view-title">Get started</h2>
          <p className="empty">
            Tap <strong>+</strong> and enter what you were paid. You will see the split before
            anything is saved.
          </p>
        </>
      )}

      <h2 className="view-title">Running totals</h2>
      <div className="stat-grid">
        <Stat label="Taken in" value={money(totals.income)} tone="up" />
        <Stat label="Spent" value={money(totals.spend)} tone="down" />
        <Stat label="Paid to you" value={money(totals.salary)} />
        <Stat label="Held in buckets" value={money(totals.held)} />
      </div>

      <h2 className="view-title">Buckets</h2>
      <div className="bucket-list">
        {BUCKETS.map((b) => (
          <BucketRow key={b.key} bucket={b} balance={balances[b.key] || 0} target={targets[b.key]} />
        ))}
      </div>

      {recent.length > 0 && (
        <>
          <h2 className="view-title">Recent activity</h2>
          <div className="tx-list">
            {recent.map((tx) => (
              <div className="tx" key={tx.id}>
                <div className="tx-main">
                  <div className="tx-title">{tx.category || tx.payee || tx.bucket_key}</div>
                  <div className="tx-meta">
                    {prettyDate(tx.date)} · {BUCKET_NAMES[tx.bucket_key] || tx.bucket_key}
                  </div>
                </div>
                <div className={`tx-amount ${Number(tx.amount) < 0 ? 'neg' : 'pos'}`}>
                  {money(tx.amount)}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
