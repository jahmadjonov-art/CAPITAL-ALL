# Handoff

Durable knowledge for whoever works here next. Facts that took effort to
establish, and mistakes worth not repeating.

Add to this when you learn something a fresh session would otherwise have to
rediscover. Delete anything that stops being true — a stale warning here is
worse than none, because it will be trusted.

---

## Orientation

**This repository is being repurposed.** It used to hold one app; that app now
sits in `legacy/` and the root is clear for new work. As of this writing the new
project has not been specified yet, so anything at the root is scaffolding
rather than product.

**`legacy/` is a real, deployed application — not dead code.** It is the Capital
Allocation Manager, a budgeting PWA that splits trucking income across tax,
repair, capital and salary buckets. Do not modify it, refactor it, or build on
top of it unless explicitly asked. It was moved with `git mv`, so
`git log --follow` traces any file's full history through the move.

**Read `SCORECARD.md` before planning anything.** Its Standing Directives
section is binding — those lines were earned from the owner's ratings of earlier
phases. `./scorecard/summary.sh` gives the short version.

---

## Things that will bite you

### The Supabase database in `legacy/` is live, shared, and holds real money data

`legacy/frontend/src/config.js` points at a real Supabase project, and the
legacy README states that local development talks to **the same database as the
production site**. There is no separate dev instance.

So running the legacy app locally and clicking around is not a dry run — adding
or deleting a transaction there mutates the owner's actual business records.
Treat `legacy/supabase/schema.sql` the same way: it is the shape of a live
database, not a scratch file.

The committed anon key is fine and is meant to be public; row-level security is
what protects the rows. The `service_role` key must never enter this repo.

### `main` is untouched and is what deploys

The live site builds from `main` on every push. Work happens on a
`claude/...` branch. Nothing done on that branch affects production until it is
merged, which is the only reason the archiving work was safe to do at all.

One consequence to carry forward: the deploy workflow moved to
`legacy/.github/workflows/deploy.yml`, and GitHub only reads workflows from
`.github/workflows/` **at the repository root**. It is therefore inert on this
branch, by design. If this branch ever merges to `main`, the legacy app stops
auto-deploying. That was a deliberate choice, not an oversight — but confirm it
is still what the owner wants before merging.

### Git rename detection is pairing-based, and a new file at the old path breaks it

Encountered directly while archiving. All 29 files were moved with `git mv` and
`git status` cleanly reported 29 renames. Then a new `README.md` was written at
the repository root — and git immediately re-paired things, reporting
`M README.md` plus `A legacy/README.md` instead of the rename it had shown a
moment earlier.

Nothing was actually wrong; the archived file was byte-identical. But the status
output alone could support either conclusion, and the whole task had been framed
as *do not lose anything*.

**The lesson: do not read `git status` letters as proof of what happened to file
contents.** Renames are inferred at display time from similarity, not recorded.
When it matters, verify against the old commit directly:

```bash
git show HEAD:path/to/file | diff - new/path/to/file
```

That was done for all 29 files before committing. Do the same for any move that
would be expensive to get wrong.

---

## Environment

An ephemeral cloud container, reclaimed after the session ends — **anything not
committed and pushed is gone.** Node 22, Python 3.11, Bash 5.2 are available.
No `gh` CLI; GitHub work goes through the `mcp__github__*` tools.

---

## Working style that has landed well so far

Not yet confirmed by a score — treat as provisional until `SCORECARD.md` has
entries backing it.

- **Look before touching.** The owner's first instruction was to inventory the
  repository specifically so nothing got deleted by accident. Surveying first
  and reporting what is there has been welcome every time.
- **Name the risk without being asked.** The live-database warning and the
  workflow-path consequence were both volunteered, and neither was challenged.
- **Prefer reversible moves, and say how to reverse them.** Archiving instead of
  deleting, with the undo command written into the README, is the shape of thing
  that has gone over well.
- **Ask when an ambiguity is structural.** One clarifying question about how to
  archive cost a round trip and prevented building the wrong layout. See
  `2-judgment-calls.md` for when that trade is worth making.
