import json
import os
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np

MODEL_DIR = Path(os.getenv("MODEL_DIR", "/opt/model"))
MODEL_PATH = MODEL_DIR / "model.joblib"
META_PATH = MODEL_DIR / "model_meta.json"

class ModelService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        self.pipe = joblib.load(MODEL_PATH)

        if META_PATH.exists():
            with open(META_PATH, "r") as f:
                self.meta = json.load(f)
        else:
            self.meta = {
                "model_version": os.getenv("MODEL_VERSION", "unknown"),
                "model_type": "unknown",
                "sklearn_version": None
            }

    def predict(self, x_ordered: np.ndarray) -> float:
        yhat = self.pipe.predict(x_ordered.reshape(1, -1)).item()
        return float(yhat)

    def health(self) -> Tuple[str, str, str, str]:
        return (
            "ok",
            self.meta.get("model_version", "unknown"),
            self.meta.get("model_type", "unknown"),
            self.meta.get("sklearn_version", None),
        )
