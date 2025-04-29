from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name="user_profile", on_delete = models.CASCADE)
    image = models.ImageField("media/img/profiles")
    full_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to = "img/categories")
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.title

class SubCategory(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(Category, related_name="subcategories", on_delete = models.CASCADE)
    class Meta:
        verbose_name_plural = "Sub Categories"
    def __str__(self):
        return self.title
     
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default = 0.0)
    inStock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(SubCategory, related_name="items", on_delete = models.CASCADE)

    def __str__(self):
        return self.name
        
class Item_image(models.Model):
    abbr = models.CharField(max_length=255)
    item = models.ForeignKey(Item, related_name="items_images", on_delete = models.CASCADE)
    file = models.ImageField(upload_to = "media/img/items")
    
    def __str__(self):
        return self.abbr

class Order(models.Model):
    user = models.ForeignKey(User, related_name="order_user", on_delete = models.CASCADE)
    item = models.ForeignKey(Item, related_name="order_item", on_delete = models.CASCADE)
    delivary = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user
        
class Request(models.Model):
    user = models.ForeignKey(User, related_name="request_user", on_delete = models.CASCADE)
    item_title = models.CharField(max_length=255, blank=False)
    item_size = models.CharField(max_length=255, blank=False)
    item_description = models.CharField(max_length=255, blank=False)
    client_fullname = models.CharField(max_length=255, blank=False)
    client_phone_number = models.CharField(max_length=255, blank=False)
    client_email = models.CharField(max_length=255, blank=False)
    client_address = models.CharField(max_length=255, blank=False)
    client_location = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return f"{self.user} - {self.item_title} - {self.client_location}"
        
class RequestFile(models.Model):
    request = models.ForeignKey(Request, related_name="request_file", on_delete = models.CASCADE)
    file = models.FileField(upload_to="media/request_files")
    
    def __str__(self):
        return self.order
