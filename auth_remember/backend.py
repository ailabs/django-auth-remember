from django.contrib.auth.models import User


class RememberBackend(object):
    def authenticate(self, remember_token=None):
        try:
            return User.objects.get(remember_me_tokens__token=remember_token)
        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
