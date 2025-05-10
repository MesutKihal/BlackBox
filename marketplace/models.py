from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name="user_profile", on_delete = models.CASCADE)
    image = models.ImageField("img/profiles")
    role = models.CharField(max_length=64, default="normal")
    full_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user} Profile"
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to = "media/img/categories")
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.title

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default = 0.0)
    inStock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name="items", on_delete = models.CASCADE)
    rating = models.IntegerField(default=1)
    specification = models.JSONField(default=dict)
    stock_range = models.IntegerField(default=5)
    tag = models.CharField(default="New", max_length=16)

    def __str__(self):
        return self.name
        
class Item_image(models.Model):
    abbr = models.CharField(max_length=255)
    item = models.ForeignKey(Item, related_name="items_images", on_delete = models.CASCADE)
    file = models.ImageField(upload_to = "media/img/items")
    
    def __str__(self):
        return self.abbr

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, related_name="order_user", on_delete = models.CASCADE)
    item = models.ForeignKey(Item, related_name="order_item", on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    name = models.CharField(max_length=255, default="Empty")
    phone = models.CharField(max_length=255, default="XXX XXXX XXX")
    email = models.CharField(max_length=255, default="test@example.com")
    delivary = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.user} - ordered => {self.item} on {self.date}"
        
class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, related_name="request_user", on_delete=models.CASCADE)
    item_title = models.CharField(max_length=255)
    item_size = models.CharField(max_length=255)
    item_description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    client_fullname = models.CharField(max_length=255)
    client_phone_number = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    client_address = models.CharField(max_length=255)
    client_location = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} - {self.item_title} - {self.client_location}"
        
class RequestFile(models.Model):
    request = models.ForeignKey(Request, related_name="request_file", on_delete = models.CASCADE)
    file = models.FileField(upload_to="media/request_files/")
    
    def __str__(self):
        return self.request


class Review(models.Model):
    user = models.ForeignKey(User, related_name="review_user", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="review_item", on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    rating = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.user} review on {self.item} -> (rating: '{self.rating}', comment: {self.comment})"