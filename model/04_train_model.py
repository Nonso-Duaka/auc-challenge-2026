"""
Step 4: Train XGBoost on REAL IGS data.
Combines all 3 benchmarks (USA, State, Urban-Rural) with benchmark as a feature.
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
import time
import warnings
warnings.filterwarnings('ignore')

LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output.log')
_logfh = open(LOGFILE, 'w')

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    _logfh.write(line + '\n')
    _logfh.flush()

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'model', 'data')

# ─── Load all 3 benchmark datasets ───────────────────────────────────────────
t0 = time.time()
dfs = []
for label, filename in [('usa', 'igs_usa.csv'), ('state', 'igs_state.csv'), ('urban_rural', 'igs_urban_rural.csv')]:
    log(f"Loading {label}...")
    d = pd.read_csv(os.path.join(DATA, filename))
    d['benchmark'] = label
    dfs.append(d)
    log(f"  {len(d):,} rows")

df = pd.concat(dfs, ignore_index=True)
log(f"Combined: {len(df):,} rows in {time.time()-t0:.1f}s")

# ─── Features: 18 metric scores + benchmark one-hot ──────────────────────────
SCORE_FEATURES = [
    'Net Occupancy Score',
    'Residential Real Estate Value Score',
    'Acres of Park Land Score',
    'Affordable Housing Score',
    'Internet Access Score',
    'Travel Time to Work Score',
    'New Businesses Score',
    'Spend Growth Score',
    'Small Business Loans Score',
    'Minority/Women Owned Businesses Score',
    'Labor Market Engagement Index Score',
    'Commercial Diversity Score',
    'Personal Income Score',
    'Spending per Capita Score',
    'Female Above Poverty Score',
    'Gini Coefficient Score',
    'Early Education Enrollment Score',
    'Health Insurance Coverage Score',
]

df['bench_usa'] = (df['benchmark'] == 'usa').astype(int)
df['bench_state'] = (df['benchmark'] == 'state').astype(int)
df['bench_urban_rural'] = (df['benchmark'] == 'urban_rural').astype(int)

ALL_FEATURES = SCORE_FEATURES + ['bench_usa', 'bench_state', 'bench_urban_rural']

TARGETS = {
    'igs': 'Inclusive Growth Score',
    'place': 'Place',
    'economy': 'Economy',
    'community': 'Community',
}

# ─── Clean data ──────────────────────────────────────────────────────────────
log("Cleaning data...")
for col in SCORE_FEATURES + list(TARGETS.values()):
    df[col] = pd.to_numeric(df[col], errors='coerce')

clean = df.dropna(subset=SCORE_FEATURES + list(TARGETS.values())).copy().reset_index(drop=True)
log(f"Clean rows: {len(clean):,} ({len(clean)/len(df)*100:.0f}% of total)")
log(f"  By benchmark: {clean['benchmark'].value_counts().to_dict()}")

X = clean[ALL_FEATURES].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
log("Features scaled.")

# ─── Train/test split ────────────────────────────────────────────────────────
X_train, X_test, y_idx_train, y_idx_test = train_test_split(
    X_scaled, np.arange(len(clean)), test_size=0.2, random_state=42
)
log(f"Split: {len(X_train):,} train / {len(X_test):,} test")

# ─── Train XGBoost for each target ───────────────────────────────────────────
log("")
log("=" * 70)
log("TRAINING XGBoost")
log("=" * 70)

models = {}

for target_key, target_col in TARGETS.items():
    y = clean[target_col].values
    y_train, y_test = y[y_idx_train], y[y_idx_test]

    log(f"\n  ── {target_key.upper()} ({target_col}) ──")
    t1 = time.time()
    log(f"    Training on {len(X_train):,} rows...")

    model = xgb.XGBRegressor(
        n_estimators=300, max_depth=6, learning_rate=0.1,
        subsample=0.8, random_state=42, verbosity=0, n_jobs=-1,
    )
    model.fit(X_train, y_train)
    elapsed = time.time() - t1

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    log(f"    R²={r2:.4f}  MAE={mae:.2f}  ({elapsed:.1f}s)")

    # Retrain on full data
    log(f"    Retraining on full dataset ({len(X_scaled):,} rows)...")
    t1 = time.time()
    model.fit(X_scaled, y)
    log(f"    Done ({time.time()-t1:.1f}s)")

    models[target_key] = model

# ─── Feature importance ──────────────────────────────────────────────────────
log("")
log("=" * 70)
log("FEATURE IMPORTANCE — IGS Score")
log("=" * 70)

importances = list(zip(ALL_FEATURES, models['igs'].feature_importances_))
importances.sort(key=lambda x: x[1], reverse=True)
max_imp = max(i[1] for i in importances)
for feat, imp in importances:
    bar = '█' * int(imp / max_imp * 30)
    log(f"  {feat:>45s}: {imp:.4f} {bar}")

# ─── Validate on St. Helena (USA benchmark) ──────────────────────────────────
log("")
log("=" * 70)
log("VALIDATION — St. Helena Parish (USA benchmark)")
log("=" * 70)

sh = clean[(clean['Census Tract FIPS code'].astype(str) == '22091951100') & (clean['benchmark'] == 'usa')]
if len(sh) > 0:
    for _, row in sh.iterrows():
        year = int(row['Year'])
        x_row = scaler.transform([row[ALL_FEATURES].values])
        pred_igs = models['igs'].predict(x_row)[0]
        actual_igs = row['Inclusive Growth Score']
        log(f"  {year}: actual={actual_igs:.0f}  predicted={pred_igs:.1f}  diff={pred_igs-actual_igs:+.1f}")
else:
    log("  St. Helena tract not found!")

# ─── Save ─────────────────────────────────────────────────────────────────────
log("")
log("Saving models...")
joblib.dump(models, os.path.join(DATA, 'igs_models.pkl'))
joblib.dump(scaler, os.path.join(DATA, 'scaler.pkl'))
joblib.dump(ALL_FEATURES, os.path.join(DATA, 'features.pkl'))

total = time.time() - t0
log(f"\nDone! Total time: {total:.0f}s ({total/60:.1f}min)")
log(f"Saved: igs_models.pkl, scaler.pkl, features.pkl")
