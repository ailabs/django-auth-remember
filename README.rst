Django auth remember app
========================

Add the auth_remember authentication backend to django:

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'auth_remember.backend.AuthRememberBackend',
    )

Add the remember middleware in your settings, right after
AuthenticationMiddleware:

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'auth_remember.middleware.AuthRememberMiddleware'
        ...
    )

Set the expire time of the session to browser close (optional):

    SESSION_EXPIRE_AT_BROWSER_CLOSE = True


To remember a user add the following code to your authentication handler::

    from auth_remember import remember_user
    remember_user(request, user)

This module uses the session var ``REMEMBER_ME_FRESH`` to indicate if the user
session is fresh.


TODOs
-----

- Introduce settings for REMEMBER_COOKIE_DOMAIN 
