from pathlib import Path
import json
import joblib
import subprocess
import sys


def test_training_script_runs(tmp_path: Path):
    out = tmp_path / "artifacts"
    subprocess.check_call([sys.executable, "-m", "ml.train", "--out-dir", str(out)])
    assert (out / "model.joblib").exists()
    assert (out / "metrics.json").exists()
    with open(out / "metrics.json") as f:
        m = json.load(f)
        assert "rmse" in m
    joblib.load(out / "model.joblib")
