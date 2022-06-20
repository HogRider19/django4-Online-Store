from email.policy import default
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ImageField()
    count_sell = models.IntegerField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    discount = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


    

