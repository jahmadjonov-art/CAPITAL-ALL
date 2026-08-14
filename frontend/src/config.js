// ---------------------------------------------------------------------------
//  Your Supabase connection details.
//
//  Yes, these get committed and shipped inside a public web page. That is how
//  Supabase is designed to work. The publishable (anon) key is a *public*
//  client key — it identifies the project, it does not grant access to
//  anything. What actually guards your numbers is the row-level security in
//  supabase/schema.sql, which makes the database return only rows belonging to
//  the logged-in user.
//
//  The one key that must NEVER appear here is the "service_role" / "secret"
//  key. That one does bypass row-level security. It stays in the dashboard.
// ---------------------------------------------------------------------------

// Your project's API endpoint. Not the dashboard address you browse — always
// https://<project-ref>.supabase.co.
const PROJECT_URL = 'https://pqoscsslcywzuwfpzazq.supabase.co'

// Supabase → Project Settings → API → publishable / anon public key.
const ANON_KEY = 'sb_publishable_Bt0SyDnqQQp0_cen6resBg_daR94x9C'

export const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || PROJECT_URL
export const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || ANON_KEY

// Catches a half-finished setup before it turns into a blank screen: a URL
// pointing at the dashboard instead of the API endpoint, or a key that isn't
// actually a Supabase client key. Checked by shape rather than by comparing
// against a placeholder, so there is only ever one string in this file to fill
// in and no second copy to paste into by mistake.
export const isConfigured =
  /^https:\/\/[a-z0-9-]+\.supabase\.(co|in)$/.test(SUPABASE_URL) &&
  (SUPABASE_ANON_KEY.startsWith('eyJ') || SUPABASE_ANON_KEY.startsWith('sb_publishable_'))
