Django auth remember app
========================

Add the auth_remember authentication backend to django::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'auth_remember.backend.AuthRememberBackend',
    )

Add the remember middleware in your settings, right after
AuthenticationMiddleware::

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'auth_remember.middleware.AuthRememberMiddleware',
        ...
    )


Add auth_remember to INSTALLED_APPS::

    INSTALLED_APPS = (
        'auth_remember',
    )


Set the cookie name and expire time (optional)::

    AUTH_REMEMBER_COOKIE_NAME = 'remember_token'
    AUTH_REMEMBER_COOKIE_AGE = 86400 * 28  # 4 weeks by default


Set the expire time of the session to browser close (optional)::

    SESSION_EXPIRE_AT_BROWSER_CLOSE = True


To remember a user add the following code to your authentication handler::

    from auth_remember import remember_user
    remember_user(request, user)


Use the user.is_fresh attribute to test if the user is fresh::

    {% if user.is_fresh %}
        This user session is fresh
    {% else %}
        This user session is NOT fresh
    {% endif %}

Under the hood auth_remember uses the session var ``AUTH_REMEMBER_FRESH`` to
indicate if the user session is fresh. The name of the session var can be
changed by setting the ``AUTH_REMEMBER_SESSION_KEY`` in you're settings file.


More information
----------------

See:
 - http://fishbowl.pastiche.org/2004/01/19/persistent_login_cookie_best_practice/
 - http://stackoverflow.com/questions/549/the-definitive-guide-to-forms-based-website-authentication#477579


TODOs
-----

- Introduce settings for AUTH_REMEMBER_COOKIE_DOMAIN
