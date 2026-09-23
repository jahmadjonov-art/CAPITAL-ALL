# A rating that combines value with news and trend

**Status:** OPEN — staked out 2026-09-23, nothing built.

## What should exist

The value screen answers one question: *is this company cheap against what it
earns?* That is a fact about the past. The owner wants a second rating on top of
it, answering a different question: *given where the economy and the news are
pointing, is this company positioned well?*

His words: *"the agents will look at the news, look at the trend, look at the
value, and then it will have its own another rating system where it will say,
based on the trend, based on the news, where the economy's headed, these
companies are positioned well for that, and they're undervalued or overvalued."*

So: **value × positioning**, with the two kept visibly separate. A cheap company
badly positioned and a dear one well positioned are different things and the
page should never blend them into one number that hides which is which.

## Why it matters

The value screen's own disclaimer is the argument for this: *a stock is usually
cheap for a reason, and finding the reason is the work this page does not do.*
That reason is almost always in the news, the filings, or the direction of the
industry. A screen that could read those would be answering the question the
current one deliberately refuses.

## What is already known

- **The value layer works** — `scanner/value.py`, ~1,400 companies, refreshed
  from cached financials. Positioning is a column to add, not a rebuild.
- **The container has open internet access** (`scout` agent, `WebSearch`,
  `WebFetch`), so news can be read today without any new subscription.
- **Massive serves no news on this plan** — `/benzinga/*` returns "not entitled".
- **X/Twitter's API is paid**, and its free tier has been effectively closed to
  this kind of use since 2023. Do not assume it is available; price it first.
- **The rate limit is about 4 requests a minute** — any per-company news fetch
  across 1,400 names has to be batched or narrowed to a shortlist.

## What is missing

1. **A news source with an actual licence.** Candidates worth pricing: the SEC's
   own filing feed (free, and 403 from this container — check whether that is
   the proxy or the IP), an aggregator with a free tier, or a paid add-on.
   Write down the cost before building on any of them.
2. **A definition of "positioned well" that can be falsified.** This is the hard
   part and the reason this is a sandbox rather than a task. "The AI reads the
   news and says it looks good" is not a rating — it is a sentence that cannot
   be wrong. A usable definition has to state in advance what would make it
   incorrect, per `research/README.md`.
3. **A pre-registered test.** The obvious one: record the rating, wait, and
   check whether the well-positioned names outperform the badly-positioned ones.
   That takes months, which is an argument for starting the record early and
   claiming nothing until it fills.

## The trap waiting here

Every artefact this repository has produced came from a filter that supplied its
own answer. A news-sentiment rating is the most inviting version of that yet: a
language model asked "is this positive?" will always return something, it will
sound confident, and **nothing in the output distinguishes a real read from a
fluent guess**. Before this ships, it needs the same test as every screen here —
*what does the rating look like when there is no signal in the news at all?* If
it looks the same, it is measuring the model, not the market.
