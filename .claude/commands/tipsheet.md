---
description: Scan for unusual option volume and rebuild the tip sheet
---

Build the morning tip sheet: which names are seeing unusual option volume, at
the day, week and month horizon, and which contracts are driving it.

```bash
python3 scanner/tipsheet.py
python3 dashboard/tipsheet.py
```

The scanner pulls full option chains from CBOE for the universe in
`scanner/tipsheet.py`. It is unauthenticated and needs no broker session, so it
runs from a plain script and from a scheduled run.

Then republish `dashboard/tipsheet.html` with the `Artifact` tool. **Pass the
existing artifact URL as `url`** — it is recorded in `thoughts/handoff.md` —
so the owner keeps the same link. Commit both `data/tipsheet.json` and the
rebuilt page so the repository and the published page agree.

## Timing matters, and it changes what the sheet means

Open interest is published once, after the close, and does not move during the
session. Volume is same-day.

- **Run before the open** and the sheet describes the *previous* session.
- **Run during the session** and volume is partial but the ratio is live.
- **Run after the close** and it is the complete day against that morning's
  open interest, which is the cleanest read.

Say which of these it is when reporting, because the owner cannot tell from the
page alone.

## What to tell him

Two or three names, in plain English: the ticker, whether the money went into
calls or puts, roughly how far out, and how unusual it was against the open
interest already standing there. No jargon, and no number without its unit.

**Do not turn a listing into a recommendation.** This screen says where new
positioning showed up. It does not say the positioning is right, it does not say
the direction, and a large call buyer may be hedging a short somewhere the
screen cannot see. If he asks whether to follow one, that is a research
question — open an experiment, do not answer from the sheet.

## The two traps already hit here

Both were caused by a filter inventing the thing it was measuring. Check any new
filter against the same standard before trusting a ranking.

1. **Ratio against a floor.** The first version ranked everything by volume / open
   interest with a floor of 50 on the denominator. The top of the sheet became
   contracts with an open interest of 0 to 21, whose "816x" was volume divided by
   the floor. Contracts with real open interest (`build`) and contracts with
   almost none (`fresh`) are now separated and ranked differently.
2. **A flag that fires on everything.** The replacement flagged a ticker as
   mechanical when three deep-in-the-money strikes shared an expiry. It fired on
   11 of the top 15 names. It is now a direct test on the greeks CBOE already
   ships — delta pinned at 1 with no vega left means the contract carries no
   optionality and is a stock substitute — and those contracts are excluded from
   the ranking and reported separately.
