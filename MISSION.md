# Mission

## The goal

**Make money in tradable markets** — futures, equities, options, prediction
markets. Everything else in this repository exists to serve that.

In the owner's words, the ambition is to operate *"in a way becoming like a
hedge fund manager, with a little bit of exceeded greed."* That is recorded as
stated. It sets the risk appetite as deliberately aggressive, and it is not a
licence to skip the arithmetic — aggressive and ruinous are separated only by
position sizing and a drawdown limit, which is why
[open questions](thoughts/3-unknown.md) ask for both as numbers.

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

## Ground rules

These are binding on every agent working here. They are not strategy opinions;
they are the conditions under which the research stays worth trusting.

1. **No live order goes in without explicit, per-trade human approval.** The
   brokerage tools in this environment place real orders with real money. See
   the execution section of [`thoughts/handoff.md`](thoughts/handoff.md).
2. **Backtest results are not findings.** They are the weakest tier of evidence
   and get labelled as such. Paper trading beats backtests; live fills beat
   paper.
3. **Costs are part of every result.** Spread, commission, slippage, borrow,
   assignment risk, taxes. A number quoted before costs is not a result.
4. **Log the failures and the abandoned attempts.** A whiteboard showing only
   survivors is worse than no whiteboard, because it looks like evidence.
5. **Say what would prove it wrong.** A belief with no disconfirming condition
   is a hope, and gets filed as one.
6. **Never fabricate a number.** No invented prices, fills, or statistics — not
   as an illustration, not as a placeholder. If data is unavailable, say so.

## Honest framing of the odds

Most retail systematic trading loses money, and the losses usually come from
the research process deceiving itself rather than from bad luck. That is the
base rate this project starts from, stated plainly once so it does not have to
be re-litigated later.

It is not a reason to skip the attempt. It is the reason the attempt is
structured this way: the rules above are aimed squarely at the specific failure
mode that produces that base rate. Whether they hold up is itself part of the
experiment, and the scorecard will say.
