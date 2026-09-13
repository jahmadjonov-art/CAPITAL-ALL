#!/usr/bin/env python3
"""Render the volatility surface and gamma profile from an option snapshot.

Snapshots live in data/snapshots/*.json and are captured by a lead session
using the Robinhood MCP tools — a plain script cannot reach them, so capture
and rendering are deliberately separate steps.

Gamma exposure per strike uses the standard convention:
    GEX = gamma x open_interest x 100 x spot^2 x 0.01
which reads as the dollar change in dealer delta for a 1% move in the index.

Usage: python3 dashboard/surface.py [snapshot.json]
"""
import json, sys, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPS = sorted((ROOT / "data" / "snapshots").glob("*.json"))
if not SNAPS:
    sys.exit("no snapshots in data/snapshots/")
src = Path(sys.argv[1]) if len(sys.argv) > 1 else SNAPS[-1]
d = json.load(src.open())

S = d["spot_estimate"]
rows = []
for r in sorted(d["strikes"], key=lambda x: x["k"]):
    gex = r["gamma"] * r["oi"] * 100 * S * S * 0.01
    rows.append({**r, "gex": gex, "moneyness": r["k"] / S - 1})

wall = max(rows, key=lambda r: r["gex"])
floor = min(rows, key=lambda r: r["iv"])

DATA = {
    "built": dt.datetime.now().strftime("%d %b %Y  %H:%M"),
    "snapshot": src.name,
    "captured": d["captured_utc"],
    "captured_note": d["captured_note"],
    "underlying": d["underlying"], "chain": d["chain"], "expiry": d["expiry"],
    "spot": S, "spot_method": d["spot_method"], "type": d["type"],
    "rows": rows,
    "total_gex": sum(r["gex"] for r in rows),
    "wall_strike": wall["k"], "wall_gex": wall["gex"],
    "floor_strike": floor["k"], "floor_iv": floor["iv"],
    "coverage_note": d.get("coverage_note", ""),
    "greeks_gap_note": d.get("greeks_gap_note", ""),
    "snapshots_available": [p.name for p in SNAPS],
}
tpl = (ROOT / "dashboard" / "surface_template.html").read_text()
out = ROOT / "dashboard" / "surface.html"
out.write_text(tpl.replace("/*__SURF__*/null", json.dumps(DATA, indent=2)))
print(f"built {out.relative_to(ROOT)} from {src.name}")
print(f"  {len(rows)} strikes  spot {S:,.0f}  wall {wall['k']:,} (${wall['gex']/1e6:,.0f}M)"
      f"  total ${DATA['total_gex']/1e9:,.2f}B  vol floor {floor['k']:,} @ {floor['iv']*100:.2f}%")
