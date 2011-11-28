from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'auth_example.views.login', name='auth_login'),
    url(r'^logout$', 'auth_example.views.logout', name='auth_logout'),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),
)
