from django.contrib import admin
from .models import Item,Cart,CartItem,Order

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
# Register your models here.
