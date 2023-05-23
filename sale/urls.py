from django.urls import path
from . import views 

urlpatterns=[
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/your-items',views.vendor_items,name='vendor-items'),
    path('home/', views.home, name='home'),
    path('item/add',views.AddItem.as_view(),name='add-item'),
    path('item/edit/<int:pk>/', views.EditItem.as_view(), name='edit-item'),
    path('item/delete/<int:pk>/', views.DeleteItem.as_view(), name='delete-item'),
    path('wallet/',views.wallet,name='wallet'),
    path('wallet/add-money/', views.AddMoney.as_view(), name='add-money'),
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
    path('item/review/<int:item_id>', views.leave_review, name='leave-review'),
    path('item/random/', views.random_item, name='random-item'),
]

