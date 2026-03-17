"""
PO: Predicted Outcomes — Model-Based IGS Projections
Data: XGBoost model trained on 1.4M real IGS observations (R²=0.9883)
Charts: C14 (Radar), C15 (Scenario bars), C16 (Waterfall), C17 (Feature importance), C18 (Trajectory)
"""

import plotly.graph_objects as go
import json
import warnings
import os
import sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'po')
os.makedirs(OUT, exist_ok=True)

SRC = 'Source: XGBoost model trained on 1.4M IGS observations (R²=0.99)  •  inclusivegrowthscore.com'

# ─── Load simulation results ─────────────────────────────────────────────────
with open(os.path.join(BASE, 'model', 'results', 'simulation_details.json')) as f:
    sim = json.load(f)

baseline = sim['baseline']
scenarios = sim['scenarios']

pillar_keys = ['igs', 'place', 'economy', 'community']
current = [baseline[k] for k in pillar_keys]
yr1 = [scenarios[0][k] for k in pillar_keys]
yr3 = [scenarios[1][k] for k in pillar_keys]
yr5 = [scenarios[2][k] for k in pillar_keys]

# ═══════════════════════════════════════════════════════════════════════════════
# PO.1 — C14: Before/After Radar Chart
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("PO.1: BEFORE/AFTER RADAR CHART")
print("=" * 60)

pillars = ['IGS', 'Place', 'Economy', 'Community']
pillars_r = pillars + [pillars[0]]
current_r = current + [current[0]]
yr3_r = yr3 + [yr3[0]]
yr5_r = yr5 + [yr5[0]]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=current_r, theta=pillars_r, name='Current (2025)',
    fill='toself', fillcolor='rgba(230,57,70,0.15)',
    line=dict(color=CORAL, width=3),
    marker=dict(size=8, color=CORAL),
))
fig.add_trace(go.Scatterpolar(
    r=yr3_r, theta=pillars_r, name='Year 3 Projection',
    fill='toself', fillcolor='rgba(244,162,97,0.12)',
    line=dict(color=AMBER, width=2.5, dash='dash'),
    marker=dict(size=7, color=AMBER),
))
fig.add_trace(go.Scatterpolar(
    r=yr5_r, theta=pillars_r, name='Year 5 Projection',
    fill='toself', fillcolor='rgba(42,157,143,0.12)',
    line=dict(color=TEAL, width=2.5, dash='dash'),
    marker=dict(size=7, color=TEAL),
))

fig.update_layout(
    **base_layout('Community Hub Could Push IGS Above 45 in 5 Years',
                  width=700, height=600, b_margin=140),
    polar=dict(
        radialaxis=dict(
            visible=True, range=[0, 55],
            tickfont=dict(size=10, color=MUTED),
            gridcolor='rgba(0,0,0,0.06)',
        ),
        angularaxis=dict(
            tickfont=dict(size=14, color=NAVY, family='Arial'),
        ),
        bgcolor=LIGHT_BG,
    ),
    legend=dict(
        orientation='h', yanchor='bottom', y=-0.22, xanchor='center', x=0.5,
        font=dict(size=12, color=NAVY), bgcolor='rgba(0,0,0,0)',
    ),
    annotations=[source_annotation(SRC, y=-0.32)],
)

fig.write_image(os.path.join(OUT, 'po_radar.png'), scale=3)
print("  → po_radar.png")

# ═══════════════════════════════════════════════════════════════════════════════
# PO.2 — C15: Scenario Comparison Grouped Bar
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PO.2: SCENARIO COMPARISON")
print("=" * 60)

categories = ['IGS Score', 'Place', 'Economy', 'Community']

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=categories, y=current, name='Current (2025)',
    marker=dict(color=CORAL, cornerradius=4),
    text=[f'<b>{v:.1f}</b>' for v in current],
    textposition='outside', textfont=dict(size=12, color=CORAL),
))
fig2.add_trace(go.Bar(
    x=categories, y=yr1, name='Year 1',
    marker=dict(color=AMBER, cornerradius=4),
    text=[f'<b>{v:.1f}</b>' for v in yr1],
    textposition='outside', textfont=dict(size=12, color=AMBER),
))
fig2.add_trace(go.Bar(
    x=categories, y=yr3, name='Year 3',
    marker=dict(color=SLATE, cornerradius=4),
    text=[f'<b>{v:.1f}</b>' for v in yr3],
    textposition='outside', textfont=dict(size=12, color=SLATE),
))
fig2.add_trace(go.Bar(
    x=categories, y=yr5, name='Year 5',
    marker=dict(color=TEAL, cornerradius=4),
    text=[f'<b>{v:.1f}</b>' for v in yr5],
    textposition='outside', textfont=dict(size=12, color=TEAL),
))

fig2.update_layout(
    **base_layout('Projected IGS Growth: From 36 to 47 in Five Years',
                  width=950, height=520, b_margin=140),
    barmode='group',
    xaxis=dict(tickfont=dict(size=14, color=NAVY)),
    yaxis=dict(
        title=dict(text='Score (Percentile)', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
        range=[0, 58],
    ),
    legend=grouped_legend(),
    bargap=0.25,
    annotations=[
        dict(text='<b>IGS 45 Threshold</b>', xref='paper', yref='y',
             x=1.01, y=45, showarrow=False,
             font=dict(size=10, color=MUTED)),
        source_annotation(SRC, y=-0.28),
    ],
    shapes=[
        dict(type='line', xref='paper', yref='y',
             x0=0, x1=1, y0=45, y1=45,
             line=dict(color=MUTED, width=1.5, dash='dot')),
    ],
)

fig2.write_image(os.path.join(OUT, 'po_scenario_bars.png'), scale=3)
print("  → po_scenario_bars.png")

# ═══════════════════════════════════════════════════════════════════════════════
# PO.3 — C16: Waterfall — What Drives the +10 Point Gain
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PO.3: WATERFALL — METRIC CONTRIBUTIONS")
print("=" * 60)

importance_order = [
    ('Labor Market\nEngagement', 0.2743),
    ('Internet\nAccess', 0.0985),
    ('Female Above\nPoverty', 0.0935),
    ('Commercial\nDiversity', 0.0841),
    ('Real Estate\nValue', 0.0644),
    ('Health\nInsurance', 0.0484),
    ('Spending\nper Capita', 0.0398),
    ('Small Business\nLoans', 0.0385),
    ('Other\nMetrics', 0.2585),
]

total_gain = scenarios[2]['igs_change']
labels = [x[0] for x in importance_order]
raw_imp = [x[1] for x in importance_order]
total_imp = sum(raw_imp)
contributions = [round(imp / total_imp * total_gain, 1) for imp in raw_imp]

fig3 = go.Figure()

cumulative = baseline['igs']
colors = []
x_vals = ['Current\nIGS'] + labels + ['Projected\nIGS']
y_vals = [baseline['igs']]
bases = [0]

for c in contributions:
    bases.append(cumulative)
    y_vals.append(c)
    cumulative += c
    colors.append(TEAL if c > 0.5 else SLATE)

bases.append(0)
y_vals.append(cumulative)

fig3.add_trace(go.Bar(
    x=x_vals, y=y_vals, base=bases,
    marker=dict(
        color=[CORAL] + colors + [TEAL],
        cornerradius=3, line=dict(width=0),
    ),
    text=[f'<b>{v:.1f}</b>' for v in y_vals],
    textposition='outside',
    textfont=dict(size=11, color=NAVY),
    width=0.55,
))

for i in range(len(x_vals) - 1):
    top = bases[i] + y_vals[i]
    fig3.add_shape(
        type='line', x0=i - 0.25, x1=i + 0.75, y0=top, y1=top,
        xref='x', yref='y',
        line=dict(color=MUTED, width=1, dash='dot'),
    )

fig3.update_layout(
    **base_layout('How the Hub Drives a +10 Point IGS Improvement',
                  width=1100, height=520, b_margin=150),
    xaxis=dict(tickfont=dict(size=10, color=NAVY)),
    yaxis=dict(
        title=dict(text='IGS Score', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
        range=[0, 55],
    ),
    showlegend=False,
    annotations=[source_annotation(SRC, y=-0.32)],
)

fig3.write_image(os.path.join(OUT, 'po_waterfall.png'), scale=3)
print("  → po_waterfall.png")

# ═══════════════════════════════════════════════════════════════════════════════
# PO.4 — C17: Feature Importance — What Matters Most for IGS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PO.4: FEATURE IMPORTANCE")
print("=" * 60)

feat_labels = [
    'Labor Market Engagement', 'Internet Access', 'Female Above Poverty',
    'Commercial Diversity', 'Real Estate Value', 'Health Insurance',
    'Spending per Capita', 'Small Business Loans', 'Net Occupancy',
    'Personal Income', 'New Businesses', 'Early Education',
    'Affordable Housing', 'Park Land', 'Minority/Women Businesses',
    'Spend Growth', 'Travel Time', 'Gini Coefficient',
]
feat_imp = [
    0.2743, 0.0985, 0.0935, 0.0841, 0.0644, 0.0484,
    0.0398, 0.0385, 0.0351, 0.0339, 0.0311, 0.0295,
    0.0291, 0.0238, 0.0220, 0.0207, 0.0173, 0.0157,
]

hub_affected = {
    'Labor Market Engagement', 'Internet Access', 'Commercial Diversity',
    'Health Insurance', 'Spending per Capita', 'Small Business Loans',
    'Personal Income', 'New Businesses', 'Early Education',
    'Minority/Women Businesses', 'Travel Time', 'Female Above Poverty',
}

feat_colors = [TEAL if f in hub_affected else MUTED for f in feat_labels]

feat_labels_r = feat_labels[::-1]
feat_imp_r = feat_imp[::-1]
feat_colors_r = feat_colors[::-1]

fig4 = go.Figure()
fig4.add_trace(go.Bar(
    y=feat_labels_r, x=feat_imp_r, orientation='h',
    marker=dict(color=feat_colors_r, cornerradius=3, line=dict(width=0)),
    text=[f'{v:.1%}' for v in feat_imp_r],
    textposition='outside',
    textfont=dict(size=10, color=NAVY),
    width=0.6,
))

fig4.update_layout(
    **base_layout('The Hub Targets 12 of 18 IGS Drivers',
                  width=900, height=620, b_margin=140, l_margin=210, r_margin=80),
    xaxis=dict(
        title=dict(text='Feature Importance', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), tickformat='.0%',
        gridcolor='rgba(0,0,0,0.04)',
    ),
    yaxis=dict(
        tickfont=dict(size=11, color=NAVY, family='Arial'),
        categoryorder='array', categoryarray=feat_labels_r,
    ),
    showlegend=False, bargap=0.2,
    annotations=[
        dict(text='<b>■ Hub-targeted metric</b>', xref='paper', yref='paper',
             x=0.95, y=0.05, showarrow=False,
             font=dict(size=11, color=TEAL)),
        dict(text='<b>■ Not directly affected</b>', xref='paper', yref='paper',
             x=0.95, y=0.01, showarrow=False,
             font=dict(size=11, color=MUTED)),
        source_annotation(SRC, y=-0.22),
    ],
)

fig4.write_image(os.path.join(OUT, 'po_feature_importance.png'), scale=3)
print("  → po_feature_importance.png")

# ═══════════════════════════════════════════════════════════════════════════════
# PO.5 — C18: IGS Trajectory Over Time
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PO.5: IGS TRAJECTORY")
print("=" * 60)

years = [2025, 2026, 2028, 2030]
igs_trajectory = [baseline['igs'], scenarios[0]['igs'], scenarios[1]['igs'], scenarios[2]['igs']]

fig5 = go.Figure()

fig5.add_trace(go.Scatter(
    x=years, y=igs_trajectory,
    mode='lines+markers+text',
    line=dict(color=TEAL, width=3),
    marker=dict(size=12, color=TEAL, line=dict(width=2, color='white')),
    text=[f'<b>{v:.1f}</b>' for v in igs_trajectory],
    textposition='top center',
    textfont=dict(size=14, color=NAVY),
    name='Projected IGS',
))

fig5.add_shape(
    type='line', xref='paper', yref='y',
    x0=0, x1=1, y0=45, y1=45,
    line=dict(color=CORAL, width=2, dash='dash'),
)
fig5.add_annotation(
    text='<b>IGS 45 Threshold</b>', xref='paper', yref='y',
    x=0.02, y=45.8, showarrow=False,
    font=dict(size=11, color=CORAL),
)

fig5.update_layout(
    **base_layout('Crossing the 45 Threshold: A 5-Year Path',
                  width=800, height=480, b_margin=140),
    xaxis=dict(
        tickfont=dict(size=12, color=NAVY),
        tickvals=years, ticktext=['2025\nCurrent', '2026\nYear 1', '2028\nYear 3', '2030\nYear 5'],
        gridcolor='rgba(0,0,0,0.04)',
    ),
    yaxis=dict(
        title=dict(text='IGS Score', font=dict(size=12, color=NAVY)),
        tickfont=dict(size=11), gridcolor='rgba(0,0,0,0.04)',
        range=[30, 52],
    ),
    showlegend=False,
    annotations=[source_annotation(SRC, y=-0.3)],
)

fig5.write_image(os.path.join(OUT, 'po_trajectory.png'), scale=3)
print("  → po_trajectory.png")

print("\n" + "=" * 60)
print("PO COMPLETE — 5 charts saved to outputs/po/")
print("=" * 60)
