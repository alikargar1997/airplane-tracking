from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from . import models


class UserSignUpForm(UserCreationForm):
    """Form for user signing up,inherited from django base UserCreationForm and changed some attributes

    Args:
        UserCreationForm ([object]): django base UserCreationForm
    """

    class Meta:
        model = models.CustomUser
        fields = ("username", "first_name", "last_name", "email", "phone_number")

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {"class": "form-row"}
        self.fields["username"].help_text = None
        self.fields["first_name"].widget.attrs = {"class": "form-row"}
        self.fields["last_name"].widget.attrs = {"class": "form-row"}
        self.fields["email"].widget.attrs = {"class": "form-row"}
        self.fields["password1"].widget.attrs = {"class": "form-row"}
        self.fields["password1"].help_text = None
        self.fields["password2"].widget.attrs = {"class": "form-row"}
        self.fields["password2"].help_text = None
        self.fields["phone_number"].widget.attrs = {"class": "form-row"}


class LoginForm(AuthenticationForm):
    """Form for login,inherited from django authenticationForm to change some attributes

    Args:
        AuthenticationForm ([object]): django base authentication form
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"autofocus": False})
