from django.contrib import auth as django_auth
from django.contrib.auth import signals
from django.dispatch import receiver

from auth_remember import utils
from auth_remember.settings import COOKIE_NAME, SESSION_KEY


class AuthRememberMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            request.user.is_fresh = request.session.get(SESSION_KEY, False)
            return

        request.user.is_fresh = False

        token = request.COOKIES.get(COOKIE_NAME, None)
        if not token:
            return
        user = django_auth.authenticate(token_string=token, request=request)
        if user:
            user._auth_remember_user = True
            django_auth.login(request, user)

    def process_response(self, request, response):
        auth_remember_token = getattr(request, '_auth_remember_token', None)

        if auth_remember_token is not None:
            if auth_remember_token:
                utils.set_cookie(response, auth_remember_token)
            else:
                utils.delete_cookie(response)
        return response


@receiver(signals.user_logged_in)
def set_user_is_fresh(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']
    user.is_fresh = not getattr(user, '_auth_remember_user', False)
    request.session[SESSION_KEY] = user.is_fresh


@receiver(signals.user_logged_out)
def remove_auth_remember(sender, **kwargs):
    utils.preset_cookie(kwargs['request'], '')
