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

## The three published pages

| Page | URL |
|---|---|
| **Office floor plan** — the firm at a glance | https://claude.ai/code/artifact/7b709ccd-35aa-4f97-a096-26026bf8573b |
| **Fair value desk** — live BTC contracts vs model | https://claude.ai/code/artifact/a0aa3e0b-1fe1-420e-99b1-fc9103ac170d |
| **Strategy library** — one tab per source | https://claude.ai/code/artifact/d39ab618-439a-48aa-a40e-d3fe756ec966 |

Each is generated: `dashboard/build.py`, `desk.py`, `strategies.py`. Republish
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
