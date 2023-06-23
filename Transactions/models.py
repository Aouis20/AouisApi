from django.db import models
from Products.models import Product
from Accounts.models import User
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    class TransactionStatusEnum(models.TextChoices):
        PROCESSING = "PROCESSING", _("Processing")
        DONE = "DONE", _("DONE")

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255,
        choices=TransactionStatusEnum.choices,
        default=TransactionStatusEnum.PROCESSING,
    )
