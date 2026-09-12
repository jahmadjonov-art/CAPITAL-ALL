# CAPITAL-ALL

This repository is being repurposed for a new project. Work in progress.

## `legacy/`

The previous occupant — **Capital Allocation Manager**, a budgeting PWA for a
trucking business — now lives untouched in [`legacy/`](legacy/). It was moved,
not rewritten: every file is byte-identical to what it was, and `git log
--follow` still traces each one's full history.

Its own [`legacy/README.md`](legacy/README.md) documents how it works and how to
run it.

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
