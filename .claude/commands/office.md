---
description: Rebuild the office floor plan and hand back the link
---

Rebuild the dashboard from the repository's current state and give the owner the
link.

```bash
python3 dashboard/build.py
```

Then republish `dashboard/office.html` with the `Artifact` tool. **Pass the
existing artifact URL as `url`** so it updates in place and the owner keeps the
same link — the URL is recorded in `thoughts/handoff.md`. Publishing without it
creates a second artifact and splits his bookmark from the live page.

Commit the rebuilt file so the repository and the published page agree.

Then tell him in one or two lines what changed on it since last time — a new
belief on the whiteboard, a plot closed, a desk added, a score recorded. If
nothing changed, say that plainly rather than dressing it up.

**Never hand-edit `dashboard/office.html`.** It is generated. Every figure on it
is read from the markdown at build time, which is the only reason the numbers on
it can be trusted — edit the source and rebuild.
