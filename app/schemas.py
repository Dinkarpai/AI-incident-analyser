from pydantic import BaseModel

class LogRequest(BaseModel):
    log_text: str

class PredictionResponse(BaseModel):
    log_text: str
    predicted_category: str
    predicted_severity: str
