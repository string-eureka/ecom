from django.contrib import admin
from .models import BaseUser,CustomerUser,VendorUser

admin.site.register(BaseUser)
admin.site.register(CustomerUser)
admin.site.register(VendorUser)


