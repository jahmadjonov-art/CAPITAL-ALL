# scanner

Screens that go looking for something across many names at once, as opposed to
`research/`, which tests one stated hypothesis at a time.

| Script | What it does |
|---|---|
| `tipsheet.py` | Unusual option volume across a 70-name universe, from CBOE, split day / week / month. Writes `data/tipsheet.json`. |

Run it with `/tipsheet`, which also rebuilds and republishes the page.

## The standard a screen has to meet here

A screen ranks things, and a ranking is easy to fake without noticing. Two
rankings in a row on this one turned out to be artifacts of their own filters —
the details are in `thoughts/handoff.md` and the reasoning in
`thoughts/2-judgment-calls.md`.

Before trusting a new filter, ask **what the output looks like if the effect it
is testing for is absent.** If the answer is "much the same", the filter is
supplying its own result. Two specific forms to watch for:

- **A floor becoming the denominator.** If a ratio is computed against a
  clamped minimum, the top of the ranking is the clamp.
- **A flag that fires on nearly everything.** That is a constant wearing a
  measurement's clothes.

Prefer testing a property directly on data the source already gives you over
inferring it. CBOE ships greeks per contract, which is why the current filter
can ask "does this contract have any optionality left" instead of guessing from
how far in the money the strike is.

Use `--cache DIR` while tuning. It saves and reuses the raw chains so an
iteration costs one fetch instead of seventy.
