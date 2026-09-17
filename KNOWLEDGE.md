# Knowledge

**The one page every session reads.** Everything else is looked up only when
this page points at it.

---

## The goal

Make money in tradable markets — futures, equities, options, prediction markets.
Full charter in [`MISSION.md`](MISSION.md).

## What we know

Claims that have earned a place here. Each is one line, carries its evidence
tier, and names the experiments behind it so the detail can be pulled on demand.

- **$100, cash, options level 2 — trading options is closed to us.** The
  100-share multiplier caps us at a $1 underlying. Reading the chain is
  not closed. — `B-001`
- **CBOE serves the whole option chain free and unauthenticated** — 28,934 SPX
  contracts per request with gamma and open interest on each, and it works from a
  script where the MCP tools do not. 0DTE net dealer gamma **−$23B (negative — do
  not fade)**. **Its open interest is end-of-day.** — `B-005`, `EXP-002`
- **Read the gamma sign before applying any level rule.** Positive = dealers
  dampen and fading works; negative = they amplify and it gets run over. A
  six-strike sample was 400× wrong — **a sampled gamma profile is not a small
  one.**
- **Kalshi is parked on one venue question.** Free resting orders exist, but
  only Kalshi-direct; we hold Robinhood (~4¢ round trip). — `B-003`, `B-004`
- **A screen must not supply the quantity it claims to measure.** Three tip-sheet
  rankings died of this: volume ÷ an open-interest *floor*; a "mechanical" flag
  firing on 11 of the top 15 names; and a per-contract volume percentile whose
  contracts had a median of **five days** of history. The test before trusting
  any ranking: *what would this look like if the effect were absent?* Same
  answer ⇒ it measures the filter. — `scanner/tipsheet.py`
- **Two option data sources; neither suffices alone.** CBOE: today's full chain
  *with greeks*, free, keyless, no history. Massive (ex-Polygon; key in
  `MASSIVE_API_KEY`, never in the repo): ~2 years of daily bars, but no greeks,
  no real-time, ~4 requests/min, and **no way to recover past option volume** —
  that must be banked daily. Its rate limit and entitlement errors look alike.
  — `scanner/massive.py`, `scanner/history.py`
- **A scheduled run cannot push, and the cause is now proven.** The git proxy
  refuses a credential for any repository not in the fired session's authorized
  set, and the Routine's set is empty — `403`, verbatim in `4-walls.md`. Fix is
  the owner's: attach the repo on the Routines page. **Until then a scheduled run
  loses everything it writes while reporting success.** The general lesson cost
  four runs: when the failure is in how work *escapes* a container, the
  diagnosis cannot travel by that same route — send it out through a channel
  that still works (here, the dashboard). — `thoughts/4-walls.md`
- **Broker quirks:** never price a spread from `get_equity_quotes` after hours
  (487× wrong on SPY); only `••••6622` is agent-reachable; **subagents and
  scheduled runs get no broker tools**; Kalshi silently returns nothing for
  pre-migration field names. `handoff.md` has the detail. — `B-002`

## What is dead

Things tried that did not work, one line each. **This section is as valuable as
the one above and cheaper to fill.** It is what stops five future sessions
independently rediscovering the same dead end.

> _Nothing yet._

## What is live right now

The question currently being worked, and by whom.

> 2026-09-17: the tip sheet is live and the push wall is solved (owner must
> attach the repo). **Which market to start in is still open**; two cheap tests
> would settle most of it — the Kalshi maker-fee test on the demo environment
> (`B-003`), and one paired quote call near 10:00 ET to learn whether `B-002` is
> an after-hours fault or a general one. A lost run's proposal to narrow the
> mission to "signals for a human trader" is with the owner, not adopted.

## Open ground

Staked out, not built. Pick any up without asking — see
[`sandbox/`](sandbox/README.md).

- [`strategies/`](strategies/README.md) — **1 source, 10 claims, all untested.**
  Options-flow gamma levels, sandbox and paper record ready. Only the 90-day
  open-interest history is missing.
- [`fair-value-model.md`](sandbox/fair-value-model.md) — **in progress.** BTC vs
  a lognormal model; gaps unbelievable because settlement is misspecified.
- [`data-collection.md`](sandbox/data-collection.md) — **partly answered.** Stock
  volume history is now bought, not collected; option volume still must be banked
  daily and cannot be backfilled. The Actions cron still needs a merge to `main`.
- [`backtest-harness.md`](sandbox/backtest-harness.md) — no code exists yet.
- [`cost-model.md`](sandbox/cost-model.md) — Kalshi priced; equities still need a
  regular-hours measurement.
- [`markets-untouched.md`](sandbox/markets-untouched.md),
  [`robinhood.md`](sandbox/robinhood.md) — market choice unargued; broker mapped.

## Where the detail lives

| Looking for | Go to |
|---|---|
| Why a belief is believed | [`research/beliefs.md`](research/beliefs.md) → the `B-NNN` id |
| What was actually run | [`research/experiments.md`](research/experiments.md) → the `EXP-NNN` id |
| Traps, live systems, working data endpoints | [`thoughts/handoff.md`](thoughts/handoff.md) |
| Where a previous session got stuck | [`thoughts/4-walls.md`](thoughts/4-walls.md) |
| What went wrong and why | [`thoughts/5-postmortems.md`](thoughts/5-postmortems.md) |
| How the owner rated past work | [`SCORECARD.md`](SCORECARD.md) |
| Work staked out but not started | [`sandbox/`](sandbox/README.md) |
| What a strategy source claims | [`strategies/`](strategies/README.md) → the `claims` list |

---

## How this page stays useful

### It has a hard cap: 150 lines

Run `./scorecard/summary.sh` — it reports the current size. **Over the cap, the
next session consolidates rather than extends.** No exceptions, because the
exception is how every document like this dies.

This constraint is the entire point. The record below grows without limit; if
catching up meant reading all of it, catch-up cost would rise forever. A
fixed-size front page means **knowledge compounds while reading cost stays flat.**

### Every session pays into it

Appending to the log is not enough — that only moves the problem. A session that
learns something also edits this page: promote what earned its place, retire
what died, sharpen a line that has become vague, delete a line that stopped
being load-bearing.

**Consolidation is real work, not tidying.** Five experiments circling one idea
should collapse into a single sentence that carries the conclusion, with the
five ids after it. That sentence is worth more than the five entries, and it is
what makes the next session fast.

### What earns a line here

Something a session would be **materially worse off not knowing.** Not
everything true, not everything interesting — only what changes what the next
agent does.

Promote a belief here when it reaches **T2 or better** (survived data it was not
designed on) or when it is a hard constraint on what is possible. Retire it the
moment its falsification condition trips, and move the line to **What is dead**
with the date. A retired belief is not deleted from `beliefs.md`; it stays there
marked `RETIRED`, because a disproven idea is more instructive than one never
tested, and deleting it invites rediscovery.

### The ids are the network

`KNOWLEDGE.md` → `B-NNN` → `EXP-NNN` → the raw work. Every line here carries the
ids it rests on, so a reader can descend from one sentence to the full evidence
in two hops and stop at whatever depth answers the question.

Keep the chain intact. An id that points nowhere breaks the path from summary to
evidence, and a summary that cannot be traced back is just an assertion.
