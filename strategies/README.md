# Strategy library

One file per source. Each is an **extraction**, not an endorsement: it records what
that source said, in its own terms, so that different approaches can be compared
on evidence rather than on how convincing they sounded.

**Published site:** https://claude.ai/code/artifact/d39ab618-439a-48aa-a40e-d3fe756ec966
Built by `dashboard/strategies.py`. One tab per file, plus a Compare tab that
pools every claim from every source into one table.

## Adding a transcript

Drop a new `.json` in this directory and rebuild — it appears as a tab with no
other change:

```bash
python3 dashboard/strategies.py
```

Then republish `dashboard/strategies.html` to the URL above.

## What goes in a file

Follow [`options-flow-gamma.json`](options-flow-gamma.json). The fields that
matter most:

| Field | Why it exists |
|---|---|
| `source` | Who said it, where, and what they claim as credentials. Attribution is part of the record. |
| `thesis` | The whole idea in one paragraph. |
| `mechanism` | The causal chain the source gives, step by step. This is what gets tested, not the conclusion. |
| `entry_rules` / `exit_rules` / `risk` / `timing` | The operational part — specific enough to code. |
| **`claims`** | **The important one.** Every factual or performance assertion, each with a `status`. |
| `data_inputs` | What a session needs in hand before it can test any of it. |
| `how_agents_should_test_this` | The concrete first experiments. |
| `blockers_here` | Why it cannot be tested in this environment yet, if it cannot. |

## The rule on claims

Every claim starts at **`untested`**. It moves only when an experiment in
[`research/experiments.md`](../research/experiments.md) says what happened, and
the entry cites that experiment id.

**Do not mark a claim tested because it sounds plausible, because the source is
credible, or because a chart looked like it.** The library is worth having only
if its status column means something — that is the whole mechanism for
eventually knowing which of several strategies actually works.

## Extraction, not commentary

Write down what the source said, including things that look wrong. A claim that
turns out to be false is a useful entry; a claim quietly omitted because an
agent doubted it is a hole nobody can see. Judgement belongs in the experiment
that tests it, not in the extraction.

Where a source states a number — a win rate, a volume share, a tick count —
record it as **their** figure, in the `claims` list, where it can be checked.
