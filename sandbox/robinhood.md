# The Robinhood connection

**Status:** OPEN
**Opened:** 2026-09-12

The owner was explicit that this account is not merely a data feed:

> "Robinhood that is connected also should be looked at as part of the sandbox,
> because it is."

It is somewhere to find out what is possible. Nobody has explored it yet.

## The goal

A clear, written account of what this connection can actually do — its account
state, permissions, limits, costs and quirks — so that no future session has to
discover any of it twice.

## Why it matters

Every research result that assumes an execution path depends on facts nobody
here has checked. A strategy designed around options spreads is worthless if the
account is not approved for them; a backtest is worthless if its cost
assumptions do not match what this broker actually charges.

## What is already known

- **73 tools** under `mcp__Robinhood__*`. Market data, fundamentals, earnings,
  SEC filings, options chains, positions, orders, watchlists, scanners, alerts.
- The account is **deliberate and currently unfunded** (2026-09-12). An order
  today would be rejected for insufficient buying power.
- Order tools require an `agentic_allowed=true` account; options require
  `option_level_2` or `option_level_3`. **Nobody has run `get_accounts` to see
  what this account actually has.**
- `review_equity_order`, `review_option_order` and `preview_crypto_order`
  simulate without placing. They are safe to call and are the obvious way to
  learn the mechanics without touching anything.
- No paper-trading mode exists in this toolset.
- `get_equity_historicals` is split-adjusted by default and documented for
  backtesting. Bars marked `interpolated: true` are synthesised gap fills and
  carry no information.

## What is missing

Almost everything. Open questions, roughly in order of usefulness:

- What does `get_accounts` report — permissions, option level, agentic status,
  buying power, account type?
- What do the `review_*` tools reveal about **real costs**? Fees, collateral,
  the actual spread on a given contract. This is the fastest route to a genuine
  cost model — see [`cost-model.md`](cost-model.md).
- How deep does the history go at each interval, and where is the bar cap?
- What do `get_scans` / `run_scan` / `get_scanner_filter_specs` offer? A
  server-side screener could be a real advantage and nobody has looked.
- Are `get_sec_filing_facts` and the fundamentals tools usable as a research
  dataset, or too thin?
- What are the rate limits, and what happens when you hit them?

## How you would know it is done

`thoughts/handoff.md` carries a section a new agent can read in two minutes and
then use the connection correctly — permissions, real costs, data limits, which
tools are worth using and which are not.

## Notes from whoever has been here

- **2026-09-12** — Connection catalogued from tool definitions only. Nothing was
  called. Opened as a sandbox rather than guessed at, because every answer above
  is one tool call away and a guess would have been written into the record as
  fact.
