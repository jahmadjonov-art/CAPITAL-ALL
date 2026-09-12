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

- **The account is $100, cash, options level 2 — which closes options to us
  entirely.** A contract covers 100 shares, so cash-secured puts and covered
  calls both cap out at a $1.00 underlying, and a long call buys one binary bet
  dominated by its own spread. Equities (fractional shares work) and crypto are
  what remain. Cash settlement is T+1, so plan on about one round trip per
  dollar per day. — `B-001`, Tested + Reasoned
- **Only one of the four brokerage accounts is reachable by an agent** —
  `••••6622`, nicknamed "Agentic". The owner's default account is closed to us
  by the broker itself, not merely by our own rule. — measured 2026-09-12

## What is dead

Things tried that did not work, one line each. **This section is as valuable as
the one above and cheaper to fill.** It is what stops five future sessions
independently rediscovering the same dead end.

> _Nothing yet._

## What is live right now

The question currently being worked, and by whom.

> Session of 2026-09-12 audited the funded account and found the capital
> constraint above. A `scout` is checking whether Kalshi is economically viable
> at $100, and a `skeptic` is attacking a claim that the quote tool's bid/ask
> fields are unusable for spread calculations. **Which market to start in is
> still open**, but options are now ruled out on arithmetic.

## Open ground

Staked out, not built. Pick any up without asking — see
[`sandbox/`](sandbox/README.md).

- [`robinhood.md`](sandbox/robinhood.md) — what the connection can actually do.
  Nothing has been called; every answer is one tool call away.
- [`cost-model.md`](sandbox/cost-model.md) — real trading costs. **The costs rule
  is unenforceable until this exists.**
- [`backtest-harness.md`](sandbox/backtest-harness.md) — no code exists yet.
- [`markets-untouched.md`](sandbox/markets-untouched.md) — which market to start
  with, argued for rather than defaulted into.

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
