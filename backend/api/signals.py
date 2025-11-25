import logging
from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def on_user_logged_in(request, user, **kwargs):
    try:
        if request and hasattr(request, 'session'):
            request.session['just_logged_in'] = True
            logger.debug('signal: user_logged_in set just_logged_in for user=%s session=%s', user.id, getattr(request.session, 'session_key', None))
    except Exception:
        logger.exception('error in on_user_logged_in')


@receiver(user_signed_up)
def on_user_signed_up(request, user, **kwargs):
    try:
        if request and hasattr(request, 'session'):
            request.session['just_signed_up'] = True
            logger.debug('signal: user_signed_up set just_signed_up for user=%s session=%s', user.id, getattr(request.session, 'session_key', None))
    except Exception:
        logger.exception('error in on_user_signed_up')
