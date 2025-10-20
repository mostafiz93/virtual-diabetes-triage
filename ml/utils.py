from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class Metrics:
    rmse: float
    precision: Optional[float] = None
    recall: Optional[float] = None
    high_risk_threshold: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"rmse": self.rmse}
        if self.precision is not None:
            result["precision"] = self.precision
        if self.recall is not None:
            result["recall"] = self.recall
        if self.high_risk_threshold is not None:
            result["high_risk_threshold"] = self.high_risk_threshold
        return result


def save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
