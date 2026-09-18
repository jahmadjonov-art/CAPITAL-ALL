# Capital Allocation Manager

A budgeting app for a trucking business, reachable from any phone or laptop, running on
$0/month permanently.

Log an income event and it splits automatically across taxes, the repair reserve, your
capital fund and your own salary, following rules you control.

## How this is free, and why there is no server

There isn't one. The app is a folder of static files on GitHub Pages, and it talks
straight to a hosted Postgres database at Supabase. Nothing has to stay running, so
nothing costs anything and nothing goes to sleep between uses.

That is also why the previous version couldn't be deployed. It was an Express server
writing to a SQLite file on disk, and free hosting gives you a disk that gets wiped on
every redeploy — the budget would have reset to zero each time. The allocation logic was
never server-shaped to begin with: it's arithmetic on a handful of numbers, so it now runs
in the browser, where you can watch a split before committing it.

```
frontend/         the entire app
  src/lib/        allocation waterfall — the only real logic here
  src/store.js    all database reads and writes
supabase/         schema.sql — run this once in the Supabase dashboard
.github/          builds and publishes on every push to main
```

## One-time setup

### 1. Create the database

1. Sign up at [supabase.com](https://supabase.com) and create a project. The free tier is
   what you want; no card required.
2. In the left sidebar open **SQL Editor**, paste in the entire contents of
   [`supabase/schema.sql`](supabase/schema.sql), and press Run.
3. Open **Project Settings → API** and copy two values: the **Project URL** and the
   **anon public** key.

### 2. Point the app at it

Paste those two values into [`frontend/src/config.js`](frontend/src/config.js), replacing
the placeholders.

These get committed to a public repo, which is correct and safe. The anon key is a public
client key — it names the project, it doesn't unlock it. What guards your numbers is the
row-level security in `schema.sql`: the database itself will only return rows belonging to
the logged-in user. **Never** put the `service_role` key here; that one does bypass those
rules and belongs only in the Supabase dashboard.

### 3. Turn on GitHub Pages

In the repo: **Settings → Pages → Source → GitHub Actions**. Then push:

```bash
git push
```

The workflow builds and publishes in about a minute. Your app lands at
**https://jahmadjonov-art.github.io/CAPITAL-ALL/**

### 4. Create your login

Open the site and click *Create an account*. By default Supabase emails you a confirmation
link. If you'd rather skip that for a single-user app, turn off **Confirm email** under
**Authentication → Providers → Email** in the Supabase dashboard before signing up.

### 5. Put it on your phone

Open the URL in Safari or Chrome on your phone and choose *Add to Home Screen*. It installs
as a real app with its own icon, opens without browser chrome, and keeps working in a dead
zone (entering new transactions needs a connection, since that writes to the database).

## Working on it locally

```bash
npm run install-all
npm run dev            # http://localhost:5173
```

Local dev talks to the same Supabase project as the live site, so you'll see the same data.
If you'd rather not hardcode keys during development, drop them in `frontend/.env.local`
instead as `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`; those take precedence over
`config.js` and are gitignored.

## How the allocation works

Each income event runs through a waterfall, in priority order:

1. **Taxes** come off the top at your tax percentage — that money was never yours.
2. **Repair reserve** is topped up by its percentage, but only until it reaches its target.
   Once the reserve is full, that money is better off as capital.
3. **Capital fund** takes its guaranteed floor percentage.
4. **You** get paid whatever is left, up to your salary cap.
5. **Surplus** above the cap falls back into capital.

Every step draws from a running remainder that stops at zero, so the lines always sum to
exactly what came in. Aggressive settings (say 60% tax plus a 60% capital floor) can starve
the later buckets, but can never allocate more money than you earned. Edit the rules under
**Rules**, where a worked example shows what a $10,000 load would do before you save.

Bucket balances are never stored — they're summed from the ledger on read, so a balance can
never quietly disagree with the transactions behind it. Deleting one line of a split
removes the whole split, for the same reason.

## Notes

- `npm audit` reports a moderate advisory in esbuild, reachable only through Vite's local
  dev server. It does not affect the static files that get deployed.
- The old Express + SQLite backend is preserved in git history at commit `c0b4b71`.
