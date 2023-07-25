from django.db import models

# Create your models here.
from django.db import models
from Categories.models import Category
from Accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    class PaymentTypeEnum(models.TextChoices):
        UNIQ = "UNIQ", _("Uniq")
        PERMANENT = "PERMANENT", _("Permanent")

    class ProductStatusEnum(models.TextChoices):
        SOLD = "SOLD", _("Sold")
        FOR_SALE = "FOR_SALE", _("For sale")

        EXCHANGED = "EXCHANGED", _("Exchanged")
        TO_EXCHANGE = "TO_EXCHANGE", _("To exchange")

        REFUNDED = "REFUNDED", _("Refunded")
        TO_REFUNDED = "TO_REFUNDED", _("to_Refunded")

        RESERVED = "RESERVED", _("Reserved")
        PENDING_PAYMENT = "PENDING_PAYMENT", _("Pending_payment")
        NEGOTIATING = "NEGOTIATING", _("Negotiating")

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

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
