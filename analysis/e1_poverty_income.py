"""
E1: Poverty Depth and Income
Data: census_tract_951100_data.csv ONLY
URL: https://data.census.gov
Charts: Poverty by age/sex grouped bar + Income 3-level comparison
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os

warnings.filterwarnings('ignore', message='.*Kaleido.*')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'e1')
os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(os.path.join(BASE, 'data', 'economy', 'census_tract_951100_data.csv'))

SRC = 'Source: U.S. Census Bureau, ACS 5-Year (2019–2023)  •  https://data.census.gov'

# ═══════════════════════════════════════════════════════════════════════════════
# E1.1 — Poverty by Age & Sex: Grouped Bar
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("E1.1: POVERTY BY AGE & SEX")
print("=" * 60)

# B17001 verified: _003=Male total (652), _004-016=male age detail
#                   _017=Female total (636), _018-030=female age detail
age_labels = ['Under 5', '5–11', '12–14', '15–17', '18–24', '25–34',
              '35–44', '45–54', '55–64', '65–74', '75+']
male_c =   [56,  58,  47, 17, 247, 33, 78, 60, 18, 10, 28]
female_c = [ 0,  69,   0,  0,  63, 84, 61, 113, 60, 12, 174]

for ag, m, f in zip(age_labels, male_c, female_c):
    print(f"  {ag:>10s}: Male {m:4d}  |  Female {f:4d}")

# Population Pyramid (Butterfly Chart) — males left, females right
fig = go.Figure()

male_neg = [-v for v in male_c]  # negative values push bars left
male_text = [str(v) if v > 0 else '' for v in male_c]
female_text = [str(v) if v > 0 else '' for v in female_c]

fig.add_trace(go.Bar(
    name='Male',
    y=age_labels,
    x=male_neg,
    orientation='h',
    marker_color='#457B9D',
    text=male_text,
    textposition='outside',
    textfont=dict(size=12, color='#1D3557'),
))

fig.add_trace(go.Bar(
    name='Female',
    y=age_labels,
    x=female_c,
    orientation='h',
    marker_color='#E63946',
    text=female_text,
    textposition='outside',
    textfont=dict(size=12, color='#9D0208'),
))

fig.update_layout(
    template='plotly_white',
    title=dict(
        text='Who Poverty Hits Hardest: Young Men and Elderly Women',
        font=dict(size=18, color='#1D3557'),
        x=0.5, xanchor='center',
    ),
    barmode='overlay',
    bargap=0.08,
    xaxis=dict(
        title='Persons Below Poverty Level',
        tickfont=dict(size=11),
        tickvals=[-250, -200, -150, -100, -50, 0, 50, 100, 150, 200, 250],
        ticktext=['250', '200', '150', '100', '50', '0', '50', '100', '150', '200', '250'],
        zeroline=True, zerolinewidth=2, zerolinecolor='#1D3557',
        range=[-320, 320],
    ),
    yaxis=dict(
        tickfont=dict(size=12),
        categoryorder='array',
        categoryarray=age_labels[::-1],  # oldest at top
    ),
    legend=dict(
        orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5,
        font=dict(size=13),
    ),
    width=1100, height=700,
    margin=dict(l=100, r=80, t=130, b=100),
    annotations=[
        dict(
            text=SRC + '  •  Table B17001',
            xref='paper', yref='paper',
            x=0.5, y=-0.12,
            showarrow=False,
            font=dict(size=9, color='#8D99AE'),
            xanchor='center',
        ),
        # Star marker on Male 18–24 bar (the real spike)
        dict(
            text='★',
            x=-247, y='18–24',
            showarrow=False,
            font=dict(size=20, color='#1D3557'),
            xshift=-40,
        ),
        # Cross marker on Female 75+ bar (elderly women spike)
        dict(
            text='✦',
            x=174, y='75+',
            showarrow=False,
            font=dict(size=18, color='#9D0208'),
            xshift=40,
        ),
        # Legend box for indicators
        dict(
            text=(
                '<b>★</b> Male 18–24: 247 — young men hit hardest<br>'
                '<b>✦</b> Women 75+: 174 — 6× more than men'
            ),
            xref='paper', yref='paper',
            x=0.02, y=0.02,
            showarrow=False,
            font=dict(size=11, color='#1D3557', family='Arial'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#8D99AE',
            borderwidth=1,
            borderpad=8,
            align='left',
            xanchor='left', yanchor='bottom',
        ),
        dict(
            text='◀ MALE',
            xref='paper', yref='paper',
            x=0.15, y=1.06,
            showarrow=False,
            font=dict(size=14, color='#457B9D', family='Arial Black'),
        ),
        dict(
            text='FEMALE ▶',
            xref='paper', yref='paper',
            x=0.85, y=1.06,
            showarrow=False,
            font=dict(size=14, color='#E63946', family='Arial Black'),
        ),
    ],
)

fig.write_image(os.path.join(OUT, 'e1_poverty_by_age.png'), scale=2)
print("  → e1_poverty_by_age.png")

# ═══════════════════════════════════════════════════════════════════════════════
# E1.2 — Poverty Rate Comparison
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("E1.2: POVERTY RATE COMPARISON")
print("=" * 60)

# Census API verified (ACS 5-Year 2023, B17001)
pov_labels = ['United States', 'Louisiana', 'St. Helena Parish']
pov_rates = [12.4, 18.9, 33.7]
pov_colors = ['#2A9D8F', '#F4A261', '#E63946']

print(f"  St. Helena Parish: 33.7%")
print(f"  Louisiana: 18.9%")
print(f"  United States: 12.4%")

fig_pov = go.Figure()

# Clean horizontal bar chart — sorted by value
fig_pov.add_trace(go.Bar(
    y=pov_labels,
    x=pov_rates,
    orientation='h',
    marker=dict(
        color=pov_colors,
        line=dict(width=0),
    ),
    text=[f'<b>{v}%</b>' for v in pov_rates],
    textposition='outside',
    textfont=dict(size=14, color='#1D3557', family='Arial'),
    width=0.55,
))

fig_pov.update_layout(
    template='plotly_white',
    width=900, height=420,
    margin=dict(l=160, r=80, t=130, b=110),
    title=dict(
        text='Poverty at 2.7× the National Rate',
        font=dict(size=20, color='#1D3557', family='Arial'),
        x=0.5, xanchor='center',
    ),
    xaxis=dict(
        title=dict(text='Poverty Rate (%)', font=dict(size=12, color='#1D3557')),
        ticksuffix='%',
        tickfont=dict(size=12),
        range=[0, 42],
        gridcolor='rgba(0,0,0,0.05)',
    ),
    yaxis=dict(
        tickfont=dict(size=14, color='#1D3557', family='Arial'),
        categoryorder='array',
        categoryarray=pov_labels,  # US at bottom, St. Helena at top
    ),
    bargap=0.3,
    showlegend=False,
    annotations=[
        # Source
        dict(
            text=SRC + '  •  Table B17001',
            xref='paper', yref='paper',
            x=0.5, y=-0.35,
            showarrow=False,
            font=dict(size=9, color='#8D99AE'),
            xanchor='center',
        ),
    ],
)

fig_pov.write_image(os.path.join(OUT, 'e1_poverty_rate.png'), scale=2)

print("  → e1_poverty_rate.png")

# ═══════════════════════════════════════════════════════════════════════════════
# E1.3 — Income 3-Level Comparison
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("E1.3: INCOME 3-LEVEL COMPARISON")
print("=" * 60)

inc = df[df['Category'] == 'Income']
per_capita = int(inc[inc['Measure'] == 'Per capita income ($)']['Value'].values[0])
median_hh = int(inc[inc['Measure'] == 'Median household income ($)']['Value'].values[0])

# Census API verified (ACS 5-Year 2023): B19013, B19301
la_median_hh = 60_023
us_median_hh = 78_538

print(f"  Tract Median HH: ${median_hh:,}")
print(f"  LA Median HH: ${la_median_hh:,}")
print(f"  US Median HH: ${us_median_hh:,}")

# Dumbbell / dot plot — shows the GAP visually
gap_pct = round((1 - median_hh / us_median_hh) * 100)

measures = ['Median Household<br>Income', 'Per Capita<br>Income']
st_helena_vals = [median_hh, per_capita]
la_vals = [la_median_hh, 34_211]
us_vals = [us_median_hh, 43_289]

fig2 = go.Figure()

# Connecting lines (the "dumbbell" bar) — St. Helena to US
for i, measure in enumerate(measures):
    fig2.add_trace(go.Scatter(
        x=[st_helena_vals[i], us_vals[i]],
        y=[measure, measure],
        mode='lines',
        line=dict(color='#D3D3D3', width=8),
        showlegend=False,
        hoverinfo='skip',
    ))

# St. Helena dots
fig2.add_trace(go.Scatter(
    x=st_helena_vals,
    y=measures,
    mode='markers+text',
    marker=dict(size=18, color='#E63946', line=dict(width=2, color='white')),
    text=[f'${v:,}' for v in st_helena_vals],
    textposition='bottom center',
    textfont=dict(size=12, color='#9D0208', family='Arial'),
    name='St. Helena Parish',
))

# Louisiana dots
fig2.add_trace(go.Scatter(
    x=la_vals,
    y=measures,
    mode='markers+text',
    marker=dict(size=18, color='#F4A261', symbol='diamond',
                line=dict(width=2, color='white')),
    text=[f'${v:,}' for v in la_vals],
    textposition='top center',
    textfont=dict(size=12, color='#8B6914', family='Arial'),
    name='Louisiana',
))

# US dots
fig2.add_trace(go.Scatter(
    x=us_vals,
    y=measures,
    mode='markers+text',
    marker=dict(size=18, color='#2A9D8F', symbol='diamond',
                line=dict(width=2, color='white')),
    text=[f'${v:,}' for v in us_vals],
    textposition='top center',
    textfont=dict(size=12, color='#1B7A6E', family='Arial'),
    name='United States',
))

fig2.update_layout(
    template='plotly_white',
    title=dict(
        text=f'Income Gap: St. Helena Parish Earns {gap_pct}% Less Than the Nation',
        font=dict(size=16, color='#1D3557'),
        x=0.5, xanchor='center',
    ),
    xaxis=dict(
        title='Income ($)',
        tickprefix='$',
        tickformat=',',
        tickfont=dict(size=11),
        range=[0, max(us_vals) * 1.15],
    ),
    yaxis=dict(tickfont=dict(size=12)),
    legend=dict(
        orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5,
        font=dict(size=12),
    ),
    width=900, height=450,
    margin=dict(l=140, r=60, t=100, b=90),
    annotations=[
        dict(
            text=SRC + '  •  Tables B19013, B19301',
            xref='paper', yref='paper',
            x=0.5, y=-0.25,
            showarrow=False,
            font=dict(size=9, color='#8D99AE'),
            xanchor='center',
        ),
    ],
)

fig2.write_image(os.path.join(OUT, 'e1_income_comparison.png'), scale=2)
print("  → e1_income_comparison.png")

print("\n" + "=" * 60)
print("E1 COMPLETE — 3 charts saved to outputs/e1/")
print("=" * 60)
