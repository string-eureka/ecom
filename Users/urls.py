from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views

urlpatterns = [
    path('home', user_views.home, name='home'),
    path('register', user_views.registerone, name='role'), 
    path('dashboard', user_views.dashboard, name='dashboard'),
    path('register/customer', user_views.register, name='creg'),
    path('register/vendor', user_views.register, name='vreg'),
    path('login/',auth_views.LoginView.as_view(template_name='Users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='Users/logout.html'),name='logout'),
    path('login-redirect/',user_views.login_redirect,name='login-redirect'),
    path('profile/', user_views.profile, name='profile'),

]
