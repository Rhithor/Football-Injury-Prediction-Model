from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
import logging

from .ml.injury_predictor import injury_predictor


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Injury Prediction API is running'
    })


@api_view(['POST'])
def predict_injury(request):
    """Predict injury risk using the trained ML model."""
    try:
        payload = build_player_payload(request.data)
        prediction = injury_predictor.predict_risk(payload)

        response_data = {
            'injury_risk': prediction['risk_level'],
            'risk_probability': round(prediction['risk_score'], 4),
            'confidence': round(prediction['confidence'], 4),
            'key_factors': prediction['key_factors'],
            'recommendations': get_recommendations(prediction, payload),
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except ValueError as exc:
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as exc:
        return Response(
            {'error': str(exc), 'message': 'Error processing prediction request'},
            status=status.HTTP_400_BAD_REQUEST
        )


def get_recommendations(prediction: dict, data: dict) -> list:
    """Generate recommendations based on prediction and player data."""
    risk_level = prediction.get('risk_level')
    recommendations = []

    if risk_level == 'high':
        recommendations += [
            "Immediate workload reduction and individualized recovery plan.",
            "Schedule medical screening before next fixture.",
            "Limit high-intensity drills for the next 72 hours."
        ]
    elif risk_level == 'medium':
        recommendations += [
            "Increase focus on recovery protocols (sleep, nutrition).",
            "Monitor training load and reduce intensity spikes.",
            "Add additional mobility and stability sessions."
        ]
    else:
        recommendations += [
            "Maintain current training plan.",
            "Continue monitoring key wellness metrics.",
            "Plan progressive overload cautiously."
        ]

    if data['fatigue_level'] > 0.7:
        recommendations.append("Fatigue readings are high — schedule active recovery or rest day.")
    if data['recovery_time'] < 24:
        recommendations.append("Recovery time under 24h detected — increase rest before next session.")
    if data['training_load'] > 0.75:
        recommendations.append("Training load trending high — consider tapering sessions.")

    return recommendations


def build_player_payload(data: dict) -> dict:
    """Map incoming request data to the model input schema."""
    matches_played = max(1, int(data.get('matches_played', 1)))
    minutes_played = float(data.get('minutes_played', 0))

    payload = {
        'age': int(data.get('age', 25)),
        'position': data.get('position', 'midfielder'),
        'matches_played': matches_played,
        'total_minutes_played': minutes_played,
        'fatigue_level': float(data.get('fatigue_level', 0.5)),
        'training_load': float(data.get('training_load', 0.5)),
        'recovery_time': float(data.get('recovery_time', 48)),
        'fitness_score': float(data.get('fitness_score', 0.8)),
        'previous_injuries_count': int(data.get('previous_injuries', 0)),
        'weather_condition': data.get('weather_condition', 'normal')
    }
    return payload


@api_view(['GET'])
@ensure_csrf_cookie
def csrf_token(request):
    """Return a CSRF token so the frontend can include it in requests."""
    return Response({'csrfToken': get_token(request)})


@require_http_methods(["GET"])
def social_login_success(request):
    """Called after allauth / social login redirects on successful login.

    If the user is authenticated, ensure they have an auth token and
    redirect to the frontend with the token so the SPA can store it and
    continue as an authenticated user.
    """
    logger = logging.getLogger(__name__)
    frontend = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')

    # Useful debug output while reproducing the flow
    session_key = getattr(getattr(request, 'session', None), 'session_key', None)
    logger.debug('social_login_success called; user=%s authenticated=%s session=%s',
                 getattr(getattr(request, 'user', None), 'id', None),
                 getattr(getattr(request, 'user', None), 'is_authenticated', False),
                 session_key)

    # If not authenticated, the social flow probably requires the user to
    # complete the `3rdparty` signup form. Protect against accidentally
    # redirecting the user to the frontend login page at this early step —
    # instead send them to the social signup page so they can complete the
    # registration step.
    if not getattr(getattr(request, 'user', None), 'is_authenticated', False):
        logger.debug('social_login_success: user not authenticated, redirecting to social signup')
        return redirect('/accounts/3rdparty/signup/')

    # Authenticated — create or fetch API token and redirect to frontend
    token, _ = Token.objects.get_or_create(user=request.user)
    logger.debug('social_login_success: issuing token for user=%s token_id=%s', request.user.id, str(token.key)[:8])
    return redirect(f"{frontend}/#token={token.key}")

