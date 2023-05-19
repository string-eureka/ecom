from django.urls import path
from . import views as sale_views

urlpatterns=[
    path('dashboard/', sale_views.dashboard, name='dashboard'),
    path('dashboard/your-items',sale_views.vendor_items,name='vendor-items'),
    path('home/', sale_views.home, name='home'),
    path('add-item/',sale_views.AddItem.as_view(),name='add-item'),
    path('edit-item/<int:pk>/', sale_views.EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>/', sale_views.DeleteItem.as_view(), name='delete-item'),
    path('add-money/', sale_views.AddMoney.as_view(), name='add-money'),
    path('item/<int:item_id>/', sale_views.item_detail, name='item-detail'),

]
