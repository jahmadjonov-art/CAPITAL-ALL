#!/usr/bin/env python3
"""Build the live desk console: market price against model fair value.

Every number is fetched at build time from public APIs and computed here.
Nothing is simulated, nothing is a placeholder, and no order is ever placed.
Where the model is known to be wrong, the page says so on its face.

Usage: python3 dashboard/desk.py
"""
import json, math, statistics, urllib.request, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard" / "desk.html"
KAL = "https://api.elections.kalshi.com/trade-api/v2"


def j(url):
    r = urllib.request.Request(url, headers={"User-Agent": "capital-all-research/1.0"})
    with urllib.request.urlopen(r, timeout=30) as f:
        return json.load(f)


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# ---------------------------------------------------------------- spot ----
spot, errs = {}, []
for name, url, pick in [
    ("Kraken", "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
     lambda d: float(list(d["result"].values())[0]["c"][0])),
    ("Coinbase", "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
     lambda d: float(d["price"])),
    ("Binance.US", "https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT",
     lambda d: float(d["price"])),
]:
    try:
        spot[name] = pick(j(url))
    except Exception as e:
        errs.append(f"{name}: {type(e).__name__}")

S = statistics.median(spot.values()) if spot else None
disagree = (max(spot.values()) - min(spot.values())) if len(spot) > 1 else None

# ------------------------------------------------------ realised vol ----
sd_min, nbars = None, 0
try:
    o = j("https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=1")
    closes = [float(b[4]) for b in list(o["result"].values())[0]][-180:]
    rets = [math.log(closes[i] / closes[i - 1])
            for i in range(1, len(closes)) if closes[i - 1] > 0]
    sd_min, nbars = statistics.pstdev(rets), len(rets)
except Exception as e:
    errs.append(f"vol: {type(e).__name__}")

# ------------------------------------------------------- contracts ------
now = dt.datetime.now(dt.timezone.utc)
rows = []
for series in ("KXBTC15M", "KXBTCD"):
    try:
        mk = j(f"{KAL}/markets?series_ticker={series}&status=open&limit=40")["markets"]
    except Exception as e:
        errs.append(f"{series}: {type(e).__name__}")
        continue
    for m in mk:
        try:
            ct = dt.datetime.fromisoformat(m["close_time"].replace("Z", "+00:00"))
            mins = (ct - now).total_seconds() / 60
            k = m.get("floor_strike") or m.get("cap_strike")
            bid = float(m.get("yes_bid_dollars") or 0)
            ask = float(m.get("yes_ask_dollars") or 0)
            vol = float(m.get("volume_24h_fp") or 0)
            if k is None or mins <= 0 or not (bid and ask):
                continue
            k = float(k)
            sig = sd_min * math.sqrt(mins)
            if sig <= 0:
                continue
            fair = norm_cdf((math.log(S / k) - 0.5 * sig * sig) / sig)
            mid = (bid + ask) / 2
            rows.append({"series": series, "ticker": m["ticker"], "strike": k,
                         "mins": round(mins, 1), "bid": bid, "ask": ask,
                         "mid": round(mid, 4), "fair": round(fair, 4),
                         "gap": round(fair - mid, 4), "vol": vol,
                         "spread": round((ask - bid) * 100, 1)})
        except Exception:
            continue
rows.sort(key=lambda r: (r["series"], r["strike"]))

DATA = {
    "built": dt.datetime.now().strftime("%d %b %Y  %H:%M:%S"),
    "built_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "spot": spot, "median": S, "disagree": disagree,
    "sd_min": sd_min, "ann_vol": (sd_min * math.sqrt(525600)) if sd_min else None,
    "nbars": nbars, "rows": rows, "errors": errs,
}
tpl = (ROOT / "dashboard" / "desk_template.html").read_text()
OUT.write_text(tpl.replace("/*__DESK__*/null", json.dumps(DATA, indent=2)))
print(f"built {OUT.relative_to(ROOT)}")
print(f"  spot ${S:,.2f}  vol {DATA['ann_vol']*100:.1f}%  contracts {len(rows)}"
      + (f"  errors: {errs}" if errs else ""))
