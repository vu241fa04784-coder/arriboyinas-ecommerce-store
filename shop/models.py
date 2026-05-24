from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    name = models.CharField(max_length=100)

    price = models.IntegerField()

    description = models.TextField()

    image = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product_name = models.CharField(max_length=200)

    price = models.IntegerField()

    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name