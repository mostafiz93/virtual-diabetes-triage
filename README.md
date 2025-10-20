# Virtual Diabetes Clinic Triage — ML Service

Predicts short-term diabetes progression risk (continuous score + high-risk classification) using scikit-learn Diabetes dataset.

**Current Version:** v0.2 (RandomForest with high-risk triage)  
**Previous Version:** v0.1 (Linear baseline)

## API

- `GET /health` → `{ "status":"ok", "model_version":"v0.2", "model_type":"random_forest", "sklearn_version":"..." }`
- `POST /predict` → `{ "prediction": <float> }`

## Model Versions

### v0.2 (Current) - RandomForest + High-Risk Triage

- **Model**: `StandardScaler + RandomForestRegressor`
- **RMSE**: ~48-50 (8-11% improvement over v0.1)
- **New**: Precision & Recall metrics for high-risk classification (75th percentile threshold)
- **Use case**: Better non-linear modeling + triage flag for urgent follow-ups

### v0.1 - Linear Baseline

- **Model**: `StandardScaler + LinearRegression`
- **RMSE**: 53.85
- **Basic regression**: Continuous risk score only

**Sample payload**

```json
{
	"age": 0.02,
	"sex": -0.044,
	"bmi": 0.06,
	"bp": -0.03,
	"s1": -0.02,
	"s2": 0.03,
	"s3": -0.02,
	"s4": 0.02,
	"s5": 0.02,
	"s6": -0.001
}
```

## Run in Docker Container

```bash
# Pull and run the latest release
docker pull ghcr.io/mostafiz93/virtual-diabetes-triage:v0.2
docker run -p 8080:8080 ghcr.io/mostafiz93/virtual-diabetes-triage:v0.2

# Or build locally after training
docker build -t ghcr.io/mostafiz93/virtual-diabetes-triage:dev .
docker run -p 8080:8080 ghcr.io/mostafiz93/virtual-diabetes-triage:dev
```

## Check results in local environemnt

```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict -H "content-type: application/json" -d '{"age":0.02,"sex":-0.044,"bmi":0.06,"bp":-0.03,"s1":-0.02,"s2":0.03,"s3":-0.02,"s4":0.02,"s5":0.02,"s6":-0.001}'
```

## CI/CD

- **CI** runs on push/PR: lint, tests, quick training, upload artifacts.
- **Release**: Tag `v0.x` to publish release + image to `ghcr.io/mostafiz93/virtual-diabetes-triage:v0.x`
  - Available images: `:v0.1` (linear baseline), `:v0.2` (RandomForest)

## Quick Links

- Repo: https://github.com/mostafiz93/virtual-diabetes-triage
- Images:
  - `ghcr.io/mostafiz93/virtual-diabetes-triage:v0.1` (Linear baseline)
  - `ghcr.io/mostafiz93/virtual-diabetes-triage:v0.2` (RandomForest + high-risk triage)
