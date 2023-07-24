from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Product
from Categories.models import Category
from Categories.serializers import CategorySerializer
from Accounts.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    # user = UserSerializer()

    class Meta:
        model = Product
        fields = "__all__"


class CreateProductSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()

    def validate_category(self, category_id):
        if not Category.objects.filter(id=category_id):
            raise ValidationError("Category does not exists")

        return category_id
