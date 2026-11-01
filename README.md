# Sajal Agarwal - Personal Portfolio

Welcome to the repository for my personal portfolio website!

## About

I am a **Senior Data Scientist** with 15+ years of experience in Machine Learning, Cloud Analytics, and Generative AI. 
This repository contains the source code for my personal portfolio, where I showcase my projects, professional experience, and education.

## Links

- **LinkedIn:** [Sajal Agarwal](https://www.linkedin.com/in/agarwalsajal/)
- **GitHub:** [@Sajalagarwal-ca](https://github.com/Sajalagarwal-ca)

## Projects Highlighted

Some of the key projects featured in this portfolio include:
- **Forecast Home Prices in Canada** (Linear Regression)
- **Cloud Cost Anomaly Detection & Optimization**
- **Time Series Forecasting for Cloud Chargeback**
- **Fraudulent Loan Application Detection**
- **AI Travel Assistant** (LLM-Powered)
- **Insurance Fraud Investigation** (RAG)
- **Executive Dashboards** (Power BI & Tableau)
- **[Application Data Quality](./power-bi-data-quality.html)** (Power BI, Power Query, DAX, SQL): snapshot-aware modeling, completeness reporting, and validation. The project card opens a case-study dialog, with a standalone page available without JavaScript. The report screenshot is a static preview, not a live Power BI embed.
- **Grafana AI Cost Observability** (Grafana, PostgreSQL, Azure Data Factory, Python): unifies Gen AI, GitHub Copilot and Copilot Studio spend into one cost-centre-level dashboard.
- **[ONE API Agent](https://github.com/Sajalagarwal-ca/one-api-agent)** (Flask, FAISS, BM25, Azure AI Foundry, AKS): a grounded multi-agent service with hybrid retrieval, confidence gating and citation enforcement — it refuses rather than hallucinates.

## Build Tools

`tools/` holds the generators for the Grafana AI Cost Observability assets. Run in order:

```bash
python tools/redact_screenshots.py    # 1. sanitise raw Grafana screenshots
python tools/build_ai_cost_pdf.py     # 2. images/Grafana_AI_Cost_Observability.pdf
python tools/build_ai_cost_blog.py    # 3. blog post, both variants
```

`build_ai_cost_blog.py` writes one file:

| Output | Images | Use |
|---|---|---|
| `tools/_build/ai_cost_observability_blog_google_blogger.html` | base64, ~1.1 MB | Paste into Blogger's HTML view. Scratch output, gitignored |

The post is published at
[thepracticaldatascientist.blogspot.com](https://thepracticaldatascientist.blogspot.com/2026/11/grafana-postgresql-azure-data-factory.html),
which is where the index's **Read Blog** button points — so the repo keeps no
second copy of the article to drift out of sync with it.

### Other tools

| Script | Purpose |
|---|---|
| `build_one_api_agent_pdf.py` | Builds `images/One_API_Agent.pdf` (project card preview) |
| `reorder_projects.py` | Sorts the project cards in `index.html` newest-first |

`reorder_projects.py` holds the authoritative project timeline in its `ORDER`
list — dates come from each card's first appearance in git history
(`git log -S<key> -- index.html`). Edit `ORDER` and re-run to re-sort. The
script refuses to write unless the result is a pure permutation of the
original file, so it cannot silently drop a card.

> **Heads-up:** `index.html` contains an HTML comment wrapping three older cards
> — *AI Travel Assistant*, *Insurance Fraud Investigation (RAG)* and *Power BI &
> Tableau Dashboards*. They do not render. The reorder script moves that block to
> the end of the card region and leaves it commented; uncomment it by hand to
> restore those cards.

**`redact_screenshots.py` must run first** — the PDF and blog builders consume only its
output in `images/ai-cost/`, never the raw screenshots. It permanently black-boxes
personal data (names, emails, employee IDs), blurs absolute financial values, and
downsamples to 1200px so residual small text is unresolvable. Requires `pillow`
and `reportlab`.

The blog file is a **Blogger-safe body fragment**: no `<!DOCTYPE>`/`<html>`/`<head>`/
`<body>`, no `<style>` block (all CSS is inline), no HTML comments, and all images
embedded as base64. Paste it into Blogger's HTML view and publish without switching
to Compose.

## Tech Stack

This website is built using:
- HTML5 / CSS3
- JavaScript (jQuery)
- Custom CSS and responsive design based on the [Massively](https://html5up.net/massively) template by HTML5 UP.

## Local Development

To view or modify this website locally:
1. Clone this repository: `git clone https://github.com/Sajalagarwal-ca/portfolio.github.io.git`
2. Open `index.html` in your preferred web browser.