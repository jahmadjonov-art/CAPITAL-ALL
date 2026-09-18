#!/usr/bin/env python3
"""Daily volume history for the scanner universe, from Massive.

WHAT THIS ANSWERS, AND WHAT IT DOES NOT

  Answers: "is this STOCK's share volume unusual against its own recent
  history?" Two years are available, so this is a real distribution rather
  than a guess.

  Does NOT answer: "is this name's OPTION volume unusual against its own
  history?" — which is the question the tip sheet actually wants. That needs
  total option volume per underlying per day, and it is **not reachable from
  this API at any sane cost**. Measured 2026-09-16:

    - There is no grouped-daily endpoint for options (400); the stock one
      returns 12,580 rows in a single call, and no options equivalent exists.
    - Daily bars exist per CONTRACT, so a ticker's total would mean summing
      every contract that traded on every day — thousands of calls per ticker
      per window, against a per-minute cap.
    - Doing it at the contract level instead does not rescue it. Sampling 83
      standout contracts off a live tip sheet: **median history 5 days**, and
      essentially none had 30. Near-dated contracts have not existed long
      enough to have a history, and those are exactly the contracts the sheet
      is about. A percentile over 5 days is the denominator trap again.

  So option-volume history has to be **banked going forward** rather than
  backfilled — see `bank_option_volume()`. Nothing can recover the days before
  we started.

MATCH ON DATE, NEVER ON "LATEST". Massive's daily bars lag: at 17:05 ET on a
Wednesday the newest bar was Tuesday's. CBOE's option volume can therefore be a
different session from the newest stock bar. Comparing them as though they were
the same day silently mixes two dates.
"""
import json, datetime as dt, statistics
from pathlib import Path

import massive

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "history"
WINDOW = 126                  # trailing complete sessions ~ six months
MIN_SESSIONS = 60             # below this, report "not enough history", not a number
LOOKBACK_DAYS = 400


def load_daily(symbols, refresh=False, progress=True, fetch=True):
    """{symbol: {iso_date: volume}}, cached on disk between runs."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / "stock-daily.json"
    store = json.loads(f.read_text()) if f.exists() and not refresh else {}
    if not fetch:
        # Read-only: use whatever is already cached and fetch nothing. Lets a
        # rebuild run while a long backfill is still going, without two
        # processes writing the same file.
        return store, 0
    today = dt.date.today()
    start = (today - dt.timedelta(days=LOOKBACK_DAYS)).isoformat()
    fetched = 0
    for s in symbols:
        have = store.get(s, {})
        # refetch when the cache has nothing recent; the API is the cheap part
        newest = max(have) if have else None
        if newest and (today - dt.date.fromisoformat(newest)).days <= 1 and not refresh:
            continue
        try:
            bars = massive.daily_bars(s, start, today.isoformat())
        except Exception as e:
            print(f"  {s}: {type(e).__name__}: {str(e)[:60]}")
            continue
        have.update({dt.datetime.fromtimestamp(b["t"] / 1000, dt.timezone.utc)
                       .date().isoformat(): b["v"] for b in bars})
        store[s] = have
        fetched += 1
        # Save as we go. Writing only at the end means a slow or interrupted
        # run shows no progress and keeps nothing — the same failure shape as
        # the scheduled run that committed and never pushed.
        if fetched % 5 == 0:
            f.write_text(json.dumps(store))
            if progress:
                print(f"  history: {fetched} fetched, newest {s} {max(have)}", flush=True)
    f.write_text(json.dumps(store))
    return store, fetched


def context(store, symbol, session):
    """How unusual `session`'s share volume was for `symbol`.

    `session` is an ISO date — the session the option data describes, not
    whatever happens to be newest. Returns None when we cannot say, with the
    reason, rather than a number built on too little.
    """
    have = store.get(symbol) or {}
    if not have:
        return {"known": False, "why": "no history fetched"}
    used, offset = session, 0
    if session not in have:
        # Massive's daily bars lag: after the close, today's option volume is in
        # hand before today's share bar exists. Rather than either silently
        # comparing two different days or showing nothing, fall back to the
        # newest complete session and CARRY ITS DATE, so the page can print it.
        newest = max(have)
        if newest > session:
            return {"known": False, "why": f"no bar at or before {session}"}
        used = newest
        offset = (dt.date.fromisoformat(session) - dt.date.fromisoformat(used)).days
        if offset > 5:
            return {"known": False,
                    "why": f"newest bar {used} is {offset} days before {session}"}
    prior = sorted(d for d in have if d < used)[-WINDOW:]
    if len(prior) < MIN_SESSIONS:
        return {"known": False,
                "why": f"only {len(prior)} prior sessions, need {MIN_SESSIONS}"}
    vol = have[used]
    hist = [have[d] for d in prior]
    med = statistics.median(hist)
    return {
        "known": True, "session": used, "offset_days": offset, "volume": vol,
        "median": med, "sessions": len(hist),
        "x_median": round(vol / med, 2) if med else None,
        "pctile": round(100.0 * sum(1 for h in hist if h < vol) / len(hist), 1),
    }


def bank_option_volume(rows, session):
    """Append today's per-ticker option volume to a growing record.

    This is the only route to "is this name's option volume unusual for it",
    since that history cannot be bought or backfilled. One row per ticker per
    session; re-running the same session overwrites rather than duplicates.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / "option-volume.json"
    store = json.loads(f.read_text()) if f.exists() else {}
    for r in rows:
        store.setdefault(r["symbol"], {})[session] = {
            "vol": r["total_vol"], "oi": r["total_oi"],
            "call": r["call_vol"], "put": r["put_vol"],
        }
    f.write_text(json.dumps(store))
    depth = statistics.median([len(v) for v in store.values()]) if store else 0
    return len(store), int(depth)


def option_context(symbol, session):
    """Same question as `context`, but for option volume, off the banked record.
    Returns not-known until enough sessions have accumulated — which is honest,
    and is the whole reason the banking exists."""
    f = CACHE / "option-volume.json"
    if not f.exists():
        return {"known": False, "why": "nothing banked yet"}
    have = (json.loads(f.read_text()).get(symbol) or {})
    prior = sorted(d for d in have if d < session)
    if session not in have:
        return {"known": False, "why": f"{session} not banked"}
    if len(prior) < MIN_SESSIONS:
        return {"known": False,
                "why": f"{len(prior)} sessions banked, need {MIN_SESSIONS}",
                "banked": len(prior), "need": MIN_SESSIONS}
    hist = [have[d]["vol"] for d in prior[-WINDOW:]]
    med = statistics.median(hist)
    vol = have[session]["vol"]
    return {"known": True, "volume": vol, "median": med, "sessions": len(hist),
            "x_median": round(vol / med, 2) if med else None,
            "pctile": round(100.0 * sum(1 for h in hist if h < vol) / len(hist), 1)}
