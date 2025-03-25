from django.db import models
from django.conf import settings
from products.models import Product
from cart.models import CartItem


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return # Немного не понимаю как правильно написать тут общую цену

    def __str__(self):
        return f"Order {self.id} by {self.user}"


# Опять же вопрос, а можно ли как-то передать количество в
# сам ордер, чтобы пользоваться встроенной связующей таблицей Джанго и не писать эту
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()\

    def get_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"
