from django.core.validators import MinValueValidator

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

from Categories.models import Category


class Product(models.Model):
    class PaymentTypeEnum(models.TextChoices):
        UNIQ = "UNIQ", _("Uniq")
        WEEKLY = "WEEKLY", _("Weekly")
        MONTHLY = "MONTHLY", _("Monthly")
        YEARLY = "YEARLY", _("Yearly")

    class ProductStatusEnum(models.TextChoices):
        SOLD = "SOLD", _("Sold")
        FOR_SALE = "FOR_SALE", _("For sale")

        EXCHANGED = "EXCHANGED", _("Exchanged")
        TO_EXCHANGE = "TO_EXCHANGE", _("To exchange")

        REFUNDED = "REFUNDED", _("Refunded")
        PENDING_REFUND = "PENDING_REFUND", _("Pending_refund")

        RESERVED = "RESERVED", _("Reserved")
        PENDING_PAYMENT = "PENDING_PAYMENT", _("Pending_payment")
        NEGOTIATING = "NEGOTIATING", _("Negotiating")

    class ConditionStatus(models.TextChoices):
        MINT = "MINT", _("Mint")
        EXCELLENT = "EXCELLENT", _("EXCELLENT")
        GOOD = "GOOD", _("Good")
        FAIR = "FAIR", _("Fair")
        POOR = "POOR", _("Poor")

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True)
    visibility = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    payment_type = models.CharField(
        max_length=255,
        choices=PaymentTypeEnum.choices,
        default=PaymentTypeEnum.UNIQ,
    )
    images = models.JSONField(default=list)
    status = models.CharField(
        max_length=255,
        choices=ProductStatusEnum.choices,
        default=ProductStatusEnum.FOR_SALE,
    )
    condition = models.CharField(
        max_length=255,
        choices=ConditionStatus.choices,
    )

    category = models.ForeignKey("Categories.Category", on_delete=models.CASCADE)
    owner = models.ForeignKey("Accounts.User", on_delete=models.CASCADE)
