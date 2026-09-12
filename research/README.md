# Research

The whiteboard. Every test run here, what came of it, and what we currently
believe as a result.

Two files, deliberately separated:

| File | What it is |
|---|---|
| [`experiments.md`](experiments.md) | **Append-only.** What was tried and what happened. Entries are never edited to look better and never deleted, including the embarrassing ones. |
| [`beliefs.md`](beliefs.md) | **Revisable.** What we currently think is true, each belief citing the experiments behind it and stating what would kill it. |

The split is the same one the scorecard uses — an immutable log, and a living
summary derived from it. It exists because beliefs must be free to change while
the evidence behind them must not.

---

## Evidence tiers

Every claim carries a tier. Nothing is ever promoted above the evidence that
actually exists for it.

| Tier | Meaning |
|---|---|
| **T0 — Idea** | A hypothesis. No test has been run. Costs nothing, proves nothing. |
| **T1 — Backtest** | Survived historical simulation. **The weakest real tier**, and the one that lies most often. |
| **T2 — Out-of-sample** | Survived data that was held out and untouched while the strategy was designed. |
| **T3 — Paper** | Traded forward on live prices with no money at risk. Catches lookahead and data-snooping that T1 and T2 cannot. |
| **T4 — Live** | Real fills, real costs, real size. The only tier that has ever paid for anything. |

A T1 result is a reason to run the next test. It is not a reason to trade.

---

## The rules that make the log worth keeping

These target one specific failure: a search process that tries many things and
keeps the winners will produce winners whether or not an edge exists. Every rule
below is aimed at that.

### 1. Pre-register before you run

Write the hypothesis, the method, and **what result would count as success**
into `experiments.md` *before* executing. A prediction made after seeing the
outcome is not a prediction, and a success threshold chosen after seeing the
result is not a threshold.

### 2. Count every variant you tried

The single most important number in an entry. If you tested thirty parameter
combinations and are reporting the best one, **the entry says thirty.** A result
reported without its attempt count is uninterpretable, because the reader cannot
tell skill from search.

Rough calibration: with 30 variants tried, expect the best one to look good at
p ≈ 0.05 by chance alone. Reaching that bar after a broad search is the *null*
result, not the finding.

### 3. Hold data back, and burn it honestly

Designate an out-of-sample period before designing anything, and do not look at
it. When you finally test against it, that period is **spent** — record that it
was used. Tuning against it and re-testing turns T2 straight back into T1, and
the log must show when that happened.

### 4. Costs are part of the result

Every number states its assumed spread, commission, slippage and any borrow or
assignment cost. A gross-of-costs figure is not a result and does not get a tier.
Many published-sounding edges are smaller than the spread they would have to
cross.

### 5. State what would falsify it

Every belief in `beliefs.md` names a concrete condition that would retire it —
a drawdown, a regime change, a number of consecutive losing trades. A belief
with no exit condition never gets retired; it just quietly keeps costing money.

### 6. Write down the alternative explanation

Required on every result, positive or negative. What else could produce this
besides the effect you are claiming? Lookahead leakage, survivorship in the
symbol list, a single outlier trade carrying the whole return, one regime that
happened to dominate the window, a corporate action handled wrong.

If you genuinely cannot think of an alternative, say so — but that is usually a
sign of not having looked, not of there being none.

### 7. Never fabricate

No invented prices, fills, returns or statistics — not as illustration, not as
placeholder, not to show what an entry would look like. Unavailable data is
recorded as unavailable. A fabricated number in this log poisons every belief
downstream of it, and nobody will know which ones.

---

## Entry formats

### `experiments.md` — newest first

```
### EXP-NNN · YYYY-MM-DD · Short title
**Tier reached:** T0–T4
**Market / instrument:**
**Hypothesis (pre-registered):** written before the run
**Success criterion (pre-registered):** the bar, set in advance
**Method:** data range, rules, position sizing
**Costs assumed:** spread, commission, slippage
**Variants tried:** N  ← including everything abandoned along the way
**Result:** what happened, against the criterion
**Alternative explanations:** what else could produce this
**Status:** promoted to T? / dead / parked — and why
```

### `beliefs.md` — strongest evidence first

```
### B-NNN · Short statement of the belief
**Tier:** T0–T4
**Evidence:** EXP-NNN, EXP-NNN
**Why we think this:** the reasoning, hedged honestly
**What would falsify it:** a concrete, checkable condition
**Last reviewed:** YYYY-MM-DD
```

Retired beliefs stay in the file, marked `RETIRED` with the date and what killed
them. A belief that was wrong is more instructive than one that was never tested,
and deleting it invites someone to rediscover it in a year.

---

## Where the data comes from

This environment has a live Robinhood connection (`mcp__Robinhood__*`) providing
real market data: `get_equity_historicals` (OHLCV bars, split-adjusted by
default, explicitly intended for backtesting), `get_equity_quotes`,
`get_option_chains`, `get_option_instruments`, `get_option_historicals`,
`get_index_quotes`, fundamentals, earnings and SEC filing tools.

**The same connection places real orders.** Read the execution rules in
[`thoughts/handoff.md`](../thoughts/handoff.md) before going anywhere near
those tools.

Known gaps to design around rather than ignore: this source is a retail
brokerage feed, not a research-grade dataset. Assume no survivorship-bias-free
delisted-symbol history, limited depth of history at fine intervals, and no
futures data — which matters, because futures are named in the mission. Finding
data for the markets this source does not cover is an open question in
[`thoughts/3-unknown.md`](../thoughts/3-unknown.md).
