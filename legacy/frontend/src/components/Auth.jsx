import React, { useState } from 'react'
import { supabase } from '../supabaseClient'

// This app belongs to one account, and that account already exists, so the
// screen only signs in. Creating another is done in the Supabase dashboard
// under Authentication → Users — removing the button here is a tidier front
// door, not a lock. The lock is "Allow new users to sign up", off, in the same
// dashboard: the anon key is public by design, so anything this screen can do,
// a determined stranger can still call directly.
function explain(message) {
  const raw = String(message || '')
  if (/email not confirmed|not confirmed/i.test(raw)) {
    return 'This account still needs its email confirmed. Use the resend button below, or turn off "Confirm email" under Authentication → Sign In / Providers → Email in your Supabase dashboard.'
  }
  if (/invalid login credentials/i.test(raw)) {
    return 'That email and password combination did not match an account. Check for a typo — and note that accounts are now made in your Supabase dashboard, under Authentication → Users.'
  }
  return raw
}

export default function Auth() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const [needsConfirm, setNeedsConfirm] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    setMessage(null)
    try {
      const { error } = await supabase.auth.signInWithPassword({ email, password })
      if (error) throw error
      // A successful sign-in fires onAuthStateChange, which swaps this screen out.
    } catch (err) {
      setNeedsConfirm(/not confirmed/i.test(err.message || ''))
      setError(explain(err.message))
    } finally {
      setBusy(false)
    }
  }

  async function resendConfirmation() {
    setBusy(true)
    setError(null)
    setMessage(null)
    try {
      const { error } = await supabase.auth.resend({ type: 'signup', email })
      if (error) throw error
      setMessage('Confirmation email sent. Supabase limits these to a few per hour on the free tier.')
    } catch (err) {
      setError(explain(err.message))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-screen">
      <form className="auth-card" onSubmit={submit}>
        <h1 className="auth-logo">Capital Allocation</h1>
        <p className="auth-sub">Sign in to reach your numbers from any device.</p>

        <label className="field">
          <span>Email</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            required
          />
        </label>

        <label className="field">
          <span>Password</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            minLength={6}
            required
          />
        </label>

        {error && <p className="banner error">{error}</p>}
        {message && <p className="banner ok">{message}</p>}

        <button className="btn primary block" disabled={busy}>
          {busy ? 'Working…' : 'Sign in'}
        </button>

        {needsConfirm && (
          <button type="button" className="btn ghost block" disabled={busy || !email} onClick={resendConfirmation}>
            Resend confirmation email
          </button>
        )}
      </form>
    </div>
  )
}
