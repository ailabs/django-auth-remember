from django.contrib import admin
from auth_remember import models


class RememberTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'serie_token', 'serie_created', 'token', 'created')
admin.site.register(models.RememberToken, RememberTokenAdmin)
