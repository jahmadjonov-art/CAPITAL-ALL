# Experiments

Append-only. What was tried, and what happened.

Entries are **never edited to look better and never deleted.** A failed
experiment is the most valuable thing in this file — it is the only kind of
entry that reliably tells the truth, because nothing is gained by writing it.

Numbering is sequential and permanent: `EXP-001`, `EXP-002`, … A retired or
disproven experiment keeps its number.

Format and the rules governing entries are in [`README.md`](README.md). The
short version: pre-register the hypothesis and the success bar before running,
count every variant tried, state your costs, and name the alternative
explanation.

Newest first.

---

### EXP-001 · 2026-09-13 · Does fee-free Kalshi liquidity actually exist?
**Tier reached:** pending — pre-registered below, before any data was pulled.
**Market / instrument:** Kalshi, open markets across series of both fee types.

**Hypothesis (pre-registered):** `B-003` established that Kalshi taker fees run
~3.5x the spread, killing active taking at $100, and that the surviving route is
resting orders on plain-`quadratic` series which appear to charge no maker fee.
A scout then warned that **the fee-free series and the liquid series are largely
different series** — the cheap venue is the thin one. If that holds, the route is
theoretical and worthless.

So: **do markets exist that are BOTH plain `quadratic` (no maker fee) AND liquid
enough to trade?**

**Success criterion (pre-registered, set before looking):** at least one plain
`quadratic` series containing markets with **24h volume above 1,000 contracts**
AND a **top-of-book spread of 2 cents or tighter**, holding across **three or
more markets** in that series rather than a single lucky contract.

Anything less means the fee-free route is real on paper and not tradable, and
`B-003`'s remaining case collapses.

**Method:** enumerate open markets via the public API, group by series, read
`fee_type` and `fee_multiplier` per series, and take top-of-book from the live
order book. No authentication, no order placed.

**Costs assumed:** none applied — this measures the venue, it does not simulate
a strategy.

**Timing caveat, stated in advance:** it is late Saturday ET. US equities are
closed, sports are mid-weekend, and Kalshi's crypto markets run continuously.
**Weekend books are not weekday books**, so a negative result here is weaker
than a positive one, and any positive must be re-measured on a weekday before it
is trusted.

**Variants tried:** 1 — this is a single pre-specified measurement, not a search.

**Result:** _running_

---
