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

strategies = []
for f in sorted((ROOT / "strategies").glob("*.json")):
    try:
        strategies.append(json.load(f.open()))
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
