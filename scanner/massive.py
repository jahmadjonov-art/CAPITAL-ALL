#!/usr/bin/env python3
"""Thin client for the Massive (formerly Polygon.io) market data API.

THE KEY NEVER LIVES IN THIS REPOSITORY. It is read from the environment:

    export MASSIVE_API_KEY="..."

For a scheduled run, set it in the Routine's environment variables — the same
settings page where the repository and connectors are attached
(`thoughts/4-walls.md`). A key committed to git is a key that has to be
reissued, and this repository is the owner's, not a private scratchpad.

WHAT THIS PLAN IS ENTITLED TO — measured 2026-09-16, not read off a pricing page
  yes  /v3/reference/options/contracts   contract reference
  yes  /v3/snapshot/options/{ticker}     full chain: strike, expiry, OI, day volume
  yes  /v2/aggs/ticker/{t}/range/...     DAILY BARS, stocks and individual option
                                         contracts, about two years back
  no   /v3/trades/...                    tick data — "not entitled"
  no   /v2/last/nbbo/...                 real-time quotes — "not entitled"
  no   greeks                            the snapshot returns `greeks: {}` and a
                                         null implied_volatility on this plan

SO IT COMPLEMENTS CBOE RATHER THAN REPLACING IT
  CBOE   today's chain WITH greeks, free, no key. Needed for anything involving
         delta, gamma or vega — including the tip sheet's zero-optionality
         filter. No history at all.
  Massive  history, which CBOE has none of, and which is the thing that unblocks
         every question of the form "is this unusual for THIS name?"

RATE LIMIT
  There is a per-minute cap. Its exact size has not been measured — an attempt to
  measure it by hammering one endpoint was correctly refused as credential
  probing, and it is better established from real use than from a benchmark.
  Exceeding it returns HTTP 429, or a 200 whose body carries status ERROR and
  "exceeded the maximum requests per minute".

  **A rate limit and a missing entitlement look almost identical.** Both can
  arrive as a non-200, and both surface under `status` values that have been
  seen to disagree with the body's message. `get()` below retries through the
  cap so the two can never be confused. Anything that skips that will eventually
  report "your plan does not include X" about data the plan does include.
"""
import json, os, time, urllib.request, urllib.error

BASE = "https://api.polygon.io"          # massive.com still serves on this host


class NotEntitled(RuntimeError):
    """The plan genuinely does not cover this — distinct from being throttled."""


def key():
    k = os.environ.get("MASSIVE_API_KEY")
    if not k:
        raise SystemExit(
            "MASSIVE_API_KEY is not set.\n"
            "  export MASSIVE_API_KEY='...'   (never commit it)\n"
            "See the header of scanner/massive.py.")
    return k


def get(path, tries=6, pause=13, **params):
    """GET a Massive endpoint, retrying through the per-minute cap.

    Raises NotEntitled for a genuine plan limit, so a caller can tell the two
    apart without parsing error strings itself.
    """
    params["apiKey"] = key()
    url = f"{BASE}{path}?" + "&".join(f"{k}={v}" for k, v in params.items())
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as f:
                d = json.load(f)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(pause); continue
            if e.code == 403:
                raise NotEntitled(f"403 on {path}")
            raise
        err = str(d.get("error", ""))
        if "exceeded the maximum requests" in err:
            time.sleep(pause); last = err; continue
        if "not entitled" in err.lower():
            raise NotEntitled(err)
        return d
    raise RuntimeError(f"rate limited throughout {tries} attempts: {last}")


def daily_bars(ticker, start, end, limit=50000):
    """Daily OHLCV. `ticker` is 'AAPL' or an option id like
    'O:AAPL270115C00300000'. Bars carry v (volume), vw (vwap), o/h/l/c,
    t (ms epoch) and n (number of trades). About two years available."""
    d = get(f"/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}", limit=limit)
    return d.get("results", []) or []


def chain_snapshot(underlying, limit=250):
    """Today's full option chain: strike, expiry, open interest, day volume.
    Pages through `next_url`. No greeks on this plan — use CBOE for those."""
    out, path = [], f"/v3/snapshot/options/{underlying}"
    params = {"limit": limit}
    while True:
        d = get(path, **params)
        out.extend(d.get("results", []) or [])
        nxt = d.get("next_url")
        if not nxt:
            return out
        cur = nxt.split("cursor=")[-1].split("&")[0]
        params = {"limit": limit, "cursor": cur}


if __name__ == "__main__":
    import sys
    sym = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    bars = daily_bars(sym, "2026-08-01", "2026-09-15")
    print(f"{sym}: {len(bars)} daily bars")
    if bars:
        b = bars[-1]
        print(f"  last: close {b['c']}  volume {b['v']:,}  trades {b.get('n', 0):,}")
