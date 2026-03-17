# CLAUDE.md — Full Project Context

## Directory Structure
- `data/` — Raw data files organized by domain (economy, healthcare, small_business, igs)
- `analysis/` — Python analysis scripts
- `outputs/` — Generated charts, tables, and results (PNG 300 DPI)
- `docs/` — Reference documentation and this file

## Data Sources Overview
- **Economy**: Census ACS API, OnTheMap worker flows, QWI (job creation & salary by age)
- **Healthcare**: CDC PLACES (40 health measures), HRSA HPSA designations, HRSA MUA/IMU scores, County Health Rankings
- **Small Business**: County Business Patterns (NAICS industries)
- **IGS**: PolicyMap Inclusive Growth Score for St. Helena Parish

## Conventions
- Python scripts go in `analysis/`
- All generated outputs (charts, CSVs, tables) go in `outputs/`
- Use pandas for data manipulation, matplotlib/seaborn for visualization, openpyxl for Excel
- CDC CSV needs `encoding='utf-8-sig'`
- CHR XLSX: Row 1=measure groups, Row 2=headers, data row 3+
- CHR: FIPS 22091 = St. Helena, FIPS 22000 = Louisiana state
- Charts: PNG 300 DPI, saved to `outputs/`

---

## What This Project Is
Submission for the **2026 Mastercard IGS & AUD DSI Data Challenge** — HBCU student competition. Over $50,000 in prize money.

**Challenge Prompt:** "In communities with an Inclusive Growth Score (IGS) below 45, how do economic conditions affect healthcare access, and how can small businesses help improve outcomes?"

The word "affect" demands CAUSATION, not description. Every finding must cause the next.

## Community Selected: St. Helena Parish, Louisiana
**Census Tract 22091 951100** — IGS Score: 36, Population: 3,541 (tract) / 10,774 (parish)

### Why St. Helena
1. **Data completeness:** 18/18 IGS metrics filled — no gaps.
2. **Extreme contrasts:** Affordable housing 99, early education 97, net occupancy 81 — BUT internet access 3, travel time 1, labor market 1. This tension is the story: "Why is this community still struggling when housing is affordable?"
3. **Healthcare angle is strongest:** Travel time 1 + internet 3 = can't physically reach care AND can't use telehealth.
4. **Small business data exists:** Minority/women business data (1.8%), commercial diversity (17.7%).

### IGS Metric Breakdown (Tract 22091 951100)
**Place Pillar (44):** Net Occupancy +20.9% (81), Residential RE +31.8% (40), Park Land 0.5% (14), Affordable Housing 94.0% (99), Internet 66.1% (3), Travel Time 33.0% (1)
**Economy Pillar (30):** New Businesses +9.8% (43), Spend Growth (34), Small Biz Loans 0.0% (45), Minority/Women Biz 1.8% (22), Labor Market 1.0 (1), Commercial Diversity 17.7% (34)
**Community Pillar (33):** Personal Income Growth -9.8% (15), Spending/Capita (34), Female Above Poverty 66.1% (12), Gini 0.5 (18), Early Education 74.7% (97), Health Insurance 92.4% (39)

## How The Analysis Approach Evolved
Initially organized by TOPIC (economy, healthcare, small business as parallel buckets). Pivoted to a CAUSAL CHAIN where each finding causes the next. The analysis WORKBENCH follows E1-E3, H1-H3, S1-S3 to pull all numbers. The PRESENTATION arranges results into the 9-link causal chain. Run all analyses first, THEN connect into the chain.

## Benchmarking Strategy (3 levels)
Every measure is compared at THREE levels using the County Health Rankings files:
- **St. Helena Parish** (FIPS 22091) — our community
- **Louisiana state** (FIPS 22000) — state context
- **US overall** — national benchmark (from CHR Sources sheet or national file)

This eliminates the excuse "rural areas are just like that." If St. Helena is worse than BOTH the state AND the nation, the argument is airtight.

### CHR Benchmark Values (3-level comparisons)

| Measure | St. Helena | Louisiana | US | Source |
|---------|-----------|-----------|-----|--------|
| Life expectancy | 70.0 yrs | 73.3 yrs | ~78 yrs | CHR Additional col 3 |
| YPLL rate (premature death) | 19,092 | 12,185 | 8,400 | CHR Select col 5, Sources |
| Preventable hosp rate | 4,862 | 3,427 | 2,666 | CHR Select col 98, Sources |
| # PCPs | 2 | 3,210 (state total) | Ratio 1,330:1 | CHR Select col 86, Sources |
| # Dentists | 1 | 2,713 (state total) | Ratio 1,360:1 | CHR Select col 94, Sources |
| # MH Providers | 9 | 16,165 (state total) | Ratio 300:1 | CHR Select col 90, Sources |
| Food Environment Index | 6.7 / 10 | 4.8 / 10 | 7.4 / 10 | CHR Select col 84, Sources |
| Broadband % | 68.3% | 84.8% | ~90% | CHR Select col 158 |
| % Fair/Poor Health | 26.5% | 20.7% | 17% | CHR Select col 71, Sources |
| Physically unhealthy days/mo | 5.2 | 4.6 | 3.9 | CHR Select col 37, Sources |
| Mentally unhealthy days/mo | 6.8 | 6.4 | 5.1 | CHR Select col 67, Sources |
| Obesity % | 46.3% | 40.3% | ~32% | CHR Additional col 110 |
| Diabetes % | 15.2% | 13.2% | ~12% | CHR Additional col 105 |
| Physical inactivity % | 35% | 27.5% | ~24% | CHR Additional col 214 |
| Median HH Income | $46,835 | $58,273 | ~$75,000 | CHR Additional col 266 |
| Homicide rate | 27.4 | 15.9 | ~6 | CHR Additional col 287 |
| % Drive Alone | 79.5% | 79.4% | ~76% | CHR Select col 130 |

**Key insight from benchmarking:** St. Helena is worse than Louisiana on every single measure, and Louisiana is already worse than the US on most. St. Helena sits at the bottom of a state that's already near the bottom nationally. For provider counts, calculate ratios: St. Helena PCP ratio = 10,774/2 = 5,387:1 vs US benchmark 1,330:1 = 4x worse. Dentist ratio = 10,774/1 = 10,774:1 vs US 1,360:1 = 7.9x worse.

## The Causal Chain (9 links)

**Link 1: People are poor and getting poorer** — 33.7% poverty (3x US). Per capita $22,536. Median HH $45,618 (vs LA $58,273 vs US ~$75k). Incomes falling -9.8%. Women 65-74 are 3.3x more likely impoverished.

**Link 2: Poverty causes food insecurity which causes chronic disease** — Food insecurity 31.7% (2.2x US). Food Env Index 6.7 vs US 7.4. This produces: HBP 49.3% vs 34.4%, diabetes 19.8% vs 12.0%, obesity 42.7% vs 32.8% (CHR confirms at 46.3% vs LA 40.3%), disability 45.6% vs 30.0%.

**Link 3: Not enough providers** — HPSA all 3 disciplines (dental 22/26, MH 20/25, PC 15/25). 2 PCPs (ratio 5,387:1 vs US 1,330:1). 1 dentist (10,774:1 vs US 1,360:1). Preventable hosp 4,862 vs LA 3,427 vs US 2,666. Life expectancy 70 vs LA 73.3 vs US ~78.

**Link 4: Can't reach them** — 90.4% commute out daily. Zero public transit. 38.2% commute 60+ min.

**Link 5: Can't use telehealth** — 68.3% broadband vs LA 84.8% vs US ~90%. IGS internet 3/100. NAICS 51 = 0.

**Link 6: Jobs don't provide insurance** — 7.9% employer insurance (US ~55%). 18.8% employed uninsured. Women dominate food/retail with zero benefits.

**Link 7: Residents ARE trying** — Checkups 83.4% (above US 77.7%). BP meds 81.7%. Dental 50.8% (-13 pts because zero dentists). Supply fails, not demand.

**Link 8: Every gap has a name** — 10/20 sectors missing. 12/16 healthcare NAICS = 0. Each connects to a specific problem.

**Link 9: Each gap = a small business** — 6 recommendations with NAICS code, CDC data, HPSA designation, federal funding pathway.

## Key Data Points That Win
- 7.9% employer insurance (vs 55% US) — the bombshell
- 90.4% of workers leave daily — the exodus
- 2 doctors, 1 dentist for 10,774 — the shortage
- 4,862 preventable hosp/100k (vs LA 3,427 vs US 2,666) — the consequence
- 70 years life expectancy (vs LA 73.3 vs US 78) — the outcome
- 12 of 16 healthcare NAICS = 0 — the opportunity
- 83.4% got checkups (above US) — demand exists, supply fails

## Data Files

### data/economy/census_tract_951100_data.csv
Source: Census ACS 5-Year (2019-2023) via API. 104 rows. Cols: Category, Measure, Value, Margin_of_Error, Notes.
Categories: Poverty, Poverty by Age, Employment, Income, Health Insurance, Insurance by Employment, Industry, Transportation, Travel Time.

### data/healthcare/CountiesCompareData_03142026.csv
Source: CDC PLACES. 161 rows. **Encoding: utf-8-sig.** ALWAYS filter Data Type == "Crude prevalence". Compare Location "St. Helena" vs "United States". 40 measures across 6 categories: Health Outcomes, Disability, Health-Related Social Needs, Prevention, Health Risk Behaviors, Health Status.

### data/small_business/cbp_st_helena_parish.csv
Source: Census CBP 2022 via API. Cols: NAICS, Industry, Establishments, Employment, Annual_Payroll_1000s, Level, Healthcare_Related.
Filter Level=="2-digit sector" for overview (10 present). Level=="MISSING SECTOR" for 10 gaps. Healthcare_Related containing "MISSING" for 12 healthcare gaps.

### data/healthcare/Hpsa_Find_Export.xlsx
Source: HRSA. Sheet "HPSA Find", header row 4. Filter Discipline not empty AND HPSA Name contains "St. Helena" (not "SOUTHEAST"). 3 parish designations + 3 FQHC designations.
Parish: Mental Health 20/25 FTE 0.72, Dental 22/26 FTE 1.39, Primary Care 15/25 MCTA 22/25 FTE 0.53.
FQHC (SCHS): 5 sites in St. Helena (1 primary clinic + 4 school-based). 27+ total across 4 parishes.

### data/healthcare/Data_Explorer_Dataset.xlsx
Source: HRSA Data Explorer. 1 data row (row 4): St. Helena Parish, MUA, IMU Score 52.5/100, Designated (threshold: below 62).

### data/healthcare/2025_County_Health_Rankings_Louisiana_Data_-_v3.xlsx
Source: CHR 2025, Louisiana only. Two sheets: "Select Measure Data" and "Additional Measure Data". Row 1 = measure group names, Row 2 = column headers. Data starts row 3.
**St. Helena = FIPS 22091. Louisiana state = FIPS 22000 (first data row).**
Key Select cols: YPLL (5), Phys days (37), Mental days (67), Fair/Poor health (71), Food Env (84), # PCPs (86), # MH (90), # Dentists (94), Preventable Hosp (98), # Uninsured (112), % Drive Alone (130), Broadband (158).
Key Additional cols: Life Expectancy (3), Diabetes (105), Obesity (110), Physical Inactivity (214), Food Insecure (147), Women's Earnings (261), Median HH Income (266), Homicide Rate (287), % Rural (392), Population (394).

### data/healthcare/2025_County_Health_Rankings_Data_-_v4.xlsx
Source: CHR 2025, ALL US counties. Same structure. Use for national comparison values. Also check "Select Measure Sources & Years" sheet — columns "Top Performers" and "US Overall" have national benchmarks.

### data/economy/otm_inandout.pdf
Source: Census OnTheMap (LEHD), 2023. Page 2: 2,880 leave (90.4%), 305 local (9.6%), 924 commute in. Total jobs: 1,229. Workers: 3,185. Deficit: 1,956.

### data/igs/Inclusive_Growth_Score_22091951100.pdf
IGS report for St. Helena Parish (Tract 22091 951100, IGS 36).

### data/economy/qwi_job_creation.svg + qwi_averagesalary.svg
QWI visuals — job creation and salary by age group.

## Analysis Structure

### Part 1: Economy (E1-E3)
- **E1 — Poverty/income:** Census CSV Poverty, Poverty by Age, Income. CHR Median HH Income for 3-level benchmark ($46,835 vs LA $58,273 vs US ~$75k).
- **E2 — Employment/exodus:** Census Employment, Transportation, Travel Time + OnTheMap. CHR % Drive Alone for parish confirmation.
- **E3 — Insurance gap:** Census Insurance by Employment, Industry, Health Insurance. **7.9% employer insurance is the bombshell.** CHR # Uninsured (687 parish) for absolute count.

### Part 2: Healthcare (H1-H3)
- **H1 — Disease burden:** CDC CSV filtered Crude prevalence, pivoted St. Helena vs US. CHR cross-validates obesity (46.3% vs LA 40.3%), diabetes (15.2% vs LA 13.2%). Life expectancy 3-level: 70 vs LA 73.3 vs US 78.
- **H2 — Federal designations + providers:** HPSA + MUA + CHR. Provider counts at 3 levels: 2 PCPs / 1 dentist vs LA totals vs US ratios. Preventable hosp 3-level: 4,862 vs LA 3,427 vs US 2,666.
- **H3 — Access barriers:** 4 dimensions: Physical (0 transit), Financial (7.9% employer ins), Digital (68.3% broadband vs LA 84.8% vs US ~90%), Provider (2 PCPs, 1 dentist). All benchmarked 3 levels.

### Part 3: Small Business (S1-S3)
- **S1 — Industry gaps:** CBP. 10 missing sectors, 12 missing healthcare NAICS.
- **S2 — Worker flow:** OnTheMap + CBP + Census. Deficit 1,956. Commute cost $4.37M/yr. Healthcare already #1 sector (450 emp, $15.7M).
- **S3 — 6 recommendations:** NAICS gap + CDC need + Census case + HPSA funding for each.

## 6 Recommendations
1. **Mobile dental clinic** — NAICS 6212=0. Dental visits -13 pts. HPSA 22/26. CHR: 1 dentist (ratio 10,774:1 vs US 1,360:1). Medicaid 43.7% is payer. Must be mobile (0 transit).
2. **Home health care** — NAICS 6216=0. Disability 45.6%. Mobility 24.3%. 0 transit. 49.1% not in LF = potential workforce.
3. **Pharmacy** — NAICS 44611=0. HBP 49.3%. BP meds 81.7% compliance. 92.4% insured. 0 transit to other parish.
4. **Medical transport** — NAICS 485=0. No transport 15.1% vs 7.7%. 0 public transit. 90.4% commute out. Preventable hosp 4,862.
5. **Telehealth hub** — NAICS 51=0. Internet 3/100. Broadband 68.3% vs LA 84.8%. Depression 25.7%. HPSA MH 20/25.
6. **Wellness center** — NAICS 71=0. Obesity 46.3% vs LA 40.3% vs US ~32%. No exercise 39.2%. Food desert.

## 13 Charts
C1: Horiz grouped bar — 8 chronic diseases, St. Helena vs US (CDC Health Outcomes)
C2: Stacked bar — employment status (Census Employment)
C3: Bar — employer insurance 7.9/27.6/55% (Census Insurance by Employment) **#1 VISUAL**
C4: Histogram — travel time brackets color-coded (Census Travel Time)
C5: Grouped bar — industry by gender (Census Industry)
C6: Horiz grouped bar — 7 social determinants with multipliers (CDC Social Needs)
C7: Grid/heatmap — 20 NAICS present vs missing (CBP)
C8: Table — 12 missing healthcare NAICS (CBP)
C9: Horiz grouped bar — 7 disability measures (CDC Disability)
C10: Infographic — worker exodus 2,880/305/924 (OnTheMap)
C11: Bar — provider counts vs needed, 3-level benchmark (CHR)
C12: Metric — preventable hosp 4,862 vs LA 3,427 vs US 2,666 (CHR)
C13: Metric — life expectancy 70 vs LA 73.3 vs US 78 (CHR)

## Cross-Validation (multiple sources, same finding)
- Obesity: CDC 42.7% ↔ CHR 46.3% ↔ both above LA 40.3%
- Broadband: FCC 68% ↔ CHR 68.3% ↔ IGS 66.1% ↔ all below LA 84.8%
- Income: Census $45,618 ↔ CHR $46,835 ↔ IGS $47,778 ↔ all below LA $58,273
- Dental crisis: CDC -13 pts ↔ CBP 6212=0 ↔ HPSA 22/26 ↔ CHR 1 dentist (10,774:1 vs US 1,360:1)
- Transit: Census 0 transit ↔ OnTheMap 90.4% leave ↔ CDC 15.1% no transport ↔ IGS travel 1/100

## Web Research (compiled)
- St. Helena Parish Hospital: 25 beds, Critical Access Hospital, appointment only, no walk-ins
- SCHS (FQHC): Started 1992, now 27+ sites across 4 parishes. CEO: Dr. Alecia Cyprian.
- Data USA ratios: PCP 5,456:1, Dentist 10,822:1, MH 1,197:1
- Parish insurance: 43.7% Medicaid, 27.6% employer
- FCC: 68% broadband, 11% cable, ISP grade C-, DCI 21/100
- USDA extreme food desert, St. Helena Farmers Market SNAP 3:1

## Commands
- `python analysis/[script].py` — Run analysis scripts
- All outputs saved to `outputs/`
