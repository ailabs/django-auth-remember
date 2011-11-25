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
    user = django_auth.authenticate(remember_token=token)
    if user:
        user._remember_user = True
        django_auth.login(request, user)


def remember_user(request, user):
    """Set the remember-me flag on the user.

    A token is automatically generated and stored in the user's session.
    This token is set as a cookie value by the middleware.

    """
    token = uuid.uuid4().hex
    RememberToken(token=token, user=user).save()
    request._remember_me = {'token': token}


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

