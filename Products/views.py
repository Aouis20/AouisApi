from django.core.files import File
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
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Accounts.models import User
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
    permission_classes = (IsAuthenticatedOrReadOnly(),)
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

    def get_permissions(self):
        permissions = {
            "default": self.permission_classes,
            "list_product": (AllowAny(),),
            "search_product": (AllowAny(),),
        }

        if self.action in permissions.keys():
            return permissions[self.action]
        else:
            return permissions["default"]

    @action(detail=False, methods=["post"], url_path="list-product")
    def list_product(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get("user_id")
        ids = serializer.validated_data.get("ids")

        productList = Product.objects.all()

        if user_id:
            productList = productList.filter(owner=user_id)

        if ids:
            productList = productList.filter(id__in=ids)

        paginator = ProductPagination()
        paginated_queryset = paginator.paginate_queryset(productList, request)

        serialized_data = ProductSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serialized_data.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_id = serializer.validated_data.get("category")
        title = serializer.validated_data.get("title")
        description = serializer.validated_data.get("description", None)
        price = serializer.validated_data.get("price")
        visibility = serializer.validated_data.get("visibility", True)
        is_service = serializer.validated_data.get("is_service", False)
        payment = serializer.validated_data.get("payment", None)
        status = serializer.validated_data.get("status", None)
        condition = serializer.validated_data.get("condition", None)
        images = serializer.validated_data.get("images")

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
                    is_service=is_service,
                    owner=owner,
                )
                if images:
                    for image in images:
                        product_image = ProductImage.objects.create(product=product, image=image)
                        product_image.save()

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

        filters = {key: value for key, value in filters.items() if value}

        if min_price > max_price:
            min_price, max_price = max_price, min_price

        productList = Product.objects.all()

        for filter_key, filter_value in filters.items():
            if filter_value is not None:
                print("filter value", filter_value)
                productList = productList.filter(**{filter_key: filter_value})

        if min_price:
            productList = productList.filter(price__gte=min_price)

        if max_price:
            productList = productList.filter(price__lte=max_price)

        paginator = ProductPagination()
        paginated_queryset = paginator.paginate_queryset(productList, request)

        serialized_data = ProductSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serialized_data.data)
