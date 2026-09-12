# CAPITAL-ALL

A trading research programme — futures, equities, options and prediction
markets. The goal is to make money; the method is an accumulating research
record that each session builds on rather than starting over.

**Start with [`MISSION.md`](MISSION.md).** It states the goal, the ground rules,
and the reasoning behind the discipline the research follows.

## Starting a session

| Command | What it does |
|---|---|
| **`/research`** | Boots an autonomous research session. Picks up where the last one left off, does the work, writes down what it found, and reports back in plain English. |
| **`/status`** | Where everything stands right now. |
| **`/score N`** | Records your rating of recent work, 1–10. |

⚠️ A live Robinhood brokerage account is connected — deliberately, and currently
unfunded. Agents research freely and choose their own markets, strategies and
risk; **no agent places a real order** until that is authorised in writing. See
[`thoughts/handoff.md`](thoughts/handoff.md).

## The records kept here

Work in this repo is done largely by AI agents, and agent sessions do not share
memory between them. Two records exist in the repository itself so that each
session starts from what the last one learned, rather than from nothing.

| | |
|---|---|
| [`research/`](research/README.md) | The whiteboard. [`experiments.md`](research/experiments.md) is an append-only log of everything tried; [`beliefs.md`](research/beliefs.md) is what we currently think is true and why. |
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
