"""
IGS Ranking: State & National — St. Helena Parish comparison charts
Chart 1: Overall IGS Score horizontal bars + stat boxes
Chart 2: IGS Component Comparison table
Source: inclusivegrowthscore.com (2025 data, USA benchmark)
"""

import plotly.graph_objects as go
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'po')
os.makedirs(OUT, exist_ok=True)

SRC = 'Source: inclusivegrowthscore.com  |  2025 USA Benchmark  |  84,400+ census tracts'

# ─── Data ─────────────────────────────────────────────────────────────────────
SH   = {'igs': 36.2, 'place': 45.1, 'economy': 29.5, 'community': 32.6}
LA   = {'igs': 44.6, 'place': 41.9, 'economy': 47.7, 'community': 44.3}
NAT  = {'igs': 49.7, 'place': 48.9, 'economy': 50.4, 'community': 50.1}

SH_SUB  = {'place_g': 60, 'place_i': 29, 'econ_g': 41, 'econ_i': 19, 'comm_g': 24, 'comm_i': 42}
LA_SUB  = {'place_g': 39.9, 'place_i': 43.9, 'econ_g': 49.8, 'econ_i': 45.5, 'comm_g': 46.4, 'comm_i': 42.4}
NAT_SUB = {'place_g': 47.6, 'place_i': 50.3, 'econ_g': 50.8, 'econ_i': 50.1, 'comm_g': 50.4, 'comm_i': 50.0}

STATE_RANK = '1,116 / 1,376'
STATE_PCTILE = '81st'
NAT_RANK = '76,054 / 85,032'
NAT_PCTILE = '89th'
POINTS_BELOW_LA = 8.4
POINTS_BELOW_NAT = 13.5

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 1: Overall IGS Score Comparison (horizontal bars + stat boxes)
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("CHART 1: IGS SCORE COMPARISON BARS")
print("=" * 60)

labels = ['National Average', 'Louisiana Average', 'St. Helena Parish']
values = [NAT['igs'], LA['igs'], SH['igs']]
colors = [SLATE, AMBER, CORAL]

fig = go.Figure()

for i, (label, val, color) in enumerate(zip(labels, values, colors)):
    fig.add_trace(go.Bar(
        y=[label], x=[val], orientation='h',
        marker=dict(color=color, cornerradius=4),
        text=[f'<b>{val:.1f}</b>'],
        textposition='outside',
        textfont=dict(size=14, color=color, family='Arial'),
        width=0.55,
        showlegend=False,
    ))

annotations = [source_annotation(SRC, y=-0.18)]

fig.update_layout(
    **base_layout('IGS Ranking: St. Helena Parish vs State & National',
                  width=750, height=380, b_margin=120, l_margin=170, r_margin=80),
    xaxis=dict(
        range=[0, 60],
        tickfont=dict(size=11, color=NAVY),
        gridcolor='rgba(0,0,0,0.04)',
        title=dict(text='IGS Score (Percentile)', font=dict(size=12, color=NAVY)),
    ),
    yaxis=dict(
        tickfont=dict(size=13, color=NAVY, family='Arial'),
        categoryorder='array',
        categoryarray=labels,
    ),
    annotations=annotations,
    shapes=[
        # IGS 45 threshold line
        dict(type='line', xref='x', yref='paper',
             x0=45, x1=45, y0=0, y1=0.95,
             line=dict(color=MUTED, width=1.5, dash='dot')),
    ],
)

# IGS 45 label
fig.add_annotation(
    text='<b>IGS 45</b>', xref='x', yref='paper',
    x=45, y=0.98, showarrow=False,
    font=dict(size=9, color=MUTED),
)

fig.write_image(os.path.join(OUT, 'igs_ranking_bars.png'), scale=3)
print("  -> igs_ranking_bars.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 2: IGS Component Comparison Table
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("CHART 2: IGS COMPONENT COMPARISON TABLE")
print("=" * 60)

# Build table data — focus on key gap metrics the Hub addresses
# Metrics sorted by severity of gap (worst first)
components = [
    'Labor Market Engagement',
    'Travel Time to Work',
    'Internet Access',
    'Female Above Poverty',
    'Personal Income',
    'Gini Coefficient',
    'Minority/Women Businesses',
    'Commercial Diversity',
    'Spending per Capita',
    'Health Insurance',
    'New Businesses',
]

parish_vals = [1, 1, 3, 12, 15, 18, 22, 34, 34, 39, 43]
state_vals  = [38.3, 50.4, 35.3, 36.5, 45.0, 37.4, 48.1, 51.5, 45.5, 47.5, 48.5]
nat_vals    = [50.7, 49.1, 50.7, 50.5, 50.4, 50.7, 46.5, 53.6, 48.2, 49.4, 51.1]

def score_color(val):
    """Red if poor (<35), amber if below avg (35-45), green if good (>45)."""
    if val < 35:
        return CORAL
    elif val < 45:
        return AMBER
    else:
        return TEAL

parish_colors = [score_color(v) for v in parish_vals]
state_colors = [score_color(v) for v in state_vals]
nat_colors = [score_color(v) for v in nat_vals]

# Format values
def fmt(v, bold=False):
    s = f'{v:.1f}'
    return f'<b>{s}</b>' if bold else s

parish_strs = [fmt(v, bold=True) for v in parish_vals]
state_strs = [fmt(v) for v in state_vals]
nat_strs = [fmt(v) for v in nat_vals]

fig2 = go.Figure(data=[go.Table(
    columnwidth=[160, 80, 80, 80],
    header=dict(
        values=['<b>Component</b>', '<b>Parish</b>', '<b>State</b>', '<b>National</b>'],
        fill_color='white',
        font=dict(color=NAVY, size=13, family='Arial'),
        align=['left', 'center', 'center', 'center'],
        height=38,
        line_color='rgba(0,0,0,0.08)',
    ),
    cells=dict(
        values=[
            [f'<b>{c}</b>' for c in components],
            parish_strs,
            state_strs,
            nat_strs,
        ],
        fill_color='white',
        font=dict(
            color=[
                [NAVY]*len(components),
                parish_colors,
                state_colors,
                nat_colors,
            ],
            size=13,
            family='Arial',
        ),
        align=['left', 'center', 'center', 'center'],
        height=36,
        line_color='rgba(0,0,0,0.06)',
    ),
)])

fig2.update_layout(
    width=560, height=610,
    margin=dict(l=10, r=10, t=80, b=60),
    title=dict(
        text='Key Gap Metrics: St. Helena Parish vs Benchmarks',
        font=dict(size=16, color=NAVY, family='Arial'),
        x=0.5, xanchor='center',
    ),
    paper_bgcolor='white',
    font=dict(family='Arial'),
    annotations=[source_annotation(SRC, y=-0.06)],
)

fig2.write_image(os.path.join(OUT, 'igs_ranking_table.png'), scale=3)
print("  -> igs_ranking_table.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3: Key Stat Boxes
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("CHART 3: KEY STAT BOXES")
print("=" * 60)

fig3 = go.Figure()

# Invisible scatter to set axes
fig3.add_trace(go.Scatter(x=[0,3], y=[0,1], mode='none', showlegend=False))

stats = [
    ('58th', '64 Parishes<br>State Ranking'),
    ('18th', 'National<br>Percentile'),
    ('-8.4 pts', 'Below Avg<br>Rural LA Average'),
]

for i, (big_num, label) in enumerate(stats):
    cx = 0.5 + i * 1.5  # x-axis coords with wider spacing

    # Card background
    fig3.add_shape(
        type='rect',
        x0=cx - 0.6, x1=cx + 0.6, y0=0.1, y1=0.9,
        fillcolor='white',
        line=dict(color='rgba(0,0,0,0.1)', width=1),
        xref='x', yref='y',
        layer='below',
    )

    # Big number
    fig3.add_annotation(
        x=cx, y=0.62,
        text=f'<b>{big_num}</b>',
        showarrow=False,
        font=dict(size=22, color=CORAL, family='Arial'),
        xref='x', yref='y',
    )

    # Label text
    fig3.add_annotation(
        x=cx, y=0.32,
        text=label,
        showarrow=False,
        font=dict(size=9, color=MUTED, family='Arial'),
        xref='x', yref='y',
        align='center',
    )

fig3.update_layout(
    width=480, height=140,
    margin=dict(l=5, r=5, t=5, b=5),
    xaxis=dict(visible=False, range=[-0.3, 4.3]),
    yaxis=dict(visible=False, range=[0, 1]),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial'),
)

fig3.write_image(os.path.join(OUT, 'igs_stat_boxes.png'), scale=3)
print("  -> igs_stat_boxes.png")

print("\n" + "=" * 60)
print("IGS RANKING CHARTS COMPLETE — 3 charts saved to outputs/po/")
print("=" * 60)
