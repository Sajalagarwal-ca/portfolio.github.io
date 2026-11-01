"""
Prepare Grafana AI-cost screenshots for PUBLIC publication.

Two classes of redaction:
  1. PII      -> hard black box (irreversible, nothing recoverable)
  2. Financials -> heavy Gaussian blur on headline KPI values + org identifier

Black boxes are used for personal data because blur can sometimes be attacked;
a filled rectangle destroys the pixels outright.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SRC = Path(r"C:\Users\agasaja\OneDrive - Manulife\Pictures\Screenshots")
DST = Path(r"C:\Users\agasaja\Python_Projects\portfolio.github.io\images\ai-cost")
DST.mkdir(parents=True, exist_ok=True)

# name: (source file, [PII boxes -> black], [financial boxes -> blur])
# Coordinates are in ORIGINAL screenshot pixels (see sizes printed on run).
JOBS = {
    "ai-cost-01-summary": (
        "Screenshot 2026-11-01 164608.png",
        [(128, 0, 262, 22)],                       # org breadcrumb
        [
            # headline KPI stats
            (772, 100, 892, 148), (1608, 100, 1782, 148),
            (230, 194, 300, 228), (505, 194, 598, 228),
            (805, 194, 893, 228), (1095, 194, 1176, 228),
            (1405, 194, 1484, 228),
            # donut centre label + legend values
            (262, 458, 348, 492), (80, 494, 440, 516),
            # 12-month trend y-axis
            (600, 268, 656, 486),
            # sub-segment chart x-axis
            (1296, 408, 1768, 452),
            # table value columns (bars left sharp, numbers blurred)
            (328, 588, 458, 808), (552, 588, 672, 808), (822, 588, 882, 808),
            (1212, 588, 1332, 808), (1456, 588, 1552, 808), (1686, 588, 1760, 808),
        ],
    ),
    "ai-cost-02-genai": (
        "Screenshot 2026-11-01 164909.png",
        [],
        [
            (496, 222, 594, 262), (1056, 222, 1186, 262), (1655, 222, 1772, 262),
            (228, 330, 350, 516),              # Total Cost column
            (380, 320, 430, 502),              # meter-category trend y-axis
            (965, 298, 1018, 482),             # env chart y-axis labels
            (1015, 296, 1790, 342),            # env top bar value label
            (1015, 400, 1790, 480),            # env remaining bar value labels
            (456, 586, 518, 668), (456, 744, 518, 772),   # product break-up charges
            (530, 576, 590, 682),              # top-10 models y-axis
            (1552, 588, 1756, 758),            # top-10 cost centre YTD column
        ],
    ),
    "ai-cost-03-copilot": (
        "Screenshot 2026-11-01 164926.png",
        [(488, 461, 1120, 628)],               # Emp ID / Name / Email columns
        [
            (342, 92, 444, 136), (787, 92, 889, 136),
            (1212, 92, 1334, 136), (1686, 92, 1769, 136),
            (326, 184, 402, 294),              # segment legend values
            (712, 208, 870, 370),              # cost-centre charges column
            (894, 178, 950, 356), (1286, 178, 1324, 356),  # trend axes
            (1686, 184, 1738, 204),            # user-level legend value
            (1594, 458, 1758, 648),            # table charges column
        ],
    ),
    "ai-cost-04-copilot-studio": (
        "Screenshot 2026-11-01 164952.png",
        [],
        [
            (355, 177, 436, 209), (807, 177, 876, 209),
            (1235, 177, 1322, 209), (1658, 177, 1766, 209),
            (268, 286, 562, 450),              # credits consumed + charges cols
            (594, 272, 658, 456),              # monthly trend y-axis
            (1548, 286, 1766, 450),            # charges-by-env charges column
            (505, 518, 590, 560),              # env donut legend values
            (594, 518, 658, 702),              # prod vs non-prod y-axis
            (1458, 538, 1766, 710),            # credits by env-name columns
        ],
    ),
}

LABEL = "REDACTED"

# Headline blurring alone is not enough: the same totals are legible in donut
# legends, table value columns and chart axes. Rather than chase dozens of tiny
# rectangles, the published image is also downsampled. At 1200px wide the ~10px
# Grafana table text becomes physically unresolvable, and because the asset is
# rasterised at that size nobody can zoom back in to recover it.
PUBLISH_WIDTH = 1200


def blur_box(img, box, radius=14):
    region = img.crop(box).filter(ImageFilter.GaussianBlur(radius))
    img.paste(region, box)


for name, (fname, pii, money) in JOBS.items():
    src = SRC / fname
    img = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(img)

    for box in money:
        blur_box(img, box)

    for box in pii:
        draw.rectangle(box, fill=(18, 20, 24))
        x0, y0, x1, y1 = box
        draw.rectangle(box, outline=(120, 130, 140), width=1)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        draw.text((cx - 32, cy - 6), LABEL, fill=(150, 160, 170))

    full = img.size
    if img.width > PUBLISH_WIDTH:
        h = round(img.height * PUBLISH_WIDTH / img.width)
        img = img.resize((PUBLISH_WIDTH, h), Image.LANCZOS)

    out = DST / f"{name}.png"
    img.save(out, optimize=True)
    print(f"{out.name:34} {full} -> {img.size}  pii={len(pii)} "
          f"blur={len(money)}  {out.stat().st_size // 1024} KB")
