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
import json, re, argparse, datetime as dt, random, time
import urllib.request, urllib.error
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
BAC JPM GS WFC C SCHW V MA PYPL XYZ
XOM CVX OXY SLB FCX NEM GLD SLV USO UNG
SPY QQQ IWM DIA TLT HYG XLF XLE SMH ARKK
BA GE CAT DE UPS FDX DAL UAL AAL CCL
DIS WBD PSKY ROKU SNAP PINS UBER LYFT ABNB DASH
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


# CBOE rate-limits. Eight workers with no backoff got a clean 70/70 one morning
# and 429s on 23 of 70 the next, which is the worst possible failure mode: the
# run "succeeds", a third of the universe is quietly missing, and the ranking is
# over whatever happened to get through. Four workers with backoff, and a
# coverage check at the end that refuses to write a thin scan.
WORKERS = 4
RETRIES = 4
BACKOFF = 2.0                 # seconds, doubling
MIN_COVERAGE = 0.9            # refuse to write a scan missing more than a tenth
MAX_FEED_AGE_DAYS = 4         # Fri close read on Mon is 3; beyond that it is a dead symbol


def feed_age(ts, today):
    """Days between the feed's own timestamp and today. None if unreadable."""
    try:
        return (today - dt.datetime.fromisoformat(str(ts)).date()).days
    except Exception:
        return None


def fetch(sym, cache=None):
    if cache:
        p = Path(cache) / f"{sym}.json"
        if p.exists():
            return sym, json.loads(p.read_text())
    last = "no attempt"
    for attempt in range(RETRIES):
        try:
            r = urllib.request.Request(CBOE.format(sym),
                                       headers={"User-Agent": "research/1.0"})
            with urllib.request.urlopen(r, timeout=45) as f:
                raw = json.load(f)
            d = raw["data"]
            d["_feed_ts"] = raw.get("timestamp")
            break
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code not in (429, 500, 502, 503, 504):
                return sym, {"_error": f"HTTPError: {e}"}
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        if attempt < RETRIES - 1:
            time.sleep(BACKOFF * (2 ** attempt) * (0.5 + random.random()))
    else:
        return sym, {"_error": f"{last} after {RETRIES} attempts"}
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
    out, errors, feed_ts = [], [], []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for sym, d in ex.map(lambda s: fetch(s, cache), universe):
            if "_error" in d:
                errors.append({"symbol": sym, "error": d["_error"]}); continue
            # CBOE keeps serving the last file it ever wrote for a delisted or
            # renamed symbol, with a 200 and no warning. SQ (now XYZ) was still
            # returning a full chain from 2025-01-21 and being ranked on it.
            # The feed stamps its own age, so check it.
            age = feed_age(d.get("_feed_ts"), today)
            if age is None or age > MAX_FEED_AGE_DAYS:
                errors.append({"symbol": sym,
                               "error": f"stale feed: {d.get('_feed_ts')} "
                                        f"({'unparseable' if age is None else f'{age} days old'})"})
                continue
            spot = float(d.get("current_price") or 0)
            tot_v = tot_oi = call_v = put_v = 0.0
            last_trade = ""
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
                # The session this volume belongs to, taken from the tape rather
                # than the clock. A pre-open run reports the PREVIOUS session,
                # and only the trades themselves know which one that is.
                if v:
                    lt = str(o.get("last_trade_time") or "")
                    if lt > last_trade: last_trade = lt
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
            if d.get("_feed_ts"): feed_ts.append(str(d["_feed_ts"]))

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
                "session": last_trade[:10],
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
    return out, errors, feed_ts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data" / "tipsheet.json"))
    ap.add_argument("--cache", default=None, help="reuse/store raw CBOE chains here")
    ap.add_argument("--cached-history", action="store_true",
                    help="use the cached volume history only; fetch nothing")
    ap.add_argument("--no-history", action="store_true",
                    help="skip the Massive volume-history lookup")
    ap.add_argument("--force", action="store_true",
                    help="write even if the scan is missing part of the universe")
    a = ap.parse_args()
    rows, errors, feed_ts = scan(UNIVERSE, a.cache)
    # Rank by the dollars behind genuinely unusual activity, not by raw turnover.
    rows.sort(key=lambda r: -r["unusual_notional"])
    # Volume history: how unusual was this session, for this name?
    session, banked_depth = "", 0
    if rows:
        from collections import Counter
        session = Counter(r["session"] for r in rows if r["session"]).most_common(1)[0][0]
    if session and not a.no_history:
        try:
            import history
            store, fetched = history.load_daily([r["symbol"] for r in rows],
                                                fetch=not a.cached_history)
            for r in rows:
                r["stock_context"] = history.context(store, r["symbol"], session)
            n, depth = history.bank_option_volume(rows, session)
            banked_depth = depth
            for r in rows:
                r["option_context"] = history.option_context(r["symbol"], session)
            known = sum(1 for r in rows if (r.get("stock_context") or {}).get("known"))
            print(f"history: session {session}, {fetched} fetched, "
                  f"{known}/{len(rows)} tickers have share-volume context; "
                  f"option volume banked for {n} tickers (median {depth} sessions)")
        except SystemExit as e:
            print(f"history skipped: {e}")
        except Exception as e:
            print(f"history skipped: {type(e).__name__}: {e}")

    payload = {
        "scanned_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "universe_size": len(UNIVERSE), "returned": len(rows), "errors": errors,
        "coverage": round(len(rows) / len(UNIVERSE), 3),
        # The feed stamps its own age. This is what the numbers describe;
        # scanned_utc is only when we asked.
        "session": session,
        "banking": {"tickers": len(rows), "depth": banked_depth,
                    "need": 60} if session else None,
        "feed_latest": max(feed_ts) if feed_ts else None,
        "feed_earliest": min(feed_ts) if feed_ts else None,
        "params": {
            "contract_vol_floor": CONTRACT_VOL_FLOOR,
            "min_oi_for_ratio": MIN_OI_FOR_RATIO,
            "fresh_oi_ceiling": FRESH_OI_CEILING,
            "no_optionality_delta": NO_OPTIONALITY_DELTA,
            "no_optionality_vega": NO_OPTIONALITY_VEGA,
        },
        "rows": rows,
    }
    coverage = len(rows) / len(UNIVERSE)
    print(f"scanned {len(UNIVERSE)} tickers, {len(rows)} returned data, "
          f"{len(errors)} errors  ({coverage:.0%} coverage)")
    if coverage < MIN_COVERAGE and not a.force:
        print(f"\nREFUSING TO WRITE: coverage {coverage:.0%} is below "
              f"{MIN_COVERAGE:.0%}. A ranking over a partial universe is not a "
              f"ranking of the market — it ranks whatever got through.\n"
              f"missing: {', '.join(e['symbol'] for e in errors)}\n"
              f"Re-run (the old {Path(a.out).name} is untouched), or pass "
              f"--force if a thin scan is genuinely what you want.")
        raise SystemExit(1)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(payload, indent=2))
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
