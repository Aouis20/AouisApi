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

from .models import Product
from .serializers import (
    CreateProductSerializer,
    GetProductListSerializer,
    ProductSerializer,
)


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

        category = Category.objects.get(id=category_id)
        owner = User.objects.get(email=request.user)

        try:
            with transaction.atomic():
                product = Product(
                    title=title,
                    description=description,
                    price=price,
                    visibility=visibility,
                    condition=condition,
                    images=[
                        "https://cdn.pixabay.com/photo/2023/07/17/13/50/baby-snow-leopard-8132690_1280.jpg",
                        "https://cdn.pixabay.com/photo/2012/03/01/00/28/animal-19621_1280.jpg",
                        "https://cdn.pixabay.com/photo/2023/06/27/10/51/man-8091933_1280.jpg",
                    ],
                    category=category,
                    owner=owner,
                )

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
