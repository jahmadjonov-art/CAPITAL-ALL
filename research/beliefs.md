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

### B-002 · After hours, the quote tool's bid/ask are unusable — the order simulator's disclosure is correct
**Tier:** T2 — corroborated against an independent tape, but at one timestamp only.
**Scope — read this before using it:** established **for after-hours only**.
There are **zero regular-hours observations.** Do not generalise it.
**Basis:** Tested (the readings) + Cited (corroboration and vendor docs)
**Why we think this:** at 20:00:00 ET on Friday 2026-09-11,
`get_equity_quotes` returned SPY bid 710.75 / ask 774.00 — a $63.25 spread. In
the same instant `review_equity_order`'s `market_data_disclosure` read
"Bid $764.35 × 480 · Ask $764.48 × 40 · Last $764.48" — 13 cents. **A 487×
discrepancy.**

The disclosure is the accurate one. Both its prices and its last print appear
verbatim in Yahoo's 1-minute post-market tape at the stated minute. Robinhood's
own documentation matches the direction: the quotes feed "can be up to a
15-minute delay during extended or overnight trading hours", while the order
summary shows a **consolidated** quote.

**The mechanism is not a bug, which is why no workaround exists.** The levels
cluster on whole dollars — the fingerprint of sparse resting retail limit orders
rather than a market maker's two-sided quote. SPY's quoted bid of 710.75 was
last a live price on 2026-04-30, four months earlier, while its quoted ask was
live days before. Bid and ask come from different price eras, so this is a
truthful read of a book that was empty on one side, not a stale snapshot. **No
correction factor can recover it, and the midpoint is off by 2.89% on SPY.**

**The symbols that look fine are the dangerous part.** IWM and TQQQ appear to
have tight spreads; they do not. IWM's real price sat 0.0011 above its bid with
the ask 56 cents away — a real bid and a phantom ask. Whether a symbol *looks*
sane is luck, which is worse than a uniform failure because eyeballing the
output will not tell you when to distrust it.

Also: `last_trade_price` is the 16:00 ET close while bid/ask are from 20:00 ET.
**They cannot be paired.** SOFI's last trade printing above its ask looks like
free money and is purely this timestamp mismatch.
**What would falsify it:** the pending regular-hours test below. If quotes land
within a cent or two of the disclosure during market hours, this belief narrows
to after-hours and stops being a general warning.
**Pending test — the obvious next move for any session:** one paired call around
10:00 ET on a trading day — `get_equity_quotes` on these eight symbols and
`review_equity_order` on SPY in the same second. Then repeat at 09:35, midday,
15:55, 16:05 and 20:00 to find where the boundary sits. Log `bid_size`/`ask_size`
too: a size that never changes between calls is a tell for a frozen field.
**Last reviewed:** 2026-09-12

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
