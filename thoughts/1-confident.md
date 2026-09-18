# Confident

The instruction, the code, or an established convention determined the answer.
Another competent agent given the same input should land in the same place.

Newest first. Kept brief on purpose — these entries exist to give the other two
files a baseline to contrast against, not because each one is interesting.

---

### 2026-09-18 — One workflow builds both sites, not two
**Asked:** publish everything the firm has built as a free website.
**Did:** folded `deploy-legacy.yml` into a single `.github/workflows/deploy.yml`
that builds the trucking app *and* the research site and uploads them as one
Pages artifact.
**If wrong:** the site that deployed second silently replaces the first.

Not a close call: a GitHub Pages deployment replaces the whole site at once, and
there is one Pages site per repository. Two workflows each uploading their own
artifact would have looked correct, passed their own checks, and left whichever
finished first overwritten. Verified rather than assumed — the app built through
the new workflow produces the same asset hashes the live site was already
serving.

---

### 2026-09-18 — Changed the trucking app's service worker, with permission first
**Asked:** put the research site at the same address as the live app.
**Did:** asked the owner before touching `legacy/`, explained the clash in plain
English, and added `ownedByApp()` to `legacy/frontend/public/sw.js` once he chose
that over a second web address.
**If wrong:** reverting is one function; the cache name is unchanged.

`handoff.md` forbids modifying `legacy/` unless explicitly asked, so the only
correct move was to ask. Worth recording that the clash was a **pre-existing
bug**, not one the research site introduced: the worker cached every page it saw
under the single shell key, so any 404 under `/CAPITAL-ALL/` could already leave
the app opening on the wrong page with no signal. The research site would merely
have made it happen reliably.

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
