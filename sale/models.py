from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
from Users.models import VendorUser, CustomerUser
from decimal import Decimal
from django.db.models import Avg


class Item(models.Model):
    vendor = models.ForeignKey(VendorUser, on_delete=models.CASCADE, related_name='items')
    item_title = models.CharField(max_length=255)
    item_image = models.ImageField(upload_to='images')
    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=
                                     [MinValueValidator(limit_value=0, message='You cannot pay to sell your product')])
    item_description = models.CharField(max_length=511)
    item_stock = models.PositiveSmallIntegerField(default=1)
    item_orders = models.PositiveSmallIntegerField(default=0)
    item_discount = models.PositiveSmallIntegerField(default=0, validators=
                                                     [MaxValueValidator(limit_value=100, message='The maximum discount is 100%')])

    def __str__(self):
        return self.item_title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.item_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.item_image.path)
    
    @property
    def selling_price(self):
        return self.item_price - ((self.item_price * self.item_discount) / 100)
    
    @property
    def average_rating(self):
        avg_rating = self.item_reviews.aggregate(Avg('rating')).get('rating__avg')
        if avg_rating is not None:
            return Decimal(avg_rating).quantize(Decimal('0.00'))
        else:
            return None

    

    
class Review(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,related_name='item_reviews')
    owner=models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name='customer_reviews')
    rating=models.PositiveIntegerField(validators=[MinValueValidator(limit_value=1,message='The Mimimum rating is 1'),
                                                   MaxValueValidator(limit_value=5,message='The Maximum rating is 5 ')])
    audit = models.CharField(max_length=511)


    def __str__(self):
        return f"Review by {self.owner} on {self.item}"
    
    def average_rating(self):
        reviews = self.item_reviews.all()
        if reviews.exists():
            total_ratings = sum(review.rating for review in reviews)
            return total_ratings / reviews.count()
        else:
            return 0
    
