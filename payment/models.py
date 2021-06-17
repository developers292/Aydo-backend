from django.db import models
from orders.models import Order


class ZarinpalPaymentInfo(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payment_info'
    )
    RefID = models.CharField(max_length=255, null=True)
    Authority = models.CharField(max_length=255)
    status_code = models.IntegerField(null=True)
