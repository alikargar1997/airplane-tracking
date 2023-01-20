from django.conf.urls import url

from . import views

app_name = "accounts"
urlpatterns = [
    url(r"^signup/$", views.SignUpView.as_view(), name="signup"),
    url(r"^signin/$", views.LoginView.as_view(), name="signin"),
    url(r"^signout/$", views.LogoutView.as_view(), name="signout"),
]
