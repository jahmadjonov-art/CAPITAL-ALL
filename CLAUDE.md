# Working in this repository

## Before you start: read the scorecard

[`SCORECARD.md`](SCORECARD.md) is a running record of how the owner of this
repository rated previous phases of work, and what he wanted differently. Read
it at the start of every session, before planning or writing anything.

**[Standing Directives](SCORECARD.md#standing-directives) is the part that
changes what you do.** It is the accumulated preferences distilled from every
score so far — treat those lines as binding instructions, not background
reading. The scored entries below them are the evidence for where each one came
from, and are worth reading when a directive's reasoning isn't obvious.

For a quick orientation before the full read:

```bash
./scorecard/summary.sh
```

## When you are given a score

The owner scores a phase when he has run it and formed an opinion. Scoring is
his call and happens whenever he feels like it — never solicit a score, never
score your own work, and never write an entry he did not give you.

When he does give one:

1. Append an entry to the **Log** in `SCORECARD.md`, newest first, using the
   template at the top of that section.
2. Record his words about what worked and what missed. Quote him where the
   phrasing carries the point. Do not soften a low score, do not editorialize,
   and do not argue with the rating in the record — if you disagree, say so to
   him in conversation and leave the entry honest.
3. If the feedback implies a lasting preference rather than a one-off note, add
   or revise a line under **Standing Directives**, and cite the phase it came
   from. A directive that contradicts an older one replaces it — edit the old
   line rather than letting both stand.
4. Commit the entry on its own, so the record is easy to follow later.

## A note on what the scorecard is for

Its value is entirely in whether it changes behaviour. A log nobody acts on is
just bookkeeping. When a directive applies to what you are about to build,
follow it; when one is genuinely wrong for the task at hand, say so out loud and
explain why, rather than quietly ignoring it.

## Repository layout

- `SCORECARD.md` — the performance record. Source of truth.
- `scorecard/summary.sh` — derives statistics from that record on demand.
- `legacy/` — the previous occupant, a trucking budget PWA. Archived, not in
  use. Do not modify it or build on it unless explicitly asked.
