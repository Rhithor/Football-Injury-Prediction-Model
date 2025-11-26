import logging
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings

logger = logging.getLogger(__name__)


class AuthDebugMiddleware:
    """Middleware to log auth-related requests during development.

    It logs requests targeting /accounts/ paths with cookies, session key and
    the current user auth state so it's easier to debug social auth redirects.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.path.startswith('/accounts/'):
                session_key = None
                try:
                    session_key = getattr(request.session, 'session_key', None)
                except Exception:
                    # session may not exist yet
                    session_key = None

                user_obj = getattr(request, 'user', None)
                is_auth = False
                try:
                    is_auth = bool(getattr(user_obj, 'is_authenticated', False))
                except Exception:
                    is_auth = False

                # If the user has just completed the social signup process
                # we will log them out and redirect to the frontend login
                # page so they must explicitly sign in with their new
                # password (prevents auto-login after signup).
                try:
                    if getattr(request, 'session', None):
                        flag = request.session.get('just_signed_up', False)
                        if flag:
                            # clear the flag and, if user is logged in, log them out
                            try:
                                request.session.pop('just_signed_up')
                            except Exception:
                                pass
                            if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False):
                                logout(request)
                                frontend = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
                                return redirect(f"{frontend}/login")
                except Exception:
                    logger.exception('Error handling just_signed_up session flag')

                logger.debug(
                    'AUTH FLOW: %s %s user_authenticated=%s session=%s cookies=%s',
                    request.method,
                    request.path,
                    is_auth,
                    session_key,
                    dict(getattr(request, 'COOKIES', {})),
                )
        except Exception:
            # Never fail the request because of debug logging
            logger.exception('Error while logging auth flow')

        return self.get_response(request)
