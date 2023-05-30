from django.db import models
from Categories.models import Category
from Accounts.models import User
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=255,
        choices=ProductStatusEnum.choices,
        default=ProductStatusEnum.FOR_SALE,
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

    def get_full_address(self):
        address_parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
        ]
        return ", ".join(filter(None, address_parts))