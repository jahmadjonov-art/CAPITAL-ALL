#!/usr/bin/env python3
"""Build the public website from the repository's own records.

Everything on the site is read from the repository at build time. The markdown
record is rendered as it stands, and the five dashboards are the exact files
their own build scripts produced — this script never regenerates them, because
some of them need live market data or a captured snapshot that CI cannot reach.
Nothing is transcribed by hand, so the site cannot quietly disagree with the
record it is showing.

Pages link to each other with relative URLs, so the same output works at the
repository root, under /CAPITAL-ALL/office/, or opened straight off disk.

Usage: python3 site/build.py [--out DIR]
"""
import argparse
import datetime
import html
import re
import subprocess
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent

# Directories whose markdown is not part of the research record. `legacy/` is
# the archived trucking app and has its own live site; it is not published here.
SKIP_DIRS = {".git", "node_modules", "legacy", "dist", "__pycache__", "site"}

REPO = "jahmadjonov-art/CAPITAL-ALL"


def git(*args, default=""):
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                           text=True, timeout=15)
        return r.stdout.strip() or default
    except Exception:
        return default


def read(rel):
    p = ROOT / rel
    return p.read_text() if p.exists() else ""


# ------------------------------------------------------------------ the record
# Every markdown file in the repository becomes a page, discovered rather than
# listed, so a new record published by a session appears here with no edit.

SECTIONS = [
    ("", "Start here", "The goal, the ground rules, and the one page every "
                       "session reads before anything else."),
    ("research", "The whiteboard", "What we currently believe, on what "
                                   "evidence, and every experiment that was "
                                   "actually run."),
    ("thoughts", "The message board", "Durable traps, the decisions that "
                                      "mattered, where sessions got stuck, and "
                                      "what went wrong."),
    ("sandbox", "Open ground", "Work staked out but not built. Anyone can pick "
                               "one up without asking."),
    ("strategies", "Strategy library", "One extraction per source. Every claim "
                                       "starts untested and moves only when an "
                                       "experiment says so."),
    ("scanner", "The scanners", "The scripts that go and fetch market data."),
    (".claude", "House rules", "How a session is run, and the specialists it "
                               "can call on."),
]
SECTION_ORDER = {key: i for i, (key, _, _) in enumerate(SECTIONS)}


def discover():
    """Every markdown file in the record, as a page with a stable URL."""
    pages = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        text = p.read_text()
        title = re.search(r"^#\s+(.+?)\s*$", text, re.M)
        top = rel.parts[0] if len(rel.parts) > 1 else ""
        pages.append({
            "src": rel,
            "text": text,
            "url": "read/" + str(rel.with_suffix("")).lower() + "/",
            "title": (title.group(1) if title else rel.stem).strip(),
            "section": top if top in SECTION_ORDER else "",
            "updated": git("log", "-1", "--format=%cs", "--", str(rel)),
            "words": len(text.split()),
        })
    pages.sort(key=lambda pg: (SECTION_ORDER.get(pg["section"], 99),
                               str(pg["src"]).lower()))
    return pages


# --------------------------------------------------------------- the dashboards
# Built elsewhere, published as they are. `desk` needs live APIs and `surface`
# needs a snapshot captured through broker tools, so CI cannot rebuild either —
# what ships is what the last session that ran them committed.

DASHBOARDS = [
    ("floor-plan", "Floor plan", "dashboard/office.html",
     "The firm at a glance — who is at which desk, what is on the whiteboard, "
     "and what ground is staked out.", "◳"),
    ("desk", "Fair value desk", "dashboard/desk.html",
     "Live Bitcoin contracts against the model's fair value, with the model's "
     "known faults stated on its face.", "◑"),
    ("strategies", "Strategy library", "dashboard/strategies.html",
     "One tab per source, every claim carrying whether it has been tested.", "▤"),
    ("surface", "Volatility surface", "dashboard/surface.html",
     "The implied volatility smile and dealer gamma by strike, from a captured "
     "option snapshot.", "◠"),
    ("tipsheet", "Tip sheet", "dashboard/tipsheet.html",
     "Unusual option volume, split by day, week and month.", "◈"),
]


# ------------------------------------------------------------------- rendering

def md_to_html(text):
    return markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False}},
    ).convert(text)


def section_body(text, heading):
    """Body of a '## heading' section, up to the next '## '."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)",
                  text, re.M | re.S)
    return m.group(1).strip() if m else ""


def relative(from_url, to_url):
    """A link from one page of this site to another, with no base path baked in."""
    depth = len([s for s in from_url.split("/") if s])
    return ("../" * depth) + to_url


def rewrite_links(body, src, page_url, by_path):
    """Point the record's own markdown links at the published pages.

    A link to another `.md` becomes the page it was rendered into; a link to a
    directory becomes its README; anything else that exists in the repository
    becomes a link to the file on GitHub. A link that resolves to nothing is
    left exactly as written rather than quietly pointed somewhere plausible.
    """
    base = (ROOT / src).parent

    def fix(m):
        quote, href = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|//)", href):
            return m.group(0)
        path, _, frag = href.partition("#")
        frag = f"#{frag}" if frag else ""
        if not path:
            return m.group(0)
        try:
            target = (base / path).resolve().relative_to(ROOT)
        except (ValueError, OSError):
            return m.group(0)
        key = str(target)
        if key in by_path:
            return f'href={quote}{relative(page_url, by_path[key]["url"])}{frag}{quote}'
        if f"{key}/README.md" in by_path:
            return (f'href={quote}'
                    f'{relative(page_url, by_path[f"{key}/README.md"]["url"])}{frag}{quote}')
        if (ROOT / target).exists():
            return f'href={quote}https://github.com/{REPO}/blob/main/{key}{frag}{quote}'
        return m.group(0)

    return re.sub(r'href=(["\'])(.*?)\1', fix, body)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600'
         '&family=Spectral:wght@500;600&display=swap">')

PALETTE = """
:root{
  --paper:#FBFAF7; --panel:#FFFFFF; --sunk:#F1EEE8;
  --ink:#16212B; --ink-2:#41505E; --ink-3:#75838F;
  --rule:#DFD9CE; --rule-2:#EBE6DC;
  --brass:#A8762E; --brass-soft:#EFE2CB;
  --up:#2E7A58; --down:#AF3F2E;
  --shadow:0 1px 2px rgba(22,33,43,.06),0 8px 24px -12px rgba(22,33,43,.18);
  color-scheme:light dark;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#111A22; --panel:#172330; --sunk:#1E2C39;
    --ink:#E7EDF2; --ink-2:#A9B8C4; --ink-3:#7C8B98;
    --rule:#2A3B49; --rule-2:#223341;
    --brass:#D3A257; --brass-soft:#3A2F1C;
    --up:#4FA97E; --down:#DD6A55;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -14px rgba(0,0,0,.6);
  }
}
:root[data-theme="dark"]{
  --paper:#111A22; --panel:#172330; --sunk:#1E2C39;
  --ink:#E7EDF2; --ink-2:#A9B8C4; --ink-3:#7C8B98;
  --rule:#2A3B49; --rule-2:#223341;
  --brass:#D3A257; --brass-soft:#3A2F1C;
  --up:#4FA97E; --down:#DD6A55;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -14px rgba(0,0,0,.6);
}
"""

# The bar sits on top of pages with their own stylesheets, including one that is
# near-black. Every rule is scoped to #sitebar and carries id specificity, so a
# page's own `a{}` or `nav{}` rules cannot reach inside it.
BAR_CSS = """
#sitebar{
  position:sticky; top:0; z-index:9999;
  display:flex; flex-wrap:wrap; gap:4px 18px; align-items:baseline;
  padding:10px 20px; margin:0;
  background:#16212B; border-bottom:1px solid #2A3B49;
  font:500 12px/1.5 "IBM Plex Mono",ui-monospace,monospace;
  letter-spacing:.04em;
}
#sitebar a{
  color:#A9B8C4; text-decoration:none; padding:2px 0; border-bottom:1px solid transparent;
}
#sitebar a:hover{color:#FBFAF7; border-bottom-color:#D3A257}
#sitebar a.here{color:#D3A257; border-bottom-color:#D3A257}
#sitebar .home{color:#FBFAF7; font-weight:600; letter-spacing:.14em; text-transform:uppercase}
#sitebar .home:hover{color:#D3A257}
#sitebar .spacer{flex:1 1 auto}
@media (max-width:640px){ #sitebar{gap:4px 14px; padding:9px 16px; font-size:11px} }
"""


def bar(page_url, active=""):
    """The strip that finally links the five pages to one another."""
    items = [('<a class="home" href="{}">Capital</a>'
              .format(relative(page_url, "")))]
    for slug, name, _, _, _ in DASHBOARDS:
        cls = ' class="here"' if slug == active else ""
        items.append(f'<a{cls} href="{relative(page_url, slug + "/")}">'
                     f'{html.escape(name)}</a>')
    items.append('<span class="spacer"></span>')
    items.append(f'<a href="{relative(page_url, "")}#record">The record</a>')
    return '<nav id="sitebar">' + "".join(items) + "</nav>"


def shell(page_url, title, description, body, css="", active="", head="",
          show_bar=True):
    """The skeleton every published page shares.

    `show_bar` exists for the front page, which is not part of the research
    site: the bar's links are relative to the office root and would point at
    nothing from a level above it.
    """
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="color-scheme" content="light dark">
{FONTS}
{head}
<style>{PALETTE}{BAR_CSS}{css}</style>
</head>
<body>
{bar(page_url, active) if show_bar else ""}
{body}
</body>
</html>
"""

# ------------------------------------------------------------- a record page

PAGE_CSS = """
*{box-sizing:border-box}
body{margin:0; background:var(--paper); color:var(--ink);
  font:400 16px/1.7 "IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:820px; margin:0 auto; padding-inline:20px; padding-block:34px 72px}
.crumb{font:400 12px/1.6 "IBM Plex Mono",monospace; letter-spacing:.08em;
  text-transform:uppercase; color:var(--ink-3); margin-bottom:10px}
.crumb a{color:var(--ink-3)}
.meta{margin:0 0 30px; padding-bottom:18px; border-bottom:2px solid var(--ink);
  font:400 12.5px/1.7 "IBM Plex Mono",monospace; color:var(--ink-3)}
article h1{font-family:Spectral,Georgia,serif; font-weight:600; letter-spacing:-.015em;
  font-size:clamp(1.8rem,4.2vw,2.4rem); line-height:1.15; margin:0 0 6px}
article h2{font-family:Spectral,Georgia,serif; font-weight:600; font-size:1.42rem;
  margin:2.4em 0 .5em; padding-top:.5em; border-top:1px solid var(--rule)}
article h3{font-size:1.08rem; font-weight:600; margin:1.9em 0 .4em}
article h4{font-size:.98rem; font-weight:600; margin:1.5em 0 .3em; color:var(--ink-2)}
article p,article li{color:var(--ink-2)}
article strong{color:var(--ink); font-weight:600}
article a{color:var(--brass); text-decoration:none; border-bottom:1px solid var(--brass-soft)}
article a:hover{border-bottom-color:var(--brass)}
article ul,article ol{padding-left:1.25em}
article li{margin:.34em 0}
article li::marker{color:var(--ink-3)}
article hr{border:0; border-top:1px solid var(--rule); margin:2.4em 0}
article blockquote{margin:1.3em 0; padding:.7em 1.1em; border-left:3px solid var(--brass);
  background:var(--sunk); border-radius:0 6px 6px 0}
article blockquote p{margin:.35em 0; color:var(--ink-2)}
article code{font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.86em;
  background:var(--sunk); border:1px solid var(--rule-2); border-radius:4px; padding:.1em .38em}
article pre{background:var(--sunk); border:1px solid var(--rule); border-radius:8px;
  padding:14px 16px; overflow-x:auto; line-height:1.55}
article pre code{background:none; border:0; padding:0; font-size:.84rem}
.tablewrap{overflow-x:auto; margin:1.3em 0}
article table{border-collapse:collapse; width:100%; font-size:.93rem}
article th,article td{text-align:left; padding:8px 12px; border-bottom:1px solid var(--rule-2);
  vertical-align:top}
article th{font:500 11.5px/1.5 "IBM Plex Mono",monospace; letter-spacing:.08em;
  text-transform:uppercase; color:var(--ink-3); border-bottom:1px solid var(--rule)}
article img{max-width:100%}
.foot{margin-top:56px; padding-top:18px; border-top:1px solid var(--rule);
  font:400 12.5px/1.7 "IBM Plex Mono",monospace; color:var(--ink-3);
  display:flex; flex-wrap:wrap; gap:8px 22px}
.foot a{color:var(--ink-3)}
"""


def record_page(page, by_path):
    body = md_to_html(page["text"])
    body = rewrite_links(body, page["src"], page["url"], by_path)
    # Tables get their own scroll container so a wide one cannot push the page
    # sideways on a phone.
    body = body.replace("<table>", '<div class="tablewrap"><table>')
    body = body.replace("</table>", "</table></div>")

    updated = page["updated"] or "not recorded"
    src = str(page["src"])
    inner = f"""<div class="wrap">
<div class="crumb"><a href="{relative(page['url'], '')}">Capital</a> ·
<a href="{relative(page['url'], '')}#record">The record</a></div>
<article>{body}</article>
<div class="foot">
  <span>{html.escape(src)}</span>
  <span>last changed {html.escape(updated)}</span>
  <span>{page['words']:,} words</span>
  <a href="https://github.com/{REPO}/blob/main/{src}">source on GitHub</a>
  <span class="spacer"></span>
  <a href="{relative(page['url'], '')}">← everything else</a>
</div>
</div>"""
    return shell(page["url"], f"{page['title']} · Capital",
                 f"{page['title']} — from the Capital research record, {src}.",
                 inner, PAGE_CSS)


# ------------------------------------------------------------- the front door

INDEX_CSS = """
*{box-sizing:border-box}
body{margin:0; background:var(--paper); color:var(--ink);
  font:400 16px/1.65 "IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1040px; margin:0 auto; padding-inline:20px; padding-block:34px 72px}
a{color:var(--brass)}
.eyebrow{font:500 11px/1 "IBM Plex Mono",monospace; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3)}
.masthead{display:flex; flex-wrap:wrap; gap:18px 32px; align-items:flex-end;
  justify-content:space-between; padding-bottom:20px; border-bottom:2px solid var(--ink)}
.firm{font-family:Spectral,Georgia,serif; font-weight:600; margin:6px 0 0;
  font-size:clamp(2rem,5vw,2.9rem); line-height:1.04; letter-spacing:-.02em}
.mandate{margin:10px 0 0; color:var(--ink-2); max-width:54ch}
.stamp{font:400 12px/1.8 "IBM Plex Mono",monospace; color:var(--ink-3); text-align:right}
.stamp b{color:var(--ink-2); font-weight:500}
h2.sec{font-family:Spectral,Georgia,serif; font-weight:600; font-size:1.5rem;
  margin:52px 0 4px}
.sec-note{color:var(--ink-3); margin:0 0 20px; font-size:.94rem; max-width:62ch}
.live{margin:26px 0 0; padding:16px 20px; background:var(--panel);
  border:1px solid var(--rule); border-left:3px solid var(--brass);
  border-radius:0 10px 10px 0; box-shadow:var(--shadow)}
.live p{margin:6px 0 0; color:var(--ink-2)}
.live strong{color:var(--ink)}
.numbers{display:grid; grid-template-columns:repeat(auto-fit,minmax(132px,1fr));
  gap:1px; margin:26px 0 0; background:var(--rule); border:1px solid var(--rule);
  border-radius:10px; overflow:hidden}
.num{background:var(--panel); padding:14px 16px}
.num b{display:block; font-family:Spectral,Georgia,serif; font-size:1.7rem; font-weight:600;
  line-height:1.1; margin-bottom:3px}
.num span{font:400 11px/1.4 "IBM Plex Mono",monospace; letter-spacing:.08em;
  text-transform:uppercase; color:var(--ink-3)}
.cards{display:grid; grid-template-columns:repeat(auto-fit,minmax(248px,1fr)); gap:14px}
.card{display:block; text-decoration:none; color:inherit; padding:18px 20px;
  background:var(--panel); border:1px solid var(--rule); border-radius:10px;
  box-shadow:var(--shadow); transition:border-color .12s,transform .12s}
.card:hover{border-color:var(--brass); transform:translateY(-1px)}
.card .glyph{font-size:1.1rem; color:var(--brass)}
.card h3{margin:6px 0 4px; font-size:1.06rem; font-weight:600}
.card p{margin:0; color:var(--ink-2); font-size:.92rem; line-height:1.55}
.card .when{display:block; margin-top:10px; font:400 11px/1 "IBM Plex Mono",monospace;
  color:var(--ink-3)}
.know{margin:0; padding-left:1.15em}
.know li{margin:.5em 0; color:var(--ink-2)}
.know li::marker{color:var(--brass)}
.know strong{color:var(--ink)}
.know a,.live a{color:var(--brass); text-decoration:none; border-bottom:1px solid var(--brass-soft)}
.know code,.live code{font-family:"IBM Plex Mono",monospace; font-size:.85em;
  background:var(--sunk); border:1px solid var(--rule-2); border-radius:4px; padding:.08em .34em}
#filter{width:100%; max-width:380px; margin:0 0 22px; padding:9px 13px;
  font:400 14px/1.4 "IBM Plex Sans",sans-serif; color:var(--ink);
  background:var(--panel); border:1px solid var(--rule); border-radius:8px}
#filter:focus{outline:2px solid var(--brass); outline-offset:1px}
.group{margin:0 0 30px}
.group h3{margin:0 0 2px; font-size:1.02rem; font-weight:600}
.group p.note{margin:0 0 10px; color:var(--ink-3); font-size:.9rem}
.rows{border:1px solid var(--rule); border-radius:10px; overflow:hidden; background:var(--panel)}
.row{display:flex; flex-wrap:wrap; gap:4px 14px; align-items:baseline;
  padding:11px 16px; text-decoration:none; color:inherit;
  border-top:1px solid var(--rule-2)}
.row:first-child{border-top:0}
.row:hover{background:var(--sunk)}
.row .t{font-weight:500}
.row .f{font:400 11.5px/1.5 "IBM Plex Mono",monospace; color:var(--ink-3)}
.row .w{margin-left:auto; font:400 11.5px/1.5 "IBM Plex Mono",monospace; color:var(--ink-3)}
.empty{padding:14px 16px; color:var(--ink-3); font-size:.92rem}
.pagefoot{margin-top:60px; padding-top:18px; border-top:2px solid var(--ink);
  font:400 12.5px/1.8 "IBM Plex Mono",monospace; color:var(--ink-3)}
.pagefoot a{color:var(--ink-3)}
@media (max-width:560px){ .row .w{display:none} }
"""

FILTER_JS = """
(function(){
  var box=document.getElementById('filter'); if(!box) return;
  var rows=[].slice.call(document.querySelectorAll('.row'));
  var groups=[].slice.call(document.querySelectorAll('.group'));
  box.addEventListener('input',function(){
    var q=box.value.trim().toLowerCase();
    rows.forEach(function(r){
      r.hidden = q && r.dataset.k.indexOf(q)===-1;
    });
    groups.forEach(function(g){
      g.hidden = !g.querySelector('.row:not([hidden])');
    });
  });
})();
"""


def counts():
    """Derived from the record itself, so the site cannot overstate the work."""
    scores = [int(m) for m in re.findall(r"^-\s+\*\*Score:\*\*\s*(\d+)/10",
                                         read("SCORECARD.md"), re.M)]
    return {
        "experiments": len(re.findall(r"^###\s+EXP-\d+", read("research/experiments.md"), re.M)),
        "beliefs": len(re.findall(r"^###\s+B-\d+", read("research/beliefs.md"), re.M)),
        "walls": len(re.findall(r"^###\s+\d{4}-\d\d-\d\d\s+—\s+OPEN",
                                read("thoughts/4-walls.md"), re.M)),
        "scores": scores,
    }


def index_page(pages, by_path, stamp, built):
    know = read("KNOWLEDGE.md")
    c = counts()

    live = section_body(know, "What is live right now")
    live_html = rewrite_links(md_to_html(live), Path("KNOWLEDGE.md"), "", by_path)

    known = section_body(know, "What we know")
    # Everything from the first bullet to the end of the section. The prose
    # above it explains the format to agents, not to the owner — but the
    # bullets themselves wrap over several lines, and taking only the lines
    # that start with a dash publishes every claim cut off mid-sentence.
    lines = known.splitlines()
    first = next((i for i, l in enumerate(lines) if re.match(r"^\s*[-*]\s+", l)), 0)
    known_html = rewrite_links(md_to_html("\n".join(lines[first:])), Path("KNOWLEDGE.md"),
                               "", by_path).replace("<ul>", '<ul class="know">')

    nums = [(c["experiments"], "experiments run"), (c["beliefs"], "beliefs held"),
            (c["walls"], "open walls"), (len(pages), "records")]
    if c["scores"]:
        avg = round(sum(c["scores"]) / len(c["scores"]), 1)
        nums.append((f"{avg}", f"avg of {len(c['scores'])} scores"))
    numbers = "".join(f'<div class="num"><b>{n}</b><span>{html.escape(t)}</span></div>'
                      for n, t in nums)

    cards = ""
    for slug, name, src, blurb, glyph in DASHBOARDS:
        if not (ROOT / src).exists():
            continue
        when = git("log", "-1", "--format=%cs", "--", src)
        cards += (f'<a class="card" href="{slug}/"><span class="glyph">{glyph}</span>'
                  f'<h3>{html.escape(name)}</h3><p>{html.escape(blurb)}</p>'
                  f'<span class="when">rebuilt {html.escape(when or "date not recorded")}'
                  f'</span></a>')

    groups = ""
    for key, name, note in SECTIONS:
        rows = ""
        for pg in [p for p in pages if p["section"] == key]:
            k = html.escape(f"{pg['title']} {pg['src']}".lower(), quote=True)
            rows += (f'<a class="row" href="{pg["url"]}" data-k="{k}">'
                     f'<span class="t">{html.escape(pg["title"])}</span>'
                     f'<span class="f">{html.escape(str(pg["src"]))}</span>'
                     f'<span class="w">{pg["words"]:,} words</span></a>')
        if not rows:
            continue
        groups += (f'<div class="group"><h3>{html.escape(name)}</h3>'
                   f'<p class="note">{html.escape(note)}</p>'
                   f'<div class="rows">{rows}</div></div>')

    inner = f"""<div class="wrap">
<header class="masthead">
  <div>
    <div class="eyebrow">Trading research programme</div>
    <h1 class="firm">Capital</h1>
    <p class="mandate">Make money in tradable markets — futures, equities,
    options and prediction markets. The record below <em>is</em> the work: every
    session reads it, adds to it, and leaves it better than it found it.</p>
  </div>
  <div class="stamp">
    built <b>{html.escape(built)}</b><br>
    commit <b>{html.escape(stamp['commit'])}</b> · {html.escape(stamp['commits'])} commits<br>
    <a href="https://github.com/{REPO}">github.com/{REPO}</a>
  </div>
</header>

<div class="live"><div class="eyebrow">What is live right now</div>{live_html}</div>

<div class="numbers">{numbers}</div>

<h2 class="sec">The live pages</h2>
<p class="sec-note">Rebuilt by their own scripts and published exactly as they
were produced. A page shows the date it was last rebuilt, so nothing here can
pass off an old reading as a current one.</p>
<div class="cards">{cards}</div>

<h2 class="sec">What we know</h2>
<p class="sec-note">Claims that have earned a place on the front page, each
carrying the evidence behind it. Follow an id to the belief, and the belief to
the experiment that produced it.</p>
{known_html}

<h2 class="sec" id="record">The record</h2>
<p class="sec-note">Every written record in the repository, rendered in full.
Nothing is summarised away — this is the same text a session reads.</p>
<input id="filter" type="search" placeholder="Filter {len(pages)} records…"
       autocomplete="off" aria-label="Filter records">
{groups}

<div class="pagefoot">
Generated from the repository by <a href="https://github.com/{REPO}/blob/main/site/build.py">site/build.py</a>
on every push to main. The trucking budget app archived in <code>legacy/</code>
is still running, at <a href="../budget/">its own address</a>.
</div>
</div>
<script>{FILTER_JS}</script>"""
    return shell("", "Capital · trading research",
                 "The Capital trading research programme — live dashboards and "
                 "the full research record.", inner, INDEX_CSS)


# -------------------------------------------------------- wrapping a dashboard

# Four of the five pages are fragments that start straight in with their own
# <style>; the tip sheet is a complete little document. Both are reduced to a
# body fragment here so every published page gets the same shell and the same
# navigation bar.
STRIP = re.compile(r"^\s*(?:<!doctype[^>]*>|<meta[^>]*>|<title>.*?</title>)\s*",
                   re.I | re.S)


def dashboard_page(slug, name, src, blurb):
    raw = (ROOT / src).read_text()
    while True:
        stripped = STRIP.sub("", raw, count=1)
        if stripped == raw:
            break
        raw = stripped
    return shell(f"{slug}/", f"{name} · Capital", blurb, raw, "", active=slug)


# --------------------------------------------------------------- the front page
# One address publishes two unrelated things. This page is what /CAPITAL-ALL/
# serves, so neither has to be buried under the other.

LANDING_CSS = """
*{box-sizing:border-box}
body{margin:0; background:var(--paper); color:var(--ink);
  font:400 16px/1.65 "IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;
  display:flex; align-items:center; min-height:100vh}
.wrap{max-width:720px; margin:0 auto; padding:40px 20px 56px; width:100%}
.eyebrow{font:500 11px/1 "IBM Plex Mono",monospace; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3)}
h1{font-family:Spectral,Georgia,serif; font-weight:600; margin:8px 0 0;
  font-size:clamp(2.1rem,6vw,3rem); line-height:1.04; letter-spacing:-.02em}
.sub{margin:10px 0 30px; color:var(--ink-2); max-width:46ch}
.doors{display:grid; gap:14px}
.door{display:block; text-decoration:none; color:inherit; padding:20px 22px;
  background:var(--panel); border:1px solid var(--rule); border-radius:12px;
  box-shadow:var(--shadow); transition:border-color .12s,transform .12s}
.door:hover{border-color:var(--brass); transform:translateY(-1px)}
.door .eyebrow{color:var(--brass)}
.door h2{margin:7px 0 5px; font-size:1.22rem; font-weight:600;
  font-family:Spectral,Georgia,serif}
.door p{margin:0; color:var(--ink-2); font-size:.95rem; line-height:1.55}
.foot{margin-top:34px; padding-top:16px; border-top:1px solid var(--rule);
  font:400 12px/1.7 "IBM Plex Mono",monospace; color:var(--ink-3)}
.foot a{color:var(--ink-3)}
"""


def landing_page(built, stamp):
    inner = f"""<div class="wrap">
<div class="eyebrow">jahmadjonov-art.github.io/CAPITAL-ALL</div>
<h1>Capital</h1>
<p class="sub">Two things are published at this address. They are unrelated —
pick the one you came for.</p>

<div class="doors">
  <a class="door" href="./budget/">
    <div class="eyebrow">The app</div>
    <h2>Capital Allocation</h2>
    <p>The trucking budget: income split across tax, repair, capital and salary.
    Add it to your home screen from there and it opens like an app, with or
    without signal.</p>
  </a>
  <a class="door" href="./office/">
    <div class="eyebrow">The research</div>
    <h2>Trading research</h2>
    <p>The tip sheet, the fair value desk, the volatility surface, and the whole
    written record of what has been tried and what is believed.</p>
  </a>
</div>

<div class="foot">
built {html.escape(built)} · commit {html.escape(stamp['commit'])} ·
<a href="https://github.com/{REPO}">github.com/{REPO}</a>
</div>
</div>"""
    return shell("", "Capital",
                 "The trucking budget app and the trading research programme.",
                 inner, LANDING_CSS, show_bar=False,
                 head='<link rel="icon" type="image/png" href="./budget/icon-192.png">')


# The app used to live at /CAPITAL-ALL/ and registered a service worker with
# that scope. It has moved to /CAPITAL-ALL/budget/ and taken its worker with
# it — but a browser that installed the old one still has it registered here,
# where it would keep answering for this front page and for the research site
# out of a cache of an app that is no longer at this address.
#
# A browser re-fetches this script whenever it navigates inside the scope, so
# serving this file is how the old worker gets told to stand down: it takes
# over, empties every cache it left behind, unregisters itself, and reloads the
# pages it was controlling so they come from the network. It has no fetch
# handler, so it answers for nothing in the meantime.
RETIRING_SW = """// Replaces the service worker the budget app registered when it lived at this
// address. Its only job is to undo that registration. See site/build.py.
self.addEventListener('install', () => self.skipWaiting())

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.matchAll({ type: 'window' }))
      .then((clients) => clients.forEach((client) => client.navigate(client.url)))
  )
})
"""


# --------------------------------------------------------------------- build

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "site" / "dist"))
    args = ap.parse_args()
    out = Path(args.out).resolve()

    pages = discover()
    by_path = {str(p["src"]): p for p in pages}
    stamp = {"commit": git("rev-parse", "--short", "HEAD", default="unknown"),
             "commits": git("rev-list", "--count", "HEAD", default="0")}
    built = datetime.datetime.now(datetime.timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    # The research site is one of two things published at this address; the app
    # is copied into ./budget/ by the workflow, beside it rather than under it.
    office = out / "office"

    def write(url, content):
        target = office / url / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    write("", index_page(pages, by_path, stamp, built))
    for page in pages:
        write(page["url"], record_page(page, by_path))

    published = 0
    for slug, name, src, blurb, _ in DASHBOARDS:
        if not (ROOT / src).exists():
            print(f"  ! {src} missing — {slug} not published")
            continue
        write(slug + "/", dashboard_page(slug, name, src, blurb))
        published += 1

    out.mkdir(parents=True, exist_ok=True)
    # GitHub Pages runs Jekyll over anything it serves unless told not to.
    (out / ".nojekyll").write_text("")
    (out / "index.html").write_text(landing_page(built, stamp))
    (out / "sw.js").write_text(RETIRING_SW)

    print(f"built {out}")
    print(f"  front page + {published} dashboards · {len(pages)} records "
          f"· commit {stamp['commit']}")


if __name__ == "__main__":
    main()
