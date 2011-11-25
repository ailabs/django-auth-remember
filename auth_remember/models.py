import datetime

from django.db import models
from django.contrib.auth.models import User


class RememberToken(models.Model):
    token = models.CharField(max_length=32, blank=False, primary_key=True)

    created = models.DateTimeField(editable=False, blank=True,
        default=datetime.datetime.now)

    user = models.ForeignKey(User, related_name="remember_me_tokens")
