# Handoff

Durable knowledge for whoever works here next. Facts that took effort to
establish, and mistakes worth not repeating.

Add to this when you learn something a fresh session would otherwise have to
rediscover. Delete anything that stops being true — a stale warning here is
worse than none, because it will be trusted.

---

## Orientation

**This repository is a trading research programme.** Read
[`MISSION.md`](../MISSION.md) first — the goal is making money in futures,
equities, options and prediction markets, and the method is an accumulating
research record that future sessions build on. `research/` is that record.

It used to hold a different app entirely; that one now sits in `legacy/` and is
unrelated to the current work.

**`legacy/` is a real, deployed application — not dead code.** It is the Capital
Allocation Manager, a budgeting PWA that splits trucking income across tax,
repair, capital and salary buckets. Do not modify it, refactor it, or build on
top of it unless explicitly asked. It was moved with `git mv`, so
`git log --follow` traces any file's full history through the move.

**Read `SCORECARD.md` before planning anything.** Its Standing Directives
section is binding — those lines were earned from the owner's ratings of earlier
phases. `./scorecard/summary.sh` gives the short version.

---

## Things that will bite you

### This environment can place real trades with real money

The most important fact in this file.

A Robinhood connection is attached (`mcp__Robinhood__*`). Alongside market data
it exposes `place_equity_order`, `place_option_order` and `place_crypto_order`,
whose own documentation begins *"Place a real equity order with real money."*
There is also `exercise_option` and the various `cancel_*` tools. This is not a
sandbox and there is no paper-trading mode in that toolset.

**The account is deliberate.** The owner created and connected it on purpose,
for exactly this environment — it is not a stray credential anyone forgot about.

### The account, measured 2026-09-12

Verified by calling `get_accounts` and `get_portfolio`. Re-check rather than
trusting these numbers indefinitely.

Four accounts exist on this login. **Only one is reachable by an agent:**

| | |
|---|---|
| Account | `792646622`, nicknamed **"Agentic"** |
| Reachable by agents | **Yes** — the only one. The owner's default account returns `agentic_allowed: false` and is beyond reach, by design |
| Type | **Cash account**, not margin |
| Options approval | **`option_level_2`** — long calls/puts, covered calls, cash-secured puts. **No spreads** (that needs level 3) |
| Funded | **$100.00**, all cash, $100.00 buying power |
| Positions | None. No order has ever been placed |

**Pass `792646622` as `account_number`.** Calls against the other three are
rejected, which is the correct behaviour and not a bug to work around.

### What $100 in a cash account at level 2 actually permits

This is the binding constraint on every strategy, and it rules more out than it
allows. An option contract covers 100 shares, so:

- **Cash-secured puts** need `strike × 100` in collateral. At $100 that caps the
  strike at **$1.00**. There is no worthwhile underlying there.
- **Covered calls** need 100 shares first. At $100 that caps the share price at
  **$1.00**. Same problem.
- **Long calls or puts** need `premium × 100` ≤ $100, so a premium under **$1.00**
  per share. Possible, but it buys one contract — a single binary bet where the
  bid-ask spread is the largest cost in the trade.

**So options are, in practice, closed to this account until it is much larger.**
That is arithmetic from the standard 100-share multiplier, not an opinion.

What remains open: **equities including fractional shares** (dollar-denominated
market orders work — a $50 SPY review returned no broker alerts), and **crypto**,
which has its own $100 buying power and trades around the clock.

One more constraint on frequency: a **cash account settles T+1**, so capital
committed to a trade is unavailable until settlement. Buying again with
unsettled proceeds causes a good-faith violation. Plan for roughly one round
trip per dollar per day — strategies needing faster turnover are not available
here regardless of whether they work.

**The rule for every agent working here: never place, modify, cancel or
exercise anything without explicit human approval for that specific trade, at
the time of the trade.** Not implied approval from a general instruction to
"trade profitably", not approval carried over from an earlier trade, not
approval inferred from an approved strategy. A standing instruction to pursue
profit is authorisation to research, never authorisation to transmit an order.

Read-only market data tools — quotes, historicals, chains, fundamentals,
filings, positions, orders — are fine to use freely. That is where essentially
all the work lives.

The broker enforces its own rails on top of this: orders require an
`agentic_allowed=true` account, options require level 2 or 3, and the tools
expect `review_equity_order` / `review_option_order` / `preview_crypto_order`
first with the result shown to the user for confirmation. **Treat those as a
backstop, not as the control.** They constrain the mechanism; they do not decide
whether a trade should exist. Use the review tools freely — they simulate
without placing, and are genuinely useful for pricing a hypothetical.

If a future session is ever given standing authority to execute autonomously,
that authority belongs in this file in the owner's own words, with its limits
written down — size, instruments, maximum loss. **Until such a line exists here,
it does not exist.**

### Never compute a spread from `get_equity_quotes` after hours

`bid_price` / `ask_price` were **487× wrong** on SPY at 20:00 ET on a Friday —
and the symbols that looked tight were one-sided quotes with a phantom side, so
you cannot eyeball which to trust. Use `review_equity_order`'s
`market_data_disclosure` string, which was verified accurate to the cent. Full
detail and the pending regular-hours test are in `research/beliefs.md` as
**B-002**. Also: `last_trade_price` is the 16:00 close while bid/ask are 20:00 —
**they cannot be paired.**

### Verified: the open internet is reachable, and it fills the Robinhood gaps

Tested 2026-09-12. `WebSearch` and `WebFetch` both work, and plain `curl` from
Bash reaches arbitrary hosts — the agent proxy reports `selective: false` and
covers every host, so no allowlist is in the way. **An agent here is not limited
to the Robinhood feed and should not act as if it were.**

Confirmed working, free, no API key, no account:

| Source | Endpoint | Gives you |
|---|---|---|
| **Yahoo Finance** | `https://query1.finance.yahoo.com/v8/finance/chart/<SYM>?range=1mo&interval=1d` | OHLCV for equities, ETFs, indexes **and futures** |
| **Kalshi** | `https://api.elections.kalshi.com/trade-api/v2/markets?status=open` | Prediction markets — tickers, order book, volume. Public data needs no auth (re-confirmed 2026-09-12). |
| **CoinGecko** | `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd` | Crypto spot |

**Yahoo covers futures**, which Robinhood does not: `GC=F` returned COMEX gold
(`instrumentType: FUTURE`) with real daily bars. `ES=F`, `CL=F`, `NG=F` and the
rest follow the same `=F` convention. This is the answer to "where does futures
data come from" — verified, not assumed.

Two that did **not** work, so nobody burns time rediscovering it:

- **SEC EDGAR** (`www.sec.gov/files/company_tickers.json`) returned **403**. SEC
  policy requires a declared User-Agent naming a real contact, in the form
  `Company Name email@domain.com`. Likely fixable; not yet retried.
- **Stooq** returned 200 but served an HTML challenge page rather than CSV — a
  bot block, not data. Parse defensively or use Yahoo instead.

Unverified and worth checking before relying on: Yahoo's endpoint is
undocumented and unofficial, so it can rate-limit or change shape without
notice. Treat a sudden parse failure as expected maintenance, not a crisis, and
write a `4-walls.md` entry if it stops working for good.

### The Robinhood feed is a retail feed, not a research dataset

`get_equity_historicals` is explicitly documented for backtesting and is
split-adjusted by default, which is the right default. But plan around what a
brokerage feed does not give you:

- **No delisted symbols.** Any universe assembled from currently-tradable
  tickers is survivorship-biased, and that bias reliably inflates backtest
  returns. It is the single easiest way to produce an impressive, worthless
  result here.
- **No futures.** The mission names futures explicitly and Robinhood does not
  cover them. **Solved** — use Yahoo Finance (`GC=F` etc.), verified above.
- **Limited intraday history**, and the call is rejected outright if a requested
  range and interval would exceed the bar cap. Narrow the range or coarsen the
  interval.
- `interpolated: true` on a bar means it was **synthesised to fill a gap** and
  carries no information. Filter these out before computing anything, or they
  will quietly flatten your volatility estimates.


### The Supabase database in `legacy/` is live, shared, and holds real money data

`legacy/frontend/src/config.js` points at a real Supabase project, and the
legacy README states that local development talks to **the same database as the
production site**. There is no separate dev instance.

So running the legacy app locally and clicking around is not a dry run — adding
or deleting a transaction there mutates the owner's actual business records.
Treat `legacy/supabase/schema.sql` the same way: it is the shape of a live
database, not a scratch file.

The committed anon key is fine and is meant to be public; row-level security is
what protects the rows. The `service_role` key must never enter this repo.

### `main` is untouched and is what deploys

The live site builds from `main` on every push. Work happens on a
`claude/...` branch. Nothing done on that branch affects production until it is
merged, which is the only reason the archiving work was safe to do at all.

One consequence to carry forward: the deploy workflow moved to
`legacy/.github/workflows/deploy.yml`, and GitHub only reads workflows from
`.github/workflows/` **at the repository root**. It is therefore inert on this
branch, by design. If this branch ever merges to `main`, the legacy app stops
auto-deploying. That was a deliberate choice, not an oversight — but confirm it
is still what the owner wants before merging.

**There are TWO deploy paths, and the note above only knew about one.** Found
2026-09-17 when PR #1 came back with a red check:

1. **GitHub Pages, via `.github/workflows/deploy.yml` — this is the live one.**
   `https://jahmadjonov-art.github.io/CAPITAL-ALL/` returns the trucking app
   right now, title "Capital Allocation". Moving the workflow makes it inert on
   merge: Pages keeps serving the last build, so **the site does not go down, it
   freezes** — no further change ever deploys.
2. **Vercel, project `capital-all-backend` under team `capall`.** A GitHub App
   watching the repository directly, so moving `.github/` did **not** disable it.
   It builds from the repository root, cannot find `package.json` there any more,
   and now fails on every push — that is the red check on PR #1, and it is caused
   by our diff.

Note that `legacy/frontend/vite.config.js` sets `base = '/CAPITAL-ALL/'` for
Pages, so a Vercel build of this app would serve broken asset paths anyway
unless `BASE_PATH=/` were set. The Vercel integration looks like an experiment
rather than the real deployment, but **that is inference, not something the
owner has confirmed** — ask before assuming it can be disconnected.

**Resolved 2026-09-17, with the owner.** He wants the trucking app to keep
deploying, so `.github/workflows/deploy-legacy.yml` now sits at the repository
root: the original workflow, unchanged except for its paths, watching only
`legacy/frontend/**` so research pushes do not trigger it. **Do not delete it
while tidying** — without it the app freezes on merge.

Verified rather than assumed: `npm ci && BASE_PATH=/CAPITAL-ALL/ npm run build`
in `legacy/frontend` succeeds, and the asset hashes it produces
(`index-ClyjfRJt.js`, `index-DDWGn6xj.css`) are **identical to the ones the live
site is serving right now**. The workflow reproduces the current deployment
exactly.

On Vercel he said he does not believe he uses it. Disconnecting it lives in the
Vercel dashboard and is his action, not ours; until he does, PR #1 carries a red
Vercel check that does not correspond to anything actually serving. **Do not
"fix" that check by moving the app back to the repository root.**

### Git rename detection is pairing-based, and a new file at the old path breaks it

Encountered directly while archiving. All 29 files were moved with `git mv` and
`git status` cleanly reported 29 renames. Then a new `README.md` was written at
the repository root — and git immediately re-paired things, reporting
`M README.md` plus `A legacy/README.md` instead of the rename it had shown a
moment earlier.

Nothing was actually wrong; the archived file was byte-identical. But the status
output alone could support either conclusion, and the whole task had been framed
as *do not lose anything*.

**The lesson: do not read `git status` letters as proof of what happened to file
contents.** Renames are inferred at display time from similarity, not recorded.
When it matters, verify against the old commit directly:

```bash
git show HEAD:path/to/file | diff - new/path/to/file
```

That was done for all 29 files before committing. Do the same for any move that
would be expensive to get wrong.

---

## Environment

An ephemeral cloud container, reclaimed after the session ends — **anything not
committed and pushed is gone.** Node 22, Python 3.11, Bash 5.2 are available.
No `gh` CLI; GitHub work goes through the `mcp__github__*` tools.

---

## Working style that has landed well so far

Not yet confirmed by a score — treat as provisional until `SCORECARD.md` has
entries backing it.

- **Look before touching.** The owner's first instruction was to inventory the
  repository specifically so nothing got deleted by accident. Surveying first
  and reporting what is there has been welcome every time.
- **Name the risk without being asked.** The live-database warning and the
  workflow-path consequence were both volunteered, and neither was challenged.
- **Prefer reversible moves, and say how to reverse them.** Archiving instead of
  deleting, with the undo command written into the README, is the shape of thing
  that has gone over well.
- **Ask when an ambiguity is structural.** One clarifying question about how to
  archive cost a round trip and prevented building the wrong layout. See
  `2-judgment-calls.md` for when that trade is worth making.

---

## How the owner starts a session

He is not a programmer and asked for one simple thing to press. Three slash
commands exist in `.claude/commands/`:

- **`/research`** — boots an autonomous session: read the records, pick one
  question, work it, write down what happened, commit and push, report back in
  plain English. This is the main one.
- **`/status`** — a plain-English summary of where everything stands.
- **`/score N`** — records his rating of recent work into `SCORECARD.md`.

If you change how the research loop works, update `.claude/commands/research.md`
to match. That file, not this one, is what actually runs when he presses the
button.

**Write for him accordingly.** Reports at the end of a session should carry no
jargon, no unexplained statistics and no walls of code. If a number matters, say
what it means.

---

## The office dashboard

The owner's view of the operation is a floor plan, not the markdown:
**https://claude.ai/code/artifact/7b709ccd-35aa-4f97-a096-26026bf8573b**

`dashboard/build.py` reads the repository and writes `dashboard/office.html`.
Every figure on it — desk count, experiments, beliefs, scores, sandbox plots — is
parsed from the markdown at build time. Nothing is stored twice, so the page can
never drift from the record.

- **Never hand-edit `office.html`.** It is generated. Edit the source and rebuild.
- **Republish to the URL above** by passing it as `url` to the `Artifact` tool,
  or he loses his bookmark to a second copy.
- Desks are generated from `.claude/agents/*.md`, so adding a specialist adds a
  desk with no dashboard change. Plots come from `sandbox/*.md` the same way.
- Unknown figures render as "not yet known", never as zero-looking placeholders.
  Keep it that way: a dashboard that invents a number is worse than no dashboard.

---

## Kalshi, in operational detail

Established 2026-09-12. Economics are in `B-003`; this is the mechanics.

- **Read the whole documentation in one fetch:** `https://docs.kalshi.com/llms-full.txt`
  is a single ~550KB markdown dump. Far easier than the JS-rendered site.
- **Public endpoints need no auth** — markets, orderbook, trades, events, series,
  exchange status. `/portfolio/*` returns 401 without credentials.
- **A demo environment exists:** `https://demo-api.kalshi.co/trade-api/v2`. This
  is how to test order behaviour without money, and it is the cheap way to
  settle the open maker-fee question in `B-003`.
- **Auth is RSA-PSS**, three headers, key self-generated in the web UI. **Sign
  the path without query parameters** — documented gotcha that will waste an
  afternoon.
- **Rate limits apply to authenticated requests only.** Basic tier is 20 reads
  and 10 writes per second. A 429 carries **no `Retry-After` header**, so back
  off on your own schedule.
- **Contracts are fractional** down to 0.01, and not every market is on a 1-cent
  grid — eleven price structures exist, with ticks down to $0.0001. Read
  `price_ranges` per market rather than assuming. Every liquid market sampled
  was still 1-cent.

### Two traps

**API keys carry a location attestation that expires.** `GET /api_keys` returns
`api_key_region_expiration_ts`; once it passes, the key silently stops working
for Sports, Elections and Entertainment markets. An automated system will just
stop trading those categories without an obvious error.

**The legal position is unsettled and the circuits split in 2026.** The Third
Circuit ruled for Kalshi in April; the **Ninth ruled against in August**,
holding the Commodity Exchange Act does not preempt state gaming law for
sports-related contracts. Massachusetts and Washington have moved against sports
and politics contracts. **Sports markets are both the most liquid on the venue
and the most legally exposed** — a strategy built on them risks the category
disappearing mid-experiment. Economic, weather and financial-data markets look
more durable.

---

## Scheduled runs

A Routine fires a **fresh research session every weekday at 15:10 UTC**
(11:10 ET in summer, 10:10 ET in winter — chosen so it stays inside US market
hours through the daylight-saving change). Trigger id
`trig_01CXe8Me3wzNA7MG7w2bMEQL`. First run: Monday 2026-09-14.

**These fired sessions have no MCP connectors.** The trigger was created from
inside a session that could not pass its connector grants through, so a
scheduled run gets **no `mcp__Robinhood__*` and no `mcp__github__*` tools.** It
can still reach Yahoo, Kalshi and CoinGecko over `curl`, plus `WebSearch` and
`WebFetch` — which covers most research — but it **cannot read the brokerage
account or quote equities through the broker.**

Two consequences:

- A scheduled session should pick work that does not need broker data. Kalshi,
  futures via Yahoo, crypto, methodology and literature work are all reachable.
- **The regular-hours quote test in `B-002` cannot be run by a scheduled
  session** — it needs `get_equity_quotes` and `review_equity_order` side by
  side. That one has to be run from an interactive session with the connectors
  attached.

The fix, if scheduled runs need broker access: the owner recreates or edits the
Routine from the Routines UI on claude.ai, where his connectors can be attached
to it. Worth doing before relying on the schedule for anything broker-shaped.

**The same edit fixes something worse.** Read on 2026-09-16, the Routine
"Capital-All — weekday research run" carries `sources: []` **and**
`mcp_connections: []` — no repository attached, not just no connectors. That is
the leading explanation for why two scheduled runs have now done their work,
committed locally, and failed to push (`thoughts/4-walls.md`, 2026-09-14). An
interactive session has the repository attached and pushes fine; a fired one
with an empty `sources` list appears not to.

So the Routine needs **two** things attached in one visit: the `capital-all`
repository, and the connectors. `update_trigger` reaches neither — it can change
the name, schedule, enabled state, model and prompt only. This is the owner's
click, and nothing an agent can do.

## Options access: what it would actually take

The account is **cash** with **`option_level_2`**. Spreads are level 3, and
level 3 **additionally requires a margin or limited-margin account** — so this
is two steps, not one:

1. Convert the account from cash to margin or limited margin
   (`get_limited_margin_upgrade_info` returns the link).
2. *Then* apply for level 3 (`get_option_level_upgrade_info`, or
   `https://applink.robinhood.com/upgrade_options?account_number=792646622`).

Both require the owner to complete an application and be approved; no agent can
do either. **And note that neither changes `B-001`** — at $100, the 100-share
contract multiplier is what closes options, not the approval level. Spreads
would reduce the collateral needed, but a $100 account still cannot carry a
meaningful position in anything but sub-$1 underlyings.

## Kalshi's Bitcoin contracts — verified 2026-09-12

`KXBTCD` ("Bitcoin price Above/below") is **`fee_type: quadratic`,
`fee_multiplier: 1`** — the fee-free-maker type, confirmed directly rather than
inferred from the series survey. Contracts are short-dated and settle through
the day (the 2026-09-12 08:00 batch closed at 12:00).

This is the pocket where the fee-free structure and real volume may overlap, and
it maps onto the owner's own interest in short-horizon crypto price contracts.
**Nobody has measured its actual order books yet** — the `/markets` listing
returns null bids and asks at weekends, so use the per-market
`/markets/{ticker}/orderbook` endpoint during active hours.

---

## Kalshi's API renamed its fields, and the old names fail SILENTLY

Cost three failed measurement passes on 2026-09-13 before it was spotted. The
fixed-point migration renamed most numeric fields, and **requesting an old name
returns nothing rather than an error** — so a script using them reports zero
markets, zero volume, and looks like a real finding.

| Do not use | Use |
|---|---|
| `yes_bid` / `yes_ask` | **`yes_bid_dollars`** / **`yes_ask_dollars`** |
| `volume_24h` / `volume` | **`volume_24h_fp`** / **`volume_fp`** |
| `open_interest` | **`open_interest_fp`** |
| `count` (on a trade) | **`count_fp`** |
| `orderbook` | **`orderbook_fp`**, with sides `yes_dollars` / `no_dollars` |

**Prices are now dollars, not cents** — `0.5300` is 53 cents.

Two more things that cost time:

- **`/markets?status=open` is not a list of tradable markets.** It returns
  thousands of auto-generated provisional combo markets (`KXMVECROSSCATEGORY`)
  created seconds ago with empty books. Paginating 8,000 of them yielded nothing
  tradable. **Use `/markets/trades?limit=1000` instead** — the trade tape shows
  what is genuinely active right now, and grouping its tickers by series is the
  fastest route to the live venue.
- **Order-book sides are both bids.** `yes_dollars` are bids for YES,
  `no_dollars` are bids for NO. The best YES *ask* is `1 - (best NO bid)`. There
  is no ask side to read directly.

Working recipe: tape → group tickers by series → `/series/{ticker}` for
`fee_type` and `fee_multiplier` → `/markets/{ticker}/orderbook` for the touch.

---

## The desk console

**https://claude.ai/code/artifact/a0aa3e0b-1fe1-420e-99b1-fc9103ac170d**

`dashboard/desk.py` builds it; `desk_template.html` is the page. It fetches spot
from three venues, measures realised volatility from one-minute bars, prices
every open Kalshi BTC contract, and shows the gap between market and model.

It is deliberately built to be un-fakeable in the way the screenshots that
inspired it were fake: no simulated fills, no P&L, no win rate, no equity curve.
Every number is fetched at build time, and the model's known defects are printed
on the page next to its own output. **Keep it that way.** A console that can show
a flattering number will eventually show one.

Crypto spot sources: **Binance.com returns 451** (geo-blocked from here).
Binance.US, Coinbase and Kraken all work; they disagreed by $33.51 on one
reading, which matters when strikes sit $100 apart.

---

## The published pages

| Page | Built by | URL |
|---|---|---|
| **Office floor plan** — the firm at a glance | `dashboard/build.py` | https://claude.ai/code/artifact/7b709ccd-35aa-4f97-a096-26026bf8573b |
| **Fair value desk** — live BTC contracts vs model | `dashboard/desk.py` | https://claude.ai/code/artifact/a0aa3e0b-1fe1-420e-99b1-fc9103ac170d |
| **Strategy library** — one tab per source | `dashboard/strategies.py` | https://claude.ai/code/artifact/d39ab618-439a-48aa-a40e-d3fe756ec966 |
| **Volatility surface** — IV smile and gamma by strike | `dashboard/surface.py` | https://claude.ai/code/artifact/f85f0329-ca21-4474-bf1a-e6449c1e9020 |
| **Tip sheet** — unusual option volume, day / week / month | `dashboard/tipsheet.py` | https://claude.ai/artifact/MqSnH99CKyT2WZuYNRu5QA |

**There is no index page linking these together.** The owner holds five separate
bookmarks and nothing on any page points at the others. Worth fixing.

Each is generated. Republish
by passing the URL above as `url` to the Artifact tool so the owner's links keep
working. **Never hand-edit the generated HTML.**

## The strategy library

`strategies/*.json` holds one extraction per source. The owner will paste more
transcripts over time; each becomes a file and a tab with no other change.

**The rule that makes it worth having:** every claim carries a `status`, starting
at `untested`, and moves only when an experiment in `research/experiments.md`
says what happened and the entry cites the id. A credible-sounding source is not
evidence. The whole point is to eventually compare several strategies on the
same footing.

Extraction is faithful, including parts that look wrong — judgement belongs in
the experiment, not the extraction. See `strategies/README.md`.

**First source in:** Freddy Siento on options flow and gamma levels. 10 claims,
all untested. Its own stated blocker is that it needs gamma-exposure-by-strike,
which nothing here currently pulls; CBOE is named as a free source with a
10-15 minute delay.

## Following a strategy on paper

`strategies/paper/<id>.jsonl` is an append-only forward record. `paper.py` opens
a signal, settles it, and reports win rate, expectancy and P&L after costs.

**The mechanism that makes it worth anything:** a signal must be committed to git
before it is settled. The tool looks up the commit that introduced the signal id
and marks anything settled without one `unverified`. Tested on a dummy signal
that showed a 100% win rate and $2,586 profit — and was correctly refused.

Without that check, a strategy log shows a strategy that works, every time, for
any strategy, because whoever writes it already knows the outcome.

Contract economics used: **NQ $5.00/tick, ES $12.50/tick**, plus one tick of
slippage each way and commission. Costs are applied on every settlement and
printed in every report, so a result can never quietly be gross of costs.

**Account size is deliberately not a filter.** A strategy is judged at the size
its source describes; whether an account can carry it is a separate question.
Do not reintroduce the $100 as a reason to narrow a study.

An options data subscription with an unlimited API pool is expected from the
owner. Each strategy file carries a `data_readiness` block naming the exact
fields it needs, so it can be wired the day access arrives. First thing to check
then: whether the feed carries intraday history or only snapshots — snapshots
allow forward testing only, history allows a backtest, and that decides how long
everything takes.

---

## Correction: we DO have gamma by strike

An earlier entry said nothing here pulls gamma exposure by strike, and that the
options-flow strategy was blocked on it. **That was wrong**, and it was wrong for
two sessions.

`mcp__Robinhood__get_option_quotes` returns, per contract:
`implied_volatility`, `delta`, **`gamma`**, `theta`, `vega`, `rho`,
`open_interest`, `volume`, plus bid/ask/mark. And `SPXW` carries **daily**
expirations, so the 0DTE chain the strategy runs on is right there.

Verified 2026-09-13 on the SPXW 2026-09-14 chain around the money:

| Strike | IV | Gamma | OI | Gamma $ per 1% |
|---|---|---|---|---|
| 7,650 | 12.75% | 0.007993 | 689 | $323M |
| **7,675** | 11.82% | **0.008138** | 1,878 | **$896M** |
| 7,700 | 11.40% | 0.005745 | 1,626 | $548M |

**$2.15bn of gamma across eight strikes**, with a clear wall at 7,675 — computed
rather than asserted. The implied-volatility smile is real too: 16.8% on the
downside wing, a floor of 11.4% near the money, 15.2% on the upside.

### How to capture and render

**MCP tools only work from a lead session; a plain script cannot call them.** So
the two steps are deliberately separate:

1. A session pulls the chain and writes `data/snapshots/<chain>-<time>.json`.
2. `python3 dashboard/surface.py` renders the newest snapshot to
   `dashboard/surface.html`.

Published: **https://claude.ai/code/artifact/f85f0329-ca21-4474-bf1a-e6449c1e9020**

### Traps found while doing it

- **`get_option_instruments` paginates and starts at the lowest strike.** SPXW
  runs from 3,000, so the first page is nowhere near the money. The cursor is
  base64 of `p=<strike>` — craft one (`base64("p=7550.0000")`) to jump straight
  to the strikes that matter instead of paging through hundreds.
- **Greeks are null on deep in-the-money strikes.** Not an error; those contracts
  have no real two-sided market. Filter rather than treating it as failure.
- **SPX spot is not in the option payload.** It was derived from the delta-0.5
  crossing between two strikes. Fetch the index level directly when it matters.
- **Two SPX chains exist:** `SPXW` (weeklies and dailies, PM settled) and `SPX`
  (monthlies, `settle_on_open: true`, AM settled). The strategy wants SPXW.

### What is still genuinely missing

The source relies on a **90-day open-interest history**. The broker returns
current open interest only. That is the real remaining gap and the one an
options subscription would close.

---

## Dealer gamma: the sign is the whole thing

The owner showed a gamma tool another Claude built for him two months ago, and it
was ahead of ours on the concept that matters most. Recorded here so nobody
rebuilds the weaker version.

**Gamma has a sign, and the sign decides the regime.** Summing gamma as a
positive quantity — which our first surface page did — throws away the finding.

```
net dealer gamma = call gamma exposure  −  put gamma exposure
```

The convention assumes dealers are **long calls** (customers sell covered calls
to them) and **short puts** (customers buy puts as portfolio hedges).

| Regime | Dealer behaviour | What it means for a trade |
|---|---|---|
| **Positive gamma** | sells rallies, buys dips | moves are dampened, mean-reverting tape, fading the edges works |
| **Negative gamma** | buys rallies, sells dips | moves are **amplified**, trend continues, **do not fade** |

Negative gamma is the snowball the options-flow transcript describes. A strategy
of fading a wall is a positive-gamma strategy and gets run over in a negative-gamma
tape — so **read the regime before applying any level rule.**

**The gamma flip** is the strike where cumulative net gamma crosses zero: the
boundary between the two regimes, and the single most actionable number on the
page. Knowing which side of it spot sits on before the open is worth more than
any level.

**Other concepts from that tool worth carrying:**

- **Call wall** = max call gamma (resistance). **Put wall** = max put gamma
  (support). **When they are the same strike it is a pin, not a barrier** —
  expect price drawn to it and chopping across it rather than reversing cleanly.
- **Max open interest** is a separate "pin candidate" from the gamma walls.
- **Cash strikes are not futures points.** That tool converts SPX cash to ES with
  a ×1.00033 basis. Ours does not convert at all yet — anything quoted in ES or
  NQ terms must be basis-adjusted or it is simply the wrong level.
- It surfaces **feed health** ("2 feeds degraded") and **session state**
  ("weekend — closed"). A dashboard that cannot say its data is stale will
  eventually mislead someone.

### What ours now computes, and what it does not

`dashboard/surface.py` does net dealer gamma, the regime, both walls, the pin
warning, and a flip estimate. On the 2026-09-11 SPXW snapshot it read
**−$54.2M net, NEGATIVE**, with call wall and put wall both at **7,675**.

**The sign agreed with the reference tool; the magnitude is not comparable** —
six strikes against a full chain, and that tool read −$14.73bn. Our flip landed
at the edge of the sampled range, which means it was not determined. Sample the
whole chain before trusting either number.

---

## The tip sheet, and the two ways a screen lies to you

`scanner/tipsheet.py` pulls full chains for 70 liquid names from CBOE and ranks
unusual option volume; `dashboard/tipsheet.py` renders it as day / week / month.
Both run unauthenticated from a plain script, so a scheduled run can do it.

**What it measures:** volume against open interest. Open interest is published
once after the close and does not move intraday — that is what makes the ratio
mean something, and it also means a pre-open run describes the *previous*
session. Say which it is when reporting.

**What it does not measure:** unusual versus this ticker's own normal day. That
needs a history of daily option volume, and nothing records one yet
(`sandbox/data-collection.md`). Names that trade huge volume every day will keep
appearing. That is turnover, not news.

**Two filters that turned out to be measuring themselves.** Both are worth
knowing before adding a third:

1. **A ratio against a floor.** Ranking on volume ÷ open interest with a floor
   of 50 on the denominator put contracts with an open interest of 0–21 at the
   top. The headline "816×" was volume divided by the floor, not by anything
   observed. Median open interest in the top 40 was 24. Fix: contracts with real
   open interest (`build`, OI ≥ 100, ranked by ratio) are now separated from
   contracts with almost none (`fresh`, OI ≤ 100, ranked by notional), and the
   ratio is simply not computed in between.
2. **A flag that fires on everything.** The replacement called a ticker
   "mechanical" when three strikes more than 8% in the money shared an expiry.
   It fired on 11 of the top 15 names, which carries no information. Fix: CBOE
   ships greeks per contract, so ask the property directly — **|delta| ≥ 0.98
   with vega ≤ 0.01 means the contract has no optionality left and is a stock
   substitute.** Volume there is financing, a roll, a box or an assignment being
   managed. Measured across the universe, 88% of contracts with delta ≥ 0.98
   also had vega ≤ 0.005, so this tests one real thing rather than two loose
   ones.

That second class of volume is not small. On 2026-09-14 it was **88% of IWM's
entire standout option notional ($1.39B)** and would have put IWM top of the
sheet on plumbing alone. It is excluded from every ranking and reported in its
own table, never silently dropped.

**Iterate the heuristic against a cache, not against CBOE.** `--cache DIR` saves
and reuses the raw chains, so tuning a threshold costs one fetch rather than 70
per attempt.

### Two ways CBOE hands you bad data with a 200

Both found on the second morning the scanner ran, both silent, both fixed in
`scanner/tipsheet.py`. Assume a third exists.

**It rate-limits, and the failure is invisible.** Eight parallel workers got a
clean 70 of 70 one morning and `429` on 23 of 70 the next. The run still
"succeeded" — it just ranked whatever got through, with the missing third
listed in small type at the bottom of the page. Now: four workers, exponential
backoff with jitter, four attempts, and the script **refuses to write** below
90% coverage rather than publishing a partial ranking. `--force` overrides it
deliberately. A full scan takes about 12 seconds.

**It serves dead symbols forever.** A renamed or delisted ticker keeps returning
a complete, well-formed chain — the last file CBOE ever wrote for it — with a
200 and no warning. `SQ` was returning a full chain stamped **2025-01-21** and
being ranked on it; `PARA` one from 2025-08-10. Both had been renamed (Block is
now `XYZ`, Paramount Skydance is `PSKY`) and the universe has been corrected.
The defence: the response's **top-level `timestamp` field** is the feed's own
age, and it is thrown away if you take `["data"]` and nothing else. `scan()` now
rejects any chain more than 4 days old (Friday's close read on Monday is 3), and
writes the range to `feed_latest` / `feed_earliest`, which the page displays —
"when we asked" and "what the numbers describe" are different things, and only
the second one matters when the sheet runs before the open.

**Nothing checks the universe for renames automatically.** A dead ticker now
drops out with a `stale feed` error instead of poisoning the ranking, but it
still has to be noticed and replaced by hand.

---

## Massive (formerly Polygon.io) — the options data subscription

The owner supplied a key on 2026-09-16. **It is not in this repository and must
never be**, `.gitignore` carries patterns for the obvious filenames, and
`scanner/massive.py` reads it from `MASSIVE_API_KEY` in the environment. For a
scheduled run, it goes in the Routine's environment variables — the same
settings page that needs the repository and connectors attached.

The host is still `api.polygon.io`; only the company name and the pricing links
changed.

**Entitlements, measured rather than read off a pricing page:**

| | |
|---|---|
| Contract reference, full chain snapshot (strike, expiry, open interest, day volume) | yes |
| **Daily bars for stocks and for individual option contracts, ~2 years back** | **yes** |
| Tick-level trades | no |
| Real-time quotes | no |
| **Greeks** — the snapshot returns `greeks: {}` and a null IV | **no** |

**It complements CBOE, it does not replace it.** CBOE gives today's chain *with*
greeks, free and unauthenticated, and no history whatsoever. Massive gives the
history. The tip sheet's zero-optionality filter is built on delta and vega, so
it stays on CBOE.

**What it unlocks.** `scanner/tipsheet.py` says in its own docstring that it
cannot answer "unusual versus this ticker's own normal volume" because nothing
records a volume history. Two years of daily bars per contract means that
history can be **backfilled rather than waited for** — which also removes the
dependency on a scheduled collector working, and that collector is the thing
currently broken. `sandbox/data-collection.md` should be re-read in this light.

### The trap this source sets

**A rate limit and a missing entitlement look almost identical, and I confused
them within ten minutes of getting the key.** An early probe reported `12/12
requests succeeded, no throttling`, and a history check reported
`NOT_AUTHORIZED` for 2024 — so the first conclusion was "unlimited calls, one
year of history". Both were wrong. There *is* a per-minute cap; the twelve calls
simply had not reached it yet. And the `NOT_AUTHORIZED` was the cap too — the
same refusal arrives variously as HTTP 429, as HTTP 403, and as a **200 whose
body carries `status: ERROR`**, sometimes with a `status` field that disagrees
with its own error text.

Measured properly, with retries through the cap: about **two years** of history,
for options and stocks alike.

`massive.get()` retries through the cap and raises `NotEntitled` only for a real
plan limit, so callers cannot repeat the mistake. **Anything that queries this
API without that retry will eventually report that the plan lacks data the plan
has.**

**The cap is about four requests a minute.** Measured from real use on
2026-09-16 — the first full history backfill fetched 59 tickers in 859 seconds,
and the adaptive gap in `massive.get()` settled at its 15-second ceiling. Worth
telling the owner: he believed the plan carried an unlimited request pool, and
what is actually there is tight enough to shape the design. A 70-name history
refresh is a **~15 minute job**, which is why `scanner/history.py` caches to
disk and refetches only what has gone stale, saves incrementally as it goes, and
offers `--cached-history` so a rebuild never waits behind a backfill.
