import argparse
import json
import os
from pathlib import Path
import joblib
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import sklearn
from datetime import datetime

from ml.utils import Metrics, save_json

FEATURES = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]


def get_model(model_version="v0.1"):
    """
    Returns model pipeline based on version.
    v0.1: StandardScaler + LinearRegression (baseline)
    v0.2: StandardScaler + RandomForestRegressor (improved)
    """
    if model_version.startswith("v0.2"):
        return Pipeline([
            ("scale", StandardScaler()),
            ("est", RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ))
        ])
    else:
        # v0.1 baseline
        return Pipeline([
            ("scale", StandardScaler()),
            ("est", LinearRegression())
        ])


def main(args):
    Xy = load_diabetes(as_frame=True)
    X = Xy.frame.drop(columns=["target"])
    y = Xy.frame["target"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=args.test_size, random_state=args.seed
    )

    model_version = os.getenv("MODEL_VERSION", "dev")
    pipe = get_model(model_version)
    pipe.fit(X_tr, y_tr)

    y_pred = pipe.predict(X_te)
    rmse = mean_squared_error(y_te, y_pred, squared=False)

    # High-risk classification (v0.2+): threshold at 75th percentile
    precision, recall, threshold = None, None, None
    if model_version.startswith("v0.2"):
        threshold = np.percentile(y_tr, 75)
        y_true_class = (y_te >= threshold).astype(int)
        y_pred_class = (y_pred >= threshold).astype(int)

        if y_pred_class.sum() > 0:  # avoid division by zero
            precision = precision_score(y_true_class, y_pred_class, zero_division=0)
            recall = recall_score(y_true_class, y_pred_class, zero_division=0)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipe, out_dir / "model.joblib")

    metrics = Metrics(
        rmse=rmse,
        precision=precision,
        recall=recall,
        high_risk_threshold=threshold
    ).to_dict()
    save_json(metrics, out_dir / "metrics.json")

    # Determine model type
    if model_version.startswith("v0.2"):
        model_type = "random_forest"
    else:
        model_type = "linear"

    meta = {
        "model_version": model_version,
        "model_type": model_type,
        "sklearn_version": sklearn.__version__,
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "seed": args.seed,
        "test_size": args.test_size,
        "features": FEATURES,
    }
    save_json(meta, out_dir / "model_meta.json")

    print("=== METRICS ===")
    print(json.dumps(metrics, indent=2))
    print("=== /METRICS ===")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--out-dir", type=str, default="artifacts")
    main(p.parse_args())
