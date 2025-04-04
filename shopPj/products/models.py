from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(
        default=0,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.name
