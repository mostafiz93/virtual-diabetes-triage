from dataclasses import dataclass
from typing import Dict, Any
import json
from pathlib import Path


@dataclass
class Metrics:
    rmse: float

    def to_dict(self) -> Dict[str, Any]:
        return {"rmse": self.rmse}


def save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
