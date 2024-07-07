from django.contrib.auth.forms import UserCreationForm
from django import forms

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")


class UpdatePasswordForm(StyleFormMixin, forms.Form):
    email = forms.CharField()