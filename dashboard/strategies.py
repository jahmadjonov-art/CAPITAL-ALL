#!/usr/bin/env python3
"""Build the strategy library site from strategies/*.json.

One tab per strategy file. Drop another JSON in strategies/ and it appears
with no change here. Content is whatever the source said — extraction only,
no evaluation. The `status` on each claim is what turns this into something
testable: it moves from untested only when an experiment says so.

Usage: python3 dashboard/strategies.py
"""
import json, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard" / "strategies.html"

def paper_stats(sid):
    """Read the forward record. Unverified signals are counted separately —
    a call settled without ever being committed first is hindsight."""
    f = ROOT / "strategies" / "paper" / f"{sid}.jsonl"
    if not f.exists():
        return {"exists": False}
    rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    done = [r for r in rows if r.get("status") == "settled"]
    unver = [r for r in done if not r.get("verified_precommitted")]
    wins = [r for r in done if (r.get("pnl_usd") or 0) > 0]
    tot = sum(r.get("pnl_usd") or 0 for r in done)
    return {
        "exists": True, "signals": len(rows),
        "open": len([r for r in rows if r.get("status") == "open"]),
        "settled": len(done), "wins": len(wins), "unverified": len(unver),
        "win_rate": round(len(wins) / len(done) * 100) if done else None,
        "total_usd": round(tot, 2) if done else None,
        "expectancy": round(tot / len(done), 2) if done else None,
    }


strategies = []
for f in sorted((ROOT / "strategies").glob("*.json")):
    try:
        d = json.load(f.open())
        d["paper"] = paper_stats(d["id"])
        strategies.append(d)
    except Exception as e:
        print(f"  SKIP {f.name}: {e}")

DATA = {
    "built": dt.datetime.now().strftime("%d %b %Y  %H:%M"),
    "strategies": strategies,
}
tpl = (ROOT / "dashboard" / "strategies_template.html").read_text()
OUT.write_text(tpl.replace("/*__STRATS__*/null", json.dumps(DATA, indent=2)))
n_claims = sum(len(s.get("claims", [])) for s in strategies)
print(f"built {OUT.relative_to(ROOT)}")
print(f"  {len(strategies)} strategies, {n_claims} claims tracked")
for s in strategies:
    print(f"    {s['id']:26} {s.get('status','?'):10} {len(s.get('claims',[]))} claims")
