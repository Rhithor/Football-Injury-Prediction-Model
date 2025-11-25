import logging
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

logger = logging.getLogger(__name__)


class DebugSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Adapter that logs important social login/signup events for debugging.

    Install by setting `SOCIALACCOUNT_ADAPTER = 'api.adapters.DebugSocialAccountAdapter'`
    in Django settings (enabled only for local development).
    """

    def pre_social_login(self, request, sociallogin):
        # Called after a successful provider authentication but before the
        # login is processed. We'll log the sociallogin object and session info
        try:
            logger.debug('adapter.pre_social_login: request.session=%s user=%s sociallogin=%s',
                         getattr(getattr(request, 'session', None), 'session_key', None),
                         getattr(getattr(request, 'user', None), 'is_authenticated', None),
                         f'provider={getattr(sociallogin.provider, "id", None)} account={getattr(getattr(sociallogin.account, "extra_data", {}), "get", lambda k, d=None: d) }')
        except Exception:
            logger.exception('error logging pre_social_login')
        return super().pre_social_login(request, sociallogin)

    def save_user(self, request, sociallogin, form=None):
        # Called when creating a new user from sociallogin.
        # Log the sociallogin state before saving.
        try:
            logger.debug('adapter.save_user: session=%s sociallogin.has_account=%s sociallogin.user=%s',
                         getattr(getattr(request, 'session', None), 'session_key', None),
                         bool(getattr(sociallogin, 'account', None)),
                         getattr(getattr(sociallogin, 'user', None), 'email', None))
        except Exception:
            logger.exception('error logging save_user')
        return super().save_user(request, sociallogin, form)
