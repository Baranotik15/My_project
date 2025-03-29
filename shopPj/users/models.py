from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    favorite_products = models.ManyToManyField(
        'products.Product',
        related_name='favorite_products',
        blank=True
    )
