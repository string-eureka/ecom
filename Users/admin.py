from django.contrib import admin
from .models import BaseUser, CustomerUser, VendorUser
from import_export.admin import ExportActionMixin


class BaseUserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "user_type",
        "name",
        "phone_number",
        "address",
        "balance",
        "profile_completed",
    )


class CustomerUserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("user",)


class VendorUserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("user",)


admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(VendorUser, VendorUserAdmin)
