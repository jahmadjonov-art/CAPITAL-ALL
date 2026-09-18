# Markets nobody has looked at yet

**Status:** OPEN
**Opened:** 2026-09-12

## The goal

Pick where to actually start. Every market named in the mission is reachable and
none has been examined.

## Why it matters

The choice of first market shapes everything after it, and it is currently being
made by nobody. **Defaulting to equities because the broker connection is wired
up would be a decision made by tooling rather than reasoning** — which is
exactly the trap the data reconnaissance was meant to avoid.

## What is already known

All verified 2026-09-12; endpoints in `thoughts/handoff.md`.

- **Futures** — Yahoo Finance, free, no key. `GC=F` returned COMEX gold with
  real daily bars. `ES=F`, `CL=F`, `NG=F` follow the same convention. Not
  tradable through this connection, so it is research-only for now.
- **Prediction markets** — Kalshi's public API works unauthenticated. **The
  optimistic read below was largely wrong and is corrected here rather than
  quietly edited away.** Taker fees run about 3.5x the bid-ask spread at 50c, so
  active trading is not viable at $100 — see `B-003`. What survives is resting
  orders (apparently free on 97% of series, untested) and holding to settlement
  (one fee instead of two; settlement itself is free).

  Also a live legal risk: the circuits split in 2026, with the Ninth ruling
  against Kalshi in August. Sports contracts are the exposed category — and they
  are also the most liquid markets on the venue, which is an uncomfortable
  overlap. Economic, weather and financial-data markets look more durable.

  _Original hunch, kept for the record: "young, thinner... where a small
  operator's edge is most likely to survive. Contracts resolve to a known truth,
  so being right is measurable." The measurability point still stands. The edge
  point did not survive contact with the fee schedule._
- **Options** — rich tooling through Robinhood: chains, instruments, historicals,
  quotes, and `review_option_order` for real fees and collateral. Also the
  easiest place here to lose money quickly, and the one where a cost model
  matters most.
- **Equities** — best-supported path. Also the most efficient, most crowded, and
  the hardest place for a small operator to find anything.
- **Crypto** — tradable, 24/7, spread-based costs.

## What is missing

A reasoned choice, written down. Not a survey of all five — **one market,
argued for**, with the reasoning recorded so that a later session can revisit
the decision rather than inherit it as an unexamined assumption.

## How you would know it is done

`KNOWLEDGE.md` names the market being worked and why, and the first experiment
in that market has run.

## Notes from whoever has been here

- **2026-09-12 (later)** — A `scout` priced the Kalshi route properly. The
  prediction-market hunch is now substantially undermined for active trading
  (`B-003`). It is not dead: the maker-fee question could revive it entirely, and
  settling that is cheap via the demo environment. **Nobody should pick this
  venue until that one test is run.**
- **2026-09-12** — Left deliberately unchosen. The reconnaissance that made all
  five reachable happened in the same session, and picking immediately would
  have meant choosing on an hour of familiarity rather than on any analysis.
  Prediction markets look most promising on structural grounds — that is a
  **Hunch**, labelled as one, and should be tested rather than trusted.
