# Data collection

**Status:** OPEN
**Opened:** 2026-09-12

## The goal

A pipeline that records market data continuously, so that research runs against
an accumulating history this programme owns rather than whatever a vendor will
hand back today.

## Why it matters

Every free source here returns **current** data. Ask Kalshi for an order book
and you get this moment; there is no way to ask what the book looked like last
Tuesday. So questions like *"how wide is this spread usually?"* or *"does this
contract drift before settlement?"* are unanswerable today and will stay
unanswerable until something starts writing snapshots down.

This is also the only route to a genuine out-of-sample test. Data we recorded
ourselves, after a hypothesis was written, cannot have been fitted to — which
is a stronger guarantee than any holdout carved out of a historical file.

## What is already known

- **Agent sessions are the wrong tool for this.** Waking a language model every
  fifteen minutes to write down a number is absurdly expensive for what it
  produces. Collection should be a plain script.
- **The likely right shape is a GitHub Actions cron.** The repository already
  proves Actions work here (the archived deploy workflow), it runs free on
  GitHub's infrastructure, it needs no container of ours to stay alive, and it
  can commit straight back to the repo.
- **Two real constraints on that route**, both worth knowing before starting:
  1. Scheduled workflows only fire on the **default branch**. Our work lives on
     `claude/greeting-jk8c0j`, so a collector does nothing until something is
     merged to `main` — which is the owner's call, not an agent's.
  2. Workflows are only read from `.github/workflows/` at the **repository
     root**. That directory is currently inside `legacy/`, so it would have to
     come back out.
- **Scheduled Actions are not punctual.** GitHub delays cron under load,
  sometimes by many minutes, and can skip runs entirely. Any analysis must read
  the timestamp actually recorded rather than assuming the cadence held.

## What is missing

- What to capture. Kalshi order books for a chosen series and crypto prices are
  the obvious first candidates, since both run 24/7 and neither needs the broker.
- Cadence, traded against repository size. A snapshot every 5 minutes is ~105k
  rows a year per series; that is fine as compressed daily files and unpleasant
  as one commit per snapshot.
- Storage shape. Append-only daily files (`data/YYYY-MM-DD.jsonl.gz`) are the
  obvious answer, but nothing has been decided.
- A decision from the owner on merging to `main`.

## How you would know it is done

A question about the past — "what was the typical spread on this contract last
week?" — can be answered from the repository without calling any API.

## Notes from whoever has been here

- **2026-09-12** — Opened, not started. The idea surfaced from the owner asking
  whether agents could "run and learn and collect data". They can research on a
  schedule already, but **collecting a time series is a different problem** and
  the honest answer is that nothing here records anything yet.
