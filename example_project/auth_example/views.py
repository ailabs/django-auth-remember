from django.contrib import auth
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from auth_remember import remember_user

from example_project.auth_example.forms import LoginForm


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data

        user = auth.authenticate(
            username=data['username'], password=data['password'])

        if user:
            auth.login(request, user)
            if data['remember_me']:
                remember_user(request, user)
        else:
            form.add_non_field_error(_("Invalid username/password"))

    return TemplateResponse(request, 'login.html', {
        'form': form,
        'user': request.user
    })


def logout(request):
    auth.logout(request)
    return redirect('auth_login')
