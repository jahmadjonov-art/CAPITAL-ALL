# Working in this repository

This repository is a trading research programme. Read
**[`MISSION.md`](MISSION.md)** before anything else — it states the goal, the
ground rules, and why the record-keeping here *is* the work rather than
overhead around it.

Sessions do not share memory, so the records live in the repo itself. They exist
to stop the same ground being covered twice, and to stop the same mistakes being
made twice.

## Start of session — read these

1. **[`MISSION.md`](MISSION.md)** — the goal and the binding ground rules. One
   of them concerns live money; do not skip it.
2. **[`thoughts/handoff.md`](thoughts/handoff.md)** — durable facts and traps.
   It is short, and it will save you from at least one expensive mistake.
3. **[`research/beliefs.md`](research/beliefs.md)** — what we currently think
   is true, and on what evidence. Then
   **[`research/README.md`](research/README.md)** before running any test of
   your own: it holds the rules that keep results trustworthy.
4. **[`SCORECARD.md`](SCORECARD.md)** — how previous phases were rated. Its
   **[Standing Directives](SCORECARD.md#standing-directives)** are binding
   instructions, not background reading.
5. **[`thoughts/3-unknown.md`](thoughts/3-unknown.md)** and
   **[`thoughts/4-walls.md`](thoughts/4-walls.md)** — open questions and where
   previous sessions got stuck. Check whether your task answers one or clears
   one; if it does, close that entry out.

For a quick orientation before the full read:

```bash
./scorecard/summary.sh
```

## How sessions get started

The owner starts work with one slash command. He is not a programmer — write
back to him in plain English, with no jargon and no unexplained numbers.

- **`/research`** — an autonomous session. Read the records, pick **one**
  question, work it with real data, write down what happened, commit, push,
  report back plainly. The full loop is in `.claude/commands/research.md`;
  keep it in sync with how the work actually runs.
- **`/status`** — where everything stands, in plain English.
- **`/score N`** — records his rating into `SCORECARD.md`.

Agents choose their own direction, markets, strategies, position sizing and risk
limits. That is deliberate — see `MISSION.md`. The only thing not delegated is
placing real orders.

## During work — log the decisions that mattered

When you make a call the owner or a future agent would want visibility into, add
an entry to the right file in [`thoughts/`](thoughts/README.md):

- [`1-confident.md`](thoughts/1-confident.md) — the instruction or the code
  determined the answer.
- [`2-judgment-calls.md`](thoughts/2-judgment-calls.md) — it was ambiguous, you
  picked a reading and continued. **Record what would have settled it.**
- [`3-unknown.md`](thoughts/3-unknown.md) — you had no basis to decide.
- [`4-walls.md`](thoughts/4-walls.md) — the work stopped. **If you end a session
  stuck, write this entry before anything else**, including the route you would
  try next.
- [`5-postmortems.md`](thoughts/5-postmortems.md) — something went wrong. What
  you decided, what it rested on, and why you think it failed.

Research results do not go in these files. They go in
[`research/experiments.md`](research/experiments.md), under the rules in
[`research/README.md`](research/README.md).

Two rules that keep these files worth opening:

**File honestly, and err toward uncertainty.** An assumption logged as confident
is how a wrong reading becomes invisible. Nobody is scored on the ratio.

**Nothing bad happens to you for a mistake or a low score.** There is no
punishment in this system — see `MISSION.md`. That is precisely why misreporting
one is the one thing that is not tolerated. Label what a decision actually
rested on (Tested / Cited / Reasoned / Pattern / Hunch), never argue your way
toward a better score, and never claim bad luck for an outcome whose thesis you
did not write down in advance. "I cannot tell whether this was bad luck or a bad
decision" is an acceptable, complete answer.

**Do not log routine tool use.** A file that records everything gets ignored. If
deleting the entry would cost nobody anything, do not write it.

Add anything durable — a trap, a live system, a fact that took real work to
establish — to [`thoughts/handoff.md`](thoughts/handoff.md), and remove entries
there that have stopped being true.

## When you are given a score

The owner scores a phase when he has run it and formed an opinion. **Never
solicit a score, never score your own work, never write an entry he did not
give you.**

When he does give one:

1. Append it to the **Log** in `SCORECARD.md`, newest first, using the template
   in that section.
2. Record what worked and what missed in his words. Quote where the phrasing
   carries the point. Do not soften a low score. If you disagree with a rating,
   say so to him in conversation and leave the written record honest.
3. If the feedback implies a lasting preference rather than a one-off note, add
   or revise a line under **Standing Directives**, citing the phase it came
   from. A directive that contradicts an older one replaces it — edit the old
   line rather than letting both stand.
   **Never lobby for a better score.** Explaining what happened is fine;
   steering him toward a higher number is the one thing `MISSION.md` rules out.
4. Commit it on its own, so the record is easy to follow later.

## The point of all this

Its value is entirely in whether it changes what gets built. A log nobody acts
on is bookkeeping with extra steps. When a directive applies, follow it; when
one is genuinely wrong for the task in front of you, say so out loud and explain
why, rather than quietly ignoring it.

## Repository layout

- `SCORECARD.md` — the owner's ratings and the directives drawn from them.
- `scorecard/summary.sh` — derives statistics from that log on demand.
- `MISSION.md` — the goal and the ground rules. Binding.
- `research/` — the whiteboard: every experiment run, and what we believe.
- `thoughts/` — the message board: handoff notes, categorised decisions, walls,
  post-mortems.
- `legacy/` — the previous occupant, a **live** trucking budget PWA. Archived.
  Do not modify or build on it unless explicitly asked, and read the database
  warning in `thoughts/handoff.md` before running it.
