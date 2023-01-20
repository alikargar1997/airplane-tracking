from abc import ABCMeta

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic import CreateView, FormView, View

from accounts import forms, models


class RedirectAuthenticationMixin(metaclass=ABCMeta):
    """Mixin for signin and login page to redirect if user is authenticated

    Args:
        metaclass ([type], optional): [description]. Defaults to ABCMeta.
    """

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse("tracking:list_tracking"))
        return super().get(*args, **kwargs)


class SignUpView(RedirectAuthenticationMixin, CreateView):
    """Signing Up view"""

    model = models.CustomUser
    template_name = "signup.html"
    form_class = forms.UserSignUpForm


class LoginView(RedirectAuthenticationMixin, FormView):
    """Login View to handle user login"""

    form_class = forms.LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse("tracking:list_tracking")


class LogoutView(LoginRequiredMixin, View):
    """User logout view"""

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(reverse("accounts:signin"))
