import logging
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

logger = logging.getLogger(__name__)


class DebugSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Adapter that logs important social login/signup events for debugging.

    Install by setting `SOCIALACCOUNT_ADAPTER = 'api.adapters.DebugSocialAccountAdapter'`
    in Django settings (enabled only for local development).
    """

    def pre_social_login(self, request, sociallogin):
        # log pre-login state
        try:
            logger.debug('adapter.pre_social_login: request.session=%s user=%s sociallogin=%s',
                         getattr(getattr(request, 'session', None), 'session_key', None),
                         getattr(getattr(request, 'user', None), 'is_authenticated', None),
                         f'provider={getattr(sociallogin.provider, "id", None)} account={getattr(getattr(sociallogin.account, "extra_data", {}), "get", lambda k, d=None: d) }')
        except Exception:
            logger.exception('error logging pre_social_login')
        return super().pre_social_login(request, sociallogin)

    def save_user(self, request, sociallogin, form=None):
        # log save_user state
        try:
            logger.debug('adapter.save_user: session=%s sociallogin.has_account=%s sociallogin.user=%s',
                         getattr(getattr(request, 'session', None), 'session_key', None),
                         bool(getattr(sociallogin, 'account', None)),
                         getattr(getattr(sociallogin, 'user', None), 'email', None))
        except Exception:
            logger.exception('error logging save_user')
        return super().save_user(request, sociallogin, form)

    def populate_user(self, request, sociallogin, data):
        """Populate a new user from the provider data before signup."""
        user = super().populate_user(request, sociallogin, data)

        extra = getattr(sociallogin.account, 'extra_data', {}) or {}

        # Prefer explicit provider supplied email fields
        email = extra.get('email') or data.get('email') or getattr(user, 'email', None)
        if email:
            user.email = email

        # extract first_name / last_name from common oauth fields
        first = extra.get('given_name') or extra.get('first_name')
        last = extra.get('family_name') or extra.get('last_name')
        name = extra.get('name') or data.get('name')
        if not (first or last) and name:
            # If only 'name' is present try a naive split
            parts = name.split()
            if parts:
                first = parts[0]
                if len(parts) > 1:
                    last = ' '.join(parts[1:])

        if first:
            try:
                user.first_name = first
            except Exception:
                pass
        if last:
            try:
                user.last_name = last
            except Exception:
                pass

        # create a sensible default username if none is present
        if not getattr(user, 'username', None):
            if email:
                base = email.split('@', 1)[0]
            else:
                base = (name or 'user').replace(' ', '').lower()
            # Keep username short for common field limits
            user.username = base[:30]

        logger.debug('adapter.populate_user: populated user %s from extra_data %s', getattr(user, 'email', None), extra)
        return user
