from django.conf import settings

COOKIE_NAME = 'remember_token'
COOKIE_AGE = 86400 * 28  # 4 weeks by default
SESSION_KEY = 'AUTH_REMEMBER_FRESH'

for k in dir(settings):
    if k.startswith('REMEMBER_ME_'):
        locals()[k.split('REMEMBER_ME_', 1)[1]] = getattr(settings, k)
