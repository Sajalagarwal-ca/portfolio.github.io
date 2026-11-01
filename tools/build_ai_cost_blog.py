"""
Build the Blogger-safe blog post for the Grafana AI Cost Observability project.

Applies all three Blogger lessons learned:
  * no <!DOCTYPE>, <html>, <head> or <body>   -> body fragment only
  * no <style> block                          -> every rule is an inline attribute
  * no HTML comments                          -> nothing can be scraped as a title

Screenshots are embedded as base64 data URLs so the file is fully self-contained.
Responsiveness uses clamp()/auto-fit rather than @media, which cannot be inlined.
"""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "images" / "ai-cost"

# The Blogger paste file is a one-time publishing artefact, not a site asset, so
# it is written to a scratch dir rather than images/. The post is live at:
#   https://thepracticaldatascientist.blogspot.com/2026/11/grafana-postgresql-azure-data-factory.html
BUILD = ROOT / "tools" / "_build"
BUILD.mkdir(parents=True, exist_ok=True)
OUT = BUILD / "ai_cost_observability_blog_google_blogger.html"
PAGE = ROOT / "ai-cost-observability.html"

NAVY, TEAL, DEEP, INK, GREY = "#13324c", "#007985", "#006a79", "#23384d", "#5f7383"
LINE, PALE, AMBER = "#d9e5eb", "#f2f8f9", "#b8720a"
SANS = "Arial,Helvetica,sans-serif"

BODY = f"color:{INK};font-family:{SANS};font-size:clamp(16px,1.7vw,17px);line-height:1.8"
P = f"margin:0 0 18px;{BODY}"
H2 = (f"color:{NAVY};font-family:{SANS};font-size:clamp(23px,3.6vw,29px);"
      "font-weight:700;line-height:1.25;letter-spacing:-.02em;margin:38px 0 14px")
H3 = (f"color:{DEEP};font-family:{SANS};font-size:clamp(18px,2.5vw,21px);"
      "font-weight:700;line-height:1.3;margin:28px 0 10px")
LI = f"margin:9px 0;{BODY}"
CAP = f"color:{GREY};font-family:{SANS};font-size:13px;line-height:1.6;margin:10px 0 0"


def b64(name):
    data = base64.b64encode((IMG / name).read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


# Figures emit a token instead of a src, so the same article can be rendered
# twice: once self-contained (base64, for pasting into Blogger) and once with
# relative paths (small, for the standalone page hosted on GitHub Pages).
def figure(name, caption):
    return (
        f'<figure style="margin:30px 0;max-width:100%">'
        f'<img alt="{caption[:120]}" src="@@IMG:{name}@@" '
        f'style="border:1px solid {LINE};border-radius:8px;display:block;'
        f'height:auto;max-width:100%;width:100%" />'
        f'<figcaption style="{CAP}">{caption}</figcaption></figure>'
    )


def note(title, body, accent=TEAL):
    return (
        f'<div style="background:{PALE};border-left:4px solid {accent};'
        f'border-radius:0 10px 10px 0;margin:26px 0;padding:20px 22px">'
        f'<p style="color:{accent};font-family:{SANS};font-size:13px;font-weight:700;'
        f'letter-spacing:.08em;margin:0 0 8px;text-transform:uppercase">{title}</p>'
        f'<p style="{P};margin:0">{body}</p></div>'
    )


def table(headers, rows):
    th = "".join(
        f'<th style="background:{NAVY};border-bottom:1px solid {LINE};color:#fff;'
        f'font-family:{SANS};font-size:15px;font-weight:700;padding:13px 16px;'
        f'text-align:left">{h}</th>' for h in headers)
    body = ""
    for i, r in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else PALE
        tds = "".join(
            f'<td style="background:{bg};border-bottom:1px solid {LINE};color:{INK};'
            f'font-family:{SANS};font-size:15px;line-height:1.6;padding:13px 16px;'
            f'text-align:left;vertical-align:top{";font-weight:700" if j == 0 else ""}">'
            f'{c}</td>' for j, c in enumerate(r))
        body += f"<tr>{tds}</tr>"
    return (
        f'<div style="border:1px solid {LINE};border-radius:10px;margin:24px 0;'
        f'overflow-x:auto"><table style="background:#fff;border-collapse:collapse;'
        f'max-width:100%;width:100%"><thead><tr>{th}</tr></thead>'
        f'<tbody>{body}</tbody></table></div>'
    )


def ul(items):
    lis = "".join(f'<li style="{LI}">{i}</li>' for i in items)
    return f'<ul style="margin:14px 0 20px;padding-left:25px">{lis}</ul>'


def p(t):
    return f'<p style="{P}">{t}</p>'


def h2(t):
    return f'<h2 style="{H2}">{t}</h2>'


def h3(t):
    return f'<h3 style="{H3}">{t}</h3>'


# --------------------------------------------------------------------------- #
parts = []

parts.append(
    f'<header style="border-bottom:4px solid {TEAL};margin:0 0 28px;padding:24px 0 20px">'
    f'<p style="color:{TEAL};font:700 12px/1.5 {SANS};letter-spacing:1.5px;margin:0 0 12px;'
    f'text-transform:uppercase">Grafana &middot; PostgreSQL &middot; Azure Data Factory &middot; FinOps</p>'
    f'<h2 style="color:{NAVY};font-family:{SANS};font-size:clamp(28px,5vw,38px);'
    f'font-weight:700;letter-spacing:-.6px;line-height:1.18;margin:0 0 16px">'
    f'Three AI Products, Three Billing Models, One Dashboard</h2>'
    f'<p style="color:{GREY};font-family:{SANS};font-size:clamp(17px,2.2vw,20px);'
    f'line-height:1.6;margin:0">What it actually takes to put Gen&nbsp;AI, GitHub Copilot and '
    f'Copilot Studio spend into a single cost-centre view &mdash; and why most of the work '
    f'happens long before the first panel is drawn.</p></header>'
)

parts.append(p(
    "Cloud cost visibility is a solved problem. You take the billing export, resolve each "
    "resource to an owner, aggregate up a hierarchy, and publish. I had already built exactly "
    "that for Azure Cost Management: Azure Data Factory for orchestration, Python for every "
    "transformation, PostgreSQL to serve, Grafana to render."))

parts.append(p(
    "So when the ask came to do the same for AI spend, it looked like a port. It was not."))

parts.append(p(
    "<b>The reason is that &ldquo;AI spend&rdquo; is not one thing.</b> It arrived from three "
    "Microsoft products that are billed on three fundamentally different models, and none of "
    "them agreed on what a cost centre was."))

parts.append(h2("Three products that refuse to be added together"))

parts.append(table(
    ["Product", "Billing model", "Why it resists consolidation"],
    [["Gen AI / Azure OpenAI", "Consumption &mdash; meter &times; resource &times; day",
      "Priced per meter category and sub-category. Subscription tags are inconsistent, and "
      "Microsoft split Foundry Models and Foundry Tools out of Cognitive Services part-way "
      "through the year, breaking the category history."],
     ["GitHub Copilot", "Per-seat licence &times; month",
      "Not a meter at all. A seat has no resource, no tag and no subscription &mdash; it has a "
      "person. Reaching a cost centre means joining to HR data, and seat counts churn monthly."],
     ["Copilot Studio", "Consumed credits &times; environment",
      "Billed in credits, not currency. And mid-year Microsoft moved capacity drawing from "
      "tenant level to environment level, which broke the comparability of the whole series."]]))

parts.append(p(
    "Read those three rows again and the engineering problem becomes obvious. There is "
    "<b>no shared key.</b> A meter record, a licensed user and an environment credit draw have "
    "nothing in common that you can join on. Each one needs its own independent route to the "
    "same destination."))

parts.append(h3("The temptation to solve this in the dashboard"))

parts.append(p(
    "The fast path is to write three sets of panel queries, each with its own joins and "
    "conversions, and let Grafana reconcile at render time. It demos well and it is the wrong "
    "answer. Logic that lives in a panel cannot be unit-tested, cannot be reconciled against an "
    "invoice, and cannot be reused by the next consumer of the data. You also discover, the "
    "first time finance challenges a number, that you have no way to explain how it was derived."))

parts.append(note(
    "The principle I carried over from the Azure build",
    "Allocate once, in the transformation layer, and make the dashboard a thin read over an "
    "already-reconciled table. If a number is wrong, there is exactly one place to look."))

parts.append(h2("The pipeline"))

parts.append(table(
    ["Stage", "What happens"],
    [["1 &middot; Ingest",
      "ADF pipelines land the three raw exports on a schedule, each into its own staging area "
      "with the run date attached. No transformation here &mdash; staging stays faithful to the source."],
     ["2 &middot; Transform (Python)",
      "Per-source Python modules normalise currency and dates, map meters to product and meter "
      "sub-category, convert Copilot Studio credits into charges, and resolve every record to a "
      "cost centre. Tax is computed as a separate column rather than baked in, so it can be "
      "toggled at query time."],
     ["3 &middot; Allocate",
      "Resolved records fold into the same segment / sub-segment / tower / function hierarchy "
      "the rest of the cloud estate already uses, so AI spend aggregates consistently with everything else."],
     ["4 &middot; Serve (PostgreSQL)",
      "Monthly fact tables plus narrow dimensions, indexed on exactly the columns the dashboard "
      "filters on."],
     ["5 &middot; Visualise (Grafana)",
      "One dashboard, four tabs, driven entirely by template variables."]]))

parts.append(h3("Why cost-centre resolution is a waterfall, not a join"))

parts.append(p(
    "This is the part that carries the most business risk, so it is deliberately boring and "
    "explicit. Resolution runs as an ordered sequence: an explicit finance override first, then "
    "a validated resource tag, then inventory and parent mappings, then history, and finally a "
    "regional default. The first rule that matches wins."))

parts.append(p(
    "Critically, <b>every record stores which rule resolved it.</b> When someone disputes an "
    "allocation &mdash; and they will &mdash; the answer is a lookup, not an investigation. "
    "A chargeback model that cannot explain itself does not survive its first finance review."))

parts.append(h2("The dashboard"))

parts.append(p(
    "Four tabs behind a single filter bar. The Summary tab answers <i>what are we spending "
    "in total, and who is spending it.</i> The three product tabs answer <i>why.</i>"))

parts.append(figure(
    "ai-cost-01-summary.png",
    "Summary tab &mdash; total AI charges across all three products, with product split, a "
    "12-month trend, and breakdowns by sub-segment and cost centre. The filter bar (month, "
    "segment, sub-segment, tower, function, cost centre, include-tax) drives every tab."))

parts.append(h3("Three decisions in that one screen"))

parts.append(ul([
    "<b>Annual and current-month side by side on every stat panel.</b> A single number invites "
    "the follow-up question &ldquo;is that a lot?&rdquo; Showing both answers it in place.",
    "<b>Include Tax is a toggle, not a second dashboard.</b> Finance reconciles with tax; "
    "engineering compares without it. Pre-computing both in the fact table turns a political "
    "argument into a filter.",
    "<b>Product split up front.</b> Gen AI dominates. Surfacing that share immediately stops "
    "teams spending a quarter optimising the product that accounts for under one percent of spend.",
]))

parts.append(figure(
    "ai-cost-02-genai.png",
    "Gen AI Consumption tab &mdash; meter-category trend, environment split, top models by YTD "
    "charge, and top cost centres by model. The note panel documents the December 2025 "
    "re-categorisation of Cognitive Services into Foundry Models and Foundry Tools."))

parts.append(p(
    "The environment split is the panel that actually changes behaviour. Non-production and "
    "sandbox spend on generative models is where unreviewed experimentation quietly accumulates. "
    "Separating it from production turns one large, undiscussable number into a specific "
    "conversation about which workloads genuinely need a frontier model and which are running "
    "one because it was the default in a tutorial."))

parts.append(figure(
    "ai-cost-03-copilot.png",
    "GitHub Copilot tab &mdash; seat charges by segment and cost centre, a consumption trend "
    "overlaying charges against total, EMU and non-EMU user counts, and a user-level detail "
    "table. Personal columns are redacted in this published version."))

parts.append(h3("A licence is not a meter"))

parts.append(p(
    "Because Copilot is billed per seat, <b>total cost is the wrong headline metric</b> &mdash; "
    "cost per active user is the right one. Plotting charges against user counts on a shared "
    "time axis makes the two forces separable:"))

parts.append(ul([
    "Charges rising while seat count is flat &rarr; a price change, not an adoption story.",
    "Charges flat while seat count falls &rarr; unreclaimed licences. Pure waste.",
    "Both rising together &rarr; genuine adoption, and the only case worth celebrating.",
]))

parts.append(p(
    "The user-level table exists for one operational reason: a cost-centre owner needs to be "
    "able to identify dormant seats and reclaim them. An aggregate cannot do that."))

parts.append(figure(
    "ai-cost-04-copilot-studio.png",
    "Copilot Studio tab &mdash; consumed credits and converted charges by sub-segment, cost "
    "centre and environment, with a production versus non-production monthly comparison."))

parts.append(h3("The discontinuity problem"))

parts.append(p(
    "Look at the trend: charges collapse from November. Nothing improved. Microsoft moved "
    "Copilot Studio capacity drawing from tenant level to environment level &mdash; a platform "
    "change, not reduced usage."))

parts.append(note(
    "Explain the break where it is seen",
    "A trend discontinuity that is not explained <i>directly above the chart</i> will be "
    "mis-read as a saving, and sooner or later somebody will claim credit for it in a steering "
    "deck. I put the disclaimer in a panel, not in documentation nobody opens. The same applies "
    "to the Foundry re-categorisation on the Gen AI tab.",
    AMBER))

parts.append(h2("What changed"))

parts.append(table(
    ["Before", "After"],
    [["Three exports reconciled by hand in spreadsheets, monthly.",
      "One scheduled pipeline; the dashboard is current without manual effort."],
     ["AI spend invisible below segment level.",
      "Every charge resolves to a cost centre, with the resolving rule recorded."],
     ["Copilot Studio reported in credits, not currency.",
      "Converted in the transformation layer; all three products sum into one number."],
     ["&ldquo;Why did this change?&rdquo; answered over email.",
      "Platform discontinuities documented in-panel, next to the trend."],
     ["Finance and engineering worked from different extracts.",
      "One dashboard; the Include Tax toggle serves both."]]))

parts.append(h2("What I would build next"))

parts.append(ul([
    "<b>Unit economics.</b> Cost per active Copilot seat, and cost per 1K tokens by model, so "
    "efficiency is trackable independently of volume. Right now a 20% cost rise and a 20% usage "
    "rise look identical.",
    "<b>Budget thresholds.</b> Grafana alerting on cost-centre spend against plan, rather than "
    "depending on somebody remembering to open a dashboard.",
    "<b>Anomaly detection.</b> Port the model already running against general cloud spend onto "
    "the AI fact tables. The Gen AI series is volatile enough to justify it.",
    "<b>Forecast overlay.</b> Project month-end spend from partial-month consumption &mdash; "
    "which is the question finance actually asks on the 12th, not the 1st.",
]))

parts.append(h2("The transferable lesson"))

parts.append(p(
    "The dashboard is the smallest part of this project. Four tabs of Grafana panels is perhaps "
    "a fifth of the effort. The other four fifths is the unglamorous work of making three "
    "incompatible billing models agree on a single business hierarchy, and doing it in a way "
    "that can be tested and explained."))

parts.append(p(
    "<b>If your cost dashboard cannot tell you why a number is what it is, it is a reporting "
    "tool, not a chargeback system.</b> The difference only shows up when somebody disagrees "
    "with the number &mdash; and somebody always does."))

parts.append(
    f'<div style="border-top:1px solid {LINE};margin:36px 0 0;padding:18px 0 0">'
    f'<p style="color:{GREY};font-family:{SANS};font-size:13px;line-height:1.65;margin:0">'
    f'<b>Note on the screenshots.</b> All images are redacted for publication. Employee names, '
    f'email addresses and employee IDs are permanently removed, and absolute financial values '
    f'are obscured. Panel layout, chart structure and dashboard design are unchanged. Figures '
    f'shown are illustrative and are not representative of any organisation&rsquo;s actual AI '
    f'expenditure.</p></div>'
)

TITLE = "Three AI Products, Three Billing Models, One Dashboard"

# One block element per line keeps the generated files reviewable in an editor
# and in git diffs. HTML ignores the newlines between block elements.
article = (f'<article style="{BODY};margin:0 auto;max-width:960px;'
           f'overflow-wrap:break-word;text-align:left">\n'
           + "\n".join(parts) + "\n</article>\n")

# ---- 1. Blogger fragment: self-contained, base64 images -------------------- #
blogger = article
for png in sorted(IMG.glob("ai-cost-*.png")):
    blogger = blogger.replace(f"@@IMG:{png.name}@@", b64(png.name))
OUT.write_bytes(blogger.encode("utf-8"))

# ---- 2. Standalone page: relative image paths, full document --------------- #
page_article = article
for png in sorted(IMG.glob("ai-cost-*.png")):
    page_article = page_article.replace(f"@@IMG:{png.name}@@", f"images/ai-cost/{png.name}")

page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="How Gen AI, GitHub Copilot and Copilot Studio spend \u2014 three incompatible billing models \u2014 were unified into one cost-centre-level Grafana dashboard.">
  <title>{TITLE} | Grafana AI Cost Observability</title>
  <style>
    body {{ background:#fff; margin:0; padding:clamp(24px,5vw,56px) clamp(16px,4vw,32px); }}
    .backlink {{ display:block; max-width:960px; margin:0 auto 28px;
                 font:600 14px/1.5 {SANS}; color:{TEAL}; text-decoration:none; }}
    .backlink:hover {{ text-decoration:underline; }}
    .pdflink {{ display:inline-block; margin:0 0 8px; font:600 15px/1.5 {SANS};
                color:{DEEP}; }}
  </style>
</head>
<body>
<a class="backlink" href="index.html">&larr; Back to portfolio</a>
{page_article}
<p style="max-width:960px;margin:28px auto 0;font:400 15px/1.7 {SANS};color:{GREY}">
  Prefer a document? <a class="pdflink" href="images/Grafana_AI_Cost_Observability.pdf"
  target="_blank" rel="noopener noreferrer">Read the full project PDF &rarr;</a>
</p>
</body>
</html>
"""
PAGE.write_bytes(page.encode("utf-8"))

# ---- Verify the Blogger constraints ---------------------------------------- #
checks = {
    "<style": blogger.count("<style"),
    "<!--": blogger.count("<!--"),
    "<!DOCTYPE/<html/<head/<body": sum(blogger.count(t) for t in ("<!DOCTYPE", "<html", "<head>", "<body")),
    "@media": blogger.count("@media"),
    "<script": blogger.count("<script"),
    "remote src=http": blogger.count('src="http'),
    "unresolved @@IMG tokens": blogger.count("@@IMG:") + page.count("@@IMG:"),
}
print(f"{OUT.name}  ({len(blogger)/1024:,.0f} KB, {blogger.count(chr(10)):,} lines)  [Blogger fragment]")
for k, v in checks.items():
    print(f"  {'OK ' if v == 0 else 'FAIL'} {k}: {v}")
print(f"  embedded images: {blogger.count('src=\"data:image/png;base64,')}")
print(f"{PAGE.name}  ({len(page)/1024:,.0f} KB)  [standalone page, relative images]")
