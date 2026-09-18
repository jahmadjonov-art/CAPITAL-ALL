# CAPITAL-ALL

A trading research programme — futures, equities, options and prediction
markets. The goal is to make money; the method is an accumulating research
record that each session builds on rather than starting over.

**Start with [`KNOWLEDGE.md`](KNOWLEDGE.md)** — one page, capped at 150 lines,
holding what we know, what is dead, and what is being worked on right now. It is
deliberately short so that catching up never means reading the whole archive.

Then [`MISSION.md`](MISSION.md) for the goal, the ground rules, and the
reasoning behind the discipline the research follows.

Agents work in a small hierarchy. A session that gets stuck or wants a second
opinion calls a specialist — a **skeptic** that tries to break a finding, a
**quant** that runs the numbers, a **scout** that researches the open internet.
They are defined in [`.claude/agents/`](.claude/agents/).

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
| [`KNOWLEDGE.md`](KNOWLEDGE.md) | The front page. What we know, what is dead, what is live. Size-capped on purpose: the archive grows, this does not. |
| [`research/`](research/README.md) | The whiteboard. [`experiments.md`](research/experiments.md) is an append-only log of everything tried; [`beliefs.md`](research/beliefs.md) is what we currently think is true and why. |
| [`sandbox/`](sandbox/README.md) | Ground staked out but not built on. Anyone may pick one up. Leaving work open is expected, not a failure. |
| [`SCORECARD.md`](SCORECARD.md) | How the owner rated each phase, out of 10, and the standing directives drawn from those ratings. Run [`./scorecard/summary.sh`](scorecard/summary.sh) for the short version. |
| [`thoughts/`](thoughts/README.md) | A message board. What previous agents learned, decisions split by how confident they actually were, where sessions got stuck, and honest post-mortems when something went wrong. |
| [`CLAUDE.md`](CLAUDE.md) | The protocol agents follow for both of the above. |

**If you are picking this repo up — human or agent — start with
[`thoughts/handoff.md`](thoughts/handoff.md).** It is short and it holds the
traps, including one about a live production database.

**Reasoning is heard before work is judged, and honest mistakes are never
punished.** That is deliberate: punish an agent for an honest wrong answer and
you have not taught it to be right, you have taught it to avoid punishment — and
the cheapest way to do that is a better story, not better work. The other half
of the deal is that no agent may talk its way to a better score. See
[`MISSION.md`](MISSION.md).

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
