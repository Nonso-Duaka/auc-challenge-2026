"""
S1: Industry Gaps — Missing NAICS Sectors
Data: cbp_st_helena_parish.csv (County Business Patterns)
URL: https://data.census.gov
Charts: C7 (Sector presence) + C8 (Healthcare gaps)
"""

import plotly.graph_objects as go
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 's1')
os.makedirs(OUT, exist_ok=True)

SRC = 'Source: U.S. Census Bureau, County Business Patterns 2022  •  https://data.census.gov'

# ═══════════════════════════════════════════════════════════════════════════════
# S1.1 — C7: Sector Presence
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("S1.1: SECTOR PRESENCE")
print("=" * 60)

sectors = [
    ('Agriculture', 0), ('Mining', 1), ('Utilities', 0), ('Construction', 1),
    ('Manufacturing', 0), ('Wholesale', 0), ('Retail', 1), ('Transportation', 1),
    ('Information', 0), ('Finance/Ins', 1), ('Real Estate', 0), ('Professional', 1),
    ('Management', 0), ('Admin/Waste', 0), ('Education', 1), ('Healthcare', 1),
    ('Arts/Entertain', 0), ('Accomm/Food', 1), ('Other Services', 1),
]

present = sum(v for _, v in sectors)
missing = len(sectors) - present
print(f"  Present: {present}  |  Missing: {missing}")

labels = [s[0] for s in sectors]
vals = [s[1] for s in sectors]
colors = [TEAL if v else CORAL for v in vals]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=labels, y=[1]*len(labels),
    marker=dict(color=colors, line=dict(width=1.5, color='white'), cornerradius=3),
    text=['✓' if v else '✗' for v in vals],
    textposition='inside',
    textfont=dict(size=14, color='white', family='Arial'),
))

fig.update_layout(
    **base_layout(f'Half the Economy Doesn\'t Exist: {missing} of 19 Sectors Missing',
                  width=1100, height=400, b_margin=150),
    xaxis=dict(tickfont=dict(size=9, color=NAVY), tickangle=-50),
    yaxis=dict(visible=False, range=[0, 1.2]),
    showlegend=False, bargap=0.08,
    annotations=[source_annotation(SRC, y=-0.42)],
)

fig.write_image(os.path.join(OUT, 's1_sector_heatmap.png'), scale=3)
print("  → s1_sector_heatmap.png")

# ═══════════════════════════════════════════════════════════════════════════════
# S1.2 — C8: Healthcare Gaps
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("S1.2: HEALTHCARE GAPS")
print("=" * 60)

hc_missing = [
    'Offices of Dentists', 'Other Health Practitioners', 'Medical/Diagnostic Labs',
    'Home Health Care', 'Other Ambulatory Care', 'Hospitals',
    'Nursing/Residential Care', 'Individual/Family Services',
    'Community Food/Housing', 'Vocational Rehab', 'Pharmacies/Drug Stores',
    'Transit/Passenger Transport',
]
hc_present = [
    ('Physician Offices', 3), ('Outpatient Care Centers', 5),
    ('Child Day Care', 6), ('Social Assistance', 2),
]

all_hc = [(n, 0) for n in hc_missing] + [(n, e) for n, e in hc_present]
all_hc.sort(key=lambda x: x[1])

hc_labels = [x[0] for x in all_hc]
hc_vals = [x[1] for x in all_hc]
hc_colors = [CORAL if v == 0 else TEAL for v in hc_vals]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    y=hc_labels,
    x=[max(v, 0.3) for v in hc_vals],
    orientation='h',
    marker=dict(color=hc_colors, line=dict(width=0), cornerradius=3),
    text=[f'<b>{v}</b>' if v > 0 else '<b>NONE</b>' for v in hc_vals],
    textposition='outside',
    textfont=dict(size=11, color=NAVY, family='Arial'),
    width=0.55,
))

fig2.update_layout(
    **base_layout('12 Healthcare Categories Have Zero Establishments',
                  width=950, height=640, b_margin=120, l_margin=230, r_margin=80),
    xaxis=dict(
        title=dict(text='Establishments', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
    ),
    yaxis=dict(
        tickfont=dict(size=11, color=NAVY, family='Arial'),
        categoryorder='array', categoryarray=hc_labels,
    ),
    showlegend=False, bargap=0.18,
    annotations=[source_annotation(SRC, y=-0.18)],
)

fig2.write_image(os.path.join(OUT, 's1_healthcare_gaps.png'), scale=3)
print("  → s1_healthcare_gaps.png")

print("\n" + "=" * 60)
print("S1 COMPLETE — 2 charts saved to outputs/s1/")
print("=" * 60)
