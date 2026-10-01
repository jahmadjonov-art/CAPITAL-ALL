# Zero to Quant — the mathematics course

A self-paced mathematics course that starts at counting and runs to the
mathematics used in quantitative finance, statistics and computing. Built for
the owner, published as a private artifact, progress saved against his account.

**Live page:** see `thoughts/handoff.md` for the current URL.

## What exists

| | |
|---|---|
| Curriculum map | 13 levels, 111 modules, **589 skills** — the whole route, written out |
| Practice built | **131 skills** (levels 0–3: counting → pre-algebra), unlimited generated questions |
| Lesson prose | 131 written lessons, about 7,800 words |
| Checks | 47,000+ generated questions validated per run, plus a real Chromium run |

Levels 4–12 are mapped in full and listed in the app as being written. Progress
is stored per skill id, so adding a level never disturbs existing progress.

## Layout

```
src/
  index.html      the page: title, design tokens, both themes, script tags
  mathcore.js     fractions, integers, an expression parser, maths typesetting
  curriculum.js   the whole map — levels, modules, skills, stable skill ids
  generators.js   one problem generator per skill
  grade.js        decides whether a typed answer is right
  engine.js       mastery levels, spaced review, unlocking, session building
  store.js        progress persistence (artifact db, localStorage fallback)
  app.js          views and interaction
  lessons/<module>.json   written lesson prose, keyed by skill id
tests/
  run.sh          every suite; run this before publishing
```

## The rules that keep it honest

**Skill ids are permanent.** Progress is keyed on them. Rename a skill's title
freely; never change its id, and never reuse one.

**A skill is practisable when `generators.js` has an entry under its id.** The
app derives that itself, so there is no "built" flag to keep in sync. A skill
with no generator shows as *being written* and is skipped by every session.

**A generator returns a question and its full working.** Signature
`fn(R, d) -> question`, where `R` is a seeded random source and `d` is a
difficulty tier (1–3). Shape:

```js
{ prompt, kind, answer, solution: [...],
  choices?, fields?, lowest?, tol?, unit?, requireFactored?, answerAlt? }
```

`kind` is one of `num`, `frac`, `mc`, `expr`, `text`, `multi`. Grading is by
value, not spelling: `expr` answers are checked by sampling both expressions at
random points, so any correct rearrangement is accepted.

**Maths is delimited by `~tildes~`, not dollars**, because prices appear
throughout and `$12.50` has to survive as text. Inside a segment: `\f{a}{b}` for
a stacked fraction, `^{}` and `_{}`, `sqrt{}`, and backslash words such as
`\in`, `\le`, `\sum` for symbols that would otherwise collide with English.

**Every generator is exercised 360 times before it ships** — `tests/run.sh`
round-trips each one's own stated answer through the real grader and rejects
unbalanced delimiters, duplicate multiple-choice options, missing working, and
currency that has landed inside maths markup. Two content bugs and four code
bugs were caught this way during the first build; do not skip it.

## Adding a level

1. Write the generators in `generators.js` under the ids already in
   `curriculum.js`. Nothing else needs touching for practice to appear.
2. Write `lessons/<module>.json` — one entry per skill, with `why` (the
   intuition, not the procedure), optional `sections`, `traps`, and `code` where
   a programming parallel genuinely helps.
3. Run `tests/run.sh`.
4. Republish the artifact to the **same URL** (see `handoff.md`) so progress and
   the link survive.

Write for someone who is not a programmer and wants to understand, not be
impressed: plain English, no unexplained jargon, and say why a rule is true
rather than asserting it.
