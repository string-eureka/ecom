from django.contrib import admin
from .models import Item, Review
from import_export.admin import ExportActionMixin


class ItemAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "vendor",
        "item_title",
        "item_image",
        "item_price",
        "item_description",
        "item_stock",
        "item_orders",
        "item_discount",
    )


class ReviewAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("item", "owner", "audit", "rating")


admin.site.register(Item, ItemAdmin)
admin.site.register(Review, ReviewAdmin)
