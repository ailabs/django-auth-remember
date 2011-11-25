from django.contrib.auth import signals
from django.dispatch import receiver

from auth_remember import auth


class RememberMeMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            auth.login(request)
        request.user.is_fresh = request.session.get('REMEMBER_ME_FRESH', False)

    def process_response(self, request, response):
        remember_me = getattr(request, '_remember_me', {})

        if remember_me.get('token'):
            auth.set_cookie(response, remember_me['token'])

        if remember_me.get('delete'):
            auth.delete_cookie(response)

        return response

@receiver(signals.user_logged_in)
def set_user_is_fresh(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']

    user.is_fresh = not getattr(user, '_remember_user', False)
    request.session['REMEMBER_ME_FRESH'] = user.is_fresh


@receiver(signals.user_logged_out)
def remove_remember_me(sender, **kwargs):
    request = kwargs['request']
    request._remember_me = {'delete': True }
