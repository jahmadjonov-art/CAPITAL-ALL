# Mission

## The goal

**Make money in tradable markets** — futures, equities, options, prediction
markets. Everything else in this repository exists to serve that.

In the owner's words, the ambition is to operate *"in a way becoming like a
hedge fund manager, with a little bit of exceeded greed."* Recorded as stated.

**Capital, position sizing and drawdown limits are the agents' own call.** The
owner was asked for numbers and deliberately declined to give any:

> "Those things will be completely up to the agents. They will try to get a
> higher score from me, therefore they're gonna try different things out. And of
> course they're gonna make mistakes. Of course they're gonna succeed."

So risk management is not a constraint handed down — it is part of what is being
researched, and getting it wrong is a legitimate way to learn something. An
agent that wants a sizing rule derives one and defends it in
`research/beliefs.md` like any other claim.

## What this actually is

An experiment, and a piece of research. The end state is clear; the route to it
is not:

> "I know and see the end result, but I don't know how we're gonna get there
> yet."

So this is not a project with a specification waiting to be implemented. It is
an environment where agents run experiments, record what happened, and leave
behind a whiteboard that the next session starts from:

> "Here are the mistakes we made. Here's why, or here, why we *think* it was a
> mistake. Here are the successes. Here, why we *think* these are successes."

Note the hedge in that phrasing — *why we think*. It is carried into the format
of every research entry deliberately. Nothing in this repository gets to claim
it knows why something worked.

## Why the record-keeping is the actual work

It would be easy to treat the knowledge base as scaffolding around the real job
of finding strategies. That is backwards.

Systematic trading research has a specific, well-documented way of failing, and
it is not running out of ideas. It is that **a search process which tests many
strategies and keeps the winners will produce winners whether or not any edge
exists.** Test forty variants, and two clearing a 5% significance bar is the
expected outcome of pure noise. Every one of those two will have a plausible
story attached. An agent loop is very good at generating variants and stories,
which makes it very good at manufacturing false confidence at a rate no human
researcher could match.

A knowledge base that accumulates successes is therefore not neutral. Built
naively, it is a machine for laundering luck into conviction, and the conviction
gets expensive at exactly the moment real capital is committed.

So the discipline in [`research/README.md`](research/README.md) — pre-registered
hypotheses, every abandoned variant counted, untouched holdout data, costs
mandatory, a stated falsification condition on every belief — is not
bureaucracy layered on top of the research. **It is the part that decides
whether any of this makes money.** The ideas are cheap and both the owner and
any competent agent will have plenty. An honest evaluation process is the scarce
thing, and it is the only defensible edge a two-person operation has over
participants with better data, faster execution and more capital.

## What agents decide for themselves

Nearly everything. This is deliberate and stated explicitly by the owner:

> "I don't wanna put rules and limitations to the agents. I want them to do
> their own research and then figure things out on their own, see what works,
> what doesn't work."

Which markets to pursue, which strategies to test, how much risk to take, what
to read, what tools or data vendors to go find on the open internet, how to
spend a session. No agent needs permission for any of it, and an unusual
direction argued well beats a safe one nobody learns from.

## What stays fixed

Four things, and **none of them limit what an agent may try.** They constrain
only how results get recorded, because the owner's score is the feedback signal
this entire programme runs on — and a score awarded for a result that was never
real teaches everyone the wrong lesson, permanently.

1. **Never fabricate a number.** No invented prices, fills, returns or
   statistics — not as illustration, not as placeholder. Unavailable data is
   recorded as unavailable. One fabricated figure silently poisons every belief
   downstream of it and nobody will know which ones.
2. **Log the failures and the abandoned attempts.** A whiteboard showing only
   survivors is worse than no whiteboard, because it looks like evidence.
3. **Label the evidence honestly.** A backtest is a backtest. Paper beats
   backtests, live fills beat paper, and costs — spread, commission, slippage,
   borrow, assignment — are part of every figure quoted.
4. **Say what would prove it wrong.** A belief with no disconfirming condition
   never gets retired; it just quietly keeps costing money.

And one line on execution, which is not a research constraint but a question of
authority:

**No agent places, cancels or exercises a real order until the owner says so in
writing.** The brokerage account is deliberate and currently unfunded, so the
practical risk today is nil — an order would simply be rejected. The rule exists
for the day it holds money, and it is the owner's to lift, explicitly, with
whatever limits he wants. It is not something an agent may infer from an
instruction to pursue profit. See
[`thoughts/handoff.md`](thoughts/handoff.md).

## Honest framing of the odds

Most retail systematic trading loses money, and the losses usually come from
the research process deceiving itself rather than from bad luck. That is the
base rate this project starts from, stated plainly once so it does not have to
be re-litigated later.

It is not a reason to skip the attempt. It is the reason the attempt is
structured this way: the rules above are aimed squarely at the specific failure
mode that produces that base rate. Whether they hold up is itself part of the
experiment, and the scorecard will say.
