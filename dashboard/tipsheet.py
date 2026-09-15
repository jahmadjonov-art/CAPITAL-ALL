#!/usr/bin/env python3
"""Render the tip sheet — unusual option activity, split day / week / month.

Reads data/tipsheet.json (written by scanner/tipsheet.py) and produces a page
listing, for each expiry horizon, the tickers seeing unusual option volume and
the individual contracts driving it.

Usage: python3 dashboard/tipsheet.py
"""
import json, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "tipsheet.json"
if not SRC.exists():
    raise SystemExit("no data/tipsheet.json — run scanner/tipsheet.py first")

d = json.load(SRC.open())
scanned = dt.datetime.fromisoformat(d["scanned_utc"])

BUCKET_LABEL = {
    "day": ("Day", "Expiring today or tomorrow"),
    "week": ("Week", "2 to 7 days out"),
    "month": ("Month", "8 to 35 days out"),
}

tabs = []
for b, (label, sub) in BUCKET_LABEL.items():
    rows = []
    for r in d["rows"]:
        bk = r["buckets"][b]
        unusual = bk["build_notional"] + bk["fresh_notional"]
        if unusual <= 0:
            continue
        rows.append({
            "symbol": r["symbol"], "spot": r["spot"], "put_call": r["put_call"],
            "unusual": unusual,
            "build_notional": bk["build_notional"],
            "fresh_notional": bk["fresh_notional"],
            "top_ratio": bk["top_ratio"],
            "vol_oi": bk["vol_oi"],
            "financing_share": r["financing_share"],
            "build": bk["build"], "fresh": bk["fresh"],
        })
    rows.sort(key=lambda r: -r["unusual"])
    tabs.append({"key": b, "label": label, "sub": sub, "rows": rows,
                 "total": sum(r["unusual"] for r in rows)})

# Financing is excluded from every ranking above. Surface the worst offenders so
# the exclusion is visible rather than a silent edit to the numbers.
fin = sorted([r for r in d["rows"] if r["financing_share"] >= 0.25],
             key=lambda r: -r["financing_notional"])[:8]

DATA = {
    "built": dt.datetime.now().strftime("%d %b %Y  %H:%M"),
    "scanned": scanned.strftime("%d %b %Y  %H:%M UTC"),
    "universe_size": d["universe_size"], "returned": d["returned"],
    "coverage": d.get("coverage"),
    "feed_latest": d.get("feed_latest"), "feed_earliest": d.get("feed_earliest"),
    "errors": [e["symbol"] for e in d["errors"]],
    "params": d["params"],
    "tabs": tabs,
    "financing": [{"symbol": r["symbol"], "notional": r["financing_notional"],
                   "share": r["financing_share"], "contracts": r["financing_contracts"]}
                  for r in fin],
}

tpl = (ROOT / "dashboard" / "tipsheet_template.html").read_text()
out = ROOT / "dashboard" / "tipsheet.html"
out.write_text(tpl.replace("/*__TIPS__*/null", json.dumps(DATA, indent=2)))
print(f"built {out.relative_to(ROOT)} from {SRC.name}")
for t in tabs:
    top = ", ".join(r["symbol"] for r in t["rows"][:5])
    print(f"  {t['label']:<6} {len(t['rows']):>2} tickers  ${t['total']/1e6:>8,.0f}M  top: {top}")
