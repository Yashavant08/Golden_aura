from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        constraints =[
            models.UniqueConstraint(fields= ['user','product'],name='unique_user_product_review')
        ]


    def __str__(self):
        return f"{self.product.name} - {self.user.username}"