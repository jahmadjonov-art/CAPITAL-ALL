# Unknown

No defensible default was available. Either the question went back to the owner,
or a guess was made and is labelled here as a guess.

An open entry in this file is not a failure. It is a question that has not been
answered yet, parked where the next session can see it instead of rediscovering
it. **Close entries out as they get resolved** — record the answer and date it,
rather than deleting the entry, so the reasoning stays traceable.

Newest first.

---

### 2026-09-12 — RESOLVED: How much capital, and what drawdown ends the experiment?
**Answered:** 2026-09-12, by the owner, who declined to set numbers on purpose.
**Answer:** *"Those things will be completely up to the agents."* Sizing and
drawdown are part of what is being researched, not a constraint handed down. An
agent that wants a rule derives one and defends it in `research/beliefs.md`.
**Also established:** the brokerage account is deliberate and currently holds no
money, so nothing is at stake while this is worked out.
**Still worth knowing, not blocking:** how much he intends to fund it with
eventually, since a rule that works at $1,000 and one that works at $100,000 are
different rules. No need to ask — it will become relevant on its own.

---

### 2026-09-12 — RESOLVED: Where does futures and prediction-market data come from?
**Answered:** 2026-09-12, by testing rather than by asking.
**Answer:** the open internet is fully reachable from this environment, and both
gaps are filled by free sources needing no API key — Yahoo Finance for futures
(`GC=F` returns COMEX gold with real bars), Kalshi for prediction markets.
Verified endpoints are in [`handoff.md`](handoff.md).
**Consequence:** the choice of which market to start with is now a research
decision rather than a tooling constraint, which was the point. Every market
named in the mission is reachable.
**Left open deliberately:** whether to pay for research-grade data later. Free
sources carry real limits — no delisted symbols, so survivorship bias is
unavoidable on any universe built from them. An agent that hits that wall should
say so rather than quietly working around it.

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
