from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer, CreateProductSerializer

from Accounts.permissions import UserPermissions
from Accounts.models import User
from Categories.models import Category
from AouisApi.pagination import ProductPagination


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
            "create": CreateProductSerializer,
        }
        if self.action in serializers.keys():
            return serializers[self.action]
        else:
            return serializers["default"]

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
        user = User.objects.get(email=request.user)

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
                    user=user,
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
