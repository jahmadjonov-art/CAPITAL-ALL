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

### EXP-002 · 2026-09-14 · Full-chain 0DTE gamma from a free source
**Tier reached:** T2
**Market / instrument:** SPX options, 2026-09-14 expiry (0DTE), via CBOE.

**Hypothesis (pre-registered):** a lost scheduled session reported that CBOE
serves full-chain gamma without a broker. Re-establish it independently: does one
unauthenticated request return every strike with greeks and open interest, and
does the resulting gamma profile agree with the six-strike broker sample?

**Success criterion (pre-registered):** the endpoint returns the whole chain with
`gamma` and `open_interest` per contract, unauthenticated, and a net dealer gamma
can be computed from it.

**Method:** one GET, parse the OCC-style option symbols into expiry/type/strike,
aggregate `gamma × open_interest × 100 × spot² × 0.01` by strike, net calls
against puts.

**Costs assumed:** none — this measures data availability, not a strategy.

**Variants tried:** 1.

**Result: criterion met.** 28,934 contracts in one 12.8 MB response, no key. The
0DTE expiry held 488 of them. Net dealer gamma **−$23.03B**, call wall and put
wall both at **7,600**, gamma flip **7,625** with spot **below** it.

**The interesting part is the disagreement.** The six-strike broker sample read
**−$54M**; the full chain reads **−$23B**. Same sign, magnitude off by ~400×.
The sign survived a 400× error in magnitude, which says the regime call is far
more robust to thin sampling than any number attached to it — and that quoting
the number from a sample would have been badly wrong.

**Alternative explanations:** the two readings are from different sessions
(Friday close vs Monday intraday), so they are not strictly comparable. The
sampling gap is still the dominant term — six strikes cannot contain a profile
whose mass sits across hundreds.

**Status:** promoted to `B-005`. Open interest here is end-of-day and does not
move intraday, so this does not solve same-day flow.

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

**Result:** **Criterion technically met — by one series — but the criterion
itself turned out to be poorly designed, and that matters more than the pass.**

Measured from a 1,000-trade tape window at ~23:30 ET, fee type per series, and
live top-of-book:

| Series | Fee type | Contracts (window) | Median spread |
|---|---|---|---|
| KXBOXING | **quadratic (free maker)** | 13,896 | 1c |
| KXNCAAFGAME | quadratic_with_maker_fees | 11,891 | 2c |
| **KXBTC15M** | **quadratic (free maker)** | 6,171 | **1c** |
| KXBOXINGMOV | quadratic (free maker) | 4,825 | 6c |
| KXLIGAMXGAME | **quadratic (free maker)** | 1,586 | **1c** |
| KXETH15M / KXSOL15M / KXBTCD | quadratic (free maker) | 550–580 | 1c |

**The headline, which contradicts the earlier finding:** fee-free series and
liquid series **do** overlap. KXBOXING traded the most contracts of any series
in the window at a 1-cent spread with no maker fee. KXBTC15M — Bitcoin
15-minute contracts — was second, also 1 cent, with 2,982 / 1,126 contracts
resting at the touch. A $100 account needs ~200 contracts at 50c, so the book
carries that size many times over.

The earlier "largely disjoint" conclusion was drawn from NFL, EPL and MLB, which
do charge maker fees. It was not wrong about those; it generalised from an
in-season sample. **Which categories are liquid changes with the sporting
calendar and the hour**, so neither reading is a fixed property of the venue.

**The criterion flaw, stated rather than defended:** the bar required 3+ markets
in one series at ≤2c. Only **KXLIGAMXGAME** cleared it — and its three markets
are home/away/tie on a *single football match*, not three independent markets.
Meanwhile **KXBTC15M failed** on 1 market despite better volume and the same 1c
spread, purely because 15-minute contracts are **sequential** — only one is live
at a time, so it can never show three.

So the bar measured *market count per event*, not liquidity, and it excluded the
most interesting candidate on a technicality. **The pass is an artifact.** The
honest reading is that the underlying question — do fee-free liquid markets
exist — is answered **yes** by the volume and spread data, and the pre-registered
test was simply the wrong instrument for it.

**Alternative explanations, not ruled out:**
- **Saturday-night selection.** College football, boxing and crypto were live;
  the NFL/MLB markets that charge maker fees were not. This may be an
  hours-of-the-week artifact rather than a property of the venue.
- **One snapshot, top-of-book only.** Depth behind the touch is unmeasured, and
  a 1c spread holding 10 contracts is not a 1c spread for a $100 position.
- **The load-bearing assumption is still untested:** that `fee_type: quadratic`
  actually means resting orders pay nothing. That is read from an API enum and a
  2022 filing, never from a filled order. **If it is false, everything above is
  irrelevant.**

**Status: WOUNDED by a skeptic — read `B-004`, not this entry, for what stands.**

What survived: fee-free and liquid genuinely do overlap, and not because of the
weekend — KXBTCD holds the same spread on **higher** Friday-afternoon volume.

What did not: the series ranking above came from a tape sample spanning **4–7
seconds**, not a window, and reshuffles completely on re-sampling. KXBOXING and
KXBOXINGMOV have **one-sided books** (bid size 194 against ask size 288,226 — the
tell was in the table above and went unread). And the ETH/SOL examples cost
**11.6%** and **17.4%** to round-trip at $100 once the book is walked properly.

The honest lesson is in `thoughts/5-postmortems.md`. The measurement was sound in
method and careless in reading.

---
