---
description: Rebuild the company-value screen — undervalued, overvalued, worth watching
---

Rebuild the valuation screen and hand back the link.

```bash
export MASSIVE_API_KEY="..."        # never commit it; see scanner/massive.py
python3 scanner/value.py            # add --refresh once a week
python3 dashboard/value.py
```

Then republish `dashboard/value.html` with the `Artifact` tool, passing the
existing URL from `thoughts/handoff.md` as `url`. Commit `data/value.json` and
the rebuilt page.

## What the three lists are, and what they are not

- **Undervalued** — passed *every* quality gate (profitable, growing revenue,
  growing earnings, a real margin, tradable volume) **and then** priced below
  fair value. Ranked by price paid per unit of delivered growth.
- **Overvalued** — priced past the expensive line. Deliberately *not*
  quality-gated: a great company can be expensive, and the sheet shows which is
  which rather than hiding one.
- **Worth watching** — good businesses merely fairly priced, or cheap ones
  failing exactly one gate. The list of things that become interesting on a
  price fall or one better quarter.

**None of these is a recommendation.** A screen says where to look. Whether any
of it pays is a research question with an experiment behind it, not a reading of
this page. If he asks "should I buy one", that is `research/`, not this.

## The two numbers from his video that are NOT here, and why

He sent a video listing P/E, **Forward P/E** and **PEG**. Two of those are
forecasts, and forecasts are a paid product:

| | |
|---|---|
| **Forward P/E** | needs analysts' estimate of next year's earnings |
| **PEG** (as popularly defined) | needs analysts' estimated growth rate |

Checked 2026-09-23: Massive serves reported figures only on this plan and
answers "not entitled" for analyst insights; Yahoo's quote endpoints now refuse
anonymous requests; SEC EDGAR returns 403 from this container and carries only
actuals in any case.

**So the PEG on this page uses growth the company actually delivered.** Say that
plainly when reporting — it is a different number from the video's, and the
difference matters: delivered growth is a fact, forecast growth is an opinion
with a decimal point on it. Do not quietly present one as the other.

## Windows: never mix them

P/E is computed on the **trailing twelve months**. Growth is computed on the
**last two complete fiscal years**. Each window is internally consistent, and
they are reported as two different things because that is what they are.
Comparing a TTM figure against a fiscal year would be the same date-mixing
mistake already made once here between option and share volume.

## The trap this screen sets

**P/E divides by earnings.** A company earning a cent a share prints a P/E in
the thousands, which is not "expensive" — it is a rounding error in the
denominator. This is the same shape of mistake that has now bitten this
repository three times (`KNOWLEDGE.md`). `MIN_TTM_EPS` excludes marginal
earners from the rankings rather than letting them top the overvalued list.

Before trusting any new filter added here, ask what the list looks like if the
effect is absent. If it looks the same, the filter is supplying its own answer.

## What to tell him

Three or four names, in plain English: the company, what it earns, what you pay
for those earnings, and whether the business is growing. No jargon. Say which
trading session the prices are from — the data is end-of-day, so a morning run
describes yesterday's close.
