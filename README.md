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

## Build Tools

`tools/` holds the generators for the Grafana AI Cost Observability assets. Run in order:

```bash
python tools/redact_screenshots.py    # 1. sanitise raw Grafana screenshots
python tools/build_ai_cost_pdf.py     # 2. images/Grafana_AI_Cost_Observability.pdf
python tools/build_ai_cost_blog.py    # 3. blog post, both variants
```

`build_ai_cost_blog.py` writes the same article twice:

| Output | Images | Use |
|---|---|---|
| `ai-cost-observability.html` | relative paths, 28 KB | Standalone local copy of the post (not linked from the index) |
| `tools/_build/ai_cost_observability_blog_google_blogger.html` | base64, ~1.1 MB | Paste into Blogger's HTML view. Scratch output, gitignored |

The post is published at
[thepracticaldatascientist.blogspot.com](https://thepracticaldatascientist.blogspot.com/2026/11/grafana-postgresql-azure-data-factory.html),
which is where the index's **Read Blog** button points.

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