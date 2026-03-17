"""
H2: Federal Designations & Provider Counts
Data: 2025 County Health Rankings (CHR)
URL: https://www.countyhealthrankings.org
Charts: C11 (Provider counts) + C12 (Preventable hosp) + C13 (Life expectancy)
"""

import plotly.graph_objects as go
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'h2')
os.makedirs(OUT, exist_ok=True)

SRC = 'Source: County Health Rankings, 2025  •  https://www.countyhealthrankings.org'


def three_level_hbar(title, labels, values, colors, x_title, outfile, x_range=None, fmt=',.0f'):
    """Build a polished 3-level horizontal bar chart."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=values, orientation='h',
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        text=[f'<b>{v:{fmt}}</b>' for v in values],
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(size=15, color='white', family='Arial'),
        width=0.5,
    ))
    layout = base_layout(title, b_margin=140)
    layout['margin'] = dict(l=170, r=130, t=110, b=140)
    fig.update_layout(
        **layout,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=12, color=NAVY)),
            tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
            **(dict(range=x_range) if x_range else {}),
        ),
        yaxis=dict(
            tickfont=dict(size=14, color=NAVY, family='Arial'),
            categoryorder='array', categoryarray=labels,
        ),
        showlegend=False, bargap=0.35,
        annotations=[source_annotation(SRC, y=-0.3)],
    )
    fig.write_image(os.path.join(OUT, outfile), scale=3)


# ═══════════════════════════════════════════════════════════════════════════════
# H2.1 — C11: Provider Counts
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("H2.1: PROVIDER COUNTS")
print("=" * 60)

providers = ['Primary Care', 'Mental Health', 'Dentists']
sh_counts = [2, 9, 1]
sh_ratios = ['5,456:1', '1,197:1', '10,822:1']

for p, c, r in zip(providers, sh_counts, sh_ratios):
    print(f"  {p}: {c} providers ({r} ratio)")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=providers, y=sh_counts,
    marker=dict(color=[CORAL, AMBER, CORAL], line=dict(width=0), cornerradius=5),
    text=[f'<b>{c}</b>' for c in sh_counts],
    textposition='outside',
    textfont=dict(size=22, color=NAVY, family='Arial Black'),
    width=0.4,
))

fig.update_layout(
    **base_layout('2 Doctors, 1 Dentist for 10,000+ Residents', width=820, height=500, b_margin=140),
    yaxis=dict(
        title=dict(text='Number of Providers', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)', range=[0, 14],
    ),
    xaxis=dict(tickfont=dict(size=13, color=NAVY)),
    showlegend=False,
    annotations=[
        dict(text='<b>5,456:1</b>', x='Primary Care', y=-1.2, xref='x', yref='y',
             showarrow=False, font=dict(size=11, color=CORAL)),
        dict(text='<b>1,197:1</b>', x='Mental Health', y=-1.2, xref='x', yref='y',
             showarrow=False, font=dict(size=11, color=AMBER)),
        dict(text='<b>10,822:1</b>', x='Dentists', y=-1.2, xref='x', yref='y',
             showarrow=False, font=dict(size=11, color=CORAL)),
        source_annotation(SRC, y=-0.3),
    ],
)
fig.write_image(os.path.join(OUT, 'h2_provider_counts.png'), scale=3)
print("  → h2_provider_counts.png")

# ═══════════════════════════════════════════════════════════════════════════════
# H2.2 — C12: Preventable Hospitalizations
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("H2.2: PREVENTABLE HOSPITALIZATIONS")
print("=" * 60)

labels = ['United States', 'Louisiana', 'St. Helena Parish']
values = [2810, 3427, 4862]
print(f"  US: {values[0]:,}  |  LA: {values[1]:,}  |  St.H: {values[2]:,}")

three_level_hbar(
    'Preventable Hospitalizations 1.7× the National Rate',
    labels, values, PALETTE_3,
    'Rate per 100,000 Medicare Enrollees',
    'h2_preventable_hosp.png',
)
print("  → h2_preventable_hosp.png")

# ═══════════════════════════════════════════════════════════════════════════════
# H2.3 — C13: Life Expectancy
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("H2.3: LIFE EXPECTANCY")
print("=" * 60)

le_labels = ['St. Helena Parish', 'Louisiana', 'United States']
le_values = [70.0, 73.3, 78.4]
print(f"  St.H: {le_values[0]}  |  LA: {le_values[1]}  |  US: {le_values[2]}")

three_level_hbar(
    'Residents Die 8 Years Younger Than the National Average',
    le_labels, le_values, PALETTE_3R,
    'Life Expectancy (Years)',
    'h2_life_expectancy.png',
    x_range=[60, 84],
    fmt='.1f',
)
print("  → h2_life_expectancy.png")

print("\n" + "=" * 60)
print("H2 COMPLETE — 3 charts saved to outputs/h2/")
print("=" * 60)
