from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    favorite_products = models.ManyToManyField(
        "products.Product", related_name="favorite_products", blank=True
    )
