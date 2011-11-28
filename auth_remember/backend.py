from django.contrib.auth.models import User

from auth_remember import auth
from auth_remember.models import RememberToken


class RememberBackend(object):
    """Custom django authentication backend, used to authenticate via the
    remember-me cookie token

    """
    def authenticate(self, remember_token, request):
        """Return the user associated with the given token.

        If the token is invalid (no valid user found) then delete all
        tokens associated with the token serie.

        """
        try:
            serie_token, user_id, token = remember_token.split(':')
        except ValueError:
            auth.preset_cookie(request, '')
            return

        try:
            token = RememberToken.objects.select_related('user').get(
                token=token,
                serie_token=serie_token,
                user=user_id)

            # Create new token cookie value
            new_token = auth.create_token_object(token.user, token)
            token.delete()
            auth.preset_cookie(request, new_token)

            return token.user
        except RememberToken.DoesNotExist:

            # We might be dealing with a stolen cookie, delete all the
            # remember me information from the user.
            RememberToken.objects.filter(
                user=user_id, serie_token=serie_token).delete()
            auth.preset_cookie(request, '')

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
