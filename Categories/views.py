from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .models import Category
from .serializers import CategorySerializer, CreateCategorySerializer
from Accounts.permissions import UserPermissions


class CategoryViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (UserPermissions,)

    def get_serializer_class(self):
        serializers = {
            "default": super().get_serializer_class(),
            "create": CreateCategorySerializer,
        }
        if self.action in serializers.keys():
            return serializers[self.action]
        else:
            return serializers["default"]
