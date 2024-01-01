from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views as user_views
from allauth.account.views import SignupView

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path(
        "accounts/google/enter/",
        auth_views.LoginView.as_view(template_name="Users/google_login.html"),
        name="google-login",
    ),
    path(
        "accounts/google/register/",
        SignupView.as_view(template_name="Users/google_register.html"),
        name="google-register",
    ),
    path("profile/complete/", user_views.complete_profile, name="complete-profile"),
    path("register/", user_views.registerone, name="role"),
    path("register/customer/", user_views.register, name="creg"),
    path("register/vendor/", user_views.register, name="vreg"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="Users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="Users/logout.html"),
        name="logout",
    ),
    path("login-redirect/", user_views.login_redirect, name="login-redirect"),
    path("profile/", user_views.profile, name="profile"),
    path("profile/edit/", user_views.edit_profile, name="edit-profile"),
]
