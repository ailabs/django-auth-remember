from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=75)

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )

    remember_me = forms.BooleanField(label=_("Remember me"), required=False)

    def add_non_field_error(self, message):
        error_list = self.errors.setdefault(NON_FIELD_ERRORS, ErrorList())
        error_list.append(message)
