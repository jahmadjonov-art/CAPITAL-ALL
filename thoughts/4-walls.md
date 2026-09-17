# Walls

Where work stopped. What the blocker actually was, and the reasoning about how
to get past it.

This file exists because a session that hits a wall and ends takes its
understanding of that wall with it. The next agent then walks into the same one,
spends the same hours, and stops in the same place. Writing the wall down is how
that stops happening.

**A wall is not a failure to report reluctantly.** It is the most useful thing a
stuck session can leave behind, and an honest one beats a vague claim of
progress every time. Being stuck and saying precisely where is a good outcome.

## What belongs here

- Hit a limit in the data, the tools, or the environment that blocked the work.
- Went several rounds on something and got nowhere.
- Found the answer but only after real effort — write the wall down anyway, with
  what got past it, so nobody pays that cost twice.
- Something is achievable but needs a decision, a credential, a data source or a
  budget that an agent cannot supply alone.

## What does not

A question you could have answered by reading a file. Check
[`handoff.md`](handoff.md) and the [research notes](../research/README.md)
first — if the wall is already recorded, add what you learned to the existing
entry rather than opening a new one.

## Format

Newest first. `RESOLVED` entries stay, with what cleared them.

```
### YYYY-MM-DD — OPEN | RESOLVED — Short title
**Goal:** what was being attempted
**Wall:** the precise point where it stopped — the error, the missing data,
          the ambiguity. Be specific enough that someone can verify it.
**Tried:** what was attempted before stopping, so nobody repeats it
**Why it is a wall:** why this is structural rather than a matter of trying harder
**Route through it:** the best current thinking on what would clear it,
          ranked by cost. Say which need the owner and which do not.
**Cost of leaving it:** what stays blocked while this stands
```

**`Route through it` is the field that matters.** A wall recorded without any
reasoning about how to get past it is just a complaint. Even a guess, labelled
as a guess, gives the next session somewhere to start.

---

### 2026-09-14 — OPEN, cause identified 2026-09-16 — A scheduled session could not push
**Goal:** the first autonomous weekday run, fired by the Routine at 15:10 UTC.
**Wall:** it did the work and **could not push to GitHub.** It made one commit,
`a2c8f4d` — the 31st on the branch — which never reached the remote. The
container was reclaimed and that commit no longer exists anywhere.
**How it was detected:** not by the session, which could not report it. A webhook
fired when it republished the office dashboard. The dashboard's build stamp read
commit `a2c8f4d`, 31 commits, while the remote was still at `bf1c2c5`, 30
commits. The gap was the whole story.
**Tried:** nothing at the time — this session was not running. Afterwards,
`git push` from a fresh session worked immediately and reported everything
up to date, so **the branch was never broken**; whatever failed was local to
that container.
**Why it is a wall:** it is silent. The session followed the loop correctly,
including rebuilding and republishing the dashboard as the last step, and that
step succeeded. Only the push failed. **A run can therefore look completely
successful from the outside and still leave nothing behind.**
**What was recovered, and how:** the dashboard is generated from the repository,
so the published HTML embedded a summary of the state at that commit — an
accidental backup. From it: a CBOE data source was found, a fifth belief written,
a second experiment run, a wall recorded, and the whiteboard rewritten. The
*finding* has since been re-established independently (see `B-005`). **The
session's own words are lost and are not recoverable.**
**Route through it, cheapest first:**
1. **Push earlier and more often.** The loop pushes once at the end, which is the
   single worst moment to discover the push is broken. Commit and push after each
   material step instead.
2. **Verify the push rather than assuming it.** `git ls-remote origin <branch>`
   after pushing, compared against local HEAD, turns a silent failure into a
   loud one the session can still act on.
3. **If the push fails, say so in the artifact.** The dashboard is the one
   channel that demonstrably still worked. A run that cannot push should
   republish with the failure stated on its face.
4. Diagnose the cause. Unknown — possibly credential scope in a fired session,
   possibly transient. A scheduled run that captures `git push` stderr into the
   dashboard would settle it next time.
**Cost of leaving it:** every scheduled run is a coin flip on whether its work
survives, and the failure is invisible. **Nothing the Routine produces can be
trusted to persist until this is fixed.**

---

**2026-09-16 — it happened a second time, and the likely cause is now named.**

The Routine fired at 15:10 UTC, ran seven minutes, and the platform recorded it
`SUCCEEDED`. The remote branch did not move: it was still at `24502a5`, the last
commit from the interactive session the day before. Two for two, both reported
as successes from outside.

Reading the Routine's own configuration (`list_triggers`) gives the candidate:

    "sources": []
    "mcp_connections": []

**The scheduled job was created with no repository attached to it.** An
interactive session has the repository attached and its git credentials scoped
to it — which is why `git push` works here and has worked 31 times. A fired
session with an empty `sources` list gets no such grant, so it can read the
public repository and clone it, do the work, commit locally, and fail at exactly
one step: the push. That matches every symptom, including the short run.

**Basis: Reasoned, not Tested.** The configuration is a fact read directly from
the platform, and the failure is a fact observed twice. That the first causes the
second is the obvious explanation and nothing else fits as well, but it has not
been demonstrated — no scheduled run has yet captured the actual error text from
`git push`, which is the thing that would settle it.

**The fix is the owner's, and it is a settings change, not a code change.** In
the Routines page on claude.ai, edit "Capital-All — weekday research run" and
attach the `capital-all` repository as a source. `update_trigger` cannot do it —
that tool reaches the name, schedule, enabled state, model and prompt, and not
the sources. Attaching the connectors in the same edit would also clear the
separate limitation in `handoff.md` about scheduled runs having no broker tools.

**2026-09-17 — tested directly, and it failed a third time.**

The owner changed a setting he believed gave scheduled runs write access, and
asked for a test. The Routine was fired manually at 12:38 UTC with an override
telling it to make one trivial edit, push immediately before doing anything
else, verify with `git ls-remote` rather than trusting the push's exit code, and
capture the stderr verbatim if it failed.

It ran 33 minutes, made five commits to `71356f2`, and the remote never moved
off `46bbfdb`. No new branch appeared either. **The error text was still not
recovered** — a cloud session's transcript is not readable from another session,
and it is not reachable by `SendMessage` (it is not on this machine), so the one
thing that would settle the cause remains out of reach from here.

What this does establish: **the setting the owner changed was not the one that
governs this.** The Routine's stored config still reads `sources: []` and its
`updated_at` is unchanged since 2026-09-12, so whatever he changed, it did not
reach this Routine. The hypothesis stands but is still unproven.

**To actually capture the error, the next attempt must write it somewhere that
survives the container.** The push is what fails, so the record cannot be a
commit. The one channel demonstrably still working is the Artifact tool. A run
told to put `git push` stderr *on the dashboard* would settle this in one shot.

**And a second failure mode showed up.** See
`thoughts/recovered/2026-09-17-lost-run.md`: the run rewrote `MISSION.md`,
narrowing the programme to "signals for a human trader, stocks and futures
only", and published that to the owner's office dashboard. The commit behind it
exists nowhere. For half an hour the owner's page showed a mission he had never
agreed to, under a footer promising nothing on it was invented.

**Until it is attached, do not schedule work whose only output is a commit.** The
mitigations already in place (push after every step, verify with `ls-remote`,
state the failure in the dashboard) make the failure loud, but a loud failure
still loses the work.
