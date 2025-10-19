# Virtual Diabetes Clinic Triage — Iteration 1 (v0.1)

Predicts short-term progression (continuous risk score) using scikit-learn Diabetes dataset.
This is **Iteration 1 (baseline)**: `StandardScaler + LinearRegression`.

## API
- `GET /health` → `{ "status":"ok", "model_version":"v0.1", "model_type":"linear", "sklearn_version":"..." }`
- `POST /predict` → `{ "prediction": <float> }`

**Sample payload**
```json
{ "age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03, "s1": -0.02, "s2": 0.03, "s3": -0.02, "s4": 0.02, "s5": 0.02, "s6": -0.001 }
```

## Windows quick start (local)
```powershell
# one-time
.\scripts\setup_windows.ps1
# then in another terminal
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict -H "content-type: application/json" -d '{"age":0.02,"sex":-0.044,"bmi":0.06,"bp":-0.03,"s1":-0.02,"s2":0.03,"s3":-0.02,"s4":0.02,"s5":0.02,"s6":-0.001}'
```

## Docker
```bash
# build after local training
docker build -t ghcr.io/israt-urme/virtual-diabetes-triage:dev .
docker run -p 8080:8080 ghcr.io/israt-urme/virtual-diabetes-triage:dev
```

## CI/CD
- CI runs on push/PR: lint, tests, quick training, upload artifacts.
- Tag `v0.1` to publish release + image to `ghcr.io/israt-urme/virtual-diabetes-triage:v0.1`.

## Reproducibility
- Python 3.11, pinned deps, fixed seed (42)
- Deterministic train/test split; artifacts baked into image

## Submission
- Repo: https://github.com/israt-urme/virtual-diabetes-triage
- Images: ghcr.io/israt-urme/virtual-diabetes-triage:v0.1
