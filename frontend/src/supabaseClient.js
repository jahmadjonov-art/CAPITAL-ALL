import { createClient } from '@supabase/supabase-js'
import { SUPABASE_URL, SUPABASE_ANON_KEY, isConfigured } from './config'

// When the keys are still placeholders we hand back null rather than letting
// createClient throw on a malformed URL — App.jsx shows setup instructions
// instead of a blank screen.
export const supabase = isConfigured
  ? createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
      },
    })
  : null
