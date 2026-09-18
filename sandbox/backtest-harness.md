# Backtest harness

**Status:** OPEN
**Opened:** 2026-09-12

## The goal

Shared code that takes a strategy specification and returns an honest result —
so that every experiment is measured the same way and nobody rebuilds the
machinery from scratch.

## Why it matters

**There is no code in this repository at all yet.** The first session to test
anything will write a backtest from nothing, and the second will write a
different one. Results measured by two different harnesses are not comparable,
and the bugs that matter here are subtle enough to be invented independently
every time.

A harness is also the natural place to make the discipline structural rather
than aspirational: if it refuses to return a gross-of-costs figure, no
experiment can quote one.

## What is already known

The errors it must make impossible, all documented in `research/README.md` and
`thoughts/handoff.md`:

- **Lookahead.** A signal from bar *t* may only fill at *t+1* or later. Using
  the same bar to decide and to fill is the most common fatal error.
- **Interpolated bars.** Robinhood marks synthesised gap fills
  `interpolated: true`. They must be dropped, or they flatten volatility.
- **Costs.** Mandatory input, not an optional adjustment.
- **Survivorship.** No available source carries delisted symbols. The harness
  cannot fix this, but it can force the assumption to be stated.
- **Trade count.** Report sample size in trades, not bars.
- **Variant count.** If it runs a parameter sweep, it should report how many
  combinations were tried, so the log cannot quietly omit it.

Language is open. Python 3.11 and Node 22 are both available; Python is the
obvious choice for the ecosystem, but nothing depends on it yet. **Whoever
builds this also settles the root `.gitignore`, which has been deliberately
deferred until the stack is known.**

## What is missing

All of it. Worth deciding early: whether to use an existing library or write a
minimal one. A dependency brings correctness and a learning curve; two hundred
lines of purpose-built code stays readable and does exactly what it says.
No opinion is recorded here on purpose — that choice belongs to whoever builds it.

## How you would know it is done

Two different strategies can be expressed and run through it, and it refuses —
structurally, not by convention — to produce a result with costs missing.

## Notes from whoever has been here

- **2026-09-12** — Opened rather than started. A harness written before any real
  strategy exists would be shaped by guesses about what strategies need. The
  better order is probably: run one strategy end-to-end by hand, notice what was
  painful, then extract the harness from that.
