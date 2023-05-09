from django.db import models
from Users.models import VendorUser

class Item(models.Model):
    vendor = models.ForeignKey(VendorUser, on_delete=models.CASCADE, related_name='items')
    # image = models.ImageField(upload_to='items')
    title = models.CharField(max_length=255,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    units_available = models.PositiveIntegerField()

    def __str__(self):
        return self.title
