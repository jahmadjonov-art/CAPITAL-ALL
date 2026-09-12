# Knowledge

**The one page every session reads.** Everything else is looked up only when
this page points at it.

---

## The goal

Make money in tradable markets — futures, equities, options, prediction markets.
Full charter in [`MISSION.md`](MISSION.md).

## What we know

Claims that have earned a place here. Each is one line, carries its evidence
tier, and names the experiments behind it so the detail can be pulled on demand.

> _Nothing yet. No experiment has been run._

## What is dead

Things tried that did not work, one line each. **This section is as valuable as
the one above and cheaper to fill.** It is what stops five future sessions
independently rediscovering the same dead end.

> _Nothing yet._

## What is live right now

The question currently being worked, and by whom.

> _Nothing in flight. The next `/research` session picks a starting market —
> see [`thoughts/3-unknown.md`](thoughts/3-unknown.md)._

## Where the detail lives

| Looking for | Go to |
|---|---|
| Why a belief is believed | [`research/beliefs.md`](research/beliefs.md) → the `B-NNN` id |
| What was actually run | [`research/experiments.md`](research/experiments.md) → the `EXP-NNN` id |
| Traps, live systems, working data endpoints | [`thoughts/handoff.md`](thoughts/handoff.md) |
| Where a previous session got stuck | [`thoughts/4-walls.md`](thoughts/4-walls.md) |
| What went wrong and why | [`thoughts/5-postmortems.md`](thoughts/5-postmortems.md) |
| How the owner rated past work | [`SCORECARD.md`](SCORECARD.md) |

---

## How this page stays useful

### It has a hard cap: 150 lines

Run `./scorecard/summary.sh` — it reports the current size. **Over the cap, the
next session consolidates rather than extends.** No exceptions, because the
exception is how every document like this dies.

This constraint is the entire point. The record below this page grows without
limit, and if catching up meant reading all of it, catch-up cost would rise
forever until sessions spent their whole budget reading and none working. A
fixed-size front page means **knowledge compounds while reading cost stays
flat.**

### Every session pays into it

Appending to the log is not enough — that only moves the problem. A session that
learns something also edits this page: promote what earned its place, retire
what died, sharpen a line that has become vague, delete a line that stopped
being load-bearing.

**Consolidation is real work, not tidying.** Five experiments circling one idea
should collapse into a single sentence that carries the conclusion, with the
five ids after it. That sentence is worth more than the five entries, and it is
what makes the next session fast.

### What earns a line here

Something a session would be **materially worse off not knowing.** Not
everything true, not everything interesting — only what changes what the next
agent does.

Promote a belief here when it reaches **T2 or better** (survived data it was not
designed on) or when it is a hard constraint on what is possible. Retire it the
moment its falsification condition trips, and move the line to **What is dead**
with the date. A retired belief is not deleted from `beliefs.md`; it stays there
marked `RETIRED`, because a disproven idea is more instructive than one never
tested, and deleting it invites rediscovery.

### The ids are the network

`KNOWLEDGE.md` → `B-NNN` → `EXP-NNN` → the raw work. Every line here carries the
ids it rests on, so a reader can descend from one sentence to the full evidence
in two hops and stop at whatever depth answers the question.

Keep the chain intact. An id that points nowhere breaks the path from summary to
evidence, and a summary that cannot be traced back is just an assertion.
