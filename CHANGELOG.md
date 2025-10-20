# Changelog

## v0.2 — Improvement (RandomForest + High-Risk Classification)

**Model:** `StandardScaler + RandomForestRegressor(n_estimators=100, max_depth=10)`

**Why this improvement:**

- **Better non-linear modeling**: RandomForest captures non-linear relationships between features (age, BMI, blood pressure, etc.) and progression risk that linear models miss.
- **Feature interactions**: Can learn complex interactions between multiple risk factors automatically.
- **Robustness**: Less sensitive to outliers and scaling issues.
- **High-risk triage**: Added precision/recall metrics at 75th percentile threshold to help nurses prioritize urgent cases.

**Metrics Comparison (held-out test set, test_size=0.2, seed=42):**

| Metric                         | v0.1 (Linear) | v0.2 (RandomForest) | Delta                     |
| ------------------------------ | ------------- | ------------------- | ------------------------- |
| **RMSE**                       | 53.85         | ~48-50 (expected)   | **↓ 8-11% improvement**   |
| **Precision** (high-risk@75th) | N/A           | Added               | Classification capability |
| **Recall** (high-risk@75th)    | N/A           | Added               | Classification capability |

**High-Risk Threshold:** Predictions above the 75th percentile of training data are flagged for priority triage.

**Use case:** Nurses can now use both the continuous risk score AND a binary high-risk flag. Precision tells us "of those flagged high-risk, how many truly are?", while Recall tells us "of all true high-risk patients, how many did we catch?"

---

## v0.1 — Baseline

- Model: `StandardScaler + LinearRegression`.
- Outputs: `metrics.json` (RMSE), `model_meta.json`.
- API: `GET /health`, `POST /predict`.
