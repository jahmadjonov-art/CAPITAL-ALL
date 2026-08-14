-- ============================================================================
--  Capital Allocation Manager — database schema
--
--  ONE-TIME SETUP: open your Supabase project, click "SQL Editor" in the left
--  sidebar, paste this entire file in, and hit Run. It is safe to run more
--  than once — every statement checks whether it already did its job.
--
--  The important part is the ROW LEVEL SECURITY section at the bottom. It is
--  what makes it safe to ship the app's connection key inside a public web
--  page: the database itself refuses to hand any row to anyone except the
--  logged-in user who owns it. No server of ours sits in between.
-- ============================================================================

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------- settings --
-- Exactly one row per user: the knobs that drive the allocation waterfall.
create table if not exists public.settings (
  user_id             uuid primary key references auth.users (id) on delete cascade,
  tax_pct             numeric not null default 20,     -- % of gross income withheld for taxes
  repair_pct          numeric not null default 10,     -- % of gross income toward the repair reserve
  repair_target       numeric not null default 30000,  -- stop funding repairs once the reserve hits this
  min_capital_pct     numeric not null default 50,     -- floor % of gross income that must go to capital
  manager_salary_cap  numeric not null default 4000,   -- most you may pay yourself from one income event
  future_truck_target numeric not null default 50000,  -- savings goal for the next truck
  updated_at          timestamptz not null default now()
);

-- ----------------------------------------------------------------- buckets --
-- Names and targets only. Balances are never stored: they are summed from the
-- transaction ledger on read, so a balance can never silently drift out of
-- agreement with the transactions that produced it.
create table if not exists public.buckets (
  id      uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  key     text not null,
  name    text not null,
  target  numeric,
  sort    integer not null default 0,
  unique (user_id, key)
);

-- ------------------------------------------------------------------ trucks --
create table if not exists public.trucks (
  id             uuid primary key default gen_random_uuid(),
  user_id        uuid not null references auth.users (id) on delete cascade,
  name           text not null,
  year           integer,
  make           text,
  model          text,
  vin            text,
  mileage        integer,
  purchase_price numeric default 0,
  purchase_date  date,
  loan_balance   numeric default 0,
  created_at     timestamptz not null default now()
);

-- ------------------------------------------------------------ transactions --
-- The ledger. Sign convention: a positive amount moves money INTO bucket_key,
-- a negative amount moves it OUT. One income event writes several rows that
-- share a group_id, so the split can be shown — or undone — as a single unit.
create table if not exists public.transactions (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references auth.users (id) on delete cascade,
  date       date not null,
  amount     numeric not null,
  type       text not null check (type in ('income', 'expense', 'transfer')),
  bucket_key text not null,
  category   text,
  payee      text,
  notes      text,
  truck_id   uuid references public.trucks (id) on delete set null,
  odometer   integer,
  group_id   uuid,
  created_at timestamptz not null default now()
);

create index if not exists transactions_user_date_idx
  on public.transactions (user_id, date desc, created_at desc);
create index if not exists transactions_user_bucket_idx
  on public.transactions (user_id, bucket_key);
create index if not exists transactions_group_idx
  on public.transactions (group_id);

-- ======================================================================== --
--  ROW LEVEL SECURITY
--
--  auth.uid() is the id of whoever is holding the login session making the
--  request. Every policy below says the same thing: you may touch a row only
--  if it is your row. Without these the anon key would expose everything, so
--  do not skip this section.
-- ======================================================================== --

alter table public.settings     enable row level security;
alter table public.buckets      enable row level security;
alter table public.trucks       enable row level security;
alter table public.transactions enable row level security;

drop policy if exists "own settings"     on public.settings;
drop policy if exists "own buckets"      on public.buckets;
drop policy if exists "own trucks"       on public.trucks;
drop policy if exists "own transactions" on public.transactions;

create policy "own settings" on public.settings
  for all to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "own buckets" on public.buckets
  for all to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "own trucks" on public.trucks
  for all to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "own transactions" on public.transactions
  for all to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);
