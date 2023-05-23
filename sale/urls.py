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
    path('item/review/<int:item_id>', views.leave_review, name='leave-review'),
    path('item/random/', views.random_item, name='random-item'),
]

