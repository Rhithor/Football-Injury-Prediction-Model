import logging

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
