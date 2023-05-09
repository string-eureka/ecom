from django.urls import path
from . import views as sale_views

urlpatterns=[
    path('dashboard', sale_views.dashboard, name='dashboard'),

]
