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

- **$100, cash account, options level 2 — options are closed to us.** A contract
  covers 100 shares, capping puts and covered calls at a $1 underlying. Equities
  (fractional works) and crypto remain; T+1 settlement allows ~one round trip
  per dollar per day. — `B-001`
- **Kalshi: fees are ~3.5× the spread, so active taking is dead at $100.** A
  round trip near 50¢ costs 7% of the account. The fee-free series and the
  liquid series are **mostly different series** — the cheap route is the thin
  one. **The one overlap worth a look: Kalshi's crypto markets are fee-free type
  *and* had real volume at 1–2¢.** Fee multipliers are per-market; never
  hard-code them. — `B-003`
- **Never price a spread from `get_equity_quotes` after hours** — 487× wrong on
  SPY, and the symbols that looked tight were the most misleading. Use
  `review_equity_order`'s disclosure. Untested in regular hours. — `B-002`
- **A weekday research run fires automatically at 15:10 UTC** — but those
  sessions get **no broker tools**, so they cannot read the account or quote
  equities. Broker-shaped work needs an interactive session. — measured
  2026-09-12
- **Only one brokerage account is agent-reachable** (`••••6622`); the owner's
  default is closed by the broker itself. **Subagents cannot reach the Robinhood
  tools at all** — the lead must fetch broker data and paste it into their brief.
  — measured 2026-09-12

## What is dead

Things tried that did not work, one line each. **This section is as valuable as
the one above and cheaper to fill.** It is what stops five future sessions
independently rediscovering the same dead end.

> _Nothing yet._

## What is live right now

The question currently being worked, and by whom.

> Session of 2026-09-12 audited the funded account. Options are ruled out on
> arithmetic (`B-001`); the quote feed's after-hours bid/ask proved unusable
> (`B-002`). **Which market to start in is still open.** A `scout` is checking
> whether Kalshi is economically viable at $100 — that answer decides it.
>
> **Two concrete tasks are queued, both cheap and both decisive:**
> 1. **The Kalshi maker-fee test** (`B-003`) — do resting orders on plain
>    `quadratic` series really cost nothing? The demo environment settles it
>    without money. If yes, look straight at `KXBTCD`/`KXETHD`, the one place
>    fee-free and liquid overlap.
> 2. **The regular-hours quote test** (`B-002`) — one paired call around 10:00 ET
>    says whether the quote feed is broken generally or only after hours.

## Open ground

Staked out, not built. Pick any up without asking — see
[`sandbox/`](sandbox/README.md).

- [`robinhood.md`](sandbox/robinhood.md) — what the connection can actually do.
  Nothing has been called; every answer is one tool call away.
- [`cost-model.md`](sandbox/cost-model.md) — Kalshi now priced (`B-003`);
  equities still need a regular-hours measurement.
- [`backtest-harness.md`](sandbox/backtest-harness.md) — no code exists yet.
- [`markets-untouched.md`](sandbox/markets-untouched.md) — still unchosen. The
  prediction-market hunch was undermined, not killed.
- [`data-collection.md`](sandbox/data-collection.md) — **nothing records
  anything yet**, so no question about the past is answerable. Likely a GitHub
  Actions cron, which needs a merge to `main` first.

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
