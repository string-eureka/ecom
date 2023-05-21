from django.urls import path
from . import views as sale_views

urlpatterns=[
    path('dashboard/', sale_views.dashboard, name='dashboard'),
    path('dashboard/your-items',sale_views.vendor_items,name='vendor-items'),
    path('home/', sale_views.home, name='home'),
    path('add-item/',sale_views.AddItem.as_view(),name='add-item'),
    path('edit-item/<int:pk>/', sale_views.EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>/', sale_views.DeleteItem.as_view(), name='delete-item'),
    path('wallet/',sale_views.wallet,name='wallet'),
    path('add-money/', sale_views.AddMoney.as_view(), name='add-money'),
    path('item/<int:item_id>/', sale_views.item_detail, name='item-detail'),
    path('your-cart/',sale_views.cart_details,name='cart-details'),
    path('add-to-cart/<int:item_id>/', sale_views.add_to_cart, name='add-to-cart'),
    path('item/removed/<int:cart_item_id>/',sale_views.remove_from_cart,name='removed-item'),
    # path('order/create/', sale_views.create_order, name='create-order'),
    # path('order/<int:order_id>/', sale_views.order_details, name='order-details'),
    # path('order/history/', sale_views.order_history, name='order-history'),
    # path('vendor/order/<int:order_id>/', sale_views.vendor_order_details, name='vendor-order-details'),
    # path('vendor/order/history/', sale_views.vendor_order_history, name='vendor-order-history'),
]
