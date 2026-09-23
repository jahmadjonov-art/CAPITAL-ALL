#!/usr/bin/env python3
"""Company value: what a business earns, against what its stock costs.

WHAT THIS ANSWERS
  Trailing P/E, actual earnings growth, PEG on that actual growth, and the
  quality measures that separate "cheap" from "cheap for a reason". From those
  it produces three lists: undervalued, overvalued, and worth watching.

WHAT IT CANNOT ANSWER, AND WHY
  Two of the three numbers in the video the owner sent are **forecasts**, not
  facts, and forecasts are a paid product:

    Forward P/E   needs analysts' estimate of next year's earnings per share.
    PEG           as popularly defined, needs analysts' estimated growth rate.

  Massive serves no estimates on this plan (checked 2026-09-23: the financials
  endpoints carry reported figures only; the analyst-insights endpoint returns
  "not entitled"). Yahoo's quote endpoints now require authentication and
  refuse anonymous requests. SEC EDGAR returns 403 from this container, and
  carries only reported actuals anyway.

  So **PEG here uses growth the company actually delivered**, not growth someone
  predicts it will. That is a different number from the video's and must never
  be presented as the same one. It is also the more honest of the two: delivered
  growth is a fact, forecast growth is an opinion with a decimal point on it.

THE DENOMINATOR TRAP, AGAIN
  P/E divides by earnings. A company earning $0.01 a share prints a P/E in the
  thousands — that is not "expensive", it is a rounding error in the
  denominator. The same shape of mistake has now bitten this repository three
  times (`KNOWLEDGE.md`). So a P/E is only reported where earnings are large
  enough for the ratio to mean something, and marginal earners are excluded from
  the rankings rather than topping them.

DATA, AND WHY IT IS CHEAP
  Prices     one grouped-daily request returns all ~12,600 US tickers.
  Financials bulk, ~109 companies per page, filtered to recent filings.
             They change once a quarter, so the cache is refreshed weekly.
  Neither needs the broker, so this runs in a scheduled session.
"""
import json, argparse, datetime as dt, statistics
from pathlib import Path
from collections import defaultdict

import re

import massive

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "fundamentals"

# --- thresholds, all stated rather than buried -------------------------------
MIN_TTM_EPS      = 0.50     # below this the P/E denominator is noise
MIN_PRIOR_EPS    = 0.25     # growth measured from a smaller base is not growth
HIGH_GROWTH      = 100.0    # above this, treat as a recovery, not a trend
COMMON_TICKER    = re.compile(r"^[A-Z]{1,5}$")   # excludes preferreds/warrants/units
# A net margin above 100% is not a wonderful business, it is a signal that the
# "revenue" line is not what this formula assumes. Mortgage REITs and some
# financials report net interest income there and book gains outside it, so the
# ratio compares two things that do not divide. Three of them (DX 279% margin,
# NLY 181%, MFA) topped the undervalued list before this check existed. This
# excludes rows where the arithmetic is broken, not a sector.
MAX_PLAUSIBLE_MARGIN = 100.0
MAX_PLAUSIBLE_REV_GROWTH = 300.0
MIN_DOLLAR_VOL   = 5e6      # $5M a day: you can actually get in and out
MIN_PRICE        = 5.00     # avoids penny-stock artefacts
CHEAP_PE         = 15.0     # the video's bands, kept deliberately
FAIR_PE          = 20.0
PRICEY_PE        = 40.0
EXPENSIVE_PE     = 50.0


def band(pe):
    if pe is None:        return "unknown"
    if pe < CHEAP_PE:     return "cheap"
    if pe < FAIR_PE:      return "fair"
    if pe < PRICEY_PE:    return "pricey"
    return "expensive"


def _rows(timeframe, since, max_pages, progress):
    """Page the bulk financials endpoint for one timeframe."""
    out, cur, pages = [], None, 0
    while pages < max_pages:
        kw = {"limit": 100, "timeframe": timeframe, "filing_date.gte": since}
        if cur: kw["cursor"] = cur
        d = massive.get("/vX/reference/financials", **kw)
        rows = d.get("results") or []
        out.extend(rows)
        pages += 1
        if progress and pages % 20 == 0:
            print(f"  {timeframe}: {pages} pages, {len(out)} rows", flush=True)
        nxt = d.get("next_url")
        if not nxt: break
        cur = nxt.split("cursor=")[-1].split("&")[0]
    return out, pages


def refresh_financials(since="2024-06-01", max_pages=900, progress=True):
    """Cache what each company earns, from two windows that are each internally
    consistent and never mixed:

      TTM     the trailing twelve months — what the P/E is computed against.
      annual  whole fiscal years — what growth is computed from, so the compare
              is like for like. TTM against a fiscal year would be two different
              windows dressed up as one, which is the date-mixing mistake this
              repository has already made once with option and share volume.

    The endpoint hands both back directly, so nothing here sums quarters. An
    earlier version did, discovered the filter returned only each company's most
    recent quarter, and produced a screen of exactly zero companies.
    """
    CACHE.mkdir(parents=True, exist_ok=True)

    def num(x, stmt, key):
        v = ((x.get("financials", {}).get(stmt) or {}).get(key) or {}).get("value")
        return float(v) if v is not None else None

    store = {}
    ttm_rows, p1 = _rows("ttm", since, max_pages, progress)
    for x in ttm_rows:
        for tk in (x.get("tickers") or []):
            store.setdefault(tk, {})["ttm"] = {
                "eps": num(x, "income_statement", "diluted_earnings_per_share"),
                "rev": num(x, "income_statement", "revenues"),
                "ni":  num(x, "income_statement", "net_income_loss"),
                "shares": num(x, "income_statement", "diluted_average_shares"),
                "end": x.get("end_date"), "name": x.get("company_name"),
            }
    ann_rows, p2 = _rows("annual", since, max_pages, progress)
    for x in ann_rows:
        rec = {
            "fy": x.get("fiscal_year"), "end": x.get("end_date"),
            "eps": num(x, "income_statement", "diluted_earnings_per_share"),
            "rev": num(x, "income_statement", "revenues"),
            "ni":  num(x, "income_statement", "net_income_loss"),
            "shares": num(x, "income_statement", "diluted_average_shares"),
            "name": x.get("company_name"),
        }
        for tk in (x.get("tickers") or []):
            store.setdefault(tk, {}).setdefault("annual", []).append(rec)
    for tk, v in store.items():
        if "annual" in v:
            seen, keep = set(), []
            for r in sorted(v["annual"], key=lambda r: r["end"] or "", reverse=True):
                if r["end"] in seen: continue
                seen.add(r["end"]); keep.append(r)
            v["annual"] = keep

    (CACHE / "financials.json").write_text(json.dumps(store))
    return store, p1 + p2


def refresh_prices(day=None):
    """One request: every US ticker's close and volume for a trading day."""
    CACHE.mkdir(parents=True, exist_ok=True)
    d0 = dt.date.fromisoformat(day) if day else dt.date.today()
    for back in range(0, 7):
        # Walk back over weekends, holidays, and today — a grouped-daily request
        # for a session that has not settled yet answers 403, which reads as
        # "not entitled" and is really "not yet". Treat both as "try yesterday".
        date = (d0 - dt.timedelta(days=back)).isoformat()
        try:
            d = massive.get(f"/v2/aggs/grouped/locale/us/market/stocks/{date}")
        except massive.NotEntitled:
            continue
        rows = d.get("results") or []
        if rows:
            px = {x["T"]: {"close": x["c"], "vol": x["v"], "vwap": x.get("vw")}
                  for x in rows}
            (CACHE / "prices.json").write_text(json.dumps({"date": date, "px": px}))
            return date, px
    raise SystemExit("no trading day with data in the last week")


def metrics(store, px):
    """Per-ticker valuation and quality, on ONE consistent window.

    Everything is computed from complete fiscal years: the P/E from the latest
    one, growth from that year against the one before it. That keeps the whole
    row like-for-like.

    An earlier version priced off the trailing twelve months, which is fresher
    and would have been better — except that Massive publishes a TTM row for
    only 281 of 6,161 companies against 3,457 with two full years, so ranking on
    it screened 99 companies and called that the market. Where a TTM figure does
    exist it is carried as `eps_ttm` for reference and is deliberately NOT used
    in any ranking: mixing the two windows row by row would make the P/E column
    mean different things on different lines.

    The cost is staleness — a fiscal year can be eleven months old — so every
    row carries the year it came from and the page prints it.
    """
    out = []
    for t, v in store.items():
        # Common stock only. Preferreds, warrants and units carry the parent's
        # earnings per share against their own unrelated price, which produces a
        # meaningless ratio — BACpL, a Bank of America preferred, came second on
        # the overvalued list before this filter existed.
        if not COMMON_TICKER.match(t): continue
        ann = v.get("annual") or []
        if len(ann) < 2: continue
        a0, a1 = ann[0], ann[1]
        eps, rev = a0.get("eps"), a0.get("rev")
        if eps is None: continue

        p = px.get(t)
        if not p or not p.get("close"): continue
        price = float(p["close"]); dollar_vol = price * float(p.get("vol") or 0)
        if price < MIN_PRICE or dollar_vol < MIN_DOLLAR_VOL: continue

        pe = price / eps if eps > 0 else None

        # Growth needs a real base. A company going from $0.03 to $0.24 a share
        # prints 700% growth and a PEG near zero, which then tops any PEG-ranked
        # list — the same denominator trap as the P/E one, moved into the growth
        # term, and how a value screen fills with one-off rebounds.
        eps_growth = rev_growth = None
        if a1.get("eps") and a1["eps"] >= MIN_PRIOR_EPS and eps > 0:
            eps_growth = (eps / a1["eps"] - 1) * 100
        if a1.get("rev") and a1["rev"] > 0 and rev:
            rev_growth = (rev / a1["rev"] - 1) * 100

        ttm = v.get("ttm") or {}
        margin = (a0["ni"] / rev * 100) if (a0.get("ni") is not None and rev) else None

        recovery = eps_growth is not None and eps_growth > HIGH_GROWTH
        peg = (pe / eps_growth
               if (pe and eps_growth and 0 < eps_growth <= HIGH_GROWTH) else None)
        sh = a0.get("shares") or ttm.get("shares")
        mcap = price * sh if sh else None

        out.append({
            "ticker": t, "name": ttm.get("name") or a0.get("name"),
            "price": round(price, 2),
            "eps": round(eps, 2),
            "eps_ttm": round(ttm["eps"], 2) if ttm.get("eps") is not None else None,
            "fiscal_year": a0.get("fy"), "fy_end": a0.get("end"),
            "pe": round(pe, 1) if pe else None,
            "band": band(pe),
            "eps_growth": round(eps_growth, 1) if eps_growth is not None else None,
            "rev_growth": round(rev_growth, 1) if rev_growth is not None else None,
            "growth_years": f"FY{a1.get('fy')}\u2192FY{a0.get('fy')}",
            "margin": round(margin, 1) if margin is not None else None,
            "peg": round(peg, 2) if peg else None,
            "mcap": round(mcap) if mcap else None,
            "dollar_vol": round(dollar_vol),
            "thin_earnings": eps < MIN_TTM_EPS,
            "recovery": recovery,
            "implausible": bool(
                (margin is not None and abs(margin) > MAX_PLAUSIBLE_MARGIN)
                or (rev_growth is not None and rev_growth > MAX_PLAUSIBLE_REV_GROWTH)),
        })
    return out


# --- the screen ---------------------------------------------------------------
#
# "Great stocks that are undervalued" is two claims, not one. Cheap is easy to
# measure and easy to be fooled by: the cheapest stocks on any screen are mostly
# cheap because the business is shrinking, and buying those is how value screens
# earn their bad name. So quality is a GATE, applied before price is considered
# at all — a company must be profitable, growing, and earning a real margin
# before its P/E is allowed to make it interesting.

QUALITY = {
    "profitable":   lambda r: r["eps"] > MIN_TTM_EPS,
    "growing":      lambda r: (r["rev_growth"] or -99) > 0,
    "earns_more":   lambda r: (r["eps_growth"] or -99) > 0,
    "real_margin":  lambda r: (r["margin"] or -99) >= 5.0,
    "liquid":       lambda r: r["dollar_vol"] >= MIN_DOLLAR_VOL,
}


def quality(r):
    """Which gates a company passes, and how many."""
    passed = {k: f(r) for k, f in QUALITY.items()}
    return passed, sum(passed.values())


def screen(rows, n=10):
    """Three lists, each with its reason for existing."""
    for r in rows:
        r["quality_passed"], r["quality_score"] = quality(r)

    graded = [r for r in rows
              if r["pe"] and not r["thin_earnings"] and not r["implausible"]]

    # UNDERVALUED — every quality gate passed, then ranked by price paid per
    # unit of delivered growth (PEG), falling back to plain P/E where growth is
    # unmeasurable. A low P/E alone is not enough to appear here.
    under = [r for r in graded if r["quality_score"] == len(QUALITY)
             and r["pe"] < FAIR_PE]
    under.sort(key=lambda r: (r["peg"] if r["peg"] else r["pe"] / 10))

    # OVERVALUED — priced past the video's "expensive" line. Deliberately NOT
    # quality-gated: an expensive great company and an expensive bad one are
    # both expensive, and the difference is shown rather than filtered.
    over = [r for r in graded if r["pe"] >= EXPENSIVE_PE]
    over.sort(key=lambda r: -r["pe"])

    # WORTH WATCHING — good businesses that are merely fairly priced, or cheap
    # ones failing exactly one gate. Not recommendations: the list of things
    # that would become interesting on a price fall or one better quarter.
    watch = [r for r in graded
             if (r["quality_score"] == len(QUALITY) and FAIR_PE <= r["pe"] < PRICEY_PE)
             or (r["quality_score"] == len(QUALITY) - 1 and r["pe"] < FAIR_PE)]
    watch.sort(key=lambda r: (-(r["quality_score"]), r["pe"]))

    return {"undervalued": under[:n], "overvalued": over[:n], "watch": watch[:n]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true",
                    help="refetch financials (slow; they only change quarterly)")
    ap.add_argument("--since", default="2025-01-01")
    ap.add_argument("--out", default=str(ROOT / "data" / "value.json"))
    ap.add_argument("-n", type=int, default=10)
    a = ap.parse_args()

    fin_path = CACHE / "financials.json"
    if a.refresh or not fin_path.exists():
        print("fetching financials (bulk, cached — only needed weekly)...")
        store, pages = refresh_financials(since=a.since)
        print(f"  {len(store)} tickers from {pages} pages")
    else:
        store = json.loads(fin_path.read_text())
        print(f"financials: {len(store)} tickers from cache")

    date, px = refresh_prices()
    print(f"prices: {len(px):,} tickers, session {date}")

    rows = metrics(store, px)
    print(f"computed: {len(rows)} companies with enough data to value")

    lists = screen(rows, a.n)
    payload = {
        "built_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "price_session": date,
        "universe": len(rows),
        "thresholds": {"cheap_pe": CHEAP_PE, "fair_pe": FAIR_PE,
                       "pricey_pe": PRICEY_PE, "expensive_pe": EXPENSIVE_PE,
                       "min_ttm_eps": MIN_TTM_EPS, "min_dollar_volume": MIN_DOLLAR_VOL},
        "peg_basis": "delivered earnings growth, not analyst forecast",
        "lists": lists,
        # Every company that could be valued, ticker order. The three lists
        # above are a starting point; this is the thing to actually look through.
        "all": sorted(
            [r for r in rows if r["pe"] and not r["thin_earnings"]
             and not r["implausible"]],
            key=lambda r: r["ticker"]),
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(payload, indent=2))

    for label in ("undervalued", "overvalued", "watch"):
        print(f"\n=== {label.upper()} ===")
        print(f"{'':>6} {'price':>9} {'P/E':>7} {'PEG':>6} {'EPS gr':>8} "
              f"{'rev gr':>8} {'margin':>7}  name")
        def fmt(v, w, suffix=""):
            # A missing number is printed as a dash, never as zero. "PEG 0.00"
            # reads as "spectacularly cheap"; it meant "not computable".
            return f"{'—':>{w}}" if v is None else f"{v:>{w}.2f}{suffix}" if not suffix \
                   else f"{v:>{w-1}.1f}{suffix}"
        for r in lists[label]:
            flag = " recovery" if r.get("recovery") else ""
            print(f"{r['ticker']:>6} {r['price']:9,.2f} {r['pe']:7.1f} "
                  f"{fmt(r['peg'],6)} {fmt(r['eps_growth'],8,'%')} "
                  f"{fmt(r['rev_growth'],8,'%')} {fmt(r['margin'],7,'%')}  "
                  f"{(r['name'] or '')[:30]}{flag}")


if __name__ == "__main__":
    main()
