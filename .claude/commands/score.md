---
description: Record the owner's score for a phase of work (1-10, 10 best)
---

The owner is scoring recent work. His rating and any comments are in
`$ARGUMENTS` — if that is empty or unclear, ask him for the number and what
prompted it, then continue.

Follow the procedure in `CLAUDE.md`:

1. Append an entry to the **Log** in `SCORECARD.md`, newest first, using the
   template in that section. Include the date and the current commit hash.
2. Record what worked and what missed **in his words**. Quote him where the
   phrasing carries the point.
3. If the feedback implies a lasting preference rather than a one-off note, add
   or revise a line under **Standing Directives**, citing the phase it came
   from. If it contradicts an existing directive, rewrite that line rather than
   leaving both standing.
4. Commit the entry on its own and push.

Then confirm briefly what you recorded and what changed as a result.

**Do not soften a low score, and do not pad a high one.** If you think a rating
is wrong, say so to him here in conversation — and still write the entry as he
gave it. The log is his, not yours.

**Do not lobby.** Explaining what actually happened is fine and often useful.
Steering him toward a higher number is not, and neither is reaching for "the
reasoning was sound, the market just moved" unless that thesis was written down
before the outcome was known. See the rule in `MISSION.md`.

A low score carries no penalty for anyone. If it came from a real mistake, the
useful response is a post-mortem in `thoughts/5-postmortems.md`, not a
negotiation.

Never write an entry he did not give you. Never score your own work.
