from django.db import models
from django.conf import settings
from products.models import Product

# НЕ уверен не должна ли эта переходная таблица создаваться автоматически
class Cart(models.Model):
    # id
    # user_id
    pass


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
