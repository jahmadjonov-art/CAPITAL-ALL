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
  100-share multiplier caps puts and covered calls at a $1 underlying. Reading
  the chain is not closed. — `B-001`
- **CBOE serves the whole option chain free and unauthenticated** — 28,934 SPX
  contracts in one request, gamma and open interest on each, and it works from a
  script or subagent where the MCP tools do not. 0DTE net dealer gamma **−$23B
  (negative — do not fade)**, walls both at 7,600, flip above spot. **Its open
  interest is end-of-day and does not move intraday.** — `B-005`, `EXP-002`
- **Read the gamma sign before applying any level rule.** Positive = dealers
  dampen, fading works. Negative = dealers amplify, fading gets run over. A
  six-strike sample got the sign right and the magnitude wrong by 400× —
  **sampling a gamma profile does not give you a small version of it.**
- **Kalshi is parked on one venue question.** Taking liquidity is dead at $100;
  resting orders are genuinely free and liquid markets exist — but it is all
  Kalshi-direct and we hold Robinhood (~4¢ round trip). A tight spread is also
  not a tradable market there. **Settle the venue before scanning further.**
  — `B-003`, `B-004`
- **A screen that ranks on a ratio must not supply the denominator.** Two
  tip-sheet rankings in a row were artifacts of their own filters: volume ÷ an
  open-interest *floor*, then a "mechanical" flag that fired on 11 of the top 15
  names. CBOE ships greeks per contract, so test the property directly — delta
  pinned at ±1 with no vega left is a stock substitute, not a position, and it
  was 88% of IWM's option notional. — `scanner/tipsheet.py`
- **Broker quirks:** never price a spread from `get_equity_quotes` after hours
  (487× wrong on SPY — use `review_equity_order`'s disclosure); only `••••6622`
  is agent-reachable; **subagents and scheduled runs get no broker tools**;
  Kalshi's API silently returns nothing for pre-migration field names. Details in
  `handoff.md`. — `B-002`

## What is dead

Things tried that did not work, one line each. **This section is as valuable as
the one above and cheaper to fill.** It is what stops five future sessions
independently rediscovering the same dead end.

> _Nothing yet._

## What is live right now

The question currently being worked, and by whom.

> 2026-09-15: the tip sheet is live — `scanner/tipsheet.py` scans 70 names on
> CBOE and `dashboard/tipsheet.py` renders it by day / week / month horizon.
> **Which market to start in is still open**, and two cheap tests would settle
> most of it: the Kalshi maker-fee test on the demo environment (`B-003` — do
> resting orders on plain `quadratic` series really cost nothing?), and one
> paired quote call around 10:00 ET to learn whether `B-002` is an after-hours
> fault or a general one.

## Open ground

Staked out, not built. Pick any up without asking — see
[`sandbox/`](sandbox/README.md).

- [`strategies/`](strategies/README.md) — **1 source, 10 claims, all untested.**
  Options-flow gamma levels, with a sandbox and forward paper record ready.
  **No longer blocked** — only the 90-day open-interest history is missing.
- [`fair-value-model.md`](sandbox/fair-value-model.md) — **in progress.** BTC
  contracts vs a lognormal model; gaps too large and unstable to believe, because
  settlement is misspecified. Fix that first.
- [`data-collection.md`](sandbox/data-collection.md) — **nothing records anything
  yet**, so no question about the past is answerable. Likely a GitHub Actions
  cron, which needs a merge to `main`.
- [`backtest-harness.md`](sandbox/backtest-harness.md) — no code exists yet.
- [`cost-model.md`](sandbox/cost-model.md) — Kalshi priced; equities still need a
  regular-hours measurement.
- [`markets-untouched.md`](sandbox/markets-untouched.md) and
  [`robinhood.md`](sandbox/robinhood.md) — market choice still unargued; the
  broker is now well mapped (account, chains, greeks, quote traps).

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

This constraint is the entire point. The record below this page grows without
limit, and if catching up meant reading all of it, catch-up cost would rise
forever until sessions spent their whole budget reading and none working. A
fixed-size front page means **knowledge compounds while reading cost stays
flat.**

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
