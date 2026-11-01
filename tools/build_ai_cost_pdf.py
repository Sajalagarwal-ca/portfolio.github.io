"""
Build the Grafana AI Cost Observability project PDF for the portfolio.

Uses the REDACTED screenshots produced by tools/redact_screenshots.py.
Run that script first.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "images" / "ai-cost"
OUT = ROOT / "images" / "Grafana_AI_Cost_Observability.pdf"

NAVY = colors.HexColor("#13324C")
TEAL = colors.HexColor("#007985")
DEEP = colors.HexColor("#006A79")
INK = colors.HexColor("#23384D")
GREY = colors.HexColor("#5F7383")
LINE = colors.HexColor("#D9E5EB")
PALE = colors.HexColor("#F2F8F9")
AMBER = colors.HexColor("#B8720A")

PW, PH = LETTER
MARGIN = 0.72 * inch
CW = PW - 2 * MARGIN

S = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=25, leading=29,
                         textColor=NAVY, spaceAfter=8),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=12.5, leading=18,
                          textColor=GREY, spaceAfter=16),
    "eyebrow": ParagraphStyle("eyebrow", fontName="Helvetica-Bold", fontSize=8.5,
                              leading=12, textColor=TEAL, spaceAfter=5),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14.5, leading=18,
                         textColor=NAVY, spaceBefore=15, spaceAfter=7),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11, leading=14,
                         textColor=DEEP, spaceBefore=10, spaceAfter=4),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=14.4,
                           textColor=INK, alignment=TA_LEFT, spaceAfter=7),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.4, leading=13.6,
                             textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=3.5),
    "cap": ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=8, leading=11,
                          textColor=GREY, spaceBefore=4, spaceAfter=12),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=11.6,
                           textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=8.4, leading=11.6,
                            textColor=NAVY),
    "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8.4, leading=11.6,
                            textColor=colors.white),
    "note": ParagraphStyle("note", fontName="Helvetica", fontSize=8.6, leading=12.4,
                           textColor=INK),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def B(t):
    return Paragraph(t, S["bullet"], bulletText="\u2022")


def rule(c=LINE, h=1.1, before=2, after=9):
    return Table([[""]], colWidths=[CW], rowHeights=[h],
                 style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), c),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 0)]),
                 spaceBefore=before, spaceAfter=after)


def shot(fname, caption):
    p = IMG / fname
    from PIL import Image as PILImage
    w, h = PILImage.open(p).size
    dw = CW
    dh = dw * h / w
    img = Image(str(p), width=dw, height=dh)
    box = Table([[img]], colWidths=[CW],
                style=TableStyle([("BOX", (0, 0), (-1, -1), 0.9, LINE),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                  ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                  ("TOPPADDING", (0, 0), (-1, -1), 0),
                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return KeepTogether([box, P(caption, "cap")])


def table(rows, widths, header=True):
    data = []
    for i, r in enumerate(rows):
        style = "cellh" if (header and i == 0) else None
        data.append([Paragraph(c, S[style or ("cellb" if j == 0 else "cell")])
                     for j, c in enumerate(r)])
    ts = [("GRID", (0, 0), (-1, -1), 0.6, LINE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 7),
          ("RIGHTPADDING", (0, 0), (-1, -1), 7),
          ("TOPPADDING", (0, 0), (-1, -1), 5.5),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5)]
    if header:
        ts += [("BACKGROUND", (0, 0), (-1, 0), NAVY),
               ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE])]
    else:
        ts += [("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, PALE])]
    return Table(data, colWidths=widths, style=TableStyle(ts),
                 spaceBefore=4, spaceAfter=11, repeatRows=1 if header else 0)


def callout(title, body, accent=TEAL):
    inner = [Paragraph(f'<font color="{accent.hexval()}"><b>{title}</b></font>', S["note"]),
             Spacer(1, 3), Paragraph(body, S["note"])]
    return Table([[inner]], colWidths=[CW],
                 style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE),
                                   ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 12),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                                   ("TOPPADDING", (0, 0), (-1, -1), 9),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]),
                 spaceBefore=6, spaceAfter=11)


# --------------------------------------------------------------------------- #
def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PH - 0.22 * inch, PW, 0.22 * inch, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PH - 0.26 * inch, PW * 0.34, 0.04 * inch, stroke=0, fill=1)
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(GREY)
    canvas.drawString(MARGIN, 0.46 * inch, "Grafana AI Cost Observability")
    canvas.drawRightString(PW - MARGIN, 0.46 * inch, f"Page {doc.page}")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, 0.62 * inch, PW - MARGIN, 0.62 * inch)
    canvas.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=LETTER,
                      leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=0.58 * inch, bottomMargin=0.78 * inch,
                      title="Grafana AI Cost Observability",
                      author="Sajal Agarwal",
                      subject="AI spend visibility and chargeback on Grafana + PostgreSQL + ADF")
frame = Frame(MARGIN, 0.78 * inch, CW, PH - 0.58 * inch - 0.78 * inch, id="f")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])

F = []

# ---- Title ---------------------------------------------------------------- #
F += [
    P("GRAFANA &nbsp;&middot;&nbsp; POSTGRESQL &nbsp;&middot;&nbsp; AZURE DATA FACTORY &nbsp;&middot;&nbsp; PYTHON &nbsp;&middot;&nbsp; FINOPS", "eyebrow"),
    P("Grafana AI Cost Observability", "h1"),
    P("Turning Gen&nbsp;AI, GitHub Copilot and Copilot Studio consumption into a single, "
      "cost-centre-level view of AI spend &mdash; built on the same ingestion and chargeback "
      "pattern already proven for Azure Cost Management.", "sub"),
    rule(NAVY, 2.2, 0, 12),
]

F += [table([
    ["Objective", "Give every segment, tower and cost centre an explainable monthly view of AI spend across three "
                  "independently billed Microsoft AI products."],
    ["Stack", "Azure Data Factory (orchestration) &rarr; Python transformation modules &rarr; PostgreSQL (serving) "
              "&rarr; Grafana (four-tab dashboard)."],
    ["Scope", "Gen&nbsp;AI / Azure OpenAI &amp; Foundry, GitHub Copilot (user-level), Copilot Studio (credit-based)."],
    ["My role", "Data model, Python transformation layer, ADF pipeline design, PostgreSQL schema and all Grafana panels."],
], [1.05 * inch, CW - 1.05 * inch], header=False)]

# ---- Problem -------------------------------------------------------------- #
F += [P("The problem", "h2"),
      P("AI spend arrived from three different places, in three different shapes, on three different cadences &mdash; "
        "and none of them agreed on what a &ldquo;cost centre&rdquo; was.", "body"),
      table([
          ["Source", "Grain it arrives at", "Why it resists consolidation"],
          ["Gen&nbsp;AI / Azure OpenAI", "Azure meter &times; resource &times; day",
           "Priced per meter category and sub-category; subscription tags are inconsistent, and "
           "Foundry Models / Foundry Tools only split out from Cognitive Services part-way through the year."],
          ["GitHub Copilot", "Licensed user &times; month",
           "A seat licence, not a consumption meter. Must be joined to HR data to reach a cost centre, "
           "and seat counts churn monthly."],
          ["Copilot Studio", "Environment &times; consumed credits",
           "Billed in credits, not currency, and the tenant-to-environment capacity change mid-year "
           "broke the comparability of the monthly series."],
      ], [1.28 * inch, 1.5 * inch, CW - 2.78 * inch])]

F += [B("<b>No shared key.</b> Meter-level Azure data, per-user licence data and per-environment credit data "
        "had no common identifier. Each needed its own route to a cost centre."),
      B("<b>Different units.</b> Credits had to be converted to currency before anything could be summed."),
      B("<b>Unstable history.</b> Microsoft re-categorised meters and moved Copilot Studio capacity mid-year, "
        "so a naive month-over-month comparison reported a cost collapse that never happened."),
      B("<b>Two audiences.</b> Finance needed segment and cost-centre totals that reconcile to the invoice; "
        "engineering needed model-, environment- and user-level detail to act on.")]

F += [callout("Design principle carried over from the Azure Cost Management build",
              "Allocate once, in the transformation layer, and make the dashboard a thin read over "
              "an already-reconciled table. Any logic pushed into Grafana panels becomes logic that "
              "cannot be tested, reconciled or reused.")]

F += [PageBreak()]

# ---- Architecture --------------------------------------------------------- #
F += [P("ARCHITECTURE", "eyebrow"), P("Pipeline", "h2"),
      P("The pipeline reuses the Azure Cost Management pattern end to end: ADF orchestrates, Python owns "
        "every transformation, PostgreSQL serves, Grafana renders.", "body")]

F += [table([
    ["Stage", "What happens"],
    ["1 &middot; Ingest",
     "ADF pipelines land raw exports on a schedule &mdash; Azure cost exports for Gen&nbsp;AI, the Copilot licence "
     "extract, and the Copilot Studio credit export &mdash; each into its own staging area with the run date attached."],
    ["2 &middot; Transform (Python)",
     "Per-source Python modules normalise currency and dates, map meters to product and meter sub-category, convert "
     "Copilot Studio credits to charges, and resolve every record to a cost centre through the ownership hierarchy. "
     "Tax is computed separately so it can be toggled on or off at query time."],
    ["3 &middot; Allocate",
     "Resolved records are folded into the shared segment / sub-segment / tower / function hierarchy so AI spend "
     "aggregates the same way as the rest of the cloud estate."],
    ["4 &middot; Serve (PostgreSQL)",
     "Monthly fact tables plus narrow dimension tables, indexed on the filter columns the dashboard exposes "
     "(month, segment, sub-segment, tower, function, cost centre)."],
    ["5 &middot; Visualise (Grafana)",
     "One dashboard, four tabs. Template variables drive every panel, so a single filter set applies across "
     "all three products simultaneously."],
], [1.22 * inch, CW - 1.22 * inch])]

F += [P("Why Grafana rather than a BI tool", "h3"),
      B("The team already operated Grafana for platform telemetry &mdash; no new tool, licence or access model."),
      B("Template variables give one filter bar across four tabs without duplicating queries per panel."),
      B("PostgreSQL is queried directly, so there is no extra semantic layer to keep in sync with the warehouse."),
      B("Dashboards version as JSON and review like code.")]

F += [callout("Cost-centre resolution",
              "Resolution runs as an ordered waterfall &mdash; explicit finance override, then validated resource tag, "
              "then inventory and parent mappings, then history, then a regional default. Every record carries the "
              "rule that resolved it, so an unexpected allocation can always be traced back to the step that produced it.",
              AMBER)]

F += [PageBreak()]

# ---- Dashboard ------------------------------------------------------------ #
F += [P("THE DASHBOARD", "eyebrow"), P("Four tabs, one filter bar", "h2"),
      P("The Summary tab answers &ldquo;what are we spending on AI in total, and who is spending it?&rdquo; "
        "The three product tabs answer &ldquo;why?&rdquo;", "body")]

F += [shot("ai-cost-01-summary.png",
           "Summary tab &mdash; total AI charges across Gen AI, GitHub Copilot and Copilot Studio, with product "
           "split, a 12-month trend, and breakdowns by sub-segment and cost centre. One filter bar (month, segment, "
           "sub-segment, tower, function, cost centre, include-tax) drives every tab.")]

F += [P("Design decisions worth noting", "h3"),
      B("<b>Annual and current-month side by side.</b> Every stat panel shows both, because "
        "the single most common question is &ldquo;is this month unusual?&rdquo;"),
      B("<b>Include Tax is a toggle, not a separate dashboard.</b> Finance reconciles with tax; "
        "engineering compares without it. Pre-computing both in the fact table makes it a filter."),
      B("<b>Product split up front.</b> Gen AI dominates spend; surfacing that share immediately "
        "stops teams optimising the wrong product.")]

F += [PageBreak()]

F += [shot("ai-cost-02-genai.png",
           "Gen AI Consumption tab &mdash; meter-category trend, environment split, top models by YTD charge, and "
           "top cost centres by model. The in-dashboard note documents the Dec-2025 re-categorisation of Cognitive "
           "Services into Foundry Models and Foundry Tools, so the trend break is explained where it is seen.")]

F += [P("The environment split is the actionable panel here: non-production and sandbox spend on "
        "generative models is where unreviewed experimentation accumulates, and separating it from "
        "production spend turns a single large number into a conversation about which workloads "
        "actually need frontier models.", "body")]

F += [Spacer(1, 6)]

F += [shot("ai-cost-03-copilot.png",
           "GitHub Copilot tab &mdash; seat charges by segment and cost centre, a consumption trend that overlays "
           "charges against total, EMU and non-EMU user counts, and a user-level detail table. Personal columns are "
           "redacted in this published version.")]

F += [P("Copilot is a licence, not a meter", "h3"),
      P("Because Copilot is billed per seat, cost per active user &mdash; not total cost &mdash; is the metric that "
        "matters. Plotting charges against user counts on a shared time axis makes the two separable: a rising "
        "line with flat seats is a price change, while flat charges with falling seats is unreclaimed licence waste. "
        "The user-level table exists so a cost-centre owner can identify dormant seats and reclaim them.", "body")]

F += [Spacer(1, 6)]

F += [shot("ai-cost-04-copilot-studio.png",
           "Copilot Studio tab &mdash; consumed credits and converted charges by sub-segment, cost centre and "
           "environment, with a production vs non-production monthly comparison. The disclaimer panel records the "
           "Microsoft capacity change that caused the November drop.")]

F += [callout("Documenting discontinuities inside the dashboard",
              "Copilot Studio charges fall sharply from November because Microsoft moved capacity drawing from "
              "tenant level to environment level &mdash; a platform change, not reduced usage. The explanation lives "
              "in a panel directly above the chart. A trend break that is not explained where it is seen will be "
              "mis-read as a saving, and someone will claim credit for it.")]

F += [PageBreak()]

# ---- Outcomes ------------------------------------------------------------- #
F += [P("OUTCOME", "eyebrow"), P("What it changed", "h2")]

F += [table([
    ["Before", "After"],
    ["Three separate exports reconciled by hand in spreadsheets, monthly.",
     "One scheduled pipeline; the dashboard is current without manual effort."],
    ["AI spend invisible below segment level.",
     "Every charge resolves to a cost centre, with the resolution rule recorded."],
    ["Copilot Studio reported in credits, not currency.",
     "Credits converted in the transformation layer; all three products sum in one number."],
    ["&ldquo;Why did this change?&rdquo; answered by email.",
     "Meter re-categorisation and the capacity change documented in-panel, next to the trend."],
    ["Finance and engineering looked at different extracts.",
     "One dashboard; the Include&nbsp;Tax toggle serves both reconciliation and comparison."],
], [CW / 2, CW / 2])]

F += [P("What I would do next", "h3"),
      B("<b>Unit economics.</b> Cost per active Copilot seat and cost per 1K tokens by model, "
        "so efficiency is trackable independently of volume."),
      B("<b>Budget thresholds.</b> Grafana alerting on cost-centre spend against plan, rather than "
        "relying on someone opening the dashboard."),
      B("<b>Anomaly detection.</b> Port the model already used for general cloud spend onto the AI "
        "fact tables &mdash; the Gen AI series is volatile enough to justify it."),
      B("<b>Forecast overlay.</b> Project month-end spend from partial-month consumption, which is "
        "the question finance actually asks mid-month.")]

F += [Spacer(1, 10), rule(LINE, 1, 0, 8)]
F += [callout("Note on this document",
              "All screenshots are redacted for publication. Employee names, email addresses and employee IDs are "
              "permanently removed, and absolute financial values are obscured. Panel layout, chart structure and "
              "dashboard design are unchanged. Figures shown are illustrative and are not representative of any "
              "organisation's actual AI expenditure.",
              GREY)]

doc.build(F)
print(f"{OUT}  ({OUT.stat().st_size // 1024} KB)")
