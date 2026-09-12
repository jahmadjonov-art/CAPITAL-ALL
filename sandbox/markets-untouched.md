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
- **Prediction markets** — Kalshi's public API works unauthenticated. Plausibly
  the most interesting ground here: young, thinner, structurally different from
  continuous markets, and where a small operator's edge is most likely to
  survive. Contracts resolve to a known truth, so being right is measurable in a
  way it is not elsewhere.
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

- **2026-09-12** — Left deliberately unchosen. The reconnaissance that made all
  five reachable happened in the same session, and picking immediately would
  have meant choosing on an hour of familiarity rather than on any analysis.
  Prediction markets look most promising on structural grounds — that is a
  **Hunch**, labelled as one, and should be tested rather than trusted.
