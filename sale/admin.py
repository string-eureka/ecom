from django.contrib import admin
from .models import Item,Cart,CartItem,Order,OrderItem

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
# Register your models here.
