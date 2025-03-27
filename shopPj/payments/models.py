from django.db import models
from orders.models import Order


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        REJECTED = 'Rejected', 'Rejected'

    class PaymentMethod(models.TextChoices):
        CARD = 'Card', 'Card'
        PAYPAL = 'PayPal', 'PayPal'
        BANK_TRANSFER = 'Bank Transfer', 'Bank Transfer'
        CASH = 'Cash', 'Cash'

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    payment_method = models.CharField(
        max_length=15,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CARD,
    )
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    payment_date = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
