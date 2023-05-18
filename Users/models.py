from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.validators import MinValueValidator

class BaseUser(AbstractUser):

    USER_TYPE_CHOICES = [
        ('CS', 'Customer'),
        ('VN', 'Vendor'),
    ]

    user_type = models.CharField(max_length=2,choices=USER_TYPE_CHOICES,default='CS')
    name = models.CharField( max_length=100)
    phone_number = models.CharField(max_length=12)
    address = models.CharField( max_length=255)
    balance = models.DecimalField(default=0,max_digits=10, decimal_places=2,validators=[MinValueValidator(limit_value=0,message='You must specify a positive amount')])

    def __str__(self):  
        return f'[{self.username}]'

class CustomerUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True, related_name='customer')

    def __str__(self):  
        return f'[{self.user.username}]'

class VendorUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True, related_name='vendor')
    
    def __str__(self):  
        return f'[{self.user.username}]'


