from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Product
from Categories.models import Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CreateProductSerializer(serializers.Serializer):
    category = serializers.CharField()
    address_line1 = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    postal_code = serializers.CharField()

    def validate_category(self, category):
        category = Category.objects.get(name=category)

        if not category:
            raise ValidationError("Category does not exists")

        return category
