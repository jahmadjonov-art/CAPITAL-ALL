# Unknown

No defensible default was available. Either the question went back to the owner,
or a guess was made and is labelled here as a guess.

An open entry in this file is not a failure. It is a question that has not been
answered yet, parked where the next session can see it instead of rediscovering
it. **Close entries out as they get resolved** — record the answer and date it,
rather than deleting the entry, so the reasoning stays traceable.

Newest first.

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

### 2026-09-12 — OPEN: What is the new project?
**Situation:** the repository has been cleared and two support systems built,
for a project that has not been described yet.
**Unknown:** everything about it. Purpose, stack, audience, whether it relates
to the trucking business at all.
**Why it cannot be assumed:** the owner said the brief is coming after the
scaffolding is finished, so this is sequencing, not an oversight. But it means
no stack-dependent decision can be made yet, and at least one thing has already
been deferred because of it — the root `.gitignore`, in
`2-judgment-calls.md`.
**Deliberately not guessed:** no framework was installed, no directory layout
was invented, no `package.json` was written. Scaffolding a Next.js app on a hunch
because the previous occupant was React would have been fabrication dressed as
initiative, and unwinding a wrong stack costs more than waiting.
**Would resolve it:** the brief.
