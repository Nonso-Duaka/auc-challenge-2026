"""
E3: Employer Insurance Gap & Industry Structure
Data: census_tract_951100_data.csv
URL: https://data.census.gov
Charts: C3 (Insurance by employment) + C5 (Industry by gender)
"""

import pandas as pd
import plotly.graph_objects as go
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'e3')
os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(os.path.join(BASE, 'data', 'economy', 'census_tract_951100_data.csv'))

SRC = 'Source: U.S. Census Bureau, ACS 5-Year (2019–2023)  •  https://data.census.gov'

# ═══════════════════════════════════════════════════════════════════════════════
# E3.1 — Insurance by Employment Status
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("E3.1: INSURANCE BY EMPLOYMENT STATUS")
print("=" * 60)

employed = 483
employer_based = 38
employer_pct = round(employer_based / employed * 100, 1)
us_employer_pct = 55.0
la_employer_pct = 27.6

print(f"  St. Helena: {employer_pct}%  |  LA: {la_employer_pct}%  |  US: {us_employer_pct}%")

labels = ['United States', 'Louisiana', 'St. Helena Parish']
values = [us_employer_pct, la_employer_pct, employer_pct]
colors = PALETTE_3

fig = go.Figure()
fig.add_trace(go.Bar(
    y=labels, x=values, orientation='h',
    marker=dict(color=colors, line=dict(width=0), cornerradius=4),
    text=[f'<b>{v}%</b>' for v in values],
    textposition='outside',
    textfont=dict(size=15, color=NAVY, family='Arial'),
    width=0.5,
))

fig.update_layout(
    **base_layout('Only 7.9% of Workers Have Employer Insurance', b_margin=140, l_margin=170, r_margin=90),
    xaxis=dict(
        title=dict(text='Workers with Employer-Based Insurance (%)', font=dict(size=11, color=NAVY)),
        ticksuffix='%', tickfont=dict(size=11),
        gridcolor='rgba(0,0,0,0.04)', range=[0, 68],
    ),
    yaxis=dict(tickfont=dict(size=14, color=NAVY, family='Arial'), categoryorder='array', categoryarray=labels),
    showlegend=False, bargap=0.35,
    annotations=[source_annotation(SRC + '  •  Table C27012', y=-0.3)],
)

fig.write_image(os.path.join(OUT, 'e3_insurance_by_employment.png'), scale=3)
print("  → e3_insurance_by_employment.png")

# ═══════════════════════════════════════════════════════════════════════════════
# E3.2 — Industry by Gender
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("E3.2: INDUSTRY BY GENDER")
print("=" * 60)

industries = ['Ag/Mining', 'Construction', 'Manufacturing', 'Wholesale', 'Retail',
              'Transport/Utilities', 'Finance/Ins/RE', 'Professional/Mgmt',
              'Education/Health', 'Arts/Food', 'Other services', 'Public admin']
male_vals =   [43, 120, 70, 0, 18, 68, 12, 19, 19, 21, 87, 6]
female_vals = [0,  0,   13, 21, 187, 42, 21, 0,  0,  214, 39, 65]

# Sort by total, filter zeros
combined = [(i, m, f) for i, m, f in zip(industries, male_vals, female_vals) if m + f > 0]
combined.sort(key=lambda x: x[1] + x[2], reverse=True)
s_ind = [x[0] for x in combined]
s_m = [x[1] for x in combined]
s_f = [x[2] for x in combined]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    y=s_ind, x=s_m, orientation='h', name='Male',
    marker=dict(color=SLATE, cornerradius=3),
    text=[str(v) if v > 0 else '' for v in s_m],
    textposition='outside', textfont=dict(size=10, color=SLATE),
))
fig2.add_trace(go.Bar(
    y=s_ind, x=s_f, orientation='h', name='Female',
    marker=dict(color=CORAL, cornerradius=3),
    text=[str(v) if v > 0 else '' for v in s_f],
    textposition='outside', textfont=dict(size=10, color=CORAL),
))

fig2.update_layout(
    **base_layout('Gender-Split Economy: Women in Food & Retail, Men in Construction',
                  width=1020, height=580, b_margin=120, l_margin=170, r_margin=80),
    barmode='group',
    xaxis=dict(
        title=dict(text='Number of Workers', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
    ),
    yaxis=dict(
        tickfont=dict(size=11, color=NAVY, family='Arial'),
        categoryorder='array', categoryarray=s_ind[::-1],
    ),
    legend=grouped_legend(),
    bargap=0.22,
    annotations=[source_annotation(SRC + '  •  Table C24030', y=-0.2)],
)

fig2.write_image(os.path.join(OUT, 'e3_industry_by_gender.png'), scale=3)
print("  → e3_industry_by_gender.png")

print("\n" + "=" * 60)
print("E3 COMPLETE — 2 charts saved to outputs/e3/")
print("=" * 60)
