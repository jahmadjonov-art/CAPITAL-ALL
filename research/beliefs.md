# Beliefs

What we currently think is true about these markets, and why we think it.

Revisable by design. Every belief cites the experiments behind it, carries an
evidence tier, and names a concrete condition that would retire it. A belief
that cannot be falsified is a hope, and is filed as `T0 — Idea` until it earns
better.

Retired beliefs stay in this file marked `RETIRED`, with the date and what
killed them. Something that was tested and proved wrong is more useful than
something never tested, and deleting it just invites rediscovery.

Strongest evidence first. Format is in [`README.md`](README.md).

---

### B-001 · At $100 in a cash account with level-2 approval, options are closed to us
**Tier:** T2 — a measured constraint, not a market claim. The account state was
read directly; the consequence follows by arithmetic.
**Evidence:** direct measurement 2026-09-12, recorded in
[`thoughts/handoff.md`](../thoughts/handoff.md). No experiment id — nothing was
simulated or backtested to reach it.
**Basis:** Tested (account state) + Reasoned (the arithmetic from it)
**Why we think this:** an option contract covers 100 shares. A cash-secured put
therefore needs `strike × 100` in collateral and a covered call needs 100 shares
outright, which at $100 of capital caps both at a $1.00 underlying — there is
nothing there worth trading. A long call or put is affordable but buys exactly
one contract, making it a single binary bet whose largest cost is the spread
crossed to enter and exit. Level 2 also excludes spreads, which are the usual
way to define risk cheaply.

The account is also **cash, not margin**, so proceeds settle T+1 and capital is
locked until they do. Any strategy needing more than roughly one round trip per
dollar per day is unavailable here regardless of whether it works.
**What is left:** equities including fractional shares — a $50 dollar-denominated
SPY market order reviewed clean, with no broker alerts — and crypto, which has
its own $100 of buying power and trades around the clock.
**What would falsify it:** the account being funded substantially higher, upgraded
to level 3, or converted to margin. Any of those reopens the question and this
belief should be retired rather than quietly carried forward.
**Last reviewed:** 2026-09-12

---

---

_The section below was written before anything had been tested. Keeping it: the
prediction it makes has so far been right._

The first entries here will most likely be constraints rather than edges — what
the data source cannot support, what costs make unviable, what timeframes are
unreachable from this environment. Those are worth recording as beliefs too;
knowing where not to look is a result.
