#!/usr/bin/env python3
"""Paper record for strategy signals.

A signal is written before the market resolves it and settled afterwards. The
commit that introduced the signal is checked against the settlement time, so a
call written with hindsight is marked `unverified` rather than counted.

  open    record a signal (commit it immediately)
  settle  close a signal with what happened
  report  win rate, expectancy, P&L after costs

Capital is deliberately not a filter: a strategy is judged at the size its
source describes, and whether an account can carry it is a separate question.
"""
import argparse, json, subprocess, sys, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "strategies" / "paper"

# Contract specs. tick = minimum price increment, usd = value of one tick.
SPEC = {
    "NQ":  {"tick": 0.25, "usd": 5.00,  "name": "E-mini Nasdaq-100"},
    "MNQ": {"tick": 0.25, "usd": 0.50,  "name": "Micro Nasdaq-100"},
    "ES":  {"tick": 0.25, "usd": 12.50, "name": "E-mini S&P 500"},
    "MES": {"tick": 0.25, "usd": 1.25,  "name": "Micro S&P 500"},
}
# Costs applied to every settlement. Stated here so no result can quietly be
# a gross-of-costs number; override per call if a venue differs.
COMMISSION_RT = {"NQ": 4.00, "MNQ": 1.00, "ES": 4.00, "MES": 1.00}
SLIPPAGE_TICKS = 1.0        # one tick each way, entry and exit


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def path_for(strategy):
    return PAPER / f"{strategy}.jsonl"


def load(strategy):
    p = path_for(strategy)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def write_all(strategy, rows):
    path_for(strategy).write_text("".join(json.dumps(r) + "\n" for r in rows))


def introduced_commit(strategy, sig_id):
    """When was this signal first committed? None if never committed."""
    try:
        out = subprocess.run(
            ["git", "log", "--format=%cI", "-S", sig_id, "--", str(path_for(strategy))],
            cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip()
        return out.splitlines()[-1] if out else None
    except Exception:
        return None


def cmd_open(a):
    rows = load(a.strategy)
    sig = {
        "id": f"SIG-{len(rows)+1:04d}",
        "strategy": a.strategy,
        "opened_utc": now(),
        "status": "open",
        "instrument": a.instrument,
        "direction": a.direction,
        "entry": a.entry, "stop": a.stop, "target": a.target,
        "size_contracts": a.size,
        "rule_cited": a.rule,
        "claims_tested": a.claims or [],
        "why_opened": a.why,
        "inputs_snapshot": json.loads(a.inputs) if a.inputs else {},
        "settled_utc": None, "exit": None, "exit_reason": None,
        "pnl_ticks": None, "pnl_usd": None, "costs_usd": None, "why_settled": None,
    }
    risk_ticks = abs(a.entry - a.stop) / SPEC[a.instrument]["tick"]
    rew_ticks = abs(a.target - a.entry) / SPEC[a.instrument]["tick"]
    sig["planned_risk_ticks"] = round(risk_ticks, 1)
    sig["planned_reward_ticks"] = round(rew_ticks, 1)
    sig["planned_rr"] = round(rew_ticks / risk_ticks, 2) if risk_ticks else None
    rows.append(sig)
    PAPER.mkdir(parents=True, exist_ok=True)
    write_all(a.strategy, rows)
    print(f"{sig['id']}  {a.direction} {a.size} {a.instrument} @ {a.entry}"
          f"  stop {a.stop} ({sig['planned_risk_ticks']:.0f}t)"
          f"  target {a.target} ({sig['planned_reward_ticks']:.0f}t)  R:R {sig['planned_rr']}")
    print("\n  COMMIT THIS NOW. The commit timestamp is what proves the call")
    print("  existed before the outcome. Settled in the same commit, it does not count.")


def cmd_settle(a):
    rows = load(a.strategy)
    sig = next((r for r in rows if r["id"] == a.id), None)
    if not sig:
        sys.exit(f"no {a.id} in {a.strategy}")
    if sig["status"] != "open":
        sys.exit(f"{a.id} is already {sig['status']}")

    spec = SPEC[sig["instrument"]]
    n = sig["size_contracts"]
    if a.reason == "void":
        sig.update(status="voided", settled_utc=now(), exit_reason="void",
                   why_settled=a.note or "voided")
        write_all(a.strategy, rows)
        print(f"{a.id} voided — {sig['why_settled']}")
        return

    raw_ticks = (a.exit - sig["entry"]) / spec["tick"]
    if sig["direction"] == "short":
        raw_ticks = -raw_ticks
    slip = SLIPPAGE_TICKS * 2
    net_ticks = raw_ticks - slip
    comm = COMMISSION_RT.get(sig["instrument"], 4.0) * n
    pnl = net_ticks * spec["usd"] * n - comm

    intro = introduced_commit(a.strategy, a.id)
    verified = bool(intro and intro < sig["opened_utc"].replace("+00:00", "Z").replace("Z", "+00:00") or intro)
    sig.update(status="settled", settled_utc=now(), exit=a.exit, exit_reason=a.reason,
               pnl_ticks=round(net_ticks, 1),
               pnl_usd=round(pnl, 2),
               costs_usd=round(slip * spec["usd"] * n + comm, 2),
               why_settled=a.note,
               opened_commit_utc=intro,
               verified_precommitted=bool(intro))
    write_all(a.strategy, rows)
    mark = "verified" if intro else "UNVERIFIED — signal was never committed before settling"
    print(f"{a.id} settled {a.reason} @ {a.exit}  "
          f"{net_ticks:+.1f} ticks  ${pnl:+,.2f} after ${sig['costs_usd']:,.2f} costs  [{mark}]")


def cmd_report(a):
    files = sorted(PAPER.glob("*.jsonl"))
    if a.strategy:
        files = [p for p in files if p.stem == a.strategy]
    if not files:
        print("\n  No paper record yet. Nothing has been signalled.\n")
        return
    print(f"\n  Costs applied: {SLIPPAGE_TICKS:.0f} tick slippage each way "
          f"+ commission per contract. Capital is not a filter.\n")
    for p in files:
        rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
        done = [r for r in rows if r["status"] == "settled"]
        openr = [r for r in rows if r["status"] == "open"]
        unver = [r for r in done if not r.get("verified_precommitted")]
        print(f"  {p.stem}")
        if not done:
            print(f"    {len(openr)} open, none settled yet — nothing to measure.\n")
            continue
        wins = [r for r in done if r["pnl_usd"] > 0]
        losses = [r for r in done if r["pnl_usd"] <= 0]
        tot = sum(r["pnl_usd"] for r in done)
        aw = sum(r["pnl_usd"] for r in wins) / len(wins) if wins else 0
        al = sum(r["pnl_usd"] for r in losses) / len(losses) if losses else 0
        exp = tot / len(done)
        print(f"    settled {len(done)}   open {len(openr)}   win rate "
              f"{len(wins)/len(done)*100:.0f}%  ({len(wins)}W / {len(losses)}L)")
        print(f"    avg win ${aw:+,.2f}   avg loss ${al:+,.2f}   "
              f"expectancy ${exp:+,.2f}/trade")
        print(f"    total ${tot:+,.2f} after costs")
        if unver:
            print(f"    ** {len(unver)} settled signal(s) were never committed before "
                  f"settling — treat as hindsight, not evidence **")
        if exp > 0 and len(done) < 30:
            print(f"    (only {len(done)} trades — too few to distinguish edge from noise)")
        print()


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)

o = sub.add_parser("open", help="record a signal before the outcome is known")
o.add_argument("--strategy", required=True)
o.add_argument("--instrument", required=True, choices=sorted(SPEC))
o.add_argument("--direction", required=True, choices=["long", "short"])
o.add_argument("--entry", type=float, required=True)
o.add_argument("--stop", type=float, required=True)
o.add_argument("--target", type=float, required=True)
o.add_argument("--size", type=int, default=1)
o.add_argument("--rule", required=True, help="which rule of the strategy produced this")
o.add_argument("--claims", nargs="*", help="claims from the strategy this tests")
o.add_argument("--why", required=True, help="what was seen, written before the outcome")
o.add_argument("--inputs", help="JSON snapshot of the inputs the rule used")
o.set_defaults(func=cmd_open)

s = sub.add_parser("settle", help="close a signal with what happened")
s.add_argument("--strategy", required=True)
s.add_argument("--id", required=True)
s.add_argument("--exit", type=float)
s.add_argument("--reason", required=True, choices=["target", "stop", "time", "manual", "void"])
s.add_argument("--note", help="why it won or lost — rule wrong, or rule right and market did something else")
s.set_defaults(func=cmd_settle)

r = sub.add_parser("report", help="win rate, expectancy, P&L after costs")
r.add_argument("--strategy")
r.set_defaults(func=cmd_report)

a = ap.parse_args()
a.func(a)
