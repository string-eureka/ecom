from django.urls import path
from . import views 

urlpatterns=[
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/your-items',views.vendor_items,name='vendor-items'),
    path('home/', views.home, name='home'),
    path('add-item/',views.AddItem.as_view(),name='add-item'),
    path('edit-item/<int:pk>/', views.EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>/', views.DeleteItem.as_view(), name='delete-item'),
    path('wallet/',views.wallet,name='wallet'),
    path('add-money/', views.AddMoney.as_view(), name='add-money'),
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
    path('your-cart/',views.cart_details,name='cart-details'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add-to-cart'),
    path('item/removed/<int:cart_item_id>/',views.remove_from_cart,name='removed-item'),
    path('create-order/', views.create_order, name='create-order'),
    path('order-details/<int:order_id>/', views.customer_order_details, name='customer-order-details'),
    path('order-history/', views.customer_order_history, name='customer-order-history'),
    path('vendor-order-history/', views.vendor_order_history, name='vendor-order-history'),
    path('vendor-order-details/<int:order_id>/', views.vendor_order_details, name='vendor-order-details'),
]

