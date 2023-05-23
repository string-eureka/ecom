from django.db import models
from Users.models import VendorUser, CustomerUser
from sale.models import Item

class Cart(models.Model):
    owner = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name='cart')
    
    @property
    def savings(self):
        cart_items = self.cart_items.all()
        total_savings = sum((item.item.item_price - item.item.selling_price) * item.quantity for item in cart_items)
        return total_savings
    
    @property
    def calculate_bill(self):
        cart_items = self.cart_items.all()
        total_bill = sum(item.item.selling_price * item.quantity for item in cart_items)
        return total_bill

    def __str__(self):
        return f"Cart #{self.pk} for {self.owner}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='fetch_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.item_title} in Cart #{self.cart.pk}"


class Order(models.Model):
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='orders')
    total_bill = models.DecimalField(max_digits=10, decimal_places=2)
    saving = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL,related_name='sold_items',null=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.quantity} x {self.item_title} in Order #{self.order.pk} for {self.order.customer}"
    

class Wishlist(models.Model):
    owner = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name='wishlists')
    items = models.ManyToManyField(Item, related_name='wishlist_items')

    def __str__(self):
        return f"Wishlist for {self.owner}"
