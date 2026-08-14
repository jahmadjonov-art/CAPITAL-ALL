// ---------------------------------------------------------------------------
//  Your Supabase connection details. Fill these two in once (see README.md).
//
//  Yes, these get committed and shipped inside a public web page. That is how
//  Supabase is designed to work. The "anon" key is a *public* client key — it
//  identifies the project, it does not grant access to anything. What actually
//  guards your numbers is the row-level security in supabase/schema.sql, which
//  makes the database return only rows belonging to the logged-in user.
//
//  The one key you must NEVER paste here is the "service_role" key. That one
//  does bypass row-level security. It stays in the Supabase dashboard.
// ---------------------------------------------------------------------------

const PLACEHOLDER_URL = 'PASTE_YOUR_SUPABASE_PROJECT_URL_HERE'
const PLACEHOLDER_KEY = 'PASTE_YOUR_SUPABASE_ANON_KEY_HERE'

export const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || PLACEHOLDER_URL
export const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || PLACEHOLDER_KEY

export const isConfigured =
  SUPABASE_URL !== PLACEHOLDER_URL &&
  SUPABASE_ANON_KEY !== PLACEHOLDER_KEY &&
  SUPABASE_URL.startsWith('http')
