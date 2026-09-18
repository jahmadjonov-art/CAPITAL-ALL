---
description: Rebuild the office floor plan and hand back the link
---

Rebuild the dashboard from the repository's current state and give the owner the
link.

```bash
python3 dashboard/build.py
```

Commit the rebuilt file and push it to `main`. **That is what publishes it** —
`.github/workflows/deploy.yml` rebuilds the whole site on every push, so the page
is live at

> https://jahmadjonov-art.github.io/CAPITAL-ALL/office/floor-plan/

a minute or two later. Check the run actually went green before telling him it is
up (`gh run list --workflow deploy.yml --limit 1`).

The site publishes the **committed** `dashboard/*.html`, so a rebuild that is
never committed changes nothing the owner can see.

The five claude.ai artifacts recorded in `thoughts/handoff.md` are frozen
snapshots from before the site existed. Do not republish them by default — one
address that is always current beats five that may disagree. Republish only if he
asks for the old link.

Then tell him in one or two lines what changed on it since last time — a new
belief on the whiteboard, a plot closed, a desk added, a score recorded. If
nothing changed, say that plainly rather than dressing it up.

**Never hand-edit `dashboard/office.html`.** It is generated. Every figure on it
is read from the markdown at build time, which is the only reason the numbers on
it can be trusted — edit the source and rebuild.
