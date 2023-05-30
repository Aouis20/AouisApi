from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


from Accounts.permissions import UserPermissions
from Categories.models import Category
from .serializers import ProductSerializer, CreateProductSerializer
from .models import Product


class ProductViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
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

        title = serialized_data.data.get("title")
        description = serialized_data.data.get("description")
        address_line1 = serialized_data.data.get("address_line1")
        address_line2 = serialized_data.data.get("address_line2")
        city = serialized_data.data.get("city")
        state = serialized_data.data.get("state")
        postal_code = serialized_data.data.get("postal_code")

        print(category)

        category = Category.objects.get(name=category)

        product = Product(
            category=category,
            user=request.user.username,
            title=title,
            description=description,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
        )

        product.save()

        return Response(ProductSerializer(product).data)
