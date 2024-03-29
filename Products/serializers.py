from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Accounts.models import User
from Accounts.serializers import UserSerializer
from Categories.models import Category
from Categories.serializers import CategorySerializer

from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = UserSerializer()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class GetProductListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    category_id = serializers.IntegerField(required=False)


class CreateProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255, allow_blank=True, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment = serializers.CharField(max_length=255, required=False)
    status = serializers.CharField(max_length=255, required=False)
    category = serializers.IntegerField(required=False)
    condition = serializers.CharField(max_length=255)
    is_service = serializers.BooleanField(default=False)
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    if (payment or price) and status == Product.ProductStatusEnum.TO_EXCHANGE:
        raise ValidationError("Unable to provide a payment method or price if the product is intended for exchange")

    def validate_price(self, price):
        if not price:
            raise ValidationError("Price is missing")

        decimal_price = Decimal(price)

        if decimal_price < 0.01:
            raise serializers.ValidationError("Price must be at least 0.01")

        if decimal_price % Decimal("0.01") != 0:
            raise serializers.ValidationError("Price must have a maximum of 2 digits after the decimal point")
        return price

    def validate_payment(self, payment):
        # Default payment type: Uniq
        if payment not in Product.PaymentTypeEnum.values:
            raise ValidationError("Payment type does not exists")

        return payment

    def validate_condition(self, condition):
        if condition not in Product.ConditionStatus.values:
            raise ValidationError("Condition type does not exists")

        return condition

    def validate_status(self, status):
        # Default status: FOR_SALE
        if status and status not in Product.ProductStatusEnum.values:
            raise ValidationError("Status type does not exists")
        return status


class SearchProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=True, required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    categories = serializers.ListField(child=serializers.IntegerField(), required=False)
    conditions = serializers.ListField(child=serializers.CharField(), required=False)
    localization = serializers.CharField(max_length=255, allow_blank=True, required=False)
