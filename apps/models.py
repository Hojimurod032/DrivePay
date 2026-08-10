import uuid
from django.db import models


def generate_order_id():
    return f"DP-{uuid.uuid4().hex[:8].upper()}"


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    order_id = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=generate_order_id
    )
    items = models.ManyToManyField(Item)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stripe_session_id = models.CharField(
        max_length=255,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id