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

### 2026-09-14 — OPEN — A scheduled session could not push, and its work is gone
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
