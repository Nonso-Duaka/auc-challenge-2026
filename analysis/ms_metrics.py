"""
MS: Metrics for Success — Baselines, Targets, Timeframes
Data: CDC PLACES, CHR, Census ACS
Chart: C17 (Metrics dashboard)
"""

import plotly.graph_objects as go
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'ms')
os.makedirs(OUT, exist_ok=True)

SRC = 'Sources: CDC PLACES 2023  •  CHR 2025  •  Census ACS 2023'

# ═══════════════════════════════════════════════════════════════════════════════
# MS.1 — C17: Metrics Dashboard
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("MS.1: SUCCESS METRICS DASHBOARD")
print("=" * 60)

metrics =    ['IGS Score', 'Employer Insurance', 'Food Insecurity',
              'Prev. Hospitalizations', 'Uninsured Rate', 'Obesity Rate', 'Poverty Rate']
baselines =  [36, 7.9, 33.4, 4862, 7.5, 42.9, 33.7]
targets =    [42, 15.0, 25.0, 3800, 5.0, 38.0, 28.0]
timeframes = ['3 yr', '5 yr', '3 yr', '5 yr', '3 yr', '5 yr', '5 yr']

for m, b, t, tf in zip(metrics, baselines, targets, timeframes):
    print(f"  {m:>25s}: {b:>8} → {t:>8}  ({tf})")

fig = go.Figure()

fig.add_trace(go.Bar(
    y=metrics, x=baselines, orientation='h',
    name='Current Baseline',
    marker=dict(color=CORAL, cornerradius=3),
    text=[f'{b}' for b in baselines],
    textposition='outside',
    textfont=dict(size=11, color=CORAL),
))

fig.add_trace(go.Bar(
    y=metrics, x=targets, orientation='h',
    name='3–5 Year Target',
    marker=dict(color=TEAL, cornerradius=3),
    text=[f'{t}' for t in targets],
    textposition='outside',
    textfont=dict(size=11, color='#1B7A6E'),
))

fig.update_layout(
    **base_layout('Success Metrics: Where We Are vs Where We\'re Going',
                  width=1020, height=560, b_margin=130, l_margin=180, r_margin=80),
    barmode='group',
    xaxis=dict(
        title=dict(text='Value', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
    ),
    yaxis=dict(
        tickfont=dict(size=12, color=NAVY, family='Arial'),
        categoryorder='array', categoryarray=metrics[::-1],
    ),
    legend=grouped_legend(),
    bargap=0.25,
    annotations=[source_annotation(SRC, y=-0.22)],
)

fig.write_image(os.path.join(OUT, 'ms_metrics_dashboard.png'), scale=3)
print("  → ms_metrics_dashboard.png")

print("\n" + "=" * 60)
print("MS COMPLETE — 1 chart saved to outputs/ms/")
print("=" * 60)
