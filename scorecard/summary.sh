#!/usr/bin/env bash
#
# Derives statistics from SCORECARD.md. Nothing here is stored — every number
# is recomputed from the log each time this runs, so it can never disagree with
# the entries it is summarising.
#
# Usage: ./scorecard/summary.sh

set -euo pipefail

ledger="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/SCORECARD.md"

if [[ ! -f "$ledger" ]]; then
  echo "No SCORECARD.md found at $ledger" >&2
  exit 1
fi

# Only digits count as a score, which is what keeps the "N/10" in the template
# comment from being read as an entry.
awk '
  /^### / {
    flush()
    heading = substr($0, 5)
    next
  }
  /^- \*\*Score:\*\*[[:space:]]*[0-9]+\/10/ {
    match($0, /[0-9]+/)
    score = substr($0, RSTART, RLENGTH) + 0
    next
  }
  /^- \*\*Date:\*\*/ {
    date = $3
    next
  }
  END { flush(); report() }

  function flush() {
    if (heading != "" && score != "") {
      n++
      headings[n] = heading
      scores[n]   = score
      dates[n]    = (date == "" ? "—" : date)
    }
    heading = ""; score = ""; date = ""
  }

  function report(   i, sum, best, worst, bestAt, worstAt, avg, recent, rn, rsum, bar) {
    if (n == 0) {
      print ""
      print "  No phases scored yet."
      print ""
      print "  The system is in place and waiting for the first score."
      print "  Nothing to learn from until then — read SCORECARD.md for how it works."
      print ""
      exit 0
    }

    best = -1; worst = 99
    for (i = 1; i <= n; i++) {
      sum += scores[i]
      if (scores[i] >= best)  { best  = scores[i]; bestAt  = i }
      if (scores[i] <= worst) { worst = scores[i]; worstAt = i }
    }
    avg = sum / n

    # Entries are newest-first in the file, so index 1 is the latest.
    rn = (n < 3 ? n : 3)
    for (i = 1; i <= rn; i++) rsum += scores[i]

    printf "\n  SCORECARD — %d phase%s scored\n\n", n, (n == 1 ? "" : "s")
    printf "  Average    %.1f / 10\n", avg
    printf "  Latest     %d / 10   (%s)\n", scores[1], headings[1]
    printf "  Last %d     %.1f / 10\n", rn, rsum / rn
    printf "  Best       %d / 10   (%s)\n", best, headings[bestAt]
    printf "  Weakest    %d / 10   (%s)\n", worst, headings[worstAt]

    print  "\n  History, newest first\n"
    for (i = 1; i <= n; i++) {
      bar = ""
      for (j = 0; j < scores[i]; j++) bar = bar "#"
      for (j = scores[i]; j < 10; j++) bar = bar "."
      printf "  %2d/10  %s  %-10s  %s\n", scores[i], bar, dates[i], headings[i]
    }

    if (worst <= 5)
      printf "\n  Note: \"%s\" scored %d. Re-read that entry before starting\n        anything similar.\n", headings[worstAt], worst

    print  "\n  Standing Directives are in SCORECARD.md and are binding.\n"
  }
' "$ledger"
