from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


from Accounts.permissions import UserPermissions
from Categories.models import Category
from Accounts.models import User
from .serializers import ProductSerializer, CreateProductSerializer
from .models import Product
from django.db import transaction
from rest_framework.exceptions import APIException, ValidationError


class ProductViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
    DestroyModelMixin,
):
    queryset = Category.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (UserPermissions,)

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
        description = serialized_data.data.get("description")

        category = Category.objects.get(id=category_id)
        user = User.objects.get(email=request.user)

        # Sur le front avoir un select qui permet de choisir sir on veux prendre son adresse ou non (TRUE or FALSe)

        try:
            with transaction.atomic():
                product = Product(
                    category=category,
                    user=user,
                    title=title,
                    description=description,
                    images=[
                        "https://cdn.pixabay.com/photo/2023/07/17/13/50/baby-snow-leopard-8132690_1280.jpg",
                        "https://cdn.pixabay.com/photo/2012/03/01/00/28/animal-19621_1280.jpg",
                        "https://cdn.pixabay.com/photo/2023/06/27/10/51/man-8091933_1280.jpg",
                    ],
                )
                product.save()

                return Response(ProductSerializer(product).data)

        except ValidationError as e:
            raise e
        except Exception as e:
            if isinstance(e, ValidationError):
                raise e
            print(e)
            raise APIException("Cannot create this Product")
