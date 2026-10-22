from django.db import models
from store.models import Product
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.product.name}"
