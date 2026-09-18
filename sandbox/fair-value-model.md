# Fair-value model for short-dated BTC contracts

**Status:** IN PROGRESS
**Opened:** 2026-09-13

## The goal

A model that prices Kalshi's short-dated Bitcoin contracts well enough that a
disagreement with the market means something. Then a calibration record proving
it, before a cent is ever risked on it.

## Why it matters

It is the one version of "spot mispricing across markets" that does **not**
require speed. A latency race against co-located firms is unwinnable from a REST
API; being better-calibrated than a thin market is not. **That reframe is the
whole reason this is worth pursuing** — it turns an impossible edge into a
merely difficult one.

## What is already known

**A working first cut exists** — `dashboard/desk.py`, published as the desk
console. It fetches spot from Kraken, Coinbase and Binance.US, measures realised
volatility from one-minute bars, and prices each open contract as
`P = Φ(d₂)`, `d₂ = [ln(S/K) − σ²τ/2] / (σ√τ)`.

First readings: a **+7.5¢ gap** against a 1¢-spread market — and shortly before,
−4.8¢ on the same series. **A gap that large and that unstable is the model
being wrong, not an edge.**

Known defects, in order of how much they probably matter:

1. **Settlement is misspecified.** These contracts resolve on a CF Benchmarks
   index averaged over the final minute, not spot at the close. Averaging cuts
   terminal variance, which pushes true fair value toward the extremes relative
   to this model. **Fix this first** — it is a known error, not a guess.
2. **σ is backward-looking** and noisy over a 15-minute horizon. Implied
   volatility from the contract ladder itself is the obvious alternative.
3. **Zero drift** is assumed. Defensible over minutes; still an assumption.
4. **Spot source is unresolved.** Three venues disagreed by $33.51, which is
   material when strikes are $100 apart. The settlement index is the only
   reference that matters and is not currently fetched.
5. **Binance.com returns 451 from here** (geo-blocked). Binance.US, Coinbase and
   Kraken all work.

## What is missing

- The settlement-index fix, and a spot feed that matches it.
- **A calibration record — the part that actually decides this.** Log predicted
  probability against realised outcome for every contract that settles, then
  check whether the 30% bucket settles yes about 30% of the time. Until that
  exists the gap column is decoration. This needs
  [`data-collection.md`](data-collection.md) to be running.
- An honest read on whether an edge survives fees, queue position and adverse
  selection once the model is right.

## How you would know it is done

A calibration curve over a few hundred settled contracts that sits near the
diagonal, and a gap column whose disagreements are small and stable rather than
large and flipping sign.

## Notes from whoever has been here

- **2026-09-13** — Built the instrument, not the model. The console is honest
  about what it does not know, and every number on it is fetched live. The first
  gaps are too large to believe and the page says so on its face.
- **The venue question still gates all of this.** A perfectly calibrated model
  is worth nothing if the funded Robinhood account cannot rest an order on the
  Kalshi book. Settle that before investing more here — see `B-004`.
