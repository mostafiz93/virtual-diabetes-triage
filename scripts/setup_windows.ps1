# Windows one-time setup for Iteration 1
python -m venv .venv
.\.venv\Scripts\pip.exe install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt
# Train baseline
$env:MODEL_VERSION="dev"
python -m ml.train --out-dir artifacts
# Run API
.\.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8080
