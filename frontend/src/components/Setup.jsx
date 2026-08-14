import React from 'react'

// Shown instead of a blank white screen when src/config.js still holds the
// placeholder keys — the single most likely reason a first deploy looks broken.
export default function Setup() {
  return (
    <div className="auth-screen">
      <div className="auth-card setup">
        <h1 className="auth-logo">Almost there</h1>
        <p className="auth-sub">
          The app is running, but it does not know which Supabase project to talk to yet.
        </p>
        <ol className="setup-steps">
          <li>
            Create a free project at <code>supabase.com</code>.
          </li>
          <li>
            Open <strong>SQL Editor</strong>, paste in <code>supabase/schema.sql</code> from this
            repo, and hit Run.
          </li>
          <li>
            Open <strong>Project Settings → API</strong> and copy the <em>Project URL</em> and the{' '}
            <em>anon public</em> key.
          </li>
          <li>
            Paste both into <code>frontend/src/config.js</code>, then commit and push.
          </li>
        </ol>
        <p className="setup-note">
          Full walkthrough is in <code>README.md</code>.
        </p>
      </div>
    </div>
  )
}
