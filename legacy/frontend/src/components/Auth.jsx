import React, { useState } from 'react'
import { supabase } from '../supabaseClient'

// Supabase returns terse API strings. For the two failures that actually block
// a first sign-in, say what to do about it instead.
function explain(message) {
  const raw = String(message || '')
  if (/email not confirmed|not confirmed/i.test(raw)) {
    return 'This account still needs its email confirmed. Use the resend button below, or turn off "Confirm email" under Authentication → Sign In / Providers → Email in your Supabase dashboard.'
  }
  if (/invalid login credentials/i.test(raw)) {
    return 'That email and password combination did not match an account. If you have not made one yet, create an account below.'
  }
  return raw
}

export default function Auth() {
  const [mode, setMode] = useState('signin')
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
      if (mode === 'signin') {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) throw error
        // A successful sign-in fires onAuthStateChange, which swaps this screen out.
      } else {
        const { data, error } = await supabase.auth.signUp({ email, password })
        if (error) throw error
        // With email confirmation enabled, signUp returns a user but no session.
        if (!data.session) {
          setNeedsConfirm(true)
          setMessage('Account created, but it needs confirming before you can sign in. Check your email — including the spam folder.')
          setMode('signin')
        }
      }
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
        <p className="auth-sub">
          {mode === 'signin'
            ? 'Sign in to reach your numbers from any device.'
            : 'Create the single account this app belongs to.'}
        </p>

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
            autoComplete={mode === 'signin' ? 'current-password' : 'new-password'}
            minLength={6}
            required
          />
        </label>

        {error && <p className="banner error">{error}</p>}
        {message && <p className="banner ok">{message}</p>}

        <button className="btn primary block" disabled={busy}>
          {busy ? 'Working…' : mode === 'signin' ? 'Sign in' : 'Create account'}
        </button>

        {needsConfirm && (
          <button type="button" className="btn ghost block" disabled={busy || !email} onClick={resendConfirmation}>
            Resend confirmation email
          </button>
        )}

        <button
          type="button"
          className="btn link"
          onClick={() => {
            setMode(mode === 'signin' ? 'signup' : 'signin')
            setError(null)
            setMessage(null)
          }}
        >
          {mode === 'signin' ? 'Need an account? Create one' : 'Already have an account? Sign in'}
        </button>
      </form>
    </div>
  )
}
