from django.core.management.base import BaseCommand

from auth_remember.models import RememberToken


class Command(BaseCommand):
    """Delete remember tokens older then AUTH_REMEMBER_COOKIE_AGE"""
    description = 'Delete remember tokens older then AUTH_REMEMBER_COOKIE_AGE'

    def handle(self, *args, **options):
        RememberToken.objects.clean_remember_tokens()
