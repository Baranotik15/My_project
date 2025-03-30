from django.db import models
from django.conf import settings
from django.db.models import F, Sum
from products.models import Product


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "Pending", "Pending"
        COMPLETED = "Completed", "Completed"
        CANCELLED = "Cancelled", "Cancelled"

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
    updated_at = models.DateTimeField(auto_now=True)

    delivery_method = models.CharField(
        max_length=20,
        choices=[("Pickup", "Pickup"), ("Delivery", "Delivery")],
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ("credit_card", "Credit Card"),
            ("paypal", "PayPal"),
            ("in_cash", "In Cash"),
        ],
    )
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    pickup_address = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(
        max_length=100,
    )
    phone_number = models.CharField(
        max_length=20,
    )

    def get_total_price(self):
        annotated_order = (
            Order.objects.filter(id=self.id)
            .annotate(
                total_price=Sum(
                    F("order_items__quantity") * F("order_items__product__price")
                )
            )
            .first()
        )
        return annotated_order.total_price or 0

    @property
    def total_price(self):
        return self.get_total_price()

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return (f"{self.quantity} x "
                f"{self.product.name} in order {self.order.id}")
