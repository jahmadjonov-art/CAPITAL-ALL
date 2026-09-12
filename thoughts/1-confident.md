# Confident

The instruction, the code, or an established convention determined the answer.
Another competent agent given the same input should land in the same place.

Newest first. Kept brief on purpose — these entries exist to give the other two
files a baseline to contrast against, not because each one is interesting.

---

### 2026-09-12 — Sent both findings to specialists before recording either
**Asked:** run a research session.
**Did:** audited the funded account, then handed the two claims that came out of
it to a `skeptic` and a `scout` rather than writing them down.
**If wrong:** nothing — verification is cheap and both came back changed.

Both returned corrections. The skeptic wounded a data-quality claim that was
over-broad in exactly the way that would have cost a future session a working
data source. The scout undermined a hunch this repository had already written
down about prediction markets, then **corrected its own report unprompted** when
its series survey turned out to have undercounted — in a direction that weakened
its own headline finding.

Recording this in the confident file because the decision was not a close call:
the rule says call the skeptic before believing anything, and the rule paid for
itself twice in the first session.

---

### 2026-09-12 — Inventory the repository before changing anything
**Asked:** look at what is in the repo so nothing gets deleted by accident.
**Did:** read every tracked file (29 of them), then reported the app's purpose,
its four database tables, the allocation logic, and the branch state.
**If wrong:** nothing — read-only.

Small enough to read exhaustively rather than sample, which is the right call
whenever the repo is this size. Two things surfaced that the owner had not asked
about but needed to know: the live shared database, and the committed anon key
being safe by design. Both are now in `handoff.md`.

---

### 2026-09-12 — Perform the archive move with `git mv`
**Asked:** move the existing app out of the way, having already settled on a
`legacy/` folder.
**Did:** `git mv` for all 29 files, verified each against `HEAD` byte-for-byte,
committed, pushed.
**If wrong:** fully reversible; the undo command is in the root `README.md`.

No ambiguity left once the layout was chosen. Worth noting that the *execution*
being obvious is exactly why the verification step mattered — see the rename
trap in `handoff.md`.
