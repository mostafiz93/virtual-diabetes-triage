from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.schemas import PredictRequest, PredictResponse, HealthResponse, FEATURES
from app.model import ModelService
import numpy as np
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Virtual Diabetes Clinic Triage - Progression Scorer")
_service = ModelService()

@app.get("/health", response_model=HealthResponse)
def health():
    status, ver, model_type, skl_ver = _service.health()
    return {"status": status, "model_version": ver, "model_type": model_type, "sklearn_version": skl_ver}

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    try:
        x = np.array([getattr(payload, f) for f in FEATURES], dtype=float)
        pred = _service.predict(x)
        return {"prediction": pred}
    except Exception as e:
        logger.exception("Prediction error")
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc)})
