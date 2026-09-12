# Unknown

No defensible default was available. Either the question went back to the owner,
or a guess was made and is labelled here as a guess.

An open entry in this file is not a failure. It is a question that has not been
answered yet, parked where the next session can see it instead of rediscovering
it. **Close entries out as they get resolved** — record the answer and date it,
rather than deleting the entry, so the reasoning stays traceable.

Newest first.

---

### 2026-09-12 — OPEN: How much capital, and what drawdown ends the experiment?
**Situation:** the stated risk appetite is *"a little bit of exceeded greed."*
**Unknown:** what that means as numbers.
**Why it cannot be assumed:** "aggressive" is not executable. Position sizing
needs an account size, and the difference between an aggressive programme and a
ruinous one is entirely a maximum-drawdown rule agreed in advance — agreed in
advance specifically because nobody sets one honestly while losing.
**Would resolve it:** two figures. Capital committed to this, and the loss at
which the experiment stops rather than doubles down. A third, the loss on any
single position, would be better still.
**Blocks:** any position sizing, so any T3 paper run or T4 live trade. It does
not block research.

---

### 2026-09-12 — OPEN: Where does futures and prediction-market data come from?
**Situation:** the mission names futures and prediction markets. The attached
Robinhood connection covers equities, options, indexes and crypto — **not
futures**, and not prediction-market venues such as Kalshi or Polymarket.
**Unknown:** whether to source that data elsewhere, or to start where the data
already is and expand later.
**Why it cannot be assumed:** starting with equities and options because that is
what is wired up is a decision made by tooling rather than by reasoning, and it
may be exactly wrong — prediction markets in particular are young, thinner, and
plausibly less efficient, which is where a small operator's edge is most likely
to be.
**Deliberately not guessed:** no data vendor has been signed up for and no API
key requested.
**Would resolve it:** which market to start with, and whether paying for data is
on the table or this stays free-tier.

---

### 2026-09-12 — OPEN: Does the no-autonomous-execution rule stand?
**Situation:** the live brokerage tools can place real orders. A conservative
default has been written into `MISSION.md` and `handoff.md`: no order is ever
placed, cancelled or exercised without explicit human approval for that specific
trade.
**Unknown:** whether the owner wants that, or something looser once a strategy
has earned confidence.
**Why it is set conservatively by default:** the cost of the rule being too
strict is that trades need a confirmation. The cost of it being too loose is
unbounded and irreversible, and an agent misreading an instruction as
authorisation is a well-documented way to lose money quickly.
**Would resolve it:** confirmation that the rule stands, or a replacement stated
in the owner's own words with explicit limits — instruments, maximum size,
maximum loss — which then goes into `handoff.md` verbatim.

---

### 2026-09-12 — OPEN: Will agents other than Claude Code ever read any of this?
**Situation:** the stated goal is that "future agents" benefit from these files.
**Unknown:** which ones, and through what tooling.
**Why it cannot be assumed:** `CLAUDE.md` is read automatically at session start
by Claude Code specifically. That is a convention of one tool, not a standard.
A different assistant opening this repository has no reason to look at it and
will most likely never see `SCORECARD.md` or `thoughts/` at all.
**Handled by:** pointing to everything from the root `README.md` too, which is
the one file essentially every tool and person does look at. That raises the
odds; it does not guarantee anything.
**Would resolve it:** knowing which assistants are actually in play. If it is
only ever Claude Code, the current setup is already right and this entry can be
closed. If others are expected, the pointers should move into the root README
proper rather than sitting one link away.

---

### 2026-09-12 — OPEN: Does this match the system that was actually pictured?
**Situation:** both the scorecard and the thoughts board were described out loud
and built from that description in one pass.
**Unknown:** whether the written result matches what was in the owner's head.
**Why it cannot be assumed:** a spoken description of a filing system leaves out
almost everything about its shape. Several choices here — the confidence ladder
as three files, "would have settled it" as a required field, directives being
binding rather than advisory — are inventions that sounded right, not things
that were specified.
**Would resolve it:** reading `2-judgment-calls.md` and saying whether that is
the kind of thing that is useful to see. That file is the whole bet; if its
entries are not what was wanted, the format should change now while there are
six of them rather than sixty.

---

### 2026-09-12 — RESOLVED: What is the new project?
**Answered:** 2026-09-12, by the owner.
**Answer:** a trading research programme covering futures, equities, options and
prediction markets, built as an accumulating research record that successive
agent sessions add to. Full charter in [`MISSION.md`](../MISSION.md).
**Consequence:** the deferred root `.gitignore` can now be written — though it
should wait until the first analysis code lands and reveals whether this is a
Python or a Node repository, which is still genuinely open.
