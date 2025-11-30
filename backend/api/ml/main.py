from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import joblib
import numpy as np
from injury_predictor import injury_predictor

app = FastAPI(title="Football Injury Predictor API")

# Global model reference
model = None
feature_names = None

@app.on_event("startup")
async def load_model():
    global model, feature_names
    try:
        if not injury_predictor.is_trained:
            injury_predictor.load_model()
        model = injury_predictor.model
        feature_names = injury_predictor.feature_names
        print("Model ready!")
    except Exception as e:
        print(f"❌ Load error: {e}")

class PlayerData(BaseModel):
    age: float
    position: str
    fatigue_level: float
    training_load: float
    fitness_score: float
    recovery_time: float
    previous_injuries_count: int
    matches_played: int
    total_minutes_played: float
    weather_condition: str

@app.get("/")
def root():
    return {"message": "Football Injury Predictor API - Ready!"}

@app.post("/predict")
def predict_injury_risk(player_data: PlayerData) -> Dict[str, Any]:
    global model
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Use YOUR exact _prepare_features method
        features = injury_predictor._prepare_features(player_data.dict())
        
        # DIRECT predict_proba call (bypasses validation bug)
        try:
            risk_proba = model.predict_proba([features])[0][1]
        except Exception as predict_error:
            # FALLBACK: Use predict() if proba fails
            risk_binary = model.predict([features])[0]
            risk_proba = float(risk_binary)
            print(f"Used predict() fallback: {predict_error}")
        
        # Manual weather adjustment (from your code)
        weather_factor = 1.0
        if 'rain' in player_data.weather_condition.lower():
            weather_factor = 1.2
        risk_score = min(0.95, risk_proba * weather_factor)
        
        return {
            "success": True,
            "risk_score": float(risk_score),
            "risk_level": "high" if risk_score > 0.7 else "medium" if risk_score > 0.3 else "low",
            "player_data": player_data.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
