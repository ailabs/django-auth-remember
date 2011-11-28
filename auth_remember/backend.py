from datetime import datetime, timedelta

from django.contrib.auth.models import User

from auth_remember import utils
from auth_remember import settings
from auth_remember.models import RememberToken


class AuthRememberBackend(object):
    """Custom django authentication backend, used to authenticate via the
    remember-me cookie token

    """
    def authenticate(self, token_string, request):
        """Return the user associated with the given token."""
        token = RememberToken.objects.get_by_string(token_string)
        if not token:
            return

        # If the token is older then COOKIE_AGE then delete it and return
        max_age = datetime.now() - timedelta(seconds=settings.COOKIE_AGE)
        if token.created_initial < max_age:
            token.delete()
            return

        user = token.user

        # Create new token cookie value and delete current token
        token_string = utils.create_token_string(user, token)
        utils.preset_cookie(request, token_string)
        token.delete()

        user._remember_me_user = True
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
