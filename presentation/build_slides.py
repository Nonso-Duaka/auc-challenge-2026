"""
AUC Data Challenge 2026 -Presentation Slide Deck (PDF)
Team DataRx | St. Helena Parish, Louisiana | Census Tract 22091 951100
"""

from fpdf import FPDF
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(BASE, 'outputs')
OUT = os.path.join(BASE, 'presentation')
os.makedirs(OUT, exist_ok=True)

# Colors (RGB)
NAVY = (29, 53, 87)
TEAL = (42, 157, 143)
CORAL = (230, 57, 70)
WHITE = (255, 255, 255)
LIGHT = (248, 249, 250)
MUTED = (141, 153, 174)
DARK = (51, 51, 51)


class SlideDeck(FPDF):
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_auto_page_break(auto=False)
        # A4 landscape: 297 x 210 mm

    def slide_bg(self, dark=False):
        if dark:
            self.set_fill_color(*NAVY)
        else:
            self.set_fill_color(*WHITE)
        self.rect(0, 0, 297, 210, 'F')
        # Accent bar at top
        self.set_fill_color(*TEAL)
        self.rect(0, 0, 297, 3, 'F')

    def slide_number(self, n, total=10):
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*MUTED)
        self.text(280, 205, f'{n}/{total}')

    def section_title(self, title, subtitle='', y=60):
        self.set_font('Helvetica', 'B', 32)
        self.set_text_color(*NAVY)
        self.set_xy(30, y)
        self.cell(237, 15, title, align='L')
        if subtitle:
            self.set_font('Helvetica', '', 14)
            self.set_text_color(*MUTED)
            self.set_xy(30, y + 18)
            self.multi_cell(237, 7, subtitle, align='L')

    def body_text(self, text, x=30, y=90, w=237, size=12, bold=False):
        self.set_font('Helvetica', 'B' if bold else '', size)
        self.set_text_color(*DARK)
        self.set_xy(x, y)
        self.multi_cell(w, 7, text, align='L')

    def bullet(self, text, x=30, y=None, size=11):
        if y:
            self.set_xy(x, y)
        self.set_font('Helvetica', '', size)
        self.set_text_color(*DARK)
        self.cell(5, 7, "-", align='L')
        self.multi_cell(225, 7, f'  {text}', align='L')

    def place_image(self, path, x, y, w=None, h=None):
        full = os.path.join(IMG, path) if not os.path.isabs(path) else path
        if os.path.exists(full):
            self.image(full, x=x, y=y, w=w, h=h)
        else:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(*CORAL)
            self.text(x, y + 10, f'[Image not found: {path}]')

    def footer_source(self, text):
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(*MUTED)
        self.text(30, 200, text)


pdf = SlideDeck()

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1: Title Slide
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 297, 210, 'F')
pdf.set_fill_color(*TEAL)
pdf.rect(0, 0, 297, 5, 'F')

pdf.set_font('Helvetica', 'B', 38)
pdf.set_text_color(*WHITE)
pdf.set_xy(30, 50)
pdf.cell(237, 18, 'Community Hub Marketplace', align='L')

pdf.set_font('Helvetica', '', 18)
pdf.set_text_color(*TEAL)
pdf.set_xy(30, 72)
pdf.cell(237, 10, 'Bridging Economic Gaps to Improve Healthcare Access', align='L')

pdf.set_font('Helvetica', '', 13)
pdf.set_text_color(200, 200, 210)
pdf.set_xy(30, 100)
pdf.cell(237, 8, 'St. Helena Parish, Louisiana  |  Census Tract 22091 951100', align='L')
pdf.set_xy(30, 110)
pdf.cell(237, 8, 'AUC Data Challenge 2026', align='L')

pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(*TEAL)
pdf.set_xy(30, 140)
pdf.cell(237, 10, 'Team DataRx', align='L')

pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(200, 200, 210)
pdf.text(30, 195, '"In communities with an IGS below 45, how do economic conditions affect healthcare access,')
pdf.text(30, 201, 'and how can small businesses help improve outcomes?"')

pdf.slide_number(1)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2: Objective & Problem Statement
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Objective & Problem Statement', '', y=15)

pdf.body_text('The Challenge:', x=30, y=42, size=14, bold=True)
pdf.body_text(
    'St. Helena Parish has an Inclusive Growth Score of just 36 -well below the 45 threshold. '
    'This rural community of ~10,000 faces compounding economic and health crises that reinforce each other.',
    x=30, y=52, size=11
)

pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(*CORAL)
pdf.set_xy(30, 76)
pdf.cell(100, 7, 'The Vicious Cycle:', align='L')

pdf.set_xy(30, 85)
pdf.bullet('No local jobs  >62% of working-age adults not employed', y=86)
pdf.bullet('No local jobs  >90% of workers commute out of parish', y=94)
pdf.bullet('No employers  >only 7.9% have employer-based insurance (vs 55% nationally)', y=102)
pdf.bullet('No healthcare  >zero pharmacies, 1 dentist, 2 PCPs for 10,000 people', y=110)
pdf.bullet('No internet  >3rd percentile nationally for internet access', y=118)
pdf.bullet('Poverty  >33.7% poverty rate (2.7x the national rate)', y=126)

pdf.body_text('Our Solution:', x=30, y=142, size=14, bold=True)
pdf.body_text(
    'A Community Hub Marketplace -a physical and digital center that creates local jobs with employer insurance, '
    'brings healthcare services (pharmacy, clinic referrals), provides broadband, incubates small businesses, '
    'and keeps spending local. One intervention, multiple IGS levers.',
    x=30, y=152, size=11
)

pdf.slide_number(2)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3: Community Overview
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Community Overview', 'St. Helena Parish -Demographics, Economic Conditions & Social Metrics', y=15)

# Left: economic table image
pdf.place_image('po/po_economic_table.png', x=10, y=45, w=130)

# Right: hub metrics image
pdf.place_image('po/po_hub_metrics.png', x=148, y=42, w=140)

pdf.footer_source('Source: U.S. Census ACS 2023, Inclusive Growth Score 2025  •  api.census.gov  •  inclusivegrowthscore.com')
pdf.slide_number(3)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4: Benchmarking
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Benchmarking', 'IGS Ranking vs State and National Averages', y=15)

# Left: IGS trend
pdf.place_image('po/po_igs_history.png', x=8, y=42, w=140)

# Right: IGS breakdown
pdf.place_image('po/po_igs_breakdown.png', x=155, y=42, w=135)

# Bottom: benchmarking chart
pdf.place_image('bm/bm_benchmarking.png', x=30, y=130, w=237)

pdf.slide_number(4)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5: Key Findings (Economic)
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Key Findings: Economic Crisis', 'Poverty, Employment & the Worker Exodus', y=15)

# 3 charts across
pdf.place_image('e1/e1_poverty_rate.png', x=5, y=40, w=95)
pdf.place_image('e2/e2_labor_force.png', x=101, y=40, w=95)
pdf.place_image('e2/e2_worker_exodus.png', x=197, y=40, w=95)

# Bottom row
pdf.place_image('e2/e2_commute_times.png', x=5, y=115, w=95)
pdf.place_image('e3/e3_insurance_by_employment.png', x=101, y=115, w=95)
pdf.place_image('e1/e1_income_comparison.png', x=197, y=115, w=95)

pdf.slide_number(5)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6: Key Findings (Healthcare)
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Key Findings: Healthcare Desert', 'Disease Burden, Provider Shortages & Preventable Hospitalizations', y=15)

pdf.place_image('h1/h1_chronic_disease.png', x=5, y=40, w=95)
pdf.place_image('h2/h2_provider_counts.png', x=101, y=40, w=95)
pdf.place_image('h2/h2_preventable_hosp.png', x=197, y=40, w=95)

pdf.place_image('h1/h1_social_determinants.png', x=5, y=115, w=95)
pdf.place_image('h2/h2_life_expectancy.png', x=101, y=115, w=95)
pdf.place_image('s1/s1_healthcare_gaps.png', x=197, y=115, w=95)

pdf.slide_number(6)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7: Proposed Solution
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Proposed Solution: Community Hub Marketplace', '', y=15)

# Feature importance -shows Hub targets the right levers
pdf.place_image('po/po_feature_importance.png', x=148, y=35, w=145)

pdf.body_text('One Hub. Multiple IGS Levers.', x=30, y=42, size=13, bold=True)

interventions = [
    ('Local Jobs', 'Create 25-50 jobs with employer-sponsored health insurance'),
    ('Broadband Center', 'Free WiFi + computer lab (internet access: 3rd to 23rd percentile)'),
    ('Pharmacy & Clinic', 'First pharmacy in parish; telehealth clinic referrals'),
    ('Small Business Incubator', 'Vendor stalls, shared commercial kitchen, SBA loan assistance'),
    ('Fresh Food Market', 'Local produce section combating 33.4% food insecurity'),
    ('Daycare & After-School', 'Enabling workforce participation for parents'),
    ('Digital Services', 'Online job portal, government services kiosk, financial literacy'),
]

y = 58
for title, desc in interventions:
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*TEAL)
    pdf.set_xy(30, y)
    pdf.cell(5, 6, "-", align='L')
    pdf.cell(50, 6, f'  {title}:', align='L')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*DARK)
    pdf.cell(70, 6, desc, align='L')
    y += 11

pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(*NAVY)
pdf.set_xy(30, y + 8)
pdf.cell(120, 7, 'The Hub targets 12 of 18 IGS drivers (see chart).')

pdf.footer_source('Source: XGBoost model feature importance trained on 1.4M IGS observations')
pdf.slide_number(7)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8: Implementation Plan
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Implementation Plan', '', y=15)

phases = [
    ('Year 1: Foundation', [
        'Secure facility (repurpose vacant commercial building)',
        'Launch broadband center + digital services kiosk',
        'Open fresh food market with local produce',
        'Partner with FQHCs for telehealth clinic',
        'Begin SBA loan outreach for small business vendors',
    ]),
    ('Year 2-3: Growth', [
        'Recruit pharmacy operator (CVS/Walgreens partnership or independent)',
        'Expand to 15-20 vendor stalls (small business incubator)',
        'Launch daycare / after-school program',
        'Establish employer-sponsored insurance for all Hub employees',
        'Digital literacy & job training programs',
    ]),
    ('Year 4-5: Scale', [
        'Hub reaches 40-50 employees with full benefits',
        'Second location or mobile Hub for outlying areas',
        'Mentor program: Hub businesses launch independent storefronts',
        'Community health worker program integrated with Hub',
        'Target: IGS above 45 threshold',
    ]),
]

y = 40
for phase_title, items in phases:
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(*TEAL)
    pdf.set_xy(30, y)
    pdf.cell(237, 8, phase_title, align='L')
    y += 10
    for item in items:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*DARK)
        pdf.set_xy(35, y)
        pdf.cell(5, 6, "-")
        pdf.cell(220, 6, f'  {item}')
        y += 7
    y += 5

# Stakeholders, risks
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(*NAVY)
pdf.set_xy(30, y + 2)
pdf.cell(237, 7, 'Key Stakeholders:')
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(*DARK)
pdf.set_xy(30, y + 10)
pdf.cell(237, 6, 'St. Helena Parish Government  |  SBA  |  USDA Rural Development  |  FQHCs  |  Mastercard Center for Inclusive Growth')

pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(*NAVY)
pdf.set_xy(30, y + 20)
pdf.cell(237, 7, 'Risks & Mitigations:')
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(*DARK)
pdf.set_xy(30, y + 28)
pdf.multi_cell(237, 6, 'Low foot traffic (mitigate: anchor tenants + essential services)  |  Funding gaps (mitigate: USDA grants + New Market Tax Credits)  |  Workforce readiness (mitigate: on-site training)')

pdf.slide_number(8)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9: Predicted Outcomes
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Predicted Outcomes', 'XGBoost Model: R²=0.99 trained on 1.4M IGS observations across 85K tracts', y=15)

# Top row: trajectory + radar
pdf.place_image('po/po_trajectory.png', x=5, y=38, w=145)
pdf.place_image('po/po_radar.png', x=150, y=35, w=142)

# Bottom row: scenario bars + waterfall
pdf.place_image('po/po_scenario_bars.png', x=5, y=115, w=145)
pdf.place_image('po/po_waterfall.png', x=150, y=115, w=145)

pdf.slide_number(9)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10: Metrics for Success
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.slide_bg()
pdf.section_title('Metrics for Success', 'Indicators to Track Long-Term Impact', y=15)

pdf.place_image('ms/ms_metrics_dashboard.png', x=148, y=35, w=145)

metrics_list = [
    ('IGS Score', '36 >45+', 'Primary outcome; model-validated'),
    ('Employer Insurance Rate', '7.9% >25%', 'Hub jobs with benefits'),
    ('Labor Participation', '50.9% >60%', 'Local job creation'),
    ('Internet Access', '3rd >25th pctile', 'Broadband center'),
    ('Commercial Diversity', '34th >54th pctile', 'New business sectors'),
    ('Preventable Hospitalizations', '4,862 >3,500 per 100K', 'Local healthcare access'),
    ('Food Insecurity', '33.4% >20%', 'Fresh food market'),
]

y = 42
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(*NAVY)
pdf.set_xy(30, y)
pdf.cell(35, 7, 'Metric')
pdf.cell(40, 7, 'Target')
pdf.cell(50, 7, 'Mechanism')
y += 9

for metric, target, mechanism in metrics_list:
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*DARK)
    pdf.set_xy(30, y)
    pdf.cell(35, 6, metric)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*TEAL)
    pdf.cell(40, 6, target)
    pdf.set_text_color(*MUTED)
    pdf.cell(50, 6, mechanism)
    y += 9

pdf.slide_number(10)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11: Conclusion
# ══════════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 297, 210, 'F')
pdf.set_fill_color(*TEAL)
pdf.rect(0, 0, 297, 5, 'F')

pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(*WHITE)
pdf.set_xy(30, 40)
pdf.cell(237, 15, 'Conclusion', align='L')

pdf.set_font('Helvetica', '', 15)
pdf.set_text_color(*TEAL)
pdf.set_xy(30, 62)
pdf.multi_cell(237, 9, 'St. Helena Parish does not need charity - it needs infrastructure.\nThe Community Hub Marketplace is that infrastructure.', align='L')

summary = [
    'One intervention targeting 12 of 18 IGS drivers simultaneously',
    'XGBoost model (R²=0.99) projects IGS from 36 to 46.5 in 5 years',
    'Crossing the 45 threshold -answering the challenge question directly',
    'Employer insurance alone could 3x coverage (7.9% >25%)',
    '10 real Louisiana tracts already at our Year 3 target -this is achievable',
    'Every dollar spent locally recirculates -the Hub creates a virtuous cycle',
]

y = 95
for s in summary:
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(200, 200, 210)
    pdf.set_xy(35, y)
    pdf.cell(5, 7, "-")
    pdf.cell(230, 7, f'  {s}')
    y += 12

pdf.set_font('Helvetica', 'B', 18)
pdf.set_text_color(*TEAL)
pdf.set_xy(30, 175)
pdf.cell(237, 10, 'Team DataRx', align='L')

pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(200, 200, 210)
pdf.text(30, 195, 'AUC Data Challenge 2026  |  St. Helena Parish, Louisiana')

pdf.slide_number(11, 11)

# ─── Save ─────────────────────────────────────────────────────────────────────
outpath = os.path.join(OUT, 'DataRx_AUC_Challenge_2026.pdf')
pdf.output(outpath)
print(f'Done! Saved: {outpath}')
print(f'Slides: 11 (Title + 10 content)')
