"""Render the Note's figures as theme-aware SVG, straight from the results files.

    python3 04-analysis/04_figures.py

Reads `05-results/` and writes `06-report/figures/`. It reads no metric table, so it runs
after unblinding without touching the outcome again, and every number it draws is one a reader
can find in the machine-readable results beside it.

WHY SVG AND WHY STATIC. The Note is a document and not a dashboard, and it has to survive
being printed, archived at Software Heritage, and read from a git diff six years from now. SVG
is text, so a figure changing shows up as a reviewable diff and not an opaque binary swap. The
visualisation guidance ships a hover layer by default for HTML and SVG charts, and that default
is declined here on purpose, since there is no interaction to offer a reader of a static
document,
and a tooltip that never appears is worse than a direct label that always does. Every value a
tooltip would have carried is printed on the mark instead.

COLOUR. Palette slots and ink tokens are the reference instance, validated with the supplied
checker instead of by eye. The two-segment stack uses categorical slots 1 and 2, which pass
every gate in both modes. The country figure uses the emphasis form, one accent hue against
de-emphasis gray, where the checker's chroma floor reports a fail on the gray: that check is
scoped to categorical palettes, in which every slot must read as a distinct hue, and emphasis is
by definition one hue plus an achromatic remainder. CVD separation for the pair is 15.9 and
normal-vision separation 17.8, both comfortably clear, and every bar is directly labelled, so
the distinction never rests on colour alone.

Bar length carries magnitude in all four figures, so colour is never asked to encode the same
thing twice.
"""
import json
import sys
from pathlib import Path

import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
RESULTS = STUDY / "05-results"
OUT = STUDY / "06-report" / "figures"

W = 760
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'

STYLE = """
  .s  { fill: #fcfcfb }
  .t1 { fill: #0b0b0b } .t2 { fill: #52514e } .tm { fill: #898781 }
  .grid  { stroke: #e1e0d9; stroke-width: 1 }
  .axis  { stroke: #c3c2b7; stroke-width: 1 }
  .c1 { fill: #2a78d6 } .c2 { fill: #eb6834 } .cg { fill: #898781 }
  .gap { stroke: #fcfcfb; stroke-width: 2 }
  @media (prefers-color-scheme: dark) {
    .s  { fill: #1a1a19 }
    .t1 { fill: #ffffff } .t2 { fill: #c3c2b7 }
    .grid { stroke: #2c2c2a } .axis { stroke: #383835 }
    .c1 { fill: #3987e5 } .c2 { fill: #d95926 }
    .gap { stroke: #1a1a19 }
  }
"""


def bar(x, y, w, h, cls, round_right=True):
    """Horizontal bar anchored at the baseline, 4px rounded on the data end only."""
    w = max(w, 0.01)
    r = min(4, w, h / 2)
    if not round_right or w <= r:
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" class="{cls}"/>'
    return (f'<path class="{cls}" d="M{x:.1f} {y} H{x+w-r:.1f} a{r} {r} 0 0 1 {r} {r} '
            f'V{y+h-r} a{r} {r} 0 0 1 -{r} {r} H{x:.1f} Z"/>')


def svg(body, height, title, subtitle, note=None):
    h = height + (18 if note else 0)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
             f'viewBox="0 0 {W} {h}" font-family=\'{FONT}\' role="img" '
             f'aria-label="{title}. {subtitle}">',
             f"<style>{STYLE}</style>",
             f'<rect width="{W}" height="{h}" class="s"/>',
             f'<text x="0" y="18" class="t1" font-size="15" font-weight="600">{title}</text>',
             f'<text x="0" y="38" class="t2" font-size="12.5">{subtitle}</text>', body]
    if note:
        parts.append(f'<text x="0" y="{h-4}" class="tm" font-size="11">{note}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def fig_gate_f(p):
    """The headline, which is that two coverage measures agree. Emphasis is on their sameness."""
    cov_pop = p["gate_f"]["coverage_population"] * 100
    cov_cnt = p["gate_f"]["coverage_gauge_count"] * 100
    rows = [("Weighted by population in reach", cov_pop),
            ("Counted per gauge, rung 2", cov_cnt)]
    x0, top, bh, gap, scale = 250, 62, 30, 22, 380 / 12.0
    b = []
    for i, (lab, v) in enumerate(rows):
        y = top + i * (bh + gap)
        b.append(f'<text x="{x0-12}" y="{y+20}" class="t2" font-size="12.5" '
                 f'text-anchor="end">{lab}</text>')
        b.append(bar(x0, y, v * scale, bh, "c1"))
        b.append(f'<text x="{x0 + v*scale + 8}" y="{y+20}" class="t1" font-size="13" '
                 f'font-weight="600">{v:.1f}%</text>')
    yb = top + 2 * (bh + gap) - gap + 6
    b.append(f'<line x1="{x0}" y1="{top-6}" x2="{x0}" y2="{yb}" class="axis"/>')
    b.append(f'<text x="{x0}" y="{yb+18}" class="tm" font-size="11">'
             f'Difference 0.26 pp, where Gate F rejects the null only above 5 pp, so the null stands.'
             f'</text>')
    return svg("\n".join(b), yb + 30,
               "Coverage of the published evidence base does not depend on population",
               "Share of African forecast points carrying a published per-gauge metric, "
               "two ways of counting")


def fig_density(p):
    """Two segments per tercile: what file presence already fixed, and what content decided."""
    t = p["secondary_by_tercile"]
    names = {"T1_sparse": "Sparsest third", "T2": "Middle third", "T3_dense": "Densest third"}
    # Left margin sized to the longest population label rather than guessed: at 11px the
    # widest string is about 105px, and the first render clipped it against x0 = 150.
    x0, top, bh, gap, scale = 200, 88, 34, 20, 420 / 100.0
    b = ['<rect x="200" y="56" width="11" height="11" class="c1"/>',
         '<text x="217" y="66" class="t2" font-size="12">Fixed by whether a gauge was '
         'evaluated</text>',
         '<rect x="490" y="56" width="11" height="11" class="c2"/>',
         '<text x="507" y="66" class="t2" font-size="12">Decided by the published '
         'values</text>']
    for i, k in enumerate(["T1_sparse", "T2", "T3_dense"]):
        y = top + i * (bh + gap)
        floor = t[k]["structural_floor"] * 100
        attr = t[k]["share"] * 100 - floor
        pop = t[k]["denominator_pop"]
        b.append(f'<text x="{x0-12}" y="{y+16}" class="t1" font-size="12.5" '
                 f'text-anchor="end" font-weight="600">{names[k]}</text>')
        b.append(f'<text x="{x0-12}" y="{y+31}" class="tm" font-size="11" '
                 f'text-anchor="end">{pop:,.0f} in reach</text>')
        b.append(bar(x0, y, floor * scale, bh, "c1", round_right=False))
        b.append(bar(x0 + floor * scale + 2, y, attr * scale - 2, bh, "c2"))
        b.append(f'<text x="{x0+8}" y="{y+22}" font-size="12" fill="#ffffff" '
                 f'font-weight="600">{floor:.1f}%</text>')
        total = t[k]["share"] * 100
        lab = "99.998%" if k == "T1_sparse" else f"{total:.1f}%"
        b.append(f'<text x="{x0 + total*scale + 8}" y="{y+22}" class="t1" font-size="12.5" '
                 f'font-weight="600">{lab}</text>')
    yb = top + 3 * (bh + gap) - gap + 6
    b.append(f'<line x1="{x0}" y1="{top-6}" x2="{x0}" y2="{yb}" class="axis"/>')
    return svg("\n".join(b), yb + 26,
               "Most of the mapping-density gradient was settled before any value was read",
               "Population in reach of no evidenced forecast point, split by what fixed it",
               "Blue is where no gauge holds a metric file at all, so only the orange remainder "
               "was decided by what the published metrics say.")


def fig_archive(c):
    """Emphasis form: one country is the finding, the rest are context."""
    top = c.sort_values("evidenced_points", ascending=False).head(6)
    total_ev = 242
    x0, y0, bh, gap, scale = 150, 78, 26, 14, 430 / 90.0
    b = []
    for i, (_, r) in enumerate(top.iterrows()):
        y = y0 + i * (bh + gap)
        share = 100 * r.evidenced_points / total_ev
        cls = "c1" if r.iso3 == "ZAF" else "cg"
        b.append(f'<text x="{x0-12}" y="{y+12}" class="t1" font-size="12.5" '
                 f'text-anchor="end" font-weight="{"600" if r.iso3=="ZAF" else "400"}">'
                 f'{r.iso3}</text>')
        b.append(f'<text x="{x0-12}" y="{y+25}" class="tm" font-size="10.5" '
                 f'text-anchor="end">{r.population_in_reach:,.0f} in reach</text>')
        b.append(bar(x0, y, share * scale, bh, cls))
        b.append(f'<text x="{x0 + share*scale + 8}" y="{y+18}" class="t1" font-size="12.5" '
                 f'font-weight="{"600" if r.iso3=="ZAF" else "400"}">'
                 f'{share:.1f}%  ({int(r.evidenced_points)} of {int(r.forecast_points):,})</text>')
    yb = y0 + 6 * (bh + gap) - gap + 6
    b.append(f'<line x1="{x0}" y1="{y0-6}" x2="{x0}" y2="{yb}" class="axis"/>')
    return svg("\n".join(b), yb + 26,
               "The published evidence base follows a century-old gauge archive",
               "Share of all 242 evidenced African forecast points, by country, with the "
               "population in reach of each country's points",
               "All 741 African gauges holding a metric file are GRDC stations, and we report the "
               "association without attributing its cause.")


def fig_ladder(p):
    """One hue: length already carries the magnitude, so colour encodes nothing extra."""
    lad = [(k, v) for k, v in p["denominator_ladder"].items() if v]
    x0, y0, bh, gap, scale = 300, 70, 28, 16, 330 / 100.0
    b = []
    for i, (name, v) in enumerate(lad):
        y = y0 + i * (bh + gap)
        share = v["p_unevidenced"] * 100
        b.append(f'<text x="{x0-12}" y="{y+13}" class="t1" font-size="12.5" '
                 f'text-anchor="end">{name.split(", ")[1].capitalize()}</text>')
        b.append(f'<text x="{x0-12}" y="{y+26}" class="tm" font-size="10.5" '
                 f'text-anchor="end">{v["basins"]:,} basins, {v["population"]:,.0f} people</text>')
        b.append(bar(x0, y, share * scale, bh, "c1"))
        b.append(f'<text x="{x0 + share*scale + 8}" y="{y+19}" class="t1" font-size="12.5" '
                 f'font-weight="600">{share:.1f}%</text>')
    yb = y0 + len(lad) * (bh + gap) - gap + 6
    b.append(f'<line x1="{x0}" y1="{y0-6}" x2="{x0}" y2="{yb}" class="axis"/>')
    return svg("\n".join(b), yb + 26,
               "The answer depends on what you count, so every rung is published",
               "Population in reach of no evidenced forecast point, at each denominator",
               "A fifth rung, the product's own display surface, is not enumerable from any "
               "released artefact and is never used.")


def main():
    p = json.load(open(RESULTS / "primary.json"))
    c = pd.read_csv(RESULTS / "country_table.csv")
    OUT.mkdir(parents=True, exist_ok=True)
    figs = {"fig1-gate-f.svg": fig_gate_f(p), "fig2-mapping-density.svg": fig_density(p),
            "fig3-gauge-archive.svg": fig_archive(c), "fig4-denominator-ladder.svg": fig_ladder(p)}
    for name, s in figs.items():
        (OUT / name).write_text(s)
        print(f"  wrote 06-report/figures/{name}  ({len(s):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
