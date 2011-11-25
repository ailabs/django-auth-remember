Django auth remember app
========================

Add the auth_remember authentication backend to django:

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'auth_remember.backend.RememberBackend',
    )

Add the remember middleware in your settings, right after
AuthenticationMiddleware:

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'auth_remember.middleware.RememberMeMiddleware'
        ...
    )

Set the expire time of the session to browser close (optional):

    SESSION_EXPIRE_AT_BROWSER_CLOSE = True


To remember a user add the following code to your authentication handler::

    from auth_remember.auth import set_remember_me
    remember_user(request, user)

This module uses the session var ``REMEMBER_ME_FRESH`` to indicate if the user
session is fresh.


TODOs
-----

- Module adds the private attribute _remember_me on the request to pass vars
  to the middleware. There might be a better place for this ??

- Persist remember cookies with ``expires`` and ``max-age``, the latter
  is not supported by IE 6, 7 and 8.

- Introduce settings for REMEMBER_COOKIE_NAME, REMEMBER_COOKIE_DOMAIN and
  REMEMBER_COOKIE_MAX_AGE