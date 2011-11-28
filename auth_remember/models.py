import datetime

from django.db import models
from django.contrib.auth.models import User
from auth_remember.auth_utils import check_password


class RememberTokenManager(models.Manager):

    def get_by_string(self, token_string):
        """Return the token for the given token_string"""
        try:
            user_id, token_hash = token_string.split(':')
        except ValueError:
            return

        for token in self.filter(user=user_id):
            if check_password(token_hash, token.token_hash):
                return token


class RememberToken(models.Model):
    token_hash = models.CharField(max_length=60, blank=False, primary_key=True)

    created = models.DateTimeField(editable=False, blank=True,
        default=datetime.datetime.now)

    created_initial = models.DateTimeField(editable=False, blank=False)

    user = models.ForeignKey(User, related_name="remember_me_tokens")

    objects = RememberTokenManager()
