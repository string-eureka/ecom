from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Wishlist
from import_export.admin import ExportActionMixin


class CartAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("owner", "savings", "calculate_bill")


class CartItemAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("cart", "item", "quantity")


class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("customer", "total_bill", "saving", "order_date")


class OrderItemAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("order", "item", "quantity", "item_price", "item_title")


class WishlistAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("owner",)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
