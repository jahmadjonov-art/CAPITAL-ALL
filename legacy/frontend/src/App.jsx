import React, { useEffect, useState } from 'react'
import { supabase } from './supabaseClient'
import { isConfigured } from './config'
import { useStore } from './store'
import Setup from './components/Setup'
import Auth from './components/Auth'
import Dashboard from './components/Dashboard'
import Transactions from './components/Transactions'
import Trucks from './components/Trucks'
import Settings from './components/Settings'
import AddSheet from './components/AddSheet'

function Shell({ session }) {
  const store = useStore(session)
  const [view, setView] = useState('dashboard')
  const [adding, setAdding] = useState(false)

  if (store.loading) {
    return <div className="splash">Loading your numbers…</div>
  }

  return (
    <div className="app">
      <header className="topbar">
        <span className="topbar-title">Capital Allocation</span>
      </header>

      <main className="content">
        {store.error && (
          <p className="banner error">
            {store.error}
            <button className="btn link" onClick={store.refresh}>
              Retry
            </button>
          </p>
        )}

        {view === 'dashboard' && (
          <Dashboard
            balances={store.balances}
            totals={store.totals}
            lastPaycheck={store.lastPaycheck}
            settings={store.settings}
            transactions={store.transactions}
          />
        )}
        {view === 'transactions' && <Transactions store={store} />}
        {view === 'trucks' && <Trucks store={store} />}
        {view === 'settings' && <Settings store={store} session={session} />}
      </main>

      <nav className="bottom-nav">
        <button
          className={view === 'dashboard' ? 'active' : ''}
          onClick={() => setView('dashboard')}
        >
          Home
        </button>
        <button
          className={view === 'transactions' ? 'active' : ''}
          onClick={() => setView('transactions')}
        >
          Ledger
        </button>
        <button className="add" onClick={() => setAdding(true)} aria-label="Add entry">
          +
        </button>
        <button className={view === 'trucks' ? 'active' : ''} onClick={() => setView('trucks')}>
          Trucks
        </button>
        <button className={view === 'settings' ? 'active' : ''} onClick={() => setView('settings')}>
          Rules
        </button>
      </nav>

      {adding && <AddSheet store={store} onClose={() => setAdding(false)} />}
    </div>
  )
}

export default function App() {
  const [session, setSession] = useState(null)
  const [checking, setChecking] = useState(true)

  useEffect(() => {
    if (!isConfigured) {
      setChecking(false)
      return
    }
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session)
      setChecking(false)
    })
    const { data: sub } = supabase.auth.onAuthStateChange((_event, next) => setSession(next))
    return () => sub.subscription.unsubscribe()
  }, [])

  if (!isConfigured) return <Setup />
  if (checking) return <div className="splash">Checking your session…</div>
  if (!session) return <Auth />

  // Remounting on user change throws away the previous user's cached rows.
  return <Shell key={session.user.id} session={session} />
}
