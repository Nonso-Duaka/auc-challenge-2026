"""
AG: Agriculture — The Food Paradox
Data: Census of Agriculture 2022 (cp22091.pdf) + CDC PLACES
URL: https://www.nass.usda.gov/AgCensus
Chart: C14 (Food paradox visual)
"""

import plotly.graph_objects as go
import plotly.subplots as sp
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'ag')
os.makedirs(OUT, exist_ok=True)

SRC = 'Sources: USDA Census of Agriculture 2022  •  CDC PLACES 2023  •  USDA Food Access Research Atlas'

# ═══════════════════════════════════════════════════════════════════════════════
# AG.1 — C14: Food Paradox — 3 panel comparison
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("AG.1: THE FOOD PARADOX")
print("=" * 60)

print("  349 farms  |  $54.2M in sales  |  96% livestock")
print("  33.4% food insecure  |  31.1% on food stamps  |  USDA food desert")

# Three-panel approach: Production vs Hunger vs Access
categories = ['Farm Sales<br>(Annual)', 'Food Insecure<br>(Residents)', 'On Food Stamps<br>(Residents)']
display_vals = [54.2, 33.4, 31.1]
bar_colors = [TEAL, CORAL, CORAL]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=display_vals,
    marker=dict(color=bar_colors, line=dict(width=0), cornerradius=5),
    text=['<b>$54.2M</b>', '<b>33.4%</b>', '<b>31.1%</b>'],
    textposition='outside',
    textfont=dict(size=18, color=NAVY, family='Arial'),
    width=0.45,
))

fig.update_layout(
    **base_layout('The Food Paradox: $54M in Farm Sales, 1 in 3 Go Hungry',
                  width=900, height=520, b_margin=150),
    yaxis=dict(visible=False),
    xaxis=dict(tickfont=dict(size=13, color=NAVY)),
    showlegend=False,
    annotations=[
        dict(
            text='349 farms  •  96% livestock/poultry  •  2.2M+ layer hens  •  USDA food desert',
            x=0.5, y=1.02, xref='paper', yref='paper',
            showarrow=False, font=dict(size=12, color=MUTED, family='Arial'),
            xanchor='center',
        ),
        source_annotation(SRC, y=-0.32),
    ],
)

fig.write_image(os.path.join(OUT, 'ag_food_paradox.png'), scale=3)
print("  → ag_food_paradox.png")

print("\n" + "=" * 60)
print("AG COMPLETE — 1 chart saved to outputs/ag/")
print("=" * 60)
