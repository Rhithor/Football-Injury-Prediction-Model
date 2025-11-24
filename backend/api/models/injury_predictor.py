import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class InjuryPredictor:
    """
    Real ML model for football injury prediction
    Uses Random Forest with feature engineering
    Now compatible with frontend fields
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.is_trained = False
        self.model_path = Path(__file__).resolve().parent / "injury_model.pkl"
        self.weather_factor = 1.0
        
    def generate_training_data(self, n_samples=1000) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Generate realistic football player training data
        In real scenario, this would come from your database
        """
        np.random.seed(42)
        
        data = []
        
        for i in range(n_samples):
            # Player demographics
            age = np.random.randint(18, 35)
            height = np.random.normal(180, 8)
            weight = np.random.normal(75, 10)
            bmi = weight / ((height/100) ** 2)
            
            # Biometric data
            hrv = np.random.normal(65, 15)  # Heart Rate Variability
            sleep_quality = np.random.normal(7, 2)
            fatigue = np.random.normal(4, 2)
            
            # Training load
            training_load = np.random.normal(400, 150)
            session_intensity = np.random.normal(6, 2)
            match_minutes = np.random.normal(70, 25)
            
            # Injury history
            previous_injuries = np.random.randint(0, 3)
            days_since_injury = np.random.randint(0, 365)
            
            # Calculate injury risk based on realistic factors
            base_risk = 0.1
            risk_factors = 0
            
            # Real risk factors
            if hrv < 50: risk_factors += 0.2  # Low HRV
            if sleep_quality < 5: risk_factors += 0.15
            if fatigue > 6: risk_factors += 0.15
            if training_load > 550: risk_factors += 0.2
            if session_intensity > 8: risk_factors += 0.1
            if previous_injuries > 1: risk_factors += 0.1
            if days_since_injury < 30: risk_factors += 0.1
            
            injury_risk = base_risk + risk_factors
            injury_occurred = 1 if injury_risk > 0.35 else 0
            
            data.append({
                'age': age,
                'height_cm': height,
                'weight_kg': weight,
                'bmi': bmi,
                'heart_rate_variability': hrv,
                'sleep_quality': sleep_quality,
                'fatigue_level': fatigue,
                'training_load': training_load,
                'session_intensity': session_intensity,
                'match_minutes': match_minutes,
                'previous_injuries_count': previous_injuries,
                'days_since_last_injury': days_since_injury,
                'injury_occurred': injury_occurred,
                'injury_risk_score': injury_risk
            })
        
        df = pd.DataFrame(data)
        X = df.drop(['injury_occurred', 'injury_risk_score'], axis=1)
        y = df['injury_occurred']
        
        self.feature_names = X.columns.tolist()
        return X, y
    
    def train(self) -> Dict:
        """Train the Random Forest model with realistic data"""
        print("Generating training data...")
        X, y = self.generate_training_data(1500)
        
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            class_weight='balanced'
        )
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.is_trained = True
        
        # Save model using joblib - UPDATED to .pkl
        joblib.dump(self.model, self.model_path)
        print(f"✅ Model saved as '{self.model_path}'")
        
        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.3f}")
        print(f"Features: {len(self.feature_names)}")
        
        return {
            'accuracy': accuracy,
            'features': self.feature_names,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def _prepare_features(self, player_data: Dict) -> List:
        """Convert frontend fields to model features - EXACT MAPPING"""
        
        # Get position and set default physical attributes
        position = player_data['position'].lower()
        
        # Position-based height and weight estimates
        position_stats = {
            'goalkeeper': (190, 85),    # Taller, heavier
            'defender': (183, 78),      # Tall, strong
            'midfielder': (178, 72),    # Average
            'forward': (180, 75)        # Athletic
        }
        height_cm, weight_kg = position_stats.get(position, (180, 75))
        bmi = weight_kg / ((height_cm/100) ** 2)
        
        # Convert frontend 0-1 scales to realistic ranges
        # Fatigue: 0-1 → 0-10 scale
        fatigue_0_10 = player_data['fatigue_level'] * 10
        
        # Training load: 0-1 → 200-600 units (realistic training load range)
        training_load_scaled = 200 + (player_data['training_load'] * 400)
        
        # Session intensity: Derived from training load
        session_intensity = player_data['training_load'] * 10
        
        # HRV: Calculated from fitness score (higher fitness = better HRV)
        # Real HRV range: 40-100 (higher is better)
        hrv = 50 + (player_data['fitness_score'] * 30)
        
        # Sleep quality: Calculated from recovery time
        recovery_hours = player_data['recovery_time']
        if recovery_hours >= 72:    # 3+ days rest
            sleep_quality = 9.0
        elif recovery_hours >= 48:  # 2 days rest
            sleep_quality = 7.5
        elif recovery_hours >= 24:  # 1 day rest
            sleep_quality = 6.0
        else:                       # Less than 24 hours
            sleep_quality = 4.0
        
        # Match minutes: Calculate average per match
        matches = max(1, player_data['matches_played'])
        total_minutes = player_data['total_minutes_played']
        match_minutes = min(90, total_minutes / matches)
        
        # Days since last injury: Estimate from injury count
        injury_count = player_data['previous_injuries_count']
        if injury_count == 0:
            days_since_injury = 365  # No injuries in a year
        else:
            # More injuries = more recent (simplified logic)
            days_since_injury = max(30, 365 - (injury_count * 60))
        
        # Weather impact (simplified)
        weather = player_data['weather_condition'].lower()
        weather_factor = 1.0
        if 'rain' in weather or 'wet' in weather:
            weather_factor = 1.2  # Increased injury risk
        elif 'hot' in weather or 'extreme' in weather:
            weather_factor = 1.1  # Moderate increased risk
        
        # Prepare features array (must match training data order)
        features = [
            player_data['age'],          # age
            height_cm,                   # height_cm  
            weight_kg,                   # weight_kg
            bmi,                         # bmi
            hrv,                         # heart_rate_variability
            sleep_quality,               # sleep_quality
            fatigue_0_10,                # fatigue_level (0-10)
            training_load_scaled,        # training_load (scaled)
            session_intensity,           # session_intensity
            match_minutes,               # match_minutes
            injury_count,                # previous_injuries_count
            days_since_injury            # days_since_last_injury
        ]
        
        # Apply weather factor to risk calculation later
        self.weather_factor = weather_factor
        
        return features
    
    def predict_risk(self, player_data: Dict) -> Dict:
        """Predict injury risk using frontend fields"""
        if not self.is_trained:
            # Try to load saved model first
            if not self.load_model():
                raise ValueError("Model not trained and no saved model found. Call train() first.")
        
        # Convert player data to feature vector
        features = self._prepare_features(player_data)
        
        # Make prediction
        risk_probability = self.model.predict_proba([features])[0][1]
        
        # Apply weather factor to final risk
        risk_probability = min(0.95, risk_probability * self.weather_factor)
        
        # Get feature importance for explanation
        feature_importance = self._get_feature_importance(features)
        
        return {
            'risk_score': float(risk_probability),
            'risk_level': self._get_risk_level(risk_probability),
            'key_factors': feature_importance,
            'confidence': min(0.95, risk_probability * 1.2)
        }
    
    def _get_feature_importance(self, features: List) -> List[Dict]:
        """Explain which features contributed most to the prediction"""
        if not hasattr(self.model, 'feature_importances_'):
            return []
        
        importance_dict = dict(zip(self.feature_names, self.model.feature_importances_))
        feature_values = dict(zip(self.feature_names, features))
        
        # Get top 3 most important features for this prediction
        top_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        
        key_factors = []
        for feature, importance in top_features:
            key_factors.append({
                'factor_name': feature,
                'factor_impact': float(importance),
                'current_value': float(feature_values[feature]),
                'description': self._get_factor_description(feature, feature_values[feature])
            })
        
        return key_factors
    
    def _get_factor_description(self, feature: str, value: float) -> str:
        """Generate human-readable descriptions for factors"""
        descriptions = {
            'training_load': f"Training load is {'very high' if value > 500 else 'high' if value > 400 else 'moderate' if value > 300 else 'low'}",
            'sleep_quality': f"Sleep quality is {'excellent' if value > 8 else 'good' if value > 6 else 'poor'}",
            'heart_rate_variability': f"HRV indicates {'excellent' if value > 75 else 'good' if value > 65 else 'moderate' if value > 55 else 'poor'} recovery",
            'fatigue_level': f"Fatigue level is {'very high' if value > 8 else 'high' if value > 6 else 'moderate' if value > 4 else 'low'}",
            'previous_injuries_count': f"Player has {int(value)} previous injuries",
            'recovery_time': f"Recovery time is {'optimal' if value > 72 else 'good' if value > 48 else 'insufficient'}",
            'fitness_score': f"Fitness score is {'excellent' if value > 0.8 else 'good' if value > 0.6 else 'average'}",
            'age': f"Player age is {int(value)} years",
            'session_intensity': f"Session intensity is {'very high' if value > 8 else 'high' if value > 6 else 'moderate'}",
            'match_minutes': f"Average match minutes is {value:.1f}"
        }
        
        return descriptions.get(feature, f"{feature} is {value:.1f}")
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert numerical risk to category"""
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.7:
            return "medium"
        else:
            return "high"
    
    def load_model(self) -> bool:
        """Load pre-trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print(f"✅ Model loaded from '{self.model_path}'")
            return True
        return False

# Create global instance
injury_predictor = InjuryPredictor()