#!/usr/bin/env python3
"""Unusual option activity scanner — the tip sheet.

Pulls full option chains from CBOE for a universe of liquid names and ranks
what is trading unusually against the open interest already standing there,
split into a day / week / month view.

THE METRIC, AND ITS LIMIT
  Unusual activity here means volume / open interest. A contract trading many
  times the open interest that existed at yesterday's close is new positioning
  rather than existing positions changing hands.

  This is NOT "unusual versus this ticker's own normal volume" — that needs a
  history of daily volume, which nothing here records yet (sandbox/data-collection.md).
  Volume against open interest is the honest version of the question we can
  actually answer today, and it is the standard screen, but it is not the same
  question.

DATA NOTES
  CBOE volume is same-day and updates through the session. Open interest is the
  official figure from the previous close and does not move intraday — which is
  exactly what makes the ratio meaningful, but means a pre-open scan reports the
  PREVIOUS session's volume.

Usage: python3 scanner/tipsheet.py [--out FILE] [--cache DIR]
"""
import json, re, argparse, datetime as dt, urllib.request
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CBOE = "https://cdn.cboe.com/api/global/delayed_quotes/options/{}.json"
SYM = re.compile(r"^([A-Z]+)(\d{6})([CP])(\d{8})$")

# Liquid, heavily optioned names. A starting universe, not the whole market —
# the scan is only ever as broad as this list.
UNIVERSE = """
AAPL MSFT NVDA AMZN GOOGL META TSLA AMD AVGO NFLX
INTC MU PLTR SOFI COIN HOOD RIVN LCID F GM
BAC JPM GS WFC C SCHW V MA PYPL SQ
XOM CVX OXY SLB FCX NEM GLD SLV USO UNG
SPY QQQ IWM DIA TLT HYG XLF XLE SMH ARKK
BA GE CAT DE UPS FDX DAL UAL AAL CCL
DIS WBD PARA ROKU SNAP PINS UBER LYFT ABNB DASH
""".split()

CONTRACT_VOL_FLOOR = 250      # ignore thin contracts — a 5x ratio on 3 lots is noise
MIN_OI_FOR_RATIO = 100        # below this the ratio is not measured, it is invented

# Two categories, deliberately separated. Mixing them was the first version's
# mistake: ranking everything by vol/OI put contracts with almost no open
# interest on top, where the "ratio" is really just the denominator floor.
#   BUILD  — heavy volume against real existing open interest. Someone is
#            trading size where positions already stand.
#   FRESH  — heavy volume where almost no open interest existed. All-new
#            positioning, which is interesting for a different reason and must
#            not be ranked on a ratio.
FRESH_OI_CEILING = 100

# ZERO-OPTIONALITY FILTER.
#
# A contract with delta pinned at 1 and no vega is not an option position — it
# is a stock substitute. Volume there is financing, a roll, a box or an
# assignment being managed, never a directional view, and it is enormous: on
# 2026-09-14 it was 82% of IWM's standout notional and would have put IWM top
# of the sheet on machinery alone.
#
# The first attempt at this used a moneyness cut (strike >8% in the money) and
# a count of strikes per expiry. It fired on 11 of the top 15 tickers, which
# made it worthless as a flag. CBOE ships greeks per contract, so the property
# can be tested directly rather than guessed at from the strike. Measured over
# the whole universe, 88% of contracts with delta >= 0.98 also have vega at or
# below 0.005, so this is testing one real thing, not two loose things.
#
# These contracts are removed from the rankings and reported separately, not
# silently dropped — the financing itself is worth seeing.
NO_OPTIONALITY_DELTA = 0.98
NO_OPTIONALITY_VEGA = 0.01

BUCKETS = ("day", "week", "month", "beyond")


def fetch(sym, cache=None):
    if cache:
        p = Path(cache) / f"{sym}.json"
        if p.exists():
            return sym, json.loads(p.read_text())
    try:
        r = urllib.request.Request(CBOE.format(sym), headers={"User-Agent": "research/1.0"})
        with urllib.request.urlopen(r, timeout=45) as f:
            d = json.load(f)["data"]
    except Exception as e:
        return sym, {"_error": f"{type(e).__name__}: {e}"}
    if cache:
        Path(cache).mkdir(parents=True, exist_ok=True)
        (Path(cache) / f"{sym}.json").write_text(json.dumps(d))
    return sym, d


def bucket(days):
    if days <= 1:   return "day"
    if days <= 7:   return "week"
    if days <= 35:  return "month"
    return "beyond"


def scan(universe, cache=None):
    today = dt.date.today()
    out, errors = [], []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for sym, d in ex.map(lambda s: fetch(s, cache), universe):
            if "_error" in d:
                errors.append({"symbol": sym, "error": d["_error"]}); continue
            spot = float(d.get("current_price") or 0)
            tot_v = tot_oi = call_v = put_v = 0.0
            fin_v = fin_notional = 0.0
            fin_n = 0
            # per bucket: aggregate turnover plus the standouts found in it
            agg = {b: {"vol": 0.0, "oi": 0.0} for b in BUCKETS}
            std = {b: {"build": [], "fresh": []} for b in BUCKETS}
            for o in d.get("options", []):
                m = SYM.match(o.get("option", ""))
                if not m: continue
                _, ymd, cp, strike = m.groups()
                try:
                    exp = dt.date(2000 + int(ymd[:2]), int(ymd[2:4]), int(ymd[4:]))
                except ValueError:
                    continue
                dte = (exp - today).days
                if dte < 0: continue
                v = float(o.get("volume") or 0)
                oi = float(o.get("open_interest") or 0)
                tot_v += v; tot_oi += oi
                if cp == "C": call_v += v
                else: put_v += v
                b = bucket(dte)
                agg[b]["vol"] += v; agg[b]["oi"] += oi
                if v < CONTRACT_VOL_FLOOR: continue

                k = int(strike) / 1000.0
                mark = float(o.get("theo") or o.get("last_trade_price") or 0)
                notional = round(v * mark * 100)
                delta = float(o.get("delta") or 0)
                vega = float(o.get("vega") or 0)
                if abs(delta) >= NO_OPTIONALITY_DELTA and vega <= NO_OPTIONALITY_VEGA:
                    fin_v += v; fin_notional += notional; fin_n += 1
                    continue

                rec = {
                    "strike": k, "type": "call" if cp == "C" else "put",
                    "expiry": exp.isoformat(), "dte": dte,
                    "vol": v, "oi": oi, "notional": notional,
                    "iv": round(float(o.get("iv") or 0), 4),
                    "delta": round(delta, 3),
                    "moneyness": round((k / spot - 1) if spot else 0.0, 4),
                }
                if oi >= MIN_OI_FOR_RATIO:
                    rec["ratio"] = round(v / oi, 2)
                    std[b]["build"].append(rec)
                elif oi <= FRESH_OI_CEILING:
                    rec["ratio"] = None
                    std[b]["fresh"].append(rec)
            if not tot_v: continue

            buckets = {}
            for b in BUCKETS:
                bu, fr = std[b]["build"], std[b]["fresh"]
                bu.sort(key=lambda r: -r["ratio"])
                fr.sort(key=lambda r: -r["notional"])
                a = agg[b]
                buckets[b] = {
                    "vol": a["vol"], "oi": a["oi"],
                    "vol_oi": round(a["vol"] / a["oi"], 4) if a["oi"] else None,
                    "build_notional": sum(r["notional"] for r in bu),
                    "fresh_notional": sum(r["notional"] for r in fr),
                    "top_ratio": bu[0]["ratio"] if bu else 0,
                    "build": bu[:8], "fresh": fr[:8],
                }
            live = ("day", "week", "month")
            bn = sum(buckets[b]["build_notional"] for b in live)
            fn = sum(buckets[b]["fresh_notional"] for b in live)
            out.append({
                "symbol": sym, "spot": spot,
                "total_vol": tot_v, "total_oi": tot_oi,
                "vol_oi": round(tot_v / tot_oi, 4) if tot_oi else None,
                "call_vol": call_v, "put_vol": put_v,
                "put_call": round(put_v / call_v, 3) if call_v else None,
                "buckets": buckets,
                "build_notional": bn, "fresh_notional": fn,
                "unusual_notional": bn + fn,
                "top_ratio": max((buckets[b]["top_ratio"] for b in live), default=0),
                # excluded from the ranking, kept visible
                "financing_notional": round(fin_notional),
                "financing_contracts": fin_n,
                "financing_share": round(fin_notional / (fin_notional + bn + fn), 3)
                                   if (fin_notional + bn + fn) else 0,
            })
    return out, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data" / "tipsheet.json"))
    ap.add_argument("--cache", default=None, help="reuse/store raw CBOE chains here")
    a = ap.parse_args()
    rows, errors = scan(UNIVERSE, a.cache)
    # Rank by the dollars behind genuinely unusual activity, not by raw turnover.
    rows.sort(key=lambda r: -r["unusual_notional"])
    payload = {
        "scanned_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "universe_size": len(UNIVERSE), "returned": len(rows), "errors": errors,
        "params": {
            "contract_vol_floor": CONTRACT_VOL_FLOOR,
            "min_oi_for_ratio": MIN_OI_FOR_RATIO,
            "fresh_oi_ceiling": FRESH_OI_CEILING,
            "no_optionality_delta": NO_OPTIONALITY_DELTA,
            "no_optionality_vega": NO_OPTIONALITY_VEGA,
        },
        "rows": rows,
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(payload, indent=2))
    print(f"scanned {len(UNIVERSE)} tickers, {len(rows)} returned data, {len(errors)} errors")
    print(f"\n{'sym':>6} {'spot':>9} {'P/C':>6} {'build $':>13} {'fresh $':>13} "
          f"{'top x':>7} {'financing $':>13} {'fin%':>5}")
    print("-" * 82)
    for r in rows[:15]:
        print(f"{r['symbol']:>6} {r['spot']:9,.2f} {(r['put_call'] or 0):6.2f} "
              f"{r['build_notional']:13,.0f} {r['fresh_notional']:13,.0f} "
              f"{r['top_ratio']:7.1f} {r['financing_notional']:13,.0f} "
              f"{r['financing_share']*100:4.0f}%")
    if errors:
        print(f"\nerrors: {[e['symbol'] for e in errors]}")


if __name__ == "__main__":
    main()
