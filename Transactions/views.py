from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .models import Transaction
from .serializers import TransactionSerializer, CreateTransactionSerializer
from Accounts.permissions import UserPermissions
from Accounts.models import User
from Products.models import Product

from rest_framework.exceptions import APIException
from rest_framework.response import Response


class TransactionViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (UserPermissions,)

    def get_serializer_class(self):
        serializers = {
            "default": self.serializer_class,
            "create": CreateTransactionSerializer,
        }
        if self.action in serializers.keys():
            return serializers[self.action]
        else:
            return serializers["default"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serialized_data = serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        product_id = serialized_data.data.get("product")
        buyer_id = serialized_data.data.get("buyer")

        product = Product.objects.get(id=product_id)
        buyer = User.objects.get(id=buyer_id)

        try:
            transaction = Transaction.objects.create(
                product=product,
                buyer=buyer,
            )

            return Response(TransactionSerializer(transaction).data)

        except Exception as e:
            print(e)
            raise APIException("Cannot create transaction")
