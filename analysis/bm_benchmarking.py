"""
BM: Benchmarking — Multi-Measure 3-Level Comparison
Data: IGS + CHR + CDC PLACES + Census ACS
URL: https://www.inclusivegrowthscore.com
Chart: C15 (Multi-measure benchmarking dashboard)
"""

import plotly.graph_objects as go
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'bm')
os.makedirs(OUT, exist_ok=True)

SRC = 'Sources: IGS 2025  •  CHR 2025  •  CDC PLACES 2023  •  Census ACS 2023'

# ═══════════════════════════════════════════════════════════════════════════════
# BM.1 — C15: Multi-Measure Benchmarking
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("BM.1: MULTI-MEASURE BENCHMARKING")
print("=" * 60)

measures = [
    'Poverty Rate', 'Life Expectancy', 'Obesity', 'Diabetes',
    'Employer Insurance', 'Disability Rate', 'Food Insecurity', 'Broadband Access',
]
sh_vals = [33.7, 70.0, 42.9, 16.2, 7.9, 43.0, 33.4, 66.1]
la_vals = [18.9, 73.3, 36.8, 13.2, 27.6, 31.0, 20.1, 83.0]
us_vals = [12.4, 78.4, 32.9, 10.3, 55.0, 28.3, 15.6, 89.1]

for m, s, l, u in zip(measures, sh_vals, la_vals, us_vals):
    print(f"  {m:>20s}: St.H {s:6.1f}  |  LA {l:6.1f}  |  US {u:6.1f}")

fig = go.Figure()

fig.add_trace(go.Bar(
    y=measures, x=us_vals, orientation='h', name='United States',
    marker=dict(color=TEAL, cornerradius=3),
))
fig.add_trace(go.Bar(
    y=measures, x=la_vals, orientation='h', name='Louisiana',
    marker=dict(color=AMBER, cornerradius=3),
))
fig.add_trace(go.Bar(
    y=measures, x=sh_vals, orientation='h', name='St. Helena Parish',
    marker=dict(color=CORAL, cornerradius=3),
))

fig.update_layout(
    **base_layout('St. Helena Trails on Every Measure That Matters',
                  width=1060, height=600, b_margin=130, l_margin=170, r_margin=60),
    barmode='group',
    xaxis=dict(
        title=dict(text='Value (% or Years)', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
    ),
    yaxis=dict(
        tickfont=dict(size=12, color=NAVY, family='Arial'),
        categoryorder='array', categoryarray=measures[::-1],
    ),
    legend=grouped_legend(),
    bargap=0.25,
    annotations=[source_annotation(SRC, y=-0.22)],
)

fig.write_image(os.path.join(OUT, 'bm_benchmarking.png'), scale=3)
print("  → bm_benchmarking.png")

print("\n" + "=" * 60)
print("BM COMPLETE — 1 chart saved to outputs/bm/")
print("=" * 60)
