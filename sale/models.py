from django.db import models
from Users.models import VendorUser, CustomerUser
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator


class Item(models.Model):
    vendor = models.ForeignKey(VendorUser, on_delete=models.CASCADE, related_name='items')
    item_title = models.CharField(max_length=255)
    item_image = models.ImageField(upload_to='images')
    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(limit_value=0, message='You cannot pay to sell your product')])
    item_description = models.CharField(max_length=511)
    item_stock = models.PositiveSmallIntegerField(default=1)
    item_orders = models.PositiveSmallIntegerField(default=0)
    item_discount = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(limit_value=100, message='The maximum discount is 100%')])

    def __str__(self):
        return self.item_title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.item_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.item_image.path)


class Cart(models.Model):
    owner = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='carts')
    def calculate_bill(self):
        cart_items = self.cart_items.all()
        total_bill = sum(item.item.item_price * item.quantity for item in cart_items)
        return total_bill

    def __str__(self):
        return f"Cart #{self.pk} for {self.owner}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.item_title} in Cart #{self.cart.pk}"


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"
