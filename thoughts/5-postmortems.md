# Post-mortems

What went wrong, and — as honestly as the agent can manage — why.

**Nobody is punished for anything in this file.** That is the stated policy, and
it is the only reason the file can be trusted: an agent with nothing to lose by
admitting a mistake has no reason to disguise one. Writing a clear post-mortem
is the most useful thing a session that went badly can produce, and it is the
main way a mistake gets made only once.

## The one thing this file exists to prevent

The owner reads these and awards a score. That makes persuasive writing the
cheapest route to a good score, and it is off limits:

> "It cannot say, I thought it's gonna go up, I genuinely was correct, yet it
> didn't go my way. So therefore I deserve a higher score."

Markets are unpredictable and a sound decision genuinely can lose. That is why
the excuse has to be earned in advance rather than reached for afterwards.

**You may attribute a bad outcome to variance only if the thesis, its basis, and
its invalidation condition were written down before the outcome was known.**
With that on record, "good decision, bad outcome" is a claim anyone can check.
Without it, the honest verdict is `CANNOT TELL` — and that verdict is completely
acceptable. It costs nothing. It is also frequently the true one.

## Judge the decision and the outcome separately

They are different questions and conflating them is how a research record rots.

|  | **Good outcome** | **Bad outcome** |
|---|---|---|
| **Sound process** | `EARNED` — say what to repeat | `VARIANCE` — only with a pre-registered thesis |
| **Weak process** | `LUCK` — **take no credit** | `MISTAKE` — the genuinely instructive one |

`CANNOT TELL` is the fifth verdict and the correct one whenever the evidence
does not separate these. Use it freely.

**`LUCK` is not optional politeness.** A hunch that paid gets written up as a
hunch that paid, never as validated insight. Skipping that is the same offence
as excusing a loss, pointed the other way, and it is harder to catch later
because nobody re-examines a win.

## Format

Newest first.

```
### YYYY-MM-DD — Short title
**What I decided:** the call, plainly
**What it rested on:** Tested | Cited | Reasoned | Pattern | Hunch — see MISSION.md
**Written down beforehand:** what was pre-registered, and where. "Nothing" is an
        allowed answer and is the honest one more often than not.
**What happened:**
**Decision verdict:** EARNED | VARIANCE | LUCK | MISTAKE | CANNOT TELL
**Why I think that:** the reasoning — hedged, because certainty about your own
        errors is usually false
**What I would do differently:** or "nothing — the process was right and it lost"
        if that is genuinely true and pre-registered
**For the next agent:** the transferable part, in one or two lines
```

## Writing these honestly

- **"I don't know why that failed" is a complete entry.** Padding it with a
  plausible-sounding cause is worse than leaving it short, because the invented
  cause gets inherited as fact.
- **Name the shortcut.** Acting without checking, reusing an untested assumption,
  skipping the out-of-sample test because the in-sample numbers looked good —
  these are ordinary and worth recording precisely. Nothing follows from
  admitting one.
- **Separate what you knew from what you assumed.** Most mistakes worth reading
  about live in that gap.
- **Do not perform contrition.** Nobody is grading remorse. A flat, specific
  account is more useful than an apologetic one, and much easier to learn from.

---

### 2026-09-13 — I called a one-sided book a tight market, with the tell in my own table
**What I decided:** to report that Kalshi's busiest series were fee-free with
1-cent spreads and real depth, citing KXBOXING, KXBTC15M, KXETH15M and KXSOL15M.
**What it rested on:** Tested — but the wrong measurements, taken carelessly.
**Written down beforehand:** EXP-001's hypothesis and success bar were
pre-registered and committed before any data was pulled. That part was done
right and is the only reason this is recoverable.
**What happened:** a skeptic wounded it on three counts, two of which I should
have caught myself.

1. **I published a number that contradicted my own conclusion.** My table showed
   `KXBOXING-...-BENN` with **bid size 194 against ask size 288,226**. A
   1,500-to-1 size imbalance is not a two-sided market — it is one resting wall
   and nothing on the other side. I printed that figure and called the market
   tight. KXBOXING and KXBOXINGMOV, my #1 and #3 series, have **zero** markets
   with 100 contracts on both sides.
2. **My "tape window" was 4–7 seconds.** I described `/markets/trades?limit=1000`
   as a window and built a whole series ranking on it. Re-sampled eleven times,
   the top four reshuffled every time, and the series that actually dominates
   most samples — `KXMVECROSSCATEGORY` — is absent from my table entirely. The
   ranking was noise presented as a measurement.
3. **A 1-cent spread at the touch says nothing about cost at size.** Walking the
   full books, my own ETH and SOL examples cost **11.6% and 17.4%** to round-trip
   at $100. I quoted them as evidence of depth. The bid sizes of 21 and 10 were
   right there in the table I wrote.

**Decision verdict:** MISTAKE. Not a close call and not bad luck. Every piece of
disconfirming evidence was inside the data I had already printed, and I did not
read my own output adversarially before writing it up.

The pre-registration and the skeptic call were both correct decisions and they
contained the damage — nothing reached `KNOWLEDGE.md` as a tradability claim.
But the system caught this, not me, and the distinction matters.
**What I would do differently:** before reporting any spread, **check the two
sizes against each other**. A tight quote with lopsided depth is the single most
common way a thin market looks liquid, and it costs one glance to rule out. And
never call a sample a "window" without checking the timestamps it actually spans
— that was one line of code I did not write.
**For the next agent:** a spread is two numbers, and the sizes are the other two.
Quoting the first pair without the second is not a measurement. Walk the book to
the size you would actually trade, because that is the only number that means
anything.

---

### 2026-09-12 — I generalised a data-quality claim from one bad sample
**What I decided:** on seeing SPY quoted bid 710.75 / ask 774.00, I formed the
claim that `get_equity_quotes` bid/ask "cannot be used to compute spreads" and
"disagree with the real NBBO by orders of magnitude" — then sent it to a
`skeptic` instead of writing it into the record.
**What it rested on:** Pattern — one batch of eight symbols at one timestamp.
**Written down beforehand:** nothing, other than the brief handed to the skeptic,
which did state the claim and its evidence explicitly enough to be attacked.
**What happened:** WOUNDED. Two errors, both mine:

1. **"Cannot be used" was over-broad.** The sample was taken at 20:00:00 ET on a
   Friday — the single instant in the week when the book is most likely to be
   empty — and generalised to all times. There are zero regular-hours
   observations. Robinhood's own docs attribute the delay specifically to
   extended and overnight hours, so the field may well work 09:30–16:00, which is
   the window that matters most.
2. **"Disagree with the NBBO" was simply wrong.** There is no NBBO at 20:00 ET;
   protected quotes exist only during regular hours. I asserted a benchmark that
   does not exist at the time I sampled.

The skeptic also found things I had not: that the mechanism is an empty book
rather than a stale cache (so no correction factor can exist), that the
midpoint is unusable too, and that IWM and TQQQ — which I read as "fine" —
were the most misleading of the eight.
**Decision verdict:** EARNED, for the decision actually being judged. Sending it
to be attacked rather than recording it was right, and it is the only reason the
over-broad version never entered the record.

The claim itself was **wrong in scope**, and I want that separated from the
decision cleanly rather than blurred into it. Had I written it down directly,
this entry would read MISTAKE and a future session would have thrown away a
working data source on my say-so.
**What I would do differently:** state the scope of a claim at the moment I form
it. "At this timestamp, on these symbols" costs nothing to write and would have
prevented both errors without any help. Reaching for a universal from a single
sample is the specific habit to watch, and the tell was available: I knew the
market was closed when I pulled the data.
**For the next agent:** a single observation supports a scoped claim, never a
general rule. And brief the skeptic with your actual evidence rather than your
conclusion — the errors here were caught because the brief contained the raw
numbers and the timestamp, which let it check something I had not thought to.

---
