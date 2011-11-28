from datetime import datetime, timedelta

from django.contrib.auth.models import User

from auth_remember import auth
from auth_remember import settings
from auth_remember.models import RememberToken


class RememberBackend(object):
    """Custom django authentication backend, used to authenticate via the
    remember-me cookie token

    """
    def authenticate(self, remember_token, request):
        """Return the user associated with the given token."""
        token = RememberToken.objects.get_by_string(
            token_string=remember_token)
        if not token:
            return

        # If the token is older then COOKIE_AGE then delete it and return
        max_age = datetime.now() - timedelta(seconds=settings.COOKIE_AGE)
        if token.created_initial < max_age:
            token.delete()
            return

        user = token.user

        # Create new token cookie value and delete current token
        token_string = auth.create_token_string(user, token)
        auth.preset_cookie(request, token_string)
        token.delete()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
