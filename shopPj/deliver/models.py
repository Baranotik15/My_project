from django.db import models
from orders.models import Order
from django.utils import timezone


class Deliver(models.Model):
    class DeliverStatus(models.TextChoices):
        DELIVERED = "Delivered", "Delivered"
        UNDELIVERED = "Undelivered", "Undelivered"

    class DeliverMethod(models.TextChoices):
        COURIER = "Courier", "Courier"
        PICKUP = "Pickup", "Pickup"
        POSTAL_SERVICE = "Postal Service", "Postal Service"

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    deliver_method = models.CharField(
        max_length=15, choices=DeliverMethod.choices, default=DeliverMethod.COURIER
    )
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=DeliverStatus.choices,
        default=DeliverStatus.UNDELIVERED,
    )
    address = models.CharField(
        max_length=120,
    )
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Time of delivery completion",
    )

    def save(self, *args, **kwargs):
        if self.status == "Delivered" and not self.finish_time:
            self.finish_time = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Delivery for order {self.order.id}"
