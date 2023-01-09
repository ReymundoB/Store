from django.db import models

from products.models import Product

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    products = models.ManyToManyField(Product, blank=True)#Relacion muchos a muchos
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title