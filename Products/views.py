import re

from django.db import transaction
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Accounts.models import User
from Accounts.permissions import UserPermissions
from AouisApi.pagination import ProductPagination
from Categories.models import Category

from .models import Product, ProductImage
from .serializers import CreateProductSerializer, GetProductListSerializer, ProductSerializer, SearchProductSerializer


class ProductViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = (UserPermissions,)
    pagination_class = ProductPagination

    def get_serializer_class(self):
        serializers = {
            "default": self.serializer_class,
            "list_product": GetProductListSerializer,
            "create": CreateProductSerializer,
            "search_product": SearchProductSerializer,
        }
        if self.action in serializers.keys():
            return serializers[self.action]
        else:
            return serializers["default"]

    @action(detail=False, methods=["post"], url_path="list-product")
    def list_product(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get("user_id")

        productList = Product.objects.all()

        if user_id:
            productList = productList.filter(owner=user_id)

        paginator = ProductPagination()
        paginated_queryset = paginator.paginate_queryset(productList, request)

        serialized_data = ProductSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serialized_data.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serialized_data = serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        category_id = serialized_data.data.get("category")
        title = serialized_data.data.get("title")
        description = serialized_data.data.get("description", None)
        price = serialized_data.data.get("price")
        visibility = serialized_data.data.get("visibility", True)
        payment = serialized_data.data.get("payment", None)
        status = serialized_data.data.get("status", None)
        condition = serialized_data.data.get("condition", None)
        uploaded_images = serialized_data.data.get("uploaded_images", [])

        category = Category.objects.get(id=category_id)
        owner = User.objects.get(email=request.user)

        try:
            with transaction.atomic():
                product = Product.objects.create(
                    title=title,
                    description=description,
                    price=price,
                    visibility=visibility,
                    condition=condition,
                    category=category,
                    owner=owner,
                )

                if len(uploaded_images):
                    for image in uploaded_images:
                        ProductImage.objects.create(product=product, image=image)

                if payment:
                    product.payment_type = payment

                if status:
                    product.status = status

                product.save()

                return Response(ProductSerializer(product).data)

        except ValidationError as e:
            raise e
        except Exception as e:
            if isinstance(e, ValidationError):
                raise e
            print(e)
            raise APIException("Cannot create this Product")

    @action(detail=False, methods=["post"], url_path="search")
    def search_product(self, request):
        serializer = self.get_serializer_class()
        serialized_data = serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        title = serialized_data.data.get("title")
        min_price = serialized_data.data.get("min_price", None)
        max_price = serialized_data.data.get("max_price", None)
        conditions = serialized_data.data.get("conditions")
        categories = serialized_data.data.get("categories")
        localization = serialized_data.data.get("localization")

        filters = {
            "title__icontains": title,
            "condition__in": conditions,
            "category__in": categories,
            "owner__postal_code__icontains": localization,
        }

        productList = Product.objects.all()

        for filter_key, filter_value in filters.items():
            if filter_value is not None:
                print("used", filter_key)
                productList = productList.filter(**{filter_key: filter_value})

        if min_price:
            if max_price:
                min_price = max_price if min_price > max_price else min_price
            print("min_price", min_price)
            productList = productList.filter(price__gte=min_price)

        if max_price:
            if min_price:
                max_price = min_price if min_price < max_price else max_price
            print("max_price", max_price)
            productList = productList.filter(price__lte=max_price)

        paginator = ProductPagination()
        paginated_queryset = paginator.paginate_queryset(productList, request)

        serialized_data = ProductSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serialized_data.data)
