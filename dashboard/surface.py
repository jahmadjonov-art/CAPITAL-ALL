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
UNIT = 100 * S * S * 0.01          # dollars per 1% move, per unit of gamma x OI

rows = []
for r in sorted(d["strikes"], key=lambda x: x["k"]):
    c, p = r["call"], r["put"]
    cg = c["gamma"] * c["oi"] * UNIT
    pg = p["gamma"] * p["oi"] * UNIT
    rows.append({"k": r["k"], "moneyness": r["k"] / S - 1,
                 "call_iv": c["iv"], "put_iv": p["iv"],
                 "call_gamma": c["gamma"], "put_gamma": p["gamma"],
                 "call_oi": c["oi"], "put_oi": p["oi"],
                 "call_vol": c["vol"], "put_vol": p["vol"],
                 "call_gex": cg, "put_gex": pg, "net_gex": cg - pg})

net_total = sum(r["net_gex"] for r in rows)
call_wall = max(rows, key=lambda r: r["call_gex"])
put_wall = max(rows, key=lambda r: r["put_gex"])
floor = min(rows, key=lambda r: r["call_iv"])
max_oi = max(rows, key=lambda r: r["call_oi"] + r["put_oi"])

# Gamma flip: where cumulative net gamma, accumulated downward from the top
# strike, crosses zero. With few strikes this is coarse and is flagged as such.
cum, flip = 0.0, None
for r in sorted(rows, key=lambda x: -x["k"]):
    prev = cum
    cum += r["net_gex"]
    if (prev > 0 >= cum) or (prev < 0 <= cum):
        flip = r["k"]
flip_reliable = flip is not None and rows[0]["k"] < flip < rows[-1]["k"]

DATA = {
    "built": dt.datetime.now().strftime("%d %b %Y  %H:%M"),
    "snapshot": src.name,
    "captured": d["captured_utc"],
    "captured_note": d["captured_note"],
    "underlying": d["underlying"], "chain": d["chain"], "expiry": d["expiry"],
    "spot": S, "spot_method": d["spot_method"],
    "rows": rows,
    "net_total": net_total,
    "regime": "NEGATIVE" if net_total < 0 else "POSITIVE",
    "regime_text": ("Dealers amplify moves. Expect trend continuation and a larger "
                    "realised range. Do not fade.") if net_total < 0 else
                   ("Dealers dampen moves. Mean-reverting tape where fading the edges "
                    "tends to work."),
    "call_wall": call_wall["k"], "call_wall_gex": call_wall["call_gex"],
    "put_wall": put_wall["k"], "put_wall_gex": put_wall["put_gex"],
    "walls_coincide": call_wall["k"] == put_wall["k"],
    "max_oi_strike": max_oi["k"], "max_oi": max_oi["call_oi"] + max_oi["put_oi"],
    "flip": flip, "flip_reliable": flip_reliable,
    "convention": d.get("convention", ""),
    "floor_strike": floor["k"], "floor_iv": floor["call_iv"],
    "coverage_note": d.get("coverage_note", ""),
    "greeks_gap_note": d.get("greeks_gap_note", ""),
    "snapshots_available": [p.name for p in SNAPS],
}
tpl = (ROOT / "dashboard" / "surface_template.html").read_text()
out = ROOT / "dashboard" / "surface.html"
out.write_text(tpl.replace("/*__SURF__*/null", json.dumps(DATA, indent=2)))
print(f"built {out.relative_to(ROOT)} from {src.name}")
print(f"  {len(rows)} strikes  spot {S:,.0f}  net ${net_total/1e6:+,.1f}M  {DATA['regime']} gamma")
print(f"  call wall {call_wall['k']:,}  put wall {put_wall['k']:,}"
      f"{'  ** SAME STRIKE — pin, not a barrier **' if DATA['walls_coincide'] else ''}")
print(f"  flip {flip if flip else 'n/a'}{'' if flip_reliable else ' (at the edge of the sample — not reliable)'}")
