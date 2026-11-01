"""
Reorder the project <article> cards in index.html newest-first.

Dates below are the project's first appearance in this repo's git history
(`git log -S<key> -- index.html`), with blog publish time breaking ties inside
2026-11-01. Edit ORDER and re-run; the script rewrites only the contiguous
block of <article> elements and leaves everything else byte-identical.
"""

import re
import sys
from pathlib import Path

INDEX = Path(__file__).resolve().parent.parent / "index.html"

# (unique substring found in that card, label, date)  -- newest first
ORDER = [
    ("Grafana_AI_Cost_Observability", "Grafana AI Cost Observability",   "2026-11-01"),
    ("Azure_FinOps_Chargeback",       "Azure Cost Management FinOps",    "2026-11-01"),
    ("One_API_Agent",                 "ONE API Agent",                   "2026-11-01"),
    ("power-bi-data-completeness",    "Application Data Quality",        "2026-10-17"),
    ("Grafana_Query_Performance",     "Grafana Query Performance",       "2026-08-24"),
    ("Shopping_Agent.pdf",            "AI Shopping Agent",               "2026-08-23"),
    ("Telecom_Agent.pdf",             "RAG Telecom Agent",               "2026-08-23"),
    ("Healthcare_premium_predictor",  "Healthcare Premium Calculator",   "2026-05-18"),
    ("Credit_Risk_Model_Portfolio",   "Credit Risk Modeling",            "2026-05-18"),
    ("RAG-Document-reader",           "RAG Document Reader",             "2026-03-13"),
    ("langchain_query_NL_PostgreSQL", "NL Query PostgreSQL",             "2026-03-12"),
    ("HL_93NOCiLU",                   "Fraudulent Loan Detection",       "2026-03-06"),
    ("expense management.jpg",        "Expense Management System",       "2026-03-06"),
    ("kycgobofe80",                   "Forecast Home Prices",            "2026-03-02"),
    ("UwXeLa8KHjk",                   "Cloud Cost Anomaly Detection",    "2026-02-22"),
]

# NOTE: index.html also contains one HTML comment (around line 496) wrapping
# three older cards - AI Travel Assistant, Insurance Fraud Investigation (RAG)
# and Power BI & Tableau Dashboards. They do not render, so they are not listed
# above. The script moves that commented block to the end of the card region
# and leaves it commented; uncomment it by hand to bring those cards back.

html = INDEX.read_text(encoding="utf-8")

# index.html contains a commented-out <article> (an older AI Travel Assistant
# card). Mask comments to the same length so offsets stay valid, then scan the
# masked copy - so commented markup is never mistaken for a live card.
masked = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), html, flags=re.S)

spans = [m.span() for m in re.finditer(r"[ \t]*<article>.*?</article>[ \t]*\r?\n",
                                       masked, re.S)]
if not spans:
    sys.exit("No <article> blocks found.")

region_start, region_end = spans[0][0], spans[-1][1]

# Separate live cards from anything sitting between them (the commented-out
# block). Cards get reordered; the extras are re-appended at the end of the
# region so hidden markup sinks to the bottom instead of travelling with a card.
cards = [html[s:e] for s, e in spans]
extras = "".join(html[a[1]:b[0]] for a, b in zip(spans, spans[1:]))
print(f"found {len(cards)} live project cards "
      f"({html.count('<article>') - len(cards)} commented-out block(s) preserved)")

if len(cards) != len(ORDER):
    sys.exit(f"ORDER lists {len(ORDER)} entries but index.html has {len(cards)} cards.")

# Map each card to its ORDER position via its unique key.
ranked, unmatched = [], list(cards)
for pos, (key, label, date) in enumerate(ORDER):
    hits = [c for c in unmatched if key in c]
    if len(hits) != 1:
        sys.exit(f"Key {key!r} matched {len(hits)} cards (expected exactly 1).")
    unmatched.remove(hits[0])
    ranked.append((pos, label, date, hits[0]))

if unmatched:
    titles = [re.search(r">([^<]{4,60})</a>", c).group(1).strip() for c in unmatched]
    sys.exit(f"Cards not covered by ORDER: {titles}")

ranked.sort(key=lambda r: r[0])
new_html = (html[:region_start] + "".join(r[3] for r in ranked)
            + extras + html[region_end:])

# Nothing may be lost: the reordered region must be a permutation of the original.
if sorted(new_html) != sorted(html):
    sys.exit("Refusing to write: content changed, not just reordered.")

if new_html == html:
    print("already in order - no change")
else:
    INDEX.write_text(new_html, encoding="utf-8")
    print(f"rewrote {INDEX.name}\n")

for pos, label, date, _ in ranked:
    print(f"  {pos + 1:2}. {date}  {label}")
