from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    archived_at = models.DateTimeField(default=None, null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, null=True)
    visibility = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)
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


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/", default="", null=True, blank=True)
