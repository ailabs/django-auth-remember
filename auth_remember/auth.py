import time
import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import auth as django_auth
from django.utils.http import cookie_date

from auth_remember.settings import COOKIE_AGE, COOKIE_NAME
from auth_remember.models import RememberToken


def login(request):
    """Authenticate the user via the remember token if available in the
    request cookies.

    """
    token = request.COOKIES.get(COOKIE_NAME, None)
    if not token:
        return
    user = django_auth.authenticate(remember_token=token, request=request)
    if user:
        user._remember_me_user = True
        django_auth.login(request, user)


def remember_user(request, user):
    """Set the remember-me flag on the user.

    A token is automatically generated and stored in the user's session.
    This token is set as a cookie value by the middleware.

    """
    token = create_token_object(user, None)
    preset_cookie(request, token)


def create_token_object(user, token=None):
    """Create a new token object for the given `user` and optionally based
    upon the given `token`.

    If the optional token is given then a new token is created for the
    same serie.

    """
    if token:
        serie_created = token.serie_created
        serie_token = token.serie_token
    else:
        serie_created = datetime.now()
        serie_token = uuid.uuid4().hex

    token = RememberToken(
        token=uuid.uuid4().hex,
        serie_created=serie_created,
        serie_token=serie_token,
        user=user
    )
    token.save()
    return token


def preset_cookie(request, token):
    """Create the cookie value for the token and save it on the request.

    The middleware will set the actual cookie (via `set_cookie`) on the
    response.

    """
    if token:
        request._remember_me_token = '%s:%s:%s' % (
            token.serie_token, token.user.id, token.token)
    else:
        request._remember_me_token = ''


def set_cookie(response, token):
    """Set the cookie with the remember token on the response object."""
    max_age = datetime.now() + timedelta(seconds=COOKIE_AGE)
    expires = cookie_date(time.time() + COOKIE_AGE)

    response.set_cookie(COOKIE_NAME, token,
        max_age=max_age, expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        path=settings.SESSION_COOKIE_PATH,
        secure=settings.SESSION_COOKIE_SECURE or None,
        httponly=settings.SESSION_COOKIE_HTTPONLY or None)

    return response


def delete_cookie(response):
    response.delete_cookie(COOKIE_NAME)
