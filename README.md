# CAPITAL-ALL

This repository is being repurposed for a new project. Work in progress.

## The records kept here

Work in this repo is done largely by AI agents, and agent sessions do not share
memory between them. Two records exist in the repository itself so that each
session starts from what the last one learned, rather than from nothing.

| | |
|---|---|
| [`SCORECARD.md`](SCORECARD.md) | How the owner rated each phase, out of 10, and the standing directives drawn from those ratings. Run [`./scorecard/summary.sh`](scorecard/summary.sh) for the short version. |
| [`thoughts/`](thoughts/README.md) | A message board. What previous agents learned, and a categorised record of the decisions they made — split by how confident they actually were. |
| [`CLAUDE.md`](CLAUDE.md) | The protocol agents follow for both of the above. |

**If you are picking this repo up — human or agent — start with
[`thoughts/handoff.md`](thoughts/handoff.md).** It is short and it holds the
traps, including one about a live production database.

**If you want to brief the work better,** read
[`thoughts/2-judgment-calls.md`](thoughts/2-judgment-calls.md). Every entry
names the one question that would have removed an agent's doubt, which is a more
practical guide to what was missing from a request than any amount of general
advice about prompting.

## `legacy/`

The previous occupant — **Capital Allocation Manager**, a budgeting PWA for a
trucking business — now lives untouched in [`legacy/`](legacy/). It was moved,
not rewritten: every file is byte-identical to what it was, and `git log
--follow` still traces each one's full history.

Its own [`legacy/README.md`](legacy/README.md) documents how it works and how to
run it — but read the database warning in
[`thoughts/handoff.md`](thoughts/handoff.md) first. Local development talks to
the same live Supabase project as the production site.

### It is still live

`main` has not been touched, so the deployed site at
<https://jahmadjonov-art.github.io/CAPITAL-ALL/> and its Supabase database keep
working exactly as before. Note that `legacy/.github/workflows/deploy.yml` is no
longer at the path GitHub reads workflows from — that only takes effect if this
branch is ever merged to `main`, at which point the old app stops auto-deploying.

### Putting it back

```bash
git mv legacy/* legacy/.github legacy/.gitignore . && rmdir legacy
```
