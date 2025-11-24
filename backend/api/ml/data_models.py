from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date

class PlayerData(BaseModel):
    player_id: str = Field(..., description="Unique player identifier")
    age: int = Field(..., ge=16, le=45, description="Player age")
    height_cm: float = Field(..., ge=150, le=220, description="Height in cm")
    weight_kg: float = Field(..., ge=50, le=120, description="Weight in kg")
    position: str = Field(..., description="Playing position")
    
    # Biometric data
    heart_rate_variability: Optional[float] = Field(None, description="HRV score")
    sleep_quality: Optional[float] = Field(None, ge=0, le=10, description="Sleep quality 0-10")
    fatigue_level: Optional[float] = Field(None, ge=0, le=10, description="Fatigue level 0-10")
    
    # Training data
    training_load: Optional[float] = Field(None, description="Recent training load")
    session_intensity: Optional[float] = Field(None, ge=0, le=10, description="Session intensity 0-10")
    match_minutes: Optional[float] = Field(None, description="Minutes played in last match")
    
    # Historical data
    previous_injuries: List[str] = Field(default_factory=list)
    days_since_last_injury: Optional[int] = Field(None, description="Days since last injury")

class PredictionRequest(BaseModel):
    player_data: PlayerData
    analysis_type: str = Field(default="full", description="Type of analysis: 'quick' or 'full'")

class RiskFactor(BaseModel):
    factor_name: str
    factor_impact: float
    description: str

class PredictionResponse(BaseModel):
    risk_score: float = Field(..., ge=0, le=1, description="Injury risk score 0-1")
    risk_level: str = Field(..., description="low/medium/high")
    confidence: float = Field(..., ge=0, le=1, description="Model confidence")
    key_risk_factors: List[RiskFactor]
    recommendations: List[str]
    similar_players_analysis: Optional[List[Dict]] = None