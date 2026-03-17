"""
E2: Employment & Economic Exodus
Data: census_tract_951100_data.csv (E2.1, E2.2)
      OTM data hardcoded from otm_inandout.pdf (E2.3)
URL: https://data.census.gov  |  https://onthemap.ces.census.gov
"""

import pandas as pd
import plotly.graph_objects as go
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

SRC_CENSUS = 'Source: U.S. Census Bureau, ACS 5-Year (2019–2023)  •  https://data.census.gov'
SRC_OTM = 'Source: U.S. Census Bureau, OnTheMap  •  https://onthemap.ces.census.gov'

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'e2')
os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(os.path.join(BASE, 'data', 'economy', 'census_tract_951100_data.csv'))

# ═══════════════════════════════════════════════════════════════════════════════
# E2.1 — DONUT CHART: Labor Force Breakdown
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("E2.1: LABOR FORCE — DONUT")
print("=" * 60)

emp = df[df['Category'] == 'Employment']
pop_16plus = int(emp[emp['Measure'] == 'Population 16 years and over']['Value'].values[0])
employed = int(emp[emp['Measure'] == 'Employed']['Value'].values[0])
unemployed = int(emp[emp['Measure'] == 'Unemployed']['Value'].values[0])
not_in_lf = int(emp[emp['Measure'] == 'Not in labor force']['Value'].values[0])

print(f"  Pop 16+: {pop_16plus:,}")
print(f"  Employed: {employed:,}  |  Unemployed: {unemployed:,}  |  Not in LF: {not_in_lf:,}")

fig = go.Figure()

labels = ['Employed', 'Unemployed', 'Not in Labor Force']
values = [employed, unemployed, not_in_lf]
colors = [TEAL, CORAL, '#B0BEC5']

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.58,
    marker=dict(colors=colors, line=dict(color='white', width=3.5)),
    textinfo='label+percent',
    textposition='outside',
    textfont=dict(size=12, color=NAVY, family='Arial'),
    pull=[0, 0.06, 0],
    sort=False,
    direction='clockwise',
    rotation=90,
))

fig.update_layout(
    **base_layout('62% of Working-Age Adults Are Not Employed', width=720, height=580, b_margin=100),
    showlegend=False,
    annotations=[
        dict(
            text=f'<b style="font-size:30px;color:{NAVY}">{pop_16plus:,}</b>'
                 f'<br><span style="font-size:12px;color:{MUTED}">Working-Age<br>Population</span>',
            x=0.5, y=0.5, xref='paper', yref='paper',
            showarrow=False, font=dict(size=14),
        ),
        source_annotation(SRC_CENSUS + '  •  Table B23025', y=-0.08),
    ],
)

fig.write_image(os.path.join(OUT, 'e2_labor_force.png'), scale=3)
print("  → e2_labor_force.png")

# ═══════════════════════════════════════════════════════════════════════════════
# E2.2 — BAR CHART: Commute Time Distribution
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("E2.2: COMMUTE TIME — BAR CHART")
print("=" * 60)

time_labels = ['5–9', '10–14', '15–19', '20–24', '25–29', '30–34',
               '35–39', '40–44', '45–59', '60–89', '90+']
time_values = [14, 85, 67, 116, 17, 112, 62, 96, 138, 339, 98]
total_commuters = sum(time_values)
long_commute = sum(time_values[8:])
pct_long = round(long_commute / total_commuters * 100, 1)

print(f"  Total commuters: {total_commuters}")
print(f"  45+ min: {long_commute} ({pct_long}%)")

# Smooth gradient from teal → amber → coral
import numpy as np
n = len(time_values)
gradient = []
for i in range(n):
    t = i / (n - 1)
    if t < 0.5:
        # teal to amber
        r = int(42 + (244-42) * t*2)
        g = int(157 + (162-157) * t*2)
        b = int(143 + (97-143) * t*2)
    else:
        # amber to coral
        t2 = (t - 0.5) * 2
        r = int(244 + (230-244) * t2)
        g = int(162 + (57-162) * t2)
        b = int(97 + (70-97) * t2)
    gradient.append(f'rgb({r},{g},{b})')

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=[f'{l}' for l in time_labels],
    y=time_values,
    marker=dict(
        color=gradient,
        line=dict(width=0.5, color='white'),
        cornerradius=3,
    ),
    text=[str(v) for v in time_values],
    textposition='outside',
    textfont=dict(size=9, color=NAVY),
))

xax, yax = hbar_axes()
fig2.update_layout(
    **base_layout(f'{pct_long}% of Workers Commute 45+ Minutes Each Way', width=1000, height=500, b_margin=140),
    xaxis=dict(
        title=dict(text='Commute Time (minutes)', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=10, color=NAVY),
        tickangle=-30,
    ),
    yaxis=dict(
        title=dict(text='Number of Workers', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11),
        gridcolor='rgba(0,0,0,0.04)',
    ),
    showlegend=False,
    bargap=0.12,
    annotations=[
        dict(
            text=f'<b>Peak: 339</b> workers<br>commute 60–89 min',
            x='60–89', y=339, xref='x', yref='y',
            showarrow=True, arrowhead=2, arrowcolor=CORAL,
            ax=-70, ay=-45,
            font=dict(size=11, color=CORAL, family='Arial'),
            bgcolor='rgba(255,255,255,0.85)', borderpad=4,
        ),
        source_annotation(SRC_CENSUS + '  •  Table B08303', y=-0.3),
    ],
)

fig2.write_image(os.path.join(OUT, 'e2_commute_times.png'), scale=3)
print("  → e2_commute_times.png")

# ═══════════════════════════════════════════════════════════════════════════════
# E2.3 — HORIZONTAL BAR: Worker Exodus (OnTheMap)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("E2.3: WORKER EXODUS")
print("=" * 60)

living_in = 3185
work_leave = 2880
work_local = 305
commute_in = 924

print(f"  Leave: {work_leave:,} ({work_leave/living_in*100:.1f}%)")
print(f"  Commute in: {commute_in:,}")
print(f"  Local: {work_local:,}")

categories = ['Live & Work Locally', 'Commute Into Parish', 'Leave Parish for Work']
vals = [work_local, commute_in, work_leave]
bar_colors = [TEAL, SLATE, CORAL]

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    y=categories,
    x=vals,
    orientation='h',
    marker=dict(color=bar_colors, line=dict(width=0), cornerradius=4),
    text=[f'<b>{v:,}</b>' for v in vals],
    textposition='outside',
    textfont=dict(size=14, color=NAVY, family='Arial'),
    width=0.5,
))

fig3.update_layout(
    **base_layout('9 in 10 Workers Leave the Parish for Jobs', b_margin=140, l_margin=190, r_margin=100),
    xaxis=dict(
        title=dict(text='Number of Workers', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11),
        gridcolor='rgba(0,0,0,0.04)',
    ),
    yaxis=dict(
        tickfont=dict(size=13, color=NAVY, family='Arial'),
        categoryorder='array', categoryarray=categories,
    ),
    showlegend=False,
    bargap=0.35,
    annotations=[
        source_annotation(SRC_OTM, y=-0.3),
    ],
)

fig3.write_image(os.path.join(OUT, 'e2_worker_exodus.png'), scale=3)
print("  → e2_worker_exodus.png")

print("\n" + "=" * 60)
print("E2 COMPLETE — 3 charts saved to outputs/e2/")
print("=" * 60)
