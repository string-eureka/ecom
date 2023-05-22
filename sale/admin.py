from django.contrib import admin
from .models import Item,Cart,CartItem,Order,OrderItem,Wishlist,Review

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Review)
# Register your models here.
