from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = "media/img/categories")
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Sub Categories"
    def __str__(self):
        return self.name
     
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
    file = models.ImageField(upload_to = "media/img/products")
    
    def __str__(self):
        return self.abbr
