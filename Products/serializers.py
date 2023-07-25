from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from decimal import Decimal

from .models import Product

from Categories.models import Category
from Categories.serializers import CategorySerializer
from Accounts.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()

    class Meta:
        model = Product
        fields = "__all__"


class CreateProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment = serializers.CharField(max_length=255, required=False)
    status = serializers.CharField(max_length=255, required=False)
    category = serializers.IntegerField()

    if (payment or price) and status == Product.ProductStatusEnum.TO_EXCHANGE:
        raise ValidationError(
            "Unable to provide a payment method or price if the product is intended for exchange"
        )

    def validate_price(self, price):
        if not price:
            raise ValidationError("Price is missing")
        
        decimal_price = Decimal(price)

        if decimal_price < 0.01:
            raise serializers.ValidationError("Price must be at least 0.01")

        if decimal_price % Decimal('0.01') != 0:
            raise serializers.ValidationError(
                "Price must have a maximum of 2 digits after the decimal point"
            )
        return price

    def validate_payment(self, payment):
        # Default payment type: Uniq
        if payment not in Product.PaymentTypeEnum.values:
            raise ValidationError("Payment type does not exists")

        return payment

    def validate_status(self, status):
        # Default status: FOR_SALE
        if status and status not in Product.ProductStatusEnum.values:
            raise ValidationError("Status type does not exists")
        return status

    def validate_category(self, category_id):
        if not Category.objects.filter(id=category_id):
            raise ValidationError("Category does not exists")

        return category_id
