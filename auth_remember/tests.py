import time

from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory


class TokenCreationTest(TestCase):
    def setUp(self):
        self.user = User(username='test_user')
        self.user.save()

    def test_create_token_string(self):
        from auth_remember.utils import create_token_string

        value = create_token_string(self.user)
        self.assertTrue(value.startswith('%d:' % self.user.id))

    def test_get_by_token_string(self):
        from auth_remember.models import RememberToken
        from auth_remember.utils import create_token_string

        value = create_token_string(self.user)
        token = RememberToken.objects.get_by_string(value)

        self.assertEqual(token.user, self.user)

    def test_create_token_string_token_arg(self):
        from auth_remember.models import RememberToken
        from auth_remember.utils import create_token_string

        value = create_token_string(self.user)
        token = RememberToken.objects.get_by_string(value)

        time.sleep(0.1)
        new_value = create_token_string(self.user, token)
        new_token = RememberToken.objects.get_by_string(new_value)
        self.assertEqual(new_token.created_initial, token.created)
        self.assertTrue(new_token.created > token.created)


class AuthTest(TestCase):
    def setUp(self):
        self.user = User(username='test_user')
        self.user.set_password('secret')
        self.user.save()
        self.factory = RequestFactory()

    def test_auth_backend(self):
        from auth_remember import middleware  # Register signals
        from auth_remember.utils import create_token_string

        value = create_token_string(self.user)

        request = self.factory.get('/')
        SessionMiddleware().process_request(request)
        user = auth.authenticate(token_string=value, request=request)
        auth.login(request, user)

        self.assertEqual(user, self.user)
        self.assertFalse(user.is_fresh)

    def test_auth_backend_fresh(self):
        from auth_remember import middleware  # Register signals

        request = self.factory.get('/')
        SessionMiddleware().process_request(request)
        user = auth.authenticate(username='test_user', password='secret')
        auth.login(request, user)
        self.assertTrue(user.is_fresh)

    def test_middleware_logout(self):
        from auth_remember import middleware  # Register signals
        from auth_remember.settings import COOKIE_NAME

        request = self.factory.get('/')
        response = HttpResponse("Test response")

        SessionMiddleware().process_request(request)
        user = auth.authenticate(username='test_user', password='secret')
        auth.login(request, user)
        self.assertTrue(user.is_fresh)

        auth.logout(request)
        middleware.AuthRememberMiddleware().process_response(request, response)
        self.assertEqual(response.cookies[COOKIE_NAME].value, '')

    def test_middleware_set_freshness(self):
        from auth_remember.middleware import AuthRememberMiddleware
        from auth_remember.settings import SESSION_KEY

        request = self.factory.get('/')
        request.user = self.user

        SessionMiddleware().process_request(request)
        request.session[SESSION_KEY] = True

        AuthRememberMiddleware().process_request(request)
        self.assertEqual(request.user, self.user)
        self.assertTrue(request.user.is_fresh)

    def test_middleware_update_token(self):
        from auth_remember.middleware import AuthRememberMiddleware
        from auth_remember.models import RememberToken
        from auth_remember.settings import COOKIE_NAME
        from auth_remember.utils import create_token_string

        request = self.factory.get('/')
        request.user = AnonymousUser()

        value = create_token_string(self.user)
        request.COOKIES[COOKIE_NAME] = value

        SessionMiddleware().process_request(request)
        AuthRememberMiddleware().process_request(request)
        self.assertEqual(request.user, self.user)

        # Remember me token should be deleted
        self.assertFalse(RememberToken.objects.get_by_string(value))

        # Create response
        response = HttpResponse("Test response")
        AuthRememberMiddleware().process_response(request, response)

        # The remember-me token should be changed
        token_string = response.cookies[COOKIE_NAME].value
        self.assertFalse(token_string == value)
        self.assertTrue(RememberToken.objects.get_by_string(token_string))

    def test_middleware_set_remember_token(self):
        from auth_remember import remember_user
        from auth_remember import settings
        from auth_remember.middleware import AuthRememberMiddleware

        request = self.factory.get('/')
        response = HttpResponse("Test response")

        # Do nothing (no cookies should be set)
        middleware = AuthRememberMiddleware()
        middleware.process_response(request, response)
        self.assertFalse(response.cookies)

        # Set remember user (sets the remember token)
        remember_user(request, self.user)
        middleware.process_response(request, response)
        self.assertTrue(response.cookies)
        cookie = response.cookies[settings.COOKIE_NAME]

        # Validate the remember token in the cookie
        user = auth.authenticate(token_string=cookie.value, request=request)
        self.assertEqual(self.user, user)
