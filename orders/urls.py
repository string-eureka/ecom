from django.urls import path
from . import views 

urlpatterns=[
    path('cart/',views.cart_details,name='cart-details'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/delete/<int:cart_item_id>/',views.remove_from_cart,name='removed-item'),

    path('order/create/', views.create_order, name='create-order'),
    path('order/details/<int:order_id>/', views.customer_order_details, name='customer-order-details'),
    path('order/history/', views.customer_order_history, name='customer-order-history'),
    path('vendororder/history/', views.vendor_order_history, name='vendor-order-history'),
    path('vendororder/details/<int:order_id>/', views.vendor_order_details, name='vendor-order-details'),
    
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist/add/<int:item_id>',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/delete/<int:item_id>/',views.remove_from_wishlist,name='remove-from-wishlist'),
]