from django.db import models
from django.conf import settings


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

    def __str__(self):
        return self.name


    

