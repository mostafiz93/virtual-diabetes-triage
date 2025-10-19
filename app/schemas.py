from typing import Optional
from pydantic import BaseModel, Field, root_validator

FEATURES = ["age","sex","bmi","bp","s1","s2","s3","s4","s5","s6"]

class PredictRequest(BaseModel):
    age: float = Field(..., description="Normalized age feature")
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

    @root_validator
    def check_all_present(cls, values):
        for k in FEATURES:
            if not isinstance(values.get(k), (int, float)):
                raise ValueError(f"Feature '{k}' must be numeric.")
        return values

class PredictResponse(BaseModel):
    prediction: float

class HealthResponse(BaseModel):
    status: str
    model_version: str
    model_type: str
    sklearn_version: Optional[str] = None
