import argparse
import json
import os
from pathlib import Path
import joblib
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import sklearn
from datetime import datetime

from ml.utils import Metrics, save_json

FEATURES = ["age","sex","bmi","bp","s1","s2","s3","s4","s5","s6"]

def get_model():
    return Pipeline([
        ("scale", StandardScaler()),
        ("est", LinearRegression())
    ])

def main(args):
    rng = np.random.RandomState(args.seed)
    Xy = load_diabetes(as_frame=True)
    X = Xy.frame.drop(columns=["target"])
    y = Xy.frame["target"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=args.test_size, random_state=args.seed
    )

    pipe = get_model()
    pipe.fit(X_tr, y_tr)

    y_pred = pipe.predict(X_te)
    rmse = mean_squared_error(y_te, y_pred, squared=False)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipe, out_dir / "model.joblib")

    metrics = Metrics(rmse=rmse).to_dict()
    save_json(metrics, out_dir / "metrics.json")

    meta = {
        "model_version": os.getenv("MODEL_VERSION", "dev"),
        "model_type": "linear",
        "sklearn_version": sklearn.__version__,
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "seed": args.seed,
        "test_size": args.test_size,
        "features": FEATURES,
    }
    save_json(meta, out_dir / "model_meta.json")

    print("=== METRICS ===")
    print(json.dumps(metrics))
    print("=== /METRICS ===")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--out-dir", type=str, default="artifacts")
    main(p.parse_args())
