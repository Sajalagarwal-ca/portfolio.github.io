"""
Build the ONE API Agent project PDF for the portfolio.

Source material: the one-api-agent README and the published blog post. There are
no UI screenshots for this project, so the diagrams are drawn with Platypus
tables rather than embedded images.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "One_API_Agent.pdf"

NAVY = colors.HexColor("#13324C")
TEAL = colors.HexColor("#007985")
DEEP = colors.HexColor("#006A79")
INK = colors.HexColor("#23384D")
GREY = colors.HexColor("#5F7383")
LINE = colors.HexColor("#D9E5EB")
PALE = colors.HexColor("#F2F8F9")
AMBER = colors.HexColor("#B8720A")
BLUE = colors.HexColor("#2251FF")

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
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=11.6,
                           textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=8.4, leading=11.6,
                            textColor=NAVY),
    "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8.4, leading=11.6,
                            textColor=colors.white),
    "note": ParagraphStyle("note", fontName="Helvetica", fontSize=8.6, leading=12.4,
                           textColor=INK),
    "lane": ParagraphStyle("lane", fontName="Helvetica-Bold", fontSize=7.6, leading=10,
                           textColor=colors.white, alignment=TA_CENTER),
    "laned": ParagraphStyle("laned", fontName="Helvetica-Bold", fontSize=7.6, leading=10,
                            textColor=NAVY, alignment=TA_CENTER),
    "lanel": ParagraphStyle("lanel", fontName="Helvetica-Bold", fontSize=7.4, leading=10,
                            textColor=BLUE),
    "stepn": ParagraphStyle("stepn", fontName="Helvetica-Bold", fontSize=11, leading=13,
                            textColor=colors.white, alignment=TA_CENTER),
    "steph": ParagraphStyle("steph", fontName="Helvetica-Bold", fontSize=7.4, leading=9.4,
                            textColor=NAVY, alignment=TA_CENTER),
    "stepb": ParagraphStyle("stepb", fontName="Helvetica", fontSize=6.5, leading=8.4,
                            textColor=GREY, alignment=TA_CENTER),
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


def lanes(rows):
    """rows = [(label, [cells], fill, fg_style)] -> stacked architecture diagram."""
    lw = 1.15 * inch
    out = []
    for label, cells, fill, fg in rows:
        n = len(cells)
        bw = (CW - lw) / n
        data = [[Paragraph(label, S["lanel"])] + [Paragraph(c, S[fg]) for c in cells]]
        ts = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
              ("TOPPADDING", (0, 0), (-1, -1), 7),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
              ("LEFTPADDING", (0, 0), (-1, -1), 4),
              ("RIGHTPADDING", (0, 0), (-1, -1), 4),
              ("BACKGROUND", (1, 0), (-1, -1), fill),
              ("GRID", (1, 0), (-1, -1), 1.6, colors.white)]
        out.append(Table(data, colWidths=[lw] + [bw] * n, style=TableStyle(ts)))
    return out


def steps(items):
    """items = [(n, head, body)] -> horizontal numbered pipeline."""
    n = len(items)
    bw = CW / n
    nums = [Paragraph(i[0], S["stepn"]) for i in items]
    heads = [Paragraph(i[1], S["steph"]) for i in items]
    bodies = [Paragraph(i[2], S["stepb"]) for i in items]
    t = Table([nums, heads, bodies], colWidths=[bw] * n,
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                  ("BACKGROUND", (0, 1), (-1, -1), PALE),
                  ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                  ("VALIGN", (0, 1), (-1, -1), "TOP"),
                  ("GRID", (0, 0), (-1, -1), 1.6, colors.white),
                  ("TOPPADDING", (0, 0), (-1, 0), 5),
                  ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                  ("TOPPADDING", (0, 1), (-1, 1), 7),
                  ("BOTTOMPADDING", (0, 2), (-1, 2), 8),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3),
                  ("RIGHTPADDING", (0, 0), (-1, -1), 3),
              ]), spaceBefore=6, spaceAfter=10)
    return t


def weightbar(label, w, desc, col):
    full = 1.55 * inch          # must fit inside the bar column width below
    bar = Table([[""]], colWidths=[full * (w / 0.55)], rowHeights=[9],
                style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), col),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                  ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                  ("TOPPADDING", (0, 0), (-1, -1), 0),
                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return [Paragraph(label, S["cellb"]), bar,
            Paragraph(f'<font color="{col.hexval()}"><b>{w:.2f}</b></font>', S["cell"]),
            Paragraph(desc, S["cell"])]


# --------------------------------------------------------------------------- #
def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PH - 0.22 * inch, PW, 0.22 * inch, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PH - 0.26 * inch, PW * 0.34, 0.04 * inch, stroke=0, fill=1)
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(GREY)
    canvas.drawString(MARGIN, 0.46 * inch, "ONE API Agent \u00b7 Grounded Multi-Agent Service")
    canvas.drawRightString(PW - MARGIN, 0.46 * inch, f"Page {doc.page}")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, 0.62 * inch, PW - MARGIN, 0.62 * inch)
    canvas.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=LETTER,
                      leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=0.58 * inch, bottomMargin=0.78 * inch,
                      title="ONE API Agent - Grounded Multi-Agent Service",
                      author="Sajal Agarwal",
                      subject="Multi-agent RAG service with confidence gating and citation enforcement")
frame = Frame(MARGIN, 0.78 * inch, CW, PH - 0.58 * inch - 0.78 * inch, id="f")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])

F = []

F += [
    P("PYTHON &middot; FLASK &middot; FAISS + BM25 &middot; AZURE AI FOUNDRY &middot; AKS &middot; ISTIO", "eyebrow"),
    P("ONE API Agent", "h1"),
    P("A multi-agent service that answers natural-language questions about applications, "
      "cost centres, platforms and incidents &mdash; with citations, a confidence score, and a "
      "hard-wired willingness to say <i>I don&rsquo;t know</i>.", "sub"),
    rule(NAVY, 2.2, 0, 12),
]

F += [table([
    ["Problem", "Estate truth is spread across an internal API, a read-only Postgres store, a published "
                "documentation index and ServiceNow. Four access paths, four query dialects, four owning teams."],
    ["Approach", "Four thin domain agents behind one OpenAI Assistants-compatible protocol, sharing a single "
                 "grounding layer: hybrid retrieval, confidence gating, citation enforcement and telemetry."],
    ["Stack", "Python 3.13, Flask 3, Gunicorn, FAISS, BM25Okapi, Azure AI Foundry, PostgreSQL, Docker, "
              "AKS, Istio, New Relic."],
    ["My role", "End-to-end: retrieval architecture, confidence model, agent design, A2A protocol layer, "
                "Kubernetes deployment and evaluation harness."],
], [0.95 * inch, CW - 0.95 * inch], header=False)]

F += [P("The problem", "h2"),
      P("A large amount of senior engineering time goes to questions that are not engineering at all. "
        "<i>Who owns this application? Which tower does this cost centre roll up to? What Kubernetes "
        "version is platform Y running? What changed before last night&rsquo;s P1?</i>", "body"),
      P("Each is a thirty-second lookup &mdash; <b>if</b> you know which system holds the answer and what "
        "the field is called. That conditional is the whole problem: the human becomes the integration "
        "layer, and context-switching is the tax paid on every question.", "body")]

F += [P("Why a generic copilot makes it worse", "h3"),
      P("Putting an off-the-shelf LLM in front of everything fails for a reason that is easy to state and "
        "hard to engineer around: <b>a general-purpose model is optimised to produce a plausible answer, "
        "and the enterprise needs a provable one.</b> A hallucinated application owner does not look "
        "wrong &mdash; it looks exactly like a correct answer, and it flows silently into a chargeback "
        "dispute, an access review or a P1 bridge.", "body")]

F += [table([
    ["Dimension", "Generic LLM copilot", "ONE API Agent"],
    ["Source of answer", "Model weights plus whatever it can reach",
     "Only retrieved, citable chunks and live API data"],
    ["On weak evidence", "Answers anyway, confidently",
     "Refuses &mdash; <i>insufficient_evidence</i>, with no LLM call at all"],
    ["Citations", "Often fabricated or unverifiable",
     "Invented chunk ids stripped; answer discarded if none survive"],
    ["Confidence", "Opaque or absent", "Transparent multi-factor blend; every sub-score returned"],
    ["Auditability", "No trace", "Every query &mdash; grounded or refused &mdash; recorded as telemetry"],
    ["Regression safety", "Prompt-tuning by hope", "Golden evals assert grounding and refusal in CI"],
], [1.1 * inch, 2.2 * inch, CW - 3.3 * inch])]

F += [callout("The design question",
              "It was never &ldquo;which model?&rdquo; It was: what control plane do you build around a "
              "model so that groundedness becomes a property of the <i>system</i> rather than a property "
              "of the prompt?")]

F += [P("ARCHITECTURE", "eyebrow"), P("One service, four agents, one grounding layer", "h2"),
      P("Flask behind Gunicorn, containerised on AKS and exposed through an Istio VirtualService. "
        "Every conversational surface enters through the same door: an OpenAI Assistants-compatible "
        "agent-to-agent protocol with Entra ID / MSAL authentication and a discovery card, which is what "
        "makes the service pluggable into Copilot Studio without writing a connector.", "body")]

F += lanes([
    ("CHANNELS", ["Copilot Studio", "Azure AI Foundry", "Self-hosted chat UI", "REST / Swagger"],
     colors.HexColor("#E9EEF2"), "laned"),
    ("ENTRY \u00b7 A2A", ["Assistants-compatible<br/>threads &amp; runs", "MSAL / Entra ID auth",
                          "Istio ingress on AKS"], NAVY, "lane"),
    ("AGENTS", ["ONE API<br/>apps &amp; infra", "Cost Center<br/>finance hierarchy",
                "ETS Platforms<br/>RAG over docs", "Incident<br/>ServiceNow + GitHub"], BLUE, "lane"),
    ("GROUNDING", ["Hybrid BM25<br/>+ FAISS", "Confidence gate", "Citation<br/>enforcement",
                   "Query cache<br/>+ telemetry"], colors.HexColor("#DCEFEF"), "laned"),
    ("SOURCES", ["ONE API", "Insights Postgres<br/>(read-only)", "Status-page<br/>doc index",
                 "ServiceNow /<br/>GitHub Actions"], colors.HexColor("#E9EEF2"), "laned"),
])

F += [Spacer(1, 10),
      P("Agents are thin and specialised; the grounding layer is shared. A new domain inherits "
        "confidence scoring, citation enforcement and telemetry on day one &mdash; and, just as "
        "importantly, cannot quietly opt out of them.", "body")]

F += [P("Groundedness as a pipeline, not a prompt", "h2"),
      P("Generation is a <b>fixed pipeline</b>. There is no agentic free-for-all in which the model "
        "decides whether to search: retrieval and gating are deterministic and happen first, generation "
        "is a single tool-less call, and the output is post-processed before a user ever sees it.", "body")]

F += [steps([
    ("1", "Ingest", "Per-platform JSON chunks with inline embeddings, cached locally"),
    ("2", "Hybrid retrieve", "FAISS cosine + BM25 keyword, side by side"),
    ("3", "Fuse &amp; rerank", "Reciprocal Rank Fusion, then optional LLM rerank"),
    ("4", "Filter", "Drop chunks below the per-chunk floor (0.30)"),
    ("5", "Score", "Semantic + lexical + margin + authority &times; freshness"),
    ("6", "Gate", "Below 0.35: refuse, with zero LLM calls"),
    ("7", "Generate", "Stuffed context, no tools \u2014 cannot fetch or invent"),
    ("8", "Enforce", "Strip unknown chunk ids; discard if none survive"),
])]

F += [table([
    ["Outcome", "What the caller receives"],
    ["Grounded answer", "Cited text plus a clickable Sources panel &mdash; chunk id, heading, platform, "
                        "commit timestamp and an absolute URL to the live document."],
    ["Refusal", "<i>insufficient_evidence</i>, grounded: false &mdash; explainable, because every "
                "confidence sub-score is returned alongside it."],
    ["Telemetry", "Index version, candidate chunk ids, confidence and gate decision, emitted for "
                  "grounded and refused queries alike."],
], [1.05 * inch, CW - 1.05 * inch])]

F += [callout("Refusal is a feature",
              "Stages 4, 6 and 8 are three independent opportunities to stop a bad answer &mdash; two of "
              "them before a single token is generated. The system is designed to say &ldquo;I don't "
              "know&rdquo; rather than produce an unverifiable answer.", AMBER)]

F += [P("Why hybrid retrieval, not just embeddings", "h3"),
      P("Pure vector search is excellent at paraphrase and terrible at identifiers &mdash; ask about a "
        "version string or an error code and cosine similarity returns a semantically adjacent paragraph "
        "that does not contain the token. Pure keyword search has the mirror failure. So the index is "
        "built twice over the same chunks: an in-memory FAISS <i>IndexFlatIP</i> over L2-normalised "
        "vectors, and a BM25Okapi index. The two rankings merge with Reciprocal Rank Fusion, which "
        "combines <i>ranks</i> rather than scores and so needs no normalisation between two incomparable "
        "scales.", "body")]

F += [P("CONFIDENCE", "eyebrow"), P("A score you can argue with", "h2"),
      P("Deliberately not a learned scorer &mdash; a transparent blend of four normalised signals with "
        "environment-tunable weights, every sub-score returned with the answer.", "body")]

F += [Table([
    weightbar("Top semantic cosine", 0.55, "Strength of the best embedding match", BLUE),
    weightbar("BM25 lexical agreement", 0.20, "Does the keyword index agree with the vectors?",
              colors.HexColor("#00A9F4")),
    weightbar("Top-vs-second margin", 0.10, "Is the winner clearly ahead of the runner-up?", TEAL),
    weightbar("Authority &times; freshness", 0.15,
              "Doc-type authority, decayed on a 180-day half-life over git commit time", AMBER),
], colWidths=[1.5 * inch, 1.75 * inch, 0.52 * inch, CW - 3.77 * inch],
    style=TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                      ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, PALE]),
                      ("LEFTPADDING", (0, 0), (-1, -1), 7),
                      ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                      ("TOPPADDING", (0, 0), (-1, -1), 7),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                      ("GRID", (0, 0), (-1, -1), 0.6, LINE)]), spaceAfter=10)]

F += [table([
    ["Gate", "Rule", "Effect"],
    ["Query gate", "confidence &ge; 0.35", "Below it the agent refuses before any LLM call is made."],
    ["Chunk floor", "per-chunk &ge; 0.30", "Weak evidence never reaches the prompt."],
    ["Scope guard", "0.35 / 0.45 bounds", "An ambiguous platform choice falls back to searching all."],
], [0.95 * inch, 1.35 * inch, CW - 2.3 * inch])]

F += [P("<b>Authority &times; freshness</b> encodes something a model has no way to know: that a generated "
        "versions file is more authoritative than an architecture note, which is more authoritative than "
        "a runbook, and that a document last committed eighteen months ago should be trusted less than "
        "one committed last week. Because every sub-score is returned, a refusal is explainable &mdash; "
        "you can see whether nothing matched semantically, or the top two candidates were "
        "indistinguishable, or the only supporting document was stale.", "body")]

F += [P("ENGINEERING", "eyebrow"), P("The parts that are not about AI at all", "h2")]

F += [table([
    ["Decision", "Why"],
    ["Stateless, context-carrying follow-ups",
     "Chat history is never injected into the grounded prompt &mdash; stacking a fresh grounded "
     "instruction on a prior one reliably pushes models into refusing. Recent turns are folded into a "
     "<i>contextualised retrieval query</i> instead, which is also used as the grounded question. One "
     "deterministic carrier of conversation context."],
    ["Enumeration-aware retrieval",
     "A single global top-k starves &ldquo;list all X across every platform&rdquo; queries. Rather than a "
     "brittle intent classifier, the strategy is derived from <i>scope cardinality</i>: one platform means "
     "focused search; two or more means per-platform retrieval, unioned and re-ranked."],
    ["An incident agent with no database",
     "GitHub Actions is the job store &mdash; each run is identified by its run name and returns a result "
     "artifact. Thread ownership lives as a hashed owner email in conversation metadata. No schema, no "
     "migrations, no state to drift."],
    ["Idempotency, guarded twice",
     "A non-blocking per-ticket lock inside the pod <i>and</i> a per-ticket workflow concurrency group "
     "upstream, because the two failure modes differ: concurrent requests to one pod, and concurrent "
     "requests across pods."],
    ["Memory as a capacity decision",
     "Each Gunicorn worker holds its own in-memory FAISS + BM25 + embeddings copy, so per-pod memory "
     "scales with worker count &mdash; which is why pod limits are sized explicitly rather than inherited. "
     "Database access is read-only by credential, not by convention."],
], [1.52 * inch, CW - 1.52 * inch])]

F += [P("Caching, and being honest about it", "h3"),
      P("A cache hit returns the stored answer and its sources, skipping retrieval <i>and</i> generation "
        "entirely, keyed on query, index version and platform scope so a re-published index invalidates "
        "naturally. Refusals are never cached, because the missing evidence may arrive tomorrow.", "body"),
      P("The caveat is published rather than hidden: the cache is <b>pod-local SQLite</b> &mdash; shared "
        "across a pod&rsquo;s workers via WAL, but not across replicas and not durable across restarts. "
        "A deliberate stage-one trade-off, and the first item on the roadmap. Documenting the limitation "
        "is part of the same discipline as refusing an ungrounded answer.", "body")]

F += [P("OUTCOME", "eyebrow"), P("What it delivers", "h2")]

F += [table([
    ["Audience", "Value"],
    ["Engineers", "Plain-language access without learning four query dialects, with follow-up questions "
                  "that retain their context."],
    ["Finance &amp; risk", "Every cost-centre or approver answer arrives with a source link and a "
                           "confidence score that can be defended in a review."],
    ["Incident response", "Ticket analysis dispatched and tracked without standing up another database, "
                          "with duplicate-run protection on the bridge."],
    ["The platform", "Grounding, confidence, citation and telemetry are shared services &mdash; the next "
                     "agent inherits them on day one."],
], [1.2 * inch, CW - 1.2 * inch])]

F += [P("Roadmap", "h3"),
      B("<b>Durable shared cache</b> across replicas, replacing the pod-local SQLite store."),
      B("<b>Close the rolling-deploy window</b> in which two pods can create one duplicate queued run."),
      B("<b>Expand golden evals</b> to the cost-centre and ONE API agents, not just platforms."),
      B("<b>Publish the grounding layer</b> as a reusable internal library so confidence thresholds "
        "become a governed, per-domain risk setting.")]

F += [Spacer(1, 8), rule(LINE, 1, 0, 8)]
F += [callout("The transferable lesson",
              "Fluency is cheap and getting cheaper. Traceability is the scarce thing &mdash; and it is "
              "an engineering property, not a model capability. Decide your refusal policy before your "
              "model: &ldquo;what happens when we don&rsquo;t know?&rdquo; is an architecture question, "
              "and answering it late means retrofitting gates around a system never designed to stop.",
              GREY)]

doc.build(F)
print(f"{OUT}  ({OUT.stat().st_size // 1024} KB)")
