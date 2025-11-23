from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from django.conf import settings


# Placeholder model - replace with your trained model
model = None


def load_model():
    """Load the trained model if it exists, otherwise create a placeholder"""
    global model
    model_path = os.path.join(settings.BASE_DIR, 'api', 'models', 'injury_model.pkl')
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        # Placeholder model for development
        # Replace this with your actual trained model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Train on dummy data (replace with actual training)
        X_dummy = np.random.rand(100, 10)
        y_dummy = np.random.randint(0, 2, 100)
        model.fit(X_dummy, y_dummy)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Injury Prediction API is running'
    })


@api_view(['POST'])
def predict_injury(request):
    """
    Predict injury risk based on player data
    
    Expected input format:
    {
        "age": 25,
        "matches_played": 30,
        "minutes_played": 2500,
        "previous_injuries": 2,
        "fatigue_level": 0.6,
        "training_load": 0.7,
        "recovery_time": 48,
        "position": "midfielder",
        "fitness_score": 0.85,
        "weather_condition": "normal"
    }
    """
    global model
    
    if model is None:
        load_model()
    
    try:
        data = request.data
        
        # Extract features (adjust based on your model's requirements)
        features = [
            data.get('age', 25),
            data.get('matches_played', 0),
            data.get('minutes_played', 0),
            data.get('previous_injuries', 0),
            data.get('fatigue_level', 0.5),
            data.get('training_load', 0.5),
            data.get('recovery_time', 48),
            data.get('fitness_score', 0.8),
        ]
        
        # Convert to numpy array and reshape for prediction
        features_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        # Return response
        return Response({
            'injury_risk': 'high' if prediction == 1 else 'low',
            'risk_probability': float(probability[1]) if len(probability) > 1 else float(probability[0]),
            'recommendations': get_recommendations(prediction, data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Error processing prediction request'
        }, status=status.HTTP_400_BAD_REQUEST)


def get_recommendations(prediction, data):
    """Generate recommendations based on prediction"""
    recommendations = []
    
    if prediction == 1:  # High risk
        recommendations.append("Consider reducing training load")
        recommendations.append("Ensure adequate recovery time")
        recommendations.append("Monitor player closely during matches")
    else:  # Low risk
        recommendations.append("Player is in good condition")
        recommendations.append("Maintain current training regimen")
    
    if data.get('fatigue_level', 0) > 0.7:
        recommendations.append("High fatigue detected - consider rest")
    
    if data.get('recovery_time', 48) < 24:
        recommendations.append("Insufficient recovery time - risk of injury increased")
    
    return recommendations

