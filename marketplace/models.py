from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=64)

    def __str__(self):
    	return self.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name
     

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default = 0.0)
    inStock = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name="items", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name="items", on_delete = models.CASCADE)
    image = models.ImageField(upload_to = "static/img", blank = True, null = True)

    def __str__(self):
        return self.name