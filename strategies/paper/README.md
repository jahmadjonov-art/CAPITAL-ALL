# Paper record

Every signal a strategy produces, logged **before** the outcome is known, then
settled with what actually happened and why.

One append-only `.jsonl` per strategy. One JSON object per line. Never edit a
line that has already been written — settle it in place through the tool, or
void it with a reason.

## The rule the whole thing rests on

**A signal is recorded before the market resolves it, or it does not count.**

That is not bureaucracy. A strategy log written after the fact will show a
strategy that works, every time, for any strategy — because the agent writing it
already knows what happened. The only thing separating a real forward test from
a flattering story is the timestamp.

**Git enforces this for us.** Each signal is committed when it is opened, so the
commit timestamp is independent proof the call existed before the outcome. An
agent that opens and settles a signal in the same commit has proved nothing, and
the report marks it `unverified` rather than counting it.

## Capital is not a filter here

The account size is deliberately ignored. A strategy is evaluated on whether its
rules produce an edge, at the size the source describes — one NQ contract, $5 a
tick. Whether a given account can carry that is a separate question, answered
later and separately. **Do not narrow the study to what is currently affordable;
that throws away the finding.**

## Recording a signal

```bash
python3 strategies/paper.py open \
  --strategy options-flow-gamma \
  --instrument NQ --direction long \
  --entry 24150 --stop 24110 --target 24280 \
  --rule "put wall rejection" \
  --claims "Price is magnetised to max gamma levels and then rejected there." \
  --why "Price arrived at max put gamma on a slow approach; slope rule says it holds." \
  --inputs '{"put_wall":24150,"call_wall":24310,"approach":"slow","session_minute":38}'
```

Commit it immediately. Then, once the market has resolved it:

```bash
python3 strategies/paper.py settle --id SIG-0001 \
  --exit 24280 --reason target \
  --note "Reversed within four minutes of touching the wall, as the rule predicts."
```

`--reason` is one of `target`, `stop`, `time`, `manual`, `void`.

## The `why` field carries the value

A settled trade with no explanation teaches nothing. Say which rule produced it,
what the agent saw, and — on a loss — whether the rule was wrong or the rule was
right and the market did something else. **That distinction is the point of the
whole exercise**, and it is only honest if the reasoning was written at open
time, before the outcome was known.

## Costs are not optional

Every settlement applies costs. Defaults are stated in `paper.py` and printed in
every report, so a result can never quietly be a gross-of-costs number.

## Reporting

```bash
python3 strategies/paper.py report                 # every strategy
python3 strategies/paper.py report --strategy options-flow-gamma
```

Reports show win rate, average win and loss, expectancy per trade, total P&L
after costs, and how many signals are `unverified` — opened and settled in the
same commit, which is the tell for hindsight.

**A win rate on its own is close to meaningless.** A strategy claiming 75% wins
with a 1:10 reward is a different animal from one claiming 75% with a 1:1, and
either can lose money. Read expectancy.
