"""
Step 5: Simulate Community Hub Marketplace interventions.
Uses trained XGBoost models to predict IGS improvement across 3 scenarios.
Outputs predictions + charts for judge presentation.
"""

import pandas as pd
import numpy as np
import joblib
import os
import time
import json

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'model', 'data')
OUT = os.path.join(BASE, 'model', 'results')
os.makedirs(OUT, exist_ok=True)

# ─── Load models and data ────────────────────────────────────────────────────
log("Loading models...")
models = joblib.load(os.path.join(DATA, 'igs_models.pkl'))
scaler = joblib.load(os.path.join(DATA, 'scaler.pkl'))
features = joblib.load(os.path.join(DATA, 'features.pkl'))
log(f"Models loaded: {list(models.keys())}")

# ─── Load USA benchmark data (IGS=36 baseline) ──────────────────────────────
log("Loading USA benchmark data...")
df = pd.read_csv(os.path.join(DATA, 'igs_usa.csv'))
for col in features:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ─── Get St. Helena's LATEST scores (2025, USA benchmark) ────────────────────
sh = df[(df['Census Tract FIPS code'].astype(str) == '22091951100') & (df['Year'] == 2025)]
if len(sh) == 0:
    sh_all = df[df['Census Tract FIPS code'].astype(str) == '22091951100'].sort_values('Year')
    sh = sh_all.tail(1)
    log(f"Using year {sh['Year'].values[0]} (latest available)")

# Build feature vector — add benchmark one-hot (USA=1, State=0, Urban-Rural=0)
base_scores = []
for feat in features:
    if feat == 'bench_usa':
        base_scores.append(1)
    elif feat == 'bench_state':
        base_scores.append(0)
    elif feat == 'bench_urban_rural':
        base_scores.append(0)
    else:
        base_scores.append(sh[feat].values[0])
current_scores = np.array(base_scores, dtype=float)
log(f"\nCurrent St. Helena metric scores (2025):")
for feat, val in zip(features, current_scores):
    log(f"  {feat:>45s}: {val:5.0f}")

# ─── Predict current IGS ─────────────────────────────────────────────────────
current_scaled = scaler.transform([current_scores])
current_pred = {target: models[target].predict(current_scaled)[0] for target in models}
log(f"\nCurrent predicted scores:")
for k, v in current_pred.items():
    log(f"  {k:>12s}: {v:.1f}")

# ─── Define Hub interventions ────────────────────────────────────────────────
# Each intervention maps a feature to (conservative, moderate, optimistic) POINT increases.
# Based on what the Community Hub Marketplace would realistically provide.

INTERVENTIONS = {
    # Hub provides broadband/WiFi center
    'Internet Access Score': (5, 12, 20),
    # Hub incubates new businesses, brings vendors
    'New Businesses Score': (4, 10, 18),
    # Hub creates local jobs, reduces commuting
    'Labor Market Engagement Index Score': (3, 8, 15),
    # Hub adds commercial diversity (pharmacy, grocery, services)
    'Commercial Diversity Score': (5, 12, 20),
    # Local jobs mean shorter commutes
    'Travel Time to Work Score': (2, 5, 10),
    # More local spending at Hub businesses
    'Spending per Capita Score': (3, 8, 15),
    # Hub attracts small business loans
    'Small Business Loans Score': (3, 7, 14),
    # Minority/women-owned businesses in Hub
    'Minority/Women Owned Businesses Score': (3, 8, 15),
    # Hub jobs provide employer insurance (7.9% → higher); pharmacy improves access
    'Health Insurance Coverage Score': (5, 12, 20),
    # Income growth from Hub employment + employer benefits = effective income boost
    'Personal Income Score': (3, 8, 15),
    # Hub daycare/after-school programs
    'Early Education Enrollment Score': (2, 5, 8),
    # Reduced poverty through employment
    'Female Above Poverty Score': (2, 5, 10),
}

# ─── Run 3 scenarios ─────────────────────────────────────────────────────────
SCENARIOS = ['Conservative (Year 1)', 'Moderate (Year 3)', 'Optimistic (Year 5)']
results = []

log(f"\n{'='*70}")
log("SIMULATION RESULTS")
log(f"{'='*70}")

for i, scenario in enumerate(SCENARIOS):
    modified = current_scores.copy()

    log(f"\n  ── {scenario} ──")
    changes = {}
    for feat_name, deltas in INTERVENTIONS.items():
        idx = features.index(feat_name)
        old_val = modified[idx]
        new_val = min(old_val + deltas[i], 99)  # Cap at 99 (percentile max)
        modified[idx] = new_val
        if deltas[i] > 0:
            changes[feat_name] = {'from': old_val, 'to': new_val, 'delta': deltas[i]}
            log(f"    {feat_name:>45s}: {old_val:5.0f} → {new_val:5.0f} (+{deltas[i]})")

    # Predict new scores
    modified_scaled = scaler.transform([modified])
    predicted = {target: models[target].predict(modified_scaled)[0] for target in models}

    log(f"\n    Predicted scores:")
    for k in ['igs', 'place', 'economy', 'community']:
        old = current_pred[k]
        new = predicted[k]
        log(f"      {k:>12s}: {old:.1f} → {new:.1f}  ({new-old:+.1f})")

    results.append({
        'scenario': scenario,
        'igs': round(predicted['igs'], 1),
        'place': round(predicted['place'], 1),
        'economy': round(predicted['economy'], 1),
        'community': round(predicted['community'], 1),
        'igs_change': round(predicted['igs'] - current_pred['igs'], 1),
        'changes': changes,
    })

# ─── Add current baseline ────────────────────────────────────────────────────
baseline = {
    'scenario': 'Current (2025)',
    'igs': round(current_pred['igs'], 1),
    'place': round(current_pred['place'], 1),
    'economy': round(current_pred['economy'], 1),
    'community': round(current_pred['community'], 1),
    'igs_change': 0,
}

# ─── Summary table ───────────────────────────────────────────────────────────
log(f"\n{'='*70}")
log("SUMMARY")
log(f"{'='*70}")
log(f"  {'Scenario':<25s} {'IGS':>6s} {'Place':>6s} {'Econ':>6s} {'Comm':>6s} {'ΔIGS':>6s}")
log(f"  {'-'*55}")
log(f"  {'Current (2025)':<25s} {baseline['igs']:6.1f} {baseline['place']:6.1f} {baseline['economy']:6.1f} {baseline['community']:6.1f}   {'—':>4s}")
for r in results:
    log(f"  {r['scenario']:<25s} {r['igs']:6.1f} {r['place']:6.1f} {r['economy']:6.1f} {r['community']:6.1f} {r['igs_change']:+6.1f}")

# ─── Find "twin" tracts ──────────────────────────────────────────────────────
# Tracts that currently have the scores we're predicting for moderate scenario
log(f"\n{'='*70}")
log("TWIN TRACTS — Real communities matching Moderate scenario")
log(f"{'='*70}")

moderate_igs = results[1]['igs']
df['Inclusive Growth Score'] = pd.to_numeric(df['Inclusive Growth Score'], errors='coerce')

# Find rural tracts with similar IGS to our moderate prediction
twins = df[
    (df['Year'] == 2025) &
    (df['Inclusive Growth Score'].between(moderate_igs - 2, moderate_igs + 2)) &
    (df['State'] == 'Louisiana')
].head(10)

if len(twins) > 0:
    for _, t in twins.iterrows():
        log(f"  {t['Census Tract FIPS code']} | {t['County']}, {t['State']} | IGS={t['Inclusive Growth Score']}")
else:
    log("  No Louisiana twins found in range, checking nationally...")
    twins = df[
        (df['Year'] == 2025) &
        (df['Inclusive Growth Score'].between(moderate_igs - 2, moderate_igs + 2))
    ].sample(min(10, len(df)), random_state=42).head(10)
    for _, t in twins.iterrows():
        log(f"  {t['Census Tract FIPS code']} | {t['County']}, {t['State']} | IGS={t['Inclusive Growth Score']}")

# ─── Save results ────────────────────────────────────────────────────────────
all_results = [baseline] + results
results_df = pd.DataFrame(all_results)
results_df.to_csv(os.path.join(OUT, 'simulation_results.csv'), index=False)

# Save detailed results as JSON
def make_serializable(obj):
    if isinstance(obj, (np.floating, np.float32, np.float64)):
        return round(float(obj), 2)
    if isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    return obj

with open(os.path.join(OUT, 'simulation_details.json'), 'w') as f:
    json.dump(make_serializable({
        'baseline': baseline,
        'scenarios': results,
        'current_scores': {feat: round(float(val), 1) for feat, val in zip(features, current_scores)},
        'feature_importance': features,
        'model_type': 'XGBoost',
        'training_r2': 0.9883,
        'training_mae': 0.75,
    }), f, indent=2)

log(f"\nResults saved to {OUT}")
log("Files: simulation_results.csv, simulation_details.json")
