from django.urls import path
from . import views as sale_views

urlpatterns=[
    path('dashboard/', sale_views.dashboard, name='dashboard'),
    path('dashboard/your-items',sale_views.vendor_items,name='vendor-items'),
    path('home/', sale_views.home, name='home'),
    path('add-item/',sale_views.AddItem.as_view(),name='add-item'),
]
