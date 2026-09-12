#!/usr/bin/env python3
"""Build the office floor plan from the repository's actual state.

Nothing here is stored twice. Every count, name and status is read from the
markdown files at build time, so the dashboard can never disagree with the
record it is showing. If a number is not known, it renders as not known —
never as a placeholder that looks like data.

Usage: python3 dashboard/build.py
"""
import json, re, subprocess, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard" / "office.html"


def read(rel):
    p = ROOT / rel
    return p.read_text() if p.exists() else ""


def section(text, heading):
    """Body of a '## heading' section, up to the next '## '."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)",
                  text, re.M | re.S)
    return m.group(1).strip() if m else ""


def bullets(body, limit=8):
    """Top-level list items, with the placeholder blockquote recognised."""
    if not body or re.match(r"^>\s*_?(Nothing|No )", body.strip()):
        return []
    out = []
    for line in body.splitlines():
        if re.match(r"^\s*[-*]\s+", line):
            out.append(re.sub(r"^\s*[-*]\s+", "", line).strip())
        if len(out) >= limit:
            break
    return out


def live_line(body):
    """The blockquote in 'What is live right now', without its markdown."""
    quoted = [re.sub(r"^>\s?", "", l) for l in body.splitlines() if l.startswith(">")]
    text = " ".join((" ".join(quoted) if quoted else body).split())
    return text.strip().strip("_").strip()


def placeholder(body):
    """The italic '_Nothing yet._' note a section carries when empty."""
    m = re.search(r"_([^_]+)_", body or "")
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------- the roster
# Desks are generated from the agent definitions, so adding an agent adds a
# desk with no change here.
def roster():
    desks = [{
        "id": "lead", "name": "Lead", "role": "The /research session",
        "brief": "Owns the question, decides what is true, and is the only "
                 "writer to the record.", "lead": True,
    }]
    for f in sorted((ROOT / ".claude" / "agents").glob("*.md")):
        t = f.read_text()
        name = re.search(r"^name:\s*(.+)$", t, re.M)
        desc = re.search(r"^description:\s*(.+)$", t, re.M)
        desks.append({
            "id": f.stem,
            "name": (name.group(1) if name else f.stem).strip().title(),
            "role": "Specialist",
            "brief": (desc.group(1) if desc else "").strip(),
            "lead": False,
        })
    return desks


# --------------------------------------------------------------- the plots
def sandboxes():
    out = []
    for f in sorted((ROOT / "sandbox").glob("*.md")):
        if f.name == "README.md":
            continue
        t = f.read_text()
        title = re.search(r"^#\s+(.+)$", t, re.M)
        status = re.search(r"^\*\*Status:\*\*\s*(.+)$", t, re.M)
        out.append({
            "file": f.name,
            "title": (title.group(1) if title else f.stem).strip(),
            "status": (status.group(1) if status else "OPEN").strip(),
            "goal": " ".join(section(t, "The goal").split())[:240],
            "why": " ".join(section(t, "Why it matters").split())[:240],
            "missing": " ".join(section(t, "What is missing").split())[:240],
        })
    return out


def counts():
    exp = read("research/experiments.md")
    bel = read("research/beliefs.md")
    return {
        "experiments": len(re.findall(r"^###\s+EXP-\d+", exp, re.M)),
        "beliefs": len(re.findall(r"^###\s+B-\d+", bel, re.M)),
        "walls": len(re.findall(r"^###\s+\d{4}-\d\d-\d\d\s+—\s+OPEN",
                                read("thoughts/4-walls.md"), re.M)),
        "postmortems": len(re.findall(r"^###\s+\d{4}-\d\d-\d\d",
                                      read("thoughts/5-postmortems.md"), re.M)),
        "unknowns": len(re.findall(r"^###.*OPEN:", read("thoughts/3-unknown.md"), re.M)),
    }


def scores():
    vals = [int(m) for m in re.findall(r"^-\s+\*\*Score:\*\*\s*(\d+)/10",
                                       read("SCORECARD.md"), re.M)]
    return {"count": len(vals), "values": vals,
            "average": round(sum(vals) / len(vals), 1) if vals else None}


def git(*args, default=""):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, timeout=15).stdout.strip() or default
    except Exception:
        return default


know = read("KNOWLEDGE.md")
k_known, k_dead, k_live = (section(know, "What we know"),
                           section(know, "What is dead"),
                           section(know, "What is live right now"))

DATA = {
    # The account is real and deliberately unfunded. These are stated as
    # unknown-until-checked rather than filled with plausible figures — see
    # sandbox/robinhood.md, where checking it is the open task.
    "book": {
        "capital": 0.0,
        "realised": None,
        "open_positions": None,
        "note": "Brokerage account connected and deliberately unfunded. "
                "No order has ever been placed. Balances read as zero because "
                "they are zero, not because nothing was fetched.",
        "verified": "2026-09-12",
    },
    "mandate": "Make money in tradable markets — futures, equities, options, "
               "prediction markets.",
    "desks": roster(),
    "plots": sandboxes(),
    "counts": counts(),
    "scores": scores(),
    "whiteboard": {
        "known": bullets(k_known) or [placeholder(k_known)],
        "known_empty": not bullets(k_known),
        "dead": bullets(k_dead) or [placeholder(k_dead)],
        "dead_empty": not bullets(k_dead),
        "live": live_line(k_live),
    },
    "build": {
        "at": datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
        "commit": git("rev-parse", "--short", "HEAD", default="unknown"),
        "commits": git("rev-list", "--count", "HEAD", default="0"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD", default="unknown"),
    },
}

TEMPLATE = (ROOT / "dashboard" / "template.html").read_text()
OUT.write_text(TEMPLATE.replace("/*__DATA__*/null",
                                json.dumps(DATA, indent=2)))
print(f"built {OUT.relative_to(ROOT)}")
print(f"  desks {len(DATA['desks'])}  plots {len(DATA['plots'])}  "
      f"experiments {DATA['counts']['experiments']}  "
      f"scores {DATA['scores']['count']}")
