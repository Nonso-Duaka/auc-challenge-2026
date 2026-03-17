"""
H1: Disease Burden & Social Determinants
Data: CountiesCompareData_03142026.csv (CDC PLACES)
URL: https://www.cdc.gov/places
Charts: C1 (Chronic diseases) + C6 (Social determinants) + C9 (Disability)
"""

import pandas as pd
import plotly.graph_objects as go
import warnings, os, sys

warnings.filterwarnings('ignore', message='.*Kaleido.*')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chart_style import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'outputs', 'h1')
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(os.path.join(BASE, 'data', 'healthcare', 'CountiesCompareData_03142026.csv'))
SRC = 'Source: CDC PLACES, 2023  •  https://www.cdc.gov/places'

sh = df[(df['Location'] == 'St. Helena') & (df['Data Type'] == 'Age-adjusted prevalence')]
us = df[(df['Location'] == 'United States') & (df['Data Type'] == 'Age-adjusted prevalence')]

def get_val(subset, keyword):
    row = subset[subset['Measure'].str.contains(keyword, case=False, na=False)]
    if len(row) > 0:
        val = row['Data Value'].values[0]
        return float(str(val).replace('%', ''))
    return None


def make_grouped_hbar(title, labels, sh_vals, us_vals, outfile, src_table=''):
    """Build a polished grouped horizontal bar chart: US vs St. Helena."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=labels, x=us_vals, orientation='h',
        name='United States',
        marker=dict(color=TEAL, cornerradius=3, line=dict(width=0)),
        text=[f'{v}%' for v in us_vals],
        textposition='outside', textfont=dict(size=10, color='#1B7A6E'),
    ))
    fig.add_trace(go.Bar(
        y=labels, x=sh_vals, orientation='h',
        name='St. Helena Parish',
        marker=dict(color=CORAL, cornerradius=3, line=dict(width=0)),
        text=[f'{v}%' for v in sh_vals],
        textposition='outside', textfont=dict(size=10, color='#9D0208'),
    ))

    fig.update_layout(
        **base_layout(title, width=1020, height=560, b_margin=130, l_margin=190, r_margin=80),
        barmode='group',
        xaxis=dict(
            title=dict(text='Prevalence (%)', font=dict(size=12, color=NAVY)),
            ticksuffix='%', tickfont=dict(size=11),
            gridcolor='rgba(0,0,0,0.04)',
        ),
        yaxis=dict(
            tickfont=dict(size=12, color=NAVY, family='Arial'),
            categoryorder='array', categoryarray=labels[::-1],
        ),
        legend=grouped_legend(),
        bargap=0.25,
        annotations=[source_annotation(SRC + src_table, y=-0.28)],
    )
    fig.write_image(os.path.join(OUT, outfile), scale=3)


# ═══════════════════════════════════════════════════════════════════════════════
# H1.1 — C1: Chronic Disease
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("H1.1: CHRONIC DISEASE — ST. HELENA vs US")
print("=" * 60)

diseases = [
    ('Obesity', 'Obesity'), ('High Blood Pressure', 'High blood pressure'),
    ('Diabetes', 'Diagnosed diabetes'), ('Depression', 'Depression'),
    ('COPD', 'Chronic obstructive'), ('Coronary Heart Disease', 'Coronary heart'),
    ('Asthma', 'Current asthma'), ('Stroke', 'Stroke'),
]

d_labels = [d[0] for d in diseases]
sh_d = [get_val(sh, d[1]) for d in diseases]
us_d = [get_val(us, d[1]) for d in diseases]

combined = sorted(zip(d_labels, sh_d, us_d), key=lambda x: x[1], reverse=True)
d_labels, sh_d, us_d = zip(*combined)

for l, s, u in zip(d_labels, sh_d, us_d):
    print(f"  {l:>25s}: St.H {s}%  |  US {u}%")

make_grouped_hbar(
    'Chronic Disease: St. Helena Far Exceeds the Nation',
    list(d_labels), list(sh_d), list(us_d),
    'h1_chronic_disease.png',
)
print("  → h1_chronic_disease.png")

# ═══════════════════════════════════════════════════════════════════════════════
# H1.2 — C6: Social Determinants
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("H1.2: SOCIAL DETERMINANTS — ST. HELENA vs US")
print("=" * 60)

social = [
    ('Food Insecurity', 'Food insecurity'), ('Loneliness', 'Loneliness'),
    ('Lack of Social Support', 'Lack of social'), ('Housing Insecurity', 'Housing insecurity'),
    ('Utility Threat', 'Utility services'), ('No Reliable Transport', 'Lack of reliable'),
    ('Food Stamps', 'Received food stamps'),
]

s_labels = [s[0] for s in social]
sh_s = [get_val(sh, s[1]) for s in social]
us_s = [get_val(us, s[1]) for s in social]

combined = sorted(zip(s_labels, sh_s, us_s), key=lambda x: x[1], reverse=True)
s_labels, sh_s, us_s = zip(*combined)

for l, s, u in zip(s_labels, sh_s, us_s):
    print(f"  {l:>25s}: St.H {s}%  |  US {u}%")

make_grouped_hbar(
    'Isolation and Insecurity Define Daily Life',
    list(s_labels), list(sh_s), list(us_s),
    'h1_social_determinants.png',
)
print("  → h1_social_determinants.png")

# ═══════════════════════════════════════════════════════════════════════════════
# H1.3 — C9: Disability
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("H1.3: DISABILITY — ST. HELENA vs US")
print("=" * 60)

disability = [
    ('Any Disability', 'Any disability'), ('Cognitive', 'Cognitive disability'),
    ('Mobility', 'Mobility disability'), ('Independent Living', 'Independent living'),
    ('Vision', 'Vision disability'), ('Hearing', 'Hearing disability'),
    ('Self-Care', 'Self-care disability'),
]

dis_labels = [d[0] for d in disability]
sh_dis = [get_val(sh, d[1]) for d in disability]
us_dis = [get_val(us, d[1]) for d in disability]

combined = sorted(zip(dis_labels, sh_dis, us_dis), key=lambda x: x[1], reverse=True)
dis_labels, sh_dis, us_dis = zip(*combined)

for l, s, u in zip(dis_labels, sh_dis, us_dis):
    print(f"  {l:>25s}: St.H {s}%  |  US {u}%")

make_grouped_hbar(
    '43% of Adults Have a Disability — 1.5× the National Rate',
    list(dis_labels), list(sh_dis), list(us_dis),
    'h1_disability.png',
)
print("  → h1_disability.png")

print("\n" + "=" * 60)
print("H1 COMPLETE — 3 charts saved to outputs/h1/")
print("=" * 60)
