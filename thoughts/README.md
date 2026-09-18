# Thoughts

A message board between whoever is working in this repository and whoever works
in it next — including the owner, who can read it to see where his instructions
landed clearly and where they left an agent guessing.

Sessions do not share memory. Without something like this, every agent rebuilds
the same understanding from scratch and repeats the same misreadings. These
files are where that understanding gets left behind on purpose.

These are the **detail layer**. The front page is [`KNOWLEDGE.md`](../KNOWLEDGE.md),
which a session reads first and which points here when it needs to. Write for a
reader who arrives by pointer, not for one reading front to back.

## The files

| File | What goes in it |
|---|---|
| [`handoff.md`](handoff.md) | Durable facts and hard-won lessons for the next agent. **A new session should read this first.** |
| [`1-confident.md`](1-confident.md) | The ask was clear, the path was obvious, the work got done. |
| [`2-judgment-calls.md`](2-judgment-calls.md) | The ask was ambiguous. Something had to be produced anyway, so an assumption got made and the work continued. |
| [`3-unknown.md`](3-unknown.md) | No real basis to decide. Either the question went back to the owner, or a guess was made and labelled as one. |
| [`4-walls.md`](4-walls.md) | Work stopped. Where it stopped, what was tried, and the reasoning on what would get past it. |
| [`5-postmortems.md`](5-postmortems.md) | Something went wrong. What was decided, what it rested on, and — honestly — why it went wrong. **Nobody is punished for anything in here.** |

**If you are the owner and only read one, read
[`2-judgment-calls.md`](2-judgment-calls.md).** Every entry there names the one
thing that would have removed the doubt. That list is the practical answer to
"how do I brief this better next time" — and often the answer is not "write more",
it is "say which of two things you meant" or "point at the file you have in mind".

## Which category an entry belongs in

The line between them is **what the decision rested on**, not how hard the task
was or how well it turned out:

- **Confident** — the instruction, the code, or an established convention
  determined the answer. Another competent agent given the same input would land
  in the same place.
- **Judgment call** — more than one reasonable reading existed and nothing in the
  request settled it. A choice got made and the work proceeded. This is the
  category that matters, because it is where silent divergence starts.
- **Unknown** — not even a defensible default was available. Guessing here would
  have been fabrication.

**Post-mortems and walls are not further rungs on that ladder** — both are
different axes. A wall is work that could not continue; a post-mortem is an
accounting of a decision that turned out badly. Neither carries a penalty, and
the post-mortem file explains why that absence is what makes it trustworthy.

**Walls are not a fourth rung on that ladder** — they are a different axis. The
first three describe what a decision rested on; a wall describes work that could
not continue at all. An agent that ends a session stuck should leave an entry in
`4-walls.md` before anything else, because that is the one another session most
directly inherits.

When an entry sits between two categories, file it in the more uncertain one.
Overstating confidence is the failure mode that costs something; understating it
just adds a line to a file.

## An honest caveat about these files

These are self-reports, written by the same agent whose reasoning they describe,
usually just after the fact. They are not a verified trace of what actually
happened inside the model, and an agent's account of why it did something can be
a plausible reconstruction rather than a true cause.

So the format deliberately favours things that can be checked from the outside —
what was assumed, what was verified and how, what was left unchecked, what would
break if the assumption was wrong — over claims about inner experience. Read an
entry as *what the agent acted as if it believed*. That is the part that is
useful, and it is the part that can be audited against the diff.

## What to log, and what not to

Log a decision a future agent or the owner would want to know about: an
assumption, a road not taken, a trap avoided, a mistake made.

Do not log routine tool use. A file that records everything gets skimmed and
then ignored, which is worse than not having it, because it looks maintained.
Roughly: if removing the entry would cost nobody anything, it should not be
written.

## Entry format

Newest first in every file. Keep entries short.

```
### YYYY-MM-DD — Short title
**Asked:** what the request actually was
**Did:** what was built or decided
**Assumed:** the reading that was chosen        (judgment calls / unknowns)
**Would have settled it:** the specific question or fact that was missing
**If wrong:** what breaks, and how hard it is to undo
```

`Would have settled it` is the field the owner gets value from. Make it a
concrete, answerable question — "which of these two layouts did you mean",
"is this data live" — never a vague wish for more detail.
