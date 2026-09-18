# Following: Options Flow / Gamma Levels

**Status:** OPEN
**Opened:** 2026-09-13
**Strategy:** [`strategies/options-flow-gamma.json`](../strategies/options-flow-gamma.json)
**Paper log:** `strategies/paper/options-flow-gamma.jsonl`

## The goal

Follow this strategy as its source describes it, keep a running record of what it
would have done, and find out which of its ten claims survive.

Not to judge it in advance. **To follow it and see.**

## Why it matters

It is the first source in the library, and the method for evaluating it is the
method every later source will be evaluated by. Getting the process right here
matters more than the verdict on this particular strategy.

## What is already known

- The strategy is fully extracted: mechanism, entry and exit rules, the slope
  filter, 30-50 tick stops, first-two-hours restriction, the volatility-surface
  reading, the calendar events. All ten of its claims are logged `untested`.
- **The one hard requirement is gamma exposure by strike, and nothing here pulls
  it.** CBOE is named in the transcript as free with a 10-15 minute delay. An
  options subscription is expected from the owner.
- Instrument economics for the paper record: NQ is $5.00 a tick, ES $12.50.
  A 40-tick stop on one NQ is $200; the 400-600 tick moves the source cites are
  $2,000-$3,000.
- `strategies/paper.py` handles the record and refuses to count a signal that was
  not committed before it was settled.

## What is missing

1. **A gamma-by-strike source.** Until then no signal can be generated at all —
   this is the blocker, not the strategy.
2. A written procedure turning the rules into a decision an agent can execute
   the same way twice: how max gamma is located, what counts as a fast versus
   slow approach, where the stop sits relative to structure.
3. The slope filter needs a number. "Steep" and "gentle" are qualitative in the
   transcript; a forward test needs a threshold, chosen in advance and recorded
   as a choice we made rather than something the source specified.
4. Thirty-plus settled signals. Below that, win rate cannot separate an edge
   from noise.

## How you would know it is done

Each of the ten claims is marked tested with an experiment id, and the paper
record carries enough settled signals to say whether the expectancy is positive
after costs — not just the win rate.

## Notes from whoever has been here

- **2026-09-13** — Opened alongside the extraction. Nothing followed yet, because
  the gamma feed does not exist here. **The honest state is: the strategy is
  understood and cannot currently be run.**
- The capital constraint has been removed from the evaluation deliberately. This
  is judged at one NQ contract as the source describes, and affordability is a
  separate question. Do not reintroduce it as a filter.
- When the subscription arrives, the first question is whether it carries
  intraday history or only snapshots. Snapshots allow forward testing only;
  history allows a backtest, and that single fact decides how long this takes.
