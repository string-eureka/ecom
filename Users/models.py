from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ("CS", "Customer"),
        ("VN", "Vendor"),
    ]

    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default="CS")
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.PositiveBigIntegerField(
        null=True,
        validators=[
            MaxValueValidator(
                limit_value=9999999999,
                message="Phone Numbers must be atmost 10 digits long",
            )
        ],
    )
    address = models.CharField(max_length=255)
    balance = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, message="You must specify a positive amount"
            )
        ],
    )
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.username}]"


class CustomerUser(models.Model):
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, primary_key=True, related_name="customer"
    )

    def __str__(self):
        return f"[{self.user.username}]"


class VendorUser(models.Model):
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, primary_key=True, related_name="vendor"
    )

    def __str__(self):
        return f"[{self.user.username}]"
