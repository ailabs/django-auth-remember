from django.contrib import auth
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorList
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from auth_remember.auth import remember_user
from example_project.auth_example.forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = auth.authenticate(
                username=data['username'], password=data['password'])

            if user:
                auth.login(request, user)
                if data['remember_me']:
                    remember_user(request, user)
            else:
                error_list = form.errors.setdefault(
                    NON_FIELD_ERRORS, ErrorList())
                error_list.append("Invalid username/password")
    else:
        form = LoginForm()

    return TemplateResponse(request, 'login.html', {
        'form': form,
        'user': request.user
    })


def logout(request):
    auth.logout(request)
    return redirect('auth_login')
