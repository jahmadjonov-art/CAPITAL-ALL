# Judgment calls

More than one reasonable reading existed, nothing in the request settled it, and
work had to continue. An assumption got made and is recorded here.

**This is the file worth reading.** Every entry names the one thing that would
have removed the doubt. Where that field says the same kind of thing repeatedly,
that is a pattern in how work gets briefed, not a run of bad luck.

Newest first.

---

### 2026-09-12 — Built the thoughts system as five files rather than one
**Asked:** create a place for categorised thoughts, described out loud, plus a
way to pass knowledge to the next agent.
**Did:** a `thoughts/` directory — a README, a handoff file, and three category
files numbered by escalating uncertainty.
**Assumed:** "those files" meant genuinely separate files per category, and that
the knowledge-handoff belongs in its own document rather than mixed into the
categories, since it is distilled and durable while the categories are
per-decision and chronological.
**Would have settled it:** whether the categories should be separate files or
one file with three sections, and whether numbered filenames are wanted or just
clutter.
**If wrong:** cosmetic. Merging the three into one file is a five-minute change
and loses nothing.

Also assumed three categories exactly, since three were described. If the real
shape of the work needs a fourth — "did this without being asked", say — it
should be added rather than forced into an existing one.

---

### 2026-09-12 — Made the scorecard derive its averages instead of storing them
**Asked:** build a scoring system that persists and can be read later.
**Did:** entries are the only stored data; `summary.sh` recomputes averages and
trends from them on every run.
**Assumed:** a summary that can silently disagree with its underlying entries is
worse than no summary, so the redundancy is not worth the convenience.
**Would have settled it:** nothing — no reasonable person would have specified
this. Recording it because the reasoning is borrowed, not invented: the archived
app applies the identical rule to bucket balances, and matching the owner's own
established pattern seemed better than importing an outside one.
**If wrong:** trivial to change; the script is 90 lines and nothing depends on it.

---

### 2026-09-12 — Deliberately did not create a root `.gitignore`
**Asked:** nothing about ignore rules.
**Did:** left the root without one, and said so.
**Assumed:** better to write one that fits the actual stack than to guess at
`node_modules` and `dist` before knowing what gets built.
**Would have settled it:** what the new project is. That is the open question
behind several of these entries — see `3-unknown.md`.
**If wrong:** a build artefact could get committed before anyone notices. Low
cost, easily fixed, but **whoever starts the new project should write the
ignore file first.**

---

### 2026-09-12 — Moved `.github/` into `legacy/`, disabling the deploy workflow
**Asked:** move the old app out of the way. Nothing was said about CI.
**Did:** moved `.github/` along with everything else, then flagged the
consequence in the commit message, the root README, and the reply.
**Assumed:** the workflow belongs to the archived app, so leaving it at the root
would be worse — after a merge to `main` it would try to build a `frontend/`
that is no longer there and fail on every push.
**Would have settled it:** "should the old app keep deploying after we take
over the repo?" A yes/no.
**If wrong:** the live site stops updating after a merge to `main`. It does not
break — already-deployed files stay served — and moving one file back fixes it.
Nothing has merged yet, so nothing has happened yet.

This is the highest-consequence assumption made so far and the one most worth
overriding if it is wrong.

---

### 2026-09-12 — Wrote a root `README.md` that was not requested
**Asked:** put the old app aside.
**Did:** also added a root README explaining what `legacy/` is, that `main` is
untouched, and how to reverse the move.
**Assumed:** an empty repository root with one unexplained folder is a puzzle for
whoever opens it next, and the undo command is worth writing down at the moment
it is still fresh.
**Would have settled it:** nothing worth asking about. Logged because it is
scope that was added unprompted, and unrequested scope is exactly the kind of
thing that should be visible rather than quietly slipped in.
**If wrong:** delete one file.

---

### 2026-09-12 — Asked how to archive instead of picking a layout
**Asked:** "put away whatever's in here, kinda a little bit to the side where it
still exists, but it doesn't get in the way."
**Did:** established the safety net first — confirmed everything was already
preserved on `origin/main` — then asked which of three layouts was wanted, and
only then moved anything.
**Assumed:** "to the side but still exists" genuinely underdetermines the
result. A folder move, a cleared branch, and building alongside all satisfy that
sentence and produce visibly different repositories.
**Would have settled it:** naming the destination — "move it into a folder", or
"clear the branch, it's on main anyway".
**If wrong:** cost one round trip.

Worth stating the general rule this came from, since it will come up again:
**ask when the readings differ in what gets built, not merely in how.** Had the
question been how to name the folder, guessing and moving on would have been
right. The clarifying question is cheap; a wrong structural guess is discovered
late and costs more than the question saves.
