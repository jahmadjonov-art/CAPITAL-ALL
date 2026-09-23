#!/usr/bin/env python3
"""Render the company-value screen from data/value.json.

Usage: python3 dashboard/value.py
"""
import json, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "value.json"
if not SRC.exists():
    raise SystemExit("no data/value.json — run scanner/value.py first")

d = json.load(SRC.open())
DATA = {
    "built": dt.datetime.fromisoformat(d["built_utc"]).strftime("%d %b %Y  %H:%M UTC"),
    "session": d["price_session"],
    "universe": d["universe"],
    "thresholds": d["thresholds"],
    "peg_basis": d["peg_basis"],
    "lists": d["lists"],
}
tpl = (ROOT / "dashboard" / "value_template.html").read_text()
out = ROOT / "dashboard" / "value.html"
out.write_text(tpl.replace("/*__VALUE__*/null", json.dumps(DATA, indent=2)))
print(f"built {out.relative_to(ROOT)}  ({d['universe']} companies valued, "
      f"prices from {d['price_session']})")
for k, v in d["lists"].items():
    print(f"  {k:<12} {len(v):>2}  {', '.join(r['ticker'] for r in v[:6])}")
