from fastapi import FastAPI, UploadFile, File, HTTPException
from app.schemas import LogRequest
from app.predictor import predict_log
import pandas as pd
import os

app = FastAPI(title="AI Incident Log Analyzer")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AI Incident Log Analyzer API is running"}

@app.post("/predict")
def predict(request: LogRequest):
    return predict_log(request.log_text)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)

    if "log_text" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'log_text' column.")

    predictions = []
    for text in df["log_text"]:
        predictions.append(predict_log(str(text)))

    return {
        "filename": file.filename,
        "predictions": predictions
    }
