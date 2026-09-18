# Cost model

**Status:** OPEN
**Opened:** 2026-09-12

## The goal

Real, sourced numbers for what a trade actually costs on each venue available
here — so that "costs assumed" in an experiment means something verifiable
instead of a number someone picked.

## Why it matters

`research/README.md` requires every result to state its costs, and
`MISSION.md` says a figure quoted before costs is not a result. **That rule is
currently unenforceable, because no agent has any basis for choosing a cost
figure.** The first session to run a backtest will invent one.

This is not a small correction. Many strategies that look profitable are smaller
than the spread they have to cross, and an optimistic cost assumption is one of
the most reliable ways to manufacture an edge that does not exist.

## What is already known

**Kalshi is now priced properly — see `B-003`.** Taker fee is
`ceil(0.07 x contracts x P x (1-P))` per side, so 3.5c round trip at a 50c
contract against a 1c spread. Settlement is free, so holding to resolution costs
one fee rather than two. Maker fees appear to be zero on 1,287 of 1,329 open
series (untested — the demo environment settles it). Caveat: the 0.07 constant
is from the 2022 CFTC filing, not the current July 2026 schedule, which is
behind a bot checkpoint.

**Equities: the quote feed cannot price a spread after hours** (`B-002`). Use
`review_equity_order`'s `market_data_disclosure`, which was verified accurate to
the cent. That tool simulates without placing, so it is the safe way to measure
real spreads — and during regular hours it is the obvious instrument for
building this model.

Still unmeasured, and the shape of what remains:

- **Equities** — commission-free at this broker, but payment-for-order-flow
  execution means the real cost is spread and price improvement, not fees.
- **Options** — per-contract fees plus regulatory fees, and the spread on
  illiquid strikes dwarfs both.
- **Crypto** — spread-based, with documented buy and sell collars in the order
  tools.
- **Futures (Yahoo data)** — not tradable through this connection at all, so any
  futures backtest needs a cost assumption from a venue we do not have. Say so
  rather than borrowing the equity number.
- **Prediction markets (Kalshi)** — **done, see above.** Note that Robinhood's
  own event contracts are *not* Kalshi contracts: Robinhood Derivatives routes
  to three exchanges and adds its own commission, `k x p x (1-p) x c` with
  k = 5% on Gold or 10% without, capped at 1c per contract, plus a
  pass-through of up to another 1c. Cheaper than Kalshi near 50c, dearer at the
  extremes. Do not treat the two venues as interchangeable.

## What is missing

- Measured spreads by instrument and time of day, rather than assumed ones.
- Slippage: how far a realistic fill sits from the quoted mid.
- The fee schedules, fetched from source rather than recalled.
- A defensible default an experiment can cite when it has nothing better —
  clearly labelled as a default, not a measurement.

## How you would know it is done

An experiment can write **"costs: X, per `cost-model.md`"** and have that be a
real, checkable claim rather than a guess.

## Notes from whoever has been here

- **2026-09-12** — Opened on noticing that the costs rule was written before
  anything existed to satisfy it. `review_option_order` returns real fees and
  collateral without placing anything, which is probably the cheapest first step.
